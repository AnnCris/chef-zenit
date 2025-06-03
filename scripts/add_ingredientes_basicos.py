import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.ingrediente import Ingrediente

def add_ingredientes_basicos():
    app = create_app()

    with app.app_context():
        ingredientes_a_agregar = [
            {"nombre": "Carne de res", "categoria": "Carnes"},
            {"nombre": "Papa", "categoria": "Verduras"},
            {"nombre": "Cebolla", "categoria": "Verduras"},
            {"nombre": "Ají amarillo", "categoria": "Condimentos"},
            {"nombre": "Comino", "categoria": "Especias"},
            {"nombre": "Orégano", "categoria": "Especias"},
            {"nombre": "Gelatina sin sabor", "categoria": "Otros"},
            {"nombre": "Maní", "categoria": "Frutos secos"},
            {"nombre": "Zanahoria", "categoria": "Verduras"},
            {"nombre": "Fideos", "categoria": "Pastas", "contiene_gluten": True},
            {"nombre": "Aceite", "categoria": "Grasas"},
            {"nombre": "Arroz", "categoria": "Cereales"},
            {"nombre": "Charque", "categoria": "Carnes"},
            {"nombre": "Tomate", "categoria": "Verduras"},
            {"nombre": "Pimentón", "categoria": "Verduras"},
            {"nombre": "Ajo", "categoria": "Condimentos"}
        ]

        existentes = {i.nombre for i in Ingrediente.query.all()}
        nuevos = []

        for ing in ingredientes_a_agregar:
            if ing["nombre"] not in existentes:
                nuevo = Ingrediente(
                    nombre=ing["nombre"],
                    categoria=ing.get("categoria"),
                    es_alergeno=ing.get("es_alergeno", False),
                    contiene_gluten=ing.get("contiene_gluten", False),
                    info_nutricional={}
                )
                nuevos.append(nuevo)

        if nuevos:
            db.session.add_all(nuevos)
            db.session.commit()
            logger.info(f"Se agregaron {len(nuevos)} ingredientes básicos")
        else:
            logger.info("Todos los ingredientes ya estaban presentes")

if __name__ == '__main__':
    add_ingredientes_basicos()
