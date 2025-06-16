-- Datos de ejemplo para el Sistema Experto Culinario
-- Ejecutar después de crear las tablas con Flask-Migrate

-- Restricciones dietéticas
INSERT INTO dietary_restriction (name, description) VALUES 
('vegetariano', 'Dieta que excluye carne y pescado'),
('vegano', 'Dieta que excluye todos los productos de origen animal'),
('sin gluten', 'Dieta libre de gluten para personas celíacas'),
('sin lactosa', 'Dieta libre de lactosa para intolerantes'),
('diabético', 'Dieta adecuada para personas con diabetes'),
('bajo sodio', 'Dieta baja en sodio para hipertensión'),
('paleo', 'Dieta paleolítica'),
('keto', 'Dieta cetogénica baja en carbohidratos');

-- Ingredientes por categorías
INSERT INTO ingredient (name, category, calories_per_100g, common_allergen) VALUES 
-- Verduras
('tomate', 'vegetables', 18, false),
('cebolla', 'vegetables', 40, false),
('ajo', 'vegetables', 149, false),
('zanahoria', 'vegetables', 41, false),
('apio', 'vegetables', 16, false),
('pimiento rojo', 'vegetables', 31, false),
('pimiento verde', 'vegetables', 20, false),
('chile jalapeño', 'vegetables', 29, false),
('calabaza', 'vegetables', 26, false),
('brócoli', 'vegetables', 34, false),
('espinaca', 'vegetables', 23, false),
('lechuga', 'vegetables', 15, false),
('pepino', 'vegetables', 16, false),
('champiñón', 'vegetables', 22, false),
('papa', 'vegetables', 77, false),
('camote', 'vegetables', 86, false),
('remolacha', 'vegetables', 43, false),
('col', 'vegetables', 25, false),
('coliflor', 'vegetables', 25, false),
('ejotes', 'vegetables', 35, false),

-- Proteínas
('pollo', 'proteins', 165, false),
('carne de res', 'proteins', 250, false),
('pescado', 'proteins', 140, false),
('salmón', 'proteins', 208, false),
('atún', 'proteins', 144, false),
('cerdo', 'proteins', 242, false),
('huevo', 'proteins', 155, true),
('frijol negro', 'proteins', 132, false),
('frijol pinto', 'proteins', 143, false),
('lenteja', 'proteins', 116, false),
('garbanzo', 'proteins', 164, false),
('tofu', 'proteins', 76, true),
('tempeh', 'proteins', 193, true),
('quinoa', 'proteins', 120, false),
('almendra', 'proteins', 579, true),
('nuez', 'proteins', 654, true),
('cacahuate', 'proteins', 567, true),

-- Cereales y granos
('arroz blanco', 'grains', 130, false),
('arroz integral', 'grains', 123, false),
('pasta', 'grains', 131, true),
('pan integral', 'grains', 247, true),
('pan blanco', 'grains', 265, true),
('harina de trigo', 'grains', 364, true),
('harina de maíz', 'grains', 361, false),
('avena', 'grains', 389, false),
('cebada', 'grains', 354, true),
('maíz', 'grains', 96, false),
('tortilla de maíz', 'grains', 218, false),
('tortilla de harina', 'grains', 304, true),

-- Lácteos
('leche entera', 'dairy', 61, true),
('leche descremada', 'dairy', 34, true),
('queso cheddar', 'dairy', 403, true),
('queso mozzarella', 'dairy', 280, true),
('queso panela', 'dairy', 321, true),
('mantequilla', 'dairy', 717, true),
('crema', 'dairy', 345, true),
('yogurt natural', 'dairy', 59, true),
('yogurt griego', 'dairy', 100, true),

-- Especias y condimentos
('sal', 'spices', 0, false),
('pimienta negra', 'spices', 251, false),
('comino', 'spices', 375, false),
('orégano', 'spices', 265, false),
('albahaca', 'spices', 22, false),
('canela', 'spices', 247, false),
('cilantro', 'spices', 23, false),
('perejil', 'spices', 36, false),
('tomillo', 'spices', 101, false),
('romero', 'spices', 131, false),
('paprika', 'spices', 282, false),
('chile en polvo', 'spices', 282, false),
('ajo en polvo', 'spices', 331, false),
('cebolla en polvo', 'spices', 341, false),

