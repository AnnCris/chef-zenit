from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional, ValidationError    
from wtforms.widgets import CheckboxInput, ListWidget
import re
from app.models import User
 
# Validador personalizado para email
def email_validator(form, field):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, field.data):
        raise ValidationError('Por favor ingresa un email válido.')
    
class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repetir Contraseña', 
                             validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Registrarse')
            
class IngredientInputForm(FlaskForm):
    ingredients = TextAreaField('Ingredientes Disponibles', 
                               validators=[DataRequired()],
                               render_kw={"placeholder": "Ingresa los ingredientes que tienes separados por comas\nEjemplo: pollo, arroz, tomate, cebolla"})
    submit = SubmitField('Buscar Recetas')

class PreferencesForm(FlaskForm):
    dietary_restrictions = MultiCheckboxField('Restricciones Dietéticas', 
                                            coerce=int,
                                            choices=[])  # Se llenarán dinámicamente
    
    max_prep_time = SelectField('Tiempo Máximo de Preparación',
                               choices=[
                                   ('', 'Sin preferencia'),
                                   ('15', '15 minutos'),
                                   ('30', '30 minutos'),
                                   ('45', '45 minutos'),
                                   ('60', '1 hora'),
                                   ('120', '2 horas')
                               ])
    
    difficulty_preference = SelectField('Dificultad Preferida',
                                      choices=[
                                          ('', 'Sin preferencia'),
                                          ('fácil', 'Fácil'),
                                          ('medio', 'Medio'),
                                          ('difícil', 'Difícil')
                                      ])
    
    preferred_cuisines = MultiCheckboxField('Tipos de Cocina Preferidos',
                                          coerce=str,
                                          choices=[
                                              ('mexicana', 'Mexicana'),
                                              ('italiana', 'Italiana'),
                                              ('asiática', 'Asiática'),
                                              ('mediterránea', 'Mediterránea'),
                                              ('americana', 'Americana'),
                                              ('francesa', 'Francesa'),
                                              ('india', 'India'),
                                              ('árabe', 'Árabe')
                                          ])
    
    disliked_ingredients = TextAreaField('Ingredientes que no te gustan',
                                       render_kw={"placeholder": "Ingredientes que prefieres evitar, separados por comas"})
    
    submit = SubmitField('Guardar Preferencias')

class RecipeRatingForm(FlaskForm):
    rating = SelectField('Calificación',
                        choices=[
                            ('5', '★★★★★ Excelente'),
                            ('4', '★★★★☆ Muy bueno'),
                            ('3', '★★★☆☆ Bueno'),
                            ('2', '★★☆☆☆ Regular'),
                            ('1', '★☆☆☆☆ Malo')
                        ],
                        validators=[DataRequired()])
    
    comment = TextAreaField('Comentario (opcional)',
                           render_kw={"placeholder": "Comparte tu experiencia con esta receta..."})
    
    submit = SubmitField('Enviar Calificación')

class AdvancedSearchForm(FlaskForm):
    ingredients = StringField('Ingredientes',
                             render_kw={"placeholder": "Ingredientes separados por comas"})
    
    cuisine_type = SelectField('Tipo de Cocina',
                              choices=[
                                  ('', 'Todos'),
                                  ('mexicana', 'Mexicana'),
                                  ('italiana', 'Italiana'),
                                  ('asiática', 'Asiática'),
                                  ('mediterránea', 'Mediterránea'),
                                  ('americana', 'Americana'),
                                  ('francesa', 'Francesa'),
                                  ('india', 'India'),
                                  ('árabe', 'Árabe')
                              ])
    
    max_time = SelectField('Tiempo Máximo',
                          choices=[
                              ('', 'Sin límite'),
                              ('15', '15 minutos'),
                              ('30', '30 minutos'),
                              ('60', '1 hora'),
                              ('120', '2 horas')
                          ])
    
    difficulty = SelectField('Dificultad',
                            choices=[
                                ('', 'Todas'),
                                ('fácil', 'Fácil'),
                                ('medio', 'Medio'),
                                ('difícil', 'Difícil')
                            ])
    
    min_rating = SelectField('Calificación mínima',
                            choices=[
                                ('', 'Sin mínimo'),
                                ('3', '3+ estrellas'),
                                ('4', '4+ estrellas'),
                                ('5', '5 estrellas')
                            ])
    
    submit = SubmitField('Buscar')

class PDFGenerationForm(FlaskForm):
    include_nutritional_info = BooleanField('Incluir información nutricional', default=True)
    include_substitutions = BooleanField('Incluir sustitutos de ingredientes', default=True)
    include_tips = BooleanField('Incluir consejos de preparación', default=True)
    recipe_ids = StringField('', validators=[DataRequired()])  # Campo oculto
    submit = SubmitField('Generar PDF')