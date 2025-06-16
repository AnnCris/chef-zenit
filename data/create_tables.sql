-- Esquema de base de datos para Sistema Experto Culinario
-- PostgreSQL

-- Eliminar tablas si existen (para reinicialización)
DROP TABLE IF EXISTS user_restrictions CASCADE;
DROP TABLE IF EXISTS recipe_ingredients CASCADE;
DROP TABLE IF EXISTS ingredient_substitution CASCADE;
DROP TABLE IF EXISTS user_ingredient CASCADE;
DROP TABLE IF EXISTS recipe_rating CASCADE;
DROP TABLE IF EXISTS user_preference CASCADE;
DROP TABLE IF EXISTS nutritional_info CASCADE;
DROP TABLE IF EXISTS ingredient_nutrition CASCADE;
DROP TABLE IF EXISTS recipe CASCADE;
DROP TABLE IF EXISTS ingredient CASCADE;
DROP TABLE IF EXISTS dietary_restriction CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;

-- Tabla de usuarios
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    profile_image VARCHAR(200),
    bio TEXT
);

-- Tabla de restricciones dietéticas
CREATE TABLE dietary_restriction (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de ingredientes
CREATE TABLE ingredient (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50),
    calories_per_100g FLOAT,
    common_allergen BOOLEAN DEFAULT FALSE,
    seasonal_availability VARCHAR(50), -- primavera, verano, otoño, invierno, todo_año
    storage_tips TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de recetas
CREATE TABLE recipe (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    instructions TEXT NOT NULL,
    prep_time INTEGER, -- en minutos
    cook_time INTEGER, -- en minutos
    servings INTEGER DEFAULT 4,
    difficulty VARCHAR(20) CHECK (difficulty IN ('fácil', 'medio', 'difícil')),
    cuisine_type VARCHAR(50),
    image_path VARCHAR(200),
    video_url VARCHAR(300),
    source_url VARCHAR(300),
    author VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_public BOOLEAN DEFAULT TRUE,
    featured BOOLEAN DEFAULT FALSE
);

-- Tabla de información nutricional por receta
CREATE TABLE nutritional_info (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipe(id) ON DELETE CASCADE,
    calories_per_serving FLOAT,
    protein FLOAT, -- gramos
    carbs FLOAT,   -- gramos
    fat FLOAT,     -- gramos
    fiber FLOAT,   -- gramos
    sugar FLOAT,   -- gramos
    sodium FLOAT,  -- miligramos
    -- Vitaminas principales
    vitamin_a FLOAT,   -- microgramos
    vitamin_c FLOAT,   -- miligramos
    vitamin_d FLOAT,   -- microgramos
    vitamin_e FLOAT,   -- miligramos
    vitamin_k FLOAT,   -- microgramos
    vitamin_b1 FLOAT,  -- miligramos (tiamina)
    vitamin_b2 FLOAT,  -- miligramos (riboflavina)
    vitamin_b3 FLOAT,  -- miligramos (niacina)
    vitamin_b6 FLOAT,  -- miligramos
    vitamin_b12 FLOAT, -- microgramos
    folate FLOAT,      -- microgramos
    -- Minerales principales
    iron FLOAT,        -- miligramos
    calcium FLOAT,     -- miligramos
    potassium FLOAT,   -- miligramos
    magnesium FLOAT,   -- miligramos
    zinc FLOAT,        -- miligramos
    phosphorus FLOAT,  -- miligramos
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(recipe_id)
);

-- Tabla de relación muchos a muchos: recetas-ingredientes
CREATE TABLE recipe_ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipe(id) ON DELETE CASCADE,
    ingredient_id INTEGER REFERENCES ingredient(id) ON DELETE CASCADE,
    quantity VARCHAR(50), -- ej: "2", "1/2", "al gusto"
    unit VARCHAR(20),     -- ej: "tazas", "cdas", "piezas", "kg"
    is_optional BOOLEAN DEFAULT FALSE,
    preparation_note VARCHAR(100), -- ej: "picado finamente", "cocido"
    UNIQUE(recipe_id, ingredient_id)
);

