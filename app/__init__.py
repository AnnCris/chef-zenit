# app/__init__.py - VERSIÓN CORREGIDA SIN FILTROS REGEX PROBLEMÁTICOS

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import nltk
import os

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
    
    # ✅ FILTROS SIMPLES Y SEGUROS PARA JINJA2 (SIN REGEX)
    @app.template_filter('safe_title')
    def safe_title_filter(text):
        """Convierte texto a título de forma segura"""
        try:
            return str(text).title() if text else ''
        except:
            return ''
    
    @app.template_filter('safe_upper')
    def safe_upper_filter(text):
        """Convierte texto a mayúsculas de forma segura"""
        try:
            return str(text).upper() if text else ''
        except:
            return ''
    
    @app.template_filter('safe_lower')
    def safe_lower_filter(text):
        """Convierte texto a minúsculas de forma segura"""
        try:
            return str(text).lower() if text else ''
        except:
            return ''
    
    @app.template_filter('safe_strip')
    def safe_strip_filter(text):
        """Remueve espacios en blanco de forma segura"""
        try:
            return str(text).strip() if text else ''
        except:
            return ''
    
    # ✅ FILTRO PARA LIMPIAR INSTRUCCIONES SIN REGEX
    @app.template_filter('clean_instructions')
    def clean_instructions_filter(text):
        """Limpia y divide instrucciones sin usar regex complejo"""
        if not text:
            return []
        
        try:
            text = str(text).strip()
            
            # Método 1: Dividir por saltos de línea
            if '\n' in text:
                steps = text.split('\n')
            # Método 2: Dividir por puntos
            elif '.' in text:
                steps = text.split('.')
            else:
                return [text]
            
            # Limpiar y filtrar pasos
            cleaned_steps = []
            for step in steps:
                if step and step.strip():
                    clean_step = step.strip()
                    # Solo agregar pasos que tengan contenido sustancial
                    if len(clean_step) > 10:
                        # Capitalizar primera letra si no está ya
                        if clean_step and clean_step[0].islower():
                            clean_step = clean_step[0].upper() + clean_step[1:]
                        
                        # Asegurar que termine con punto
                        if not clean_step.endswith('.'):
                            clean_step += '.'
                        
                        cleaned_steps.append(clean_step)
            
            return cleaned_steps if cleaned_steps else [text]
            
        except Exception as e:
            print(f"Error en clean_instructions: {e}")
            return [str(text)]
    
    # ✅ FILTRO PARA FORMATEAR NÚMEROS DE FORMA SEGURA
    @app.template_filter('safe_format')
    def safe_format_filter(value, format_str='%.1f'):
        """Formatea números de forma segura"""
        try:
            if value is None:
                return '0'
            return format_str % float(value)
        except:
            return str(value) if value else '0'
    
    # ✅ FILTRO PARA MANEJAR VALORES POR DEFECTO
    @app.template_filter('default_value')
    def default_value_filter(value, default='N/A'):
        """Devuelve un valor por defecto si el valor es None o vacío"""
        try:
            return value if value is not None and str(value).strip() else default
        except:
            return default
    
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
        except Exception as e:
            print(f"⚠️ Error general con NLTK: {e}")
    
    # Configurar NLTK en un hilo separado para no bloquear la app
    try:
        import threading
        nltk_thread = threading.Thread(target=setup_nltk)
        nltk_thread.daemon = True
        nltk_thread.start()
    except Exception as e:
        print(f"⚠️ No se pudo inicializar NLTK: {e}")
    
    # ✅ MANEJAR ERRORES DE TEMPLATE DE FORMA SEGURA
    @app.errorhandler(500)
    def handle_template_error(error):
        print(f"❌ Error 500: {error}")
        # En caso de error de template, devolver una respuesta básica
        return "Error interno del servidor. Por favor, intenta nuevamente.", 500
    
    @app.errorhandler(Exception)
    def handle_general_error(error):
        print(f"❌ Error general: {error}")
        # Logging del error para debug
        import traceback
        traceback.print_exc()
        return "Ha ocurrido un error. Por favor, intenta nuevamente.", 500
    
    # Registrar blueprints
    try:
        from app.routes import main
        from app.auth import auth
        app.register_blueprint(main)
        app.register_blueprint(auth, url_prefix='/auth')
        print("✅ Blueprints registrados correctamente")
    except Exception as e:
        print(f"❌ Error registrando blueprints: {e}")
        raise e
    
    # Crear directorios necesarios
    try:
        os.makedirs(app.config.get('PDF_UPLOAD_FOLDER', 'static/pdfs'), exist_ok=True)
        os.makedirs(app.config.get('ML_MODEL_PATH', 'ml_models/trained_models'), exist_ok=True)
        print("✅ Directorios creados correctamente")
    except Exception as e:
        print(f"⚠️ Error creando directorios: {e}")
    
    # ✅ CONFIGURACIÓN ADICIONAL PARA TEMPLATE ENGINE
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    
    print("✅ Aplicación Flask configurada correctamente")
    return app