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
    
    if form.validate_on_submit():
        ingredients_text = form.ingredients.data
        
        # Obtener preferencias del usuario
        preferences = {}
        if current_user.user_preferences:
            pref = current_user.user_preferences[0]
            preferences = {
                'max_prep_time': pref.max_prep_time,
                'difficulty_preference': pref.difficulty_preference
            }
        
        # Obtener recomendaciones del sistema experto
        recommendations = expert_system.get_recommendations(
            current_user.id, 
            ingredients_text.split(','),
            preferences
        )
        
        # Calcular información adicional para cada receta
        enhanced_recommendations = []
        for recipe in recommendations:
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
            
            # Recetas similares
            similar_recipes = clustering_model.get_similar_recipes(recipe.id, 3)
            
            enhanced_recommendations.append({
                'recipe': recipe,
                'missing_info': missing_info,
                'substitutions': substitutions,
                'nutritional_analysis': nutritional_analysis,
                'similar_recipes': similar_recipes
            })
        
        return render_template('recommendations.html', 
                             recommendations=enhanced_recommendations,
                             search_ingredients=ingredients_text)
    
    flash('Por favor ingresa algunos ingredientes', 'error')
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
    
    # Recetas similares
    similar_recipes = clustering_model.get_similar_recipes(recipe_id, 4)
    
    # Consejos de cocina
    cooking_tips = expert_system.nlp_processor.generate_cooking_tips(
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
    # Obtener recetas agrupadas por beneficios nutricionales
    nutritional_categories = {
        'high_protein': Recipe.query.join(Recipe.nutritional_info).filter(
            Recipe.nutritional_info.has(protein__gte=20)
        ).limit(6).all(),
        'high_fiber': Recipe.query.join(Recipe.nutritional_info).filter(
            Recipe.nutritional_info.has(fiber__gte=8)
        ).limit(6).all(),
        'low_sodium': Recipe.query.join(Recipe.nutritional_info).filter(
            Recipe.nutritional_info.has(sodium__lte=600)
        ).limit(6).all(),
        'vitamin_rich': Recipe.query.join(Recipe.nutritional_info).filter(
            Recipe.nutritional_info.has(vitamin_c__gte=30)
        ).limit(6).all()
    }
    
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
        
        pdf_path = pdf_generator.generate_recipes_pdf(
            recipes, 
            current_user.username,
            pdf_options
        )
        
        if pdf_path and os.path.exists(pdf_path):
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f'recetas_{current_user.username}_{datetime.now().strftime("%Y%m%d")}.pdf'
            )
        else:
            flash('Error al generar PDF', 'error')
    
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
    
    # Análisis de preferencias del usuario basado en clustering
    user_preferences_analysis = clustering_model.analyze_user_preferences(current_user.id)
    
    return render_template('my_recipes.html', 
                         user_ratings=user_ratings,
                         preferences_analysis=user_preferences_analysis)

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
    nutritional_analysis = expert_system.get_nutritional_analysis(recipe)
    cooking_tips = expert_system.nlp_processor.generate_cooking_tips(recipe)
    
    return render_template('recipe_of_the_day.html', 
                         recipe=recipe,
                         nutritional_analysis=nutritional_analysis,
                         cooking_tips=cooking_tips)