-- Tabla de preferencias del usuario
CREATE TABLE user_preference (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    preferred_cuisines JSON, -- array de tipos de cocina preferidos
    disliked_ingredients JSON, -- array de ingredientes que no le gustan
    max_prep_time INTEGER, -- tiempo máximo de preparación preferido
    difficulty_preference VARCHAR(20) CHECK (difficulty_preference IN ('fácil', 'medio', 'difícil')),
    dietary_goals VARCHAR(100), -- ej: "perder peso", "ganar músculo", "mantener"
    spice_tolerance VARCHAR(20) CHECK (spice_tolerance IN ('bajo', 'medio', 'alto')),
    cooking_skill_level VARCHAR(20) CHECK (cooking_skill_level IN ('principiante', 'intermedio', 'avanzado')),
    budget_preference VARCHAR(20) CHECK (budget_preference IN ('bajo', 'medio', 'alto')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- Tabla de calificaciones de recetas
CREATE TABLE recipe_rating (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    recipe_id INTEGER REFERENCES recipe(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    would_make_again BOOLEAN,
    difficulty_rating INTEGER CHECK (difficulty_rating >= 1 AND difficulty_rating <= 5),
    taste_rating INTEGER CHECK (taste_rating >= 1 AND taste_rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, recipe_id)
);

-- Tabla de ingredientes disponibles del usuario
CREATE TABLE user_ingredient (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    ingredient_id INTEGER REFERENCES ingredient(id) ON DELETE CASCADE,
    quantity VARCHAR(50),
    unit VARCHAR(20),
    expiry_date DATE,
    purchase_date DATE,
    storage_location VARCHAR(50), -- refrigerador, congelador, despensa
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, ingredient_id)
);

-- Tabla de sustituciones de ingredientes
CREATE TABLE ingredient_substitution (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipe(id) ON DELETE CASCADE,
    original_ingredient_id INTEGER REFERENCES ingredient(id) ON DELETE CASCADE,
    substitute_ingredient_id INTEGER REFERENCES ingredient(id) ON DELETE CASCADE,
    conversion_ratio VARCHAR(50), -- ej: "1:1", "2:3", "al gusto"
    notes TEXT,
    dietary_benefit VARCHAR(100), -- ej: "sin gluten", "vegano", "bajo sodio"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(recipe_id, original_ingredient_id, substitute_ingredient_id)
);

-- Tabla de relación muchos a muchos: usuarios-restricciones dietéticas
CREATE TABLE user_restrictions (
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    restriction_id INTEGER REFERENCES dietary_restriction(id) ON DELETE CASCADE,
    severity VARCHAR(20) CHECK (severity IN ('leve', 'moderada', 'severa')),
    notes TEXT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, restriction_id)
);

-- Tabla de información nutricional detallada por ingrediente
CREATE TABLE ingredient_nutrition (
    id SERIAL PRIMARY KEY,
    ingredient_id INTEGER REFERENCES ingredient(id) ON DELETE CASCADE,
    -- Macronutrientes por 100g
    protein FLOAT DEFAULT 0,
    carbohydrates FLOAT DEFAULT 0,
    fat FLOAT DEFAULT 0,
    fiber FLOAT DEFAULT 0,
    sugar FLOAT DEFAULT 0,
    sodium FLOAT DEFAULT 0,
    -- Vitaminas
    vitamin_a FLOAT DEFAULT 0,      -- mcg
    vitamin_c FLOAT DEFAULT 0,      -- mg  
    vitamin_d FLOAT DEFAULT 0,      -- mcg
    vitamin_e FLOAT DEFAULT 0,      -- mg
    vitamin_k FLOAT DEFAULT 0,      -- mcg
    vitamin_b1 FLOAT DEFAULT 0,     -- mg (tiamina)
    vitamin_b2 FLOAT DEFAULT 0,     -- mg (riboflavina)
    vitamin_b3 FLOAT DEFAULT 0,     -- mg (niacina)
    vitamin_b6 FLOAT DEFAULT 0,     -- mg
    vitamin_b12 FLOAT DEFAULT 0,    -- mcg
    folate FLOAT DEFAULT 0,         -- mcg
    -- Minerales
    iron FLOAT DEFAULT 0,           -- mg
    calcium FLOAT DEFAULT 0,        -- mg
    potassium FLOAT DEFAULT 0,      -- mg
    magnesium FLOAT DEFAULT 0,      -- mg
    zinc FLOAT DEFAULT 0,           -- mg
    phosphorus FLOAT DEFAULT 0,     -- mg
    selenium FLOAT DEFAULT 0,       -- mcg
    -- Información adicional
    glycemic_index INTEGER,         -- índice glucémico
    water_content FLOAT,            -- porcentaje de agua
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ingredient_id)
);

