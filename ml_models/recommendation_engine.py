import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import pickle
import os
from app.models import Recipe, User, RecipeRating, Ingredient, NutritionalInfo

class RecommendationEngine:
    def __init__(self):
        self.content_filter = ContentBasedFilter()
        self.rating_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.model_path = 'ml_models/trained_models/'
        
        # Cargar modelos entrenados si existen
        self.load_models()
    
    def train_models(self):
        """Entrena los modelos de machine learning"""
        print("Entrenando modelos de recomendación...")
        
        # Preparar datos para entrenamiento
        recipe_features, ratings_data = self._prepare_training_data()
        
        if len(ratings_data) > 0:
            # Entrenar modelo de predicción de ratings
            self._train_rating_predictor(recipe_features, ratings_data)
        
        # Entrenar filtro basado en contenido
        self.content_filter.train()
        
        # Guardar modelos
        self.save_models()
        print("Modelos entrenados y guardados exitosamente.")
    
    def _prepare_training_data(self):
        """Prepara los datos para entrenamiento"""
        recipes = Recipe.query.all()
        ratings = RecipeRating.query.all()
        
        # Crear características de recetas
        recipe_features = []
        for recipe in recipes:
            features = self._extract_recipe_features(recipe)
            recipe_features.append(features)
        
        recipe_df = pd.DataFrame(recipe_features)
        
        # Crear dataset de ratings
        ratings_data = []
        for rating in ratings:
            recipe_features = self._extract_recipe_features(rating.recipe)
            user_features = self._extract_user_features(rating.user)
            
            combined_features = {**recipe_features, **user_features}
            combined_features['rating'] = rating.rating
            ratings_data.append(combined_features)
        
        return recipe_df, pd.DataFrame(ratings_data)
    
    def _extract_recipe_features(self, recipe):
        """Extrae características numéricas de una receta"""
        features = {
            'recipe_id': recipe.id,
            'prep_time': recipe.prep_time or 0,
            'cook_time': recipe.cook_time or 0,
            'total_time': recipe.total_time,
            'servings': recipe.servings or 4,
            'num_ingredients': len(recipe.ingredients),
            'difficulty_easy': 1 if recipe.difficulty == 'fácil' else 0,
            'difficulty_medium': 1 if recipe.difficulty == 'medio' else 0,
            'difficulty_hard': 1 if recipe.difficulty == 'difícil' else 0,
            'cuisine_mexican': 1 if recipe.cuisine_type == 'mexicana' else 0,
            'cuisine_italian': 1 if recipe.cuisine_type == 'italiana' else 0,
            'cuisine_asian': 1 if recipe.cuisine_type == 'asiática' else 0,
            'avg_rating': recipe.average_rating
        }
        
        # Características nutricionales
        if recipe.nutritional_info:
            nutrition = recipe.nutritional_info
            features.update({
                'calories': nutrition.calories_per_serving or 0,
                'protein': nutrition.protein or 0,
                'carbs': nutrition.carbs or 0,
                'fat': nutrition.fat or 0,
                'fiber': nutrition.fiber or 0,
                'sugar': nutrition.sugar or 0,
                'sodium': nutrition.sodium or 0
            })
        else:
            # Valores por defecto si no hay información nutricional
            features.update({
                'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0,
                'fiber': 0, 'sugar': 0, 'sodium': 0
            })
        
        return features
    
    def _extract_user_features(self, user):
        """Extrae características del usuario"""
        features = {
            'user_id': user.id,
            'has_dietary_restrictions': len(user.dietary_restrictions) > 0,
            'num_ratings': len(user.recipe_ratings),
            'avg_rating_given': np.mean([r.rating for r in user.recipe_ratings]) if user.recipe_ratings else 3.0
        }
        
        # Preferencias del usuario
        if user.user_preferences:
            pref = user.user_preferences[0]
            features.update({
                'max_prep_time': pref.max_prep_time or 60,
                'prefers_easy': 1 if pref.difficulty_preference == 'fácil' else 0,
                'prefers_medium': 1 if pref.difficulty_preference == 'medio' else 0,
                'prefers_hard': 1 if pref.difficulty_preference == 'difícil' else 0
            })
        else:
            features.update({
                'max_prep_time': 60,
                'prefers_easy': 0,
                'prefers_medium': 0,
                'prefers_hard': 0
            })
        
        return features
    
    def _train_rating_predictor(self, recipe_features, ratings_data):
        """Entrena el modelo de predicción de ratings"""
        if len(ratings_data) < 10:  # Necesitamos datos suficientes
            print("Insuficientes datos de rating para entrenar el modelo.")
            return
        
        # Preparar características para entrenamiento
        feature_columns = [col for col in ratings_data.columns if col != 'rating']
        X = ratings_data[feature_columns].fillna(0)
        y = ratings_data['rating']
        
        # Escalar características
        X_scaled = self.scaler.fit_transform(X)
        
        # Entrenar modelo
        self.rating_predictor.fit(X_scaled, y)
        
        # Calcular accuracy
        score = self.rating_predictor.score(X_scaled, y)
        print(f"Accuracy del modelo de rating: {score:.3f}")
    
    def rank_recipes(self, recipes, user_id, available_ingredients):
        """Rankea recetas usando machine learning"""
        if not recipes:
            return []
        
        user = User.query.get(user_id)
        if not user:
            return recipes
        
        scored_recipes = []
        
        for recipe in recipes:
            # Calcular score basado en contenido
            content_score = self.content_filter.calculate_similarity(recipe, available_ingredients)
            
            # Predecir rating del usuario para esta receta
            predicted_rating = self._predict_user_rating(user, recipe)
            
            # Calcular score de cobertura de ingredientes
            coverage_score = self._calculate_ingredient_coverage(recipe, available_ingredients)
            
            # Score combinado (ponderado)
            combined_score = (
                0.4 * content_score +
                0.3 * predicted_rating / 5.0 +  # Normalizar rating a 0-1
                0.3 * coverage_score
            )
            
            scored_recipes.append((recipe, combined_score))
        
        # Ordenar por score descendente
        scored_recipes.sort(key=lambda x: x[1], reverse=True)
        
        return [recipe for recipe, score in scored_recipes]
    
    def _predict_user_rating(self, user, recipe):
        """Predice el rating que un usuario daría a una receta"""
        try:
            # Extraer características
            recipe_features = self._extract_recipe_features(recipe)
            user_features = self._extract_user_features(user)
            
            # Combinar características
            combined_features = {**recipe_features, **user_features}
            
            # Crear DataFrame con las características
            feature_df = pd.DataFrame([combined_features])
            
            # Remover columnas de ID y rating si existen
            feature_columns = [col for col in feature_df.columns 
                             if col not in ['recipe_id', 'user_id', 'rating']]
            X = feature_df[feature_columns].fillna(0)
            
            # Predecir si el modelo está entrenado
            if hasattr(self.rating_predictor, 'feature_importances_'):
                X_scaled = self.scaler.transform(X)
                predicted_rating = self.rating_predictor.predict(X_scaled)[0]
                return max(1, min(5, predicted_rating))  # Asegurar que esté entre 1-5
            else:
                # Si no hay modelo entrenado, usar rating promedio de la receta
                return recipe.average_rating or 3.0
                
        except Exception as e:
            print(f"Error prediciendo rating: {e}")
            return 3.0  # Rating neutral por defecto
    
    def _calculate_ingredient_coverage(self, recipe, available_ingredients):
        """Calcula qué porcentaje de ingredientes de la receta están disponibles"""
        if not recipe.ingredients:
            return 0.0
        
        available_set = set(ing.lower().strip() for ing in available_ingredients)
        recipe_ingredients = set(ing.name.lower() for ing in recipe.ingredients)
        
        if not recipe_ingredients:
            return 0.0
        
        intersection = available_set.intersection(recipe_ingredients)
        return len(intersection) / len(recipe_ingredients)
    
    def save_models(self):
        """Guarda los modelos entrenados"""
        os.makedirs(self.model_path, exist_ok=True)
        
        # Guardar modelo de rating predictor
        if hasattr(self.rating_predictor, 'feature_importances_'):
            with open(f"{self.model_path}rating_predictor.pkl", 'wb') as f:
                pickle.dump(self.rating_predictor, f)
        
        # Guardar scaler
        if hasattr(self.scaler, 'scale_'):
            with open(f"{self.model_path}scaler.pkl", 'wb') as f:
                pickle.dump(self.scaler, f)
        
        # Guardar filtro de contenido
        self.content_filter.save_model(f"{self.model_path}content_filter.pkl")
    
    def load_models(self):
        """Carga modelos previamente entrenados"""
        try:
            # Cargar rating predictor
            rating_path = f"{self.model_path}rating_predictor.pkl"
            if os.path.exists(rating_path):
                with open(rating_path, 'rb') as f:
                    self.rating_predictor = pickle.load(f)
            
            # Cargar scaler
            scaler_path = f"{self.model_path}scaler.pkl"
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
            
            # Cargar filtro de contenido
            content_path = f"{self.model_path}content_filter.pkl"
            if os.path.exists(content_path):
                self.content_filter.load_model(content_path)
                
        except Exception as e:
            print(f"Error cargando modelos: {e}")

