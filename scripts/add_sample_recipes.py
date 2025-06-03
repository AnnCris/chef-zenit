# scripts/add_sample_recipes.py
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

def add_sample_recipes():
    """
    Agrega recetas de ejemplo a la base de datos
    """
    # Crear una aplicación Flask
    app = create_app()
    
    with app.app_context():
        # Verificar si ya hay recetas
        if Receta.query.count() > 0:
            logger.info("Ya existen recetas en la base de datos")
            return
        
        # Obtener algunos ingredientes
        tomate = Ingrediente.query.filter_by(nombre='Tomate').first()
        cebolla = Ingrediente.query.filter_by(nombre='Cebolla').first()
        lechuga = Ingrediente.query.filter_by(nombre='Lechuga').first()
        pollo = Ingrediente.query.filter_by(nombre='Pollo').first()
        arroz = Ingrediente.query.filter_by(nombre='Arroz').first()
        aceite = Ingrediente.query.filter_by(nombre='Aceite de oliva').first()
        sal = Ingrediente.query.filter_by(nombre='Sal').first()
        pimienta = Ingrediente.query.filter_by(nombre='Pimienta').first()
        
        if not all([tomate, cebolla, lechuga, pollo, arroz, aceite, sal, pimienta]):
            logger.error("No se encuentran todos los ingredientes necesarios")
            return
        
        # Crear receta de ensalada
        ensalada = Receta(
            nombre='Ensalada fresca',
            descripcion='Una ensalada sencilla y refrescante',
            tiempo_preparacion=15,
            porciones=2,
            dificultad='Fácil',
            categoria='Ensaladas',
            calorias=120,
            proteinas=3.5,
            carbohidratos=8.0,
            grasas=6.2
        )
        db.session.add(ensalada)
        db.session.flush()  # Para obtener el ID
        
        # Ingredientes de la ensalada
        ingredientes_ensalada = [
            RecetaIngrediente(receta_id=ensalada.id, ingrediente_id=tomate.id, cantidad=2, unidad='unidades'),
            RecetaIngrediente(receta_id=ensalada.id, ingrediente_id=cebolla.id, cantidad=0.5, unidad='unidad'),
            RecetaIngrediente(receta_id=ensalada.id, ingrediente_id=lechuga.id, cantidad=1, unidad='unidad'),
            RecetaIngrediente(receta_id=ensalada.id, ingrediente_id=aceite.id, cantidad=2, unidad='cucharadas'),
            RecetaIngrediente(receta_id=ensalada.id, ingrediente_id=sal.id, cantidad=1, unidad='pizca'),
            RecetaIngrediente(receta_id=ensalada.id, ingrediente_id=pimienta.id, cantidad=1, unidad='pizca')
        ]
        db.session.add_all(ingredientes_ensalada)
        
        # Pasos de preparación
        pasos_ensalada = [
            PasoPreparacion(receta_id=ensalada.id, numero_paso=1, descripcion='Lavar y cortar la lechuga en trozos pequeños'),
            PasoPreparacion(receta_id=ensalada.id, numero_paso=2, descripcion='Cortar los tomates en cubos'),
            PasoPreparacion(receta_id=ensalada.id, numero_paso=3, descripcion='Picar finamente la cebolla'),
            PasoPreparacion(receta_id=ensalada.id, numero_paso=4, descripcion='Mezclar todos los ingredientes en un bol'),
            PasoPreparacion(receta_id=ensalada.id, numero_paso=5, descripcion='Aliñar con aceite, sal y pimienta')
        ]
        db.session.add_all(pasos_ensalada)
        
        # Información nutricional
        valor_ensalada = ValorNutricional(
            receta_id=ensalada.id,
            vitamina_a=120.5,
            vitamina_c=35.2,
            calcio=45.3,
            hierro=1.2,
            potasio=320.5
        )
        db.session.add(valor_ensalada)
        
        # Crear receta de arroz con pollo
        arroz_pollo = Receta(
            nombre='Arroz con pollo',
            descripcion='Un plato clásico y nutritivo',
            tiempo_preparacion=45,
            porciones=4,
            dificultad='Media',
            categoria='Platos principales',
            calorias=450,
            proteinas=25.0,
            carbohidratos=60.0,
            grasas=10.5
        )
        db.session.add(arroz_pollo)
        db.session.flush()  # Para obtener el ID
        
        # Ingredientes del arroz con pollo
        ingredientes_arroz = [
            RecetaIngrediente(receta_id=arroz_pollo.id, ingrediente_id=pollo.id, cantidad=500, unidad='gramos'),
            RecetaIngrediente(receta_id=arroz_pollo.id, ingrediente_id=arroz.id, cantidad=2, unidad='tazas'),
            RecetaIngrediente(receta_id=arroz_pollo.id, ingrediente_id=cebolla.id, cantidad=1, unidad='unidad'),
            RecetaIngrediente(receta_id=arroz_pollo.id, ingrediente_id=tomate.id, cantidad=2, unidad='unidades'),
            RecetaIngrediente(receta_id=arroz_pollo.id, ingrediente_id=aceite.id, cantidad=3, unidad='cucharadas'),
            RecetaIngrediente(receta_id=arroz_pollo.id, ingrediente_id=sal.id, cantidad=1, unidad='cucharadita'),
            RecetaIngrediente(receta_id=arroz_pollo.id, ingrediente_id=pimienta.id, cantidad=0.5, unidad='cucharadita')
        ]
        db.session.add_all(ingredientes_arroz)
        
        # Pasos de preparación
        pasos_arroz = [
            PasoPreparacion(receta_id=arroz_pollo.id, numero_paso=1, descripcion='Cortar el pollo en trozos y sazonar con sal y pimienta'),
            PasoPreparacion(receta_id=arroz_pollo.id, numero_paso=2, descripcion='Calentar el aceite en una olla y dorar el pollo'),
            PasoPreparacion(receta_id=arroz_pollo.id, numero_paso=3, descripcion='Retirar el pollo y en el mismo aceite, sofreír la cebolla y el tomate'),
            PasoPreparacion(receta_id=arroz_pollo.id, numero_paso=4, descripcion='Añadir el arroz y tostar ligeramente'),
            PasoPreparacion(receta_id=arroz_pollo.id, numero_paso=5, descripcion='Agregar 4 tazas de agua caliente y el pollo'),
            PasoPreparacion(receta_id=arroz_pollo.id, numero_paso=6, descripcion='Cocinar a fuego medio durante unos 20 minutos hasta que el arroz esté tierno')
        ]
        db.session.add_all(pasos_arroz)
        
        # Información nutricional
        valor_arroz = ValorNutricional(
            receta_id=arroz_pollo.id,
            vitamina_a=50.2,
            vitamina_c=18.5,
            calcio=30.1,
            hierro=3.5,
            potasio=450.3
        )
        db.session.add(valor_arroz)
        
        # Guardar cambios
        db.session.commit()
        logger.info("Recetas de ejemplo agregadas correctamente")

if __name__ == '__main__':
    add_sample_recipes()