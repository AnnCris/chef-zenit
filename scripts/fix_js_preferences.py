# scripts/fix_js_preferences.py
import os
import re

def fix_js_preferences():
    """
    Mejora el manejo de errores en la función guardarPreferencias en el JavaScript
    """
    file_path = os.path.join('app', 'static', 'js', 'app.js')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Buscar la función guardarPreferencias
        function_pattern = r"async function guardarPreferencias\(\) \{[\s\S]*?\}"
        
        function_match = re.search(function_pattern, content)
        
        if not function_match:
            print("No se encontró la función guardarPreferencias en el archivo JavaScript")
            return False
        
        # Obtener la función actual
        current_function = function_match.group(0)
        
        # Crear una versión mejorada
        improved_function = """async function guardarPreferencias() {
        try {
            // Obtener restricciones dietéticas seleccionadas
            const restricciones = [];
            const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
            checkboxes.forEach(checkbox => {
                restricciones.push(checkbox.value);
            });
            
            console.log("Restricciones seleccionadas:", restricciones);
            console.log("Alergias seleccionadas:", alergias);
            
            // Mostrar indicador de carga
            resultadosContainer.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Guardando...</span></div><p class="mt-2">Guardando preferencias...</p></div>';
            
            // Realizar petición a la API
            const response = await fetch('/api/recomendaciones/preferencias', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    restricciones: restricciones,
                    alergias: alergias
                }),
            });
            
            // Obtener texto de la respuesta para diagnóstico
            const responseText = await response.text();
            console.log('Respuesta del servidor (texto):', responseText);
            
            // Intentar parsear como JSON
            let data;
            try {
                data = JSON.parse(responseText);
            } catch (e) {
                console.error('Error al parsear JSON:', e);
                mostrarMensaje('Error: La respuesta del servidor no es un JSON válido. Verifica los logs para más detalles.', 'danger');
                return;
            }
            
            if (data.success) {
                mostrarMensaje(data.message || 'Preferencias guardadas correctamente. A partir de ahora, las recomendaciones tendrán en cuenta tus preferencias y restricciones.', 'success');
            } else {
                mostrarMensaje(data.error || 'No se pudieron guardar las preferencias.', 'warning');
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarMensaje('Ocurrió un error al guardar las preferencias. Por favor, intenta de nuevo más tarde.', 'danger');
        }
    }"""
        
        # Reemplazar la función
        new_content = content.replace(current_function, improved_function)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"Función guardarPreferencias mejorada en {file_path}")
        return True
    except Exception as e:
        print(f"Error al modificar la función guardarPreferencias: {str(e)}")
        return False

if __name__ == "__main__":
    fix_js_preferences()