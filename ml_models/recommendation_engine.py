import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import pickle
import os

class RecommendationEngine:
    def __init__(self):
        self.content_filter = ContentBasedFilter()
        self.rating_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.model_path = 'ml_models/trained_models/'
        self.is_trained = False
        
        # Cargar modelos entrenados si existen
        self.load_models()
    
    def train_models(self, recipes_data=None, ratings_data=None):
        """Entrena los modelos de machine learning"""
        print("🧠 Entrenando modelos de recomendación...")
        
        # Usar datos de ejemplo si no se proporcionan
        if recipes_data is None:
            recipes_data = self._generate_sample_recipes()
        if ratings_data is None:
            ratings_data = self._generate_sample_ratings()
        
        # Preparar datos para entrenamiento
        recipe_features, ratings_df = self._prepare_training_data(recipes_data, ratings_data)
        
        if len(ratings_df) > 0:
            # Entrenar modelo de predicción de ratings
            self._train_rating_predictor(recipe_features, ratings_df)
        
        # Entrenar filtro basado en contenido
        self.content_filter.train(recipes_data)
        
        # Guardar modelos
        self.save_models()
        self.is_trained = True
        print("✅ Modelos entrenados y guardados exitosamente.")
    
    def _generate_sample_recipes(self):
        """Genera datos de ejemplo de recetas"""
        return [
            {
                'id': 1,
                'name': 'Arroz con Pollo',
                'description': 'Plato tradicional latino con arroz, pollo y verduras',
                'ingredients': ['arroz', 'pollo', 'cebolla', 'ajo', 'pimiento', 'tomate'],
                'cuisine_type': 'latina',
                'difficulty': 'medio',
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
                'avg_rating': 4.5
            },
            {
                'id': 2,
                'name': 'Ensalada César',
                'description': 'Ensalada fresca con lechuga y aderezo césar',
                'ingredients': ['lechuga', 'queso', 'ajo', 'limón', 'pan'],
                'cuisine_type': 'italiana',
                'difficulty': 'fácil',
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
                'avg_rating': 4.3
            },
            {
                'id': 3,
                'name': 'Sopa de Lentejas',
                'description': 'Sopa nutritiva con lentejas y verduras',
                'ingredients': ['lenteja', 'cebolla', 'ajo', 'zanahoria', 'apio'],
                'cuisine_type': 'mediterránea',
                'difficulty': 'fácil',
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
                'avg_rating': 4.7
            }
        ]
    
    def _generate_sample_ratings(self):
        """Genera datos de ejemplo de ratings"""
        return [
            {'user_id': 1, 'recipe_id': 1, 'rating': 5, 'user_profile': {'dietary_restrictions': [], 'avg_rating_given': 4.2}},
            {'user_id': 1, 'recipe_id': 2, 'rating': 4, 'user_profile': {'dietary_restrictions': [], 'avg_rating_given': 4.2}},
            {'user_id': 2, 'recipe_id': 1, 'rating': 4, 'user_profile': {'dietary_restrictions': ['vegetariano'], 'avg_rating_given': 3.8}},
            {'user_id': 2, 'recipe_id': 3, 'rating': 5, 'user_profile': {'dietary_restrictions': ['vegetariano'], 'avg_rating_given': 3.8}},
            {'user_id': 3, 'recipe_id': 2, 'rating': 5, 'user_profile': {'dietary_restrictions': [], 'avg_rating_given': 4.5}},
            {'user_id': 3, 'recipe_id': 3, 'rating': 5, 'user_profile': {'dietary_restrictions': [], 'avg_rating_given': 4.5}}
        ]
    
    def _prepare_training_data(self, recipes_data, ratings_data):
        """Prepara los datos para entrenamiento"""
        # Crear características de recetas
        recipe_features = []
        for recipe in recipes_data:
            features = self._extract_recipe_features(recipe)
            recipe_features.append(features)
        
        recipe_df = pd.DataFrame(recipe_features)
        
        # Crear dataset de ratings
        ratings_list = []
        for rating in ratings_data:
            # Encontrar la receta correspondiente
            recipe = next((r for r in recipes_data if r['id'] == rating['recipe_id']), None)
            if recipe:
                recipe_features = self._extract_recipe_features(recipe)
                user_features = self._extract_user_features(rating['user_profile'])
                
                combined_features = {**recipe_features, **user_features}
                combined_features['rating'] = rating['rating']
                ratings_list.append(combined_features)
        
        return recipe_df, pd.DataFrame(ratings_list)
    
    def _extract_recipe_features(self, recipe):
        """Extrae características numéricas de una receta"""
        features = {
            'recipe_id': recipe.get('id', 0),
            'prep_time': recipe.get('prep_time', 0),
            'cook_time': recipe.get('cook_time', 0),
            'total_time': (recipe.get('prep_time', 0) + recipe.get('cook_time', 0)),
            'servings': recipe.get('servings', 4),
            'num_ingredients': len(recipe.get('ingredients', [])),
            'difficulty_easy': 1 if recipe.get('difficulty') == 'fácil' else 0,
            'difficulty_medium': 1 if recipe.get('difficulty') == 'medio' else 0,
            'difficulty_hard': 1 if recipe.get('difficulty') == 'difícil' else 0,
            'cuisine_mexican': 1 if recipe.get('cuisine_type') == 'mexicana' else 0,
            'cuisine_italian': 1 if recipe.get('cuisine_type') == 'italiana' else 0,
            'cuisine_asian': 1 if recipe.get('cuisine_type') == 'asiática' else 0,
            'cuisine_mediterranean': 1 if recipe.get('cuisine_type') == 'mediterránea' else 0,
            'cuisine_latin': 1 if recipe.get('cuisine_type') == 'latina' else 0,
            'avg_rating': recipe.get('avg_rating', 3.0)
        }
        
        # Características nutricionales
        nutrition = recipe.get('nutritional_info', {})
        if nutrition:
            features.update({
                'calories': nutrition.get('calories_per_serving', 0),
                'protein': nutrition.get('protein', 0),
                'carbs': nutrition.get('carbs', 0),
                'fat': nutrition.get('fat', 0),
                'fiber': nutrition.get('fiber', 0),
                'sugar': nutrition.get('sugar', 0),
                'sodium': nutrition.get('sodium', 0)
            })
        else:
            # Valores por defecto si no hay información nutricional
            features.update({
                'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0,
                'fiber': 0, 'sugar': 0, 'sodium': 0
            })
        
        return features
    
    def _extract_user_features(self, user_profile):
        """Extrae características del usuario"""
        features = {
            'has_dietary_restrictions': len(user_profile.get('dietary_restrictions', [])) > 0,
            'avg_rating_given': user_profile.get('avg_rating_given', 3.0),
            'is_vegetarian': 'vegetariano' in user_profile.get('dietary_restrictions', []),
            'is_vegan': 'vegano' in user_profile.get('dietary_restrictions', []),
            'gluten_free': 'sin gluten' in user_profile.get('dietary_restrictions', [])
        }
        
        return features
    
    def _train_rating_predictor(self, recipe_features, ratings_data):
        """Entrena el modelo de predicción de ratings"""
        if len(ratings_data) < 5:  # Necesitamos datos suficientes
            print("⚠️ Insuficientes datos de rating para entrenar el modelo.")
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
        print(f"✅ Accuracy del modelo de rating: {score:.3f}")
    
    def rank_recipes(self, recipes, user_profile, available_ingredients):
        """Rankea recetas usando machine learning"""
        if not recipes:
            return []
        
        if not self.is_trained:
            print("⚠️ Modelos no entrenados. Usando ranking básico.")
            return self._basic_ranking(recipes, available_ingredients)
        
        scored_recipes = []
        
        for recipe in recipes:
            # Calcular score basado en contenido
            content_score = self._calculate_content_score(recipe, available_ingredients)
            
            # Predecir rating del usuario para esta receta
            predicted_rating = self._predict_user_rating(user_profile, recipe)
            
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
    
    def _basic_ranking(self, recipes, available_ingredients):
        """Ranking básico cuando los modelos ML no están disponibles"""
        scored_recipes = []
        
        for recipe in recipes:
            # Score simple basado en cobertura de ingredientes y rating
            coverage = self._calculate_ingredient_coverage(recipe, available_ingredients)
            rating = recipe.get('avg_rating', 3.0)
            
            # Score combinado simple
            score = 0.6 * coverage + 0.4 * (rating / 5.0)
            scored_recipes.append((recipe, score))
        
        # Ordenar por score descendente
        scored_recipes.sort(key=lambda x: x[1], reverse=True)
        return [recipe for recipe, score in scored_recipes]
    
    def _calculate_content_score(self, recipe, available_ingredients):
        """Calcula score basado en similitud de contenido"""
        try:
            return self.content_filter.calculate_similarity(available_ingredients, recipe.get('id', 0))
        except:
            # Fallback simple
            recipe_ingredients = set(ing.lower() for ing in recipe.get('ingredients', []))
            available_set = set(ing.lower() for ing in available_ingredients)
            intersection = recipe_ingredients.intersection(available_set)
            return len(intersection) / len(recipe_ingredients) if recipe_ingredients else 0
    
    def _predict_user_rating(self, user_profile, recipe):
        """Predice el rating que un usuario daría a una receta"""
        try:
            # Extraer características
            recipe_features = self._extract_recipe_features(recipe)
            user_features = self._extract_user_features(user_profile)
            
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
                return recipe.get('avg_rating', 3.0)
                
        except Exception as e:
            print(f"⚠️ Error prediciendo rating: {e}")
            return 3.0  # Rating neutral por defecto
    
    def _calculate_ingredient_coverage(self, recipe, available_ingredients):
        """Calcula qué porcentaje de ingredientes de la receta están disponibles"""
        recipe_ingredients = recipe.get('ingredients', [])
        if not recipe_ingredients:
            return 0.0
        
        available_set = set(ing.lower().strip() for ing in available_ingredients)
        recipe_ingredients_set = set(ing.lower() for ing in recipe_ingredients)
        
        if not recipe_ingredients_set:
            return 0.0
        
        intersection = available_set.intersection(recipe_ingredients_set)
        return len(intersection) / len(recipe_ingredients_set)
    
    def get_recommendations(self, user_profile, available_ingredients, recipes_data=None, n_recommendations=10):
        """Obtiene recomendaciones personalizadas para un usuario"""
        if recipes_data is None:
            recipes_data = self._generate_sample_recipes()
        
        # Filtrar recetas por restricciones dietéticas
        filtered_recipes = self._apply_dietary_filters(recipes_data, user_profile)
        
        # Rankear recetas
        ranked_recipes = self.rank_recipes(filtered_recipes, user_profile, available_ingredients)
        
        # Agregar información adicional a cada recomendación
        enhanced_recommendations = []
        for recipe in ranked_recipes[:n_recommendations]:
            recommendation = {
                'recipe': recipe,
                'ingredient_coverage': self._calculate_ingredient_coverage(recipe, available_ingredients),
                'predicted_rating': self._predict_user_rating(user_profile, recipe),
                'missing_ingredients': self._get_missing_ingredients(recipe, available_ingredients),
                'substitution_suggestions': self._get_substitution_suggestions(recipe, available_ingredients)
            }
            enhanced_recommendations.append(recommendation)
        
        return enhanced_recommendations
    
    def _apply_dietary_filters(self, recipes, user_profile):
        """Aplica filtros de restricciones dietéticas"""
        dietary_restrictions = user_profile.get('dietary_restrictions', [])
        
        if not dietary_restrictions:
            return recipes
        
        filtered_recipes = []
        for recipe in recipes:
            is_compatible = True
            
            for restriction in dietary_restrictions:
                if not self._recipe_meets_restriction(recipe, restriction):
                    is_compatible = False
                    break
            
            if is_compatible:
                filtered_recipes.append(recipe)
        
        return filtered_recipes
    
    def _recipe_meets_restriction(self, recipe, restriction):
        """Verifica si una receta cumple con una restricción dietética"""
        recipe_ingredients = [ing.lower() for ing in recipe.get('ingredients', [])]
        ingredients_text = ' '.join(recipe_ingredients)
        
        if restriction == 'vegetariano':
            forbidden = ['pollo', 'carne', 'pescado', 'cerdo', 'pavo']
            return not any(item in ingredients_text for item in forbidden)
        
        elif restriction == 'vegano':
            forbidden = ['pollo', 'carne', 'pescado', 'huevo', 'leche', 'queso', 'mantequilla']
            return not any(item in ingredients_text for item in forbidden)
        
        elif restriction == 'sin gluten':
            forbidden = ['harina', 'trigo', 'pan', 'pasta']
            return not any(item in ingredients_text for item in forbidden)
        
        elif restriction == 'sin lactosa':
            forbidden = ['leche', 'queso', 'mantequilla', 'crema', 'yogurt']
            return not any(item in ingredients_text for item in forbidden)
        
        return True
    
    def _get_missing_ingredients(self, recipe, available_ingredients):
        """Obtiene lista de ingredientes faltantes"""
        available_set = set(ing.lower().strip() for ing in available_ingredients)
        recipe_ingredients = set(ing.lower() for ing in recipe.get('ingredients', []))
        
        missing = recipe_ingredients - available_set
        return list(missing)
    
    def _get_substitution_suggestions(self, recipe, available_ingredients):
        """Obtiene sugerencias de sustitución para ingredientes faltantes"""
        missing_ingredients = self._get_missing_ingredients(recipe, available_ingredients)
        
        # Sustituciones básicas
        substitutions = {
            'leche': ['leche de almendra', 'leche de soja'],
            'mantequilla': ['aceite de oliva', 'margarina'],
            'huevo': ['linaza molida + agua', 'aquafaba'],
            'queso': ['levadura nutricional', 'queso vegano'],
            'pollo': ['tofu', 'seitán', 'tempeh'],
            'carne': ['lentejas', 'frijoles', 'quinoa'],
            'harina de trigo': ['harina de arroz', 'harina de almendra'],
            'azúcar': ['stevia', 'miel', 'jarabe de maple']
        }
        
        suggestions = {}
        for ingredient in missing_ingredients:
            if ingredient in substitutions:
                suggestions[ingredient] = substitutions[ingredient]
        
        return suggestions
    
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
        
        print(f"✅ Modelos guardados en: {self.model_path}")
    
    def load_models(self):
        """Carga modelos previamente entrenados"""
        try:
            # Cargar rating predictor
            rating_path = f"{self.model_path}rating_predictor.pkl"
            if os.path.exists(rating_path):
                with open(rating_path, 'rb') as f:
                    self.rating_predictor = pickle.load(f)
                    print("✅ Rating predictor cargado")
            
            # Cargar scaler
            scaler_path = f"{self.model_path}scaler.pkl"
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                    print("✅ Scaler cargado")
            
            # Cargar filtro de contenido
            content_path = f"{self.model_path}content_filter.pkl"
            if os.path.exists(content_path):
                if self.content_filter.load_model(content_path):
                    print("✅ Content filter cargado")
                    self.is_trained = True
                    
        except Exception as e:
            print(f"⚠️ Error cargando modelos: {e}")
    
    def analyze_model_performance(self, test_data=None):
        """Analiza el rendimiento del modelo"""
        if not self.is_trained:
            print("⚠️ Modelos no entrenados para análisis")
            return
        
        print("\n📊 Análisis de Rendimiento del Motor de Recomendaciones:")
        print("=" * 60)
        
        # Analizar filtro de contenido
        if hasattr(self.content_filter, 'recipe_ids'):
            print(f"Recetas en filtro de contenido: {len(self.content_filter.recipe_ids)}")
        
        # Analizar predictor de ratings
        if hasattr(self.rating_predictor, 'feature_importances_'):
            print("Top 5 características más importantes para predicción de ratings:")
            # Esto requeriría conocer los nombres de las características
            importances = self.rating_predictor.feature_importances_
            top_indices = np.argsort(importances)[-5:][::-1]
            for i, idx in enumerate(top_indices):
                print(f"  {i+1}. Característica {idx}: {importances[idx]:.3f}")


