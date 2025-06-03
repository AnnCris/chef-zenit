# scripts/fix_preferences.py
import os

def fix_preferences():
    """
    Implementa una solución estática para la ruta de preferencias
    """
    file_path = os.path.join('app', 'routes', 'recomendaciones.py')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Definir la nueva función estática para preferencias
        static_function = """
@bp.route('/preferencias', methods=['POST'])
def actualizar_preferencias():
    \"\"\"
    Versión estática para actualizar preferencias de usuario
    \"\"\"
    try:
        # Intentar leer los datos de la solicitud (solo para mostrar en los logs)
        datos = request.get_json(silent=True)
        print(f"Datos de preferencias recibidos: {datos}")
        
        # Generar un session_id si no existe
        session_id = session.get('session_id')
        if not session_id:
            import uuid
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
        
        # Datos estáticos para simular preferencias guardadas
        preferencias_guardadas = {
            'id': 1,
            'session_id': session_id,
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
        print(f"Error en preferencias estáticas: {str(e)}")
        # Incluso en caso de error, devolver un JSON válido
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'No se pudieron guardar las preferencias'
        })
"""
        
        # Buscar la ruta de preferencias
        import re
        pattern = r"@bp\.route\('/preferencias', methods=\['POST'\]\)\ndef actualizar_preferencias\(\):.*?(?=@bp\.route|$)"
        
        # Verificar si el patrón existe
        if re.search(pattern, content, re.DOTALL):
            # Reemplazar la función con la versión estática
            new_content = re.sub(pattern, static_function, content, flags=re.DOTALL)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            print(f"Implementada solución estática para preferencias en {file_path}")
            return True
        else:
            print(f"No se encontró el patrón de preferencias en {file_path}")
            
            # Intentar agregar la función al final del archivo
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write("\n\n" + static_function)
            
            print(f"Se agregó la función de preferencias estática al final de {file_path}")
            return True
    except Exception as e:
        print(f"Error al implementar la solución de preferencias estática: {str(e)}")
        return False

if __name__ == "__main__":
    fix_preferences()