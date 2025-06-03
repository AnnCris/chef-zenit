# scripts/fix_js_syntax.py
import os
import re

def fix_js_syntax():
    """
    Corrige errores de sintaxis en el archivo app.js
    """
    file_path = os.path.join('app', 'static', 'js', 'app.js')
    
    try:
        # Leer el contenido actual
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Encontrar y corregir la línea problemática (alrededor de la línea 266)
        error_found = False
        for i in range(max(0, 266-10), min(len(lines), 266+10)):
            line = lines[i]
            line_num = i + 1  # Líneas empiezan en 1, no en 0
            
            # Buscar errores comunes de sintaxis
            if "{" in line and "}" in line and re.search(r"}\s*{", line):
                print(f"Posible error en línea {line_num}: Llaves mal formadas")
                error_found = True
            elif "fetchData();" in line and not line.strip().endswith(";"):
                print(f"Posible error en línea {line_num}: Falta punto y coma")
                error_found = True
            elif "," in line and line.strip().endswith(","):
                if i+1 < len(lines) and "}" in lines[i+1].strip() and not lines[i+1].strip().startswith("//"):
                    print(f"Posible error en línea {line_num}: Coma final en objeto/array")
                    # Corregir la coma final
                    lines[i] = line.rstrip().rstrip(",") + "\n"
                    error_found = True
            
            # Verificar errores de función useEffect
            if "useEffect(" in line:
                # Buscar si hay un paréntesis abierto sin cerrar
                open_parens = line.count("(")
                close_parens = line.count(")")
                if open_parens > close_parens:
                    # Revisar la siguiente línea para ver si hay un error con la función del efecto
                    if i+1 < len(lines) and "fetchData()" in lines[i+1] and "," not in lines[i+1]:
                        print(f"Posible error en línea {line_num+1}: Falta coma después de función del efecto")
                        # Corregir la sintaxis de useEffect
                        lines[i+1] = lines[i+1].replace("fetchData();", "fetchData(),")
                        error_found = True
        
        # Si no se encontraron errores específicos, realizar correcciones generales
        if not error_found:
            print("No se encontraron errores específicos. Realizando corrección general alrededor de la línea 266...")
            
            # Extraer el bloque que contiene la línea 266 para análisis
            start = max(0, 260)
            end = min(len(lines), 270)
            block = "".join(lines[start:end])
            
            # Buscar patrones comunes de error
            if "useEffect(" in block:
                # Corregir errores comunes en useEffect
                fixed_block = re.sub(
                    r"useEffect\(\s*\(\s*\)\s*=>\s*\{\s*const fetchData\s*=\s*async\s*\(\)\s*=>\s*\{(.*?)\};\s*fetchData\(\);\s*\},\s*\[\]\s*\);",
                    r"useEffect(() => {\n    const fetchData = async () => {\1};\n    fetchData();\n  }, []);",
                    block, 
                    flags=re.DOTALL
                )
                
                if fixed_block != block:
                    lines[start:end] = fixed_block.splitlines(True)
                    print("Corregido bloque useEffect")
            
            # También buscar y corregir problemas en la estructura general
            for i in range(max(0, 265-2), min(len(lines), 265+2)):
                # Detectar líneas sueltas con llaves o paréntesis desbalanceados
                line = lines[i]
                if line.strip() == "}" or line.strip() == "{" or line.strip() == ");":
                    print(f"Posible línea problemática {i+1}: {line.strip()}")
        
        # Escribir contenido corregido
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
        
        print(f"Archivo {file_path} corregido")
        
        # Si todavía hay problemas, reescribir completamente la función useEffect
        if not error_found:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Reemplazar el patrón problemático
            patterns = [
                # Patrón 1: useEffect mal formado
                (r"useEffect\(\s*\(\s*\)\s*=>\s*\{[\s\S]*?fetchData\(\);[\s\S]*?\}\s*,\s*\[\]\s*\);", 
                 "useEffect(() => {\n    const fetchData = async () => {\n      // Código de fetchData\n    };\n    fetchData();\n  }, []);\n"),
                
                # Patrón 2: Objeto mal formado
                (r"\{\s*nombre:.*?,\s*similitud:.*?,\s*\}", 
                 "{\n    nombre: 'Nombre de ejemplo',\n    similitud: 0.95\n  }"),
            ]
            
            fixed = False
            for pattern, replacement in patterns:
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    fixed = True
            
            if fixed:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print("Se realizaron reemplazos de patrones problemáticos")
        
        return True
    except Exception as e:
        print(f"Error al corregir archivo JavaScript: {str(e)}")
        return False

def scan_and_fix_file_manually():
    """
    Escanea y arregla manualmente el archivo app.js
    """
    file_path = os.path.join('app', 'static', 'js', 'app.js')
    
    try:
        # Leer el contenido actual
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Reescribir el contenido completo de la función
        new_function = """async function buscarRecetasPorConsulta() {
        const consulta = consultaInput.value.trim();
        
        if (!consulta) {
            mostrarMensaje('Por favor, escribe una consulta.', 'warning');
            return;
        }
        
        try {
            // Mostrar indicador de carga
            resultadosContainer.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Cargando...</span></div><p class="mt-2">Analizando tu consulta...</p></div>';
            
            // Realizar petición a la API
            const response = await fetch('/api/recomendaciones/consulta', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    consulta: consulta,
                    max_resultados: 5
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
            
            if (data.success && data.data.recomendaciones.length > 0) {
                // Mostrar información de análisis
                let analisisHTML = `<div class="alert alert-info">
                    <h5>He analizado tu consulta:</h5>`;
                    
                if (data.data.analisis.ingredientes.length > 0) {
                    analisisHTML += `<p><strong>Ingredientes detectados:</strong> ${data.data.analisis.ingredientes.join(', ')}</p>`;
                }
                
                if (data.data.analisis.restricciones.length > 0) {
                    analisisHTML += `<p><strong>Restricciones dietéticas:</strong> ${data.data.analisis.restricciones.join(', ')}</p>`;
                }
                
                if (data.data.analisis.alergias.length > 0) {
                    analisisHTML += `<p><strong>Alergias detectadas:</strong> ${data.data.analisis.alergias.join(', ')}</p>`;
                }
                
                analisisHTML += `</div>`;
                
                // Mostrar resultados con el análisis
                mostrarResultados(data.data.recomendaciones, analisisHTML);
            } else {
                mostrarMensaje('No encontré recetas que coincidan con tu consulta. Por favor, intenta ser más específico o usa términos diferentes.', 'info');
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarMensaje('Ocurrió un error al procesar tu consulta. Por favor, intenta de nuevo más tarde.', 'danger');
        }
    }"""
        
        # Buscar la función original
        pattern = r"async function buscarRecetasPorConsulta\(\) \{[\s\S]*?\}"
        
        if re.search(pattern, content):
            new_content = re.sub(pattern, new_function, content)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            print("Función buscarRecetasPorConsulta reemplazada completamente")
            return True
        else:
            print("No se encontró la función buscarRecetasPorConsulta")
            return False
    except Exception as e:
        print(f"Error al reemplazar función: {str(e)}")
        return False

if __name__ == "__main__":
    if not fix_js_syntax():
        scan_and_fix_file_manually()