-- Frutas
('limón', 'fruits', 29, false),
('lima', 'fruits', 30, false),
('naranja', 'fruits', 47, false),
('manzana', 'fruits', 52, false),
('plátano', 'fruits', 89, false),
('fresa', 'fruits', 32, false),
('uva', 'fruits', 69, false),
('piña', 'fruits', 50, false),
('mango', 'fruits', 60, false),
('aguacate', 'fruits', 160, false),
('jitomate', 'fruits', 18, false),

-- Grasas y aceites
('aceite de oliva', 'fats', 884, false),
('aceite vegetal', 'fats', 884, false),
('aceite de coco', 'fats', 862, false),
('manteca de cerdo', 'fats', 902, false),
('aceite de aguacate', 'fats', 884, false);

-- Recetas de ejemplo
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, image_path) VALUES 

('Arroz con Pollo Tradicional', 
'Plato clásico de la cocina latina con arroz, pollo tierno y verduras frescas. Perfecto para reuniones familiares.',
'1. Sazonar el pollo con sal, pimienta y comino. Reservar. 2. En una olla grande, calentar aceite y dorar el pollo por todos lados hasta que esté bien cocido. Retirar y reservar. 3. En la misma olla, sofreír cebolla, ajo y pimiento hasta que estén transparentes. 4. Agregar el tomate picado y cocinar hasta que se ablande. 5. Añadir el arroz y mezclar con los vegetales por 2 minutos. 6. Verter el caldo caliente, añadir sal al gusto. 7. Regresar el pollo a la olla, tapar y cocinar a fuego bajo por 20 minutos. 8. Reposar 5 minutos antes de servir. 9. Decorar con cilantro fresco.',
15, 25, 4, 'medio', 'latina', '/static/images/arroz_con_pollo.jpg'),

('Ensalada César Clásica',
'Ensalada fresca y crujiente con lechuga romana, crutones caseros y aderezo césar cremoso.',
'1. Lavar y secar bien la lechuga romana. Cortarla en trozos grandes. 2. Para el aderezo, mezclar mayonesa, ajo molido, jugo de limón, mostaza, salsa inglesa y queso parmesano rallado. 3. Sazonar con sal y pimienta al gusto. 4. Cortar el pan en cubos y tostar en una sartén con aceite hasta dorar. 5. En un bowl grande, mezclar la lechuga con el aderezo. 6. Servir en platos individuales, agregar crutones y más queso parmesano. 7. Decorar con pimienta negra recién molida.',
10, 5, 2, 'fácil', 'italiana', '/static/images/ensalada_cesar.jpg'),

('Sopa de Lentejas Nutritiva',
'Sopa reconfortante y nutritiva, rica en proteínas vegetales y fibra. Ideal para días fríos.',
'1. Remojar las lentejas en agua fría por 2 horas. Escurrir y enjuagar. 2. En una olla grande, calentar aceite y sofreír cebolla, ajo, zanahoria y apio picados finamente. 3. Cocinar hasta que las verduras estén suaves, aproximadamente 8 minutos. 4. Agregar las lentejas escurridas y el caldo de verduras. 5. Sazonar con sal, pimienta, comino y una hoja de laurel. 6. Llevar a ebullición, luego reducir fuego y cocinar a fuego lento por 30-35 minutos. 7. Rectificar sazón y servir caliente. 8. Opcional: licuar la mitad de la sopa para una textura más cremosa.',
10, 35, 4, 'fácil', 'mediterránea', '/static/images/sopa_lentejas.jpg'),

