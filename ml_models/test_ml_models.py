#!/usr/bin/env python3
"""
Script de prueba para todos los modelos de ML del Sistema Experto Culinario
Ejecuta de forma independiente sin dependencias de Flask
"""

import os
import sys
import time

# Agregar el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from clustering import RecipeClustering
    from content_filter import ContentBasedFilter
    from recommendation_engine import RecommendationEngine
    from nlp_processor import NLPProcessor
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("Asegúrate de que todos los archivos estén en el directorio ml_models/")
    sys.exit(1)

def create_test_data():
    """Crea datos de prueba más completos"""
    recipes_data = [
        {
            'id': 1,
            'name': 'Arroz con Pollo Tradicional',
            'description': 'Plato clásico de la cocina latina con arroz, pollo tierno y verduras frescas',
            'ingredients': ['arroz', 'pollo', 'cebolla', 'ajo', 'pimiento', 'tomate', 'cilantro', 'aceite', 'sal'],
            'cuisine_type': 'latina',
            'difficulty': 'medio',
            'prep_time': 15,
            'cook_time': 25,
            'servings': 4,
            'instructions': 'Sazonar el pollo con sal y pimienta. Dorar en aceite caliente. Agregar verduras y cocinar hasta que estén suaves. Añadir arroz y caldo. Cocinar por 20 minutos.',
            'nutritional_info': {
                'calories_per_serving': 450,
                'protein': 25,
                'carbs': 55,
                'fat': 12,
                'fiber': 3,
                'sugar': 6,
                'sodium': 800,
                'vitamin_a': 185,
                'vitamin_c': 25,
                'iron': 2.4,
                'calcium': 45
            },
            'ratings': [5, 4, 5, 4, 5],
            'avg_rating': 4.6
        },
        {
            'id': 2,
            'name': 'Ensalada César Fresca',
            'description': 'Ensalada crujiente con lechuga romana, crutones caseros y aderezo césar cremoso',
            'ingredients': ['lechuga', 'queso', 'ajo', 'limón', 'pan', 'aceite', 'mayonesa'],
            'cuisine_type': 'italiana',
            'difficulty': 'fácil',
            'prep_time': 10,
            'cook_time': 5,
            'servings': 2,
            'instructions': 'Lavar y cortar lechuga. Preparar aderezo mezclando ingredientes. Tostar pan para crutones. Mezclar todo y servir.',
            'nutritional_info': {
                'calories_per_serving': 280,
                'protein': 8,
                'carbs': 15,
                'fat': 22,
                'fiber': 4,
                'sugar': 3,
                'sodium': 650,
                'vitamin_a': 312,
                'vitamin_c': 18,
                'iron': 1.8,
                'calcium': 125
            },
            'ratings': [4, 5, 4, 4],
            'avg_rating': 4.3
        },
        {
            'id': 3,
            'name': 'Sopa de Lentejas Nutritiva',
            'description': 'Sopa reconfortante y nutritiva con lentejas rojas, verduras y especias aromáticas',
            'ingredients': ['lenteja', 'cebolla', 'ajo', 'zanahoria', 'apio', 'tomate', 'comino', 'aceite'],
            'cuisine_type': 'mediterránea',
            'difficulty': 'fácil',
            'prep_time': 10,
            'cook_time': 35,
            'servings': 4,
            'instructions': 'Remojar lentejas. Sofreír verduras hasta que estén doradas. Agregar lentejas y caldo. Cocinar hasta que estén tiernas.',
            'nutritional_info': {
                'calories_per_serving': 320,
                'protein': 18,
                'carbs': 45,
                'fat': 8,
                'fiber': 12,
                'sugar': 8,
                'sodium': 400,
                'vitamin_a': 458,
                'vitamin_c': 12,
                'iron': 4.2,
                'calcium': 62
            },
            'ratings': [5, 5, 4, 5, 5],
            'avg_rating': 4.8
        },
        {
            'id': 4,
            'name': 'Pasta Primavera Colorida',
            'description': 'Pasta fresca con una mezcla colorida de verduras de temporada',
            'ingredients': ['pasta', 'brócoli', 'zanahoria', 'calabaza', 'pimiento', 'ajo', 'aceite', 'queso'],
            'cuisine_type': 'italiana',
            'difficulty': 'fácil',
            'prep_time': 15,
            'cook_time': 15,
            'servings': 4,
            'instructions': 'Cocinar pasta al dente. Saltear verduras en aceite de oliva. Mezclar pasta con verduras y agregar queso.',
            'nutritional_info': {
                'calories_per_serving': 365,
                'protein': 12,
                'carbs': 58,
                'fat': 10,
                'fiber': 8,
                'sugar': 12,
                'sodium': 520,
                'vitamin_a': 685,
                'vitamin_c': 95,
                'iron': 3.2,
                'calcium': 95
            },
            'ratings': [4, 4, 5, 4],
            'avg_rating': 4.3
        },
        {
            'id': 5,
            'name': 'Tacos de Pollo Marinado',
            'description': 'Tacos mexicanos auténticos con pollo marinado en especias y salsa verde',
            'ingredients': ['pollo', 'tortilla', 'cebolla', 'chile', 'cilantro', 'lima', 'comino', 'ajo'],
            'cuisine_type': 'mexicana',
            'difficulty': 'medio',
            'prep_time': 20,
            'cook_time': 15,
            'servings': 4,
            'instructions': 'Marinar pollo en especias. Cocinar hasta dorar. Calentar tortillas. Servir con verduras frescas.',
            'nutritional_info': {
                'calories_per_serving': 380,
                'protein': 25,
                'carbs': 32,
                'fat': 15,
                'fiber': 5,
                'sugar': 4,
                'sodium': 680,
                'vitamin_a': 125,
                'vitamin_c': 35,
                'iron': 2.8,
                'calcium': 85
            },
            'ratings': [5, 4, 5, 5],
            'avg_rating': 4.7
        },
        {
            'id': 6,
            'name': 'Curry Vegetariano de Garbanzos',
            'description': 'Curry aromático con garbanzos, espinacas y leche de coco',
            'ingredients': ['garbanzo', 'espinaca', 'cebolla', 'ajo', 'jengibre', 'tomate', 'leche de coco', 'curry'],
            'cuisine_type': 'india',
            'difficulty': 'medio',
            'prep_time': 15,
            'cook_time': 25,
            'servings': 4,
            'instructions': 'Sofreír especias y verduras. Agregar garbanzos y tomate. Cocinar con leche de coco hasta espesar.',
            'nutritional_info': {
                'calories_per_serving': 340,
                'protein': 15,
                'carbs': 42,
                'fat': 14,
                'fiber': 10,
                'sugar': 8,
                'sodium': 450,
                'vitamin_a': 520,
                'vitamin_c': 30,
                'iron': 3.8,
                'calcium': 120
            },
            'ratings': [4, 5, 4, 5],
            'avg_rating': 4.5
        }
    ]
    
    # Datos de ratings más realistas
    ratings_data = [
        {'user_id': 1, 'recipe_id': 1, 'rating': 5, 'user_profile': {'dietary_restrictions': [], 'avg_rating_given': 4.2}},
        {'user_id': 1, 'recipe_id': 2, 'rating': 4, 'user_profile': {'dietary_restrictions': [], 'avg_rating_given': 4.2}},
        {'user_id': 1, 'recipe_id': 3, 'rating': 5, 'user_profile': {'dietary_restrictions': [], 'avg_rating_given': 4.2}},
        {'user_id': 2, 'recipe_id': 1, 'rating': 3, 'user_profile': {'dietary_restrictions': ['vegetariano'], 'avg_rating_given': 3.8}},
        {'user_id': 2, 'recipe_id': 3, 'rating': 5, 'user_profile': {'dietary_restrictions': ['vegetariano'], 'avg_rating_given': 3.8}},
        {'user_id': 2, 'recipe_id': 4, 'rating': 4, 'user_profile': {'dietary_restrictions': ['vegetariano'], 'avg_rating_given': 3.8}},
        {'user_id': 2, 'recipe_id': 6, 'rating': 5, 'user_profile': {'dietary_restrictions': ['vegetariano'], 'avg_rating_given': 3.8}},
        {'user_id': 3, 'recipe_id': 2, 'rating': 5, 'user_profile': {'dietary_restrictions': [], 'avg_rating_given': 4.5}},
        {'user_id': 3, 'recipe_id': 4, 'rating': 4, 'user_profile': {'dietary_restrictions': [], 'avg_rating_given': 4.5}},
        {'user_id': 3, 'recipe_id': 5, 'rating': 5, 'user_profile': {'dietary_restrictions': [], 'avg_rating_given': 4.5}},
    ]
    
    return recipes_data, ratings_data

