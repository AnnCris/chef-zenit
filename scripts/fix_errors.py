# scripts/fix_errors.py
import os
import re
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_file(file_path, replacements):
    """
    Realiza reemplazos en un archivo
    
    Args:
        file_path: Ruta al archivo
        replacements: Lista de tuplas (pattern, replacement)
    """
    try:
        # Leer el contenido del archivo
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Aplicar reemplazos
        modified = False
        for pattern, replacement in replacements:
            if re.search(pattern, content):
                new_content = re.sub(pattern, replacement, content)
                if new_content != content:
                    content = new_content
                    modified = True
        
        # Guardar solo si hubo cambios
        if modified:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.info(f"Archivo {file_path} modificado correctamente")
        else:
            logger.info(f"No se requirieron cambios en {file_path}")
        
        return modified
    except Exception as e:
        logger.error(f"Error al modificar {file_path}: {str(e)}")
        return False

def fix_all_errors():
    """Corrige todos los errores identificados"""
    
    # 1. Corregir db no definido en recomendaciones.py
    fix_file(
        os.path.join('app', 'routes', 'recomendaciones.py'),
        [
            (
                r'import logging\n',
                'import logging\nfrom app import db\n'
            ),
            (
                r'from flask import Blueprint',
                'from flask import Blueprint'
            )
        ]
    )
    
    # 2. Corregir receta_restricciones y Sustitucion no definidos en motor_inferencia.py
    fix_file(
        os.path.join('app', 'services', 'motor_inferencia.py'),
        [
            (
                r'from app.models.receta import Receta, RecetaIngrediente, RestriccionDietetica',
                'from app.models.receta import Receta, RecetaIngrediente, RestriccionDietetica, receta_restricciones, Sustitucion'
            )
        ]
    )
    
    # 3. Corregir this6 en pdf_generator.py
    fix_file(
        os.path.join('app', 'services', 'pdf_generator.py'),
        [
            (
                r'this6',
                '6'
            )
        ]
    )
    
    # 4. Corregir or_ no definido en recomendacion.py
    fix_file(
        os.path.join('app', 'services', 'recomendacion.py'),
        [
            (
                r'from sqlalchemy import func',
                'from sqlalchemy import func, or_, and_, not_'
            ),
            (
                r'import numpy as np',
                'import numpy as np'
            )
        ]
    )
    
    logger.info("Todos los errores corregidos")

if __name__ == '__main__':
    fix_all_errors()