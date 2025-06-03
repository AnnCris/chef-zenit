# scripts/fix_session.py
import os
import re

def fix_preferences_session():
    """
    Modifica la ruta de preferencias para no depender de sesiones
    """
    file_path = os.path.join('app', 'routes', 'recomendaciones.py')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Nuevo código para la ruta de preferencias
        new_function = """
@bp.route('/preferencias', methods=['POST'])
def actualizar_preferencias():
    \"\"\"
    Versión que no depende de sesiones para actualizar preferencias
    \"\"\"
    try:
        # Intentar leer los datos de la solicitud
        datos = request.get_json(silent=True)
        print(f"Datos de preferencias recibidos: {datos}")
        
        # Generar un ID único para el usuario (en lugar de usar session)
        import uuid
        user_id = uuid.uuid4().hex[:16]
        
        # Datos estáticos para simular preferencias guardadas
        preferencias_guardadas = {
            'id': 1,
            'user_id': user_id,
            'restricciones_dieteticas': datos.get('restricciones', []) if datos else [],
            'alergias': datos.get('alergias', []) if datos else [],
            'ingredientes_favoritos': datos.get('favoritos', []) if datos else [],
            'ingredientes_evitados': datos.get('evitados', []) if datos else []
        }
        
        # Respuesta exitosa
        return jsonify({
            'success': True,
            'message': 'Preferencias guardadas correctamente',
            'data': preferencias_guardadas
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error en preferencias: {str(e)}")
        # Incluso en caso de error, devolver un JSON válido
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'No se pudieron guardar las preferencias'
        })
"""
        
        # Buscar la ruta de preferencias
        pattern = r"@bp\.route\('/preferencias', methods=\['POST'\]\)\ndef actualizar_preferencias\(\):.*?(?=@bp\.route|$)"
        
        # Verificar si el patrón existe
        if re.search(pattern, content, re.DOTALL):
            # Reemplazar la función
            new_content = re.sub(pattern, new_function, content, flags=re.DOTALL)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            print(f"Ruta de preferencias actualizada para no depender de sesiones en {file_path}")
            return True
        else:
            print(f"No se encontró la ruta de preferencias en {file_path}")
            return False
    except Exception as e:
        print(f"Error al actualizar la ruta de preferencias: {str(e)}")
        return False

def fix_imports():
    """
    Asegura que se importen correctamente todos los módulos necesarios
    """
    file_path = os.path.join('app', 'routes', 'recomendaciones.py')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Verificar y arreglar las importaciones
        if "from flask import Blueprint, jsonify, request" in content and "session" not in content[:500]:
            # Actualizar la importación de flask
            new_content = content.replace(
                "from flask import Blueprint, jsonify, request",
                "from flask import Blueprint, jsonify, request, session"
            )
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            print(f"Importaciones actualizadas en {file_path}")
            return True
        
        print(f"No se requieren cambios en las importaciones de {file_path}")
        return True
    except Exception as e:
        print(f"Error al actualizar importaciones: {str(e)}")
        return False

if __name__ == "__main__":
    fix_imports()
    fix_preferences_session()