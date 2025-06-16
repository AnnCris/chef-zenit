import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pickle
import matplotlib.pyplot as plt
from app.models import Recipe, User, RecipeRating, Ingredient, NutritionalInfo

class RecipeClustering:
    def __init__(self, n_clusters=8):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)  # Mantener 95% de la varianza
        self.feature_names = []
        self.cluster_labels = {}
        self.cluster_descriptions = {}
        
    def prepare_recipe_features(self):
        """
        Prepara las características de las recetas para clustering
        """
        recipes = Recipe.query.all()
        if not recipes:
            return None
        
        features_list = []
        recipe_ids = []
        
        for recipe in recipes:
            features = self._extract_clustering_features(recipe)
            features_list.append(features)
            recipe_ids.append(recipe.id)
        
        # Crear DataFrame
        df = pd.DataFrame(features_list)
        self.feature_names = df.columns.tolist()
        
        return df, recipe_ids
    
    def _extract_clustering_features(self, recipe):
        """
        Extrae características específicas para clustering
        """
        features = {}
        
        # Características básicas de la receta
        features['prep_time'] = recipe.prep_time or 30
        features['cook_time'] = recipe.cook_time or 30
        features['total_time'] = features['prep_time'] + features['cook_time']
        features['servings'] = recipe.servings or 4
        features['num_ingredients'] = len(recipe.ingredients)
        
        # Dificultad (one-hot encoding)
        features['difficulty_easy'] = 1 if recipe.difficulty == 'fácil' else 0
        features['difficulty_medium'] = 1 if recipe.difficulty == 'medio' else 0
        features['difficulty_hard'] = 1 if recipe.difficulty == 'difícil' else 0
        
        # Tipo de cocina (one-hot encoding)
        cuisines = ['mexicana', 'italiana', 'asiática', 'mediterránea', 'francesa', 'americana', 'india', 'árabe']
        for cuisine in cuisines:
            features[f'cuisine_{cuisine}'] = 1 if recipe.cuisine_type == cuisine else 0
        
        # Características nutricionales
        if recipe.nutritional_info:
            nutrition = recipe.nutritional_info
            features['calories_per_serving'] = nutrition.calories_per_serving or 400
            features['protein_ratio'] = (nutrition.protein or 15) / (features['calories_per_serving'] / 4)  # proteína por caloría
            features['carb_ratio'] = (nutrition.carbs or 50) / (features['calories_per_serving'] / 4)
            features['fat_ratio'] = (nutrition.fat or 10) / (features['calories_per_serving'] / 9)
            features['fiber_content'] = nutrition.fiber or 3
            features['sugar_content'] = nutrition.sugar or 10
            features['sodium_content'] = nutrition.sodium or 800
            
            # Densidad de vitaminas (normalizada)
            vitamin_density = 0
            if nutrition.vitamin_a: vitamin_density += 1
            if nutrition.vitamin_c: vitamin_density += 1
            if nutrition.vitamin_d: vitamin_density += 1
            if nutrition.vitamin_b12: vitamin_density += 1
            features['vitamin_density'] = vitamin_density
            
            # Densidad de minerales
            mineral_density = 0
            if nutrition.iron: mineral_density += 1
            if nutrition.calcium: mineral_density += 1
            features['mineral_density'] = mineral_density
        else:
            # Valores por defecto si no hay información nutricional
            features.update({
                'calories_per_serving': 400,
                'protein_ratio': 0.15,
                'carb_ratio': 0.50,
                'fat_ratio': 0.25,
                'fiber_content': 3,
                'sugar_content': 10,
                'sodium_content': 800,
                'vitamin_density': 0,
                'mineral_density': 0
            })
        
        # Características de ingredientes por categoría
        ingredient_categories = {
            'vegetables': 0, 'proteins': 0, 'grains': 0, 'dairy': 0, 
            'spices': 0, 'fruits': 0, 'fats': 0
        }
        
        for ingredient in recipe.ingredients:
            category = self._categorize_ingredient(ingredient.name.lower())
            if category in ingredient_categories:
                ingredient_categories[category] += 1
        
        # Agregar categorías de ingredientes como características
        for category, count in ingredient_categories.items():
            features[f'ingredient_{category}'] = count
        
        # Rating promedio de la receta
        features['avg_rating'] = recipe.average_rating or 3.0
        features['num_ratings'] = len(recipe.ratings)
        
        return features
    
    def _categorize_ingredient(self, ingredient_name):
        """
        Categoriza un ingrediente según su tipo
        """
        vegetables = ['tomate', 'cebolla', 'ajo', 'zanahoria', 'apio', 'pimiento', 'chile', 'calabaza', 'brócoli', 'espinaca', 'lechuga']
        proteins = ['pollo', 'carne', 'pescado', 'cerdo', 'huevo', 'frijol', 'lenteja', 'garbanzo', 'tofu']
        grains = ['arroz', 'pasta', 'pan', 'harina', 'avena', 'quinoa', 'maíz']
        dairy = ['leche', 'queso', 'mantequilla', 'crema', 'yogurt']
        spices = ['sal', 'pimienta', 'comino', 'orégano', 'albahaca', 'canela', 'cilantro', 'perejil']
        fruits = ['limón', 'naranja', 'manzana', 'plátano', 'fresa', 'uva', 'piña']
        fats = ['aceite', 'manteca', 'aguacate', 'nuez', 'almendra']
        
        for veg in vegetables:
            if veg in ingredient_name:
                return 'vegetables'
        for prot in proteins:
            if prot in ingredient_name:
                return 'proteins'
        for grain in grains:
            if grain in ingredient_name:
                return 'grains'
        for d in dairy:
            if d in ingredient_name:
                return 'dairy'
        for spice in spices:
            if spice in ingredient_name:
                return 'spices'
        for fruit in fruits:
            if fruit in ingredient_name:
                return 'fruits'
        for fat in fats:
            if fat in ingredient_name:
                return 'fats'
        
        return 'other'
    
    def train_clustering(self):
        """
        Entrena el modelo de clustering
        """
        # Preparar datos
        data, recipe_ids = self.prepare_recipe_features()
        if data is None:
            print("No hay suficientes recetas para entrenar el clustering.")
            return
        
        # Rellenar valores faltantes
        data = data.fillna(data.mean())
        
        # Escalar características
        data_scaled = self.scaler.fit_transform(data)
        
        # Aplicar PCA para reducción de dimensionalidad
        data_pca = self.pca.fit_transform(data_scaled)
        
        # Entrenar KMeans
        self.kmeans.fit(data_pca)
        
        # Asignar etiquetas de cluster a recetas
        cluster_labels = self.kmeans.labels_
        for recipe_id, label in zip(recipe_ids, cluster_labels):
            self.cluster_labels[recipe_id] = label
        
        # Generar descripciones de clusters
        self._generate_cluster_descriptions(data, cluster_labels)
        
        print(f"Clustering entrenado con {len(recipe_ids)} recetas en {self.n_clusters} clusters.")
        
        return self.cluster_labels
    
    def _generate_cluster_descriptions(self, data, cluster_labels):
        """
        Genera descripciones interpretables para cada cluster
        """
        data_with_clusters = data.copy()
        data_with_clusters['cluster'] = cluster_labels
        
        for cluster_id in range(self.n_clusters):
            cluster_data = data_with_clusters[data_with_clusters['cluster'] == cluster_id]
            
            if len(cluster_data) == 0:
                continue
            
            # Calcular estadísticas del cluster
            cluster_stats = cluster_data.mean()
            
            # Generar descripción basada en características dominantes
            description = self._interpret_cluster(cluster_stats)
            self.cluster_descriptions[cluster_id] = description
    
    def _interpret_cluster(self, cluster_stats):
        """
        Interpreta las estadísticas de un cluster para generar descripción
        """
        description_parts = []
        
        # Analizar tiempo de preparación
        if cluster_stats['total_time'] <= 30:
            description_parts.append("Recetas rápidas")
        elif cluster_stats['total_time'] <= 60:
            description_parts.append("Recetas de tiempo moderado")
        else:
            description_parts.append("Recetas que requieren tiempo")
        
        # Analizar dificultad
        if cluster_stats['difficulty_easy'] > 0.5:
            description_parts.append("fáciles de preparar")
        elif cluster_stats['difficulty_hard'] > 0.5:
            description_parts.append("de alta complejidad")
        else:
            description_parts.append("de dificultad media")
        
        # Analizar tipo de cocina dominante
        cuisine_cols = [col for col in cluster_stats.index if col.startswith('cuisine_')]
        if cuisine_cols:
            max_cuisine = max(cuisine_cols, key=lambda x: cluster_stats[x])
            if cluster_stats[max_cuisine] > 0.3:
                cuisine_name = max_cuisine.replace('cuisine_', '')
                description_parts.append(f"principalmente de cocina {cuisine_name}")
        
        # Analizar perfil nutricional
        if cluster_stats['protein_ratio'] > 0.25:
            description_parts.append("ricas en proteína")
        elif cluster_stats['carb_ratio'] > 0.6:
            description_parts.append("ricas en carbohidratos")
        elif cluster_stats['fat_ratio'] > 0.35:
            description_parts.append("con contenido alto de grasas")
        
        if cluster_stats['fiber_content'] > 8:
            description_parts.append("con alta fibra")
        
        if cluster_stats['sodium_content'] < 500:
            description_parts.append("bajas en sodio")
        
        # Analizar ingredientes dominantes
        ingredient_cols = [col for col in cluster_stats.index if col.startswith('ingredient_')]
        if ingredient_cols:
            max_ingredient_type = max(ingredient_cols, key=lambda x: cluster_stats[x])
            if cluster_stats[max_ingredient_type] > 2:
                ingredient_type = max_ingredient_type.replace('ingredient_', '')
                type_translations = {
                    'vegetables': 'verduras',
                    'proteins': 'proteínas',
                    'grains': 'cereales',
                    'dairy': 'lácteos',
                    'spices': 'especias',
                    'fruits': 'frutas',
                    'fats': 'grasas'
                }
                if ingredient_type in type_translations:
                    description_parts.append(f"con énfasis en {type_translations[ingredient_type]}")
        
        return ", ".join(description_parts)
    
    def get_similar_recipes(self, recipe_id, n_recommendations=5):
        """
        Obtiene recetas similares basadas en el clustering
        """
        if recipe_id not in self.cluster_labels:
            return []
        
        target_cluster = self.cluster_labels[recipe_id]
        
        # Encontrar otras recetas en el mismo cluster
        similar_recipe_ids = [
            rid for rid, cluster in self.cluster_labels.items() 
            if cluster == target_cluster and rid != recipe_id
        ]
        
        # Obtener objetos Recipe
        similar_recipes = Recipe.query.filter(Recipe.id.in_(similar_recipe_ids)).all()
        
        # Ordenar por rating promedio
        similar_recipes.sort(key=lambda x: x.average_rating or 0, reverse=True)
        
        return similar_recipes[:n_recommendations]
    
    def get_cluster_recommendations_for_user(self, user_id, n_recommendations=10):
        """
        Recomienda recetas basadas en los clusters que el usuario ha calificado positivamente
        """
        user = User.query.get(user_id)
        if not user or not user.recipe_ratings:
            return []
        
        # Analizar clusters preferidos del usuario
        preferred_clusters = {}
        for rating in user.recipe_ratings:
            if rating.rating >= 4:  # Calificaciones altas
                recipe_cluster = self.cluster_labels.get(rating.recipe_id)
                if recipe_cluster is not None:
                    preferred_clusters[recipe_cluster] = preferred_clusters.get(recipe_cluster, 0) + 1
        
        if not preferred_clusters:
            return []
        
        # Ordenar clusters por preferencia
        sorted_clusters = sorted(preferred_clusters.items(), key=lambda x: x[1], reverse=True)
        
        # Obtener recetas de los clusters preferidos
        recommended_recipes = []
        rated_recipe_ids = {rating.recipe_id for rating in user.recipe_ratings}
        
        for cluster_id, _ in sorted_clusters:
            cluster_recipe_ids = [
                rid for rid, cluster in self.cluster_labels.items() 
                if cluster == cluster_id and rid not in rated_recipe_ids
            ]
            
            cluster_recipes = Recipe.query.filter(Recipe.id.in_(cluster_recipe_ids)).all()
            cluster_recipes.sort(key=lambda x: x.average_rating or 0, reverse=True)
            
            recommended_recipes.extend(cluster_recipes)
            
            if len(recommended_recipes) >= n_recommendations:
                break
        
        return recommended_recipes[:n_recommendations]
    
    def analyze_user_preferences(self, user_id):
        """
        Analiza las preferencias del usuario basadas en clustering
        """
        user = User.query.get(user_id)
        if not user or not user.recipe_ratings:
            return None
        
        # Analizar clusters de recetas bien calificadas
        cluster_ratings = {}
        for rating in user.recipe_ratings:
            recipe_cluster = self.cluster_labels.get(rating.recipe_id)
            if recipe_cluster is not None:
                if recipe_cluster not in cluster_ratings:
                    cluster_ratings[recipe_cluster] = []
                cluster_ratings[recipe_cluster].append(rating.rating)
        
        # Calcular rating promedio por cluster
        cluster_preferences = {}
        for cluster_id, ratings in cluster_ratings.items():
            avg_rating = np.mean(ratings)
            cluster_preferences[cluster_id] = {
                'avg_rating': avg_rating,
                'num_ratings': len(ratings),
                'description': self.cluster_descriptions.get(cluster_id, f"Cluster {cluster_id}")
            }
        
        # Ordenar por preferencia
        sorted_preferences = sorted(
            cluster_preferences.items(), 
            key=lambda x: x[1]['avg_rating'], 
            reverse=True
        )
        
        return sorted_preferences
    
    def save_model(self, filepath):
        """
        Guarda el modelo de clustering
        """
        model_data = {
            'kmeans': self.kmeans,
            'scaler': self.scaler,
            'pca': self.pca,
            'cluster_labels': self.cluster_labels,
            'cluster_descriptions': self.cluster_descriptions,
            'feature_names': self.feature_names,
            'n_clusters': self.n_clusters
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath):
        """
        Carga el modelo de clustering
        """
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.kmeans = model_data['kmeans']
            self.scaler = model_data['scaler']
            self.pca = model_data['pca']
            self.cluster_labels = model_data['cluster_labels']
            self.cluster_descriptions = model_data['cluster_descriptions']
            self.feature_names = model_data['feature_names']
            self.n_clusters = model_data['n_clusters']
            
            return True
        except Exception as e:
            print(f"Error cargando modelo de clustering: {e}")
            return False