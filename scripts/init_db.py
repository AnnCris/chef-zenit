import os
import sys
import psycopg2
import logging

# Añadir directorio raíz al path para poder importar desde app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from app import create_app, db
from app.models.ingrediente import Ingrediente
from app.models.receta import Receta, RecetaIngrediente, PasoPreparacion, ValorNutricional, Sustitucion, RestriccionDietetica

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def crear_base_datos():
    """
    Crea la base de datos si no existe
    """
    try:
        # Conectar a PostgreSQL sin especificar una base de datos
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
        exists = cursor.fetchone()
        
        if not exists:
            # Crear base de datos
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            logger.info(f"Base de datos '{DB_NAME}' creada exitosamente")
        else:
            logger.info(f"La base de datos '{DB_NAME}' ya existe")
            
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        logger.error(f"Error al crear la base de datos: {str(e)}")
        return False

def crear_tablas():
    """
    Crea las tablas en la base de datos
    """
    try:
        # Crear una aplicación Flask
        app = create_app()
        
        with app.app_context():
            # Crear todas las tablas
            db.create_all()
            logger.info("Tablas creadas exitosamente")
            
        return True
    except Exception as e:
        logger.error(f"Error al crear tablas: {str(e)}")
        return False

def cargar_datos_iniciales():
    """
    Carga datos iniciales en la base de datos
    """
    try:
        # Crear una aplicación Flask
        app = create_app()
        
        with app.app_context():
            # Restricciones dietéticas
            restricciones = [
                RestriccionDietetica(nombre='vegetariano', descripcion='Sin carne animal'),
                RestriccionDietetica(nombre='vegano', descripcion='Sin productos de origen animal'),
                RestriccionDietetica(nombre='sin_gluten', descripcion='Sin gluten, apto para celíacos'),
                RestriccionDietetica(nombre='sin_lactosa', descripcion='Sin lactosa'),
                RestriccionDietetica(nombre='bajo_sodio', descripcion='Bajo en sodio'),
                RestriccionDietetica(nombre='bajo_azucar', descripcion='Bajo en azúcar'),
                RestriccionDietetica(nombre='keto', descripcion='Dieta cetogénica'),
                RestriccionDietetica(nombre='paleo', descripcion='Dieta paleolítica')
            ]
            
            for r in restricciones:
                db.session.add(r)
            
            # Ingredientes
            categorias_ingredientes = {
                'verduras': [
                    {'nombre': 'Tomate', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Cebolla', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Lechuga', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Zanahoria', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Pimiento', 'es_alergeno': False, 'contiene_gluten': False}
                ],
                'frutas': [
                    {'nombre': 'Manzana', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Plátano', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Naranja', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Fresa', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Limón', 'es_alergeno': False, 'contiene_gluten': False}
                ],
                'carnes': [
                    {'nombre': 'Pollo', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Ternera', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Cerdo', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Cordero', 'es_alergeno': False, 'contiene_gluten': False}
                ],
                'pescados': [
                    {'nombre': 'Salmón', 'es_alergeno': True, 'contiene_gluten': False},
                    {'nombre': 'Atún', 'es_alergeno': True, 'contiene_gluten': False},
                    {'nombre': 'Merluza', 'es_alergeno': True, 'contiene_gluten': False},
                    {'nombre': 'Bacalao', 'es_alergeno': True, 'contiene_gluten': False}
                ],
                'lácteos': [
                    {'nombre': 'Leche', 'es_alergeno': True, 'contiene_gluten': False},
                    {'nombre': 'Queso', 'es_alergeno': True, 'contiene_gluten': False},
                    {'nombre': 'Yogur', 'es_alergeno': True, 'contiene_gluten': False},
                    {'nombre': 'Mantequilla', 'es_alergeno': True, 'contiene_gluten': False}
                ],
                'cereales': [
                    {'nombre': 'Arroz', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Pasta', 'es_alergeno': False, 'contiene_gluten': True},
                    {'nombre': 'Pan', 'es_alergeno': False, 'contiene_gluten': True},
                    {'nombre': 'Avena', 'es_alergeno': False, 'contiene_gluten': True}
                ],
                'legumbres': [
                    {'nombre': 'Lentejas', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Garbanzos', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Judías', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Guisantes', 'es_alergeno': False, 'contiene_gluten': False}
                ],
                'frutos_secos': [
                    {'nombre': 'Almendras', 'es_alergeno': True, 'contiene_gluten': False},
                    {'nombre': 'Nueces', 'es_alergeno': True, 'contiene_gluten': False},
                    {'nombre': 'Avellanas', 'es_alergeno': True, 'contiene_gluten': False},
                    {'nombre': 'Pistachos', 'es_alergeno': True, 'contiene_gluten': False}
                ],
                'aceites': [
                    {'nombre': 'Aceite de oliva', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Aceite de girasol', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Aceite de coco', 'es_alergeno': False, 'contiene_gluten': False}
                ],
                'especias': [
                    {'nombre': 'Sal', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Pimienta', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Orégano', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Comino', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Pimentón', 'es_alergeno': False, 'contiene_gluten': False}
                ],
                'otros': [
                    {'nombre': 'Huevo', 'es_alergeno': True, 'contiene_gluten': False},
                    {'nombre': 'Miel', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Azúcar', 'es_alergeno': False, 'contiene_gluten': False},
                    {'nombre': 'Chocolate', 'es_alergeno': False, 'contiene_gluten': False}
                ]
            }
            
            for categoria, ingredientes in categorias_ingredientes.items():
                for ing_data in ingredientes:
                    ingrediente = Ingrediente(
                        nombre=ing_data['nombre'],
                        categoria=categoria,
                        es_alergeno=ing_data['es_alergeno'],
                        contiene_gluten=ing_data['contiene_gluten']
                    )
                    db.session.add(ingrediente)
            
            # Guardar cambios
            db.session.commit()
            logger.info("Datos iniciales cargados exitosamente")
            
        return True
    except Exception as e:
        logger.error(f"Error al cargar datos iniciales: {str(e)}")
        return False

def inicializar_base_datos():
    """
    Inicializa la base de datos completa
    """
    if crear_base_datos():
        if crear_tablas():
            if cargar_datos_iniciales():
                logger.info("Base de datos inicializada correctamente")
                return True
    
    logger.error("Error al inicializar la base de datos")
    return False

if __name__ == '__main__':
    inicializar_base_datos()