from app import create_app
from app.models import db, User, Recipe, Ingredient, DietaryRestriction, NutritionalInfo
from flask_migrate import upgrade
import os

app = create_app()

@app.cli.command()
def init_db():
    """Inicializar la base de datos con datos de ejemplo"""
    print("Inicializando base de datos...")
    
    # Crear todas las tablas
    db.create_all()
    
    # Crear restricciones dietéticas básicas
    restrictions = [
        ('vegetariano', 'Dieta que excluye carne y pescado'),
        ('vegano', 'Dieta que excluye todos los productos de origen animal'),
        ('sin gluten', 'Dieta libre de gluten para personas celíacas'),
        ('sin lactosa', 'Dieta libre de lactosa para intolerantes'),
        ('diabético', 'Dieta adecuada para personas con diabetes'),
        ('bajo sodio', 'Dieta baja en sodio para hipertensión'),
        ('paleo', 'Dieta paleolítica'),
        ('keto', 'Dieta cetogénica baja en carbohidratos')
    ]
    
    for name, description in restrictions:
        if not DietaryRestriction.query.filter_by(name=name).first():
            restriction = DietaryRestriction(name=name, description=description)
            db.session.add(restriction)
    
    # Crear ingredientes básicos
    basic_ingredients = [
        # Verduras
        ('tomate', 'vegetables'), ('cebolla', 'vegetables'), ('ajo', 'vegetables'),
        ('zanahoria', 'vegetables'), ('apio', 'vegetables'), ('pimiento', 'vegetables'),
        ('chile', 'vegetables'), ('calabaza', 'vegetables'), ('brócoli', 'vegetables'),
        ('espinaca', 'vegetables'), ('lechuga', 'vegetables'), ('pepino', 'vegetables'),
        
        # Proteínas
        ('pollo', 'proteins'), ('carne de res', 'proteins'), ('pescado', 'proteins'),
        ('cerdo', 'proteins'), ('huevo', 'proteins'), ('frijol', 'proteins'),
        ('lenteja', 'proteins'), ('garbanzo', 'proteins'), ('tofu', 'proteins'),
        
        # Cereales y granos
        ('arroz', 'grains'), ('pasta', 'grains'), ('pan', 'grains'),
        ('harina', 'grains'), ('avena', 'grains'), ('quinoa', 'grains'),
        ('maíz', 'grains'),
        
        # Lácteos
        ('leche', 'dairy'), ('queso', 'dairy'), ('mantequilla', 'dairy'),
        ('crema', 'dairy'), ('yogurt', 'dairy'),
        
        # Especias y condimentos
        ('sal', 'spices'), ('pimienta', 'spices'), ('comino', 'spices'),
        ('orégano', 'spices'), ('albahaca', 'spices'), ('canela', 'spices'),
        ('cilantro', 'spices'), ('perejil', 'spices'), ('ají', 'spices'),
        
        # Frutas
        ('limón', 'fruits'), ('naranja', 'fruits'), ('manzana', 'fruits'),
        ('plátano', 'fruits'), ('fresa', 'fruits'), ('aguacate', 'fruits'),
        
        # Grasas y aceites
        ('aceite de oliva', 'fats'), ('aceite', 'fats'), ('manteca', 'fats'),
        ('nuez', 'fats'), ('almendra', 'fats')
    ]
    
    for name, category in basic_ingredients:
        if not Ingredient.query.filter_by(name=name).first():
            ingredient = Ingredient(name=name, category=category)
            db.session.add(ingredient)
    
    # Crear recetas de ejemplo
    sample_recipes = [
        {
            'name': 'Arroz con Pollo',
            'description': 'Plato tradicional latino con arroz, pollo y verduras',
            'instructions': '1. Sazonar el pollo con sal y pimienta. 2. Dorar el pollo en aceite caliente. 3. Agregar cebolla, ajo y pimiento. 4. Añadir arroz y caldo. 5. Cocinar por 20 minutos.',
            'prep_time': 15,
            'cook_time': 25,
            'servings': 4,
            'difficulty': 'medio',
            'cuisine_type': 'latina',
            'ingredients': ['arroz', 'pollo', 'cebolla', 'ajo', 'pimiento', 'sal', 'aceite'],
            'nutrition': {
                'calories_per_serving': 450,
                'protein': 25,
                'carbs': 55,
                'fat': 12,
                'fiber': 3,
                'sodium': 800
            }
        },
        {
            'name': 'Ensalada César',
            'description': 'Ensalada fresca con lechuga, queso parmesano y aderezo césar',
            'instructions': '1. Lavar y cortar la lechuga. 2. Preparar el aderezo mezclando mayonesa, ajo, limón y queso. 3. Mezclar la lechuga con el aderezo. 4. Agregar crutones y queso.',
            'prep_time': 10,
            'cook_time': 0,
            'servings': 2,
            'difficulty': 'fácil',
            'cuisine_type': 'italiana',
            'ingredients': ['lechuga', 'queso', 'ajo', 'limón', 'pan'],
            'nutrition': {
                'calories_per_serving': 280,
                'protein': 8,
                'carbs': 15,
                'fat': 22,
                'fiber': 4,
                'sodium': 650
            }
        },
        {
            'name': 'Sopa de Lentejas',
            'description': 'Sopa nutritiva y reconfortante con lentejas y verduras',
            'instructions': '1. Remojar las lentejas por 2 horas. 2. Sofreír cebolla, ajo y zanahoria. 3. Agregar las lentejas y caldo. 4. Cocinar por 30 minutos. 5. Sazonar al gusto.',
            'prep_time': 10,
            'cook_time': 35,
            'servings': 4,
            'difficulty': 'fácil',
            'cuisine_type': 'mediterránea',
            'ingredients': ['lenteja', 'cebolla', 'ajo', 'zanahoria', 'apio', 'sal'],
            'nutrition': {
                'calories_per_serving': 320,
                'protein': 18,
                'carbs': 45,
                'fat': 8,
                'fiber': 12,
                'sodium': 400
            }
        }
    ]
    
    for recipe_data in sample_recipes:
        if not Recipe.query.filter_by(name=recipe_data['name']).first():
            recipe = Recipe(
                name=recipe_data['name'],
                description=recipe_data['description'],
                instructions=recipe_data['instructions'],
                prep_time=recipe_data['prep_time'],
                cook_time=recipe_data['cook_time'],
                servings=recipe_data['servings'],
                difficulty=recipe_data['difficulty'],
                cuisine_type=recipe_data['cuisine_type']
            )
            
            # Agregar ingredientes
            for ingredient_name in recipe_data['ingredients']:
                ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
                if ingredient:
                    recipe.ingredients.append(ingredient)
            
            db.session.add(recipe)
            db.session.flush()  # Para obtener el ID de la receta
            
            # Agregar información nutricional
            if 'nutrition' in recipe_data:
                nutrition = NutritionalInfo(
                    recipe_id=recipe.id,
                    **recipe_data['nutrition']
                )
                db.session.add(nutrition)
    
    # Crear usuario administrador
    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            email='admin@sistema-culinario.com'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
    
    try:
        db.session.commit()
        print("Base de datos inicializada exitosamente!")
        print("Usuario admin creado - username: admin, password: admin123")
    except Exception as e:
        db.session.rollback()
        print(f"Error inicializando base de datos: {e}")