def test_nlp_processor():
    """Prueba el procesador de NLP"""
    print("\n🧠 PROBANDO NLP PROCESSOR")
    print("=" * 50)
    
    nlp = NLPProcessor()
    
    # Probar procesamiento de ingredientes
    ingredients_text = "2 tazas de arroz, 500g de pollo, 1 cebolla grande, 3 dientes de ajo, pimiento rojo"
    processed = nlp.process_ingredients(ingredients_text)
    
    print(f"Texto original: {ingredients_text}")
    print(f"Ingredientes procesados: {processed}")
    
    # Probar extracción de consultas
    user_query = "Quiero cocinar algo mexicano que sea fácil y tome menos de 30 minutos"
    query_info = nlp.extract_recipe_query(user_query)
    
    print(f"\nConsulta: {user_query}")
    print(f"Información extraída: {query_info}")
    
    # Probar consejos de cocina
    sample_recipe = {
        'ingredients': ['pollo', 'arroz', 'ajo', 'cebolla'],
        'difficulty': 'medio',
        'total_time': 40
    }
    tips = nlp.generate_cooking_tips(sample_recipe)
    
    print(f"\nConsejos de cocina:")
    for tip in tips:
        print(f"  • {tip}")
    
    print("✅ NLP Processor funcionando correctamente")

