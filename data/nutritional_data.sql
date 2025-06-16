-- Información nutricional para las recetas del Sistema Experto Culinario
-- Ejecutar después de insertar las recetas

-- Información nutricional para Arroz con Pollo (ID: 1)
INSERT INTO nutritional_info (
    recipe_id, calories_per_serving, protein, carbs, fat, fiber, sugar, sodium,
    vitamin_a, vitamin_c, vitamin_d, vitamin_b12, iron, calcium
) VALUES (
    1, 452, 28.5, 55.2, 12.8, 3.2, 6.5, 820,
    185.5, 25.8, 0.2, 0.8, 2.4, 45.2
);

-- Información nutricional para Ensalada César (ID: 2)
INSERT INTO nutritional_info (
    recipe_id, calories_per_serving, protein, carbs, fat, fiber, sugar, sodium,
    vitamin_a, vitamin_c, vitamin_d, vitamin_b12, iron, calcium
) VALUES (
    2, 285, 8.2, 15.8, 22.4, 4.1, 3.2, 650,
    312.8, 18.5, 0.1, 0.2, 1.8, 125.4
);

-- Información nutricional para Sopa de Lentejas (ID: 3)
INSERT INTO nutritional_info (
    recipe_id, calories_per_serving, protein, carbs, fat, fiber, sugar, sodium,
    vitamin_a, vitamin_c, vitamin_d, vitamin_b12, iron, calcium
) VALUES (
    3, 320, 18.2, 45.8, 8.5, 12.3, 8.2, 420,
    458.2, 12.8, 0, 0, 4.2, 62.5
);

-- Información nutricional para Tacos de Pollo (ID: 4)
INSERT INTO nutritional_info (
    recipe_id, calories_per_serving, protein, carbs, fat, fiber, sugar, sodium,
    vitamin_a, vitamin_c, vitamin_d, vitamin_b12, iron, calcium
) VALUES (
    4, 380, 25.8, 32.5, 15.2, 5.8, 4.2, 680,
    125.8, 35.2, 0.1, 0.6, 2.8, 85.2
);

-- Información nutricional para Pasta Primavera (ID: 5)
INSERT INTO nutritional_info (
    recipe_id, calories_per_serving, protein, carbs, fat, fiber, sugar, sodium,
    vitamin_a, vitamin_c, vitamin_d, vitamin_b12, iron, calcium
) VALUES (
    5, 365, 12.5, 58.2, 10.8, 8.5, 12.8, 520,
    685.2, 95.8, 0, 0, 3.2, 95.8
);

-- Información nutricional para Salmón Teriyaki (ID: 6)
INSERT INTO nutritional_info (
    recipe_id, calories_per_serving, protein, carbs, fat, fiber, sugar, sodium,
    vitamin_a, vitamin_c, vitamin_d, vitamin_b12, iron, calcium
) VALUES (
    6, 485, 32.8, 48.5, 18.2, 2.1, 8.5, 950,
    85.2, 2.5, 12.8, 4.2, 1.8, 28.5
);

-- Información nutricional para Chili Vegetariano (ID: 7)
INSERT INTO nutritional_info (
    recipe_id, calories_per_serving, protein, carbs, fat, fiber, sugar, sodium,
    vitamin_a, vitamin_c, vitamin_d, vitamin_b12, iron, calcium
) VALUES (
    7, 285, 15.8, 48.2, 6.5, 15.2, 12.5, 380,
    485.2, 65.8, 0, 0, 5.2, 125.8
);

-- Información nutricional para Risotto de Champiñones (ID: 8)
INSERT INTO nutritional_info (
    recipe_id, calories_per_serving, protein, carbs, fat, fiber, sugar, sodium,
    vitamin_a, vitamin_c, vitamin_d, vitamin_b12, iron, calcium
) VALUES (
    8, 420, 14.2, 65.8, 12.5, 3.8, 4.2, 720,
    125.8, 8.5, 0.8, 0.2, 2.1, 185.2
);

-- Información nutricional para Bowl Buddha (ID: 9)
INSERT INTO nutritional_info (
    recipe_id, calories_per_serving, protein, carbs, fat, fiber, sugar, sodium,
    vitamin_a, vitamin_c, vitamin_d, vitamin_b12, iron, calcium
) VALUES (
    9, 385, 16.8, 52.5, 14.2, 11.8, 15.2, 320,
    1250.8, 125.8, 0, 0, 4.8, 158.2
);

