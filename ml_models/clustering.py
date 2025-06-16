import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pickle
import matplotlib.pyplot as plt
import os

class RecipeClustering:
    def __init__(self, n_clusters=8):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)  # Mantener 95% de la varianza
        self.feature_names = []
        self.cluster_labels = {}
        self.cluster_descriptions = {}
        
    def prepare_recipe_features(self, recipes_data=None):
        """
        Prepara las características de las recetas para clustering
        Si no se proporciona recipes_data, usa datos de ejemplo
        """
        if recipes_data is None:
            recipes_data = self._generate_sample_data()
        
        features_list = []
        recipe_ids = []
        
        for recipe in recipes_data:
            features = self._extract_clustering_features(recipe)
            features_list.append(features)
            recipe_ids.append(recipe.get('id', len(recipe_ids) + 1))
        
        # Crear DataFrame
        df = pd.DataFrame(features_list)
        self.feature_names = df.columns.tolist()
        
        return df, recipe_ids
    
    def _generate_sample_data(self):
        """Genera datos de ejemplo para pruebas"""
        sample_recipes = [
            {
                'id': 1,
                'name': 'Arroz con Pollo',
                'prep_time': 15,
                'cook_time': 25,
                'servings': 4,
                'difficulty': 'medio',
                'cuisine_type': 'latina',
                'ingredients': ['arroz', 'pollo', 'cebolla', 'ajo', 'pimiento'],
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
                'ratings': [5, 4, 5, 4],
                'avg_rating': 4.5
            },
            {
                'id': 2,
                'name': 'Ensalada César',
                'prep_time': 10,
                'cook_time': 0,
                'servings': 2,
                'difficulty': 'fácil',
                'cuisine_type': 'italiana',
                'ingredients': ['lechuga', 'queso', 'ajo', 'limón', 'pan'],
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
                'ratings': [4, 5, 4],
                'avg_rating': 4.3
            },
            {
                'id': 3,
                'name': 'Sopa de Lentejas',
                'prep_time': 10,
                'cook_time': 35,
                'servings': 4,
                'difficulty': 'fácil',
                'cuisine_type': 'mediterránea',
                'ingredients': ['lenteja', 'cebolla', 'ajo', 'zanahoria', 'apio'],
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
                'ratings': [5, 5, 4, 5],
                'avg_rating': 4.7
            },
            {
                'id': 4,
                'name': 'Pasta Primavera',
                'prep_time': 15,
                'cook_time': 15,
                'servings': 4,
                'difficulty': 'fácil',
                'cuisine_type': 'italiana',
                'ingredients': ['pasta', 'brócoli', 'zanahoria', 'calabaza', 'pimiento'],
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
                'ratings': [4, 4, 5],
                'avg_rating': 4.3
            },
            {
                'id': 5,
                'name': 'Tacos de Pollo',
                'prep_time': 20,
                'cook_time': 15,
                'servings': 4,
                'difficulty': 'medio',
                'cuisine_type': 'mexicana',
                'ingredients': ['pollo', 'tortilla', 'cebolla', 'chile', 'cilantro'],
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
                'ratings': [5, 4, 5],
                'avg_rating': 4.6
            }
        ]
        return sample_recipes
    
    def _extract_clustering_features(self, recipe):
        """
        Extrae características específicas para clustering
        """
        features = {}
        
        # Características básicas de la receta
        features['prep_time'] = recipe.get('prep_time', 30)
        features['cook_time'] = recipe.get('cook_time', 30)
        features['total_time'] = features['prep_time'] + features['cook_time']
        features['servings'] = recipe.get('servings', 4)
        features['num_ingredients'] = len(recipe.get('ingredients', []))
        
        # Dificultad (one-hot encoding)
        difficulty = recipe.get('difficulty', 'fácil')
        features['difficulty_easy'] = 1 if difficulty == 'fácil' else 0
        features['difficulty_medium'] = 1 if difficulty == 'medio' else 0
        features['difficulty_hard'] = 1 if difficulty == 'difícil' else 0
        
        # Tipo de cocina (one-hot encoding)
        cuisines = ['mexicana', 'italiana', 'asiática', 'mediterránea', 'francesa', 'americana', 'india', 'árabe']
        cuisine_type = recipe.get('cuisine_type', '')
        for cuisine in cuisines:
            features[f'cuisine_{cuisine}'] = 1 if cuisine_type == cuisine else 0
        
        # Características nutricionales
        nutrition = recipe.get('nutritional_info', {})
        if nutrition:
            features['calories_per_serving'] = nutrition.get('calories_per_serving', 400)
            calories = features['calories_per_serving']
            features['protein_ratio'] = (nutrition.get('protein', 15)) / (calories / 4) if calories > 0 else 0.15
            features['carb_ratio'] = (nutrition.get('carbs', 50)) / (calories / 4) if calories > 0 else 0.50
            features['fat_ratio'] = (nutrition.get('fat', 10)) / (calories / 9) if calories > 0 else 0.25
            features['fiber_content'] = nutrition.get('fiber', 3)
            features['sugar_content'] = nutrition.get('sugar', 10)
            features['sodium_content'] = nutrition.get('sodium', 800)
            
            # Densidad de vitaminas (normalizada)
            vitamin_density = 0
            if nutrition.get('vitamin_a'): vitamin_density += 1
            if nutrition.get('vitamin_c'): vitamin_density += 1
            if nutrition.get('vitamin_d'): vitamin_density += 1
            if nutrition.get('vitamin_b12'): vitamin_density += 1
            features['vitamin_density'] = vitamin_density
            
            # Densidad de minerales
            mineral_density = 0
            if nutrition.get('iron'): mineral_density += 1
            if nutrition.get('calcium'): mineral_density += 1
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
        
        ingredients = recipe.get('ingredients', [])
        for ingredient in ingredients:
            category = self._categorize_ingredient(ingredient.lower())
            if category in ingredient_categories:
                ingredient_categories[category] += 1
        
        # Agregar categorías de ingredientes como características
        for category, count in ingredient_categories.items():
            features[f'ingredient_{category}'] = count
        
        # Rating promedio de la receta
        features['avg_rating'] = recipe.get('avg_rating', 3.0)
        features['num_ratings'] = len(recipe.get('ratings', []))
        
        return features
    
    def _categorize_ingredient(self, ingredient_name):
        """
        Categoriza un ingrediente según su tipo
        """
        vegetables = ['tomate', 'cebolla', 'ajo', 'zanahoria', 'apio', 'pimiento', 'chile', 'calabaza', 'brócoli', 'espinaca', 'lechuga']
        proteins = ['pollo', 'carne', 'pescado', 'cerdo', 'huevo', 'frijol', 'lenteja', 'garbanzo', 'tofu']
        grains = ['arroz', 'pasta', 'pan', 'harina', 'avena', 'quinoa', 'maíz', 'tortilla']
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
    
    def train_clustering(self, recipes_data=None):
        """
        Entrena el modelo de clustering
        """
        # Preparar datos
        data, recipe_ids = self.prepare_recipe_features(recipes_data)
        if data is None or len(data) == 0:
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
        
        print(f"✅ Clustering entrenado con {len(recipe_ids)} recetas en {self.n_clusters} clusters.")
        
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
            print(f"Cluster {cluster_id}: {description}")
    
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
        
        return ", ".join(description_parts)
    
    def get_similar_recipes(self, recipe_id, recipe_data, n_recommendations=5):
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
        
        # Filtrar recetas por IDs similares
        similar_recipes = [recipe for recipe in recipe_data 
                          if recipe.get('id') in similar_recipe_ids]
        
        # Ordenar por rating promedio
        similar_recipes.sort(key=lambda x: x.get('avg_rating', 0), reverse=True)
        
        return similar_recipes[:n_recommendations]
    
    def save_model(self, filepath):
        """
        Guarda el modelo de clustering
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
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
        
        print(f"✅ Modelo guardado en: {filepath}")
    
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
            
            print(f"✅ Modelo cargado desde: {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error cargando modelo de clustering: {e}")
            return False
    
    def analyze_clusters(self):
        """
        Analiza y muestra información sobre los clusters
        """
        print("\n📊 Análisis de Clusters:")
        print("=" * 50)
        
        for cluster_id in range(self.n_clusters):
            recipes_in_cluster = [rid for rid, cluster in self.cluster_labels.items() 
                                if cluster == cluster_id]
            description = self.cluster_descriptions.get(cluster_id, f"Cluster {cluster_id}")
            
            print(f"\nCluster {cluster_id}: {len(recipes_in_cluster)} recetas")
            print(f"Descripción: {description}")
            print(f"Recetas: {recipes_in_cluster}")


def main():
    """Función principal para probar el clustering"""
    print("🧠 Iniciando entrenamiento de clustering de recetas...")
    
    # Crear instancia del clustering
    clustering = RecipeClustering(n_clusters=3)  # Menos clusters para datos de ejemplo
    
    # Entrenar el modelo
    cluster_labels = clustering.train_clustering()
    
    # Analizar resultados
    clustering.analyze_clusters()
    
    # Guardar modelo
    model_path = "ml_models/trained_models/clustering_model.pkl"
    clustering.save_model(model_path)
    
    # Probar carga del modelo
    new_clustering = RecipeClustering()
    if new_clustering.load_model(model_path):
        print("\n✅ Modelo cargado correctamente para verificación")
    
    # Probar recomendaciones
    print("\n🔍 Probando recomendaciones similares...")
    sample_data = clustering._generate_sample_data()
    similar_recipes = clustering.get_similar_recipes(1, sample_data, 3)
    
    if similar_recipes:
        print("Recetas similares a 'Arroz con Pollo':")
        for recipe in similar_recipes:
            print(f"- {recipe['name']} (Rating: {recipe['avg_rating']})")
    else:
        print("No se encontraron recetas similares.")


if __name__ == "__main__":
    main()