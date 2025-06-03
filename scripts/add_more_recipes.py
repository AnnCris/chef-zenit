# scripts/add_more_recipes.py
import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.receta import Receta, RecetaIngrediente, PasoPreparacion, ValorNutricional
from app.models.ingrediente import Ingrediente

def add_more_recipes():
    # Crear una aplicación Flask
    app = create_app()
    
    with app.app_context():
        # Verificar si ya hay recetas
        existing_count = Receta.query.count()
        logger.info(f"Recetas existentes: {existing_count}")
        
        # Obtener ingredientes
        ingredientes = {ing.nombre: ing for ing in Ingrediente.query.all()}
        
        if not ingredientes:
            logger.error("No hay ingredientes en la base de datos")
            return
        
        # Lista de recetas a agregar
        recetas_data = [
            {
                'nombre': 'Ensalada Mediterránea',
                'descripcion': 'Una refrescante ensalada mediterránea con tomate, pepino y aceitunas',
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
                    'Lavar y cortar la lechuga en trozos pequeños',
                    'Cortar los tomates en cubos',
                    'Picar finamente la cebolla',
                    'Mezclar todos los ingredientes en un bol',
                    'Aliñar con aceite de oliva y sal'
                ]
            },
            {
                'nombre': 'Pasta con Tomate y Albahaca',
                'descripcion': 'Un clásico italiano sencillo y delicioso',
                'tiempo_preparacion': 20,
                'porciones': 4,
                'dificultad': 'Fácil',
                'categoria': 'Pastas',
                'calorias': 380,
                'proteinas': 12.0,
                'carbohidratos': 65.0,
                'grasas': 8.5,
                'ingredientes': [
                    {'nombre': 'Pasta', 'cantidad': 400, 'unidad': 'gramos'},
                    {'nombre': 'Tomate', 'cantidad': 4, 'unidad': 'unidades'},
                    {'nombre': 'Aceite de oliva', 'cantidad': 3, 'unidad': 'cucharadas'},
                    {'nombre': 'Sal', 'cantidad': 1, 'unidad': 'cucharadita'}
                ],
                'pasos': [
                    'Hervir agua con sal y cocinar la pasta',
                    'Mientras tanto, cortar los tomates en cubos',
                    'Calentar el aceite en una sartén y añadir los tomates',
                    'Cocinar a fuego medio hasta que formen una salsa',
                    'Escurrir la pasta y mezclar con la salsa'
                ]
            },
            {
                'nombre': 'Tortilla de Patatas',
                'descripcion': 'La clásica tortilla española',
                'tiempo_preparacion': 30,
                'porciones': 4,
                'dificultad': 'Media',
                'categoria': 'Huevos',
                'calorias': 320,
                'proteinas': 15.0,
                'carbohidratos': 30.0,
                'grasas': 18.0,
                'ingredientes': [
                    {'nombre': 'Huevo', 'cantidad': 6, 'unidad': 'unidades'},
                    {'nombre': 'Cebolla', 'cantidad': 1, 'unidad': 'unidad'},
                    {'nombre': 'Aceite de oliva', 'cantidad': 4, 'unidad': 'cucharadas'},
                    {'nombre': 'Sal', 'cantidad': 1, 'unidad': 'cucharadita'}
                ],
                'pasos': [
                    'Pelar y cortar las patatas en rodajas finas',
                    'Picar la cebolla finamente',
                    'Calentar el aceite en una sartén y freír las patatas y la cebolla a fuego medio-bajo',
                    'Batir los huevos con sal en un bol grande',
                    'Escurrir las patatas y la cebolla y mezclar con los huevos batidos',
                    'Calentar un poco de aceite en una sartén y verter la mezcla',
                    'Cocinar a fuego medio-bajo y darle la vuelta cuando esté cuajada por abajo'
                ]
            },
            {
                'nombre': 'Arroz con Pollo',
                'descripcion': 'Un plato completo y nutritivo',
                'tiempo_preparacion': 45,
                'porciones': 4,
                'dificultad': 'Media',
                'categoria': 'Arroces',
                'calorias': 480,
                'proteinas': 28.0,
                'carbohidratos': 60.0,
                'grasas': 12.0,
                'ingredientes': [
                    {'nombre': 'Arroz', 'cantidad': 400, 'unidad': 'gramos'},
                    {'nombre': 'Pollo', 'cantidad': 500, 'unidad': 'gramos'},
                    {'nombre': 'Cebolla', 'cantidad': 1, 'unidad': 'unidad'},
                    {'nombre': 'Tomate', 'cantidad': 2, 'unidad': 'unidades'},
                    {'nombre': 'Aceite de oliva', 'cantidad': 3, 'unidad': 'cucharadas'},
                    {'nombre': 'Sal', 'cantidad': 1, 'unidad': 'cucharadita'},
                    {'nombre': 'Pimienta', 'cantidad': 0.5, 'unidad': 'cucharadita'}
                ],
                'pasos': [
                    'Cortar el pollo en trozos y sazonar con sal y pimienta',
                    'Calentar el aceite en una olla y dorar el pollo',
                    'Agregar la cebolla picada y los tomates en cubos',
                    'Añadir el arroz y sofreír unos minutos',
                    'Verter agua caliente (el doble del volumen del arroz)',
                    'Cocinar a fuego medio-bajo durante 20 minutos o hasta que el arroz esté tierno'
                ]
            }
        ]
        
        # Agregar recetas
        added_count = 0
        for receta_data in recetas_data:
            # Verificar si la receta ya existe
            if Receta.query.filter_by(nombre=receta_data['nombre']).first():
                logger.info(f"La receta '{receta_data['nombre']}' ya existe")
                continue
            
            receta = Receta(
                nombre=receta_data['nombre'],
                descripcion=receta_data['descripcion'],
                tiempo_preparacion=receta_data['tiempo_preparacion'],
                porciones=receta_data['porciones'],
                dificultad=receta_data['dificultad'],
                categoria=receta_data['categoria'],
                calorias=receta_data['calorias'],
                proteinas=receta_data['proteinas'],
                carbohidratos=receta_data['carbohidratos'],
                grasas=receta_data['grasas']
            )
            db.session.add(receta)
            db.session.flush()  # Para obtener el ID
            
            # Agregar ingredientes
            for ing_data in receta_data['ingredientes']:
                ingrediente = ingredientes.get(ing_data['nombre'])
                if ingrediente:
                    ri = RecetaIngrediente(
                        receta_id=receta.id,
                        ingrediente_id=ingrediente.id,
                        cantidad=ing_data['cantidad'],
                        unidad=ing_data['unidad']
                    )
                    db.session.add(ri)
                else:
                    logger.warning(f"Ingrediente '{ing_data['nombre']}' no encontrado")
            
            # Agregar pasos
            for i, paso_text in enumerate(receta_data['pasos'], 1):
                paso = PasoPreparacion(
                    receta_id=receta.id,
                    numero_paso=i,
                    descripcion=paso_text
                )
                db.session.add(paso)
            
            # Agregar valor nutricional
            valor = ValorNutricional(
                receta_id=receta.id,
                vitamina_a=50.0,
                vitamina_c=30.0,
                calcio=40.0,
                hierro=2.5,
                potasio=300.0
            )
            db.session.add(valor)
            
            added_count += 1
        
        # Guardar cambios
        if added_count > 0:
            db.session.commit()
            logger.info(f"Se agregaron {added_count} nuevas recetas")
        else:
            logger.info("No se agregaron nuevas recetas")

if __name__ == '__main__':
    add_more_recipes()