('Tacos de Pollo con Salsa Verde',
'Tacos tradicionales mexicanos con pollo marinado y salsa verde casera de tomatillo.',
'1. Marinar el pollo en jugo de lima, ajo, comino, chile en polvo, sal y pimienta por 30 minutos. 2. Para la salsa verde, asar tomatillos y chiles serranos en una sartén hasta que estén ligeramente quemados. 3. Licuar los tomatillos con chiles, cebolla, ajo, cilantro y sal al gusto. 4. Cocinar el pollo marinado en una sartén caliente hasta que esté bien cocido y ligeramente dorado. 5. Desmenuzar el pollo y reservar. 6. Calentar las tortillas en una plancha o sartén. 7. Servir el pollo en las tortillas calientes con salsa verde, cebolla picada y cilantro fresco.',
20, 15, 4, 'medio', 'mexicana', '/static/images/tacos_pollo.jpg'),

('Pasta Primavera Vegetariana',
'Pasta fresca con una mezcla colorida de verduras de temporada en salsa ligera de aceite de oliva.',
'1. Cocinar la pasta según las instrucciones del paquete hasta que esté al dente. Reservar 1 taza del agua de cocción. 2. Mientras tanto, cortar todas las verduras en trozos uniformes. 3. En una sartén grande, calentar aceite de oliva y saltear ajo hasta que esté fragante. 4. Agregar brócoli y zanahoria, cocinar 3 minutos. 5. Añadir calabaza, pimiento y ejotes, cocinar otros 4 minutos. 6. Incorporar la pasta escurrida a las verduras. 7. Agregar un poco del agua de cocción si es necesario para mantener húmedo. 8. Sazonar con sal, pimienta y hierbas frescas. 9. Servir inmediatamente con queso parmesano rallado.',
15, 15, 4, 'fácil', 'italiana', '/static/images/pasta_primavera.jpg'),

('Salmón Teriyaki con Arroz',
'Filetes de salmón glaseados con salsa teriyaki casera, servidos sobre arroz japonés.',
'1. Para la salsa teriyaki, mezclar salsa de soja, miel, vinagre de arroz, ajo molido y jengibre rallado en una sartén pequeña. 2. Cocinar a fuego medio hasta que espese ligeramente, aproximadamente 5 minutos. 3. Sazonar los filetes de salmón con sal y pimienta. 4. En una sartén antiadherente, cocinar el salmón con la piel hacia abajo por 4 minutos. 5. Voltear y cocinar 3 minutos más. 6. Pincelar con la salsa teriyaki durante los últimos 2 minutos. 7. Servir sobre arroz cocido y decorar con semillas de sésamo y cebolla verde picada.',
10, 12, 4, 'medio', 'asiática', '/static/images/salmon_teriyaki.jpg'),

('Chili Vegetariano Picante',
'Guiso espeso y picante con frijoles mixtos, verduras y especias. Rico en proteínas vegetales.',
'1. En una olla grande, calentar aceite y sofreír cebolla, ajo, pimiento y apio hasta que estén suaves. 2. Agregar chile jalapeño picado finamente y cocinar 1 minuto más. 3. Añadir tomate triturado, frijoles escurridos, maíz y caldo de verduras. 4. Sazonar con comino, chile en polvo, paprika, orégano, sal y pimienta. 5. Llevar a ebullición, luego reducir fuego y cocinar a fuego lento por 45 minutos, revolviendo ocasionalmente. 6. Rectificar sazón y agregar más especias si se desea más picante. 7. Servir caliente con cilantro fresco, aguacate en cubos y crema agria.',
15, 50, 6, 'fácil', 'americana', '/static/images/chili_vegetariano.jpg'),

('Risotto de Champiñones',
'Risotto cremoso italiano con champiñones mixtos y queso parmesano. Elegante y reconfortante.',
'1. Calentar el caldo de verduras en una olla y mantener caliente. 2. En una sartén, saltear los champiñones con un poco de aceite hasta que estén dorados. Reservar. 3. En una olla pesada, calentar aceite de oliva y sofreír cebolla finamente picada hasta que esté transparente. 4. Agregar el arroz arborio y tostar por 2 minutos, revolviendo constantemente. 5. Añadir vino blanco y cocinar hasta que se evapore. 6. Agregar caldo caliente de a poco, revolviendo constantemente hasta que el arroz esté cremoso, aproximadamente 18-20 minutos. 7. Incorporar los champiñones, mantequilla y queso parmesano. 8. Sazonar con sal, pimienta y perejil fresco.',
10, 25, 4, 'difícil', 'italiana', '/static/images/risotto_champinones.jpg'),

