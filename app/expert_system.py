from app.models import Recipe, Ingredient, User, DietaryRestriction, IngredientSubstitution, NutritionalInfo
from ml_models.recommendation_engine import RecommendationEngine
from ml_models.nlp_processor import NLPProcessor
import json

class CulinaryExpertSystem:
    def __init__(self):
        self.recommendation_engine = RecommendationEngine()
        self.nlp_processor = NLPProcessor()
        
        # Reglas de inferencia del sistema experto
        self.rules = {
            'dietary_restrictions': self._apply_dietary_restrictions,
            'ingredient_matching': self._match_ingredients,
            'time_constraints': self._apply_time_constraints,
            'difficulty_preference': self._apply_difficulty_preference,
            'nutritional_requirements': self._apply_nutritional_requirements,
            'substitution_rules': self._generate_substitutions
        }
    
    def get_recommendations(self, user_id, available_ingredients, preferences=None):
        """
        Motor principal de recomendaciones que aplica las reglas del sistema experto
        """
        user = User.query.get(user_id)
        if not user:
            return []
        
        # Procesar ingredientes con NLP
        processed_ingredients = self.nlp_processor.process_ingredients(available_ingredients)
        
        # Obtener recetas candidatas
        candidate_recipes = self._get_candidate_recipes(processed_ingredients)
        
        # Aplicar reglas del sistema experto
        filtered_recipes = self._apply_expert_rules(candidate_recipes, user, processed_ingredients, preferences)
        
        # Aplicar machine learning para ranking final
        ranked_recipes = self.recommendation_engine.rank_recipes(
            filtered_recipes, user_id, processed_ingredients
        )
        
        return ranked_recipes
    
    def _get_candidate_recipes(self, ingredients):
        """Obtiene recetas que contienen al menos uno de los ingredientes disponibles"""
        ingredient_names = [ing.lower().strip() for ing in ingredients]
        
        # Buscar ingredientes en la base de datos
        db_ingredients = Ingredient.query.filter(
            Ingredient.name.in_(ingredient_names)
        ).all()
        
        if not db_ingredients:
            return Recipe.query.all()  # Si no se encuentran ingredientes específicos, devolver todas
        
        # Obtener recetas que contengan estos ingredientes
        recipes = Recipe.query.join(Recipe.ingredients).filter(
            Ingredient.id.in_([ing.id for ing in db_ingredients])
        ).distinct().all()
        
        return recipes
    
    def _apply_expert_rules(self, recipes, user, ingredients, preferences):
        """Aplica las reglas del sistema experto"""
        filtered_recipes = recipes
        
        # Aplicar cada regla
        for rule_name, rule_func in self.rules.items():
            try:
                filtered_recipes = rule_func(filtered_recipes, user, ingredients, preferences)
            except Exception as e:
                print(f"Error aplicando regla {rule_name}: {e}")
                continue
        
        return filtered_recipes
    
    def _generate_substitutions(self, recipes, user, ingredients, preferences):
        """Regla: Generar sustituciones para ingredientes faltantes"""
        for recipe in recipes:
            recipe.suggested_substitutions = self.get_ingredient_substitutions(recipe, ingredients)
        return recipes
    
    def get_ingredient_substitutions(self, recipe, available_ingredients):
        """Obtiene sustituciones para ingredientes faltantes en una receta"""
        available_set = set(ing.lower().strip() for ing in available_ingredients)
        substitutions = {}
        
        for ingredient in recipe.ingredients:
            ingredient_name = ingredient.name.lower()
            
            # Si no tenemos el ingrediente, buscar sustitutos
            if ingredient_name not in available_set:
                substitutes = IngredientSubstitution.query.filter_by(
                    recipe_id=recipe.id,
                    original_ingredient_id=ingredient.id
                ).all()
                
                if substitutes:
                    substitutions[ingredient.name] = [
                        {
                            'substitute': sub.substitute_ingredient.name,
                            'ratio': sub.conversion_ratio,
                            'notes': sub.notes
                        } for sub in substitutes
                    ]
                else:
                    # Sustituciones genéricas basadas en categoría
                    generic_subs = self._get_generic_substitutions(ingredient)
                    if generic_subs:
                        substitutions[ingredient.name] = generic_subs
        
        return substitutions
    
    def _get_generic_substitutions(self, ingredient):
        """Obtiene sustituciones genéricas basadas en el tipo de ingrediente"""
        ingredient_name = ingredient.name.lower()
        
        generic_substitutions = {
            # Lácteos
            'leche': [
                {'substitute': 'leche de almendra', 'ratio': '1:1', 'notes': 'Para personas sin lactosa'},
                {'substitute': 'leche de coco', 'ratio': '1:1', 'notes': 'Sabor más dulce'},
                {'substitute': 'leche de soja', 'ratio': '1:1', 'notes': 'Opción vegana'}
            ],
            'mantequilla': [
                {'substitute': 'aceite de coco', 'ratio': '1:1', 'notes': 'Opción vegana'},
                {'substitute': 'margarina', 'ratio': '1:1', 'notes': 'Sin lactosa'},
                {'substitute': 'aceite de oliva', 'ratio': '3:4', 'notes': 'Para hornear'}
            ],
            'queso': [
                {'substitute': 'queso vegano', 'ratio': '1:1', 'notes': 'Opción sin lactosa'},
                {'substitute': 'levadura nutricional', 'ratio': '1:4', 'notes': 'Sabor similar al queso'}
            ],
            
            # Huevos
            'huevo': [
                {'substitute': 'linaza molida + agua', 'ratio': '1 tbsp linaza + 3 tbsp agua por huevo', 'notes': 'Opción vegana'},
                {'substitute': 'puré de manzana', 'ratio': '1/4 taza por huevo', 'notes': 'Para hornear'},
                {'substitute': 'aquafaba', 'ratio': '3 tbsp por huevo', 'notes': 'Líquido de garbanzos'}
            ],
            
            # Harinas
            'harina de trigo': [
                {'substitute': 'harina de arroz', 'ratio': '1:1', 'notes': 'Sin gluten'},
                {'substitute': 'harina de almendra', 'ratio': '1:1', 'notes': 'Baja en carbohidratos'},
                {'substitute': 'harina de avena', 'ratio': '1:1', 'notes': 'Más fibra'}
            ],
            
            # Azúcares
            'azúcar': [
                {'substitute': 'stevia', 'ratio': '1:8', 'notes': 'Para diabéticos'},
                {'substitute': 'miel', 'ratio': '3:4', 'notes': 'Opción natural'},
                {'substitute': 'jarabe de maple', 'ratio': '3:4', 'notes': 'Sabor distintivo'}
            ],
            
            # Carnes
            'pollo': [
                {'substitute': 'tofu', 'ratio': '1:1', 'notes': 'Opción vegetariana'},
                {'substitute': 'seitán', 'ratio': '1:1', 'notes': 'Alto en proteína'},
                {'substitute': 'setas portobello', 'ratio': '1:1', 'notes': 'Textura similar'}
            ],
            'carne de res': [
                {'substitute': 'lentejas', 'ratio': '1:1', 'notes': 'Rica en proteína'},
                {'substitute': 'frijoles negros', 'ratio': '1:1', 'notes': 'Opción vegetariana'},
                {'substitute': 'quinoa', 'ratio': '1:1', 'notes': 'Proteína completa'}
            ]
        }
        
        return generic_substitutions.get(ingredient_name, [])
    
    def calculate_missing_ingredients(self, recipe, available_ingredients):
        """Calcula qué ingredientes faltan para una receta"""
        available_set = set(ing.lower().strip() for ing in available_ingredients)
        recipe_ingredients = set(ing.name.lower() for ing in recipe.ingredients)
        
        missing = recipe_ingredients - available_set
        available = recipe_ingredients.intersection(available_set)
        
        return {
            'missing': list(missing),
            'available': list(available),
            'coverage_percentage': len(available) / len(recipe_ingredients) * 100 if recipe_ingredients else 0
        }
    
    def get_nutritional_analysis(self, recipe):
        """Proporciona análisis nutricional de una receta"""
        if not recipe.nutritional_info:
            return None
        
        nutrition = recipe.nutritional_info
        analysis = {
            'calories_per_serving': nutrition.calories_per_serving,
            'macronutrients': {
                'protein': nutrition.protein,
                'carbs': nutrition.carbs,
                'fat': nutrition.fat,
                'fiber': nutrition.fiber
            },
            'vitamins': {
                'vitamin_a': nutrition.vitamin_a,
                'vitamin_c': nutrition.vitamin_c,
                'vitamin_d': nutrition.vitamin_d,
                'vitamin_b12': nutrition.vitamin_b12
            },
            'minerals': {
                'iron': nutrition.iron,
                'calcium': nutrition.calcium,
                'sodium': nutrition.sodium
            }
        }
        
        # Agregar recomendaciones nutricionales
        recommendations = []
        
        if nutrition.protein and nutrition.protein > 20:
            recommendations.append("Rica en proteínas - excelente para el crecimiento muscular")
        
        if nutrition.fiber and nutrition.fiber > 5:
            recommendations.append("Alto contenido de fibra - bueno para la digestión")
        
        if nutrition.vitamin_c and nutrition.vitamin_c > 30:
            recommendations.append("Rica en vitamina C - fortalece el sistema inmune")
        
        if nutrition.iron and nutrition.iron > 3:
            recommendations.append("Buena fuente de hierro - previene la anemia")
        
        if nutrition.sodium and nutrition.sodium > 1500:
            recommendations.append("Alto contenido de sodio - considerar para hipertensión")
        
        analysis['recommendations'] = recommendations
        
        return analysis
    
    def suggest_additional_ingredients(self, recipe, available_ingredients):
        """Sugiere ingredientes adicionales para completar la receta"""
        missing_analysis = self.calculate_missing_ingredients(recipe, available_ingredients)
        missing_ingredients = missing_analysis['missing']
        
        suggestions = []
        for missing_ingredient in missing_ingredients:
            # Buscar el ingrediente en la base de datos
            ingredient = Ingredient.query.filter_by(name=missing_ingredient).first()
            if ingredient:
                suggestion = {
                    'name': ingredient.name,
                    'category': ingredient.category,
                    'alternatives': []
                }
                
                # Buscar alternativas del mismo tipo
                if ingredient.category:
                    alternatives = Ingredient.query.filter_by(category=ingredient.category).limit(3).all()
                    suggestion['alternatives'] = [alt.name for alt in alternatives if alt.name != ingredient.name]
                
                suggestions.append(suggestion)
        
        return suggestions
    
    def _apply_dietary_restrictions(self, recipes, user, ingredients, preferences):
        """Regla: Filtrar recetas según restricciones dietéticas"""
        if not user.dietary_restrictions:
            return recipes
        
        filtered_recipes = []
        for recipe in recipes:
            is_compatible = True
            
            for restriction in user.dietary_restrictions:
                if not self._recipe_meets_restriction(recipe, restriction):
                    is_compatible = False
                    break
            
            if is_compatible:
                filtered_recipes.append(recipe)
        
        return filtered_recipes
    
    def _recipe_meets_restriction(self, recipe, restriction):
        """Verifica si una receta cumple con una restricción dietética específica"""
        restriction_name = restriction.name.lower()
        recipe_ingredients = [ing.name.lower() for ing in recipe.ingredients]
        
        # Reglas específicas por tipo de restricción
        if restriction_name == 'vegetariano':
            forbidden = ['pollo', 'carne', 'pescado', 'cerdo', 'pavo', 'cordero']
            return not any(forbidden_item in ' '.join(recipe_ingredients) for forbidden_item in forbidden)
        
        elif restriction_name == 'vegano':
            forbidden = ['pollo', 'carne', 'pescado', 'huevo', 'leche', 'queso', 'mantequilla', 'crema']
            return not any(forbidden_item in ' '.join(recipe_ingredients) for forbidden_item in forbidden)
        
        elif restriction_name == 'sin gluten':
            forbidden = ['harina', 'trigo', 'avena', 'cebada', 'centeno', 'pan']
            return not any(forbidden_item in ' '.join(recipe_ingredients) for forbidden_item in forbidden)
        
        elif restriction_name == 'sin lactosa':
            forbidden = ['leche', 'queso', 'mantequilla', 'crema', 'yogurt']
            return not any(forbidden_item in ' '.join(recipe_ingredients) for forbidden_item in forbidden)
        
        elif restriction_name == 'diabético':
            # Priorizar recetas con bajo contenido de azúcar
            if recipe.nutritional_info:
                return recipe.nutritional_info.sugar < 10  # menos de 10g de azúcar
        
        return True
    
    def _match_ingredients(self, recipes, user, ingredients, preferences):
        """Regla: Priorizar recetas que usen más ingredientes disponibles"""
        ingredient_set = set(ing.lower().strip() for ing in ingredients)
        
        scored_recipes = []
        for recipe in recipes:
            recipe_ingredients = set(ing.name.lower() for ing in recipe.ingredients)
            
            # Calcular porcentaje de ingredientes disponibles
            available_count = len(ingredient_set.intersection(recipe_ingredients))
            total_needed = len(recipe_ingredients)
            
            coverage_score = available_count / total_needed if total_needed > 0 else 0
            
            # Solo incluir recetas con al menos 30% de ingredientes disponibles
            if coverage_score >= 0.3:
                scored_recipes.append((recipe, coverage_score))
        
        # Ordenar por cobertura de ingredientes
        scored_recipes.sort(key=lambda x: x[1], reverse=True)
        return [recipe for recipe, score in scored_recipes]
    
    def _apply_time_constraints(self, recipes, user, ingredients, preferences):
        """Regla: Filtrar por tiempo máximo de preparación"""
        max_time = None
        
        if preferences and preferences.get('max_prep_time'):
            max_time = int(preferences['max_prep_time'])
        elif user.user_preferences:
            pref = user.user_preferences[0]
            max_time = pref.max_prep_time
        
        if not max_time:
            return recipes
        
        return [recipe for recipe in recipes if recipe.total_time <= max_time]
    
    def _apply_difficulty_preference(self, recipes, user, ingredients, preferences):
        """Regla: Filtrar por dificultad preferida"""
        difficulty = None
        
        if preferences and preferences.get('difficulty_preference'):
            difficulty = preferences['difficulty_preference']
        elif user.user_preferences:
            pref = user.user_preferences[0]
            difficulty = pref.difficulty_preference
        
        if not difficulty:
            return recipes
        
        return [recipe for recipe in recipes if recipe.difficulty == difficulty]
    
    def _apply_nutritional_requirements(self, recipes, user, ingredients, preferences):
        """Regla: Aplicar requisitos nutricionales específicos"""
        # Esta regla puede expandirse según necesidades específicas
        # Por ejemplo, para usuarios diabéticos, priorizar recetas bajas en azúcar
        
        filtered_recipes = []
        for recipe in recipes:
            if recipe.nutritional_info:
                # Ejemplo: evitar recetas muy altas en sodio
                if recipe.nutritional_info.sodium and recipe.nutritional_info.sodium > 2000:
                    continue
                filtered_recipes.append(recipe)
            else:
                # Si no hay info nutricional, incluir la receta
                filtered_recipes.append(recipe)
        
        return filtered_recipes