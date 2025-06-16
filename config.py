import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:2458@localhost/sistema_culinario'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración para ML
    ML_MODEL_PATH = 'ml_models/trained_models/'
    MAX_RECOMMENDATIONS = 10
    
    # Configuración para PDFs
    PDF_UPLOAD_FOLDER = 'static/pdfs/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Configuración NLTK
    NLTK_DATA_PATH = 'nltk_data/'