('Bowl Buddha Nutritivo',
'Bowl completo y balanceado con quinoa, verduras asadas, aguacate y aderezo tahini.',
'1. Precalentar horno a 200°C. 2. Cortar camote, brócoli y remolacha en trozos uniformes. 3. Rociar con aceite de oliva, sal y pimienta. Asar por 25-30 minutos. 4. Cocinar quinoa según instrucciones del paquete. 5. Para el aderezo, mezclar tahini, jugo de limón, ajo molido, agua y sal hasta obtener consistencia cremosa. 6. En bowls individuales, colocar quinoa como base. 7. Disponer verduras asadas, espinaca fresca y aguacate en rebanadas. 8. Rociar con aderezo de tahini y decorar con semillas de girasol y cilantro.',
20, 30, 4, 'fácil', 'saludable', '/static/images/bowl_buddha.jpg'),

('Pollo al Curry Thai',
'Curry tailandés aromático con pollo tierno, leche de coco y verduras frescas.',
'1. Cortar el pollo en trozos medianos y sazonar con sal. 2. En una sartén grande o wok, calentar aceite y dorar el pollo por todos lados. Retirar y reservar. 3. En la misma sartén, sofreír cebolla, ajo y jengibre hasta que estén fragantes. 4. Agregar pasta de curry rojo y cocinar 1 minuto. 5. Verter leche de coco y llevar a ebullición suave. 6. Regresar el pollo a la sartén junto con pimiento, calabaza y ejotes. 7. Cocinar por 15-20 minutos hasta que las verduras estén tiernas. 8. Rectificar sazón con sal, azúcar y jugo de lima. 9. Servir sobre arroz jasmine con cilantro fresco y lima.',
15, 25, 4, 'medio', 'asiática', '/static/images/curry_thai.jpg');

-- Relaciones entre recetas e ingredientes (recipe_ingredients)
-- Arroz con Pollo (ID: 1)
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
(1, (SELECT id FROM ingredient WHERE name = 'pollo'), '800', 'g'),
(1, (SELECT id FROM ingredient WHERE name = 'arroz blanco'), '2', 'tazas'),
(1, (SELECT id FROM ingredient WHERE name = 'cebolla'), '1', 'pieza'),
(1, (SELECT id FROM ingredient WHERE name = 'ajo'), '3', 'dientes'),
(1, (SELECT id FROM ingredient WHERE name = 'pimiento rojo'), '1', 'pieza'),
(1, (SELECT id FROM ingredient WHERE name = 'tomate'), '2', 'piezas'),
(1, (SELECT id FROM ingredient WHERE name = 'aceite de oliva'), '3', 'cdas'),
(1, (SELECT id FROM ingredient WHERE name = 'sal'), '1', 'cdita'),
(1, (SELECT id FROM ingredient WHERE name = 'comino'), '1', 'cdita'),
(1, (SELECT id FROM ingredient WHERE name = 'cilantro'), '1/4', 'taza');

-- Ensalada César (ID: 2)
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
(2, (SELECT id FROM ingredient WHERE name = 'lechuga'), '2', 'cabezas'),
(2, (SELECT id FROM ingredient WHERE name = 'pan blanco'), '4', 'rebanadas'),
(2, (SELECT id FROM ingredient WHERE name = 'ajo'), '2', 'dientes'),
(2, (SELECT id FROM ingredient WHERE name = 'limón'), '1', 'pieza'),
(2, (SELECT id FROM ingredient WHERE name = 'aceite de oliva'), '4', 'cdas'),
(2, (SELECT id FROM ingredient WHERE name = 'queso cheddar'), '1/2', 'taza'),
(2, (SELECT id FROM ingredient WHERE name = 'sal'), '1/2', 'cdita'),
(2, (SELECT id FROM ingredient WHERE name = 'pimienta negra'), '1/4', 'cdita');

