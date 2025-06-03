from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from app.utils.db import init_db

db = SQLAlchemy()

def create_app(test_config=None):
    # Crear y configurar la app
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuración por defecto
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
        
        # Asegurar que hay una clave secreta
        if 'SECRET_KEY' not in app.config or not app.config['SECRET_KEY']:
            from app.config import SECRET_KEY
            app.config['SECRET_KEY'] = SECRET_KEY
    else:
        app.config.from_mapping(test_config)
    
    # Asegurarse que el directorio de la instancia existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Inicializar la base de datos
    init_db(app)
    db.init_app(app)
    
    # Habilitar CORS
    CORS(app)
    
    # Registrar blueprints
    from app.routes import ingredientes, recetas, recomendaciones
    app.register_blueprint(ingredientes.bp)
    app.register_blueprint(recetas.bp)
    app.register_blueprint(recomendaciones.bp)
    
    # Ruta para la página principal
    @app.route('/')
    def index():
        return render_template('index.html')  # Usa render_template en lugar de send_static_file
    
    return app