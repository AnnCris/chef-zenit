# app/__init__.py - VERSIÓN CON FILTROS REGEX AÑADIDOS

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import nltk
import os
import re

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    app.config.from_object('config.Config')
    
    # Inicializar extensiones
    from app.models import db
    db.init_app(app)
    
    migrate = Migrate(app, db)
    
    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # ✅ AGREGAR FILTROS PERSONALIZADOS PARA JINJA2
    @app.template_filter('regex_search')
    def regex_search_filter(text, pattern):
        """Busca un patrón regex en el texto"""
        try:
            return bool(re.search(pattern, str(text)))
        except:
            return False
    
    @app.template_filter('regex_split')
    def regex_split_filter(text, pattern):
        """Divide texto usando un patrón regex"""
        try:
            return re.split(pattern, str(text))
        except:
            return [str(text)]
    
    @app.template_filter('regex_replace')
    def regex_replace_filter(text, pattern, replacement=''):
        """Reemplaza texto usando regex"""
        try:
            return re.sub(pattern, replacement, str(text))
        except:
            return str(text)
    
    @app.template_filter('regex_match')
    def regex_match_filter(text, pattern):
        """Verifica si el texto coincide completamente con el patrón"""
        try:
            return bool(re.match(pattern, str(text)))
        except:
            return False
    
    # ✅ FILTRO PARA LIMPIAR INSTRUCCIONES SIN REGEX
    @app.template_filter('clean_instructions')
    def clean_instructions_filter(text):
        """Limpia y divide instrucciones sin usar regex complejo"""
        if not text:
            return []
        
        text = str(text).strip()
        
        # Método 1: Dividir por saltos de línea
        if '\n' in text:
            steps = text.split('\n')
        # Método 2: Dividir por números seguidos de punto
        elif '1.' in text or '2.' in text:
            # Dividir manualmente por números
            steps = []
            current_step = ""
            lines = text.split('.')
            
            for line in lines:
                line = line.strip()
                if line and any(line.startswith(str(i)) for i in range(1, 21)):
                    if current_step:
                        steps.append(current_step.strip())
                    current_step = line[1:].strip() if len(line) > 1 else line
                else:
                    current_step += '. ' + line if current_step else line
            
            if current_step:
                steps.append(current_step.strip())
        # Método 3: Dividir por puntos
        else:
            steps = text.split('.')
        
        # Limpiar y filtrar pasos
        cleaned_steps = []
        for step in steps:
            step = step.strip()
            if step and len(step) > 15:
                # Remover numeración al inicio
                for i in range(1, 21):
                    if step.startswith(f'{i}.') or step.startswith(f'{i})'):
                        step = step[len(str(i))+1:].strip()
                        break
                
                # Capitalizar primera letra
                if step:
                    step = step[0].upper() + step[1:] if len(step) > 1 else step.upper()
                    
                    # Asegurar que termine con punto
                    if not step.endswith('.'):
                        step += '.'
                    
                    cleaned_steps.append(step)
        
        return cleaned_steps if cleaned_steps else [text]
    
    # ✅ MEJORAR DESCARGA DE DATOS NLTK
    def setup_nltk():
        try:
            # Intentar usar punkt
            nltk.data.find('tokenizers/punkt')
            print("✅ NLTK punkt ya disponible")
        except LookupError:
            try:
                print("📥 Descargando datos NLTK...")
                nltk.download('punkt', quiet=True)
                nltk.download('punkt_tab', quiet=True)
                nltk.download('stopwords', quiet=True)
                print("✅ Datos NLTK descargados")
            except Exception as e:
                print(f"⚠️ Error descargando NLTK: {e}")
    
    # Configurar NLTK en un hilo separado para no bloquear la app
    import threading
    nltk_thread = threading.Thread(target=setup_nltk)
    nltk_thread.daemon = True
    nltk_thread.start()
    
    # Registrar blueprints
    from app.routes import main
    from app.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    
    # Crear directorios necesarios
    os.makedirs(app.config.get('PDF_UPLOAD_FOLDER', 'static/pdfs'), exist_ok=True)
    os.makedirs(app.config.get('ML_MODEL_PATH', 'ml_models/trained_models'), exist_ok=True)
    
    return app