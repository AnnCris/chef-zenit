import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import pickle
from app.models import Recipe, Ingredient, NutritionalInfo

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
        
    def train(self):
        """Entrenar el filtro basado en contenido"""
        recipes = Recipe.query.all()
        
        if not recipes:
            print("No hay recetas disponibles para entrenar el filtro de contenido.")
            return
        
        # Preparar datos de contenido textual
        recipe_texts = []
        recipe_features = []
        self.recipe_ids = []
        
        for recipe in recipes:
            # Crear texto descriptivo de la receta
            text_content = self._create_recipe_text(recipe)
            recipe_texts.append(text_content)
            
            # Extraer características numéricas
            features = self._extract_numerical_features(recipe)
            recipe_features.append(features)
            
            self.recipe_ids.append(recipe.id)
        
        # Entrenar TF-IDF en contenido textual
        self.recipe_content_matrix = self.tfidf_vectorizer.fit_transform(recipe_texts)
        
        # Normalizar características numéricas
        features_df = pd.DataFrame(recipe_features)
        features_df = features_df.fillna(0)
        self.feature_names = features_df.columns.tolist()
        self.recipe_features_matrix = self.scaler.fit_transform(features_df)
        
        print(f"Filtro de contenido entrenado con {len(recipes)} recetas.")
    
    def _create_recipe_text(self, recipe):
        """Crear texto descriptivo de la receta"""
        text_parts = []
        
        # Nombre de la receta
        if recipe.name:
            text_parts.append(recipe.name)
        
        # Descripción
        if recipe.description:
            text_parts.append(recipe.description)
        
        # Ingredientes
        if recipe.ingredients:
            ingredients_text = ' '.join([ing.name for ing in recipe.ingredients])
            text_parts.append(ingredients_text)
        
        # Tipo de cocina
        if recipe.cuisine_type:
            text_parts.append(recipe.cuisine_type)
        
        # Dificultad
        if recipe.difficulty:
            text_parts.append(recipe.difficulty)
        
        # Instrucciones (primeras 200 palabras)
        if recipe.instructions:
            instructions_words = recipe.instructions.split()[:200]
            text_parts.append(' '.join(instructions_words))
        
        return ' '.join(text_parts).lower()
    
    def _extract_numerical_features(self, recipe):
        """Extraer características numéricas de la receta"""
        features = {}
        
        # Características básicas
        features['prep_time'] = recipe.prep_time or 30
        features['cook_time'] = recipe.cook_time or 30
        features['total_time'] = (recipe.prep_time or 0) + (recipe.cook_time or 0)
        features['servings'] = recipe.servings or 4
        features['num_ingredients'] = len(recipe.ingredients)
        features['avg_rating'] = recipe.average_rating or 3.0
        features['num_ratings'] = len(recipe.ratings)
        
        # Dificultad (codificación one-hot)
        features['difficulty_easy'] = 1 if recipe.difficulty == 'fácil' else 0
        features['difficulty_medium'] = 1 if recipe.difficulty == 'medio' else 0
        features['difficulty_hard'] = 1 if recipe.difficulty == 'difícil' else 0
        
        # Tipo de cocina (codificación one-hot)
        cuisine_types = ['mexicana', 'italiana', 'asiática', 'mediterránea', 'francesa', 'americana']
        for cuisine in cuisine_types:
            features[f'cuisine_{cuisine}'] = 1 if recipe.cuisine_type == cuisine else 0
        
        # Características nutricionales
        if recipe.nutritional_info:
            nutrition = recipe.nutritional_info
            features['calories'] = nutrition.calories_per_serving or 400
            features['protein'] = nutrition.protein or 15
            features['carbs'] = nutrition.carbs or 50
            features['fat'] = nutrition.fat or 10
            features['fiber'] = nutrition.fiber or 3
            features['sugar'] = nutrition.sugar or 10
            features['sodium'] = nutrition.sodium or 800
            
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
        ingredient_categories = self._categorize_ingredients(recipe.ingredients)
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
            'grains': ['arroz', 'pasta', 'pan', 'harina', 'avena', 'quinoa', 'maíz'],
            'dairy': ['leche', 'queso', 'mantequilla', 'crema', 'yogurt'],
            'spices': ['sal', 'pimienta', 'comino', 'orégano', 'albahaca', 'canela', 'cilantro'],
            'fruits': ['limón', 'naranja', 'manzana', 'plátano', 'fresa', 'aguacate'],
            'fats': ['aceite', 'manteca', 'nuez', 'almendra']
        }
        
        for ingredient in ingredients:
            ingredient_name = ingredient.name.lower()
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
    
    def find_similar_recipes(self, target_recipe_id, n_recommendations=5):
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
        
        # Obtener objetos Recipe
        similar_recipes = Recipe.query.filter(Recipe.id.in_(similar_recipe_ids)).all()
        
        # Ordenar según el orden de similitud
        recipe_order = {recipe_id: i for i, recipe_id in enumerate(similar_recipe_ids)}
        similar_recipes.sort(key=lambda r: recipe_order.get(r.id, float('inf')))
        
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
        
        # Obtener objetos Recipe
        recommended_recipes = Recipe.query.filter(Recipe.id.in_(recommended_recipe_ids)).all()
        
        # Ordenar según similitud
        recipe_order = {recipe_id: i for i, recipe_id in enumerate(recommended_recipe_ids)}
        recommended_recipes.sort(key=lambda r: recipe_order.get(r.id, float('inf')))
        
        return recommended_recipes
    
    def _apply_user_preferences(self, similarities, user_preferences):
        """Aplicar preferencias del usuario para ajustar similitudes"""
        adjusted_similarities = similarities.copy()
        
        for i, recipe_id in enumerate(self.recipe_ids):
            recipe = Recipe.query.get(recipe_id)
            if not recipe:
                continue
            
            # Penalizar recetas que no coinciden con preferencias de tiempo
            if user_preferences.get('max_prep_time'):
                max_time = user_preferences['max_prep_time']
                if recipe.total_time > max_time:
                    adjusted_similarities[i] *= 0.5
            
            # Penalizar recetas que no coinciden con dificultad preferida
            if user_preferences.get('difficulty_preference'):
                if recipe.difficulty != user_preferences['difficulty_preference']:
                    adjusted_similarities[i] *= 0.8
            
            # Bonificar recetas del tipo de cocina preferido
            if user_preferences.get('preferred_cuisines'):
                if recipe.cuisine_type in user_preferences['preferred_cuisines']:
                    adjusted_similarities[i] *= 1.2
        
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
            print(f"Modelo de filtro de contenido guardado en {filepath}")
        except Exception as e:
            print(f"Error guardando modelo: {e}")
    
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
            
            print(f"Modelo de filtro de contenido cargado desde {filepath}")
            return True
        except Exception as e:
            print(f"Error cargando modelo: {e}")
            return False
