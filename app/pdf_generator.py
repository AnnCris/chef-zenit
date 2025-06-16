from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
import re
import tempfile

class RecipePDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configurar estilos personalizados para el PDF"""
        # Estilo para títulos principales
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Estilo para títulos de recetas
        self.recipe_title_style = ParagraphStyle(
            'RecipeTitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkgreen
        )
        
        # Estilo para subtítulos
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=6,
            spaceBefore=12,
            textColor=colors.darkred
        )
        
        # Estilo para texto normal
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        )
        
        # Estilo para ingredientes
        self.ingredient_style = ParagraphStyle(
            'IngredientStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=3,
            leftIndent=20
        )
        
        # Estilo para instrucciones
        self.instruction_style = ParagraphStyle(
            'InstructionStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            leftIndent=15,
            alignment=TA_JUSTIFY
        )
    
    def generate_recipes_pdf(self, recipes, username, options=None):
        """
        Genera un PDF con las recetas seleccionadas y lo guarda en Downloads
        """
        if options is None:
            options = {
                'include_nutritional_info': True,
                'include_substitutions': True,
                'include_tips': True
            }
        
        try:
            # Usar la carpeta Downloads del usuario
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            
            # Si no existe Downloads, usar un directorio temporal
            if not os.path.exists(downloads_folder):
                downloads_folder = tempfile.gettempdir()
                print(f"⚠️ Downloads no encontrado, usando: {downloads_folder}")
            
            # Limpiar nombre de usuario para el archivo
            safe_username = re.sub(r'[^\w\-_.]', '_', username)
            
            # Nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recetas_{safe_username}_{timestamp}.pdf"
            
            # Ruta completa del archivo (usar solo barras normales)
            filepath = os.path.join(downloads_folder, filename).replace('\\', '/')
            
            print(f"📁 Generando PDF en: {filepath}")
            
            # Crear documento PDF
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=inch,
                leftMargin=inch,
                topMargin=inch,
                bottomMargin=inch
            )
            
            # Contenido del PDF
            story = []
            
            # Portada
            self._add_cover_page(story, username, len(recipes))
            
            # Índice
            self._add_table_of_contents(story, recipes)
            
            # Recetas
            for i, recipe in enumerate(recipes):
                self._add_recipe_page(story, recipe, options)
                if i < len(recipes) - 1:  # No agregar salto de página en la última receta
                    story.append(PageBreak())
            
            # Información nutricional resumida
            if options.get('include_nutritional_info', True):
                self._add_nutritional_summary(story, recipes)
            
            # Generar PDF
            print("🔄 Construyendo PDF...")
            doc.build(story)
            
            # Verificar que el archivo se creó correctamente
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath) / 1024  # Tamaño en KB
                print(f"✅ PDF generado exitosamente: {filename} ({file_size:.1f} KB)")
                return filepath
            else:
                print(f"❌ Error: El archivo no se creó en {filepath}")
                return None
                
        except Exception as e:
            print(f"❌ Error generando PDF: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _add_cover_page(self, story, username, recipe_count):
        """Agregar portada al PDF"""
        story.append(Spacer(1, 2*inch))
        
        # Título principal
        title = Paragraph("Recetario Personal", self.title_style)
        story.append(title)
        story.append(Spacer(1, 0.5*inch))
        
        # Información del usuario
        user_info = Paragraph(f"Compilado para: <b>{username}</b>", self.normal_style)
        story.append(user_info)
        story.append(Spacer(1, 0.3*inch))
        
        # Fecha de generación
        date_info = Paragraph(
            f"Fecha de generación: {datetime.now().strftime('%d de %B de %Y')}",
            self.normal_style
        )
        story.append(date_info)
        story.append(Spacer(1, 0.3*inch))
        
        # Número de recetas
        recipe_info = Paragraph(f"Total de recetas: {recipe_count}", self.normal_style)
        story.append(recipe_info)
        story.append(Spacer(1, 1*inch))
        
        # Descripción
        description = Paragraph(
            "Este recetario ha sido generado por el Sistema Experto Culinario, "
            "incluyendo recomendaciones nutricionales, sustitutos de ingredientes "
            "y consejos de preparación personalizados.",
            self.normal_style
        )
        story.append(description)
        
        story.append(PageBreak())
    
    def _add_table_of_contents(self, story, recipes):
        """Agregar índice de contenidos"""
        story.append(Paragraph("Índice de Recetas", self.title_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Crear tabla con las recetas
        toc_data = [['#', 'Receta', 'Tiempo Total', 'Dificultad']]
        
        for i, recipe in enumerate(recipes, 1):
            total_time = f"{recipe.total_time} min" if recipe.total_time else "N/A"
            difficulty = recipe.difficulty or "No especificada"
            
            toc_data.append([
                str(i),
                recipe.name,
                total_time,
                difficulty
            ])
        
        # Crear tabla
        toc_table = Table(toc_data, colWidths=[0.5*inch, 3.5*inch, 1*inch, 1*inch])
        toc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(toc_table)
        story.append(PageBreak())
    
    def _add_recipe_page(self, story, recipe, options):
        """Agregar página de receta individual"""
        # Título de la receta
        story.append(Paragraph(recipe.name, self.recipe_title_style))
        
        # Información básica en tabla
        basic_info_data = []
        if recipe.prep_time:
            basic_info_data.append(['Tiempo de preparación:', f'{recipe.prep_time} minutos'])
        if recipe.cook_time:
            basic_info_data.append(['Tiempo de cocción:', f'{recipe.cook_time} minutos'])
        if recipe.servings:
            basic_info_data.append(['Porciones:', str(recipe.servings)])
        if recipe.difficulty:
            basic_info_data.append(['Dificultad:', recipe.difficulty.capitalize()])
        if recipe.cuisine_type:
            basic_info_data.append(['Tipo de cocina:', recipe.cuisine_type.capitalize()])
        
        if basic_info_data:
            basic_table = Table(basic_info_data, colWidths=[2*inch, 2*inch])
            basic_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            story.append(basic_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Descripción si existe
        if recipe.description:
            story.append(Paragraph("Descripción", self.subtitle_style))
            story.append(Paragraph(recipe.description, self.normal_style))
            story.append(Spacer(1, 0.2*inch))
        
        # Ingredientes
        story.append(Paragraph("Ingredientes", self.subtitle_style))
        for ingredient in recipe.ingredients:
            story.append(Paragraph(f"• {ingredient.name}", self.ingredient_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Instrucciones
        story.append(Paragraph("Instrucciones", self.subtitle_style))
        if recipe.instructions:
            # Dividir instrucciones en pasos usando función simple
            steps = self._clean_recipe_instructions_simple(recipe.instructions)
            
            for i, step in enumerate(steps, 1):
                step_text = f"<b>{i}.</b> {step}"
                story.append(Paragraph(step_text, self.instruction_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Información nutricional
        if options.get('include_nutritional_info', True) and recipe.nutritional_info:
            self._add_nutritional_info(story, recipe.nutritional_info)
        
        # Sustitutos de ingredientes
        if options.get('include_substitutions', True):
            self._add_substitutions_info(story, recipe)
        
        # Consejos de cocina
        if options.get('include_tips', True):
            self._add_cooking_tips(story, recipe)
    
    def _clean_recipe_instructions_simple(self, instructions_text):
        """Limpia y estructura las instrucciones de cocina de forma simple"""
        # Separar por pasos (números, puntos, etc.)
        steps = re.split(r'\d+[\.\)]\s*|\n\s*[-\*]\s*|\n{2,}', instructions_text)
        
        cleaned_steps = []
        for step in steps:
            step = step.strip()
            if step and len(step) > 10:  # Filtrar pasos muy cortos
                # Capitalizar primera letra
                step = step[0].upper() + step[1:] if step else step
                # Asegurar que termina con punto
                if not step.endswith('.'):
                    step += '.'
                cleaned_steps.append(step)
        
        return cleaned_steps
    
    def _add_nutritional_info(self, story, nutrition):
        """Agregar información nutricional"""
        story.append(Paragraph("Información Nutricional (por porción)", self.subtitle_style))
        
        # Crear tabla nutricional
        nutrition_data = [
            ['Nutriente', 'Cantidad', 'Nutriente', 'Cantidad']
        ]
        
        # Macronutrientes
        nutrition_data.append([
            'Calorías', f'{nutrition.calories_per_serving or 0:.0f} kcal',
            'Proteínas', f'{nutrition.protein or 0:.1f} g'
        ])
        nutrition_data.append([
            'Carbohidratos', f'{nutrition.carbs or 0:.1f} g',
            'Grasas', f'{nutrition.fat or 0:.1f} g'
        ])
        nutrition_data.append([
            'Fibra', f'{nutrition.fiber or 0:.1f} g',
            'Azúcar', f'{nutrition.sugar or 0:.1f} g'
        ])
        
        # Vitaminas y minerales
        if nutrition.vitamin_c:
            nutrition_data.append([
                'Vitamina C', f'{nutrition.vitamin_c:.1f} mg',
                'Sodio', f'{nutrition.sodium or 0:.0f} mg'
            ])
        
        if nutrition.iron:
            nutrition_data.append([
                'Hierro', f'{nutrition.iron:.1f} mg',
                'Calcio', f'{nutrition.calcium or 0:.0f} mg'
            ])
        
        nutrition_table = Table(nutrition_data, colWidths=[1.5*inch, 1*inch, 1.5*inch, 1*inch])
        nutrition_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.darkgreen)
        ]))
        
        story.append(nutrition_table)
        story.append(Spacer(1, 0.2*inch))
    
    def _add_substitutions_info(self, story, recipe):
        """Agregar información de sustitutos usando función simple"""
        substitutions = self._get_simple_substitutions(recipe)
        
        if substitutions:
            story.append(Paragraph("Sustitutos de Ingredientes", self.subtitle_style))
            
            for ingredient, subs in substitutions.items():
                story.append(Paragraph(f"<b>{ingredient}:</b>", self.normal_style))
                for sub in subs:
                    sub_text = f"  • {sub['substitute']} ({sub['ratio']})"
                    if sub.get('notes'):
                        sub_text += f" - {sub['notes']}"
                    story.append(Paragraph(sub_text, self.ingredient_style))
            
            story.append(Spacer(1, 0.2*inch))
    
    def _get_simple_substitutions(self, recipe):
        """Obtiene sustituciones simples sin usar expert_system"""
        substitutions = {}
        
        # Sustituciones básicas hardcodeadas
        common_substitutions = {
            'leche': [
                {'substitute': 'leche de almendra', 'ratio': '1:1', 'notes': 'Opción sin lactosa'},
                {'substitute': 'leche de coco', 'ratio': '1:1', 'notes': 'Sabor más cremoso'}
            ],
            'mantequilla': [
                {'substitute': 'aceite de coco', 'ratio': '1:1', 'notes': 'Opción vegana'},
                {'substitute': 'margarina', 'ratio': '1:1', 'notes': 'Sin lactosa'}
            ],
            'huevo': [
                {'substitute': 'linaza molida + agua', 'ratio': '1 tbsp + 3 tbsp agua', 'notes': 'Opción vegana'},
                {'substitute': 'aquafaba', 'ratio': '3 tbsp por huevo', 'notes': 'Líquido de garbanzos'}
            ],
            'azúcar': [
                {'substitute': 'stevia', 'ratio': '1:8', 'notes': 'Mucho más dulce'},
                {'substitute': 'miel', 'ratio': '3:4', 'notes': 'Opción natural'}
            ],
            'harina': [
                {'substitute': 'harina de arroz', 'ratio': '1:1', 'notes': 'Sin gluten'},
                {'substitute': 'harina de almendra', 'ratio': '1:1', 'notes': 'Baja en carbohidratos'}
            ]
        }
        
        # Buscar ingredientes que tengan sustitutos
        for ingredient in recipe.ingredients:
            ingredient_name = ingredient.name.lower()
            for key, subs in common_substitutions.items():
                if key in ingredient_name:
                    substitutions[ingredient.name] = subs
                    break
        
        return substitutions
    
    def _add_cooking_tips(self, story, recipe):
        """Agregar consejos de cocina usando función simple"""
        tips = self._generate_simple_cooking_tips(recipe)
        
        if tips:
            story.append(Paragraph("Consejos de Preparación", self.subtitle_style))
            
            for tip in tips:
                story.append(Paragraph(f"• {tip}", self.ingredient_style))
            
            story.append(Spacer(1, 0.2*inch))
    
    def _generate_simple_cooking_tips(self, recipe):
        """Genera consejos simples sin usar expert_system"""
        tips = []
        
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
        
        if 'pasta' in ingredients_text:
            tips.append("Agrega sal al agua cuando hierva, antes de la pasta")
        
        # Consejos por dificultad
        if recipe.difficulty == 'difícil':
            tips.append("Tómate tu tiempo y sigue cada paso cuidadosamente")
        elif recipe.difficulty == 'fácil':
            tips.append("Receta perfecta para principiantes")
        
        return tips[:5]  # Máximo 5 consejos
    
    def _add_nutritional_summary(self, story, recipes):
        """Agregar resumen nutricional de todas las recetas"""
        story.append(PageBreak())
        story.append(Paragraph("Resumen Nutricional", self.title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Calcular totales nutricionales
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        total_fiber = 0
        recipes_with_nutrition = 0
        
        for recipe in recipes:
            if recipe.nutritional_info:
                recipes_with_nutrition += 1
                nutrition = recipe.nutritional_info
                total_calories += nutrition.calories_per_serving or 0
                total_protein += nutrition.protein or 0
                total_carbs += nutrition.carbs or 0
                total_fat += nutrition.fat or 0
                total_fiber += nutrition.fiber or 0
        
        if recipes_with_nutrition > 0:
            # Promedios
            avg_calories = total_calories / recipes_with_nutrition
            avg_protein = total_protein / recipes_with_nutrition
            avg_carbs = total_carbs / recipes_with_nutrition
            avg_fat = total_fat / recipes_with_nutrition
            avg_fiber = total_fiber / recipes_with_nutrition
            
            # Crear tabla de resumen
            summary_data = [
                ['Nutriente', 'Promedio por Receta', 'Total (todas las recetas)'],
                ['Calorías', f'{avg_calories:.0f} kcal', f'{total_calories:.0f} kcal'],
                ['Proteínas', f'{avg_protein:.1f} g', f'{total_protein:.1f} g'],
                ['Carbohidratos', f'{avg_carbs:.1f} g', f'{total_carbs:.1f} g'],
                ['Grasas', f'{avg_fat:.1f} g', f'{total_fat:.1f} g'],
                ['Fibra', f'{avg_fiber:.1f} g', f'{total_fiber:.1f} g']
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.darkblue)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Información adicional
        story.append(Paragraph("Información Adicional", self.subtitle_style))
        
        additional_info = [
            "Este recetario fue generado automáticamente por el Sistema Experto Culinario.",
            "Las recomendaciones nutricionales son orientativas y no sustituyen el consejo médico.",
            "Los sustitutos de ingredientes están basados en equivalencias culinarias comunes.",
            "Para dudas específicas sobre nutrición, consulta con un profesional de la salud."
        ]
        
        for info in additional_info:
            story.append(Paragraph(f"• {info}", self.normal_style))