# Sistema Experto de Recomendación Culinaria

Un sistema inteligente para recomendar recetas basadas en los ingredientes disponibles, preferencias y restricciones dietéticas.

## Características

- Recomendación de recetas basadas en ingredientes disponibles
- Procesamiento de lenguaje natural para consultas en lenguaje natural
- Motor de inferencia para manejar restricciones dietéticas y alergias
- Sugerencia de ingredientes sustitutos
- Información nutricional detallada
- Generación de PDFs con recetas
- Algoritmo de filtrado basado en contenido para mejorar las recomendaciones

## Estructura del Proyecto

```
├── app/
│   ├── __init__.py
│   ├── config.py                 # Configuración de la aplicación
│   ├── models/                   # Modelos de datos
│   │   ├── __init__.py
│   │   ├── ingrediente.py
│   │   ├── receta.py
│   │   └── usuario.py
│   ├── routes/                   # Rutas de la API
│   │   ├── __init__.py
│   │   ├── ingredientes.py
│   │   └── recetas.py
│   ├── services/                 # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── recomendacion.py      # Sistema de recomendación
│   │   ├── nlp_service.py        # Procesamiento de lenguaje natural
│   │   ├── motor_inferencia.py   # Motor de inferencia
│   │   └── pdf_generator.py      # Generador de PDFs
│   ├── static/                   # Archivos estáticos
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/              # Imágenes de recetas
│   ├── templates/                # Plantillas HTML
│   │   ├── index.html
│   │   └── receta.html
│   └── utils/                    # Utilidades
│       ├── __init__.py
│       └── db.py                 # Conexión a la base de datos
├── ml_models/                    # Modelos de machine learning
│   ├── content_based_filter.py
│   └── content_based_model.pkl
├── scripts/                      # Scripts de utilidad
│   ├── init_db.py                # Inicializar la base de datos
│   └── train_model.py            # Entrenar el modelo de recomendación
├── .env                          # Variables de entorno
├── README.md                     # Este archivo
├── requirements.txt              # Dependencias del proyecto
└── run.py                        # Punto de entrada de la aplicación
```

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
   ```
   git clone https://github.com/tu-usuario/sistema-recomendacion-culinaria.git
   cd sistema-recomendacion-culinaria
   ```

2. Crear un entorno virtual e instalar dependencias:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configurar las variables de entorno:
   - Renombrar `.env.example` a `.env`
   - Editar el archivo `.env` con la configuración de tu base de datos PostgreSQL

4. Inicializar la base de datos:
   ```
   python scripts/init_db.py
   ```

5. Entrenar el modelo de recomendación (opcional, pero recomendado):
   ```
   python scripts/train_model.py
   ```

6. Ejecutar la aplicación:
   ```
   python run.py
   ```

7. Abrir en el navegador:
   ```
   http://localhost:5000
   ```

## Uso

1. **Recomendación por ingredientes**:
   - Introduce los ingredientes que tienes disponibles
   - El sistema recomendará recetas que puedes preparar

2. **Consulta en lenguaje natural**:
   - Describe lo que buscas (ej. "Quiero hacer algo rápido y saludable con pollo")
   - El sistema analizará tu consulta y recomendará recetas adecuadas

3. **Preferencias y restricciones**:
   - Configura tus restricciones dietéticas (vegetariano, sin gluten, etc.)
   - Añade ingredientes a evitar por alergias u otras razones

4. **Detalles de recetas**:
   - Ver ingredientes, pasos de preparación e información nutricional
   - Descargar recetas en PDF

## Tecnologías Utilizadas

- **Backend**: Python, Flask, SQLAlchemy
- **Base de datos**: PostgreSQL
- **NLP**: NLTK, spaCy
- **Machine Learning**: scikit-learn
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Generación de PDFs**: ReportLab

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.