-- Información nutricional para Pollo al Curry Thai (ID: 10)
INSERT INTO nutritional_info (
    recipe_id, calories_per_serving, protein, carbs, fat, fiber, sugar, sodium,
    vitamin_a, vitamin_c, vitamin_d, vitamin_b12, iron, calcium
) VALUES (
    10, 465, 28.2, 42.8, 20.5, 6.2, 8.8, 680,
    385.2, 85.8, 0.2, 0.8, 3.2, 85.2
);

-- Información nutricional adicional para ingredientes comunes
UPDATE ingredient SET calories_per_100g = 18 WHERE name = 'tomate';
UPDATE ingredient SET calories_per_100g = 40 WHERE name = 'cebolla';
UPDATE ingredient SET calories_per_100g = 149 WHERE name = 'ajo';
UPDATE ingredient SET calories_per_100g = 41 WHERE name = 'zanahoria';
UPDATE ingredient SET calories_per_100g = 16 WHERE name = 'apio';
UPDATE ingredient SET calories_per_100g = 31 WHERE name = 'pimiento rojo';
UPDATE ingredient SET calories_per_100g = 20 WHERE name = 'pimiento verde';
UPDATE ingredient SET calories_per_100g = 29 WHERE name = 'chile jalapeño';
UPDATE ingredient SET calories_per_100g = 26 WHERE name = 'calabaza';
UPDATE ingredient SET calories_per_100g = 34 WHERE name = 'brócoli';
UPDATE ingredient SET calories_per_100g = 23 WHERE name = 'espinaca';
UPDATE ingredient SET calories_per_100g = 15 WHERE name = 'lechuga';
UPDATE ingredient SET calories_per_100g = 16 WHERE name = 'pepino';
UPDATE ingredient SET calories_per_100g = 22 WHERE name = 'champiñón';
UPDATE ingredient SET calories_per_100g = 77 WHERE name = 'papa';
UPDATE ingredient SET calories_per_100g = 86 WHERE name = 'camote';
UPDATE ingredient SET calories_per_100g = 43 WHERE name = 'remolacha';
UPDATE ingredient SET calories_per_100g = 25 WHERE name = 'col';
UPDATE ingredient SET calories_per_100g = 25 WHERE name = 'coliflor';
UPDATE ingredient SET calories_per_100g = 35 WHERE name = 'ejotes';

-- Proteínas
UPDATE ingredient SET calories_per_100g = 165 WHERE name = 'pollo';
UPDATE ingredient SET calories_per_100g = 250 WHERE name = 'carne de res';
UPDATE ingredient SET calories_per_100g = 140 WHERE name = 'pescado';
UPDATE ingredient SET calories_per_100g = 208 WHERE name = 'salmón';
UPDATE ingredient SET calories_per_100g = 144 WHERE name = 'atún';
UPDATE ingredient SET calories_per_100g = 242 WHERE name = 'cerdo';
UPDATE ingredient SET calories_per_100g = 155 WHERE name = 'huevo';
UPDATE ingredient SET calories_per_100g = 132 WHERE name = 'frijol negro';
UPDATE ingredient SET calories_per_100g = 143 WHERE name = 'frijol pinto';
UPDATE ingredient SET calories_per_100g = 116 WHERE name = 'lenteja';
UPDATE ingredient SET calories_per_100g = 164 WHERE name = 'garbanzo';
UPDATE ingredient SET calories_per_100g = 76 WHERE name = 'tofu';
UPDATE ingredient SET calories_per_100g = 193 WHERE name = 'tempeh';
UPDATE ingredient SET calories_per_100g = 120 WHERE name = 'quinoa';

-- Cereales y granos
UPDATE ingredient SET calories_per_100g = 130 WHERE name = 'arroz blanco';
UPDATE ingredient SET calories_per_100g = 123 WHERE name = 'arroz integral';
UPDATE ingredient SET calories_per_100g = 131 WHERE name = 'pasta';
UPDATE ingredient SET calories_per_100g = 247 WHERE name = 'pan integral';
UPDATE ingredient SET calories_per_100g = 265 WHERE name = 'pan blanco';
UPDATE ingredient SET calories_per_100g = 364 WHERE name = 'harina de trigo';
UPDATE ingredient SET calories_per_100g = 361 WHERE name = 'harina de maíz';
UPDATE ingredient SET calories_per_100g = 389 WHERE name = 'avena';
UPDATE ingredient SET calories_per_100g = 354 WHERE name = 'cebada';
UPDATE ingredient SET calories_per_100g = 96 WHERE name = 'maíz';
UPDATE ingredient SET calories_per_100g = 218 WHERE name = 'tortilla de maíz';
UPDATE ingredient SET calories_per_100g = 304 WHERE name = 'tortilla de harina';