-- Sopa de Lentejas (ID: 3)
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
(3, (SELECT id FROM ingredient WHERE name = 'lenteja'), '1', 'taza'),
(3, (SELECT id FROM ingredient WHERE name = 'cebolla'), '1', 'pieza'),
(3, (SELECT id FROM ingredient WHERE name = 'ajo'), '3', 'dientes'),
(3, (SELECT id FROM ingredient WHERE name = 'zanahoria'), '2', 'piezas'),
(3, (SELECT id FROM ingredient WHERE name = 'apio'), '2', 'tallos'),
(3, (SELECT id FROM ingredient WHERE name = 'aceite de oliva'), '2', 'cdas'),
(3, (SELECT id FROM ingredient WHERE name = 'sal'), '1', 'cdita'),
(3, (SELECT id FROM ingredient WHERE name = 'comino'), '1/2', 'cdita'),
(3, (SELECT id FROM ingredient WHERE name = 'pimienta negra'), '1/2', 'cdita');

-- Tacos de Pollo (ID: 4)
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
(4, (SELECT id FROM ingredient WHERE name = 'pollo'), '600', 'g'),
(4, (SELECT id FROM ingredient WHERE name = 'tortilla de maíz'), '8', 'piezas'),
(4, (SELECT id FROM ingredient WHERE name = 'lima'), '2', 'piezas'),
(4, (SELECT id FROM ingredient WHERE name = 'cebolla'), '1/2', 'pieza'),
(4, (SELECT id FROM ingredient WHERE name = 'ajo'), '2', 'dientes'),
(4, (SELECT id FROM ingredient WHERE name = 'chile en polvo'), '1', 'cdita'),
(4, (SELECT id FROM ingredient WHERE name = 'comino'), '1', 'cdita'),
(4, (SELECT id FROM ingredient WHERE name = 'cilantro'), '1/2', 'taza'),
(4, (SELECT id FROM ingredient WHERE name = 'sal'), '1', 'cdita');

-- Pasta Primavera (ID: 5)
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
(5, (SELECT id FROM ingredient WHERE name = 'pasta'), '400', 'g'),
(5, (SELECT id FROM ingredient WHERE name = 'brócoli'), '1', 'taza'),
(5, (SELECT id FROM ingredient WHERE name = 'zanahoria'), '1', 'pieza'),
(5, (SELECT id FROM ingredient WHERE name = 'calabaza'), '1', 'taza'),
(5, (SELECT id FROM ingredient WHERE name = 'pimiento verde'), '1', 'pieza'),
(5, (SELECT id FROM ingredient WHERE name = 'ejotes'), '1', 'taza'),
(5, (SELECT id FROM ingredient WHERE name = 'ajo'), '3', 'dientes'),
(5, (SELECT id FROM ingredient WHERE name = 'aceite de oliva'), '3', 'cdas'),
(5, (SELECT id FROM ingredient WHERE name = 'sal'), '1', 'cdita'),
(5, (SELECT id FROM ingredient WHERE name = 'albahaca'), '2', 'cdas');

-- Salmón Teriyaki (ID: 6)
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
(6, (SELECT id FROM ingredient WHERE name = 'salmón'), '4', 'filetes'),
(6, (SELECT id FROM ingredient WHERE name = 'arroz blanco'), '1.5', 'tazas'),
(6, (SELECT id FROM ingredient WHERE name = 'ajo'), '2', 'dientes'),
(6, (SELECT id FROM ingredient WHERE name = 'aceite vegetal'), '2', 'cdas'),
(6, (SELECT id FROM ingredient WHERE name = 'sal'), '1/2', 'cdita'),
(6, (SELECT id FROM ingredient WHERE name = 'pimienta negra'), '1/4', 'cdita');

