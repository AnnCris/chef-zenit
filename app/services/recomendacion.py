# app/services/sistema_recomendacion.py

import os
import pickle
import logging

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier

from sqlalchemy.sql import func
from app import db
from app.models.receta import Receta, RecetaIngrediente, HistoricoRecomendacion
from app.models.ingrediente import Ingrediente
from app.models.usuario import PreferenciaUsuario
from app.services.motor_inferencia import MotorInferencia

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SistemaRecomendacion:
    """
    Sistema de recomendación de recetas que combina:
      - Filtrado de contenido (TF-IDF sobre nombre, descripción, ingredientes, categoría, dificultad, restricciones)
      - Filtrado por ingredientes (conteo en base de datos)
      - KMeans sobre matriz binaria de ingredientes
      - Random Forest sobre la misma matriz binaria de ingredientes
    """

    def __init__(self):
        self.motor_inferencia = MotorInferencia()

        # Parámetros del modelo de contenido (TF-IDF)
        self.vectorizer = None
        self.recipe_vectors = None
        self.recipe_ids_cb = None  # IDs de recetas para content-based

        # Parámetros del modelo de KMeans / Random Forest
        self.kmeans_model = None
        self.rf_model = None
        self.binary_matrix = None  # Matriz binaria (recetas × ingredientes)
        self.recipe_ids_bin = None  # IDs de recetas para binarios

        # Flags de entrenamiento
        self.content_trained = False
        self.kmeans_trained = False
        self.rf_trained = False

        # Intentar cargar modelos pre-entrenados
        self._cargar_modelos_preentrenados()

    # ----------------------------
    # Métodos para persistir modelos
    # ----------------------------
    def _cargar_modelos_preentrenados(self):
        """
        Carga los modelos TF-IDF, KMeans y RandomForest si existen en disco,
        para evitar reentrenar cada vez.
        """
        base_dir = os.path.join(os.getcwd(), "ml_models")
        # 1) Modelo content-based
        path_cb = os.path.join(base_dir, "content_based_model.pkl")
        if os.path.exists(path_cb):
            try:
                with open(path_cb, "rb") as f:
                    data = pickle.load(f)
                    self.vectorizer = data["vectorizer"]
                    self.recipe_vectors = data["recipe_vectors"]
                    self.recipe_ids_cb = data["recipe_ids_cb"]
                    self.content_trained = True
                    logger.info("Modelo content-based cargado correctamente")
            except Exception as e:
                logger.error(f"No se pudo cargar modelo content-based: {e}")

        # 2) Modelo KMeans y RandomForest
        path_bin = os.path.join(base_dir, "bin_models.pkl")
        if os.path.exists(path_bin):
            try:
                with open(path_bin, "rb") as f:
                    data = pickle.load(f)
                    self.binary_matrix = data["binary_matrix"]
                    self.recipe_ids_bin = data["recipe_ids_bin"]
                    self.kmeans_model = data["kmeans_model"]
                    self.rf_model = data["rf_model"]
                    self.kmeans_trained = True
                    self.rf_trained = True
                    logger.info("Modelos KMeans y RandomForest cargados correctamente")
            except Exception as e:
                logger.error(f"No se pudo cargar modelos binarios: {e}")

    def _guardar_modelos(self):
        """
        Guarda los modelos entrenados en disco:
         - content_based_model.pkl     (vectorizer + recipe_vectors + recipe_ids_cb)
         - bin_models.pkl              (binary_matrix + recipe_ids_bin + kmeans_model + rf_model)
        """
        base_dir = os.path.join(os.getcwd(), "ml_models")
        os.makedirs(base_dir, exist_ok=True)

        # 1) Content-based
        if self.content_trained:
            path_cb = os.path.join(base_dir, "content_based_model.pkl")
            try:
                with open(path_cb, "wb") as f:
                    pickle.dump({
                        "vectorizer": self.vectorizer,
                        "recipe_vectors": self.recipe_vectors,
                        "recipe_ids_cb": self.recipe_ids_cb
                    }, f)
                logger.info("Modelo content-based guardado en disco")
            except Exception as e:
                logger.error(f"Error guardando content-based model: {e}")

        # 2) KMeans + RandomForest
        if self.kmeans_trained and self.rf_trained:
            path_bin = os.path.join(base_dir, "bin_models.pkl")
            try:
                with open(path_bin, "wb") as f:
                    pickle.dump({
                        "binary_matrix": self.binary_matrix,
                        "recipe_ids_bin": self.recipe_ids_bin,
                        "kmeans_model": self.kmeans_model,
                        "rf_model": self.rf_model
                    }, f)
                logger.info("Modelos KMeans y RandomForest guardados en disco")
            except Exception as e:
                logger.error(f"Error guardando bin_models: {e}")

    # ----------------------------
    # 1) FILTRADO DE CONTENIDO (TF-IDF)
    # ----------------------------
    def entrenar_content_based(self):
        """
        Entrena el modelo content-based usando TF-IDF sobre:
          - Nombre de la receta
          - Descripción
          - Ingredientes (concatenados)
          - Categoría
          - Dificultad
          - Restricciones dietéticas
        """
        try:
            recetas = Receta.query.all()
            if not recetas:
                logger.warning("No hay recetas para entrenar content-based")
                return False

            textos = []
            ids = []
            for receta in recetas:
                # Ingredientes: lista de nombres
                ingredientes = [ri.ingrediente.nombre for ri in receta.ingredientes if ri.ingrediente]
                ingredientes_text = " ".join(ingredientes)

                # Categoría y dificultad (si existen)
                categorias_text = receta.categoria or ""
                dificultad_text = receta.dificultad or ""

                # Restricciones dietéticas (si existen)
                restricciones = [r.nombre for r in receta.restricciones] if hasattr(receta, "restricciones") else []
                restricciones_text = " ".join(restricciones)

                # Mezclar todo en un solo texto
                texto = " ".join([
                    receta.nombre or "",
                    receta.descripcion or "",
                    ingredientes_text,
                    categorias_text,
                    dificultad_text,
                    restricciones_text
                ])
                textos.append(texto)
                ids.append(receta.id)

            # Crear y entrenar vectorizador
            self.vectorizer = TfidfVectorizer(
                analyzer="word",
                ngram_range=(1, 2),
                min_df=0.01,
                max_df=0.9,
                stop_words=["de","la","y","el","en","los","del","las","un","por","con","para"]
            )
            self.recipe_vectors = self.vectorizer.fit_transform(textos)
            self.recipe_ids_cb = ids
            self.content_trained = True

            # Guardar en disco
            self._guardar_modelos()
            logger.info(f"Content-based entrenado con {len(ids)} recetas")
            return True

        except Exception as e:
            logger.error(f"Error entrenando content-based: {e}")
            return False

    def recomendar_content_based(self, receta_id, max_resultados=5):
        """
        Dado un receta_id, devuelve hasta max_resultados recetas similares
        basadas en similitud coseno sobre los vectores TF-IDF.
        """
        if not self.content_trained:
            exito = self.entrenar_content_based()
            if not exito:
                return []

        try:
            if receta_id not in self.recipe_ids_cb:
                logger.warning(f"Receta ID {receta_id} no está en el modelo TF-IDF")
                return []

            idx = self.recipe_ids_cb.index(receta_id)
            sims = cosine_similarity(self.recipe_vectors[idx], self.recipe_vectors)[0]
            # Obtenemos índices ordenados de mayor a menor similitud, excepto la propia receta
            top_idxs = sims.argsort()[::-1][1: max_resultados+1]

            resultados = []
            for i in top_idxs:
                rid = self.recipe_ids_cb[i]
                receta = Receta.query.get(rid)
                if receta:
                    resultados.append(receta.to_dict_full())
            return resultados

        except Exception as e:
            logger.error(f"Error en recomendar_content_based: {e}")
            return []

    # ----------------------------
    # 2) FILTRADO POR INGREDIENTES (conteo directo)
    # ----------------------------
    def recomendar_por_ingredientes(self, ingredientes_ids, max_resultados=5):
        """
        Recomienda recetas basadas en una lista de ingredient IDs (conteo directo).
        Si no encuentra suficiente cantidad, cae a KMeans y luego a RandomForest.
        """
        try:
            total = Receta.query.count()
            if total == 0:
                logger.warning("No hay recetas en la base de datos")
                return []

            # Si no se pasaron ingredientes, devolvemos random
            if not ingredientes_ids:
                recetas = Receta.query.order_by(func.random()).limit(max_resultados).all()
                return [r.to_dict_full() for r in recetas]

            # 1) Contar coincidencias directas en RecetaIngrediente
            subq = db.session.query(
                RecetaIngrediente.receta_id,
                func.count(RecetaIngrediente.ingrediente_id).label("cnt")
            ).filter(
                RecetaIngrediente.ingrediente_id.in_(ingredientes_ids)
            ).group_by(
                RecetaIngrediente.receta_id
            ).subquery()

            query = db.session.query(Receta, subq.c.cnt)\
                              .join(subq, Receta.id == subq.c.receta_id)\
                              .order_by(subq.c.cnt.desc())\
                              .limit(max_resultados)

            results = query.all()
            if results:
                logger.info(f"Filtrado directo encontró {len(results)} recetas")
                out = []
                for receta, cnt in results:
                    rec_d = receta.to_dict_full()
                    # Calcular IDs de ingredientes faltantes
                    ings_rec = [ri.ingrediente_id for ri in receta.ingredientes]
                    faltantes = [iid for iid in ings_rec if iid not in ingredientes_ids]
                    # Obtener nombres de faltantes
                    faltantes_nombres = []
                    if faltantes:
                        falt_objs = Ingrediente.query.filter(Ingrediente.id.in_(faltantes)).all()
                        faltantes_nombres = [f.nombre for f in falt_objs]
                    rec_d["ingredientes_faltantes"] = faltantes_nombres
                    out.append(rec_d)
                return out

            # 2) Si no hubo coincidencias directas, caer a KMeans
            return self._recomendar_por_kmeans(ingredientes_ids, max_resultados)

        except Exception as e:
            logger.error(f"Error en recomendar_por_ingredientes: {e}")
            logger.error(__import__("traceback").format_exc())
            # Como último recurso, devolver algunas recetas random
            fallback = Receta.query.limit(max_resultados).all()
            return [r.to_dict_full() for r in fallback]

    # ----------------------------
    # 3) KMEANS SOBRE MATRIZ BINARIA DE INGREDIENTES
    # ----------------------------
    def _construir_matriz_binaria(self):
        """
        Crea la matriz binaria (n_recetas × n_ingredientes)
        """
        recetas = Receta.query.all()
        if not recetas:
            return False

        # Obtener todos los ingredientes activos para asignar columnas
        todos_ings = Ingrediente.query.all()
        ing_ids = [ing.id for ing in todos_ings]
        ing_idx_map = {ing_id: idx for idx, ing_id in enumerate(ing_ids)}

        n_recetas = len(recetas)
        n_ings = len(ing_ids)

        # Inicializar matriz de ceros
        mat = np.zeros((n_recetas, n_ings), dtype=int)
        receta_ids = []
        for i, receta in enumerate(recetas):
            receta_ids.append(receta.id)
            for ri in receta.ingredientes:
                if ri.ingrediente_id in ing_idx_map:
                    mat[i, ing_idx_map[ri.ingrediente_id]] = 1

        # Guardar estado
        self.binary_matrix = mat
        self.recipe_ids_bin = receta_ids
        self.ingredient_idx_map = ing_idx_map  # para referencia posterior
        return True

    def entrenar_kmeans_rf(self, n_clusters=5):
        """
        Entrena KMeans y RandomForest sobre la misma matriz binaria de ingredientes
        """
        if not self._construir_matriz_binaria():
            logger.warning("No se pudo construir matriz binaria para KMeans/RF")
            return False

        # 1) Entrenar KMeans
        self.kmeans_model = KMeans(n_clusters=min(n_clusters, self.binary_matrix.shape[0]), random_state=0)
        self.kmeans_model.fit(self.binary_matrix)
        self.kmeans_trained = True

        # 2) Entrenar RandomForest para predecir clusters
        self.rf_model = RandomForestClassifier(n_estimators=50, random_state=0)
        clusters = self.kmeans_model.labels_
        self.rf_model.fit(self.binary_matrix, clusters)
        self.rf_trained = True

        # Guardar en disco
        self._guardar_modelos()
        logger.info("KMeans y RandomForest entrenados sobre matriz binaria")
        return True

    def _recomendar_por_kmeans(self, ingredientes_ids, max_resultados=5):
        """
        Usa KMeans para recomendar: 
        - Construye vector binario del usuario (sobre las mismas columnas de ingrediente)
        - Predice a qué clúster pertenece
        - Devuelve las recetas de ese clúster ordenadas aleatoriamente o por proximidad
        """
        if not self.kmeans_trained:
            exito = self.entrenar_kmeans_rf()
            if not exito:
                return []

        # Crear vector binario del usuario
        user_vec = np.zeros((len(self.ingredient_idx_map),), dtype=int)
        for iid in ingredientes_ids:
            if iid in self.ingredient_idx_map:
                user_vec[self.ingredient_idx_map[iid]] = 1
        user_vec = user_vec.reshape(1, -1)

        try:
            # Predicción de clúster
            clust = self.kmeans_model.predict(user_vec)[0]
            # Filtrar recetas en ese clúster
            mask = (self.kmeans_model.labels_ == clust)
            recetas_en_cluster = np.array(self.recipe_ids_bin)[mask]

            # Si hay muchas, tomar max_resultados aleatoriamente
            if len(recetas_en_cluster) > max_resultados:
                chosen = np.random.choice(recetas_en_cluster, size=max_resultados, replace=False)
            else:
                chosen = recetas_en_cluster

            # Devolverlas
            out = []
            for rid in chosen:
                receta = Receta.query.get(int(rid))
                if receta:
                    out.append(receta.to_dict_full())
            if out:
                logger.info(f"KMeans devolvió {len(out)} recetas")
                return out

        except Exception as e:
            logger.error(f"Error en recomendar_por_kmeans: {e}")

        # Si falla o no hay recetas, caer a RandomForest
        return self._recomendar_por_randomforest(ingredientes_ids, max_resultados)

    # ----------------------------
    # 4) RANDOM FOREST SOBRE MATRIZ BINARIA
    # ----------------------------
    def _recomendar_por_randomforest(self, ingredientes_ids, max_resultados=5):
        """
        Usa RandomForest para predecir el clúster de la receta que mejor coincide con el perfil,
        luego devuelve recetas de ese clúster.
        """
        if not self.rf_trained:
            exito = self.entrenar_kmeans_rf()
            if not exito:
                return []

        # Vector binario del usuario
        user_vec = np.zeros((len(self.ingredient_idx_map),), dtype=int)
        for iid in ingredientes_ids:
            if iid in self.ingredient_idx_map:
                user_vec[self.ingredient_idx_map[iid]] = 1
        user_vec = user_vec.reshape(1, -1)

        try:
            # Predecir clúster
            pred_clust = self.rf_model.predict(user_vec)[0]
            # Filtrar recetas de ese clúster
            mask = (self.kmeans_model.labels_ == pred_clust)
            recetas_en_cluster = np.array(self.recipe_ids_bin)[mask]

            # Si hay muchas, tomar max_resultados aleatoriamente
            if len(recetas_en_cluster) > max_resultados:
                chosen = np.random.choice(recetas_en_cluster, size=max_resultados, replace=False)
            else:
                chosen = recetas_en_cluster

            out = []
            for rid in chosen:
                receta = Receta.query.get(int(rid))
                if receta:
                    out.append(receta.to_dict_full())
            logger.info(f"RandomForest devolvió {len(out)} recetas")
            return out

        except Exception as e:
            logger.error(f"Error en recomendar_por_randomforest: {e}")

        # Si todo falla, devolver lista vacía
        return []

    # ----------------------------
    # 5) RECOMENDACIÓN POR TEXTO (search + motor de inferencia)
    # ----------------------------
    def recomendar_por_texto(self, texto, session_id=None, max_resultados=5):
        """
        1) Analiza con el Motor de Inferencia la consulta → extrae ingredientes, restricciones, etc.
        2) Si hay ingredientes en la consulta, llama a recomendar_por_ingredientes()
        3) Si no hay, usa búsqueda por texto en nombre/descripción/categoría
        """
        try:
            analisis = self.motor_inferencia.analizar_consulta(texto, session_id)
            preferencias = None
            if session_id:
                preferencias = PreferenciaUsuario.obtener_por_session(session_id)

            if analisis["ingredientes"]:
                ingredientes_ids = analisis["ingredientes"]
                recetas = self.recomendar_por_ingredientes(ingredientes_ids, max_resultados)
                # Registrar en histórico si hay session_id
                if session_id and recetas:
                    for rec in recetas:
                        self.registrar_recomendacion(session_id, rec["id"])
                return recetas

            # Si no hay ingredientes extraídos, buscar por palabras clave
            palabras = [p for p in texto.lower().split() if len(p) > 2]
            if not palabras:
                return []

            condiciones = []
            for p in palabras:
                condiciones.append(Receta.nombre.ilike(f"%{p}%"))
                condiciones.append(Receta.descripcion.ilike(f"%{p}%"))
                condiciones.append(Receta.categoria.ilike(f"%{p}%"))

            recetas_objs = Receta.query.filter(func.or_(*condiciones)).distinct().limit(max_resultados).all()
            return [r.to_dict_full() for r in recetas_objs]

        except Exception as e:
            logger.error(f"Error en recomendar_por_texto: {e}")
            logger.error(__import__("traceback").format_exc())
            return []

    # ----------------------------
    # 6) HISTÓRICO Y FEEDBACK
    # ----------------------------
    def registrar_recomendacion(self, session_id, receta_id):
        """
        Registra una nueva fila en HistoricoRecomendacion para trackear la recomendación
        """
        try:
            hist = HistoricoRecomendacion(session_id=session_id, receta_id=receta_id)
            db.session.add(hist)
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error registrando recomendación: {e}")
            db.session.rollback()
            return False

    def registrar_feedback(self, historico_id, feedback):
        """
        Actualiza el feedback (like/dislike, comentario, etc.) en HistoricoRecomendacion
        """
        try:
            hist = HistoricoRecomendacion.query.get(historico_id)
            if hist:
                hist.feedback = feedback
                db.session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error registrando feedback: {e}")
            db.session.rollback()
            return False

    # ----------------------------
    # 7) MÉTODOS AUXILIARES
    # ----------------------------
    def obtener_sustitutos(self, ingrediente_id, tipo_sustitucion=None):
        """
        Delegar al MotorInferencia para sugerir sustitutos de un ingrediente
        """
        return self.motor_inferencia.sugerir_sustitutos(ingrediente_id, tipo_sustitucion)

    def obtener_informacion_nutricional(self, receta_id):
        """
        Delegar al MotorInferencia para traer info nutricional de la receta
        """
        return self.motor_inferencia.obtener_informacion_nutricional(receta_id)

    def actualizar_preferencias_usuario(self, session_id, restricciones=None, alergias=None,
                                        favoritos=None, evitados=None):
        """
        Delegar a PreferenciaUsuario para crear o actualizar las preferencias del usuario
        """
        return PreferenciaUsuario.crear_o_actualizar(
            session_id=session_id,
            restricciones=restricciones,
            alergias=alergias,
            favoritos=favoritos,
            evitados=evitados
        )
