# app/services/recomendacion_mejorada.py

import os
import pickle
import logging
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sqlalchemy.sql import func
from app import db
from app.models.receta import Receta, RecetaIngrediente, HistoricoRecomendacion
from app.models.ingrediente import Ingrediente
from app.models.usuario import PreferenciaUsuario

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SistemaRecomendacionMejorado:
    """
    Sistema híbrido de recomendación que combina:
    1. Filtrado basado en contenido (TF-IDF)
    2. K-means para agrupación de recetas
    3. Random Forest para predicción de preferencias
    """
    
    def __init__(self):
        # Modelos y datos
        self.vectorizer_contenido = None
        self.matriz_tfidf = None
        self.kmeans_model = None
        self.random_forest_model = None
        self.scaler = None
        
        # Datos de recetas
        self.recetas_df = None
        self.matriz_ingredientes = None
        self.recetas_ids = []
        
        # Estado de entrenamiento
        self.modelo_entrenado = False
        
        # Directorio para guardar modelos
        self.models_dir = "ml_models"
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Intentar cargar modelos existentes
        self._cargar_modelos()
    
    def _cargar_modelos(self):
        """Carga modelos pre-entrenados si existen"""
        model_path = os.path.join(self.models_dir, "sistema_hibrido.pkl")
        
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    data = pickle.load(f)
                
                self.vectorizer_contenido = data.get('vectorizer_contenido')
                self.matriz_tfidf = data.get('matriz_tfidf')
                self.kmeans_model = data.get('kmeans_model')
                self.random_forest_model = data.get('random_forest_model')
                self.scaler = data.get('scaler')
                self.recetas_df = data.get('recetas_df')
                self.matriz_ingredientes = data.get('matriz_ingredientes')
                self.recetas_ids = data.get('recetas_ids', [])
                self.modelo_entrenado = True
                
                logger.info("Modelos cargados correctamente")
            except Exception as e:
                logger.error(f"Error al cargar modelos: {e}")
                self.modelo_entrenado = False
    
    def _guardar_modelos(self):
        """Guarda los modelos entrenados"""
        model_path = os.path.join(self.models_dir, "sistema_hibrido.pkl")
        
        try:
            data = {
                'vectorizer_contenido': self.vectorizer_contenido,
                'matriz_tfidf': self.matriz_tfidf,
                'kmeans_model': self.kmeans_model,
                'random_forest_model': self.random_forest_model,
                'scaler': self.scaler,
                'recetas_df': self.recetas_df,
                'matriz_ingredientes': self.matriz_ingredientes,
                'recetas_ids': self.recetas_ids
            }
            
            with open(model_path, 'wb') as f:
                pickle.dump(data, f)
            
            logger.info("Modelos guardados correctamente")
        except Exception as e:
            logger.error(f"Error al guardar modelos: {e}")
    
    def _preparar_datos(self):
        """Prepara los datos para entrenamiento"""
        try:
            # Obtener todas las recetas
            recetas = Receta.query.all()
            
            if len(recetas) < 5:
                logger.error("No hay suficientes recetas para entrenar")
                return False
            
            # Crear DataFrame con información de recetas
            recetas_data = []
            textos_contenido = []
            self.recetas_ids = []
            
            for receta in recetas:
                # Información básica
                receta_info = {
                    'id': receta.id,
                    'nombre': receta.nombre,
                    'categoria': receta.categoria or 'general',
                    'dificultad': receta.dificultad or 'media',
                    'tiempo_preparacion': receta.tiempo_preparacion or 30,
                    'porciones': receta.porciones or 4,
                    'calorias': receta.calorias or 300,
                    'proteinas': receta.proteinas or 15,
                    'carbohidratos': receta.carbohidratos or 40,
                    'grasas': receta.grasas or 10
                }
                
                # Texto para análisis de contenido
                ingredientes_nombres = [ri.ingrediente.nombre for ri in receta.ingredientes if ri.ingrediente]
                texto = f"{receta.nombre} {receta.descripcion or ''} {receta.categoria or ''} {' '.join(ingredientes_nombres)}"
                
                recetas_data.append(receta_info)
                textos_contenido.append(texto)
                self.recetas_ids.append(receta.id)
            
            self.recetas_df = pd.DataFrame(recetas_data)
            
            # Preparar matriz de ingredientes binaria
            self._crear_matriz_ingredientes()
            
            # Preparar textos para TF-IDF
            self.textos_contenido = textos_contenido
            
            logger.info(f"Datos preparados: {len(recetas)} recetas")
            return True
            
        except Exception as e:
            logger.error(f"Error al preparar datos: {e}")
            return False
    
    def _crear_matriz_ingredientes(self):
        """Crea matriz binaria de ingredientes por recetas"""
        try:
            # Obtener todos los ingredientes únicos
            ingredientes = Ingrediente.query.all()
            ingredientes_dict = {ing.id: idx for idx, ing in enumerate(ingredientes)}
            
            # Crear matriz binaria
            n_recetas = len(self.recetas_ids)
            n_ingredientes = len(ingredientes)
            
            matriz = np.zeros((n_recetas, n_ingredientes))
            
            for i, receta_id in enumerate(self.recetas_ids):
                receta = Receta.query.get(receta_id)
                for ri in receta.ingredientes:
                    if ri.ingrediente_id in ingredientes_dict:
                        j = ingredientes_dict[ri.ingrediente_id]
                        matriz[i, j] = 1
            
            self.matriz_ingredientes = matriz
            self.ingredientes_dict = ingredientes_dict
            
            logger.info(f"Matriz de ingredientes creada: {matriz.shape}")
            
        except Exception as e:
            logger.error(f"Error al crear matriz de ingredientes: {e}")
    
    def entrenar(self):
        """Entrena todos los modelos del sistema híbrido"""
        try:
            logger.info("Iniciando entrenamiento del sistema híbrido...")
            
            # Preparar datos
            if not self._preparar_datos():
                return False
            
            # 1. Entrenar modelo de contenido (TF-IDF)
            self._entrenar_modelo_contenido()
            
            # 2. Entrenar K-means
            self._entrenar_kmeans()
            
            # 3. Entrenar Random Forest
            self._entrenar_random_forest()
            
            # Marcar como entrenado
            self.modelo_entrenado = True
            
            # Guardar modelos
            self._guardar_modelos()
            
            logger.info("Sistema híbrido entrenado correctamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en entrenamiento: {e}")
            return False
    
    def _entrenar_modelo_contenido(self):
        """Entrena el modelo TF-IDF para filtrado basado en contenido"""
        try:
            # Crear vectorizador TF-IDF
            self.vectorizer_contenido = TfidfVectorizer(
                max_features=1000,
                stop_words=['de', 'la', 'y', 'el', 'en', 'los', 'del', 'las', 'un', 'por', 'con', 'para'],
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8
            )
            
            # Ajustar y transformar textos
            self.matriz_tfidf = self.vectorizer_contenido.fit_transform(self.textos_contenido)
            
            logger.info("Modelo de contenido TF-IDF entrenado")
            
        except Exception as e:
            logger.error(f"Error al entrenar modelo de contenido: {e}")
    
    def _entrenar_kmeans(self):
        """Entrena K-means para agrupación de recetas"""
        try:
            # Combinar características numéricas y matriz de ingredientes
            caracteristicas_numericas = self.recetas_df[['tiempo_preparacion', 'porciones', 'calorias', 'proteinas', 'carbohidratos', 'grasas']].values
            
            # Normalizar características numéricas
            self.scaler = StandardScaler()
            caracteristicas_norm = self.scaler.fit_transform(caracteristicas_numericas)
            
            # Combinar con matriz de ingredientes (reducida)
            if self.matriz_ingredientes.shape[1] > 50:
                # Si hay muchos ingredientes, usar solo los más comunes
                suma_ingredientes = self.matriz_ingredientes.sum(axis=0)
                indices_top = np.argsort(suma_ingredientes)[-50:]
                matriz_ingredientes_reducida = self.matriz_ingredientes[:, indices_top]
            else:
                matriz_ingredientes_reducida = self.matriz_ingredientes
            
            # Combinar características
            X = np.hstack([caracteristicas_norm, matriz_ingredientes_reducida])
            
            # Determinar número óptimo de clusters
            n_clusters = min(8, len(self.recetas_ids) // 3)
            n_clusters = max(3, n_clusters)
            
            # Entrenar K-means
            self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            self.clusters = self.kmeans_model.fit_predict(X)
            
            # Guardar matriz de características para uso posterior
            self.X_features = X
            
            logger.info(f"K-means entrenado con {n_clusters} clusters")
            
        except Exception as e:
            logger.error(f"Error al entrenar K-means: {e}")
    
    def _entrenar_random_forest(self):
        """Entrena Random Forest para predicción de preferencias"""
        try:
            # Crear datos de entrenamiento simulados basados en clusters
            # En una implementación real, usarías datos de preferencias del usuario
            
            X = self.X_features
            
            # Simular preferencias basadas en clusters y características
            y = []
            for i, cluster in enumerate(self.clusters):
                # Simular preferencias basadas en características de la receta
                receta_data = self.recetas_df.iloc[i]
                
                # Lógica simple para simular preferencias
                score = 0
                
                # Preferir recetas con tiempo moderado
                if 15 <= receta_data['tiempo_preparacion'] <= 45:
                    score += 1
                
                # Preferir recetas con calorías moderadas
                if 200 <= receta_data['calorias'] <= 500:
                    score += 1
                
                # Preferir ciertas categorías
                if receta_data['categoria'] in ['ensaladas', 'platos principales', 'sopas']:
                    score += 1
                
                # Convertir a clasificación binaria
                y.append(1 if score >= 2 else 0)
            
            # Entrenar Random Forest
            self.random_forest_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            self.random_forest_model.fit(X, y)
            
            logger.info("Random Forest entrenado")
            
        except Exception as e:
            logger.error(f"Error al entrenar Random Forest: {e}")
    
    def recomendar_hibrido(self, ingredientes=None, texto_consulta=None, receta_id=None, 
                          session_id=None, max_resultados=5):
        """
        Método principal que combina todos los enfoques para generar recomendaciones
        """
        try:
            if not self.modelo_entrenado:
                if not self.entrenar():
                    return self._recomendaciones_fallback(max_resultados)
            
            recomendaciones = []
            
            # 1. Recomendaciones por contenido (si hay texto o receta_id)
            if texto_consulta:
                recs_contenido = self._recomendar_por_contenido_texto(texto_consulta, max_resultados)
                recomendaciones.extend(recs_contenido)
            
            if receta_id:
                recs_similares = self._recomendar_por_contenido_receta(receta_id, max_resultados)
                recomendaciones.extend(recs_similares)
            
            # 2. Recomendaciones por K-means (si hay ingredientes)
            if ingredientes:
                recs_kmeans = self._recomendar_por_kmeans(ingredientes, max_resultados)
                recomendaciones.extend(recs_kmeans)
            
            # 3. Recomendaciones por Random Forest
            recs_rf = self._recomendar_por_random_forest(max_resultados)
            recomendaciones.extend(recs_rf)
            
            # Combinar y eliminar duplicados
            recomendaciones_unicas = self._combinar_recomendaciones(recomendaciones, max_resultados)
            
            # Convertir a formato final
            return self._formatear_recomendaciones(recomendaciones_unicas)
            
        except Exception as e:
            logger.error(f"Error en recomendación híbrida: {e}")
            return self._recomendaciones_fallback(max_resultados)
    
    def _recomendar_por_contenido_texto(self, texto, max_resultados):
        """Recomendaciones basadas en texto usando TF-IDF"""
        try:
            # Vectorizar texto de consulta
            vector_consulta = self.vectorizer_contenido.transform([texto])
            
            # Calcular similitudes
            similitudes = cosine_similarity(vector_consulta, self.matriz_tfidf)[0]
            
            # Obtener índices de mayor similitud
            indices_similares = np.argsort(similitudes)[::-1][:max_resultados]
            
            recomendaciones = []
            for idx in indices_similares:
                if similitudes[idx] > 0.1:  # Threshold mínimo
                    receta_id = self.recetas_ids[idx]
                    recomendaciones.append({
                        'receta_id': receta_id,
                        'score': float(similitudes[idx]),
                        'metodo': 'contenido_texto'
                    })
            
            return recomendaciones
            
        except Exception as e:
            logger.error(f"Error en recomendación por contenido: {e}")
            return []
    
    def _recomendar_por_contenido_receta(self, receta_id, max_resultados):
        """Recomendaciones basadas en similitud con una receta específica"""
        try:
            if receta_id not in self.recetas_ids:
                return []
            
            idx_receta = self.recetas_ids.index(receta_id)
            
            # Calcular similitudes
            similitudes = cosine_similarity(self.matriz_tfidf[idx_receta], self.matriz_tfidf)[0]
            
            # Obtener índices de mayor similitud (excluyendo la misma receta)
            indices_similares = np.argsort(similitudes)[::-1][1:max_resultados+1]
            
            recomendaciones = []
            for idx in indices_similares:
                if similitudes[idx] > 0.1:
                    rec_id = self.recetas_ids[idx]
                    recomendaciones.append({
                        'receta_id': rec_id,
                        'score': float(similitudes[idx]),
                        'metodo': 'contenido_receta'
                    })
            
            return recomendaciones
            
        except Exception as e:
            logger.error(f"Error en recomendación por receta similar: {e}")
            return []
    
    def _recomendar_por_kmeans(self, ingredientes, max_resultados):
        """Recomendaciones usando K-means"""
        try:
            # Crear vector de ingredientes del usuario
            vector_usuario = np.zeros(len(self.ingredientes_dict))
            
            for ingrediente in ingredientes:
                if isinstance(ingrediente, str):
                    # Buscar ingrediente por nombre
                    ing_obj = Ingrediente.query.filter_by(nombre=ingrediente).first()
                    if ing_obj and ing_obj.id in self.ingredientes_dict:
                        idx = self.ingredientes_dict[ing_obj.id]
                        vector_usuario[idx] = 1
                elif isinstance(ingrediente, int):
                    # Usar ID directamente
                    if ingrediente in self.ingredientes_dict:
                        idx = self.ingredientes_dict[ingrediente]
                        vector_usuario[idx] = 1
            
            # Crear características sintéticas para el usuario
            # (en una implementación real, estas vendrían de las preferencias del usuario)
            caracteristicas_usuario = np.array([[30, 4, 350, 20, 45, 12]])  # valores promedio
            caracteristicas_usuario_norm = self.scaler.transform(caracteristicas_usuario)
            
            # Reducir vector de ingredientes si es necesario
            if vector_usuario.shape[0] > 50:
                suma_ingredientes = self.matriz_ingredientes.sum(axis=0)
                indices_top = np.argsort(suma_ingredientes)[-50:]
                vector_usuario_reducido = vector_usuario[indices_top].reshape(1, -1)
            else:
                vector_usuario_reducido = vector_usuario.reshape(1, -1)
            
            # Combinar características
            X_usuario = np.hstack([caracteristicas_usuario_norm, vector_usuario_reducido])
            
            # Predecir cluster
            cluster_usuario = self.kmeans_model.predict(X_usuario)[0]
            
            # Obtener recetas del mismo cluster
            indices_cluster = np.where(self.clusters == cluster_usuario)[0]
            
            # Calcular distancias dentro del cluster
            distancias = []
            for idx in indices_cluster:
                X_receta = self.X_features[idx].reshape(1, -1)
                distancia = np.linalg.norm(X_usuario - X_receta)
                distancias.append((idx, distancia))
            
            # Ordenar por distancia y seleccionar mejores
            distancias.sort(key=lambda x: x[1])
            
            recomendaciones = []
            for idx, distancia in distancias[:max_resultados]:
                receta_id = self.recetas_ids[idx]
                score = 1.0 / (1.0 + distancia)  # Convertir distancia a score
                recomendaciones.append({
                    'receta_id': receta_id,
                    'score': float(score),
                    'metodo': 'kmeans'
                })
            
            return recomendaciones
            
        except Exception as e:
            logger.error(f"Error en recomendación por K-means: {e}")
            return []
    
    def _recomendar_por_random_forest(self, max_resultados):
        """Recomendaciones usando Random Forest"""
        try:
            # Predecir probabilidades para todas las recetas
            probabilidades = self.random_forest_model.predict_proba(self.X_features)
            
            # Obtener probabilidad de clase positiva (le gustará)
            prob_positiva = probabilidades[:, 1] if probabilidades.shape[1] > 1 else probabilidades[:, 0]
            
            # Obtener índices de mayor probabilidad
            indices_mejores = np.argsort(prob_positiva)[::-1][:max_resultados]
            
            recomendaciones = []
            for idx in indices_mejores:
                if prob_positiva[idx] > 0.3:  # Threshold mínimo
                    receta_id = self.recetas_ids[idx]
                    recomendaciones.append({
                        'receta_id': receta_id,
                        'score': float(prob_positiva[idx]),
                        'metodo': 'random_forest'
                    })
            
            return recomendaciones
            
        except Exception as e:
            logger.error(f"Error en recomendación por Random Forest: {e}")
            return []
    
    def _combinar_recomendaciones(self, todas_recomendaciones, max_resultados):
        """Combina y rankea recomendaciones de diferentes métodos"""
        try:
            # Diccionario para acumular scores por receta
            scores_combinados = {}
            
            # Pesos para cada método
            pesos = {
                'contenido_texto': 0.4,
                'contenido_receta': 0.4,
                'kmeans': 0.3,
                'random_forest': 0.3
            }
            
            for rec in todas_recomendaciones:
                receta_id = rec['receta_id']
                metodo = rec['metodo']
                score = rec['score']
                
                if receta_id not in scores_combinados:
                    scores_combinados[receta_id] = {
                        'score_total': 0,
                        'metodos': [],
                        'scores_individuales': {}
                    }
                
                # Aplicar peso del método
                peso = pesos.get(metodo, 0.2)
                score_ponderado = score * peso
                
                scores_combinados[receta_id]['score_total'] += score_ponderado
                scores_combinados[receta_id]['metodos'].append(metodo)
                scores_combinados[receta_id]['scores_individuales'][metodo] = score
            
            # Bonus por aparecer en múltiples métodos
            for receta_id, data in scores_combinados.items():
                num_metodos = len(set(data['metodos']))
                if num_metodos > 1:
                    data['score_total'] *= (1 + 0.2 * (num_metodos - 1))
            
            # Ordenar por score total
            recetas_ordenadas = sorted(
                scores_combinados.items(),
                key=lambda x: x[1]['score_total'],
                reverse=True
            )
            
            # Retornar top resultados
            return recetas_ordenadas[:max_resultados]
            
        except Exception as e:
            logger.error(f"Error al combinar recomendaciones: {e}")
            return []
    
    def _formatear_recomendaciones(self, recomendaciones_combinadas):
        """Convierte recomendaciones al formato final"""
        try:
            resultados = []
            
            for receta_id, data in recomendaciones_combinadas:
                receta = Receta.query.get(receta_id)
                if receta:
                    receta_dict = receta.to_dict_full()
                    receta_dict['score_recomendacion'] = data['score_total']
                    receta_dict['metodos_usados'] = list(set(data['metodos']))
                    receta_dict['ingredientes_faltantes'] = []
                    resultados.append(receta_dict)
            
            return resultados
            
        except Exception as e:
            logger.error(f"Error al formatear recomendaciones: {e}")
            return []
    
    def _recomendaciones_fallback(self, max_resultados):
        """Recomendaciones básicas cuando falla el sistema principal"""
        try:
            recetas = Receta.query.order_by(func.random()).limit(max_resultados).all()
            return [receta.to_dict_full() for receta in recetas]
        except:
            return []
    
    # Métodos de conveniencia para compatibilidad
    def recomendar_por_ingredientes(self, ingredientes, max_resultados=5):
        """Método de compatibilidad"""
        return self.recomendar_hibrido(ingredientes=ingredientes, max_resultados=max_resultados)
    
    def recomendar_por_texto(self, texto, max_resultados=5):
        """Método de compatibilidad"""
        return self.recomendar_hibrido(texto_consulta=texto, max_resultados=max_resultados)
    
    def recomendar_recetas_similares(self, receta_id, max_resultados=5):
        """Método de compatibilidad"""
        return self.recomendar_hibrido(receta_id=receta_id, max_resultados=max_resultados)


# Instancia global
sistema_recomendacion_mejorado = SistemaRecomendacionMejorado()