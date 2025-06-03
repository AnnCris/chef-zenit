-- Database: chef_virtual

-- DROP DATABASE IF EXISTS chef_virtual;

CREATE DATABASE chef_virtual
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Mexico.1252'
    LC_CTYPE = 'Spanish_Mexico.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- Tabla de Ingredientes
CREATE TABLE ingredientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    es_alergeno BOOLEAN DEFAULT FALSE,
    contiene_gluten BOOLEAN DEFAULT FALSE,
    info_nutricional JSONB
);

-- Tabla de Recetas
CREATE TABLE recetas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    tiempo_preparacion INTEGER, -- en minutos
    porciones INTEGER,
    dificultad VARCHAR(20),
    imagen_url VARCHAR(255),
    categoria VARCHAR(50),
    calorias INTEGER,
    proteinas FLOAT,
    carbohidratos FLOAT,
    grasas FLOAT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Relación Recetas-Ingredientes
CREATE TABLE receta_ingredientes (
    id SERIAL PRIMARY KEY,
    receta_id INTEGER REFERENCES recetas(id),
    ingrediente_id INTEGER REFERENCES ingredientes(id),
    cantidad FLOAT,
    unidad VARCHAR(30),
    es_opcional BOOLEAN DEFAULT FALSE
);

-- Tabla de Pasos de Preparación
CREATE TABLE pasos_preparacion (
    id SERIAL PRIMARY KEY,
    receta_id INTEGER REFERENCES recetas(id),
    numero_paso INTEGER,
    descripcion TEXT
);

-- Tabla de Valor Nutricional
CREATE TABLE valor_nutricional (
    id SERIAL PRIMARY KEY,
    receta_id INTEGER REFERENCES recetas(id),
    vitamina_a FLOAT,
    vitamina_c FLOAT,
    vitamina_d FLOAT,
    vitamina_e FLOAT,
    calcio FLOAT,
    hierro FLOAT,
    potasio FLOAT,
    otros_nutrientes JSONB
);

-- Tabla de Sustituciones
CREATE TABLE sustituciones (
    id SERIAL PRIMARY KEY,
    ingrediente_original_id INTEGER REFERENCES ingredientes(id),
    ingrediente_sustituto_id INTEGER REFERENCES ingredientes(id),
    tipo_sustitucion VARCHAR(50), -- ej: "sin_gluten", "vegano", "bajo_sodio"
    notas TEXT
);

-- Tabla de Restricciones Dietéticas
CREATE TABLE restricciones_dieteticas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT
);

-- Tabla Relación Recetas-Restricciones
CREATE TABLE receta_restricciones (
    receta_id INTEGER REFERENCES recetas(id),
    restriccion_id INTEGER REFERENCES restricciones_dieteticas(id),
    PRIMARY KEY (receta_id, restriccion_id)
);

-- Tabla para el histórico de recomendaciones al usuario
CREATE TABLE historico_recomendaciones (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100),
    receta_id INTEGER REFERENCES recetas(id),
    fecha_recomendacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    feedback INTEGER -- escala del 1-5
);

-- Tabla para almacenar preferencias de usuario
CREATE TABLE preferencias_usuario (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100),
    restricciones_dieteticas INTEGER[] REFERENCES restricciones_dieteticas(id),
    alergias INTEGER[] REFERENCES ingredientes(id),
    ingredientes_favoritos INTEGER[] REFERENCES ingredientes(id),
    ingredientes_evitados INTEGER[] REFERENCES ingredientes(id)
);