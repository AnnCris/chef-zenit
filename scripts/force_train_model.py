# scripts/force_train_model.py
import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.services.recomendacion import SistemaRecomendacion

def force_train():
    """
    Fuerza el reentrenamiento del modelo
    """
    app = create_app()
    
    with app.app_context():
        sistema = SistemaRecomendacion()
        
        # Eliminar modelo existente si hay
        model_path = os.path.join('ml_models', 'content_based_model.pkl')
        if os.path.exists(model_path):
            os.remove(model_path)
            logger.info(f"Modelo existente eliminado: {model_path}")
        
        # Entrenar modelo
        logger.info("Forzando el entrenamiento del modelo...")
        success = sistema.entrenar_modelo()
        
        if success:
            logger.info("Modelo entrenado correctamente")
        else:
            logger.error("Error al entrenar el modelo")

if __name__ == '__main__':
    force_train()