@app.cli.command()
def train_ml_models():
    """Entrenar los modelos de machine learning"""
    print("Entrenando modelos de machine learning...")
    
    try:
        from ml_models.recommendation_engine import RecommendationEngine
        from ml_models.clustering import RecipeClustering
        
        # Entrenar sistema de recomendaciones
        print("Entrenando sistema de recomendaciones...")
        rec_engine = RecommendationEngine()
        rec_engine.train_models()
        
        # Entrenar clustering
        print("Entrenando modelo de clustering...")
        clustering = RecipeClustering()
        clustering.train_clustering()
        
        print("Modelos entrenados exitosamente!")
        
    except Exception as e:
        print(f"Error entrenando modelos: {e}")

@app.cli.command()
def create_sample_user():
    """Crear usuario de ejemplo para pruebas"""
    username = input("Nombre de usuario: ")
    email = input("Email: ")
    password = input("Contraseña: ")
    
    if User.query.filter_by(username=username).first():
        print("El usuario ya existe")
        return
    
    user = User(username=username, email=email)
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        print(f"Usuario {username} creado exitosamente!")
    except Exception as e:
        db.session.rollback()
        print(f"Error creando usuario: {e}")

if __name__ == '__main__':
    # Verificar si la base de datos existe
    if not os.path.exists('instance'):
        os.makedirs('instance')
    
    with app.app_context():
        # Verificar si las tablas existen
        try:
            # Intentar una consulta simple
            User.query.first()
        except Exception as e:
            print("Base de datos no inicializada. Ejecuta: flask init-db")
    
    app.run(debug=True, host='0.0.0.0', port=5000)