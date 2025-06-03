import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Configuración de la base de datos
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '2458')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'recetas_db')

# Configuración de la aplicación
SECRET_KEY = '2fe25b324839730ed39b30b0af544c3c589334285d3090e29a41f0d0776cc090'
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# URI de conexión a la base de datos
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuración de rutas
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB máximo para subidas de archivos

# Asegurar que el directorio de subidas existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)