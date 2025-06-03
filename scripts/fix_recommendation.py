# scripts/fix_recommendation.py
import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def fix_recommendation_service():
    """
    Reemplaza el método de recomendación por ingredientes por una versión simplificada
    """
    file_path = os.path.join('app', 'services', 'recomendacion.py')
    
    try:
        # Leer el contenido actual
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Nuevo método simplificado
        new_method = '''
    def recomendar_por_ingredientes(self, ingredientes, session_id=None, max_resultados=5):
        """
        Recomienda recetas basadas en los ingredientes disponibles (versión simplificada)
        """
        try:
            from app.models.receta import Receta, RecetaIngrediente
            from sqlalchemy.sql import func
            from app import db
            
            logger.info(f"Buscando recetas con ingredientes: {ingredientes}")
            
            # Contar cuántas recetas hay en total
            total_recetas = Receta.query.count()
            logger.info(f"Total de recetas en la base de datos: {total_recetas}")
            
            if total_recetas == 0:
                logger.warning("No hay recetas en la base de datos")
                return []
            
            # Si no hay ingredientes, devolver algunas recetas aleatorias
            if not ingredientes:
                logger.info("No se proporcionaron ingredientes, devolviendo recetas aleatorias")
                recetas = Receta.query.order_by(func.random()).limit(max_resultados).all()
                return [r.to_dict_full() for r in recetas]
            
            # Buscar recetas que tengan al menos uno de los ingredientes
            subquery = db.session.query(
                RecetaIngrediente.receta_id,
                func.count(RecetaIngrediente.ingrediente_id).label('count')
            ).filter(
                RecetaIngrediente.ingrediente_id.in_(ingredientes)
            ).group_by(
                RecetaIngrediente.receta_id
            ).subquery()
            
            query = db.session.query(Receta, subquery.c.count).join(
                subquery, Receta.id == subquery.c.receta_id
            ).order_by(
                subquery.c.count.desc()
            ).limit(max_resultados)
            
            results = query.all()
            logger.info(f"Encontradas {len(results)} recetas")
            
            if not results:
                logger.info("No se encontraron coincidencias, devolviendo recetas aleatorias")
                recetas = Receta.query.order_by(func.random()).limit(max_resultados).all()
                return [r.to_dict_full() for r in recetas]
            
            # Transformar resultados
            recetas_result = []
            for receta, count in results:
                receta_dict = receta.to_dict_full()
                
                # Calcular ingredientes faltantes
                ingredientes_receta = [ri.ingrediente_id for ri in receta.ingredientes]
                faltantes = [ing_id for ing_id in ingredientes_receta if ing_id not in ingredientes]
                
                # Obtener nombres de ingredientes faltantes
                from app.models.ingrediente import Ingrediente
                faltantes_info = []
                if faltantes:
                    ing_objs = Ingrediente.query.filter(Ingrediente.id.in_(faltantes)).all()
                    faltantes_info = [ing.nombre for ing in ing_objs]
                
                receta_dict['ingredientes_faltantes'] = faltantes_info
                recetas_result.append(receta_dict)
            
            return recetas_result
        
        except Exception as e:
            logger.error(f"Error en recomendación por ingredientes: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            
            # En caso de error, intentar devolver algunas recetas
            try:
                from app.models.receta import Receta
                recetas = Receta.query.limit(max_resultados).all()
                return [r.to_dict_full() for r in recetas]
            except:
                return []
'''
        
        # Reemplazar el método en el contenido
        import re
        pattern = r'def recomendar_por_ingredientes\(self.*?def'
        replacement = new_method + '\n    def'
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Escribir el nuevo contenido
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        logger.info("Método de recomendación por ingredientes reemplazado correctamente")
        return True
    except Exception as e:
        logger.error(f"Error al reemplazar el método: {str(e)}")
        return False

if __name__ == '__main__':
    fix_recommendation_service()