-- Chili Vegetariano (ID: 7)
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
(7, (SELECT id FROM ingredient WHERE name = 'frijol negro'), '1', 'taza'),
(7, (SELECT id FROM ingredient WHERE name = 'frijol pinto'), '1', 'taza'),
(7, (SELECT id FROM ingredient WHERE name = 'cebolla'), '1', 'pieza'),
(7, (SELECT id FROM ingredient WHERE name = 'ajo'), '3', 'dientes'),
(7, (SELECT id FROM ingredient WHERE name = 'pimiento rojo'), '1', 'pieza'),
(7, (SELECT id FROM ingredient WHERE name = 'apio'), '2', 'tallos'),
(7, (SELECT id FROM ingredient WHERE name = 'chile jalapeño'), '1', 'pieza'),
(7, (SELECT id FROM ingredient WHERE name = 'tomate'), '2', 'latas'),
(7, (SELECT id FROM ingredient WHERE name = 'maíz'), '1', 'taza'),
(7, (SELECT id FROM ingredient WHERE name = 'comino'), '2', 'cditas'),
(7, (SELECT id FROM ingredient WHERE name = 'chile en polvo'), '2', 'cditas'),
(7, (SELECT id FROM ingredient WHERE name = 'paprika'), '1', 'cdita');

-- Risotto de Champiñones (ID: 8)
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
(8, (SELECT id FROM ingredient WHERE name = 'arroz blanco'), '1.5', 'tazas'),
(8, (SELECT id FROM ingredient WHERE name = 'champiñón'), '300', 'g'),
(8, (SELECT id FROM ingredient WHERE name = 'cebolla'), '1', 'pieza'),
(8, (SELECT id FROM ingredient WHERE name = 'ajo'), '2', 'dientes'),
(8, (SELECT id FROM ingredient WHERE name = 'aceite de oliva'), '3', 'cdas'),
(8, (SELECT id FROM ingredient WHERE name = 'mantequilla'), '2', 'cdas'),
(8, (SELECT id FROM ingredient WHERE name = 'queso cheddar'), '1/2', 'taza'),
(8, (SELECT id FROM ingredient WHERE name = 'perejil'), '2', 'cdas');

-- Bowl Buddha (ID: 9)
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
(9, (SELECT id FROM ingredient WHERE name = 'quinoa'), '1', 'taza'),
(9, (SELECT id FROM ingredient WHERE name = 'camote'), '2', 'piezas'),
(9, (SELECT id FROM ingredient WHERE name = 'brócoli'), '1', 'taza'),
(9, (SELECT id FROM ingredient WHERE name = 'remolacha'), '2', 'piezas'),
(9, (SELECT id FROM ingredient WHERE name = 'espinaca'), '2', 'tazas'),
(9, (SELECT id FROM ingredient WHERE name = 'aguacate'), '1', 'pieza'),
(9, (SELECT id FROM ingredient WHERE name = 'aceite de oliva'), '3', 'cdas'),
(9, (SELECT id FROM ingredient WHERE name = 'limón'), '1', 'pieza'),
(9, (SELECT id FROM ingredient WHERE name = 'ajo'), '1', 'diente');

-- Pollo al Curry Thai (ID: 10)
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
(10, (SELECT id FROM ingredient WHERE name = 'pollo'), '700', 'g'),
(10, (SELECT id FROM ingredient WHERE name = 'cebolla'), '1', 'pieza'),
(10, (SELECT id FROM ingredient WHERE name = 'ajo'), '3', 'dientes'),
(10, (SELECT id FROM ingredient WHERE name = 'pimiento rojo'), '1', 'pieza'),
(10, (SELECT id FROM ingredient WHERE name = 'calabaza'), '1', 'taza'),
(10, (SELECT id FROM ingredient WHERE name = 'ejotes'), '1', 'taza'),
(10, (SELECT id FROM ingredient WHERE name = 'aceite de coco'), '2', 'cdas'),
(10, (SELECT id FROM ingredient WHERE name = 'cilantro'), '1/4', 'taza'),
(10, (SELECT id FROM ingredient WHERE name = 'lima'), '1', 'pieza'),
(10, (SELECT id FROM ingredient WHERE name = 'arroz blanco'), '1.5', 'tazas');

