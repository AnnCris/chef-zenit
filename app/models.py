from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Tabla de asociación para restricciones dietéticas del usuario
user_restrictions = db.Table('user_restrictions',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('restriction_id', db.Integer, db.ForeignKey('dietary_restriction.id'), primary_key=True)
)

# Tabla de asociación para ingredientes de recetas
recipe_ingredients = db.Table('recipe_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True),
    db.Column('quantity', db.String(50)),
    db.Column('unit', db.String(20))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ✅ RELACIONES CORREGIDAS - cada una con backref único
    recipe_ratings = db.relationship('RecipeRating', backref='rating_user', lazy=True)
    user_preferences = db.relationship('UserPreference', backref='preference_user', lazy=True)
    available_ingredients = db.relationship('UserIngredient', backref='ingredient_owner', lazy=True)
    dietary_restrictions = db.relationship('DietaryRestriction', 
                                         secondary=user_restrictions, 
                                         backref='restricted_users')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer)  # en minutos
    cook_time = db.Column(db.Integer)  # en minutos
    servings = db.Column(db.Integer, default=4)
    difficulty = db.Column(db.String(20))  # fácil, medio, difícil
    cuisine_type = db.Column(db.String(50))
    image_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    ingredients = db.relationship('Ingredient', 
                                secondary=recipe_ingredients, 
                                backref='recipe_list')
    nutritional_info = db.relationship('NutritionalInfo', backref='recipe', uselist=False)
    ratings = db.relationship('RecipeRating', backref='rated_recipe', lazy=True)
    substitutions = db.relationship('IngredientSubstitution', backref='recipe', lazy=True)
    
    @property
    def total_time(self):
        return (self.prep_time or 0) + (self.cook_time or 0)
    
    @property
    def average_rating(self):
        if self.ratings:
            return sum(rating.rating for rating in self.ratings) / len(self.ratings)
        return 0

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50))  # vegetales, carnes, lácteos, etc.
    calories_per_100g = db.Column(db.Float)
    common_allergen = db.Column(db.Boolean, default=False)
    
    # Relaciones con backref únicos
    substitutions_as_original = db.relationship('IngredientSubstitution', 
                                              foreign_keys='IngredientSubstitution.original_ingredient_id',
                                              backref='original_ingredient')
    substitutions_as_substitute = db.relationship('IngredientSubstitution',
                                                foreign_keys='IngredientSubstitution.substitute_ingredient_id',
                                                backref='substitute_ingredient')

class DietaryRestriction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)

class NutritionalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    calories_per_serving = db.Column(db.Float)
    protein = db.Column(db.Float)  # gramos
    carbs = db.Column(db.Float)    # gramos
    fat = db.Column(db.Float)      # gramos
    fiber = db.Column(db.Float)    # gramos
    sugar = db.Column(db.Float)    # gramos
    sodium = db.Column(db.Float)   # mg
    
    # Vitaminas principales
    vitamin_a = db.Column(db.Float)  # mcg
    vitamin_c = db.Column(db.Float)  # mg
    vitamin_d = db.Column(db.Float)  # mcg
    vitamin_b12 = db.Column(db.Float) # mcg
    iron = db.Column(db.Float)       # mg
    calcium = db.Column(db.Float)    # mg

class IngredientSubstitution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    original_ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    substitute_ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    conversion_ratio = db.Column(db.String(50))  # ej: "1:1", "2:1"
    notes = db.Column(db.Text)

class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    preferred_cuisines = db.Column(db.JSON)  # lista de tipos de cocina preferidos
    disliked_ingredients = db.Column(db.JSON)  # lista de ingredientes que no le gustan
    max_prep_time = db.Column(db.Integer)  # tiempo máximo de preparación preferido
    difficulty_preference = db.Column(db.String(20))  # fácil, medio, difícil
    
class RecipeRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 estrellas
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserIngredient(db.Model):
    """Ingredientes que el usuario tiene disponibles"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.String(50))
    expiry_date = db.Column(db.Date)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con ingrediente
    ingredient = db.relationship('Ingredient', backref='user_stocks')