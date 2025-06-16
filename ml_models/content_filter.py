import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import pickle
import os

class ContentBasedFilter:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words=None,
            ngram_range=(1, 2),
            lowercase=True
        )
        self.recipe_features_matrix = None
        self.recipe_content_matrix = None
        self.scaler = MinMaxScaler()
        self.recipe_ids = []
        self.feature_names = []
        
    def train(self, recipes_data=None):
        """Entrenar el filtro basado en contenido"""
        if recipes_data is None:
            recipes_data = self._generate_sample_data()
        
        if not recipes_data:
            print("No hay recetas disponibles para entrenar el filtro de contenido.")
            return
        
        # Preparar datos de contenido textual
        recipe_texts = []
        recipe_features = []
        self.recipe_ids = []
        
        for recipe in recipes_data:
            # Crear texto descriptivo de la receta
            text_content = self._create_recipe_text(recipe)
            recipe_texts.append(text_content)
            
            # Extraer características numéricas
            features = self._extract_numerical_features(recipe)
            recipe_features.append(features)
            
            self.recipe_ids.append(recipe.get('id', len(self.recipe_ids) + 1))
        
        # Entrenar TF-IDF en contenido textual
        self.recipe_content_matrix = self.tfidf_vectorizer.fit_transform(recipe_texts)
        
        # Normalizar características numéricas
        features_df = pd.DataFrame(recipe_features)
        features_df = features_df.fillna(0)
        self.feature_names = features_df.columns.tolist()
        self.recipe_features_matrix = self.scaler.fit_transform(features_df)
        
        print(f"✅ Filtro de contenido entrenado con {len(recipes_data)} recetas.")
    
    def _generate_sample_data(self):
        """Genera datos de ejemplo para pruebas"""
        sample_recipes = [
            {
                'id': 1,
                'name': 'Arroz con Pollo',
                'description': 'Plato tradicional latino con arroz, pollo y verduras',
                'ingredients': ['arroz', 'pollo', 'cebolla', 'ajo', 'pimiento', 'tomate'],
                'cuisine_type': 'latina',
                'difficulty': 'medio',
                'instructions': 'Sazonar el pollo, dorar, agregar verduras y arroz, cocinar.',
                'prep_time': 15,
                'cook_time': 25,
                'servings': 4,
                'nutritional_info': {
                    'calories_per_serving': 450,
                    'protein': 25,
                    'carbs': 55,
                    'fat': 12,
                    'fiber': 3,
                    'sugar': 6,
                    'sodium': 800
                },
                'ratings': [5, 4, 5, 4],
                'avg_rating': 4.5
            },
            {
                'id': 2,
                'name': 'Ensalada César',
                'description': 'Ensalada fresca con lechuga, queso parmesano y aderezo césar',
                'ingredients': ['lechuga', 'queso', 'ajo', 'limón', 'pan'],
                'cuisine_type': 'italiana',
                'difficulty': 'fácil',
                'instructions': 'Lavar lechuga, preparar aderezo, mezclar, agregar crutones.',
                'prep_time': 10,
                'cook_time': 5,
                'servings': 2,
                'nutritional_info': {
                    'calories_per_serving': 280,
                    'protein': 8,
                    'carbs': 15,
                    'fat': 22,
                    'fiber': 4,
                    'sugar': 3,
                    'sodium': 650
                },
                'ratings': [4, 5, 4],
                'avg_rating': 4.3
            },
            {
                'id': 3,
                'name': 'Sopa de Lentejas',
                'description': 'Sopa nutritiva y reconfortante con lentejas y verduras',
                'ingredients': ['lenteja', 'cebolla', 'ajo', 'zanahoria', 'apio'],
                'cuisine_type': 'mediterránea',
                'difficulty': 'fácil',
                'instructions': 'Remojar lentejas, sofreír verduras, cocinar todo junto.',
                'prep_time': 10,
                'cook_time': 35,
                'servings': 4,
                'nutritional_info': {
                    'calories_per_serving': 320,
                    'protein': 18,
                    'carbs': 45,
                    'fat': 8,
                    'fiber': 12,
                    'sugar': 8,
                    'sodium': 400
                },
                'ratings': [5, 5, 4, 5],
                'avg_rating': 4.7
            },
            {
                'id': 4,
                'name': 'Pasta Primavera',
                'description': 'Pasta fresca con verduras de temporada',
                'ingredients': ['pasta', 'brócoli', 'zanahoria', 'calabaza', 'pimiento'],
                'cuisine_type': 'italiana',
                'difficulty': 'fácil',
                'instructions': 'Cocinar pasta, saltear verduras, mezclar con aceite de oliva.',
                'prep_time': 15,
                'cook_time': 15,
                'servings': 4,
                'nutritional_info': {
                    'calories_per_serving': 365,
                    'protein': 12,
                    'carbs': 58,
                    'fat': 10,
                    'fiber': 8,
                    'sugar': 12,
                    'sodium': 520
                },
                'ratings': [4, 4, 5],
                'avg_rating': 4.3
            },
            {
                'id': 5,
                'name': 'Tacos de Pollo',
                'description': 'Tacos mexicanos con pollo marinado',
                'ingredients': ['pollo', 'tortilla', 'cebolla', 'chile', 'cilantro'],
                'cuisine_type': 'mexicana',
                'difficulty': 'medio',
                'instructions': 'Marinar pollo, cocinar, servir en tortillas con verduras.',
                'prep_time': 20,
                'cook_time': 15,
                'servings': 4,
                'nutritional_info': {
                    'calories_per_serving': 380,
                    'protein': 25,
                    'carbs': 32,
                    'fat': 15,
                    'fiber': 5,
                    'sugar': 4,
                    'sodium': 680
                },
                'ratings': [5, 4, 5],
                'avg_rating': 4.6
            }
        ]
        return sample_recipes
    
    def _create_recipe_text(self, recipe):
        """Crear texto descriptivo de la receta"""
        text_parts = []
        
        # Nombre de la receta
        if recipe.get('name'):
            text_parts.append(recipe['name'])
        
        # Descripción
        if recipe.get('description'):
            text_parts.append(recipe['description'])
        
        # Ingredientes
        if recipe.get('ingredients'):
            ingredients_text = ' '.join(recipe['ingredients'])
            text_parts.append(ingredients_text)
        
        # Tipo de cocina
        if recipe.get('cuisine_type'):
            text_parts.append(recipe['cuisine_type'])
        
        # Dificultad
        if recipe.get('difficulty'):
            text_parts.append(recipe['difficulty'])
        
        # Instrucciones (primeras 200 palabras)
        if recipe.get('instructions'):
            instructions_words = recipe['instructions'].split()[:200]
            text_parts.append(' '.join(instructions_words))
        
        return ' '.join(text_parts).lower()
    
    def _extract_numerical_features(self, recipe):
        """Extraer características numéricas de la receta"""
        features = {}
        
        # Características básicas
        features['prep_time'] = recipe.get('prep_time', 30)
        features['cook_time'] = recipe.get('cook_time', 30)
        features['total_time'] = features['prep_time'] + features['cook_time']
        features['servings'] = recipe.get('servings', 4)
        features['num_ingredients'] = len(recipe.get('ingredients', []))
        features['avg_rating'] = recipe.get('avg_rating', 3.0)
        features['num_ratings'] = len(recipe.get('ratings', []))
        
        # Dificultad (codificación one-hot)
        difficulty = recipe.get('difficulty', 'fácil')
        features['difficulty_easy'] = 1 if difficulty == 'fácil' else 0
        features['difficulty_medium'] = 1 if difficulty == 'medio' else 0
        features['difficulty_hard'] = 1 if difficulty == 'difícil' else 0
        
        # Tipo de cocina (codificación one-hot)
        cuisine_types = ['mexicana', 'italiana', 'asiática', 'mediterránea', 'francesa', 'americana']
        cuisine_type = recipe.get('cuisine_type', '')
        for cuisine in cuisine_types:
            features[f'cuisine_{cuisine}'] = 1 if cuisine_type == cuisine else 0
        
        # Características nutricionales
        nutrition = recipe.get('nutritional_info', {})
        if nutrition:
            features['calories'] = nutrition.get('calories_per_serving', 400)
            features['protein'] = nutrition.get('protein', 15)
            features['carbs'] = nutrition.get('carbs', 50)
            features['fat'] = nutrition.get('fat', 10)
            features['fiber'] = nutrition.get('fiber', 3)
            features['sugar'] = nutrition.get('sugar', 10)
            features['sodium'] = nutrition.get('sodium', 800)
            
            # Ratios nutricionales
            total_calories = features['calories']
            if total_calories > 0:
                features['protein_ratio'] = (features['protein'] * 4) / total_calories
                features['carbs_ratio'] = (features['carbs'] * 4) / total_calories
                features['fat_ratio'] = (features['fat'] * 9) / total_calories
            else:
                features['protein_ratio'] = 0.15
                features['carbs_ratio'] = 0.55
                features['fat_ratio'] = 0.30
        else:
            # Valores por defecto
            default_nutrition = {
                'calories': 400, 'protein': 15, 'carbs': 50, 'fat': 10,
                'fiber': 3, 'sugar': 10, 'sodium': 800,
                'protein_ratio': 0.15, 'carbs_ratio': 0.55, 'fat_ratio': 0.30
            }
            features.update(default_nutrition)
        
        # Categorías de ingredientes
        ingredient_categories = self._categorize_ingredients(recipe.get('ingredients', []))
        features.update(ingredient_categories)
        
        return features
    
    def _categorize_ingredients(self, ingredients):
        """Categorizar ingredientes y contar por tipo"""
        categories = {
            'vegetables_count': 0, 'proteins_count': 0, 'grains_count': 0,
            'dairy_count': 0, 'spices_count': 0, 'fruits_count': 0, 'fats_count': 0
        }
        
        category_keywords = {
            'vegetables': ['tomate', 'cebolla', 'ajo', 'zanahoria', 'apio', 'pimiento', 'chile', 'brócoli', 'espinaca'],
            'proteins': ['pollo', 'carne', 'pescado', 'cerdo', 'huevo', 'frijol', 'lenteja', 'garbanzo', 'tofu'],
            'grains': ['arroz', 'pasta', 'pan', 'harina', 'avena', 'quinoa', 'maíz', 'tortilla'],
            'dairy': ['leche', 'queso', 'mantequilla', 'crema', 'yogurt'],
            'spices': ['sal', 'pimienta', 'comino', 'orégano', 'albahaca', 'canela', 'cilantro'],
            'fruits': ['limón', 'naranja', 'manzana', 'plátano', 'fresa', 'aguacate'],
            'fats': ['aceite', 'manteca', 'nuez', 'almendra']
        }
        
        for ingredient in ingredients:
            ingredient_name = ingredient.lower()
            categorized = False
            
            for category, keywords in category_keywords.items():
                if any(keyword in ingredient_name for keyword in keywords):
                    categories[f'{category}_count'] += 1
                    categorized = True
                    break
        
        return categories
    
    def calculate_similarity(self, query_ingredients, recipe_id):
        """Calcular similitud entre ingredientes de consulta y una receta"""
        if self.recipe_content_matrix is None:
            return 0.0
        
        try:
            # Encontrar índice de la receta
            recipe_idx = self.recipe_ids.index(recipe_id)
        except ValueError:
            return 0.0
        
        # Crear texto de consulta con ingredientes
        query_text = ' '.join(query_ingredients).lower()
        
        # Vectorizar consulta
        query_vector = self.tfidf_vectorizer.transform([query_text])
        
        # Calcular similitud coseno con contenido textual
        recipe_vector = self.recipe_content_matrix[recipe_idx]
        content_similarity = cosine_similarity(query_vector, recipe_vector)[0][0]
        
        return content_similarity
    
    def find_similar_recipes(self, target_recipe_id, recipes_data, n_recommendations=5):
        """Encontrar recetas similares a una receta objetivo"""
        if self.recipe_content_matrix is None or self.recipe_features_matrix is None:
            return []
        
        try:
            target_idx = self.recipe_ids.index(target_recipe_id)
        except ValueError:
            return []
        
        # Combinar similitud de contenido y características
        target_content = self.recipe_content_matrix[target_idx]
        target_features = self.recipe_features_matrix[target_idx].reshape(1, -1)
        
        # Calcular similitudes
        content_similarities = cosine_similarity(target_content, self.recipe_content_matrix)[0]
        feature_similarities = cosine_similarity(target_features, self.recipe_features_matrix)[0]
        
        # Combinar similitudes (70% contenido, 30% características)
        combined_similarities = 0.7 * content_similarities + 0.3 * feature_similarities
        
        # Obtener índices de recetas más similares (excluyendo la receta objetivo)
        similar_indices = np.argsort(combined_similarities)[::-1]
        similar_indices = [idx for idx in similar_indices if idx != target_idx][:n_recommendations]
        
        # Obtener IDs de recetas similares
        similar_recipe_ids = [self.recipe_ids[idx] for idx in similar_indices]
        
        # Filtrar recetas de los datos
        similar_recipes = [recipe for recipe in recipes_data 
                          if recipe.get('id') in similar_recipe_ids]
        
        # Ordenar según el orden de similitud
        recipe_order = {recipe_id: i for i, recipe_id in enumerate(similar_recipe_ids)}
        similar_recipes.sort(key=lambda r: recipe_order.get(r.get('id'), float('inf')))
        
        return similar_recipes
    
    def recommend_by_ingredients(self, ingredients_list, user_preferences=None, n_recommendations=10):
        """Recomendar recetas basadas en lista de ingredientes"""
        if self.recipe_content_matrix is None:
            return []
        
        # Crear consulta con ingredientes
        query_text = ' '.join(ingredients_list).lower()
        query_vector = self.tfidf_vectorizer.transform([query_text])
        
        # Calcular similitudes con todas las recetas
        similarities = cosine_similarity(query_vector, self.recipe_content_matrix)[0]
        
        # Aplicar filtros de preferencias del usuario si se proporcionan
        if user_preferences:
            similarities = self._apply_user_preferences(similarities, user_preferences)
        
        # Obtener índices de recetas más similares
        top_indices = np.argsort(similarities)[::-1][:n_recommendations]
        
        # Obtener IDs de recetas recomendadas
        recommended_recipe_ids = [self.recipe_ids[idx] for idx in top_indices if similarities[idx] > 0.1]
        
        return recommended_recipe_ids
    
    def _apply_user_preferences(self, similarities, user_preferences):
        """Aplicar preferencias del usuario para ajustar similitudes"""
        adjusted_similarities = similarities.copy()
        
        # Ejemplo de aplicación de preferencias
        # Esto se puede expandir según las necesidades
        for i, recipe_id in enumerate(self.recipe_ids):
            # Penalizar según tiempo máximo
            if user_preferences.get('max_prep_time'):
                max_time = user_preferences['max_prep_time']
                # Aquí necesitaríamos acceso a los datos de la receta
                # Por simplicidad, aplicamos un factor general
                if max_time < 30:
                    adjusted_similarities[i] *= 0.8
        
        return adjusted_similarities
    
    def get_recipe_features_importance(self, recipe_id):
        """Obtener la importancia de las características para una receta"""
        if self.recipe_features_matrix is None:
            return {}
        
        try:
            recipe_idx = self.recipe_ids.index(recipe_id)
        except ValueError:
            return {}
        
        recipe_features = self.recipe_features_matrix[recipe_idx]
        
        # Crear diccionario de características con sus valores
        features_dict = {}
        for i, feature_name in enumerate(self.feature_names):
            features_dict[feature_name] = recipe_features[i]
        
        return features_dict
    
    def save_model(self, filepath):
        """Guardar el modelo del filtro de contenido"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'tfidf_vectorizer': self.tfidf_vectorizer,
            'recipe_content_matrix': self.recipe_content_matrix,
            'recipe_features_matrix': self.recipe_features_matrix,
            'scaler': self.scaler,
            'recipe_ids': self.recipe_ids,
            'feature_names': self.feature_names
        }
        
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
            print(f"✅ Modelo de filtro de contenido guardado en {filepath}")
        except Exception as e:
            print(f"❌ Error guardando modelo: {e}")
    
    def load_model(self, filepath):
        """Cargar el modelo del filtro de contenido"""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.tfidf_vectorizer = model_data['tfidf_vectorizer']
            self.recipe_content_matrix = model_data['recipe_content_matrix']
            self.recipe_features_matrix = model_data['recipe_features_matrix']
            self.scaler = model_data['scaler']
            self.recipe_ids = model_data['recipe_ids']
            self.feature_names = model_data['feature_names']
            
            print(f"✅ Modelo de filtro de contenido cargado desde {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            return False
    
    def analyze_model(self):
        """Analizar el modelo entrenado"""
        print("\n📊 Análisis del Filtro de Contenido:")
        print("=" * 50)
        print(f"Número de recetas: {len(self.recipe_ids)}")
        print(f"Características numéricas: {len(self.feature_names)}")
        print(f"Vocabulario TF-IDF: {len(self.tfidf_vectorizer.vocabulary_) if hasattr(self.tfidf_vectorizer, 'vocabulary_') else 0}")
        
        if self.recipe_features_matrix is not None:
            print(f"Forma de matriz de características: {self.recipe_features_matrix.shape}")
        
        if self.recipe_content_matrix is not None:
            print(f"Forma de matriz de contenido: {self.recipe_content_matrix.shape}")


def main():
    """Función principal para probar el filtro de contenido"""
    print("🔍 Iniciando entrenamiento de filtro basado en contenido...")
    
    # Crear instancia del filtro
    content_filter = ContentBasedFilter()
    
    # Entrenar el modelo
    content_filter.train()
    
    # Analizar modelo
    content_filter.analyze_model()
    
    # Guardar modelo
    model_path = "ml_models/trained_models/content_filter_model.pkl"
    content_filter.save_model(model_path)
    
    # Probar recomendaciones por ingredientes
    print("\n🔍 Probando recomendaciones por ingredientes...")
    test_ingredients = ['pollo', 'arroz', 'tomate']
    recommendations = content_filter.recommend_by_ingredients(test_ingredients, n_recommendations=3)
    
    if recommendations:
        print(f"Recomendaciones para {test_ingredients}:")
        for recipe_id in recommendations:
            print(f"- Receta ID: {recipe_id}")
    
    # Probar similitud
    print("\n🔍 Probando similitud entre recetas...")
    sample_data = content_filter._generate_sample_data()
    similar_recipes = content_filter.find_similar_recipes(1, sample_data, 3)
    
    if similar_recipes:
        print("Recetas similares a 'Arroz con Pollo':")
        for recipe in similar_recipes:
            print(f"- {recipe['name']} (Rating: {recipe['avg_rating']})")
    
    # Probar carga del modelo
    print("\n🔄 Probando carga del modelo...")
    new_filter = ContentBasedFilter()
    if new_filter.load_model(model_path):
        print("✅ Modelo cargado correctamente para verificación")
        
        # Probar funcionalidad con modelo cargado
        test_similarity = new_filter.calculate_similarity(['arroz', 'pollo'], 1)
        print(f"Similitud de prueba: {test_similarity:.3f}")


if __name__ == "__main__":
    main()