class ContentBasedFilter:
    """Versión simplificada del filtro de contenido para el motor de recomendaciones"""
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words=None,
            ngram_range=(1, 2)
        )
        self.recipe_tfidf_matrix = None
        self.recipe_texts = {}
        self.recipe_ids = []
    
    def train(self, recipes_data):
        """Entrena el filtro basado en contenido"""
        if not recipes_data:
            print("⚠️ No hay recetas disponibles para entrenar el filtro de contenido.")
            return
        
        # Crear textos descriptivos para cada receta
        recipe_documents = []
        self.recipe_ids = []
        
        for recipe in recipes_data:
            text = self._create_recipe_text(recipe)
            self.recipe_texts[recipe['id']] = text
            recipe_documents.append(text)
            self.recipe_ids.append(recipe['id'])
        
        # Entrenar TF-IDF
        self.recipe_tfidf_matrix = self.tfidf_vectorizer.fit_transform(recipe_documents)
        print(f"✅ Filtro de contenido entrenado con {len(recipes_data)} recetas.")
    
    def _create_recipe_text(self, recipe):
        """Crea un texto descriptivo de la receta para TF-IDF"""
        text_parts = []
        
        # Nombre de la receta
        text_parts.append(recipe.get('name', ''))
        
        # Ingredientes
        ingredients = ' '.join(recipe.get('ingredients', []))
        text_parts.append(ingredients)
        
        # Tipo de cocina
        if recipe.get('cuisine_type'):
            text_parts.append(recipe['cuisine_type'])
        
        # Dificultad
        if recipe.get('difficulty'):
            text_parts.append(recipe['difficulty'])
        
        # Descripción
        if recipe.get('description'):
            text_parts.append(recipe['description'])
        
        return ' '.join(text_parts).lower()
    
    def calculate_similarity(self, available_ingredients, recipe_id):
        """Calcula similitud entre receta e ingredientes disponibles"""
        if self.recipe_tfidf_matrix is None:
            return 0.0
        
        try:
            # Crear texto de ingredientes disponibles
            ingredients_text = ' '.join(available_ingredients).lower()
            
            # Vectorizar ingredientes disponibles
            ingredients_vector = self.tfidf_vectorizer.transform([ingredients_text])
            
            # Encontrar índice de la receta
            recipe_idx = self.recipe_ids.index(recipe_id)
            
            # Calcular similitud coseno
            recipe_vector = self.recipe_tfidf_matrix[recipe_idx]
            similarity = cosine_similarity(ingredients_vector, recipe_vector)[0][0]
            
            return similarity
            
        except Exception as e:
            return 0.0
    
    def save_model(self, filepath):
        """Guarda el modelo de filtro de contenido"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            model_data = {
                'vectorizer': self.tfidf_vectorizer,
                'tfidf_matrix': self.recipe_tfidf_matrix,
                'recipe_texts': self.recipe_texts,
                'recipe_ids': self.recipe_ids
            }
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
            print(f"✅ Content filter guardado en: {filepath}")
        except Exception as e:
            print(f"❌ Error guardando filtro de contenido: {e}")
    
    def load_model(self, filepath):
        """Carga el modelo de filtro de contenido"""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.tfidf_vectorizer = model_data['vectorizer']
            self.recipe_tfidf_matrix = model_data['tfidf_matrix']
            self.recipe_texts = model_data['recipe_texts']
            self.recipe_ids = model_data['recipe_ids']
            
            return True
        except Exception as e:
            print(f"❌ Error cargando filtro de contenido: {e}")
            return False


def main():
    """Función principal para probar el motor de recomendaciones"""
    print("🚀 Iniciando Sistema de Recomendaciones...")
    
    # Crear instancia del motor
    recommendation_engine = RecommendationEngine()
    
    # Entrenar modelos
    recommendation_engine.train_models()
    
    # Analizar rendimiento
    recommendation_engine.analyze_model_performance()
    
    # Probar recomendaciones
    print("\n🔍 Probando recomendaciones personalizadas...")
    
    # Perfil de usuario de ejemplo
    user_profile = {
        'dietary_restrictions': ['vegetariano'],
        'avg_rating_given': 4.2,
        'preferred_cuisines': ['italiana', 'mediterránea']
    }
    
    # Ingredientes disponibles
    available_ingredients = ['tomate', 'ajo', 'cebolla', 'aceite', 'pasta']
    
    # Obtener recomendaciones
    recommendations = recommendation_engine.get_recommendations(
        user_profile, 
        available_ingredients, 
        n_recommendations=3
    )
    
    print(f"\nRecomendaciones para usuario vegetariano con ingredientes: {available_ingredients}")
    print("-" * 80)
    
    for i, rec in enumerate(recommendations, 1):
        recipe = rec['recipe']
        print(f"\n{i}. {recipe['name']}")
        print(f"   Rating predicho: {rec['predicted_rating']:.1f}/5.0")
        print(f"   Cobertura de ingredientes: {rec['ingredient_coverage']:.1%}")
        print(f"   Ingredientes faltantes: {rec['missing_ingredients']}")
        if rec['substitution_suggestions']:
            print(f"   Sustituciones sugeridas: {rec['substitution_suggestions']}")
    
    # Probar con usuario sin restricciones
    print("\n" + "="*80)
    print("🔍 Probando con usuario sin restricciones dietéticas...")
    
    user_profile_2 = {
        'dietary_restrictions': [],
        'avg_rating_given': 3.8,
        'preferred_cuisines': ['latina', 'mexicana']
    }
    
    available_ingredients_2 = ['pollo', 'arroz', 'cebolla', 'tomate']
    
    recommendations_2 = recommendation_engine.get_recommendations(
        user_profile_2, 
        available_ingredients_2, 
        n_recommendations=3
    )
    
    print(f"\nRecomendaciones para usuario general con ingredientes: {available_ingredients_2}")
    print("-" * 80)
    
    for i, rec in enumerate(recommendations_2, 1):
        recipe = rec['recipe']
        print(f"\n{i}. {recipe['name']}")
        print(f"   Rating predicho: {rec['predicted_rating']:.1f}/5.0")
        print(f"   Cobertura de ingredientes: {rec['ingredient_coverage']:.1%}")
        print(f"   Tipo de cocina: {recipe.get('cuisine_type', 'N/A')}")


if __name__ == "__main__":
    main()