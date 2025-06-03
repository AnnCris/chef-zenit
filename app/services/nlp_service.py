import nltk
import re
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

# Descargar recursos de NLTK necesarios
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Cargar el modelo de spaCy para español
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    # Si el modelo no está disponible, intentamos descargarlo
    import sys
    import subprocess
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "es_core_news_sm"])
    nlp = spacy.load("es_core_news_sm")

class NLPService:
    def __init__(self):
        self.stop_words_es = set(stopwords.words('spanish'))
        self.stop_words_en = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
    def preprocesar_texto(self, texto, idioma='es'):
        """
        Preprocesa un texto: tokenización, eliminación de stopwords, lematización
        """
        if not texto:
            return []
            
        # Convertir a minúsculas
        texto = texto.lower()
        
        # Eliminar puntuación y números
        texto = re.sub(r'[^\w\s]', ' ', texto)
        texto = re.sub(r'\d+', ' ', texto)
        
        # Tokenizar
        tokens = word_tokenize(texto)
        
        # Eliminar stopwords
        stop_words = self.stop_words_es if idioma == 'es' else self.stop_words_en
        tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
        
        # Lematizar
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        return tokens
    
    def extraer_ingredientes(self, texto):
        """
        Extrae posibles ingredientes de un texto usando NER y patrones
        """
        doc = nlp(texto)
        
        # Extraer entidades que podrían ser ingredientes
        ingredientes = []
        
        # Buscar entidades de tipo MISC, PRODUCT, FOOD
        for ent in doc.ents:
            if ent.label_ in ["MISC", "PRODUCT"] or "food" in ent.label_.lower():
                ingredientes.append(ent.text.lower())
        
        # Buscar sustantivos que podrían ser ingredientes
        for token in doc:
            if token.pos_ == "NOUN" and token.text.lower() not in ingredientes:
                ingredientes.append(token.text.lower())
                
        # Limpiar y normalizar
        ingredientes = [ing.strip() for ing in ingredientes if len(ing.strip()) > 2]
        
        return ingredientes
    
    def extraer_restricciones(self, texto):
        """
        Extrae posibles restricciones dietéticas de un texto
        """
        # Lista de palabras clave asociadas a restricciones dietéticas
        restricciones_keywords = {
            'vegetariano': ['vegetariano', 'vegetal', 'sin carne'],
            'vegano': ['vegano', 'sin animal', 'sin productos animales'],
            'sin_gluten': ['sin gluten', 'celiaco', 'celíaco', 'celiaquía', 'celiaquia'],
            'sin_lactosa': ['sin lactosa', 'intolerante a la lactosa', 'alergia lactosa'],
            'bajo_sodio': ['bajo en sodio', 'sin sal', 'reducido en sal', 'hipertensión'],
            'bajo_azucar': ['bajo en azúcar', 'sin azúcar', 'diabético', 'diabetes'],
            'keto': ['keto', 'cetogénico', 'cetogenico', 'bajo en carbohidratos'],
            'paleo': ['paleo', 'paleolítico', 'paleolitico'],
        }
        
        restricciones_encontradas = []
        texto_lower = texto.lower()
        
        for restriccion, keywords in restricciones_keywords.items():
            for keyword in keywords:
                if keyword in texto_lower:
                    restricciones_encontradas.append(restriccion)
                    break
        
        return restricciones_encontradas
    
    def extraer_alergias(self, texto):
        """
        Extrae posibles alergias alimentarias de un texto
        """
        # Lista de alergenos comunes
        alergenos = {
            'lacteos': ['leche', 'lácteo', 'lacteo', 'queso', 'yogur', 'mantequilla', 'nata', 'crema'],
            'gluten': ['gluten', 'trigo', 'cebada', 'centeno', 'avena'],
            'frutos_secos': ['frutos secos', 'nuez', 'nueces', 'almendra', 'almendras', 'avellana', 
                           'avellanas', 'pistacho', 'pistachos', 'anacardo', 'anacardos', 'cacahuete', 'cacahuetes'],
            'mariscos': ['marisco', 'mariscos', 'camarón', 'camarones', 'gamba', 'gambas', 'langostino', 
                      'langostinos', 'cangrejo', 'langosta'],
            'pescado': ['pescado', 'atún', 'salmón', 'merluza', 'bacalao'],
            'huevo': ['huevo', 'huevos', 'clara', 'yema'],
            'soja': ['soja', 'soya', 'tofu', 'edamame'],
            'moluscos': ['moluscos', 'almeja', 'almejas', 'mejillón', 'mejillones', 'calamar', 'calamares', 'pulpo']
        }
        
        alergias_encontradas = []
        texto_lower = texto.lower()
        
        # Buscar menciones directas de alergias
        alergia_patterns = [
            r'soy\s+al[ée]rgic[oa]\s+a\s+(?P<alergia>[\w\s]+)',
            r'tengo\s+alergia\s+a\s+(?P<alergia>[\w\s]+)',
            r'alergia\s+a\s+(?P<alergia>[\w\s]+)',
            r'no\s+puedo\s+comer\s+(?P<alergia>[\w\s]+)',
            r'evitar\s+(?P<alergia>[\w\s]+)'
        ]
        
        for pattern in alergia_patterns:
            matches = re.finditer(pattern, texto_lower)
            for match in matches:
                alergia_text = match.group('alergia').strip()
                if alergia_text:
                    for key, keywords in alergenos.items():
                        for keyword in keywords:
                            if keyword in alergia_text:
                                alergias_encontradas.append(key)
        
        # Buscar menciones de alergenos específicos
        for alergeno, keywords in alergenos.items():
            for keyword in keywords:
                if keyword in texto_lower:
                    # Verificar que no sea una negación (no quiero leche vs. quiero leche)
                    indice = texto_lower.find(keyword)
                    inicio_contexto = max(0, indice - 15)
                    contexto = texto_lower[inicio_contexto:indice]
                    if 'no ' in contexto or 'sin ' in contexto or 'evitar ' in contexto:
                        alergias_encontradas.append(alergeno)
                        break
        
        # Eliminar duplicados
        return list(set(alergias_encontradas))
        
    def analizar_consulta_usuario(self, texto):
        """
        Analiza una consulta de usuario para extraer información relevante
        """
        resultado = {
            'ingredientes': self.extraer_ingredientes(texto),
            'restricciones': self.extraer_restricciones(texto),
            'alergias': self.extraer_alergias(texto),
            'texto_procesado': self.preprocesar_texto(texto)
        }
        
        return resultado