# scripts/test_recommendation.py
import os
import sys
import logging
import traceback

# Configurar logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.services.recomendacion import SistemaRecomendacion
from app.models.ingrediente import Ingrediente
from app.models.receta import Receta

def test_recommendation():
    """
    Realiza pruebas específicas en el sistema de recomendación
    """
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar si hay ingredientes en la base de datos
            ingredientes_count = Ingrediente.query.count()
            logger.info(f"Número de ingredientes en la base de datos: {ingredientes_count}")
            
            if ingredientes_count == 0:
                logger.error("No hay ingredientes en la base de datos")
                return
            
            # Verificar si hay recetas en la base de datos
            recetas_count = Receta.query.count()
            logger.info(f"Número de recetas en la base de datos: {recetas_count}")
            
            if recetas_count == 0:
                logger.error("No hay recetas en la base de datos")
                return
            
            # Obtener algunos ingredientes para probar
            ingredientes = Ingrediente.query.limit(3).all()
            ingredientes_ids = [ing.id for ing in ingredientes]
            ingredientes_nombres = [ing.nombre for ing in ingredientes]
            
            logger.info(f"Probando recomendación con ingredientes: {', '.join(ingredientes_nombres)}")
            
            # Crear instancia del sistema de recomendación
            sistema = SistemaRecomendacion()
            
            # Probar recomendación por ingredientes
            try:
                recomendaciones = sistema.recomendar_por_ingredientes(ingredientes=ingredientes_ids)
                
                if recomendaciones:
                    logger.info(f"Se encontraron {len(recomendaciones)} recomendaciones")
                    for i, rec in enumerate(recomendaciones[:2], 1):  # Mostrar solo las 2 primeras
                        logger.info(f"Recomendación {i}: {rec['nombre']}")
                else:
                    logger.warning("No se encontraron recomendaciones")
            except Exception as e:
                logger.error(f"Error al recomendar por ingredientes: {str(e)}")
                logger.error(traceback.format_exc())
            
            # Probar recomendación por texto
            try:
                texto_consulta = f"Receta con {ingredientes_nombres[0]} y {ingredientes_nombres[1]}"
                logger.info(f"Probando recomendación por texto: '{texto_consulta}'")
                
                recomendaciones = sistema.recomendar_por_texto(texto=texto_consulta)
                
                if recomendaciones:
                    logger.info(f"Se encontraron {len(recomendaciones)} recomendaciones")
                    for i, rec in enumerate(recomendaciones[:2], 1):  # Mostrar solo las 2 primeras
                        logger.info(f"Recomendación {i}: {rec['nombre']}")
                else:
                    logger.warning("No se encontraron recomendaciones por texto")
            except Exception as e:
                logger.error(f"Error al recomendar por texto: {str(e)}")
                logger.error(traceback.format_exc())
            
            # Probar recomendación de recetas similares
            if recetas_count > 0:
                try:
                    receta_id = Receta.query.first().id
                    logger.info(f"Probando recomendación de similares para receta ID {receta_id}")
                    
                    recomendaciones = sistema.recomendar_recetas_similares(receta_id)
                    
                    if recomendaciones:
                        logger.info(f"Se encontraron {len(recomendaciones)} recetas similares")
                        for i, rec in enumerate(recomendaciones[:2], 1):  # Mostrar solo las 2 primeras
                            logger.info(f"Similar {i}: {rec['nombre']}")
                    else:
                        logger.warning("No se encontraron recetas similares")
                except Exception as e:
                    logger.error(f"Error al recomendar recetas similares: {str(e)}")
                    logger.error(traceback.format_exc())
        except Exception as e:
            logger.error(f"Error general: {str(e)}")
            logger.error(traceback.format_exc())

if __name__ == '__main__':
    test_recommendation()