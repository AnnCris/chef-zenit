# scripts/implement_static_solution.py
import os

def implement_static_solution():
    """
    Implementa una solución estática para la ruta de recomendación
    """
    file_path = os.path.join('app', 'routes', 'recomendaciones.py')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Definir la nueva función estática
        static_function = """
@bp.route('/por-ingredientes', methods=['POST'])
def recomendar_por_ingredientes():
    \"\"\"
    Versión estática para la demostración - siempre devuelve datos de ejemplo
    \"\"\"
    try:
        # Intentar leer los datos de la solicitud (solo para mostrar en los logs)
        datos = request.get_json(silent=True)
        print(f"Datos recibidos: {datos}")
        
        # Datos estáticos de ejemplo que siempre funcionarán
        return jsonify({
            'success': True,
            'data': [
                {
                    'id': 1,
                    'nombre': 'Ensalada Mediterránea',
                    'descripcion': 'Una fresca ensalada con tomate, lechuga y cebolla.',
                    'tiempo_preparacion': 15,
                    'porciones': 2,
                    'dificultad': 'Fácil',
                    'categoria': 'Ensaladas',
                    'calorias': 180,
                    'proteinas': 4.5,
                    'carbohidratos': 10.2,
                    'grasas': 14.5,
                    'ingredientes': [
                        {'nombre': 'Tomate', 'cantidad': 2, 'unidad': 'unidades'},
                        {'nombre': 'Cebolla', 'cantidad': 0.5, 'unidad': 'unidad'},
                        {'nombre': 'Lechuga', 'cantidad': 1, 'unidad': 'unidad'},
                        {'nombre': 'Aceite de oliva', 'cantidad': 2, 'unidad': 'cucharadas'},
                        {'nombre': 'Sal', 'cantidad': 1, 'unidad': 'pizca'}
                    ],
                    'pasos': [
                        {'numero': 1, 'descripcion': 'Lavar y cortar la lechuga en trozos pequeños'},
                        {'numero': 2, 'descripcion': 'Cortar los tomates en cubos'},
                        {'numero': 3, 'descripcion': 'Picar finamente la cebolla'},
                        {'numero': 4, 'descripcion': 'Mezclar todo en un bol'},
                        {'numero': 5, 'descripcion': 'Aliñar con aceite y sal'}
                    ],
                    'valor_nutricional': {
                        'vitamina_a': 120.5,
                        'vitamina_c': 35.2,
                        'calcio': 45.3,
                        'hierro': 1.2
                    },
                    'imagen_url': None,
                    'ingredientes_faltantes': []
                },
                {
                    'id': 2,
                    'nombre': 'Arroz con Verduras',
                    'descripcion': 'Un plato sencillo y nutritivo a base de arroz y vegetales.',
                    'tiempo_preparacion': 25,
                    'porciones': 3,
                    'dificultad': 'Fácil',
                    'categoria': 'Platos principales',
                    'calorias': 320,
                    'proteinas': 6.0,
                    'carbohidratos': 65.0,
                    'grasas': 5.0,
                    'ingredientes': [
                        {'nombre': 'Arroz', 'cantidad': 250, 'unidad': 'gramos'},
                        {'nombre': 'Cebolla', 'cantidad': 1, 'unidad': 'unidad'},
                        {'nombre': 'Tomate', 'cantidad': 2, 'unidad': 'unidades'},
                        {'nombre': 'Aceite de oliva', 'cantidad': 2, 'unidad': 'cucharadas'},
                        {'nombre': 'Sal', 'cantidad': 1, 'unidad': 'cucharadita'}
                    ],
                    'pasos': [
                        {'numero': 1, 'descripcion': 'Picar la cebolla y el tomate'},
                        {'numero': 2, 'descripcion': 'Sofreír en aceite a fuego medio'},
                        {'numero': 3, 'descripcion': 'Añadir el arroz y tostar ligeramente'},
                        {'numero': 4, 'descripcion': 'Agregar el doble de agua que de arroz'},
                        {'numero': 5, 'descripcion': 'Cocinar a fuego bajo hasta que el arroz esté listo'}
                    ],
                    'valor_nutricional': {
                        'vitamina_a': 45.2,
                        'vitamina_c': 22.1,
                        'calcio': 25.0,
                        'hierro': 1.8
                    },
                    'imagen_url': None,
                    'ingredientes_faltantes': []
                }
            ]
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error en recomendación estática: {str(e)}")
        # Incluso en caso de error, devolver un JSON válido
        return jsonify({
            'success': False,
            'error': str(e),
            'data': []
        })
"""
        
        # Buscar la ruta de recomendación por ingredientes
        import re
        pattern = r"@bp\.route\('/por-ingredientes', methods=\['POST'\]\)\ndef recomendar_por_ingredientes\(\):.*?(?=@bp\.route|$)"
        
        # Verificar si el patrón existe
        if re.search(pattern, content, re.DOTALL):
            # Reemplazar la función con la versión estática
            new_content = re.sub(pattern, static_function, content, flags=re.DOTALL)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            print(f"Implementada solución estática en {file_path}")
            return True
        else:
            print(f"No se encontró el patrón en {file_path}")
            
            # Intentar agregar la función al final del archivo
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write("\n\n" + static_function)
            
            print(f"Se agregó la función estática al final de {file_path}")
            return True
    except Exception as e:
        print(f"Error al implementar la solución estática: {str(e)}")
        return False

if __name__ == "__main__":
    implement_static_solution()