-- Lácteos
UPDATE ingredient SET calories_per_100g = 61 WHERE name = 'leche entera';
UPDATE ingredient SET calories_per_100g = 34 WHERE name = 'leche descremada';
UPDATE ingredient SET calories_per_100g = 403 WHERE name = 'queso cheddar';
UPDATE ingredient SET calories_per_100g = 280 WHERE name = 'queso mozzarella';
UPDATE ingredient SET calories_per_100g = 321 WHERE name = 'queso panela';
UPDATE ingredient SET calories_per_100g = 717 WHERE name = 'mantequilla';
UPDATE ingredient SET calories_per_100g = 345 WHERE name = 'crema';
UPDATE ingredient SET calories_per_100g = 59 WHERE name = 'yogurt natural';
UPDATE ingredient SET calories_per_100g = 100 WHERE name = 'yogurt griego';

-- Especias y condimentos (la mayoría tienen calorías negligibles)
UPDATE ingredient SET calories_per_100g = 0 WHERE name = 'sal';
UPDATE ingredient SET calories_per_100g = 251 WHERE name = 'pimienta negra';
UPDATE ingredient SET calories_per_100g = 375 WHERE name = 'comino';
UPDATE ingredient SET calories_per_100g = 265 WHERE name = 'orégano';
UPDATE ingredient SET calories_per_100g = 22 WHERE name = 'albahaca';
UPDATE ingredient SET calories_per_100g = 247 WHERE name = 'canela';
UPDATE ingredient SET calories_per_100g = 23 WHERE name = 'cilantro';
UPDATE ingredient SET calories_per_100g = 36 WHERE name = 'perejil';
UPDATE ingredient SET calories_per_100g = 101 WHERE name = 'tomillo';
UPDATE ingredient SET calories_per_100g = 131 WHERE name = 'romero';
UPDATE ingredient SET calories_per_100g = 282 WHERE name = 'paprika';
UPDATE ingredient SET calories_per_100g = 282 WHERE name = 'chile en polvo';
UPDATE ingredient SET calories_per_100g = 331 WHERE name = 'ajo en polvo';
UPDATE ingredient SET calories_per_100g = 341 WHERE name = 'cebolla en polvo';

-- Frutas
UPDATE ingredient SET calories_per_100g = 29 WHERE name = 'limón';
UPDATE ingredient SET calories_per_100g = 30 WHERE name = 'lima';
UPDATE ingredient SET calories_per_100g = 47 WHERE name = 'naranja';
UPDATE ingredient SET calories_per_100g = 52 WHERE name = 'manzana';
UPDATE ingredient SET calories_per_100g = 89 WHERE name = 'plátano';
UPDATE ingredient SET calories_per_100g = 32 WHERE name = 'fresa';
UPDATE ingredient SET calories_per_100g = 69 WHERE name = 'uva';
UPDATE ingredient SET calories_per_100g = 50 WHERE name = 'piña';
UPDATE ingredient SET calories_per_100g = 60 WHERE name = 'mango';
UPDATE ingredient SET calories_per_100g = 160 WHERE name = 'aguacate';
UPDATE ingredient SET calories_per_100g = 18 WHERE name = 'jitomate';

-- Grasas y aceites
UPDATE ingredient SET calories_per_100g = 884 WHERE name = 'aceite de oliva';
UPDATE ingredient SET calories_per_100g = 884 WHERE name = 'aceite vegetal';
UPDATE ingredient SET calories_per_100g = 862 WHERE name = 'aceite de coco';
UPDATE ingredient SET calories_per_100g = 902 WHERE name = 'manteca de cerdo';
UPDATE ingredient SET calories_per_100g = 884 WHERE name = 'aceite de aguacate';