-- Usuario administrador de ejemplo
INSERT INTO "user" (username, email, password_hash) VALUES 
('admin', 'admin@sistema-culinario.com', 'pbkdf2:sha256:260000$8xQZJq8K9P2L$c8f8c7d8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6');

-- Usuario de prueba
INSERT INTO "user" (username, email, password_hash) VALUES 
('usuario_test', 'test@email.com', 'pbkdf2:sha256:260000$8xQZJq8K9P2L$c8f8c7d8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6');

-- Calificaciones de ejemplo
INSERT INTO recipe_rating (user_id, recipe_id, rating, comment, created_at) VALUES
(1, 1, 5, 'Excelente receta, muy sabrosa y fácil de seguir. La familia la amó.', NOW()),
(2, 1, 4, 'Muy buena, aunque le agregué más especias a mi gusto.', NOW()),
(1, 2, 4, 'Ensalada fresca y deliciosa. Perfect para el almuerzo.', NOW()),
(2, 2, 5, 'La mejor ensalada césar que he probado. El aderezo es perfecto.', NOW()),
(1, 3, 5, 'Sopa muy nutritiva y reconfortante. Ideal para días fríos.', NOW()),
(1, 4, 4, 'Tacos auténticos y deliciosos. La salsa verde está increíble.', NOW()),
(2, 5, 4, 'Pasta llena de verduras frescas. Muy colorida y saludable.', NOW()),
(1, 6, 5, 'El salmón quedó perfecto y la salsa teriyaki casera es deliciosa.', NOW()),
(2, 7, 5, 'Chili vegetariano muy sabroso y lleno de proteínas.', NOW()),
(1, 8, 3, 'Risotto cremoso pero requiere paciencia y técnica.', NOW()),
(2, 9, 5, 'Bowl muy completo y nutritivo. Perfecto para una comida balanceada.', NOW()),
(1, 10, 4, 'Curry tailandés auténtico con buen balance de sabores.', NOW());

-- Preferencias de usuario de ejemplo
INSERT INTO user_preference (user_id, preferred_cuisines, disliked_ingredients, max_prep_time, difficulty_preference) VALUES
(1, '["italiana", "mediterránea", "asiática"]', '["chile jalapeño"]', 45, 'medio'),
(2, '["mexicana", "latina", "americana"]', '["pescado", "mariscos"]', 30, 'fácil');

-- Asociar restricciones dietéticas con usuarios
INSERT INTO user_restrictions (user_id, restriction_id) VALUES
(2, (SELECT id FROM dietary_restriction WHERE name = 'sin gluten')),
(2, (SELECT id FROM dietary_restriction WHERE name = 'bajo sodio'));

-- Ingredientes disponibles para usuario de prueba
INSERT INTO user_ingredient (user_id, ingredient_id, quantity, expiry_date, added_at) VALUES
(1, (SELECT id FROM ingredient WHERE name = 'pollo'), '1 kg', DATE_ADD(NOW(), INTERVAL 3 DAY), NOW()),
(1, (SELECT id FROM ingredient WHERE name = 'arroz blanco'), '500g', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW()),
(1, (SELECT id FROM ingredient WHERE name = 'cebolla'), '3 piezas', DATE_ADD(NOW(), INTERVAL 7 DAY), NOW()),
(1, (SELECT id FROM ingredient WHERE name = 'ajo'), '1 cabeza', DATE_ADD(NOW(), INTERVAL 14 DAY), NOW()),
(1, (SELECT id FROM ingredient WHERE name = 'tomate'), '4 piezas', DATE_ADD(NOW(), INTERVAL 5 DAY), NOW()),
(1, (SELECT id FROM ingredient WHERE name = 'aceite de oliva'), '500ml', DATE_ADD(NOW(), INTERVAL 90 DAY), NOW()),
(2, (SELECT id FROM ingredient WHERE name = 'pasta'), '500g', DATE_ADD(NOW(), INTERVAL 60 DAY), NOW()),
(2, (SELECT id FROM ingredient WHERE name = 'brócoli'), '1 pieza', DATE_ADD(NOW(), INTERVAL 3 DAY), NOW()),
(2, (SELECT id FROM ingredient WHERE name = 'zanahoria'), '2 piezas', DATE_ADD(NOW(), INTERVAL 7 DAY), NOW()),
(2, (SELECT id FROM ingredient WHERE name = 'queso mozzarella'), '200g', DATE_ADD(NOW(), INTERVAL 10 DAY), NOW());