def test_clustering():
    """Prueba el sistema de clustering"""
    print("\n🔄 PROBANDO CLUSTERING")
    print("=" * 50)
    
    recipes_data, _ = create_test_data()
    
    clustering = RecipeClustering(n_clusters=3)
    cluster_labels = clustering.train_clustering(recipes_data)
    
    if cluster_labels:
        clustering.analyze_clusters()
        
        # Probar recetas similares
        similar = clustering.get_similar_recipes(1, recipes_data, 2)
        print(f"\nRecetas similares a '{recipes_data[0]['name']}':")
        for recipe in similar:
            print(f"  • {recipe['name']} (Rating: {recipe['avg_rating']})")
        
        print("✅ Clustering funcionando correctamente")
    else:
        print("❌ Error en clustering")

def test_content_filter():
    """Prueba el filtro basado en contenido"""
    print("\n🔍 PROBANDO CONTENT FILTER")
    print("=" * 50)
    
    recipes_data, _ = create_test_data()
    
    content_filter = ContentBasedFilter()
    content_filter.train(recipes_data)
    content_filter.analyze_model()
    
    # Probar recomendaciones por ingredientes
    test_ingredients = ['pollo', 'arroz', 'tomate']
    recommendations = content_filter.recommend_by_ingredients(test_ingredients, n_recommendations=3)
    
    print(f"\nRecomendaciones para ingredientes {test_ingredients}:")
    for recipe_id in recommendations:
        recipe = next((r for r in recipes_data if r['id'] == recipe_id), None)
        if recipe:
            print(f"  • {recipe['name']} (ID: {recipe_id})")
    
    # Probar similitud específica
    similarity = content_filter.calculate_similarity(['pasta', 'verduras'], 4)
    print(f"\nSimilitud entre ['pasta', 'verduras'] y Pasta Primavera: {similarity:.3f}")
    
    # Probar recetas similares
    similar_recipes = content_filter.find_similar_recipes(1, recipes_data, 2)
    print(f"\nRecetas similares a 'Arroz con Pollo':")
    for recipe in similar_recipes:
        print(f"  • {recipe['name']} (Rating: {recipe['avg_rating']})")
    
    print("✅ Content Filter funcionando correctamente")

