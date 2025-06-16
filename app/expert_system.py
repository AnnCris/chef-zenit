from app.models import Recipe, Ingredient, User, DietaryRestriction, IngredientSubstitution, NutritionalInfo, db
from sqlalchemy import or_, func
import re

class CulinaryExpertSystem:
    def __init__(self):
        # Configuración simplificada para funcionar con Flask
        self.rules = {
            'dietary_restrictions': self._apply_dietary_restrictions,
            'ingredient_matching': self._match_ingredients,
            'time_constraints': self._apply_time_constraints,
            'difficulty_preference': self._apply_difficulty_preference,
        }
    
    def get_recommendations(self, user_id, available_ingredients, preferences=None):
        """
        Motor principal de recomendaciones que aplica las reglas del sistema experto
        """
        print(f"🔍 DEBUG: Buscando recomendaciones para usuario {user_id}")
        print(f"🔍 DEBUG: Ingredientes disponibles: {available_ingredients}")
        
        user = User.query.get(user_id)
        if not user:
            print(f"❌ DEBUG: Usuario {user_id} no encontrado")
            return []
        
        # Procesar ingredientes con NLP básico
        processed_ingredients = self._process_ingredients_simple(available_ingredients)
        print(f"🔍 DEBUG: Ingredientes procesados: {processed_ingredients}")
        
        # Obtener recetas candidatas
        candidate_recipes = self._get_candidate_recipes(processed_ingredients)
        print(f"🔍 DEBUG: Recetas candidatas encontradas: {len(candidate_recipes)}")
        
        if not candidate_recipes:
            print("❌ DEBUG: No se encontraron recetas candidatas")
            # Si no hay candidatas con ingredientes específicos, obtener todas las recetas
            candidate_recipes = Recipe.query.limit(20).all()
            print(f"🔍 DEBUG: Usando todas las recetas como fallback: {len(candidate_recipes)}")
        
        # Aplicar reglas del sistema experto
        filtered_recipes = self._apply_expert_rules(candidate_recipes, user, processed_ingredients, preferences)
        print(f"🔍 DEBUG: Recetas después de filtros: {len(filtered_recipes)}")
        
        # Rankear por coincidencia de ingredientes y rating
        ranked_recipes = self._rank_recipes_simple(filtered_recipes, processed_ingredients)
        print(f"🔍 DEBUG: Recetas rankeadas: {len(ranked_recipes)}")
        
        return ranked_recipes[:10]  # Devolver máximo 10 recomendaciones
    
    def _process_ingredients_simple(self, ingredients_text):
        """Procesamiento simple de ingredientes"""
        if isinstance(ingredients_text, list):
            ingredients = ingredients_text
        else:
            # Separar por comas, punto y coma o saltos de línea
            ingredients = re.split(r'[,;\n]+', str(ingredients_text))
        
        processed = []
        for ingredient in ingredients:
            if ingredient.strip():
                # Limpiar y normalizar
                clean_ingredient = ingredient.strip().lower()
                # Remover cantidades y unidades básicas
                clean_ingredient = re.sub(r'\d+\s*(kg|g|taza|tazas|cdas?|cditas?|piezas?|dientes?)', '', clean_ingredient)
                clean_ingredient = clean_ingredient.strip()
                if len(clean_ingredient) > 2:
                    processed.append(clean_ingredient)
        
        return processed
    
    def _get_candidate_recipes(self, ingredients):
        """Obtiene recetas que contienen al menos uno de los ingredientes disponibles"""
        if not ingredients:
            return Recipe.query.limit(20).all()
        
        print(f"🔍 DEBUG: Buscando recetas con ingredientes: {ingredients}")
        
        # Buscar ingredientes en la base de datos usando LIKE para coincidencias parciales
        ingredient_conditions = []
        for ingredient_name in ingredients:
            ingredient_conditions.append(Ingredient.name.ilike(f'%{ingredient_name}%'))
        
        # Buscar ingredientes que coincidan
        matching_ingredients = Ingredient.query.filter(or_(*ingredient_conditions)).all()
        print(f"🔍 DEBUG: Ingredientes encontrados en BD: {[ing.name for ing in matching_ingredients]}")
        
        if not matching_ingredients:
            print("❌ DEBUG: No se encontraron ingredientes en la BD")
            return Recipe.query.limit(20).all()
        
        # Obtener recetas que contengan estos ingredientes
        recipe_ids = db.session.query(Recipe.id).join(Recipe.ingredients).filter(
            Ingredient.id.in_([ing.id for ing in matching_ingredients])
        ).distinct().all()
        
        recipe_ids = [rid[0] for rid in recipe_ids]
        print(f"🔍 DEBUG: IDs de recetas encontradas: {recipe_ids}")
        
        recipes = Recipe.query.filter(Recipe.id.in_(recipe_ids)).all()
        print(f"🔍 DEBUG: Recetas obtenidas: {[r.name for r in recipes]}")
        
        return recipes
    
    def _apply_expert_rules(self, recipes, user, ingredients, preferences):
        """Aplica las reglas del sistema experto"""
        filtered_recipes = recipes
        
        # Aplicar cada regla
        for rule_name, rule_func in self.rules.items():
            try:
                print(f"🔍 DEBUG: Aplicando regla: {rule_name}")
                filtered_recipes = rule_func(filtered_recipes, user, ingredients, preferences)
                print(f"🔍 DEBUG: Recetas después de {rule_name}: {len(filtered_recipes)}")
            except Exception as e:
                print(f"❌ ERROR aplicando regla {rule_name}: {e}")
                continue
        
        return filtered_recipes
    
    def _rank_recipes_simple(self, recipes, available_ingredients):
        """Rankea recetas por coincidencia de ingredientes y rating"""
        scored_recipes = []
        
        for recipe in recipes:
            score = 0
            
            # Score por coincidencia de ingredientes (peso 60%)
            ingredient_score = self._calculate_ingredient_match_score(recipe, available_ingredients)
            score += ingredient_score * 0.6
            
            # Score por rating promedio (peso 30%)
            rating_score = (recipe.average_rating or 3.0) / 5.0
            score += rating_score * 0.3
            
            # Score por popularidad (peso 10%)
            popularity_score = min(len(recipe.ratings), 10) / 10.0
            score += popularity_score * 0.1
            
            scored_recipes.append((recipe, score))
            print(f"🔍 DEBUG: {recipe.name} - Score: {score:.3f} (ingredientes: {ingredient_score:.3f}, rating: {rating_score:.3f})")
        
        # Ordenar por score descendente
        scored_recipes.sort(key=lambda x: x[1], reverse=True)
        return [recipe for recipe, score in scored_recipes]
    
    def _calculate_ingredient_match_score(self, recipe, available_ingredients):
        """Calcula el score de coincidencia de ingredientes"""
        if not recipe.ingredients or not available_ingredients:
            return 0.0
        
        recipe_ingredient_names = [ing.name.lower() for ing in recipe.ingredients]
        available_lower = [ing.lower() for ing in available_ingredients]
        
        matches = 0
        for recipe_ing in recipe_ingredient_names:
            for available_ing in available_lower:
                if available_ing in recipe_ing or recipe_ing in available_ing:
                    matches += 1
                    break
        
        score = matches / len(recipe_ingredient_names)
        return score
    
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
        ingredients_text = ' '.join(recipe_ingredients)
        
        # Reglas específicas por tipo de restricción
        if restriction_name == 'vegetariano':
            forbidden = ['pollo', 'carne', 'pescado', 'cerdo', 'pavo', 'cordero']
            return not any(forbidden_item in ingredients_text for forbidden_item in forbidden)
        
        elif restriction_name == 'vegano':
            forbidden = ['pollo', 'carne', 'pescado', 'huevo', 'leche', 'queso', 'mantequilla', 'crema']
            return not any(forbidden_item in ingredients_text for forbidden_item in forbidden)
        
        elif restriction_name == 'sin gluten':
            forbidden = ['harina', 'trigo', 'avena', 'cebada', 'centeno', 'pan', 'pasta']
            return not any(forbidden_item in ingredients_text for forbidden_item in forbidden)
        
        elif restriction_name == 'sin lactosa':
            forbidden = ['leche', 'queso', 'mantequilla', 'crema', 'yogurt']
            return not any(forbidden_item in ingredients_text for forbidden_item in forbidden)
        
        return True
    
    def _match_ingredients(self, recipes, user, ingredients, preferences):
        """Regla: Priorizar recetas que usen más ingredientes disponibles"""
        # Esta regla ya se aplica en el ranking, simplemente devolver todas
        return recipes
    
    def _apply_time_constraints(self, recipes, user, ingredients, preferences):
        """Regla: Filtrar por tiempo máximo de preparación"""
        max_time = None
        
        if preferences and preferences.get('max_prep_time'):
            try:
                max_time = int(preferences['max_prep_time'])
            except (ValueError, TypeError):
                pass
        elif user.user_preferences:
            pref = user.user_preferences[0]
            max_time = pref.max_prep_time
        
        if not max_time:
            return recipes
        
        filtered = []
        for recipe in recipes:
            total_time = (recipe.prep_time or 0) + (recipe.cook_time or 0)
            if total_time <= max_time:
                filtered.append(recipe)
        
        return filtered if filtered else recipes  # Si no hay ninguna, devolver todas
    
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
        
        filtered = [recipe for recipe in recipes if recipe.difficulty == difficulty]
        return filtered if filtered else recipes  # Si no hay ninguna, devolver todas
    
    def get_ingredient_substitutions(self, recipe, available_ingredients):
        """Obtiene sustituciones para ingredientes faltantes en una receta"""
        available_set = set(ing.lower().strip() for ing in available_ingredients)
        substitutions = {}
        
        for ingredient in recipe.ingredients:
            ingredient_name = ingredient.name.lower()
            
            # Si no tenemos el ingrediente, buscar sustitutos
            if not any(avail in ingredient_name or ingredient_name in avail for avail in available_set):
                # Buscar sustituciones en la base de datos
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
                {'substitute': 'leche de coco', 'ratio': '1:1', 'notes': 'Sabor más dulce'}
            ],
            'mantequilla': [
                {'substitute': 'aceite de coco', 'ratio': '1:1', 'notes': 'Opción vegana'},
                {'substitute': 'margarina', 'ratio': '1:1', 'notes': 'Sin lactosa'}
            ],
            'queso': [
                {'substitute': 'queso vegano', 'ratio': '1:1', 'notes': 'Opción sin lactosa'},
                {'substitute': 'levadura nutricional', 'ratio': '1:4', 'notes': 'Sabor similar al queso'}
            ],
            
            # Huevos
            'huevo': [
                {'substitute': 'linaza molida + agua', 'ratio': '1 tbsp linaza + 3 tbsp agua por huevo', 'notes': 'Opción vegana'},
                {'substitute': 'aquafaba', 'ratio': '3 tbsp por huevo', 'notes': 'Líquido de garbanzos'}
            ],
            
            # Harinas
            'harina': [
                {'substitute': 'harina de arroz', 'ratio': '1:1', 'notes': 'Sin gluten'},
                {'substitute': 'harina de almendra', 'ratio': '1:1', 'notes': 'Baja en carbohidratos'}
            ],
            
            # Carnes
            'pollo': [
                {'substitute': 'tofu', 'ratio': '1:1', 'notes': 'Opción vegetariana'},
                {'substitute': 'setas portobello', 'ratio': '1:1', 'notes': 'Textura similar'}
            ],
            'carne': [
                {'substitute': 'lentejas', 'ratio': '1:1', 'notes': 'Rica en proteína'},
                {'substitute': 'frijoles negros', 'ratio': '1:1', 'notes': 'Opción vegetariana'}
            ]
        }
        
        # Buscar coincidencias parciales
        for key, subs in generic_substitutions.items():
            if key in ingredient_name:
                return subs
        
        return []
    
    def calculate_missing_ingredients(self, recipe, available_ingredients):
        """Calcula qué ingredientes faltan para una receta"""
        available_set = set(ing.lower().strip() for ing in available_ingredients)
        recipe_ingredients = [ing.name.lower() for ing in recipe.ingredients]
        
        missing = []
        available = []
        
        for recipe_ing in recipe_ingredients:
            found = False
            for avail_ing in available_set:
                if avail_ing in recipe_ing or recipe_ing in avail_ing:
                    available.append(recipe_ing)
                    found = True
                    break
            if not found:
                missing.append(recipe_ing)
        
        coverage_percentage = len(available) / len(recipe_ingredients) * 100 if recipe_ingredients else 0
        
        return {
            'missing': missing,
            'available': available,
            'coverage_percentage': coverage_percentage
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
    
    def generate_cooking_tips(self, recipe, user_skill_level='principiante'):
        """Genera consejos de cocina personalizados"""
        tips = []
        
        # Consejos generales por nivel
        if user_skill_level == 'principiante':
            tips.extend([
                "Lee toda la receta antes de empezar a cocinar",
                "Prepara todos los ingredientes antes de comenzar (mise en place)",
                "Usa un timer para controlar los tiempos de cocción"
            ])
        
        # Consejos específicos según ingredientes
        recipe_ingredients = [ing.name.lower() for ing in recipe.ingredients]
        
        if any('ajo' in ing for ing in recipe_ingredients):
            tips.append("Para pelar ajo fácilmente, aplástalo ligeramente con el lado plano del cuchillo")
        
        if any('cebolla' in ing for ing in recipe_ingredients):
            tips.append("Para evitar llorar al cortar cebolla, refrigérala 30 minutos antes")
        
        if any('arroz' in ing for ing in recipe_ingredients):
            tips.append("Lava el arroz hasta que el agua salga clara para mejor textura")
        
        if any('pollo' in ing for ing in recipe_ingredients):
            tips.append("Asegúrate de que el pollo alcance 75°C de temperatura interna")
        
        if any('pasta' in ing for ing in recipe_ingredients):
            tips.append("Agrega sal al agua cuando hierva, antes de añadir la pasta")
        
        # Consejos según tiempo de preparación
        total_time = (recipe.prep_time or 0) + (recipe.cook_time or 0)
        if total_time > 60:
            tips.append("Esta receta toma tiempo, considera prepararla en fin de semana")
        
        if recipe.difficulty == 'difícil':
            tips.append("Lee cada paso cuidadosamente y no te apresures")
        
        return tips[:5]  # Máximo 5 consejos