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