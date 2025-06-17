# app/routes.py - VERSIÓN CORREGIDA CON ML
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app.models import Recipe, Ingredient, User, DietaryRestriction, UserPreference, RecipeRating, db
from app.forms import IngredientInputForm, PreferencesForm, RecipeRatingForm, AdvancedSearchForm, PDFGenerationForm
from app.expert_system import CulinaryExpertSystem
import json
from datetime import datetime
import os

main = Blueprint('main', __name__)

# Inicializar sistema experto (con ML integrado)
expert_system = CulinaryExpertSystem()

# Intentar inicializar modelos ML adicionales
try:
    from ml_models.clustering import RecipeClustering
    clustering_model = RecipeClustering()
    print("✅ Clustering model inicializado")
except Exception as e:
    clustering_model = None
    print(f"⚠️ Clustering model no disponible: {e}")

try:
    from ml_models.recommendation_engine import RecommendationEngine
    recommendation_engine = RecommendationEngine()
    print("✅ Recommendation engine inicializado")
except Exception as e:
    recommendation_engine = None
    print(f"⚠️ Recommendation engine no disponible: {e}")

@main.route('/')
def index():
    """Página principal"""
    recent_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(6).all()
    return render_template('index.html', recent_recipes=recent_recipes)

@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard del usuario con recomendaciones ML"""
    form = IngredientInputForm()
    
    # Obtener estadísticas del usuario
    user_stats = {
        'total_ratings': len(current_user.recipe_ratings),
        'avg_rating_given': sum(r.rating for r in current_user.recipe_ratings) / len(current_user.recipe_ratings) if current_user.recipe_ratings else 0,
        'favorite_recipes': Recipe.query.join(RecipeRating).filter(
            RecipeRating.user_id == current_user.id,
            RecipeRating.rating >= 4
        ).limit(5).all()
    }
    
    # Recomendaciones personalizadas usando ML si está disponible
    cluster_recommendations = []
    try:
        if clustering_model and hasattr(clustering_model, 'cluster_labels') and clustering_model.cluster_labels:
            # Usar clustering ML
            cluster_recommendations = get_cluster_recommendations_for_user_ml(current_user.id, 5)
        else:
            # Fallback: recomendaciones basadas en ratings del usuario
            cluster_recommendations = get_recommendations_by_ratings(current_user.id, 5)
    except Exception as e:
        print(f"Error obteniendo recomendaciones: {e}")
        cluster_recommendations = Recipe.query.filter(Recipe.average_rating >= 4.0).limit(5).all()
    
    return render_template('dashboard.html', 
                         form=form, 
                         user_stats=user_stats,
                         cluster_recommendations=cluster_recommendations)

def get_cluster_recommendations_for_user_ml(user_id, limit=5):
    """Obtiene recomendaciones usando clustering ML"""
    try:
        # Obtener recetas que el usuario ha calificado bien
        user_high_ratings = RecipeRating.query.filter(
            RecipeRating.user_id == user_id,
            RecipeRating.rating >= 4
        ).all()
        
        if not user_high_ratings:
            return Recipe.query.filter(Recipe.average_rating >= 4.0).limit(limit).all()
        
        # Usar el sistema experto con ML para obtener similares
        similar_recipes = []
        for rating in user_high_ratings[:3]:  # Usar top 3 recetas del usuario
            try:
                similar = expert_system.get_similar_recipes_ml(rating.recipe_id, 2)
                similar_recipes.extend(similar)
            except:
                continue
        
        # Remover duplicados y limitar
        seen_ids = set()
        unique_recommendations = []
        for recipe in similar_recipes:
            if recipe.id not in seen_ids:
                seen_ids.add(recipe.id)
                unique_recommendations.append(recipe)
                if len(unique_recommendations) >= limit:
                    break
        
        return unique_recommendations
        
    except Exception as e:
        print(f"Error en ML clustering recommendations: {e}")
        return get_recommendations_by_ratings(user_id, limit)

def get_recommendations_by_ratings(user_id, limit=5):
    """Fallback: recomendaciones basadas en ratings"""
    try:
        # Obtener tipos de cocina que le gustan al usuario
        user_ratings = RecipeRating.query.filter(
            RecipeRating.user_id == user_id,
            RecipeRating.rating >= 4
        ).join(Recipe).all()
        
        preferred_cuisines = []
        for rating in user_ratings:
            if rating.rated_recipe and rating.rated_recipe.cuisine_type:
                cuisine = rating.rated_recipe.cuisine_type
                if cuisine not in preferred_cuisines:
                    preferred_cuisines.append(cuisine)
        
        # Buscar recetas similares
        if preferred_cuisines:
            recommendations = Recipe.query.filter(
                Recipe.cuisine_type.in_(preferred_cuisines),
                Recipe.average_rating >= 4.0
            ).limit(limit).all()
        else:
            recommendations = Recipe.query.filter(
                Recipe.average_rating >= 4.0
            ).limit(limit).all()
        
        return recommendations
        
    except Exception as e:
        print(f"Error en fallback recommendations: {e}")
        return Recipe.query.limit(limit).all()

@main.route('/get_recommendations', methods=['POST'])
@login_required
def get_recommendations():
    """Obtiene recomendaciones basadas en ingredientes usando ML"""
    form = IngredientInputForm()
    
    print(f"🔍 DEBUG: Método: {request.method}")
    print(f"🔍 DEBUG: Form válido: {form.validate_on_submit()}")
    print(f"🔍 DEBUG: Form errors: {form.errors}")
    
    if form.validate_on_submit():
        ingredients_text = form.ingredients.data
        print(f"🔍 DEBUG: Ingredientes recibidos: '{ingredients_text}'")
        
        if not ingredients_text or not ingredients_text.strip():
            flash('Por favor ingresa algunos ingredientes', 'error')
            return redirect(url_for('main.dashboard'))
        
        try:
            # Obtener preferencias del usuario
            preferences = {}
            if current_user.user_preferences:
                pref = current_user.user_preferences[0]
                preferences = {
                    'max_prep_time': pref.max_prep_time,
                    'difficulty_preference': pref.difficulty_preference
                }
            
            print(f"🔍 DEBUG: Preferencias del usuario: {preferences}")
            
            # Obtener recomendaciones del sistema experto (con ML integrado)
            recommendations = expert_system.get_recommendations(
                current_user.id, 
                ingredients_text,
                preferences
            )
            
            print(f"🔍 DEBUG: Recomendaciones obtenidas: {len(recommendations)}")
            for i, recipe in enumerate(recommendations):
                print(f"🔍 DEBUG: {i+1}. {recipe.name}")
            
            if not recommendations:
                flash('No se encontraron recetas con esos ingredientes. Intenta con otros ingredientes o verifica que estén bien escritos.', 'warning')
                return redirect(url_for('main.dashboard'))
            
            # Calcular información adicional para cada receta
            enhanced_recommendations = []
            for recipe in recommendations:
                try:
                    # Calcular ingredientes faltantes
                    missing_info = expert_system.calculate_missing_ingredients(
                        recipe, ingredients_text.split(',')
                    )
                    
                    # Obtener sustituciones
                    substitutions = expert_system.get_ingredient_substitutions(
                        recipe, ingredients_text.split(',')
                    )
                    
                    # Análisis nutricional
                    nutritional_analysis = expert_system.get_nutritional_analysis(recipe)
                    
                    # Recetas similares usando ML si está disponible
                    similar_recipes = []
                    try:
                        similar_recipes = expert_system.get_similar_recipes_ml(recipe.id, 3)
                    except:
                        similar_recipes = []
                    
                    enhanced_recommendations.append({
                        'recipe': recipe,
                        'missing_info': missing_info,
                        'substitutions': substitutions,
                        'nutritional_analysis': nutritional_analysis,
                        'similar_recipes': similar_recipes
                    })
                    
                except Exception as e:
                    print(f"❌ ERROR procesando receta {recipe.name}: {e}")
                    # Agregar receta básica sin información adicional
                    enhanced_recommendations.append({
                        'recipe': recipe,
                        'missing_info': {'missing': [], 'available': [], 'coverage_percentage': 0},
                        'substitutions': {},
                        'nutritional_analysis': None,
                        'similar_recipes': []
                    })
            
            print(f"🔍 DEBUG: Recomendaciones mejoradas: {len(enhanced_recommendations)}")
            
            return render_template('recommendations.html', 
                                 recommendations=enhanced_recommendations,
                                 search_ingredients=ingredients_text)
                                 
        except Exception as e:
            print(f"❌ ERROR en get_recommendations: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Error al obtener recomendaciones: {str(e)}', 'error')
            return redirect(url_for('main.dashboard'))
    
    # Si el formulario no es válido
    print(f"❌ DEBUG: Formulario no válido. Errores: {form.errors}")
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error en {field}: {error}', 'error')
    
    return redirect(url_for('main.dashboard'))

@main.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """Detalle de una receta específica con análisis ML"""
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Formulario de calificación
    rating_form = RecipeRatingForm()
    
    # Obtener calificación del usuario actual si está logueado
    user_rating = None
    if current_user.is_authenticated:
        user_rating = RecipeRating.query.filter_by(
            user_id=current_user.id,
            recipe_id=recipe_id
        ).first()
    
    # Análisis nutricional usando expert system
    nutritional_analysis = expert_system.get_nutritional_analysis(recipe)
    
    # Recetas similares usando ML
    similar_recipes = []
    try:
        similar_recipes = expert_system.get_similar_recipes_ml(recipe_id, 4)
    except Exception as e:
        print(f"Error obteniendo recetas similares: {e}")
        # Fallback: obtener recetas del mismo tipo de cocina
        if recipe.cuisine_type:
            similar_recipes = Recipe.query.filter(
                Recipe.cuisine_type == recipe.cuisine_type,
                Recipe.id != recipe_id
            ).limit(4).all()
    
    # Consejos de cocina usando el expert_system
    cooking_tips = expert_system.generate_cooking_tips(
        recipe, 
        'principiante' if current_user.is_authenticated else 'principiante'
    )
    
    return render_template('recipe_detail.html',
                         recipe=recipe,
                         rating_form=rating_form,
                         user_rating=user_rating,
                         nutritional_analysis=nutritional_analysis,
                         similar_recipes=similar_recipes,
                         cooking_tips=cooking_tips)

@main.route('/rate_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def rate_recipe(recipe_id):
    """Calificar una receta y reentrenar modelos ML"""
    recipe = Recipe.query.get_or_404(recipe_id)
    form = RecipeRatingForm()
    
    if form.validate_on_submit():
        # Verificar si el usuario ya calificó esta receta
        existing_rating = RecipeRating.query.filter_by(
            user_id=current_user.id,
            recipe_id=recipe_id
        ).first()
        
        if existing_rating:
            # Actualizar calificación existente
            existing_rating.rating = int(form.rating.data)
            existing_rating.comment = form.comment.data
        else:
            # Crear nueva calificación
            new_rating = RecipeRating(
                user_id=current_user.id,
                recipe_id=recipe_id,
                rating=int(form.rating.data),
                comment=form.comment.data
            )
            db.session.add(new_rating)
        
        try:
            db.session.commit()
            flash('¡Calificación guardada exitosamente!', 'success')
            
            # Reentrenar modelos ML si están disponibles
            try:
                if recommendation_engine:
                    print("🔄 Reentrenando RecommendationEngine...")
                    recommendation_engine.train_models()
                    print("✅ RecommendationEngine reentrenado")
                
                if clustering_model:
                    print("🔄 Reentrenando Clustering...")
                    # Obtener datos actualizados para reentrenamiento
                    recipes_data = prepare_recipes_data_for_ml()
                    clustering_model.train_clustering(recipes_data)
                    print("✅ Clustering reentrenado")
                    
            except Exception as e:
                print(f"⚠️ Error reentrenando modelos ML: {e}")
                # No afecta la funcionalidad principal
            
        except Exception as e:
            db.session.rollback()
            flash('Error al guardar la calificación', 'error')
    
    return redirect(url_for('main.recipe_detail', recipe_id=recipe_id))

def prepare_recipes_data_for_ml():
    """Prepara datos de recetas para ML"""
    recipes = Recipe.query.all()
    recipes_data = []
    
    for recipe in recipes:
        recipe_dict = {
            'id': recipe.id,
            'name': recipe.name,
            'description': recipe.description or '',
            'ingredients': [ing.name for ing in recipe.ingredients],
            'cuisine_type': recipe.cuisine_type,
            'difficulty': recipe.difficulty,
            'prep_time': recipe.prep_time or 30,
            'cook_time': recipe.cook_time or 30,
            'servings': recipe.servings or 4,
            'avg_rating': recipe.average_rating or 3.0,
            'ratings': [r.rating for r in recipe.ratings]
        }
        
        # Agregar info nutricional si existe
        if recipe.nutritional_info:
            recipe_dict['nutritional_info'] = {
                'calories_per_serving': recipe.nutritional_info.calories_per_serving or 400,
                'protein': recipe.nutritional_info.protein or 15,
                'carbs': recipe.nutritional_info.carbs or 50,
                'fat': recipe.nutritional_info.fat or 12,
                'fiber': recipe.nutritional_info.fiber or 3,
                'sugar': recipe.nutritional_info.sugar or 8,
                'sodium': recipe.nutritional_info.sodium or 800
            }
        
        recipes_data.append(recipe_dict)
    
    return recipes_data

@main.route('/preferences', methods=['GET', 'POST'])
@login_required
def user_preferences():
    """Configurar preferencias del usuario"""
    form = PreferencesForm()
    
    # Cargar restricciones dietéticas disponibles
    restrictions = DietaryRestriction.query.all()
    form.dietary_restrictions.choices = [(r.id, r.name) for r in restrictions]
    
    if form.validate_on_submit():
        # Obtener o crear preferencias del usuario
        user_pref = UserPreference.query.filter_by(user_id=current_user.id).first()
        if not user_pref:
            user_pref = UserPreference(user_id=current_user.id)
        
        # Actualizar preferencias
        user_pref.preferred_cuisines = form.preferred_cuisines.data
        user_pref.max_prep_time = int(form.max_prep_time.data) if form.max_prep_time.data else None
        user_pref.difficulty_preference = form.difficulty_preference.data
        user_pref.disliked_ingredients = form.disliked_ingredients.data.split(',') if form.disliked_ingredients.data else []
        
        # Actualizar restricciones dietéticas
        current_user.dietary_restrictions.clear()
        for restriction_id in form.dietary_restrictions.data:
            restriction = DietaryRestriction.query.get(restriction_id)
            if restriction:
                current_user.dietary_restrictions.append(restriction)
        
        try:
            db.session.add(user_pref)
            db.session.commit()
            flash('Preferencias actualizadas exitosamente', 'success')
            
            # Opcional: Reentrenar modelos con nuevas preferencias
            try:
                if recommendation_engine:
                    print("🔄 Actualizando RecommendationEngine con nuevas preferencias...")
                    recommendation_engine.train_models()
            except Exception as e:
                print(f"⚠️ Error actualizando ML con preferencias: {e}")
                
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar preferencias', 'error')
        
        return redirect(url_for('main.dashboard'))
    
    # Cargar datos existentes en el formulario
    if current_user.user_preferences:
        pref = current_user.user_preferences[0]
        form.preferred_cuisines.data = pref.preferred_cuisines or []
        form.max_prep_time.data = str(pref.max_prep_time) if pref.max_prep_time else ''
        form.difficulty_preference.data = pref.difficulty_preference or ''
        form.disliked_ingredients.data = ','.join(pref.disliked_ingredients or [])
    
    form.dietary_restrictions.data = [r.id for r in current_user.dietary_restrictions]
    
    return render_template('preferences.html', form=form)

@main.route('/advanced_search', methods=['GET', 'POST'])
def advanced_search():
    """Búsqueda avanzada de recetas con ML"""
    form = AdvancedSearchForm()
    results = []
    
    if form.validate_on_submit():
        query = Recipe.query
        
        # Filtrar por ingredientes
        if form.ingredients.data:
            ingredient_names = [ing.strip().lower() for ing in form.ingredients.data.split(',')]
            query = query.join(Recipe.ingredients).filter(
                Ingredient.name.in_(ingredient_names)
            )
        
        # Filtrar por tipo de cocina
        if form.cuisine_type.data:
            query = query.filter(Recipe.cuisine_type == form.cuisine_type.data)
        
        # Filtrar por tiempo máximo
        if form.max_time.data:
            max_time = int(form.max_time.data)
            query = query.filter(
                (Recipe.prep_time + Recipe.cook_time) <= max_time
            )
        
        # Filtrar por dificultad
        if form.difficulty.data:
            query = query.filter(Recipe.difficulty == form.difficulty.data)
        
        # Filtrar por calificación mínima
        if form.min_rating.data:
            min_rating = float(form.min_rating.data)
            # Subquery para calcular rating promedio
            from sqlalchemy import func
            rating_subquery = db.session.query(
                RecipeRating.recipe_id,
                func.avg(RecipeRating.rating).label('avg_rating')
            ).group_by(RecipeRating.recipe_id).subquery()
            
            query = query.join(rating_subquery, Recipe.id == rating_subquery.c.recipe_id)
            query = query.filter(rating_subquery.c.avg_rating >= min_rating)
        
        results = query.distinct().limit(20).all()
        
        # Si tenemos ML disponible, reordenar resultados usando content filter
        if expert_system.ml_models['content_filter'] and form.ingredients.data:
            try:
                ingredient_list = [ing.strip() for ing in form.ingredients.data.split(',')]
                recommended_ids = expert_system.ml_models['content_filter'].recommend_by_ingredients(
                    ingredient_list, n_recommendations=len(results)
                )
                
                # Reordenar results según ML recommendations
                results_dict = {r.id: r for r in results}
                reordered_results = []
                for rec_id in recommended_ids:
                    if rec_id in results_dict:
                        reordered_results.append(results_dict[rec_id])
                
                # Agregar cualquier resultado que no esté en las recomendaciones ML
                for recipe in results:
                    if recipe not in reordered_results:
                        reordered_results.append(recipe)
                
                results = reordered_results
                print(f"✅ Resultados reordenados usando ML: {len(results)}")
                
            except Exception as e:
                print(f"⚠️ Error aplicando ML a búsqueda avanzada: {e}")
    
    return render_template('advanced_search.html', form=form, results=results)

@main.route('/nutrition_guide')
def nutrition_guide():
    """Guía nutricional con categorización ML"""
    
    # Intentar usar ML para categorización nutricional más precisa
    nutritional_categories = {
        'high_protein': [],
        'high_fiber': [],
        'low_sodium': [],
        'vitamin_rich': []
    }
    
    try:
        # Obtener todas las recetas con información nutricional
        recipes_with_nutrition = Recipe.query.filter(Recipe.nutritional_info.isnot(None)).all()
        
        # Si tenemos clustering ML, usar para mejor categorización
        if expert_system.ml_models['clustering'] and hasattr(expert_system.ml_models['clustering'], 'cluster_labels'):
            try:
                # Usar análisis de clusters para encontrar patrones nutricionales
                nutritional_categories = categorize_recipes_with_ml(recipes_with_nutrition)
                print("✅ Categorización nutricional usando ML")
            except Exception as e:
                print(f"⚠️ Error en categorización ML: {e}")
                nutritional_categories = categorize_recipes_traditional(recipes_with_nutrition)
        else:
            nutritional_categories = categorize_recipes_traditional(recipes_with_nutrition)
        
        print(f"🍎 Categorías nutricionales: {[(k, len(v)) for k, v in nutritional_categories.items()]}")
        
    except Exception as e:
        print(f"❌ Error en nutrition_guide: {e}")
        # Fallback: usar recetas aleatorias
        try:
            all_recipes = Recipe.query.limit(24).all()
            chunk_size = len(all_recipes) // 4
            if chunk_size > 0:
                nutritional_categories = {
                    'high_protein': all_recipes[0:chunk_size],
                    'high_fiber': all_recipes[chunk_size:chunk_size*2],
                    'low_sodium': all_recipes[chunk_size*2:chunk_size*3],
                    'vitamin_rich': all_recipes[chunk_size*3:chunk_size*4]
                }
        except:
            pass
    
    return render_template('nutrition_guide.html', categories=nutritional_categories)

def categorize_recipes_with_ml(recipes):
    """Categorización nutricional usando ML clustering"""
    categories = {
        'high_protein': [],
        'high_fiber': [],
        'low_sodium': [],
        'vitamin_rich': []
    }
    
    # Usar clustering para encontrar patrones nutricionales
    try:
        for recipe in recipes:
            if recipe.nutritional_info:
                nutrition = recipe.nutritional_info
                
                # Aplicar lógica mejorada con ML insights
                protein_score = (nutrition.protein or 0) / 25.0  # Normalizar
                fiber_score = (nutrition.fiber or 0) / 10.0
                sodium_score = 1.0 - min((nutrition.sodium or 800) / 2000.0, 1.0)  # Invertir (menos sodio = mejor)
                vitamin_score = ((nutrition.vitamin_c or 0) / 100.0 + 
                               (nutrition.vitamin_a or 0) / 1000.0) / 2.0
                
                # Asignar a categoría con mayor score
                scores = {
                    'high_protein': protein_score,
                    'high_fiber': fiber_score,
                    'low_sodium': sodium_score,
                    'vitamin_rich': vitamin_score
                }
                
                best_category = max(scores, key=scores.get)
                if scores[best_category] > 0.6:  # Umbral mínimo
                    if len(categories[best_category]) < 6:
                        categories[best_category].append(recipe)
        
        return categories
        
    except Exception as e:
        print(f"Error en categorización ML: {e}")
        return categorize_recipes_traditional(recipes)

def categorize_recipes_traditional(recipes):
    """Categorización nutricional tradicional"""
    categories = {
        'high_protein': [],
        'high_fiber': [],
        'low_sodium': [],
        'vitamin_rich': []
    }
    
    for recipe in recipes:
        if recipe.nutritional_info:
            nutrition = recipe.nutritional_info
            
            # Recetas altas en proteína (20g+)
            if nutrition.protein and nutrition.protein >= 20:
                if len(categories['high_protein']) < 6:
                    categories['high_protein'].append(recipe)
            
            # Recetas altas en fibra (8g+)
            if nutrition.fiber and nutrition.fiber >= 8:
                if len(categories['high_fiber']) < 6:
                    categories['high_fiber'].append(recipe)
            
            # Recetas bajas en sodio (600mg o menos)
            if nutrition.sodium and nutrition.sodium <= 600:
                if len(categories['low_sodium']) < 6:
                    categories['low_sodium'].append(recipe)
            
            # Recetas ricas en vitamina C (30mg+)
            if nutrition.vitamin_c and nutrition.vitamin_c >= 30:
                if len(categories['vitamin_rich']) < 6:
                    categories['vitamin_rich'].append(recipe)
    
    return categories

@main.route('/cooking_assistant')
@login_required
def cooking_assistant():
    """Asistente de cocina con IA"""
    return render_template('cooking_assistant.html')

@main.route('/chat_assistant', methods=['POST'])
@login_required
def chat_assistant():
    """Endpoint para el asistente de cocina con ML"""
    user_message = request.json.get('message', '')
    
    response = {
        'message': '',
        'recommendations': [],
        'tips': []
    }
    
    try:
        # Usar expert system para procesar mensaje y generar respuesta
        # El expert system ya tiene integrado el procesamiento NLP
        if 'receta' in user_message.lower() or 'cocinar' in user_message.lower():
            # Extraer ingredientes del mensaje si los hay
            ingredients = extract_ingredients_from_message(user_message)
            
            if ingredients:
                # Obtener recomendaciones usando ML
                recommendations = expert_system.get_recommendations(
                    current_user.id,
                    ingredients,
                    {}
                )
                
                response['recommendations'] = [
                    {
                        'id': recipe.id,
                        'name': recipe.name,
                        'prep_time': recipe.prep_time,
                        'difficulty': recipe.difficulty,
                        'rating': recipe.average_rating
                    } for recipe in recommendations[:3]
                ]
                
                response['message'] = f"Encontré {len(recommendations)} recetas con {', '.join(ingredients)}. ¡Echa un vistazo!"
            else:
                response['message'] = "Para recomendarte recetas específicas, menciona qué ingredientes tienes. Por ejemplo: 'Tengo pollo, arroz y tomate'"
        else:
            response['message'] = "¿En qué puedo ayudarte? Puedo recomendarte recetas, explicar técnicas culinarias o resolver problemas de cocina."
        
    except Exception as e:
        print(f"Error en chat assistant: {e}")
        response['message'] = "Disculpa, hubo un error. ¿Podrías intentar de nuevo?"
    
    return jsonify(response)

def extract_ingredients_from_message(message):
    """Extrae ingredientes mencionados en un mensaje"""
    # Lista básica de ingredientes comunes
    common_ingredients = [
        'pollo', 'carne', 'pescado', 'arroz', 'pasta', 'tomate', 'cebolla', 
        'ajo', 'papa', 'zanahoria', 'pimiento', 'huevo', 'queso', 'leche'
    ]
    
    message_lower = message.lower()
    found_ingredients = []
    
    for ingredient in common_ingredients:
        if ingredient in message_lower:
            found_ingredients.append(ingredient)
    
    return found_ingredients

@main.route('/generate_pdf', methods=['POST'])
@login_required
def generate_pdf():
    """Generar PDF con recetas seleccionadas"""
    form = PDFGenerationForm()
    
    if form.validate_on_submit():
        try:
            recipe_ids = [int(id.strip()) for id in form.recipe_ids.data.split(',') if id.strip()]
            recipes = Recipe.query.filter(Recipe.id.in_(recipe_ids)).all()
            
            if not recipes:
                flash('No se encontraron recetas para generar PDF', 'error')
                return redirect(url_for('main.dashboard'))
            
            # Generar PDF
            from app.pdf_generator import RecipePDFGenerator
            pdf_generator = RecipePDFGenerator()
            
            pdf_options = {
                'include_nutritional_info': form.include_nutritional_info.data,
                'include_substitutions': form.include_substitutions.data,
                'include_tips': form.include_tips.data
            }
            
            print(f"🔄 Generando PDF para {len(recipes)} recetas...")
            pdf_path = pdf_generator.generate_recipes_pdf(
                recipes, 
                current_user.username,
                pdf_options
            )
            
            if pdf_path and os.path.exists(pdf_path):
                print(f"✅ PDF generado exitosamente: {pdf_path}")
                
                filename = os.path.basename(pdf_path)
                
                try:
                    response = send_file(
                        pdf_path,
                        as_attachment=True,
                        download_name=filename,
                        mimetype='application/pdf'
                    )
                    
                    # Cleanup programado
                    import threading
                    import time
                    
                    def cleanup_file():
                        time.sleep(10)
                        try:
                            if os.path.exists(pdf_path):
                                os.remove(pdf_path)
                                print(f"🗑️ Archivo temporal eliminado: {pdf_path}")
                        except Exception as e:
                            print(f"⚠️ No se pudo eliminar archivo temporal: {e}")
                    
                    cleanup_thread = threading.Thread(target=cleanup_file)
                    cleanup_thread.daemon = True
                    cleanup_thread.start()
                    
                    flash(f'PDF generado exitosamente: {len(recipes)} recetas', 'success')
                    return response
                    
                except Exception as e:
                    print(f"❌ Error enviando archivo: {e}")
                    flash('PDF generado pero error al descargar. Revisa tu carpeta Downloads.', 'warning')
                    
            else:
                print(f"❌ Error: PDF no se generó correctamente")
                flash('Error al generar PDF. Intenta nuevamente.', 'error')
                
        except Exception as e:
            print(f"❌ Error general en generate_pdf: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Error al generar PDF: {str(e)}', 'error')
    
    else:
        print(f"❌ Formulario no válido: {form.errors}")
        flash('Datos del formulario inválidos', 'error')
    
    return redirect(url_for('main.dashboard'))

@main.route('/train_models')
@login_required
def train_models():
    """Entrenar modelos ML (solo para administradores)"""
    if current_user.username != 'admin':
        flash('No tienes permisos para esta acción', 'error')
        return redirect(url_for('main.dashboard'))
    
    try:
        # Entrenar sistema de recomendaciones
        if recommendation_engine:
            print("🔄 Entrenando RecommendationEngine...")
            recipes_data = prepare_recipes_data_for_ml()
            ratings_data = prepare_ratings_data_for_ml()
            recommendation_engine.train_models(recipes_data, ratings_data)
            print("✅ RecommendationEngine entrenado")
        
        # Entrenar clustering
        if clustering_model:
            print("🔄 Entrenando Clustering...")
            recipes_data = prepare_recipes_data_for_ml()
            clustering_model.train_clustering(recipes_data)
            print("✅ Clustering entrenado")
        
        flash('Modelos entrenados exitosamente', 'success')
        
    except Exception as e:
        print(f"❌ Error entrenando modelos: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Error entrenando modelos: {str(e)}', 'error')
    
    return redirect(url_for('main.dashboard'))

def prepare_ratings_data_for_ml():
    """Prepara datos de ratings para ML"""
    ratings = RecipeRating.query.all()
    ratings_data = []
    
    for rating in ratings:
        if rating.rated_recipe:
            user_profile = {
                'dietary_restrictions': [dr.name for dr in rating.rating_user.dietary_restrictions],
                'avg_rating_given': sum(r.rating for r in rating.rating_user.recipe_ratings) / len(rating.rating_user.recipe_ratings) if rating.rating_user.recipe_ratings else 4.0
            }
            
            ratings_data.append({
                'user_id': rating.user_id,
                'recipe_id': rating.recipe_id,
                'rating': rating.rating,
                'user_profile': user_profile
            })
    
    return ratings_data

@main.route('/my_recipes')
@login_required
def my_recipes():
    """Recetas calificadas por el usuario con análisis ML"""
    user_ratings = RecipeRating.query.filter_by(user_id=current_user.id).order_by(
        RecipeRating.created_at.desc()
    ).all()
    
    # Análisis de preferencias usando ML si está disponible
    preferences_analysis = None
    
    if user_ratings:
        try:
            if expert_system.ml_models['clustering']:
                # Usar clustering ML para análisis más sofisticado
                preferences_analysis = analyze_user_preferences_with_ml(current_user.id, user_ratings)
            else:
                # Análisis tradicional
                preferences_analysis = analyze_user_preferences_simple(current_user.id, user_ratings)
        except Exception as e:
            print(f"Error en análisis de preferencias: {e}")
            preferences_analysis = None
    
    return render_template('my_recipes.html', 
                         user_ratings=user_ratings,
                         preferences_analysis=preferences_analysis)

def analyze_user_preferences_with_ml(user_id, user_ratings):
    """Análisis de preferencias usando ML clustering"""
    try:
        # Obtener recetas bien calificadas
        high_rated_recipes = [rating.rated_recipe for rating in user_ratings if rating.rating >= 4 and rating.rated_recipe]
        
        if not high_rated_recipes:
            return analyze_user_preferences_simple(user_id, user_ratings)
        
        # Usar clustering para encontrar patrones
        recipe_features = []
        for recipe in high_rated_recipes:
            features = {
                'cuisine_type': recipe.cuisine_type or 'unknown',
                'difficulty': recipe.difficulty or 'fácil',
                'prep_time': recipe.prep_time or 30,
                'cook_time': recipe.cook_time or 30,
                'protein': recipe.nutritional_info.protein if recipe.nutritional_info else 15,
                'calories': recipe.nutritional_info.calories_per_serving if recipe.nutritional_info else 400
            }
            recipe_features.append(features)
        
        # Análisis de patrones
        favorite_cuisines = {}
        preferred_difficulty = {}
        avg_prep_time = sum(f['prep_time'] for f in recipe_features) / len(recipe_features)
        avg_calories = sum(f['calories'] for f in recipe_features) / len(recipe_features)
        
        for features in recipe_features:
            cuisine = features['cuisine_type']
            difficulty = features['difficulty']
            
            favorite_cuisines[cuisine] = favorite_cuisines.get(cuisine, 0) + 1
            preferred_difficulty[difficulty] = preferred_difficulty.get(difficulty, 0) + 1
        
        # Generar recomendaciones ML-enhanced
        recommendations = []
        
        if favorite_cuisines:
            top_cuisine = max(favorite_cuisines.items(), key=lambda x: x[1])
            recommendations.append(f"Prefieres especialmente la cocina {top_cuisine[0]} ({top_cuisine[1]} recetas)")
        
        if avg_prep_time < 30:
            recommendations.append("Te gustan las recetas rápidas de preparar")
        elif avg_prep_time > 60:
            recommendations.append("No te importa invertir tiempo en recetas elaboradas")
        
        if avg_calories < 350:
            recommendations.append("Tiendes a preferir opciones más ligeras")
        elif avg_calories > 500:
            recommendations.append("Prefieres platos más sustanciosos")
        
        return {
            'favorite_cuisines': favorite_cuisines,
            'preferred_difficulty': preferred_difficulty,
            'recommendations': recommendations,
            'high_rated_count': len(high_rated_recipes),
            'average_rating': sum(r.rating for r in user_ratings) / len(user_ratings),
            'avg_prep_time': avg_prep_time,
            'avg_calories': avg_calories
        }
        
    except Exception as e:
        print(f"Error en análisis ML: {e}")
        return analyze_user_preferences_simple(user_id, user_ratings)

def analyze_user_preferences_simple(user_id, user_ratings):
    """Análisis simple de preferencias sin ML"""
    if not user_ratings:
        return None
    
    favorite_cuisines = {}
    preferred_difficulty = {}
    high_rated_recipes = []
    
    for rating in user_ratings:
        if rating.rated_recipe:
            recipe = rating.rated_recipe
            
            if rating.rating >= 4 and recipe.cuisine_type:
                cuisine = recipe.cuisine_type
                favorite_cuisines[cuisine] = favorite_cuisines.get(cuisine, 0) + 1
            
            if recipe.difficulty:
                difficulty = recipe.difficulty
                preferred_difficulty[difficulty] = preferred_difficulty.get(difficulty, 0) + 1
            
            if rating.rating >= 4:
                high_rated_recipes.append(recipe)
    
    recommendations = []
    
    if favorite_cuisines:
        top_cuisine = max(favorite_cuisines.items(), key=lambda x: x[1])
        recommendations.append(f"Te gusta especialmente la cocina {top_cuisine[0]}")
    
    if preferred_difficulty:
        top_difficulty = max(preferred_difficulty.items(), key=lambda x: x[1])
        recommendations.append(f"Prefieres recetas de dificultad {top_difficulty[0]}")
    
    avg_rating = sum(r.rating for r in user_ratings) / len(user_ratings)
    if avg_rating >= 4:
        recommendations.append("Eres un crítico exigente, tus calificaciones son altas")
    
    return {
        'favorite_cuisines': favorite_cuisines,
        'preferred_difficulty': preferred_difficulty,
        'recommendations': recommendations,
        'high_rated_count': len(high_rated_recipes),
        'average_rating': avg_rating
    }

@main.route('/ingredient_suggestions')
def ingredient_suggestions():
    """API para sugerencias de ingredientes"""
    query = request.args.get('q', '').lower()
    
    if len(query) < 2:
        return jsonify([])
    
    ingredients = Ingredient.query.filter(
        Ingredient.name.ilike(f'%{query}%')
    ).limit(10).all()
    
    suggestions = [{'id': ing.id, 'name': ing.name} for ing in ingredients]
    
    return jsonify(suggestions)

@main.route('/recipe_of_the_day')
def recipe_of_the_day():
    """Receta del día con ML insights"""
    from datetime import date
    import hashlib
    
    today = date.today()
    seed = int(hashlib.md5(str(today).encode()).hexdigest(), 16) % 1000000
    
    total_recipes = Recipe.query.count()
    if total_recipes == 0:
        return render_template('recipe_of_the_day.html', recipe=None)
    
    # Si tenemos ML, usar para seleccionar mejor receta del día
    recipe = None
    try:
        if expert_system.ml_models['recommendation_engine']:
            # Usar ML para seleccionar receta más popular/recomendada
            high_rated_recipes = Recipe.query.filter(Recipe.average_rating >= 4.0).all()
            if high_rated_recipes:
                recipe_index = seed % len(high_rated_recipes)
                recipe = high_rated_recipes[recipe_index]
            else:
                recipe_index = seed % total_recipes
                recipe = Recipe.query.offset(recipe_index).first()
        else:
            # Método tradicional
            recipe_index = seed % total_recipes
            recipe = Recipe.query.offset(recipe_index).first()
    except Exception as e:
        print(f"Error seleccionando receta del día: {e}")
        recipe_index = seed % total_recipes
        recipe = Recipe.query.offset(recipe_index).first()
    
    # Información adicional
    nutritional_analysis = None
    cooking_tips = []
    
    if recipe:
        try:
            nutritional_analysis = expert_system.get_nutritional_analysis(recipe)
        except:
            nutritional_analysis = None
        
        try:
            cooking_tips = expert_system.generate_cooking_tips(recipe)
        except:
            cooking_tips = generate_simple_cooking_tips_for_recipe(recipe)
    
    return render_template('recipe_of_the_day.html', 
                         recipe=recipe,
                         nutritional_analysis=nutritional_analysis,
                         cooking_tips=cooking_tips)

def generate_simple_cooking_tips_for_recipe(recipe):
    """Genera consejos simples para una receta"""
    tips = []
    
    if not recipe:
        return tips
    
    tips.append("Lee toda la receta antes de empezar")
    tips.append("Prepara todos los ingredientes antes de cocinar")
    
    ingredient_names = [ing.name.lower() for ing in recipe.ingredients]
    ingredients_text = ' '.join(ingredient_names)
    
    if 'ajo' in ingredients_text:
        tips.append("Aplasta el ajo con el lado plano del cuchillo para pelarlo fácilmente")
    
    if 'cebolla' in ingredients_text:
        tips.append("Refrigera la cebolla 30 minutos antes de cortarla para evitar llorar")
    
    if 'arroz' in ingredients_text:
        tips.append("Lava el arroz hasta que el agua salga clara")
    
    if 'pollo' in ingredients_text:
        tips.append("Asegúrate de que el pollo alcance 75°C de temperatura interna")
    
    if recipe.difficulty == 'difícil':
        tips.append("Tómate tu tiempo y sigue cada paso cuidadosamente")
    elif recipe.difficulty == 'fácil':
        tips.append("Receta perfecta para principiantes")
    
    return tips[:5]