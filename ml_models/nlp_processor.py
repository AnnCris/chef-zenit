import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string

try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.stem import SnowballStemmer
    NLTK_AVAILABLE = True
    
    # Intentar descargar datos si no están disponibles
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
        
except ImportError:
    NLTK_AVAILABLE = False
    print("⚠️ NLTK no disponible - usando procesamiento básico")

class NLPProcessor:
    def __init__(self):
        # Configurar NLTK para español
        self.stemmer = SnowballStemmer('spanish')
        
        # Stop words en español
        self.spanish_stopwords = set([
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le',
            'da', 'su', 'por', 'son', 'con', 'no', 'me', 'uno', 'todo', 'también', 'muy',
            'una', 'del', 'al', 'para', 'como', 'pero', 'sus', 'las', 'si', 'ya', 'porque',
            'cuando', 'sin', 'sobre', 'este', 'ser', 'tiene', 'le', 'ha', 'estos', 'está',
            'entre', 'durante', 'tres', 'dos', 'cuatro', 'cinco', 'donde', 'cual', 'quien'
        ])
        
        # Diccionario de sinónimos de ingredientes
        self.ingredient_synonyms = {
            'jitomate': 'tomate',
            'elote': 'maíz',
            'chícharo': 'guisante',
            'frijol': 'alubia',
            'ejote': 'judía verde',
            'betabel': 'remolacha',
            'apio': 'celery',
            'chile': 'pimiento',
            'calabacita': 'calabacín',
            'papa': 'patata',
            'camote': 'boniato',
            'col': 'repollo',
            'cilantro': 'culantro',
            'puerco': 'cerdo',
            'res': 'carne de res',
            'pollo': 'carne de pollo'
        }
        
        # Unidades de medida comunes
        self.measurement_units = {
            'kg', 'kilogramo', 'kilogramos', 'kilo', 'kilos',
            'g', 'gramo', 'gramos', 'gr',
            'l', 'litro', 'litros',
            'ml', 'mililitro', 'mililitros',
            'taza', 'tazas', 'cup', 'cups',
            'cucharada', 'cucharadas', 'cda', 'tbsp',
            'cucharadita', 'cucharaditas', 'cdita', 'tsp',
            'pizca', 'pizcas',
            'rebanada', 'rebanadas',
            'pieza', 'piezas', 'pza',
            'diente', 'dientes',
            'rama', 'ramas',
            'hoja', 'hojas'
        }
    
    def _tokenize_safe(self, text):
        """Tokenización segura con fallback si NLTK no está disponible"""
        if NLTK_AVAILABLE and self.stemmer:
            try:
                return word_tokenize(text, language='spanish')
            except:
                pass
        
        # Fallback: tokenización básica
        # Remover puntuación y dividir por espacios
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text.lower().split()

    def process_ingredients(self, ingredient_text):
        """
        Procesa el texto de ingredientes ingresado por el usuario
        """
        if isinstance(ingredient_text, str):
            # Separar por comas, punto y coma o saltos de línea
            ingredients = re.split(r'[,;\n]+', ingredient_text)
        else:
            ingredients = ingredient_text
        
        processed_ingredients = []
        
        for ingredient in ingredients:
            if ingredient.strip():
                processed = self._process_single_ingredient(ingredient.strip())
                if processed:
                    processed_ingredients.extend(processed)
        
        return list(set(processed_ingredients))  # Eliminar duplicados
    
    def _process_single_ingredient(self, ingredient_text):
        """
        Procesa un ingrediente individual
        """
        # Convertir a minúsculas
        ingredient_text = ingredient_text.lower()
        
        # Remover puntuación
        ingredient_text = ingredient_text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenizar de forma segura
        tokens = self._tokenize_safe(ingredient_text)
        
        # Remover números y unidades de medida
        cleaned_tokens = []
        for token in tokens:
            if not self._is_number(token) and token not in self.measurement_units:
                cleaned_tokens.append(token)
        
        # Remover stop words
        filtered_tokens = [token for token in cleaned_tokens 
                          if token not in self.spanish_stopwords and len(token) > 2]
        
        # Aplicar stemming si está disponible
        final_ingredients = []
        for token in filtered_tokens:
            # Aplicar sinónimos
            if token in self.ingredient_synonyms:
                token = self.ingredient_synonyms[token]
            
            # Stemming si está disponible
            if self.stemmer:
                try:
                    stemmed_token = self.stemmer.stem(token)
                    final_ingredients.append(stemmed_token)
                except:
                    final_ingredients.append(token)
            else:
                final_ingredients.append(token)
        
        return final_ingredients
    
    def _is_number(self, text):
        """
        Verifica si un texto representa un número
        """
        try:
            float(text)
            return True
        except ValueError:
            # Verificar fracciones como "1/2", "3/4"
            if '/' in text:
                parts = text.split('/')
                if len(parts) == 2:
                    try:
                        float(parts[0])
                        float(parts[1])
                        return True
                    except ValueError:
                        pass
            return False
    
    def extract_recipe_query(self, user_input):
        """
        Extrae información estructurada de una consulta de usuario
        """
        user_input = user_input.lower()
        
        query_info = {
            'ingredients': [],
            'cuisine_type': None,
            'difficulty': None,
            'time_constraint': None,
            'dietary_restrictions': []
        }
        
        # Extraer tipo de cocina
        cuisine_patterns = {
            'mexicana': r'\b(mexican[ao]s?|méxico|azteca|tacos?|enchiladas?)\b',
            'italiana': r'\b(italian[ao]s?|italia|pasta|pizza|risotto)\b',
            'asiática': r'\b(asiátic[ao]s?|china|chino|japonés|sushi|wok)\b',
            'francesa': r'\b(frances[ao]s?|francia|francés)\b',
            'mediterránea': r'\b(mediterráne[ao]s?|grieg[ao]s?)\b'
        }
        
        for cuisine, pattern in cuisine_patterns.items():
            if re.search(pattern, user_input):
                query_info['cuisine_type'] = cuisine
                break
        
        # Extraer dificultad
        if re.search(r'\b(fácil|simple|sencill[ao]s?|rápid[ao]s?)\b', user_input):
            query_info['difficulty'] = 'fácil'
        elif re.search(r'\b(difícil|complej[ao]s?|avanzad[ao]s?)\b', user_input):
            query_info['difficulty'] = 'difícil'
        elif re.search(r'\b(medi[ao]s?|intermedi[ao]s?)\b', user_input):
            query_info['difficulty'] = 'medio'
        
        # Extraer restricciones de tiempo
        time_patterns = {
            15: r'\b(15|quince)\s*(minutos?|mins?)\b',
            30: r'\b(30|treinta)\s*(minutos?|mins?|media hora)\b',
            60: r'\b(60|una hora|1 hora)\b'
        }
        
        for minutes, pattern in time_patterns.items():
            if re.search(pattern, user_input):
                query_info['time_constraint'] = minutes
                break
        
        # Extraer restricciones dietéticas
        dietary_patterns = {
            'vegetariano': r'\b(vegetarian[ao]s?|sin carne)\b',
            'vegano': r'\b(vegan[ao]s?|sin lácteos|sin huevos)\b',
            'sin gluten': r'\b(sin gluten|libre de gluten|celíac[ao]s?)\b',
            'sin lactosa': r'\b(sin lactosa|intolerante lactosa)\b',
            'diabético': r'\b(diabétic[ao]s?|sin azúcar|bajo azúcar)\b'
        }
        
        for restriction, pattern in dietary_patterns.items():
            if re.search(pattern, user_input):
                query_info['dietary_restrictions'].append(restriction)
        
        return query_info
    
    def enhance_ingredient_matching(self, user_ingredient, database_ingredients):
        """
        Mejora el matching de ingredientes usando similaridad fonética y léxica
        """
        user_ingredient = user_ingredient.lower().strip()
        matches = []
        
        for db_ingredient in database_ingredients:
            db_name = db_ingredient.name.lower()
            
            # Coincidencia exacta
            if user_ingredient == db_name:
                matches.append((db_ingredient, 1.0))
                continue
            
            # Coincidencia parcial
            if user_ingredient in db_name or db_name in user_ingredient:
                similarity = max(len(user_ingredient), len(db_name)) / \
                           min(len(user_ingredient), len(db_name))
                matches.append((db_ingredient, similarity * 0.8))
                continue
            
            # Similitud de Levenshtein simplificada
            similarity = self._calculate_string_similarity(user_ingredient, db_name)
            if similarity > 0.6:
                matches.append((db_ingredient, similarity * 0.6))
        
        # Ordenar por similitud descendente
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:5]  # Top 5 matches
    
    def _calculate_string_similarity(self, str1, str2):
        """
        Calcula similitud entre dos strings usando distancia de Levenshtein
        """
        if len(str1) < len(str2):
            return self._calculate_string_similarity(str2, str1)
        
        if len(str2) == 0:
            return 0.0
        
        previous_row = list(range(len(str2) + 1))
        for i, c1 in enumerate(str1):
            current_row = [i + 1]
            for j, c2 in enumerate(str2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        max_len = max(len(str1), len(str2))
        return 1.0 - (previous_row[-1] / max_len)
    
    def generate_cooking_tips(self, recipe, user_skill_level='principiante'):
        """
        Genera consejos de cocina personalizados basados en la receta y nivel del usuario
        """
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
        if recipe.total_time > 60:
            tips.append("Esta receta toma tiempo, considera prepararla en fin de semana")
        
        if recipe.difficulty == 'difícil':
            tips.append("Lee cada paso cuidadosamente y no te apresures")
        
        return tips[:5]  # Máximo 5 consejos
    
    def extract_nutritional_queries(self, user_input):
        """
        Extrae consultas específicas sobre nutrición
        """
        user_input = user_input.lower()
        
        nutritional_focus = {
            'protein': False,
            'low_carb': False,
            'low_fat': False,
            'high_fiber': False,
            'low_sodium': False,
            'vitamins': False
        }
        
        # Patrones para diferentes necesidades nutricionales
        if re.search(r'\b(proteína|proteínas|músculo|ejercicio)\b', user_input):
            nutritional_focus['protein'] = True
        
        if re.search(r'\b(bajos? carbohidratos?|keto|cetogénic[ao])\b', user_input):
            nutritional_focus['low_carb'] = True
        
        if re.search(r'\b(baj[ao] en grasa|sin grasa|light)\b', user_input):
            nutritional_focus['low_fat'] = True
        
        if re.search(r'\b(fibra|digestión|estreñimiento)\b', user_input):
            nutritional_focus['high_fiber'] = True
        
        if re.search(r'\b(bajo sodio|sin sal|hipertensión)\b', user_input):
            nutritional_focus['low_sodium'] = True
        
        if re.search(r'\b(vitaminas?|minerales?|hierro|calcio)\b', user_input):
            nutritional_focus['vitamins'] = True
        
        return nutritional_focus
    
    def clean_recipe_instructions(self, instructions_text):
        """
        Limpia y estructura las instrucciones de cocina
        """
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