-- Nuevos ingredientes agregados
UPDATE ingredient SET calories_per_100g = 22 WHERE name = 'vinagre de manzana';
UPDATE ingredient SET calories_per_100g = 304 WHERE name = 'miel';
UPDATE ingredient SET calories_per_100g = 380 WHERE name = 'azúcar morena';
UPDATE ingredient SET calories_per_100g = 0 WHERE name = 'stevia';
UPDATE ingredient SET calories_per_100g = 17 WHERE name = 'leche de almendra';
UPDATE ingredient SET calories_per_100g = 230 WHERE name = 'leche de coco';
UPDATE ingredient SET calories_per_100g = 595 WHERE name = 'tahini';
UPDATE ingredient SET calories_per_100g = 8 WHERE name = 'salsa de soja';
UPDATE ingredient SET calories_per_100g = 80 WHERE name = 'jengibre';
UPDATE ingredient SET calories_per_100g = 354 WHERE name = 'cúrcuma';
UPDATE ingredient SET calories_per_100g = 486 WHERE name = 'semillas de chía';
UPDATE ingredient SET calories_per_100g = 584 WHERE name = 'semillas de girasol';
UPDATE ingredient SET calories_per_100g = 628 WHERE name = 'avellana';
UPDATE ingredient SET calories_per_100g = 560 WHERE name = 'pistache';
UPDATE ingredient SET calories_per_100g = 277 WHERE name = 'dátil';
UPDATE ingredient SET calories_per_100g = 354 WHERE name = 'coco rallado';

-- Marcar ingredientes como alérgenos comunes
UPDATE ingredient SET common_allergen = true WHERE name IN (
    'huevo', 'pasta', 'pan integral', 'pan blanco', 'harina de trigo', 'cebada', 
    'tortilla de harina', 'leche entera', 'leche descremada', 'queso cheddar', 
    'queso mozzarella', 'queso panela', 'mantequilla', 'crema', 'yogurt natural', 
    'yogurt griego', 'tofu', 'tempeh', 'almendra', 'nuez', 'cacahuate', 
    'leche de almendra', 'tahini', 'salsa de soja', 'avellana', 'pistache'
);

-- Datos nutricionales adicionales específicos por vitaminas y minerales

-- Actualizar información de vitaminas para ingredientes ricos en vitamina C
UPDATE ingredient SET calories_per_100g = 53 WHERE name = 'pimiento rojo'; -- Rico en vitamina C
UPDATE ingredient SET calories_per_100g = 190 WHERE name = 'chile jalapeño'; -- Rico en vitamina C
UPDATE ingredient SET calories_per_100g = 89 WHERE name = 'brócoli'; -- Rico en vitamina C y K

-- Ingredientes ricos en hierro
UPDATE ingredient SET calories_per_100g = 116 WHERE name = 'lenteja'; -- Rica en hierro
UPDATE ingredient SET calories_per_100g = 25 WHERE name = 'espinaca'; -- Rica en hierro y folato

-- Ingredientes ricos en calcio
UPDATE ingredient SET calories_per_100g = 47 WHERE name = 'col'; -- Rica en calcio
UPDATE ingredient SET calories_per_100g = 25 WHERE name = 'brócoli'; -- Rico en calcio

-- Crear tabla de información nutricional detallada por ingrediente (opcional)
CREATE TABLE IF NOT EXISTS ingredient_nutrition (
    id SERIAL PRIMARY KEY,
    ingredient_id INTEGER REFERENCES ingredient(id),
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
    iron FLOAT DEFAULT 0,           -- mg
    calcium FLOAT DEFAULT 0,        -- mg
    potassium FLOAT DEFAULT 0,      -- mg
    magnesium FLOAT DEFAULT 0,      -- mg
    zinc FLOAT DEFAULT 0,           -- mg
    phosphorus FLOAT DEFAULT 0,     -- mg
    protein FLOAT DEFAULT 0,        -- g por 100g
    carbohydrates FLOAT DEFAULT 0,  -- g por 100g
    fat FLOAT DEFAULT 0,            -- g por 100g
    fiber FLOAT DEFAULT 0,          -- g por 100g
    sugar FLOAT DEFAULT 0,          -- g por 100g
    sodium FLOAT DEFAULT 0          -- mg por 100g
);

-- Insertar información nutricional detallada para ingredientes clave

