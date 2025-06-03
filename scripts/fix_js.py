# scripts/fix_js.py
import os

def fix_js_file():
    file_path = os.path.join('app', 'static', 'js', 'app.js')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Buscar la parte donde se procesa la respuesta de la API
        target_code = "const data = await response.json();"
        replacement_code = """
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
        """
        
        if target_code in content:
            new_content = content.replace(target_code, replacement_code)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            print(f"Archivo {file_path} actualizado correctamente")
            return True
        else:
            print(f"No se encontró el código objetivo en {file_path}")
            return False
    except Exception as e:
        print(f"Error al modificar el archivo JS: {str(e)}")
        return False

if __name__ == "__main__":
    fix_js_file()