# scripts/check_model.py
import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_models.content_based_filter import ContentBasedFilter
from app import create_app
from app.models.receta import Receta

def check_model():
    """
    Verifica si el modelo está entrenado y proporciona información de diagnóstico
    """
    # Cargar el modelo
    model = ContentBasedFilter()
    model_loaded = model.load_model()
    
    logger.info(f"Estado del modelo: {'Cargado correctamente' if model_loaded else 'No se pudo cargar'}")
    
    # Verificar datos en la base de datos
    app = create_app()
    
    with app.app_context():
        # Contar recetas
        recetas_count = Receta.query.count()
        logger.info(f"Número de recetas en la base de datos: {recetas_count}")
        
        # Si hay recetas, mostrar algunos detalles
        if recetas_count > 0:
            recetas = Receta.query.limit(3).all()
            for receta in recetas:
                logger.info(f"Receta: {receta.nombre} (ID: {receta.id})")
                ingredientes = [ri.ingrediente.nombre for ri in receta.ingredientes if ri.ingrediente]
                logger.info(f"  Ingredientes: {', '.join(ingredientes)}")
        
        # Si el modelo está cargado, probar una recomendación
        if model_loaded and recetas_count > 0:
            receta_id = Receta.query.first().id
            recomendaciones = model.recommend(receta_id, top_n=3)
            
            if recomendaciones:
                logger.info(f"Recomendaciones para la receta ID {receta_id}:")
                for rec in recomendaciones:
                    logger.info(f"  - {rec['nombre']} (Similitud: {rec['similitud']:.4f})")
            else:
                logger.warning("No se pudieron obtener recomendaciones")

if __name__ == '__main__':
    check_model()