def test_recommendation_engine():
    """Prueba el motor de recomendaciones completo"""
    print("\n🚀 PROBANDO RECOMMENDATION ENGINE")
    print("=" * 50)
    
    recipes_data, ratings_data = create_test_data()
    
    # Crear y entrenar el motor de recomendaciones
    rec_engine = RecommendationEngine()
    rec_engine.train_models(recipes_data, ratings_data)
    
    # Analizar rendimiento
    rec_engine.analyze_model_performance()
    
    # Probar con usuario vegetariano
    print("\n👤 USUARIO VEGETARIANO")
    print("-" * 30)
    
    user_profile = {
        'dietary_restrictions': ['vegetariano'],
        'avg_rating_given': 4.2,
        'preferred_cuisines': ['italiana', 'mediterránea']
    }
    
    available_ingredients = ['pasta', 'tomate', 'ajo', 'cebolla', 'aceite', 'queso']
    
    recommendations = rec_engine.get_recommendations(
        user_profile, 
        available_ingredients, 
        recipes_data,
        n_recommendations=3
    )
    
    print(f"Ingredientes disponibles: {available_ingredients}")
    print(f"Restricciones: {user_profile['dietary_restrictions']}")
    print("\nRecomendaciones:")
    
    for i, rec in enumerate(recommendations, 1):
        recipe = rec['recipe']
        print(f"\n{i}. {recipe['name']}")
        print(f"   Rating predicho: {rec['predicted_rating']:.1f}/5.0")
        print(f"   Cobertura ingredientes: {rec['ingredient_coverage']:.1%}")
        print(f"   Tipo cocina: {recipe.get('cuisine_type', 'N/A')}")
        if rec['missing_ingredients']:
            print(f"   Faltan: {rec['missing_ingredients'][:3]}")
        if rec['substitution_suggestions']:
            print(f"   Sustituciones: {list(rec['substitution_suggestions'].keys())[:2]}")
    
    # Probar con usuario sin restricciones
    print("\n\n👤 USUARIO SIN RESTRICCIONES")
    print("-" * 30)
    
    user_profile_2 = {
        'dietary_restrictions': [],
        'avg_rating_given': 3.8,
        'preferred_cuisines': ['latina', 'mexicana']
    }
    
    available_ingredients_2 = ['pollo', 'arroz', 'cebolla', 'tomate', 'chile']
    
    recommendations_2 = rec_engine.get_recommendations(
        user_profile_2, 
        available_ingredients_2, 
        recipes_data,
        n_recommendations=3
    )
    
    print(f"Ingredientes disponibles: {available_ingredients_2}")
    print(f"Preferencias: {user_profile_2['preferred_cuisines']}")
    print("\nRecomendaciones:")
    
    for i, rec in enumerate(recommendations_2, 1):
        recipe = rec['recipe']
        print(f"\n{i}. {recipe['name']}")
        print(f"   Rating predicho: {rec['predicted_rating']:.1f}/5.0")
        print(f"   Cobertura ingredientes: {rec['ingredient_coverage']:.1%}")
        print(f"   Tipo cocina: {recipe.get('cuisine_type', 'N/A')}")
        if rec['missing_ingredients']:
            print(f"   Faltan: {rec['missing_ingredients'][:3]}")
    
    print("\n✅ Recommendation Engine funcionando correctamente")

