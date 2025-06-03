"""
Script para entrenar el modelo de recomendación basado en contenido
"""

import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Añadir directorio raíz al path para poder importar desde ml_models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def train_model():
    """
    Entrena el modelo de recomendación basado en contenido
    """
    try:
        from ml_models.content_based_filter import ContentBasedFilter
        
        logger.info("Iniciando entrenamiento del modelo de recomendación...")
        
        # Crear instancia del modelo
        model = ContentBasedFilter()
        
        # Entrenar modelo
        success = model.train()
        
        if success:
            logger.info("Modelo entrenado correctamente")
            
            # Evaluar modelo
            eval_results = model.evaluate()
            if eval_results:
                logger.info("Resultados de la evaluación:")
                logger.info(f"  - Precisión de categoría: {eval_results['precision_categoria']:.4f}")
                logger.info(f"  - Recall de ingredientes: {eval_results['recall_ingredientes']:.4f}")
        else:
            logger.error("Error al entrenar el modelo")
    
    except Exception as e:
        logger.error(f"Error al entrenar el modelo: {str(e)}")

if __name__ == '__main__':
    train_model()