-- Espinaca (muy nutritiva)
INSERT INTO ingredient_nutrition (
    ingredient_id, vitamin_a, vitamin_c, vitamin_k, folate, iron, calcium, 
    potassium, magnesium, protein, carbohydrates, fat, fiber
) VALUES (
    (SELECT id FROM ingredient WHERE name = 'espinaca'),
    469, 28.1, 483, 194, 2.7, 99, 558, 79, 2.9, 3.6, 0.4, 2.2
);

-- Brócoli (rico en vitaminas)
INSERT INTO ingredient_nutrition (
    ingredient_id, vitamin_a, vitamin_c, vitamin_k, folate, iron, calcium,
    potassium, protein, carbohydrates, fat, fiber
) VALUES (
    (SELECT id FROM ingredient WHERE name = 'brócoli'),
    31, 89.2, 102, 63, 0.7, 47, 316, 2.8, 6.6, 0.4, 2.6
);

-- Salmón (rico en omega-3 y vitamina D)
INSERT INTO ingredient_nutrition (
    ingredient_id, vitamin_d, vitamin_b12, protein, fat, phosphorus
) VALUES (
    (SELECT id FROM ingredient WHERE name = 'salmón'),
    11.0, 3.2, 25.4, 13.4, 200
);

-- Aguacate (grasas saludables)
INSERT INTO ingredient_nutrition (
    ingredient_id, vitamin_k, folate, potassium, protein, carbohydrates, fat, fiber
) VALUES (
    (SELECT id FROM ingredient WHERE name = 'aguacate'),
    21, 20, 485, 2.0, 8.5, 14.7, 6.7
);

-- Lentejas (proteína vegetal y hierro)
INSERT INTO ingredient_nutrition (
    ingredient_id, folate, iron, potassium, magnesium, protein, carbohydrates, fiber
) VALUES (
    (SELECT id FROM ingredient WHERE name = 'lenteja'),
    181, 3.3, 369, 36, 9.0, 20.1, 7.9
);

-- Quinoa (proteína completa)
INSERT INTO ingredient_nutrition (
    ingredient_id, iron, magnesium, phosphorus, protein, carbohydrates, fat, fiber
) VALUES (
    (SELECT id FROM ingredient WHERE name = 'quinoa'),
    1.5, 64, 152, 4.4, 21.3, 1.9, 2.8
);

-- Tomate (licopeno y vitamina C)
INSERT INTO ingredient_nutrition (
    ingredient_id, vitamin_a, vitamin_c, vitamin_k, potassium, protein, carbohydrates, fiber
) VALUES (
    (SELECT id FROM ingredient WHERE name = 'tomate'),
    42, 13.7, 7.9, 237, 0.9, 3.9, 1.2
);

-- Ajo (antioxidantes)
INSERT INTO ingredient_nutrition (
    ingredient_id, vitamin_c, vitamin_b6, calcium, phosphorus, protein, carbohydrates
) VALUES (
    (SELECT id FROM ingredient WHERE name = 'ajo'),
    31.2, 1.2, 181, 153, 6.4, 33.1
);

-- Crear índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_ingredient_nutrition_ingredient_id ON ingredient_nutrition(ingredient_id);
CREATE INDEX IF NOT EXISTS idx_nutritional_info_recipe_id ON nutritional_info(recipe_id);
CREATE INDEX IF NOT EXISTS idx_ingredient_category ON ingredient(category);
CREATE INDEX IF NOT EXISTS idx_ingredient_allergen ON ingredient(common_allergen);

-- Comentarios finales sobre el uso de estos datos
/*
Este archivo contiene información nutricional detallada para el Sistema Experto Culinario.

NOTAS IMPORTANTES:
1. Los valores nutricionales están basados en bases de datos como USDA y son aproximados
2. Los valores pueden variar según la preparación y origen de los alimentos
3. Para uso médico o dietético específico, consultar con profesionales de la salud
4. Los datos de alérgenos son generales y pueden variar según la persona

PARA ACTUALIZAR EN PRODUCCIÓN:
1. Revisar y validar todos los valores nutricionales
2. Agregar más ingredientes según necesidades regionales
3. Considerar variaciones estacionales en los valores nutricionales
4. Mantener actualizadas las listas de alérgenos según regulaciones locales

EXTENSIONES FUTURAS:
- Agregar información sobre índice glucémico
- Incluir datos sobre antioxidantes específicos
- Agregar información sobre sostenibilidad ambiental
- Incluir datos sobre origen y estacionalidad de ingredientes
*/