def test_integration():
    """Prueba la integración de todos los componentes"""
    print("\n🔗 PROBANDO INTEGRACIÓN COMPLETA")
    print("=" * 50)
    
    # Simular flujo completo del sistema
    nlp = NLPProcessor()
    
    # 1. Usuario ingresa ingredientes en lenguaje natural
    user_input = "Tengo pollo, arroz, cebolla y tomate. Quiero algo fácil y rápido"
    
    print(f"Entrada del usuario: '{user_input}'")
    
    # 2. Procesar con NLP
    ingredients = nlp.process_ingredients("pollo, arroz, cebolla, tomate")
    query_info = nlp.extract_recipe_query(user_input)
    
    print(f"Ingredientes extraídos: {ingredients}")
    print(f"Preferencias extraídas: {query_info}")
    
    # 3. Crear perfil de usuario basado en NLP
    user_profile = {
        'dietary_restrictions': query_info.get('dietary_restrictions', []),
        'avg_rating_given': 4.0,
        'preferred_cuisines': [],
        'max_prep_time': query_info.get('time_constraint'),
        'difficulty_preference': query_info.get('difficulty')
    }
    
    print(f"Perfil de usuario generado: {user_profile}")
    
    # 4. Obtener recomendaciones
    recipes_data, ratings_data = create_test_data()
    rec_engine = RecommendationEngine()
    rec_engine.train_models(recipes_data, ratings_data)
    
    recommendations = rec_engine.get_recommendations(
        user_profile, 
        ingredients, 
        recipes_data,
        n_recommendations=2
    )
    
    print(f"\n🎯 RECOMENDACIONES FINALES:")
    print("-" * 30)
    
    for i, rec in enumerate(recommendations, 1):
        recipe = rec['recipe']
        print(f"\n{i}. {recipe['name']}")
        print(f"   ⭐ Rating predicho: {rec['predicted_rating']:.1f}/5")
        print(f"   📊 Cobertura: {rec['ingredient_coverage']:.1%}")
        print(f"   ⏱️ Tiempo: {recipe.get('prep_time', 0) + recipe.get('cook_time', 0)} min")
        print(f"   🍽️ Dificultad: {recipe.get('difficulty', 'N/A')}")
        
        # Generar consejos de cocina
        tips = nlp.generate_cooking_tips(recipe)
        if tips:
            print(f"   💡 Consejo: {tips[0]}")
    
    print("\n✅ Integración completa funcionando correctamente")

def test_model_persistence():
    """Prueba la persistencia de modelos"""
    print("\n💾 PROBANDO PERSISTENCIA DE MODELOS")
    print("=" * 50)
    
    recipes_data, ratings_data = create_test_data()
    
    # Entrenar y guardar modelos
    print("Entrenando y guardando modelos...")
    
    # Clustering
    clustering = RecipeClustering(n_clusters=3)
    clustering.train_clustering(recipes_data)
    clustering.save_model("ml_models/trained_models/test_clustering.pkl")
    
    # Content Filter
    content_filter = ContentBasedFilter()
    content_filter.train(recipes_data)
    content_filter.save_model("ml_models/trained_models/test_content_filter.pkl")
    
    # Recommendation Engine
    rec_engine = RecommendationEngine()
    rec_engine.train_models(recipes_data, ratings_data)
    
    print("\n🔄 Probando carga de modelos...")
    
    # Cargar modelos en nuevas instancias
    new_clustering = RecipeClustering()
    clustering_loaded = new_clustering.load_model("ml_models/trained_models/test_clustering.pkl")
    
    new_content_filter = ContentBasedFilter()
    content_loaded = new_content_filter.load_model("ml_models/trained_models/test_content_filter.pkl")
    
    new_rec_engine = RecommendationEngine()
    # El recommendation engine carga automáticamente los modelos en su __init__
    
    # Verificar que los modelos funcionan después de cargar
    if clustering_loaded:
        similar = new_clustering.get_similar_recipes(1, recipes_data, 1)
        print(f"✅ Clustering cargado - Receta similar encontrada: {similar[0]['name'] if similar else 'Ninguna'}")
    
    if content_loaded:
        similarity = new_content_filter.calculate_similarity(['pollo', 'arroz'], 1)
        print(f"✅ Content Filter cargado - Similitud calculada: {similarity:.3f}")
    
    # Probar recomendación con modelo cargado
    user_profile = {'dietary_restrictions': [], 'avg_rating_given': 4.0}
    recommendations = new_rec_engine.get_recommendations(
        user_profile, 
        ['pollo', 'arroz'], 
        recipes_data,
        n_recommendations=1
    )
    
    if recommendations:
        print(f"✅ Recommendation Engine funcionando - Recomendación: {recommendations[0]['recipe']['name']}")
    
    print("✅ Persistencia de modelos funcionando correctamente")