-- Sustituciones de ingredientes comunes
INSERT INTO ingredient_substitution (recipe_id, original_ingredient_id, substitute_ingredient_id, conversion_ratio, notes) VALUES
-- Para Arroz con Pollo
(1, (SELECT id FROM ingredient WHERE name = 'arroz blanco'), (SELECT id FROM ingredient WHERE name = 'arroz integral'), '1:1', 'Opción más saludable, requiere más tiempo de cocción'),
(1, (SELECT id FROM ingredient WHERE name = 'pollo'), (SELECT id FROM ingredient WHERE name = 'tofu'), '1:1', 'Alternativa vegetariana'),

-- Para Ensalada César
(2, (SELECT id FROM ingredient WHERE name = 'pan blanco'), (SELECT id FROM ingredient WHERE name = 'pan integral'), '1:1', 'Opción más nutritiva'),
(2, (SELECT id FROM ingredient WHERE name = 'queso cheddar'), (SELECT id FROM ingredient WHERE name = 'queso mozzarella'), '1:1', 'Sabor más suave'),

-- Para Sopa de Lentejas
(3, (SELECT id FROM ingredient WHERE name = 'lenteja'), (SELECT id FROM ingredient WHERE name = 'garbanzo'), '1:1', 'Textura diferente pero igual de nutritivo'),

-- Para Pasta Primavera
(5, (SELECT id FROM ingredient WHERE name = 'pasta'), (SELECT id FROM ingredient WHERE name = 'quinoa'), '1:1', 'Opción sin gluten'),
(5, (SELECT id FROM ingredient WHERE name = 'queso cheddar'), (SELECT id FROM ingredient WHERE name = 'levadura nutricional'), '1:4', 'Opción vegana'),

-- Para Salmón Teriyaki
(6, (SELECT id FROM ingredient WHERE name = 'salmón'), (SELECT id FROM ingredient WHERE name = 'atún'), '1:1', 'Pescado alternativo'),
(6, (SELECT id FROM ingredient WHERE name = 'arroz blanco'), (SELECT id FROM ingredient WHERE name = 'quinoa'), '1:1', 'Opción más proteica');

-- Más ingredientes útiles
INSERT INTO ingredient (name, category, calories_per_100g, common_allergen) VALUES 
('vinagre de manzana', 'condiments', 22, false),
('miel', 'sweeteners', 304, false),
('azúcar morena', 'sweeteners', 380, false),
('stevia', 'sweeteners', 0, false),
('leche de almendra', 'dairy_alternatives', 17, true),
('leche de coco', 'dairy_alternatives', 230, false),
('tahini', 'condiments', 595, true),
('salsa de soja', 'condiments', 8, true),
('jengibre', 'spices', 80, false),
('cúrcuma', 'spices', 354, false),
('semillas de chía', 'seeds', 486, false),
('semillas de girasol', 'seeds', 584, false),
('avellana', 'nuts', 628, true),
('pistache', 'nuts', 560, true),
('dátil', 'fruits', 277, false),
('coco rallado', 'fruits', 354, false);

-- Comentario final
-- Este archivo contiene datos de ejemplo para inicializar el sistema
-- Para usar en producción, ejecutar: psql -d sistema_culinario -f recipes_data.sql