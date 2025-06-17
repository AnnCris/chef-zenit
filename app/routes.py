from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app.models import Recipe, Ingredient, User, DietaryRestriction, UserPreference, RecipeRating, db
from app.forms import IngredientInputForm, PreferencesForm, RecipeRatingForm, AdvancedSearchForm, PDFGenerationForm
from app.expert_system import CulinaryExpertSystem
from ml_models.clustering import RecipeClustering
from ml_models.recommendation_engine import RecommendationEngine
import json
from datetime import datetime
import os
from app.models import Recipe, Ingredient, User, DietaryRestriction, UserPreference, RecipeRating, NutritionalInfo, db

main = Blueprint('main', __name__)

# Inicializar sistema experto y modelos ML
expert_system = CulinaryExpertSystem()
clustering_model = RecipeClustering()
recommendation_engine = RecommendationEngine()

@main.route('/')
def index():
    """Página principal"""
    recent_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(6).all()
    return render_template('index.html', recent_recipes=recent_recipes)

@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard del usuario"""
    form = IngredientInputForm()
    
    # Obtener estadísticas del usuario con nombres de relación correctos
    user_stats = {
        'total_ratings': len(current_user.recipe_ratings),
        'avg_rating_given': sum(r.rating for r in current_user.recipe_ratings) / len(current_user.recipe_ratings) if current_user.recipe_ratings else 0,
        'favorite_recipes': Recipe.query.join(RecipeRating).filter(
            RecipeRating.user_id == current_user.id,
            RecipeRating.rating >= 4
        ).limit(5).all()
    }
    
    # Recomendaciones personalizadas basadas en clustering
    try:
        cluster_recommendations = clustering_model.get_cluster_recommendations_for_user(current_user.id, 5)
    except Exception as e:
        print(f"Error obteniendo recomendaciones: {e}")
        cluster_recommendations = []
    
    return render_template('dashboard.html', 
                         form=form, 
                         user_stats=user_stats,
                         cluster_recommendations=cluster_recommendations)

@main.route('/get_recommendations', methods=['POST'])
@login_required
def get_recommendations():
    """Obtiene recomendaciones basadas en ingredientes"""
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
            
            # Obtener recomendaciones del sistema experto
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
                    
                    # Recetas similares (simplificado por ahora)
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
    """Detalle de una receta específica"""
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
    
    # Análisis nutricional
    nutritional_analysis = expert_system.get_nutritional_analysis(recipe)
    
    # Recetas similares - usando clustering si está disponible
    similar_recipes = []
    try:
        if hasattr(clustering_model, 'get_similar_recipes'):
            similar_recipes = clustering_model.get_similar_recipes(recipe_id, 4)
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

def generate_simple_cooking_tips(recipe):
    """Genera consejos de cocina simples sin usar NLP"""
    tips = []
    
    # Consejos generales
    tips.append("Lee toda la receta antes de empezar a cocinar")
    tips.append("Prepara todos los ingredientes antes de comenzar (mise en place)")
    
    # Consejos específicos según ingredientes
    recipe_ingredients = [ing.name.lower() for ing in recipe.ingredients]
    ingredients_text = ' '.join(recipe_ingredients)
    
    if 'ajo' in ingredients_text:
        tips.append("Para pelar ajo fácilmente, aplástalo ligeramente con el lado plano del cuchillo")
    
    if 'cebolla' in ingredients_text:
        tips.append("Para evitar llorar al cortar cebolla, refrigérala 30 minutos antes")
    
    if 'arroz' in ingredients_text:
        tips.append("Lava el arroz hasta que el agua salga clara para mejor textura")
    
    if 'pollo' in ingredients_text:
        tips.append("Asegúrate de que el pollo alcance 75°C de temperatura interna")
    
    if 'pasta' in ingredients_text:
        tips.append("Agrega sal al agua cuando hierva, antes de añadir la pasta")
    
    if 'huevo' in ingredients_text:
        tips.append("Usa huevos a temperatura ambiente para mejores resultados")
    
    # Consejos según tiempo de preparación
    if recipe.total_time and recipe.total_time > 60:
        tips.append("Esta receta toma tiempo, considera prepararla en fin de semana")
    
    if recipe.difficulty == 'difícil':
        tips.append("Lee cada paso cuidadosamente y no te apresures")
    elif recipe.difficulty == 'fácil':
        tips.append("Esta es una receta perfecta para principiantes")
    
    # Consejos según tipo de cocina
    if recipe.cuisine_type:
        cuisine_tips = {
            'italiana': "Usa ingredientes frescos de buena calidad",
            'mexicana': "Ajusta el nivel de picante según tu tolerancia",
            'asiática': "Ten todos los ingredientes listos antes de empezar a cocinar",
            'mediterránea': "Usa aceite de oliva extra virgen para mejor sabor",
            'francesa': "La técnica es importante, sigue los pasos con precisión"
        }
        if recipe.cuisine_type in cuisine_tips:
            tips.append(cuisine_tips[recipe.cuisine_type])
    
    # Retornar máximo 5 consejos
    return tips[:5]

@main.route('/rate_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def rate_recipe(recipe_id):
    """Calificar una receta"""
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
            
            # Reentrenar modelos con nueva información
            recommendation_engine.train_models()
            
        except Exception as e:
            db.session.rollback()
            flash('Error al guardar la calificación', 'error')
    
    return redirect(url_for('main.recipe_detail', recipe_id=recipe_id))

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
    """Búsqueda avanzada de recetas"""
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
    
    return render_template('advanced_search.html', form=form, results=results)

@main.route('/nutrition_guide')
def nutrition_guide():
    """Guía nutricional con recomendaciones"""
    
    # Versión simplificada que funciona sin joins complejos
    nutritional_categories = {
        'high_protein': [],
        'high_fiber': [],
        'low_sodium': [],
        'vitamin_rich': []
    }
    
    try:
        # Obtener todas las recetas con información nutricional
        recipes_with_nutrition = Recipe.query.filter(Recipe.nutritional_info.isnot(None)).all()
        
        for recipe in recipes_with_nutrition:
            if recipe.nutritional_info:
                nutrition = recipe.nutritional_info
                
                # Recetas altas en proteína (20g+)
                if nutrition.protein and nutrition.protein >= 20:
                    if len(nutritional_categories['high_protein']) < 6:
                        nutritional_categories['high_protein'].append(recipe)
                
                # Recetas altas en fibra (8g+)
                if nutrition.fiber and nutrition.fiber >= 8:
                    if len(nutritional_categories['high_fiber']) < 6:
                        nutritional_categories['high_fiber'].append(recipe)
                
                # Recetas bajas en sodio (600mg o menos)
                if nutrition.sodium and nutrition.sodium <= 600:
                    if len(nutritional_categories['low_sodium']) < 6:
                        nutritional_categories['low_sodium'].append(recipe)
                
                # Recetas ricas en vitamina C (30mg+)
                if nutrition.vitamin_c and nutrition.vitamin_c >= 30:
                    if len(nutritional_categories['vitamin_rich']) < 6:
                        nutritional_categories['vitamin_rich'].append(recipe)
        
        print(f"🍎 Categorías nutricionales: {[(k, len(v)) for k, v in nutritional_categories.items()]}")
        
    except Exception as e:
        print(f"❌ Error en nutrition_guide: {e}")
        # Si hay error, usar recetas aleatorias
        try:
            all_recipes = Recipe.query.limit(24).all()
            # Dividir en 4 categorías
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

@main.route('/cooking_assistant')
@login_required
def cooking_assistant():
    """Asistente de cocina con chat interactivo"""
    return render_template('cooking_assistant.html')

@main.route('/chat_assistant', methods=['POST'])
@login_required
def chat_assistant():
    """Endpoint para el asistente de cocina"""
    user_message = request.json.get('message', '')
    
    # Procesar mensaje con NLP
    query_info = expert_system.nlp_processor.extract_recipe_query(user_message)
    nutritional_focus = expert_system.nlp_processor.extract_nutritional_queries(user_message)
    
    response = {
        'message': '',
        'recommendations': [],
        'tips': []
    }
    
    # Generar respuesta basada en la consulta
    if any(query_info.values()) or any(nutritional_focus.values()):
        # Buscar recetas basadas en la consulta procesada
        recommendations = expert_system.get_recommendations(
            current_user.id,
            query_info.get('ingredients', []),
            query_info
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
        
        response['message'] = "Encontré algunas recetas que podrían interesarte basadas en tu consulta."
    else:
        response['message'] = "¿Podrías ser más específico? Puedes preguntarme sobre recetas con ingredientes específicos, tipos de cocina, o necesidades nutricionales."
    
    return jsonify(response)

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
                
                # Crear nombre para la descarga
                filename = os.path.basename(pdf_path)
                
                try:
                    # Enviar archivo para descarga directa
                    response = send_file(
                        pdf_path,
                        as_attachment=True,
                        download_name=filename,
                        mimetype='application/pdf'
                    )
                    
                    # Programar eliminación del archivo después de la descarga
                    import threading
                    import time
                    
                    def cleanup_file():
                        time.sleep(10)  # Esperar 10 segundos antes de limpiar
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
    if current_user.username != 'admin':  # Simple verificación de admin
        flash('No tienes permisos para esta acción', 'error')
        return redirect(url_for('main.dashboard'))
    
    try:
        # Entrenar sistema de recomendaciones
        recommendation_engine.train_models()
        
        # Entrenar clustering
        clustering_model.train_clustering()
        
        flash('Modelos entrenados exitosamente', 'success')
    except Exception as e:
        flash(f'Error entrenando modelos: {str(e)}', 'error')
    
    return redirect(url_for('main.dashboard'))

@main.route('/my_recipes')
@login_required
def my_recipes():
    """Recetas calificadas por el usuario"""
    user_ratings = RecipeRating.query.filter_by(user_id=current_user.id).order_by(
        RecipeRating.created_at.desc()
    ).all()
    
    # Análisis simple de preferencias del usuario (sin clustering)
    preferences_analysis = None
    
    if user_ratings:
        try:
            # Análisis básico sin clustering
            preferences_analysis = analyze_user_preferences_simple(current_user.id, user_ratings)
        except Exception as e:
            print(f"Error en análisis de preferencias: {e}")
            preferences_analysis = None
    
    return render_template('my_recipes.html', 
                         user_ratings=user_ratings,
                         preferences_analysis=preferences_analysis)

def analyze_user_preferences_simple(user_id, user_ratings):
    """Análisis simple de preferencias sin clustering"""
    if not user_ratings:
        return None
    
    # Contar tipos de cocina favoritos
    favorite_cuisines = {}
    preferred_difficulty = {}
    high_rated_recipes = []
    
    for rating in user_ratings:
        if rating.rated_recipe:
            recipe = rating.rated_recipe
            
            # Contar tipos de cocina de recetas bien calificadas (4+)
            if rating.rating >= 4 and recipe.cuisine_type:
                cuisine = recipe.cuisine_type
                favorite_cuisines[cuisine] = favorite_cuisines.get(cuisine, 0) + 1
            
            # Contar dificultad preferida
            if recipe.difficulty:
                difficulty = recipe.difficulty
                preferred_difficulty[difficulty] = preferred_difficulty.get(difficulty, 0) + 1
            
            # Recopilar recetas muy bien calificadas
            if rating.rating >= 4:
                high_rated_recipes.append(recipe)
    
    # Generar recomendaciones simples
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
    elif avg_rating <= 2.5:
        recommendations.append("Eres selectivo con las recetas, busca nuevas opciones")
    
    if len([r for r in user_ratings if r.comment]) > len(user_ratings) * 0.5:
        recommendations.append("Te gusta compartir tu experiencia con comentarios detallados")
    
    return {
        'favorite_cuisines': favorite_cuisines,
        'preferred_difficulty': preferred_difficulty,
        'recommendations': recommendations,
        'high_rated_count': len(high_rated_recipes),
        'average_rating': avg_rating
    }

@main.route('/ingredient_suggestions')
def ingredient_suggestions():
    """API para sugerencias de ingredientes mientras se escribe"""
    query = request.args.get('q', '').lower()
    
    if len(query) < 2:
        return jsonify([])
    
    # Buscar ingredientes que contengan la consulta
    ingredients = Ingredient.query.filter(
        Ingredient.name.ilike(f'%{query}%')
    ).limit(10).all()
    
    suggestions = [{'id': ing.id, 'name': ing.name} for ing in ingredients]
    
    return jsonify(suggestions)

@main.route('/recipe_of_the_day')
def recipe_of_the_day():
    """Receta del día basada en la fecha actual"""
    from datetime import date
    import hashlib
    
    # Generar seed basado en la fecha para consistencia diaria
    today = date.today()
    seed = int(hashlib.md5(str(today).encode()).hexdigest(), 16) % 1000000
    
    # Obtener receta pseudoaleatoria pero consistente para el día
    total_recipes = Recipe.query.count()
    if total_recipes == 0:
        return render_template('recipe_of_the_day.html', recipe=None)
    
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
            # Consejos simples sin NLP
            cooking_tips = generate_simple_cooking_tips_for_recipe(recipe)
        except:
            cooking_tips = []
    
    return render_template('recipe_of_the_day.html', 
                         recipe=recipe,
                         nutritional_analysis=nutritional_analysis,
                         cooking_tips=cooking_tips)

def generate_simple_cooking_tips_for_recipe(recipe):
    """Genera consejos simples para una receta"""
    tips = []
    
    if not recipe:
        return tips
    
    # Consejos generales
    tips.append("Lee toda la receta antes de empezar")
    tips.append("Prepara todos los ingredientes antes de cocinar")
    
    # Consejos específicos por ingredientes
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
    
    # Consejos por dificultad
    if recipe.difficulty == 'difícil':
        tips.append("Tómate tu tiempo y sigue cada paso cuidadosamente")
    elif recipe.difficulty == 'fácil':
        tips.append("Receta perfecta para principiantes")
    
    return tips[:5]