class ContentBasedFilter:
    """Filtro basado en contenido usando TF-IDF y similitud coseno"""
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words=None,  # Definiremos stop words en español
            ngram_range=(1, 2)
        )
        self.recipe_tfidf_matrix = None
        self.recipe_texts = {}
    
    def train(self):
        """Entrena el filtro basado en contenido"""
        recipes = Recipe.query.all()
        
        if not recipes:
            print("No hay recetas disponibles para entrenar el filtro de contenido.")
            return
        
        # Crear textos descriptivos para cada receta
        recipe_documents = []
        for recipe in recipes:
            text = self._create_recipe_text(recipe)
            self.recipe_texts[recipe.id] = text
            recipe_documents.append(text)
        
        # Entrenar TF-IDF
        self.recipe_tfidf_matrix = self.tfidf_vectorizer.fit_transform(recipe_documents)
        print(f"Filtro de contenido entrenado con {len(recipes)} recetas.")
    
    def _create_recipe_text(self, recipe):
        """Crea un texto descriptivo de la receta para TF-IDF"""
        text_parts = []
        
        # Nombre de la receta
        text_parts.append(recipe.name)
        
        # Ingredientes
        ingredients = ' '.join([ing.name for ing in recipe.ingredients])
        text_parts.append(ingredients)
        
        # Tipo de cocina
        if recipe.cuisine_type:
            text_parts.append(recipe.cuisine_type)
        
        # Dificultad
        if recipe.difficulty:
            text_parts.append(recipe.difficulty)
        
        # Descripción
        if recipe.description:
            text_parts.append(recipe.description)
        
        return ' '.join(text_parts).lower()
    
    def calculate_similarity(self, recipe, available_ingredients):
        """Calcula similitud entre receta e ingredientes disponibles"""
        if self.recipe_tfidf_matrix is None:
            return 0.0
        
        try:
            # Crear texto de ingredientes disponibles
            ingredients_text = ' '.join(available_ingredients).lower()
            
            # Vectorizar ingredientes disponibles
            ingredients_vector = self.tfidf_vectorizer.transform([ingredients_text])
            
            # Encontrar índice de la receta
            recipe_idx = None
            recipes = Recipe.query.all()
            for idx, r in enumerate(recipes):
                if r.id == recipe.id:
                    recipe_idx = idx
                    break
            
            if recipe_idx is None:
                return 0.0
            
            # Calcular similitud coseno
            recipe_vector = self.recipe_tfidf_matrix[recipe_idx]
            similarity = cosine_similarity(ingredients_vector, recipe_vector)[0][0]
            
            return similarity
            
        except Exception as e:
            print(f"Error calculando similitud: {e}")
            return 0.0
    
    def save_model(self, filepath):
        """Guarda el modelo de filtro de contenido"""
        try:
            model_data = {
                'vectorizer': self.tfidf_vectorizer,
                'tfidf_matrix': self.recipe_tfidf_matrix,
                'recipe_texts': self.recipe_texts
            }
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
        except Exception as e:
            print(f"Error guardando filtro de contenido: {e}")
    
    def load_model(self, filepath):
        """Carga el modelo de filtro de contenido"""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.tfidf_vectorizer = model_data['vectorizer']
            self.recipe_tfidf_matrix = model_data['tfidf_matrix']
            self.recipe_texts = model_data['recipe_texts']
            
        except Exception as e:
            print(f"Error cargando filtro de contenido: {e}")