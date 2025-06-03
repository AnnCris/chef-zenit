# scripts/set_secret_key.py
import os
import re
import secrets
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_secret_key():
    """
    Genera una clave secreta segura
    """
    return secrets.token_hex(32)

def update_config_file():
    """
    Actualiza el archivo .env con una clave secreta
    """
    env_file = '.env'
    
    # Generar una clave secreta
    secret_key = generate_secret_key()
    
    # Verificar si el archivo .env existe
    if os.path.exists(env_file):
        try:
            # Leer el contenido actual
            with open(env_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Verificar si ya hay una clave secreta
            if 'SECRET_KEY=' in content:
                # Reemplazar la clave existente
                new_content = re.sub(r'SECRET_KEY=.*', f'SECRET_KEY={secret_key}', content)
            else:
                # Añadir la clave al final
                new_content = content + f'\nSECRET_KEY={secret_key}\n'
            
            # Escribir el contenido actualizado
            with open(env_file, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            logger.info(f"Clave secreta actualizada en {env_file}")
        except Exception as e:
            logger.error(f"Error al actualizar .env: {str(e)}")
            return False
    else:
        # Crear el archivo .env si no existe
        try:
            with open(env_file, 'w', encoding='utf-8') as file:
                file.write(f"SECRET_KEY={secret_key}\n")
            logger.info(f"Archivo {env_file} creado con la clave secreta")
        except Exception as e:
            logger.error(f"Error al crear .env: {str(e)}")
            return False
    
    return True

def update_app_init():
    """
    Actualiza app/__init__.py para asegurar que la clave secreta se carga correctamente
    """
    init_file = os.path.join('app', '__init__.py')
    
    try:
        # Leer el contenido actual
        with open(init_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Verificar si necesitamos modificar create_app
        if "app.config.from_pyfile('config.py'" in content:
            # Buscar el bloque de configuración
            pattern = r"if test_config is None:.*?app\.config\.from_pyfile\('config\.py', silent=True\)"
            
            if re.search(pattern, content, re.DOTALL):
                # Reemplazar el bloque de configuración
                replacement = """if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
        
        # Asegurar que hay una clave secreta
        if 'SECRET_KEY' not in app.config or not app.config['SECRET_KEY']:
            from app.config import SECRET_KEY
            app.config['SECRET_KEY'] = SECRET_KEY"""
                
                new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                
                # Escribir el contenido actualizado
                with open(init_file, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                
                logger.info(f"Configuración de clave secreta actualizada en {init_file}")
                return True
            else:
                logger.warning(f"No se encontró el patrón de configuración en {init_file}")
                return False
        else:
            logger.warning(f"El archivo {init_file} no parece tener la estructura esperada")
            return False
    except Exception as e:
        logger.error(f"Error al actualizar {init_file}: {str(e)}")
        return False

def update_direct_secret_key():
    """
    Actualiza app/config.py para incluir la clave secreta directamente
    """
    config_file = os.path.join('app', 'config.py')
    
    try:
        # Leer el contenido actual
        with open(config_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Verificar si ya hay una línea SECRET_KEY
        if "SECRET_KEY =" in content:
            # Generar una clave secreta
            secret_key = generate_secret_key()
            
            # Reemplazar la línea existente
            new_content = re.sub(r"SECRET_KEY =.*", f"SECRET_KEY = '{secret_key}'", content)
            
            # Escribir el contenido actualizado
            with open(config_file, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            logger.info(f"Clave secreta actualizada directamente en {config_file}")
            return True
        else:
            logger.warning(f"No se encontró la línea SECRET_KEY en {config_file}")
            return False
    except Exception as e:
        logger.error(f"Error al actualizar {config_file}: {str(e)}")
        return False

def main():
    """
    Función principal que orquesta todas las actualizaciones
    """
    # Actualizar .env
    env_update = update_config_file()
    
    # Actualizar app/__init__.py
    init_update = update_app_init()
    
    # Actualización directa en config.py (asegurando que al menos un método funcione)
    config_update = update_direct_secret_key()
    
    if env_update or init_update or config_update:
        logger.info("¡Clave secreta configurada correctamente! Reinicia la aplicación para aplicar los cambios.")
        return True
    else:
        logger.error("No se pudo configurar la clave secreta en ningún archivo")
        return False

if __name__ == "__main__":
    main()