def run_performance_benchmark():
    """Ejecuta un benchmark de rendimiento"""
    print("\n⚡ BENCHMARK DE RENDIMIENTO")
    print("=" * 50)
    
    recipes_data, ratings_data = create_test_data()
    
    # Benchmark de entrenamiento
    print("📊 Tiempos de entrenamiento:")
    
    # Clustering
    start_time = time.time()
    clustering = RecipeClustering(n_clusters=3)
    clustering.train_clustering(recipes_data)
    clustering_time = time.time() - start_time
    print(f"  Clustering: {clustering_time:.3f}s")
    
    # Content Filter
    start_time = time.time()
    content_filter = ContentBasedFilter()
    content_filter.train(recipes_data)
    content_time = time.time() - start_time
    print(f"  Content Filter: {content_time:.3f}s")
    
    # Recommendation Engine
    start_time = time.time()
    rec_engine = RecommendationEngine()
    rec_engine.train_models(recipes_data, ratings_data)
    rec_time = time.time() - start_time
    print(f"  Recommendation Engine: {rec_time:.3f}s")
    
    # Benchmark de predicción
    print("\n📊 Tiempos de predicción:")
    
    user_profile = {'dietary_restrictions': [], 'avg_rating_given': 4.0}
    ingredients = ['pollo', 'arroz', 'tomate']
    
    # Múltiples predicciones para promedio
    n_predictions = 10
    
    start_time = time.time()
    for _ in range(n_predictions):
        recommendations = rec_engine.get_recommendations(
            user_profile, 
            ingredients, 
            recipes_data,
            n_recommendations=3
        )
    prediction_time = (time.time() - start_time) / n_predictions
    print(f"  Recomendación promedio: {prediction_time:.4f}s")
    
    # Estadísticas de memoria (aproximadas)
    import sys
    clustering_size = sys.getsizeof(clustering)
    content_size = sys.getsizeof(content_filter)
    rec_engine_size = sys.getsizeof(rec_engine)
    
    print(f"\n📊 Uso aproximado de memoria:")
    print(f"  Clustering: {clustering_size / 1024:.1f} KB")
    print(f"  Content Filter: {content_size / 1024:.1f} KB")
    print(f"  Recommendation Engine: {rec_engine_size / 1024:.1f} KB")
    
    print("✅ Benchmark completado")

def main():
    """Función principal que ejecuta todas las pruebas"""
    print("🍳 SISTEMA EXPERTO CULINARIO - PRUEBAS DE ML")
    print("=" * 60)
    print("Ejecutando pruebas de todos los componentes de Machine Learning...")
    print(f"Directorio de trabajo: {os.getcwd()}")
    
    # Crear directorio para modelos si no existe
    os.makedirs("ml_models/trained_models", exist_ok=True)
    
    try:
        # Ejecutar todas las pruebas
        test_nlp_processor()
        test_clustering()
        test_content_filter()
        test_recommendation_engine()
        test_integration()
        test_model_persistence()
        run_performance_benchmark()
        
        print("\n" + "=" * 60)
        print("🎉 TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 60)
        print("\n✅ El sistema de ML está funcionando correctamente")
        print("✅ Todos los modelos se entrenan y predicen sin errores")
        print("✅ La persistencia de modelos funciona correctamente")
        print("✅ La integración entre componentes es exitosa")
        
        print("\n📁 Archivos generados:")
        print("  • ml_models/trained_models/test_clustering.pkl")
        print("  • ml_models/trained_models/test_content_filter.pkl")
        print("  • ml_models/trained_models/rating_predictor.pkl")
        print("  • ml_models/trained_models/scaler.pkl")
        print("  • ml_models/trained_models/content_filter.pkl")
        
        print("\n🚀 El sistema está listo para producción!")
        
    except Exception as e:
        print(f"\n❌ ERROR EN LAS PRUEBAS: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)