-- Tabla de planes de comidas (opcional para futuras expansiones)
CREATE TABLE meal_plan (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    goal VARCHAR(50), -- ej: "pérdida de peso", "ganancia muscular"
    total_calories_target INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Tabla de comidas del plan
CREATE TABLE meal_plan_recipe (
    id SERIAL PRIMARY KEY,
    meal_plan_id INTEGER REFERENCES meal_plan(id) ON DELETE CASCADE,
    recipe_id INTEGER REFERENCES recipe(id) ON DELETE CASCADE,
    meal_date DATE NOT NULL,
    meal_type VARCHAR(20) CHECK (meal_type IN ('desayuno', 'almuerzo', 'cena', 'snack')),
    servings FLOAT DEFAULT 1,
    notes TEXT,
    completed BOOLEAN DEFAULT FALSE,
    UNIQUE(meal_plan_id, meal_date, meal_type)
);

-- Tabla de listas de compras
CREATE TABLE shopping_list (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_completed BOOLEAN DEFAULT FALSE,
    total_estimated_cost DECIMAL(10,2)
);

-- Tabla de items de lista de compras
CREATE TABLE shopping_list_item (
    id SERIAL PRIMARY KEY,
    shopping_list_id INTEGER REFERENCES shopping_list(id) ON DELETE CASCADE,
    ingredient_id INTEGER REFERENCES ingredient(id) ON DELETE CASCADE,
    quantity VARCHAR(50),
    unit VARCHAR(20),
    estimated_cost DECIMAL(8,2),
    is_purchased BOOLEAN DEFAULT FALSE,
    notes VARCHAR(200),
    priority INTEGER DEFAULT 1 CHECK (priority >= 1 AND priority <= 5)
);

-- Tabla de historial de cocina
CREATE TABLE cooking_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    recipe_id INTEGER REFERENCES recipe(id) ON DELETE CASCADE,
    cooked_date DATE NOT NULL,
    servings_made FLOAT,
    modifications TEXT, -- cambios que hizo el usuario
    success_rating INTEGER CHECK (success_rating >= 1 AND success_rating <= 5),
    time_taken INTEGER, -- tiempo real que tomó
    would_cook_again BOOLEAN,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX idx_user_email ON "user"(email);
CREATE INDEX idx_user_username ON "user"(username);
CREATE INDEX idx_recipe_name ON recipe(name);
CREATE INDEX idx_recipe_cuisine ON recipe(cuisine_type);
CREATE INDEX idx_recipe_difficulty ON recipe(difficulty);
CREATE INDEX idx_recipe_featured ON recipe(featured);
CREATE INDEX idx_ingredient_name ON ingredient(name);
CREATE INDEX idx_ingredient_category ON ingredient(category);
CREATE INDEX idx_ingredient_allergen ON ingredient(common_allergen);
CREATE INDEX idx_recipe_ingredients_recipe ON recipe_ingredients(recipe_id);
CREATE INDEX idx_recipe_ingredients_ingredient ON recipe_ingredients(ingredient_id);
CREATE INDEX idx_recipe_rating_recipe ON recipe_rating(recipe_id);
CREATE INDEX idx_recipe_rating_user ON recipe_rating(user_id);
CREATE INDEX idx_recipe_rating_rating ON recipe_rating(rating);
CREATE INDEX idx_user_ingredient_user ON user_ingredient(user_id);
CREATE INDEX idx_user_ingredient_expiry ON user_ingredient(expiry_date);
CREATE INDEX idx_nutritional_info_recipe ON nutritional_info(recipe_id);
CREATE INDEX idx_ingredient_nutrition_ingredient ON ingredient_nutrition(ingredient_id);
CREATE INDEX idx_cooking_history_user ON cooking_history(user_id);
CREATE INDEX idx_cooking_history_date ON cooking_history(cooked_date);

-- Crear índices compuestos para consultas frecuentes
CREATE INDEX idx_recipe_cuisine_difficulty ON recipe(cuisine_type, difficulty);
CREATE INDEX idx_recipe_prep_cook_time ON recipe(prep_time, cook_time);
CREATE INDEX idx_user_restrictions_combo ON user_restrictions(user_id, restriction_id);

-- Agregar triggers para actualizar timestamps automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar trigger a tablas relevantes
CREATE TRIGGER update_recipe_updated_at BEFORE UPDATE ON recipe
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_nutritional_info_updated_at BEFORE UPDATE ON nutritional_info
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_preference_updated_at BEFORE UPDATE ON user_preference
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_recipe_rating_updated_at BEFORE UPDATE ON recipe_rating
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ingredient_nutrition_updated_at BEFORE UPDATE ON ingredient_nutrition
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Crear vistas útiles para consultas frecuentes

-- Vista de recetas con información nutricional básica
CREATE VIEW recipe_with_nutrition AS
SELECT 
    r.id,
    r.name,
    r.description,
    r.prep_time,
    r.cook_time,
    (r.prep_time + r.cook_time) as total_time,
    r.servings,
    r.difficulty,
    r.cuisine_type,
    r.image_path,
    ni.calories_per_serving,
    ni.protein,
    ni.carbs,
    ni.fat,
    ni.fiber,
    ni.sodium,
    ROUND(AVG(rr.rating), 1) as avg_rating,
    COUNT(rr.rating) as rating_count
FROM recipe r
LEFT JOIN nutritional_info ni ON r.id = ni.recipe_id
LEFT JOIN recipe_rating rr ON r.id = rr.recipe_id
WHERE r.is_public = true
GROUP BY r.id, ni.calories_per_serving, ni.protein, ni.carbs, ni.fat, ni.fiber, ni.sodium;

-- Vista de ingredientes con información nutricional
CREATE VIEW ingredient_with_nutrition AS
SELECT 
    i.id,
    i.name,
    i.category,
    i.calories_per_100g,
    i.common_allergen,
    i.seasonal_availability,
    inn.protein,
    inn.carbohydrates,
    inn.fat,
    inn.fiber,
    inn.vitamin_c,
    inn.iron,
    inn.calcium
FROM ingredient i
LEFT JOIN ingredient_nutrition inn ON i.id = inn.ingredient_id;

-- Vista de recetas populares
CREATE VIEW popular_recipes AS
SELECT 
    r.id,
    r.name,
    r.cuisine_type,
    r.difficulty,
    ROUND(AVG(rr.rating), 1) as avg_rating,
    COUNT(rr.rating) as rating_count,
    COUNT(ch.id) as times_cooked
FROM recipe r
LEFT JOIN recipe_rating rr ON r.id = rr.recipe_id
LEFT JOIN cooking_history ch ON r.id = ch.recipe_id
WHERE r.is_public = true
GROUP BY r.id, r.name, r.cuisine_type, r.difficulty
HAVING COUNT(rr.rating) >= 3
ORDER BY avg_rating DESC, rating_count DESC;

-- Función para calcular compatibilidad de receta con restricciones dietéticas
CREATE OR REPLACE FUNCTION is_recipe_compatible_with_restrictions(recipe_id_param INTEGER, user_id_param INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    restriction_count INTEGER;
    incompatible_count INTEGER;
BEGIN
    -- Contar restricciones del usuario
    SELECT COUNT(*) INTO restriction_count
    FROM user_restrictions ur
    WHERE ur.user_id = user_id_param;
    
    -- Si no tiene restricciones, la receta es compatible
    IF restriction_count = 0 THEN
        RETURN TRUE;
    END IF;
    
    -- Verificar incompatibilidades (esto sería más complejo en la realidad)
    -- Por simplicidad, asumimos que ciertas combinaciones son incompatibles
    SELECT COUNT(*) INTO incompatible_count
    FROM user_restrictions ur
    JOIN dietary_restriction dr ON ur.restriction_id = dr.id
    JOIN recipe_ingredients ri ON ri.recipe_id = recipe_id_param
    JOIN ingredient i ON ri.ingredient_id = i.id
    WHERE ur.user_id = user_id_param
    AND (
        (dr.name = 'vegetariano' AND i.category = 'proteins' AND i.name LIKE '%carne%')
        OR (dr.name = 'vegano' AND i.category IN ('dairy', 'proteins') AND i.name IN ('huevo', 'leche', 'queso'))
        OR (dr.name = 'sin gluten' AND i.common_allergen = true AND i.name LIKE '%harina%')
        OR (dr.name = 'sin lactosa' AND i.category = 'dairy')
    );
    
    RETURN incompatible_count = 0;
END;
$ LANGUAGE plpgsql;

-- Función para calcular el score nutricional de una receta
CREATE OR REPLACE FUNCTION calculate_nutrition_score(recipe_id_param INTEGER)
RETURNS DECIMAL(5,2) AS $
DECLARE
    score DECIMAL(5,2) := 0;
    nutrition_record RECORD;
BEGIN
    SELECT * INTO nutrition_record
    FROM nutritional_info
    WHERE recipe_id = recipe_id_param;
    
    IF NOT FOUND THEN
        RETURN 0;
    END IF;
    
    -- Puntuación basada en diferentes factores nutricionales
    -- Proteína (max 25 puntos)
    IF nutrition_record.protein >= 20 THEN
        score := score + 25;
    ELSIF nutrition_record.protein >= 15 THEN
        score := score + 20;
    ELSIF nutrition_record.protein >= 10 THEN
        score := score + 15;
    END IF;
    
    -- Fibra (max 20 puntos)
    IF nutrition_record.fiber >= 8 THEN
        score := score + 20;
    ELSIF nutrition_record.fiber >= 5 THEN
        score := score + 15;
    ELSIF nutrition_record.fiber >= 3 THEN
        score := score + 10;
    END IF;
    
    -- Vitamina C (max 15 puntos)
    IF nutrition_record.vitamin_c >= 50 THEN
        score := score + 15;
    ELSIF nutrition_record.vitamin_c >= 25 THEN
        score := score + 10;
    ELSIF nutrition_record.vitamin_c >= 10 THEN
        score := score + 5;
    END IF;
    
    -- Hierro (max 15 puntos)
    IF nutrition_record.iron >= 4 THEN
        score := score + 15;
    ELSIF nutrition_record.iron >= 2 THEN
        score := score + 10;
    ELSIF nutrition_record.iron >= 1 THEN
        score := score + 5;
    END IF;
    
    -- Penalización por exceso de sodio (max -15 puntos)
    IF nutrition_record.sodium > 2000 THEN
        score := score - 15;
    ELSIF nutrition_record.sodium > 1500 THEN
        score := score - 10;
    ELSIF nutrition_record.sodium > 1000 THEN
        score := score - 5;
    END IF;
    
    -- Penalización por exceso de azúcar (max -10 puntos)
    IF nutrition_record.sugar > 20 THEN
        score := score - 10;
    ELSIF nutrition_record.sugar > 15 THEN
        score := score - 5;
    END IF;
    
    -- Asegurar que el score esté entre 0 y 100
    IF score < 0 THEN
        score := 0;
    ELSIF score > 100 THEN
        score := 100;
    END IF;
    
    RETURN score;
END;
$ LANGUAGE plpgsql;

-- Crear tabla para almacenar configuraciones del sistema
CREATE TABLE system_config (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    description TEXT,
    data_type VARCHAR(20) CHECK (data_type IN ('string', 'integer', 'float', 'boolean', 'json')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar configuraciones por defecto
INSERT INTO system_config (config_key, config_value, description, data_type) VALUES
('max_recommendations_per_user', '20', 'Número máximo de recomendaciones por usuario', 'integer'),
('min_recipe_rating_for_featured', '4.0', 'Calificación mínima para recetas destacadas', 'float'),
('enable_ingredient_substitutions', 'true', 'Habilitar sustituciones de ingredientes', 'boolean'),
('default_serving_size', '4', 'Tamaño de porción por defecto', 'integer'),
('max_cooking_time_quick_recipes', '30', 'Tiempo máximo para recetas rápidas (minutos)', 'integer'),
('featured_recipes_rotation_days', '7', 'Días para rotar recetas destacadas', 'integer'),
('enable_nutritional_analysis', 'true', 'Habilitar análisis nutricional', 'boolean'),
('supported_languages', '["es", "en"]', 'Idiomas soportados', 'json'),
('max_ingredients_per_recipe', '20', 'Máximo de ingredientes por receta', 'integer'),
('enable_ml_recommendations', 'true', 'Habilitar recomendaciones ML', 'boolean');

-- Crear tabla de logs para auditoría
CREATE TABLE activity_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50), -- 'recipe', 'ingredient', 'user', etc.
    entity_id INTEGER,
    details JSON,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para logs
CREATE INDEX idx_activity_log_user ON activity_log(user_id);
CREATE INDEX idx_activity_log_action ON activity_log(action);
CREATE INDEX idx_activity_log_created_at ON activity_log(created_at);
CREATE INDEX idx_activity_log_entity ON activity_log(entity_type, entity_id);

-- Tabla para almacenar métricas del sistema
CREATE TABLE system_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,4),
    metric_date DATE NOT NULL,
    additional_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(metric_name, metric_date)
);

-- Crear procedimiento para limpiar datos antiguos
CREATE OR REPLACE FUNCTION cleanup_old_data()
RETURNS VOID AS $
BEGIN
    -- Limpiar logs de actividad mayores a 90 días
    DELETE FROM activity_log 
    WHERE created_at < CURRENT_DATE - INTERVAL '90 days';
    
    -- Limpiar métricas mayores a 1 año
    DELETE FROM system_metrics 
    WHERE metric_date < CURRENT_DATE - INTERVAL '1 year';
    
    -- Limpiar ingredientes de usuario expirados hace más de 30 días
    DELETE FROM user_ingredient 
    WHERE expiry_date < CURRENT_DATE - INTERVAL '30 days';
    
    -- Log de limpieza
    INSERT INTO activity_log (action, details)
    VALUES ('system_cleanup', '{"cleaned_tables": ["activity_log", "system_metrics", "user_ingredient"]}');
END;
$ LANGUAGE plpgsql;

-- Crear función para obtener estadísticas del usuario
CREATE OR REPLACE FUNCTION get_user_statistics(user_id_param INTEGER)
RETURNS JSON AS $
DECLARE
    result JSON;
    total_recipes_rated INTEGER;
    avg_rating_given DECIMAL(3,2);
    total_recipes_cooked INTEGER;
    favorite_cuisine VARCHAR(50);
    total_cooking_time INTEGER;
BEGIN
    -- Calcular estadísticas
    SELECT COUNT(*), ROUND(AVG(rating), 2)
    INTO total_recipes_rated, avg_rating_given
    FROM recipe_rating
    WHERE user_id = user_id_param;
    
    SELECT COUNT(*)
    INTO total_recipes_cooked
    FROM cooking_history
    WHERE user_id = user_id_param;
    
    SELECT r.cuisine_type
    INTO favorite_cuisine
    FROM recipe_rating rr
    JOIN recipe r ON rr.recipe_id = r.id
    WHERE rr.user_id = user_id_param
    GROUP BY r.cuisine_type
    ORDER BY COUNT(*) DESC
    LIMIT 1;
    
    SELECT COALESCE(SUM(time_taken), 0)
    INTO total_cooking_time
    FROM cooking_history
    WHERE user_id = user_id_param;
    
    -- Construir JSON resultado
    result := json_build_object(
        'total_recipes_rated', COALESCE(total_recipes_rated, 0),
        'avg_rating_given', COALESCE(avg_rating_given, 0),
        'total_recipes_cooked', COALESCE(total_recipes_cooked, 0),
        'favorite_cuisine', COALESCE(favorite_cuisine, 'No data'),
        'total_cooking_time_minutes', COALESCE(total_cooking_time, 0)
    );
    
    RETURN result;
END;
$ LANGUAGE plpgsql;

-- Crear vista para el dashboard administrativo
CREATE VIEW admin_dashboard_stats AS
SELECT 
    'users' as metric_type,
    'Total Users' as metric_name,
    COUNT(*)::TEXT as metric_value,
    CURRENT_DATE as metric_date
FROM "user"
WHERE is_active = true

UNION ALL

SELECT 
    'recipes' as metric_type,
    'Total Recipes' as metric_name,
    COUNT(*)::TEXT as metric_value,
    CURRENT_DATE as metric_date
FROM recipe
WHERE is_public = true

UNION ALL

SELECT 
    'ratings' as metric_type,
    'Total Ratings' as metric_name,
    COUNT(*)::TEXT as metric_value,
    CURRENT_DATE as metric_date
FROM recipe_rating

UNION ALL

SELECT 
    'ingredients' as metric_type,
    'Total Ingredients' as metric_name,
    COUNT(*)::TEXT as metric_value,
    CURRENT_DATE as metric_date
FROM ingredient

UNION ALL

SELECT 
    'avg_rating' as metric_type,
    'Average Recipe Rating' as metric_name,
    ROUND(AVG(rating), 2)::TEXT as metric_value,
    CURRENT_DATE as metric_date
FROM recipe_rating;

-- Crear triggers para logging automático
CREATE OR REPLACE FUNCTION log_recipe_activity()
RETURNS TRIGGER AS $
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO activity_log (action, entity_type, entity_id, details)
        VALUES ('recipe_created', 'recipe', NEW.id, 
                json_build_object('name', NEW.name, 'cuisine', NEW.cuisine_type));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO activity_log (action, entity_type, entity_id, details)
        VALUES ('recipe_updated', 'recipe', NEW.id,
                json_build_object('name', NEW.name));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO activity_log (action, entity_type, entity_id, details)
        VALUES ('recipe_deleted', 'recipe', OLD.id,
                json_build_object('name', OLD.name));
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$ LANGUAGE plpgsql;

-- Aplicar trigger a la tabla recipe
CREATE TRIGGER recipe_activity_log 
    AFTER INSERT OR UPDATE OR DELETE ON recipe
    FOR EACH ROW EXECUTE FUNCTION log_recipe_activity();

-- Crear función para recalcular estadísticas diarias
CREATE OR REPLACE FUNCTION update_daily_metrics()
RETURNS VOID AS $
BEGIN
    -- Insertar métricas del día
    INSERT INTO system_metrics (metric_name, metric_value, metric_date)
    VALUES 
        ('total_users', (SELECT COUNT(*) FROM "user" WHERE is_active = true), CURRENT_DATE),
        ('total_recipes', (SELECT COUNT(*) FROM recipe WHERE is_public = true), CURRENT_DATE),
        ('total_ratings', (SELECT COUNT(*) FROM recipe_rating), CURRENT_DATE),
        ('avg_recipe_rating', (SELECT ROUND(AVG(rating), 2) FROM recipe_rating), CURRENT_DATE),
        ('recipes_cooked_today', (SELECT COUNT(*) FROM cooking_history WHERE cooked_date = CURRENT_DATE), CURRENT_DATE)
    ON CONFLICT (metric_name, metric_date) 
    DO UPDATE SET 
        metric_value = EXCLUDED.metric_value,
        created_at = CURRENT_TIMESTAMP;
END;
$ LANGUAGE plpgsql;

-- Comentarios finales y notas de uso
/*
INSTRUCCIONES DE USO:

1. Para crear la base de datos:
   createdb sistema_culinario

2. Para ejecutar este script:
   psql -d sistema_culinario -f create_tables.sql

3. Para cargar datos de ejemplo:
   psql -d sistema_culinario -f recipes_data.sql
   psql -d sistema_culinario -f nutritional_data.sql

4. Para configurar un usuario administrador:
   INSERT INTO "user" (username, email, password_hash) 
   VALUES ('admin', 'admin@example.com', 'hash_password_here');

5. Para limpiar datos antiguos (ejecutar periódicamente):
   SELECT cleanup_old_data();

6. Para actualizar métricas diarias:
   SELECT update_daily_metrics();

NOTAS IMPORTANTES:
- Todos los timestamps están en UTC
- Las contraseñas deben hashearse antes de almacenar
- Los valores nutricionales son por porción o por 100g según se especifique
- Las cantidades en recipe_ingredients son strings para mayor flexibilidad
- Los índices están optimizados para las consultas más frecuentes
- Las funciones y triggers proporcionan funcionalidad automática
- Las vistas simplifican consultas complejas frecuentes

EXTENSIONES FUTURAS:
- Agregar soporte para múltiples idiomas
- Implementar sistema de notificaciones
- Añadir funcionalidad de redes sociales
- Incluir sistema de puntos/gamificación
- Agregar soporte para videos de recetas
- Implementar sistema de comentarios anidados
- Añadir funcionalidad de planificación de comidas avanzada
*/