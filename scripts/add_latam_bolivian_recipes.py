# scripts/add_latam_bolivian_recipes.py
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

def add_latam_bolivian_recipes():
    app = create_app()

    with app.app_context():
        existing_count = Receta.query.count()
        logger.info(f"Recetas existentes: {existing_count}")

        ingredientes = {ing.nombre: ing for ing in Ingrediente.query.all()}

        if not ingredientes:
            logger.error("No hay ingredientes en la base de datos")
            return

        recetas_data = [
            {
                'nombre': 'Salteñas',
                'descripcion': 'Empanadas jugosas típicas de Bolivia con carne y papa.',
                'tiempo_preparacion': 90,
                'porciones': 6,
                'dificultad': 'Alta',
                'categoria': 'Empanadas',
                'calorias': 450,
                'proteinas': 18.0,
                'carbohidratos': 40.0,
                'grasas': 20.0,
                'ingredientes': [
                    {'nombre': 'Carne de res', 'cantidad': 300, 'unidad': 'gramos'},
                    {'nombre': 'Papa', 'cantidad': 2, 'unidad': 'unidades'},
                    {'nombre': 'Cebolla', 'cantidad': 1, 'unidad': 'unidad'},
                    {'nombre': 'Ají amarillo', 'cantidad': 1, 'unidad': 'unidad'},
                    {'nombre': 'Comino', 'cantidad': 1, 'unidad': 'cucharadita'},
                    {'nombre': 'Orégano', 'cantidad': 1, 'unidad': 'cucharadita'},
                    {'nombre': 'Gelatina sin sabor', 'cantidad': 1, 'unidad': 'sobre'}
                ],
                'pasos': [
                    'Picar la carne, cebolla y papa en cubos pequeños.',
                    'Cocinar con ají, comino, orégano hasta que estén cocidos.',
                    'Agregar la gelatina para que la mezcla se solidifique al enfriar.',
                    'Preparar la masa con harina y margarina.',
                    'Rellenar con la mezcla y cerrar las salteñas.',
                    'Hornear por 20 minutos a 200°C.'
                ]
            },
            {
                'nombre': 'Sopa de Maní',
                'descripcion': 'Sopa tradicional boliviana con maní, carne y papas.',
                'tiempo_preparacion': 60,
                'porciones': 4,
                'dificultad': 'Media',
                'categoria': 'Sopas',
                'calorias': 500,
                'proteinas': 22.0,
                'carbohidratos': 45.0,
                'grasas': 25.0,
                'ingredientes': [
                    {'nombre': 'Maní', 'cantidad': 100, 'unidad': 'gramos'},
                    {'nombre': 'Carne de res', 'cantidad': 400, 'unidad': 'gramos'},
                    {'nombre': 'Papa', 'cantidad': 3, 'unidad': 'unidades'},
                    {'nombre': 'Zanahoria', 'cantidad': 1, 'unidad': 'unidad'},
                    {'nombre': 'Fideos', 'cantidad': 100, 'unidad': 'gramos'},
                    {'nombre': 'Cebolla', 'cantidad': 1, 'unidad': 'unidad'},
                    {'nombre': 'Aceite', 'cantidad': 2, 'unidad': 'cucharadas'}
                ],
                'pasos': [
                    'Licuar el maní tostado con agua.',
                    'Cocinar la carne y cebolla en aceite.',
                    'Agregar zanahoria y papa en cubos.',
                    'Incorporar la mezcla de maní y hervir.',
                    'Agregar fideos y cocinar hasta que estén suaves.'
                ]
            },
            {
                'nombre': 'Majadito Cruceño',
                'descripcion': 'Plato oriental de arroz con charque o carne desmenuzada.',
                'tiempo_preparacion': 45,
                'porciones': 4,
                'dificultad': 'Media',
                'categoria': 'Arroces',
                'calorias': 480,
                'proteinas': 24.0,
                'carbohidratos': 50.0,
                'grasas': 18.0,
                'ingredientes': [
                    {'nombre': 'Arroz', 'cantidad': 300, 'unidad': 'gramos'},
                    {'nombre': 'Charque', 'cantidad': 250, 'unidad': 'gramos'},
                    {'nombre': 'Tomate', 'cantidad': 2, 'unidad': 'unidades'},
                    {'nombre': 'Pimentón', 'cantidad': 1, 'unidad': 'unidad'},
                    {'nombre': 'Cebolla', 'cantidad': 1, 'unidad': 'unidad'},
                    {'nombre': 'Ajo', 'cantidad': 2, 'unidad': 'dientes'}
                ],
                'pasos': [
                    'Desmenuzar el charque cocido.',
                    'Freír cebolla, ajo, tomate y pimentón.',
                    'Agregar arroz y sofreír.',
                    'Incorporar agua y cocinar hasta que el arroz esté listo.',
                    'Añadir el charque y mezclar bien.'
                ]
            }
        ]

        added_count = 0
        for receta_data in recetas_data:
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
            db.session.flush()

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

            for i, paso_text in enumerate(receta_data['pasos'], 1):
                paso = PasoPreparacion(
                    receta_id=receta.id,
                    numero_paso=i,
                    descripcion=paso_text
                )
                db.session.add(paso)

            valor = ValorNutricional(
                receta_id=receta.id,
                vitamina_a=60.0,
                vitamina_c=20.0,
                calcio=30.0,
                hierro=3.0,
                potasio=350.0
            )
            db.session.add(valor)

            added_count += 1

        if added_count > 0:
            db.session.commit()
            logger.info(f"Se agregaron {added_count} nuevas recetas")
        else:
            logger.info("No se agregaron nuevas recetas")

if __name__ == '__main__':
    add_latam_bolivian_recipes()