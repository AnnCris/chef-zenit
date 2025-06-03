from app.models.receta import Receta, RecetaIngrediente, RestriccionDietetica, receta_restricciones, Sustitucion
from app.models.ingrediente import Ingrediente
from app.models.usuario import PreferenciaUsuario
from app.services.nlp_service import NLPService
from app import db
from sqlalchemy import func, or_, and_, not_
import json
import logging
from app.models.receta import Receta, RecetaIngrediente, RestriccionDietetica, receta_restricciones, Sustitucion, receta_restricciones, Sustitucion

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MotorInferencia:
    """
    Motor de inferencia para el sistema experto de recomendación de recetas
    """
    
    def __init__(self):
        self.nlp_service = NLPService()
    
    def recomendar_recetas_por_ingredientes(self, ingredientes, preferencias=None, 
                                          max_resultados=5, incluir_similares=True):
        """
        Recomienda recetas basadas en los ingredientes disponibles
        
        Args:
            ingredientes: Lista de nombres de ingredientes o IDs
            preferencias: Objeto de preferencias de usuario (opcional)
            max_resultados: Número máximo de resultados a retornar
            incluir_similares: Incluir recetas que usan ingredientes similares
            
        Returns:
            Lista de recetas recomendadas
        """
        if not ingredientes:
            return []
        
        # Convertir los nombres de ingredientes a IDs si es necesario
        ingrediente_ids = []
        for ing in ingredientes:
            if isinstance(ing, int):
                ingrediente_ids.append(ing)
            else:
                # Buscar el ingrediente por nombre
                ingrediente = Ingrediente.query.filter(
                    func.lower(Ingrediente.nombre) == func.lower(ing)
                ).first()
                
                if ingrediente:
                    ingrediente_ids.append(ingrediente.id)
                else:
                    # Intentar buscar ingredientes similares
                    similar = Ingrediente.query.filter(
                        Ingrediente.nombre.ilike(f'%{ing}%')
                    ).first()
                    
                    if similar:
                        ingrediente_ids.append(similar.id)
        
        if not ingrediente_ids:
            return []
        
        # Cantidad de ingredientes proporcionados
        num_ingredientes = len(ingrediente_ids)
        
        # Subconsulta para contar cuántos ingredientes de la lista tiene cada receta
        subquery = db.session.query(
            RecetaIngrediente.receta_id,
            func.count(RecetaIngrediente.ingrediente_id).label('ingredientes_match')
        ).filter(
            RecetaIngrediente.ingrediente_id.in_(ingrediente_ids)
        ).group_by(
            RecetaIngrediente.receta_id
        ).subquery()
        
        # Consulta principal
        query = db.session.query(
            Receta, subquery.c.ingredientes_match
        ).join(
            subquery, Receta.id == subquery.c.receta_id
        )
        
        # Aplicar filtros de preferencias del usuario si existen
        if preferencias:
            # Filtrar alergias
            if preferencias.alergias and len(preferencias.alergias) > 0:
                # Subconsulta para identificar recetas con alérgenos
                recetas_con_alergenos = db.session.query(
                    RecetaIngrediente.receta_id
                ).join(
                    Ingrediente, RecetaIngrediente.ingrediente_id == Ingrediente.id
                ).filter(
                    Ingrediente.id.in_(preferencias.alergias)
                ).distinct().subquery()
                
                # Excluir recetas con alérgenos
                query = query.filter(~Receta.id.in_(recetas_con_alergenos))
            
            # Filtrar restricciones dietéticas
            if preferencias.restricciones_dieteticas and len(preferencias.restricciones_dieteticas) > 0:
                for restriccion_id in preferencias.restricciones_dieteticas:
                    recetas_compatibles = db.session.query(
                        Receta.id
                    ).join(
                        receta_restricciones, Receta.id == receta_restricciones.c.receta_id
                    ).filter(
                        receta_restricciones.c.restriccion_id == restriccion_id
                    ).subquery()
                    
                    query = query.filter(Receta.id.in_(recetas_compatibles))
            
            # Filtrar ingredientes evitados
            if preferencias.ingredientes_evitados and len(preferencias.ingredientes_evitados) > 0:
                recetas_con_evitados = db.session.query(
                    RecetaIngrediente.receta_id
                ).filter(
                    RecetaIngrediente.ingrediente_id.in_(preferencias.ingredientes_evitados),
                    RecetaIngrediente.es_opcional == False
                ).distinct().subquery()
                
                query = query.filter(~Receta.id.in_(recetas_con_evitados))
            
            # Dar prioridad a recetas con ingredientes favoritos
            if preferencias.ingredientes_favoritos and len(preferencias.ingredientes_favoritos) > 0:
                # Subconsulta para contar ingredientes favoritos en cada receta
                favoritos_subquery = db.session.query(
                    RecetaIngrediente.receta_id,
                    func.count(RecetaIngrediente.ingrediente_id).label('favoritos_count')
                ).filter(
                    RecetaIngrediente.ingrediente_id.in_(preferencias.ingredientes_favoritos)
                ).group_by(
                    RecetaIngrediente.receta_id
                ).subquery()
                
                # Unir con la consulta principal y ordenar por cantidad de favoritos
                query = query.outerjoin(
                    favoritos_subquery, Receta.id == favoritos_subquery.c.receta_id
                ).order_by(
                    func.coalesce(favoritos_subquery.c.favoritos_count, 0).desc()
                )
        
        # Ordenar por cantidad de ingredientes coincidentes (descendente)
        query = query.order_by(subquery.c.ingredientes_match.desc())
        
        # Si incluir_similares=False, solo incluir recetas que tengan al menos la mitad de ingredientes
        if not incluir_similares:
            min_ingredientes = max(num_ingredientes // 2, 1)
            query = query.filter(subquery.c.ingredientes_match >= min_ingredientes)
        
        # Limitar resultados
        query = query.limit(max_resultados)
        
        # Ejecutar consulta
        resultados = query.all()
        
        # Obtener recetas recomendadas
        recetas_recomendadas = []
        for receta, _ in resultados:
            # Obtener los ingredientes faltantes
            ingredientes_receta = [ri.ingrediente_id for ri in receta.ingredientes]
            faltantes = [ing_id for ing_id in ingredientes_receta if ing_id not in ingrediente_ids]
            
            # Obtener información de los ingredientes faltantes
            ingredientes_faltantes = []
            if faltantes:
                ing_info = Ingrediente.query.filter(Ingrediente.id.in_(faltantes)).all()
                ingredientes_faltantes = [ing.nombre for ing in ing_info]
            
            # Agregar diccionario con la información de la receta
            receta_dict = receta.to_dict_full()
            receta_dict['ingredientes_faltantes'] = ingredientes_faltantes
            recetas_recomendadas.append(receta_dict)
        
        return recetas_recomendadas
    
    def sugerir_sustitutos(self, ingrediente_id, tipo_sustitucion=None):
        """
        Sugiere sustitutos para un ingrediente dado
        """
        query = db.session.query(Ingrediente).join(
            Sustitucion, Sustitucion.ingrediente_sustituto_id == Ingrediente.id
        ).filter(
            Sustitucion.ingrediente_original_id == ingrediente_id
        )
        
        if tipo_sustitucion:
            query = query.filter(Sustitucion.tipo_sustitucion == tipo_sustitucion)
        
        sustitutos = query.all()
        return [ing.to_dict() for ing in sustitutos]
    
    def procesar_restricciones(self, texto):
        """
        Procesa un texto para identificar restricciones dietéticas
        """
        restricciones_str = self.nlp_service.extraer_restricciones(texto)
        
        # Mapear las restricciones extraídas a IDs de la base de datos
        restricciones = []
        
        for restriccion_str in restricciones_str:
            # Buscar por nombre similar
            restriccion = RestriccionDietetica.query.filter(
                RestriccionDietetica.nombre.ilike(f'%{restriccion_str}%')
            ).first()
            
            if restriccion:
                restricciones.append(restriccion.id)
        
        return restricciones
    
    def procesar_alergias(self, texto):
        """
        Procesa un texto para identificar alergias
        """
        alergias_str = self.nlp_service.extraer_alergias(texto)
        
        # Mapear las alergias extraídas a IDs de la base de datos
        alergias = []
        
        for alergia_str in alergias_str:
            # Definir términos de búsqueda según el tipo de alergia
            busqueda = None
            
            if alergia_str == 'lacteos':
                busqueda = ['leche', 'lácteo']
            elif alergia_str == 'gluten':
                busqueda = ['gluten', 'trigo']
            elif alergia_str == 'frutos_secos':
                busqueda = ['nuez', 'nueces', 'almendra']
            elif alergia_str == 'mariscos':
                busqueda = ['marisco', 'camarón']
            elif alergia_str == 'pescado':
                busqueda = ['pescado']
            elif alergia_str == 'huevo':
                busqueda = ['huevo']
            elif alergia_str == 'soja':
                busqueda = ['soja', 'soya']
            elif alergia_str == 'moluscos':
                busqueda = ['molusco', 'almeja']
            
            if busqueda:
                # Crear condiciones de búsqueda OR
                conditions = [Ingrediente.nombre.ilike(f'%{termino}%') for termino in busqueda]
                ingredientes = Ingrediente.query.filter(or_(*conditions)).all()
                
                for ing in ingredientes:
                    alergias.append(ing.id)
        
        return alergias
    
    def analizar_consulta(self, texto, session_id=None):
        """
        Analiza una consulta completa del usuario
        """
        resultado = self.nlp_service.analizar_consulta_usuario(texto)
        
        # Procesar restricciones y alergias
        restricciones_ids = self.procesar_restricciones(texto)
        alergias_ids = self.procesar_alergias(texto)
        
        # Guardar preferencias de usuario si tenemos session_id
        if session_id:
            PreferenciaUsuario.crear_o_actualizar(
                session_id=session_id,
                restricciones=restricciones_ids,
                alergias=alergias_ids
            )
        
        # Añadir información procesada
        resultado['restricciones_ids'] = restricciones_ids
        resultado['alergias_ids'] = alergias_ids
        
        return resultado
    
    def obtener_informacion_nutricional(self, receta_id):
        """
        Obtiene información nutricional detallada de una receta
        """
        receta = Receta.query.get(receta_id)
        if not receta:
            return None
            
        info_nutricional = {}
        
        # Información básica
        info_nutricional['calorias'] = receta.calorias
        info_nutricional['proteinas'] = receta.proteinas
        info_nutricional['carbohidratos'] = receta.carbohidratos
        info_nutricional['grasas'] = receta.grasas
        
        # Información detallada de vitaminas y minerales
        if receta.valor_nutricional:
            vn = receta.valor_nutricional
            info_nutricional['vitaminas'] = {
                'A': vn.vitamina_a,
                'C': vn.vitamina_c,
                'D': vn.vitamina_d,
                'E': vn.vitamina_e
            }
            
            info_nutricional['minerales'] = {
                'calcio': vn.calcio,
                'hierro': vn.hierro,
                'potasio': vn.potasio
            }
            
            if vn.otros_nutrientes:
                otros = vn.otros_nutrientes
                if isinstance(otros, str):
                    try:
                        otros = json.loads(otros)
                    except:
                        otros = {}
                        
                info_nutricional['otros'] = otros
        
        return info_nutricional