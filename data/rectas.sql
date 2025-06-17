-- Database: sistema_culinario

-- DROP DATABASE IF EXISTS sistema_culinario;

CREATE DATABASE sistema_culinario
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Mexico.1252'
    LC_CTYPE = 'Spanish_Mexico.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


-- Script de Recetas Bolivianas para Sistema Experto Culinario
-- 30 Recetas tradicionales de Bolivia con ingredientes autóctonos
-- Ejecutar después de crear las tablas base

-- Ingredientes típicos bolivianos (que no están en el archivo original)
INSERT INTO ingredient (name, category, calories_per_100g, common_allergen, seasonal_availability) VALUES 
-- Tubérculos andinos
('papa wayk''a', 'vegetables', 85, false, 'todo_año'),
('papa imilla', 'vegetables', 82, false, 'todo_año'),
('papa runa', 'vegetables', 88, false, 'todo_año'),
('chuño', 'vegetables', 323, false, 'todo_año'),
('tunta', 'vegetables', 315, false, 'todo_año'),
('oca', 'vegetables', 61, false, 'invierno'),
('papalisa', 'vegetables', 67, false, 'invierno'),
('isaño', 'vegetables', 58, false, 'invierno'),

-- Cereales andinos
('quinua real', 'grains', 368, false, 'todo_año'),
('quinua blanca', 'grains', 364, false, 'todo_año'),
('amaranto', 'grains', 371, false, 'todo_año'),
('cañahua', 'grains', 341, false, 'todo_año'),
('tarwi', 'proteins', 440, false, 'invierno'),

-- Carnes típicas
('llama', 'proteins', 165, false, 'todo_año'),
('alpaca', 'proteins', 122, false, 'todo_año'),
('charque', 'proteins', 410, false, 'todo_año'),
('chorizo chuquisaqueño', 'proteins', 301, false, 'todo_año'),

-- Vegetales andinos
('locoto', 'vegetables', 31, false, 'verano'),
('ulluco', 'vegetables', 65, false, 'invierno'),
('choclo', 'vegetables', 96, false, 'verano'),
('habas', 'proteins', 341, false, 'verano'),
('arveja', 'proteins', 81, false, 'verano'),

-- Condimentos y especias bolivianas
('ají amarillo', 'spices', 40, false, 'verano'),
('ají colorado', 'spices', 282, false, 'todo_año'),
('wakataya', 'spices', 15, false, 'todo_año'),
('muña', 'spices', 25, false, 'todo_año'),
('k''oa', 'spices', 12, false, 'todo_año'),
('hierba buena', 'spices', 70, false, 'todo_año'),

-- Lácteos locales
('queso fresco boliviano', 'dairy', 264, true, 'todo_año'),
('requesón', 'dairy', 98, true, 'todo_año'),

-- Otros ingredientes
('maní', 'nuts', 567, true, 'todo_año'),
('chía boliviana', 'seeds', 486, false, 'todo_año'),
('mote de maíz', 'grains', 96, false, 'todo_año'),
('chicha de maíz', 'beverages', 54, false, 'todo_año'),
('singani', 'beverages', 231, false, 'todo_año'),
('api morado', 'grains', 87, false, 'invierno'),
('tostado de maíz', 'grains', 365, false, 'todo_año'),
('yuca', 'vegetables', 160, false, 'todo_año'),
('plátano verde', 'fruits', 89, false, 'todo_año'),
('plátano maduro', 'fruits', 122, false, 'todo_año'),
('palmito', 'vegetables', 115, false, 'todo_año'),
('surubí', 'proteins', 105, false, 'todo_año'),
('pacu', 'proteins', 108, false, 'todo_año'),
('tucumana', 'vegetables', 158, false, 'verano');

-- 30 RECETAS BOLIVIANAS TRADICIONALES

-- 1. Salteña Paceña
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Salteña Paceña Tradicional', 
'Empanada jugosa típica de La Paz, rellena de carne, papa, arveja y caldo gelatinoso. El desayuno más querido de Bolivia.',
'1. Para el relleno: cocinar carne de res cortada en cubitos pequeños con cebolla, ajo, ají colorado y comino hasta dorar. 2. Agregar papas en cubitos, arvejas, huevo duro picado, aceitunas y pasas. 3. Preparar gelatina con caldo de carne y gelatina sin sabor, agregar al relleno frío. 4. Para la masa: mezclar harina, manteca, azúcar, sal y achiote hasta formar masa lisa. 5. Estirar, rellenar con abundante relleno jugoso. 6. Cerrar con repulgue característico en forma de trenza. 7. Pintar con huevo batido. 8. Hornear a 180°C por 25-30 minutos hasta dorar.',
60, 30, 12, 'difícil', 'boliviana', 'Tradición Paceña');

-- 2. Sopa de Maní
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Sopa de Maní Boliviana', 
'Sopa cremosa a base de maní molido, con carne de res, papa y verduras. Plato tradicional muy nutritivo.',
'1. Tostar maní en sartén hasta dorar, dejar enfriar y moler finamente. 2. Cocinar carne de res en trozos con agua, sal y cebolla hasta tiernizar. 3. Agregar papa en cubos, zanahoria y arveja al caldo. 4. Diluir maní molido con caldo caliente, colar para evitar grumos. 5. Incorporar la mezcla de maní al caldo, cocinar 15 minutos revolviendo. 6. Sazonar con sal, pimienta y ají colorado. 7. Agregar fideos finos y cocinar 8 minutos más. 8. Servir caliente con perejil picado y chuño phuthi.',
20, 45, 6, 'medio', 'boliviana', 'Receta Cochabambina');

-- 3. Fricasé de Cerdo
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Fricasé de Cerdo Paceño', 
'Guiso tradicional paceño con carne de cerdo, chuño, maíz y ají amarillo. Plato festivo de gran tradición.',
'1. Cocinar carne de cerdo en trozos grandes con agua y sal hasta tiernizar. 2. En sartén aparte, freír cebolla, ajo y ají amarillo molido. 3. Agregar la carne cocida al sofrito y dorar bien. 4. Incorporar chuño remojado y escurrido, mote de maíz. 5. Añadir caldo de la cocción, sal, pimienta y comino. 6. Cocinar a fuego lento 30 minutos hasta que espese. 7. Rectificar sazón y agregar hierba buena picada. 8. Servir con papa cocida y llajwa.',
25, 90, 8, 'medio', 'boliviana', 'Tradición Paceña');

-- 4. Pique Macho
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Pique Macho Cochabambino', 
'Plato abundante con carne de res, salchichas, papas fritas, huevo, tomate y locoto. Ideal para compartir.',
'1. Cortar carne de res en tiras y sazonar con sal, pimienta y comino. 2. Freír papas en bastones hasta dorar, reservar. 3. Saltear la carne a fuego alto hasta dorar, reservar. 4. Freír salchichas en rodajas hasta dorar. 5. Freír huevos y cortar en tiras. 6. En la misma sartén, saltear cebolla y tomate en cubos. 7. Mezclar todos los ingredientes: carne, papas, salchichas, huevo. 8. Sazonar con sal, locoto picado y mayonesa. 9. Servir inmediatamente bien caliente.',
20, 25, 4, 'fácil', 'boliviana', 'Tradición Cochabambina');

-- 5. Chairo Paceño
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Chairo Paceño Tradicional', 
'Sopa espesa con chuño, papa, carne, verduras y quinua. Plato emblemático del altiplano boliviano.',
'1. Remojar chuño en agua tibia, pelar y cortar en trozos. 2. Cocinar carne de cordero o res con agua, sal y cebolla. 3. Agregar papa, oca, zanahoria y habas al caldo. 4. Incorporar chuño, quinua y trigo remojado. 5. Sazonar con ají colorado, sal, pimienta y wakataya. 6. Cocinar a fuego lento 45 minutos hasta espesar. 7. Agregar verduras frescas: apio, perejil, hierba buena. 8. Servir caliente con queso fresco desmenuzado.',
30, 60, 8, 'medio', 'boliviana', 'Receta Altiplánica');

-- 6. Silpancho Cochabambino
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Silpancho Cochabambino', 
'Carne apanada muy fina servida sobre arroz, papa, ensalada y huevo frito. Plato típico del valle.',
'1. Aplanar carne de res hasta dejar muy fina, sazonar con sal y pimienta. 2. Pasar por harina, huevo batido y pan molido. 3. Freír en aceite caliente hasta dorar ambos lados. 4. Cocinar arroz blanco suelto. 5. Hervir papas y cortar en rodajas. 6. Preparar ensalada con tomate, cebolla, locoto y vinagre. 7. Freír huevos manteniendo la yema líquida. 8. Servir armando el plato: arroz, papa, carne, ensalada y huevo encima.',
25, 20, 4, 'medio', 'boliviana', 'Valle Central');

-- 7. Majadito Batido
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Majadito Batido Cruceño', 
'Arroz con charque desmenuzado, plátano maduro y huevo. Desayuno tradicional de Santa Cruz.',
'1. Remojar charque en agua caliente, desmenuzar finamente quitando sal. 2. Sofreír cebolla, ajo y ají colorado en aceite. 3. Agregar charque desmenuzado y saltear. 4. Incorporar arroz cocido y mezclar bien. 5. Batir huevos y agregar al arroz, revolver constantemente. 6. Freír plátano maduro en rodajas hasta caramelizar. 7. Servir el majadito con plátano frito y yuca hervida. 8. Acompañar con café con leche.',
15, 20, 4, 'fácil', 'boliviana', 'Tradición Cruceña');

-- 8. Queso Humacha
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Queso Humacha Potosino', 
'Sopa de queso fresco con papa, choclo, habas y hierbas aromáticas. Especialidad de Potosí.',
'1. Picar queso fresco en cubos medianos. 2. Cocinar papas enteras con cáscara hasta tiernizar. 3. En olla aparte, hervir choclo desgranado y habas. 4. Preparar sofrito con cebolla, ajo y ají amarillo. 5. Agregar agua o caldo, llevar a ebullición. 6. Incorporar papas peladas en trozos, choclo y habas. 7. Añadir queso y cocinar hasta que se derrita parcialmente. 8. Sazonar con muña, sal y pimienta. Servir con pan.',
20, 35, 6, 'fácil', 'boliviana', 'Villa Imperial');

-- 9. Llajwa Cochabambina
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Llajwa Cochabambina Original', 
'Salsa picante boliviana con locoto, tomate y quirquiña. Acompañante indispensable de la comida boliviana.',
'1. Asar locoto y tomate en comal hasta que se ablanden y tuesten. 2. Pelar el tomate asado. 3. En batán de piedra, moler locoto asado con sal gruesa. 4. Agregar tomate asado y continuar moliendo. 5. Incorporar quirquiña o hierba buena picada finamente. 6. Moler hasta obtener consistencia rústica, no muy lisa. 7. Rectificar sal y picante al gusto. 8. Servir fresca como acompañamiento.',
15, 10, 8, 'fácil', 'boliviana', 'Valle Central');

-- 10. Tukumana Salteña
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Tukumana Salteña', 
'Tamal salteño envuelto en chala de choclo, relleno de carne, papa, arveja y ají colorado.',
'1. Preparar masa con harina de maíz, manteca, sal y caldo caliente. 2. Cocinar carne de cerdo en cubitos con cebolla y ají colorado. 3. Agregar papa en cubos, arvejas y comino al relleno. 4. Limpiar y lavar chalas de choclo. 5. Extender masa en chala, colocar relleno al centro. 6. Envolver formando paquete, atar con tira de chala. 7. Cocinar al vapor en olla con rejilla por 45 minutos. 8. Servir caliente con llajwa y té.',
45, 45, 10, 'difícil', 'boliviana', 'Tradición Salteña');

-- 11. Ranga de Pollo
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Ranga de Pollo Paceña', 
'Pollo guisado con papa, zanahoria y arvejas en salsa espesa. Comida casera tradicional.',
'1. Trozar pollo en presas, sazonar con sal, pimienta y comino. 2. Dorar presas de pollo en aceite caliente. 3. Sofreír cebolla, ajo y ají colorado molido. 4. Agregar pollo dorado al sofrito. 5. Incorporar agua o caldo, papa en trozos grandes. 6. Añadir zanahoria, arvejas y sazonar. 7. Cocinar tapado 30 minutos hasta que pollo esté tierno. 8. Servir con arroz blanco y ensalada.',
20, 40, 6, 'fácil', 'boliviana', 'Tradición Paceña');

-- 12. Mondongo Chuquisaqueño
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Mondongo Chuquisaqueño', 
'Sopa de mondongo con mote, papa, arveja y verduras. Plato nutritivo de la capital constitucional.',
'1. Limpiar y hervir mondongo con sal hasta tiernizar (2-3 horas). 2. Cortar mondongo cocido en tiras. 3. Preparar sofrito con cebolla, ajo y ají colorado. 4. Agregar mondongo cortado al sofrito y dorar. 5. Incorporar caldo, mote de maíz remojado, papa. 6. Añadir arveja, zanahoria y hierbas aromáticas. 7. Cocinar 30 minutos hasta que verduras estén tiernas. 8. Servir caliente con perejil y pan.',
30, 180, 8, 'difícil', 'boliviana', 'Ciudad Blanca');

-- 13. Locro de Gallina
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Locro de Gallina Cochabambino', 
'Guiso espeso de gallina con choclo, zapallo, habas y papa. Comida sustanciosa del valle.',
'1. Cocinar gallina en presas con agua, sal y cebolla hasta tiernizar. 2. Desmenuzar la carne y reservar caldo. 3. Sofreír cebolla, ajo y ají amarillo molido. 4. Agregar choclo desgranado, zapallo en cubos. 5. Incorporar papa, habas y caldo de gallina. 6. Añadir carne desmenuzada y cocinar 25 minutos. 7. Espesar con papa machacada si es necesario. 8. Servir con perejil picado y pan.',
25, 75, 6, 'medio', 'boliviana', 'Valle Central');

-- 14. Pacumutu Oriental
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Pacumutu Oriental', 
'Pescado pacu relleno con yuca, plátano y especias, cocido al vapor en hoja de plátano.',
'1. Limpiar pacu entero, hacer cortes profundos sin traspasar. 2. Hervir yuca y plátano verde, hacer puré. 3. Mezclar puré con cebolla, ajo, ají, sal y hierbas. 4. Rellenar pescado con la mezcla de yuca. 5. Envolver en hojas de plátano limpias. 6. Atar con pita o alambre delgado. 7. Cocinar al vapor sobre rejilla 45 minutos. 8. Servir con arroz, ensalada y palmito.',
30, 45, 4, 'medio', 'boliviana', 'Oriente Boliviano');

-- 15. Sopa de Quinua
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Sopa de Quinua Real', 
'Sopa nutritiva con quinua real, verduras andinas y carne. Rica en proteínas y minerales.',
'1. Lavar quinua hasta que agua salga transparente. 2. Cocinar carne de llama o res con agua y sal. 3. Agregar papa, oca, papalisa al caldo hirviendo. 4. Incorporar quinua lavada y cocinar 20 minutos. 5. Añadir zanahoria, apio, cebolla picada. 6. Sazonar con sal, pimienta, k''oa y wakataya. 7. Cocinar hasta que quinua esté transparente. 8. Servir con queso fresco y pan integral.',
15, 40, 6, 'fácil', 'boliviana', 'Altiplano Sur');

-- 16. Chanka de Pollo
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Chanka de Pollo Potosina', 
'Pollo desmenuzado con papa, arveja, zanahoria y especias. Comida reconfortante de la Villa Imperial.',
'1. Cocinar pollo entero hasta tiernizar completamente. 2. Desmenuzar finamente toda la carne. 3. Sofreír cebolla, ajo y ají colorado en aceite. 4. Agregar pollo desmenuzado y dorar ligeramente. 5. Incorporar papa en cubitos, arveja, zanahoria. 6. Añadir caldo del pollo y sazonar bien. 7. Cocinar hasta que papa esté suave y mezcla espese. 8. Servir caliente con arroz o chuño.',
20, 50, 6, 'fácil', 'boliviana', 'Villa Imperial');

-- 17. Surubí al Horno
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Surubí al Horno Cruceño', 
'Filete de surubí horneado con verduras tropicales y especias amazónicas. Plato del oriente boliviano.',
'1. Sazonar filetes de surubí con sal, pimienta, ajo y limón. 2. Cortar yuca, plátano verde, palmito en bastones. 3. Preparar sofrito con cebolla, ají amarillo, cilantro. 4. En fuente para horno, colocar verduras al fondo. 5. Acomodar pescado sobre verduras. 6. Cubrir con sofrito y agregar caldo de pescado. 7. Hornear a 180°C por 25 minutos. 8. Servir con arroz con coco y ensalada.',
20, 25, 4, 'medio', 'boliviana', 'Oriente Boliviano');

-- 18. Api Morado con Pastel
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Api Morado con Pastel', 
'Bebida caliente de maíz morado con especias, acompañada de pastel frito. Desayuno tradicional de invierno.',
'1. Hervir maíz morado con canela, clavo de olor, cáscara de naranja. 2. Colar y volver a hervir el líquido coloreado. 3. Disolver chuño en agua fría, agregar al api hirviendo. 4. Cocinar revolviendo hasta espesar, endulzar con azúcar. 5. Para el pastel: mezclar harina, polvo de hornear, sal, azúcar. 6. Agregar agua tibia hasta formar masa blanda. 7. Freír porciones de masa en aceite caliente. 8. Servir api caliente con pastel recién frito.',
15, 30, 6, 'fácil', 'boliviana', 'Tradición Altiplánica');

-- 19. Pejerrey de Titicaca
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Pejerrey del Titicaca Frito', 
'Pescado pejerrey del lago Titicaca, simplemente frito y servido con papa y chuño. Especialidad lacustre.',
'1. Limpiar pejerreys enteros, quitar escamas y vísceras. 2. Sazonar con sal, pimienta y limón. 3. Enharinar ligeramente los pescados. 4. Freír en aceite caliente hasta dorar y cocinar completamente. 5. Cocinar papas pequeñas con cáscara. 6. Hervir chuño hasta suavizar. 7. Preparar ensalada de tomate, cebolla, locoto. 8. Servir pescado con papa, chuño y ensalada fresca.',
15, 20, 4, 'fácil', 'boliviana', 'Región Lacustre');

-- 20. Chicharrón de Llama
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Chicharrón de Llama Altiplánico', 
'Carne de llama frita con mote, papa y ensalada. Plato proteico tradicional del altiplano.',
'1. Cortar carne de llama en trozos medianos. 2. Sazonar con sal, pimienta, comino y ajo molido. 3. Cocinar en su propia grasa hasta dorar y cocinar. 4. Remover grasa excesiva, mantener carne dorada. 5. Hervir mote de maíz hasta suavizar. 6. Cocinar papas con cáscara. 7. Preparar ensalada mixta con vinagreta. 8. Servir chicharrón caliente con guarniciones.',
15, 30, 4, 'fácil', 'boliviana', 'Altiplano Boliviano');

-- 21. Thimpu de Cordero
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Thimpu de Cordero Orureño', 
'Guiso de cordero con papa, oca, chuño y quinua. Plato ceremonial del altiplano central.',
'1. Cortar cordero en presas medianas, sazonar. 2. Dorar carne en olla de barro con grasa. 3. Agregar cebolla, ajo, ají colorado molido. 4. Incorporar agua, papa, oca, ulluco. 5. Añadir chuño remojado y quinua. 6. Sazonar con sal, wakataya, muña. 7. Cocinar a fuego lento 60 minutos. 8. Servir en platos de barro con pan.',
25, 75, 6, 'medio', 'boliviana', 'Tradición Orureña');

-- 22. Enrollado de Pollo
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Enrollado de Pollo Tarijeño', 
'Matambre de pollo relleno con verduras, huevo y especias. Especialidad de los valles tarijeños.',
'1. Aplanar pechuga de pollo formando lámina grande. 2. Sazonar con sal, pimienta, ajo, romero. 3. Hervir huevos duros, zanahoria, arveja. 4. Colocar relleno sobre pollo: huevo, verduras, aceitunas. 5. Enrollar firmemente, atar con pita. 6. Dorar enrollado en sartén con aceite. 7. Terminar cocción en horno 30 minutos. 8. Enfriar, cortar en rodajas, servir con ensalada.',
30, 45, 6, 'medio', 'boliviana', 'Valles Tarijeños');

-- 23. Cuñapé Cruceño
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Cuñapé Cruceño Original', 
'Pan de queso tradicional cruceño hecho con almidón de yuca. Acompañamiento clásico del desayuno.',
'1. Mezclar almidón de yuca con sal en bowl grande. 2. Agregar huevos uno por uno batiendo bien. 3. Incorporar leche tibia gradualmente. 4. Añadir queso fresco rallado y mantequilla derretida. 5. Amasar hasta obtener masa homogénea y elástica. 6. Formar bolitas del tamaño de una nuez. 7. Hornear a 180°C por 15-20 minutos hasta dorar. 8. Servir caliente con café con leche.',
20, 20, 15, 'fácil', 'boliviana', 'Tradición Cruceña');

-- 24. Picante de Pollo
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Picante de Pollo Cochabambino', 
'Pollo en salsa picante de ají amarillo con papa y chuño. Plato festivo del valle central.',
'1. Cocinar pollo en presas hasta tiernizar. 2. Preparar ají amarillo: asar, pelar, desvenar. 3. Licuar ají con caldo de pollo, colar. 4. Sofreír cebolla, ajo en aceite de pollo. 5. Agregar salsa de ají colada, cocinar 10 minutos. 6. Incorporar pollo cocido, papa, chuño. 7. Sazonar con sal, pimienta, comino. 8. Cocinar hasta espesar, servir con arroz.',
25, 45, 6, 'medio', 'boliviana', 'Valle Central');

-- 25. Saice Tarijeño
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Saice Tarijeño Tradicional', 
'Carne picada guisada con especias, servida con arroz, papa y huevo frito. Plato típico de Tarija.',
'1. Picar carne de res muy finamente a cuchillo. 2. Sofreír cebolla picada finamente hasta cristalizar. 3. Agregar ajo molido, ají colorado, comino. 4. Incorporar carne picada, cocinar revolviendo. 5. Sazonar con sal, pimienta, orégano. 6. Agregar un poco de caldo, cocinar hasta secar. 7. Servir con arroz, papa hervida y huevo frito. 8. Acompañar con ensalada y llajwa.',
20, 25, 4, 'fácil', 'boliviana', 'Valles Tarijeños');

-- 26. Ají de Fideo
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Ají de Fideo Boliviano', 
'Fideos en salsa picante de ají amarillo con carne y verduras. Plato popular en todo el país.',
'1. Cocinar fideos hasta al dente, escurrir y reservar. 2. Preparar ají amarillo: asar, pelar, licuar con caldo. 3. Sofreír carne en tiras con cebolla y ajo. 4. Agregar salsa de ají colada, cocinar 15 minutos. 5. Incorporar papa en cubos, arveja, zanahoria. 6. Añadir fideos cocidos, mezclar suavemente. 7. Sazonar con sal, pimienta, hierba buena. 8. Servir caliente con queso fresco rallado.',
20, 30, 6, 'medio', 'boliviana', 'Nacional');

-- 27. Keperi de Quinua
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Keperi de Quinua Altiplánico', 
'Quinua cocida con verduras andinas y carne seca. Plato ancestral rico en proteínas.',
'1. Lavar quinua hasta agua transparente, tostar ligeramente. 2. Remojar charque, desalar y desmenuzar. 3. Cocinar quinua con doble cantidad de agua y sal. 4. Sofreír cebolla, ajo, ají colorado molido. 5. Agregar charque desmenuzado, dorar. 6. Incorporar papa, oca, papalisa en cubos. 7. Mezclar con quinua cocida, sazonar. 8. Servir con queso fresco y muña.',
25, 35, 6, 'fácil', 'boliviana', 'Altiplano');

-- 28. Empanada de Queso
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Empanada de Queso Boliviana', 
'Empanada horneada rellena de queso fresco, cebolla y especias. Merienda tradicional.',
'1. Preparar masa: mezclar harina, manteca, sal, azúcar y agua tibia. 2. Amasar hasta lisa, reposar 30 minutos. 3. Para relleno: mezclar queso fresco desmenuzado con cebolla picada. 4. Sazonar con sal, pimienta y orégano. 5. Estirar masa, cortar círculos de 12cm. 6. Rellenar, cerrar con tenedor haciendo repulgue. 7. Pintar con huevo batido. 8. Hornear a 180°C por 20 minutos hasta dorar.',
45, 20, 12, 'fácil', 'boliviana', 'Nacional');

-- 29. Lawak''a de Cordero
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Lawak''a de Cordero Andino', 
'Cordero cocido en olla de barro con papas andinas y hierbas aromáticas. Cocción ancestral a la tierra.',
'1. Cortar cordero en presas medianas, sazonar con sal y especias. 2. En olla de barro, dorar carne con su grasa. 3. Agregar papa wayk''a, oca, isaño enteros. 4. Incorporar agua hasta cubrir, agregar wakataya y muña. 5. Tapar herméticamente, cocinar a fuego lento 90 minutos. 6. No destapar durante la cocción para conservar vapores. 7. Rectificar sazón al final. 8. Servir en la misma olla de barro.',
20, 90, 6, 'medio', 'boliviana', 'Tradición Andina');

-- 30. Helado de Canela
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Helado de Canela Paceño', 
'Helado artesanal de canela con leche y azúcar. Postre tradicional vendido en las calles de La Paz.',
'1. Hervir leche con ramas de canela y azúcar. 2. Dejar enfriar completamente la mezcla. 3. Colar para quitar canela, agregar esencia de vainilla. 4. Verter en moldes individuales o helador manual. 5. Si usa moldes, introducir palito de madera. 6. Congelar por 4-6 horas hasta solidificar. 7. Para helado manual, batir cada hora las primeras 3 horas. 8. Servir como postre o merienda refrescante.',
20, 10, 8, 'fácil', 'boliviana', 'Tradición Paceña');

-- Asociar ingredientes con las recetas bolivianas

-- Salteña Paceña (ID será el siguiente disponible)
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
((SELECT MAX(id) FROM recipe WHERE name = 'Salteña Paceña Tradicional'), (SELECT id FROM ingredient WHERE name = 'carne de res'), '500', 'g'),
((SELECT MAX(id) FROM recipe WHERE name = 'Salteña Paceña Tradicional'), (SELECT id FROM ingredient WHERE name = 'papa'), '3', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Salteña Paceña Tradicional'), (SELECT id FROM ingredient WHERE name = 'arveja'), '1', 'taza'),
((SELECT MAX(id) FROM recipe WHERE name = 'Salteña Paceña Tradicional'), (SELECT id FROM ingredient WHERE name = 'cebolla'), '2', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Salteña Paceña Tradicional'), (SELECT id FROM ingredient WHERE name = 'ajo'), '3', 'dientes'),
((SELECT MAX(id) FROM recipe WHERE name = 'Salteña Paceña Tradicional'), (SELECT id FROM ingredient WHERE name = 'ají colorado'), '2', 'cdas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Salteña Paceña Tradicional'), (SELECT id FROM ingredient WHERE name = 'huevo'), '4', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Salteña Paceña Tradicional'), (SELECT id FROM ingredient WHERE name = 'harina de trigo'), '500', 'g'),
((SELECT MAX(id) FROM recipe WHERE name = 'Salteña Paceña Tradicional'), (SELECT id FROM ingredient WHERE name = 'aceite vegetal'), '3', 'cdas');

-- Sopa de Maní
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
((SELECT MAX(id) FROM recipe WHERE name = 'Sopa de Maní Boliviana'), (SELECT id FROM ingredient WHERE name = 'maní'), '1', 'taza'),
((SELECT MAX(id) FROM recipe WHERE name = 'Sopa de Maní Boliviana'), (SELECT id FROM ingredient WHERE name = 'carne de res'), '400', 'g'),
((SELECT MAX(id) FROM recipe WHERE name = 'Sopa de Maní Boliviana'), (SELECT id FROM ingredient WHERE name = 'papa'), '3', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Sopa de Maní Boliviana'), (SELECT id FROM ingredient WHERE name = 'zanahoria'), '2', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Sopa de Maní Boliviana'), (SELECT id FROM ingredient WHERE name = 'arveja'), '1/2', 'taza'),
((SELECT MAX(id) FROM recipe WHERE name = 'Sopa de Maní Boliviana'), (SELECT id FROM ingredient WHERE name = 'cebolla'), '1', 'pieza'),
((SELECT MAX(id) FROM recipe WHERE name = 'Sopa de Maní Boliviana'), (SELECT id FROM ingredient WHERE name = 'ajo'), '2', 'dientes');

-- Fricasé de Cerdo
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
((SELECT MAX(id) FROM recipe WHERE name = 'Fricasé de Cerdo Paceño'), (SELECT id FROM ingredient WHERE name = 'cerdo'), '800', 'g'),
((SELECT MAX(id) FROM recipe WHERE name = 'Fricasé de Cerdo Paceño'), (SELECT id FROM ingredient WHERE name = 'chuño'), '6', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Fricasé de Cerdo Paceño'), (SELECT id FROM ingredient WHERE name = 'mote de maíz'), '1', 'taza'),
((SELECT MAX(id) FROM recipe WHERE name = 'Fricasé de Cerdo Paceño'), (SELECT id FROM ingredient WHERE name = 'cebolla'), '2', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Fricasé de Cerdo Paceño'), (SELECT id FROM ingredient WHERE name = 'ají amarillo'), '3', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Fricasé de Cerdo Paceño'), (SELECT id FROM ingredient WHERE name = 'hierba buena'), '2', 'ramas');

-- Pique Macho
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
((SELECT MAX(id) FROM recipe WHERE name = 'Pique Macho Cochabambino'), (SELECT id FROM ingredient WHERE name = 'carne de res'), '400', 'g'),
((SELECT MAX(id) FROM recipe WHERE name = 'Pique Macho Cochabambino'), (SELECT id FROM ingredient WHERE name = 'papa'), '4', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Pique Macho Cochabambino'), (SELECT id FROM ingredient WHERE name = 'huevo'), '2', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Pique Macho Cochabambino'), (SELECT id FROM ingredient WHERE name = 'tomate'), '2', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Pique Macho Cochabambino'), (SELECT id FROM ingredient WHERE name = 'cebolla'), '1', 'pieza'),
((SELECT MAX(id) FROM recipe WHERE name = 'Pique Macho Cochabambino'), (SELECT id FROM ingredient WHERE name = 'locoto'), '1', 'pieza');

-- Chairo Paceño
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
((SELECT MAX(id) FROM recipe WHERE name = 'Chairo Paceño Tradicional'), (SELECT id FROM ingredient WHERE name = 'chuño'), '8', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Chairo Paceño Tradicional'), (SELECT id FROM ingredient WHERE name = 'papa'), '4', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Chairo Paceño Tradicional'), (SELECT id FROM ingredient WHERE name = 'oca'), '6', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Chairo Paceño Tradicional'), (SELECT id FROM ingredient WHERE name = 'quinua blanca'), '1/2', 'taza'),
((SELECT MAX(id) FROM recipe WHERE name = 'Chairo Paceño Tradicional'), (SELECT id FROM ingredient WHERE name = 'habas'), '1/2', 'taza'),
((SELECT MAX(id) FROM recipe WHERE name = 'Chairo Paceño Tradicional'), (SELECT id FROM ingredient WHERE name = 'llama'), '300', 'g'),
((SELECT MAX(id) FROM recipe WHERE name = 'Chairo Paceño Tradicional'), (SELECT id FROM ingredient WHERE name = 'wakataya'), '1', 'rama');

-- Información nutricional para algunas recetas bolivianas clave
INSERT INTO nutritional_info (
    recipe_id, calories_per_serving, protein, carbs, fat, fiber, sugar, sodium,
    vitamin_a, vitamin_c, iron, calcium
) VALUES 
((SELECT MAX(id) FROM recipe WHERE name = 'Salteña Paceña Tradicional'), 420, 18.5, 45.2, 16.8, 3.2, 5.1, 680, 125.8, 15.2, 2.8, 65.2),
((SELECT MAX(id) FROM recipe WHERE name = 'Sopa de Maní Boliviana'), 385, 22.8, 28.5, 21.2, 4.8, 3.2, 520, 485.2, 8.5, 3.8, 95.8),
((SELECT MAX(id) FROM recipe WHERE name = 'Chairo Paceño Tradicional'), 295, 16.8, 48.5, 6.2, 8.5, 4.8, 420, 285.2, 12.8, 4.2, 125.8),
((SELECT MAX(id) FROM recipe WHERE name = 'Pique Macho Cochabambino'), 580, 28.5, 42.8, 32.1, 5.2, 6.8, 720, 185.2, 25.8, 3.2, 85.2),
((SELECT MAX(id) FROM recipe WHERE name = 'Silpancho Cochabambino'), 650, 32.8, 58.2, 28.5, 4.2, 8.5, 680, 125.8, 18.5, 3.8, 95.2);

-- Calificaciones de ejemplo para recetas bolivianas
INSERT INTO recipe_rating (user_id, recipe_id, rating, comment, created_at) VALUES
(1, (SELECT MAX(id) FROM recipe WHERE name = 'Salteña Paceña Tradicional'), 5, 'La mejor salteña que he probado. Muy jugosa y auténtica.', NOW()),
(1, (SELECT MAX(id) FROM recipe WHERE name = 'Sopa de Maní Boliviana'), 5, 'Sopa deliciosa y muy nutritiva. Perfecta para el frío.', NOW()),
(1, (SELECT MAX(id) FROM recipe WHERE name = 'Chairo Paceño Tradicional'), 4, 'Plato muy consistente y sabroso. Ideal para el altiplano.', NOW()),
(2, (SELECT MAX(id) FROM recipe WHERE name = 'Pique Macho Cochabambino'), 5, 'Plato abundante y delicioso. Perfecto para compartir.', NOW()),
(2, (SELECT MAX(id) FROM recipe WHERE name = 'Silpancho Cochabambino'), 4, 'Carne muy bien preparada. Un clásico cochabambino.', NOW()),
(1, (SELECT MAX(id) FROM recipe WHERE name = 'Fricasé de Cerdo Paceño'), 5, 'Plato tradicional paceño excelente. Muy auténtico.', NOW()),
(2, (SELECT MAX(id) FROM recipe WHERE name = 'Majadito Batido Cruceño'), 4, 'Desayuno energético y sabroso del oriente.', NOW()),
(1, (SELECT MAX(id) FROM recipe WHERE name = 'Llajwa Cochabambina Original'), 5, 'La salsa boliviana por excelencia. Perfecta.', NOW());

-- Sustituciones específicas para ingredientes bolivianos
INSERT INTO ingredient_substitution (recipe_id, original_ingredient_id, substitute_ingredient_id, conversion_ratio, notes, dietary_benefit) VALUES
-- Para Chairo Paceño
((SELECT MAX(id) FROM recipe WHERE name = 'Chairo Paceño Tradicional'), (SELECT id FROM ingredient WHERE name = 'llama'), (SELECT id FROM ingredient WHERE name = 'carne de res'), '1:1', 'Alternativa más común', 'disponibilidad'),
((SELECT MAX(id) FROM recipe WHERE name = 'Chairo Paceño Tradicional'), (SELECT id FROM ingredient WHERE name = 'chuño'), (SELECT id FROM ingredient WHERE name = 'papa'), '1:2', 'Si no hay chuño disponible', 'disponibilidad'),
((SELECT MAX(id) FROM recipe WHERE name = 'Chairo Paceño Tradicional'), (SELECT id FROM ingredient WHERE name = 'oca'), (SELECT id FROM ingredient WHERE name = 'camote'), '1:1', 'Tubérculo similar', 'disponibilidad'),

-- Para Sopa de Maní
((SELECT MAX(id) FROM recipe WHERE name = 'Sopa de Maní Boliviana'), (SELECT id FROM ingredient WHERE name = 'maní'), (SELECT id FROM ingredient WHERE name = 'almendra'), '1:1', 'Alternativa para alérgicos al maní', 'sin alérgenos'),

-- Para Fricasé
((SELECT MAX(id) FROM recipe WHERE name = 'Fricasé de Cerdo Paceño'), (SELECT id FROM ingredient WHERE name = 'mote de maíz'), (SELECT id FROM ingredient WHERE name = 'choclo'), '1:1', 'Maíz fresco en lugar de seco', 'disponibilidad'),

-- Para recetas con quinua
((SELECT MAX(id) FROM recipe WHERE name = 'Sopa de Quinua Real'), (SELECT id FROM ingredient WHERE name = 'quinua real'), (SELECT id FROM ingredient WHERE name = 'quinua blanca'), '1:1', 'Variedad más común', 'disponibilidad'),
((SELECT MAX(id) FROM recipe WHERE name = 'Keperi de Quinua Altiplánico'), (SELECT id FROM ingredient WHERE name = 'charque'), (SELECT id FROM ingredient WHERE name = 'carne de res'), '1:2', 'Carne fresca en lugar de seca', 'disponibilidad');

-- Comentarios sobre el uso del script
/*
SCRIPT DE RECETAS BOLIVIANAS TRADICIONALES

Este script contiene 30 recetas auténticas de Bolivia, organizadas por regiones:
- ALTIPLANO: La Paz, Oruro, Potosí (Chairo, Fricasé, Api, etc.)
- VALLES: Cochabamba, Sucre, Tarija (Salteña, Silpancho, Saice, etc.)  
- LLANOS: Santa Cruz, Beni, Pando (Majadito, Pacumutu, Cuñapé, etc.)

INGREDIENTES AUTÓCTONOS INCLUIDOS:
- Tubérculos: chuño, tunta, oca, papalisa, isaño
- Cereales: quinua real, amaranto, cañahua, tarwi
- Carnes: llama, alpaca, charque, surubí, pacu
- Condimentos: locoto, ají amarillo, wakataya, muña

NOTAS IMPORTANTES:
1. Las recetas respetan las tradiciones culinarias regionales
2. Se incluyen variaciones estacionales de ingredientes
3. Los tiempos de cocción consideran técnicas tradicionales
4. Se preservan nombres originales en quechua/aymara cuando corresponde

PARA EJECUTAR:
1. Asegurarse de que las tablas base estén creadas
2. Ejecutar: psql -d sistema_culinario -f bolivian_recipes.sql
3. Verificar que no haya conflictos con datos existentes

EXTENSIONES SUGERIDAS:
- Agregar más recetas regionales específicas
- Incluir bebidas tradicionales (chicha, té de coca)
- Añadir postres bolivianos (tawa tawa, buñuelos)
- Incorporar recetas de festividades (carnaval, todos santos)
*/	

-- Script de 30 Recetas Regionales Mixtas - Bolivia y Sudamérica
-- Fusión de cocina boliviana con países vecinos y técnicas regionales
-- Ejecutar después de los scripts anteriores

-- Nuevos ingredientes regionales sudamericanos
INSERT INTO ingredient (name, category, calories_per_100g, common_allergen, seasonal_availability) VALUES 
-- Ingredientes peruanos/ecuatorianos
('ají rocoto', 'spices', 30, false, 'todo_año'),
('culantro', 'spices', 23, false, 'todo_año'),
('chicha morada', 'beverages', 45, false, 'todo_año'),
('ají panca', 'spices', 35, false, 'todo_año'),
('cancha serrana', 'grains', 350, false, 'todo_año'),

-- Ingredientes argentinos/chilenos  
('chimichurri', 'condiments', 180, false, 'todo_año'),
('merkén', 'spices', 290, false, 'todo_año'),
('mote pelado', 'grains', 98, false, 'todo_año'),
('charqui chileno', 'proteins', 420, false, 'todo_año'),

-- Ingredientes brasileños/paraguayos
('farofa', 'grains', 340, false, 'todo_año'),
('mandioca', 'vegetables', 160, false, 'todo_año'),
('cupuaçu', 'fruits', 49, false, 'verano'),
('tucumán', 'fruits', 180, false, 'verano'),
('guaraná', 'beverages', 30, false, 'todo_año'),

-- Frutas amazónicas/tropicales  
('acaí', 'fruits', 70, false, 'todo_año'),
('cacao amazónico', 'fruits', 228, false, 'todo_año'),
('copoazú', 'fruits', 52, false, 'verano'),
('motojobobo', 'fruits', 95, false, 'verano'),
('achachairú', 'fruits', 58, false, 'verano'),

-- Especias y condimentos regionales
('huacatay', 'spices', 25, false, 'todo_año'),
('paico', 'spices', 20, false, 'todo_año'),
('coca boliviana', 'spices', 15, false, 'todo_año'),
('totora', 'vegetables', 45, false, 'todo_año'),

-- Quesos y lácteos regionales
('queso de cabra andino', 'dairy', 290, true, 'todo_año'),
('quesillo boliviano', 'dairy', 250, true, 'todo_año'),
('leche de cabra', 'dairy', 69, true, 'todo_año');

-- 30 NUEVAS RECETAS REGIONALES MIXTAS

-- 1. Anticucho Boliviano-Peruano
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Anticucho Boliviano-Peruano', 
'Corazón de res marinado en ají panca y chicha de jora, asado a la parrilla. Fusión andina perfecta.',
'1. Limpiar corazones de res, cortar en cubos medianos. 2. Preparar marinada: ají panca licuado, chicha de jora, ajo, comino, sal. 3. Marinar corazones 4 horas mínimo. 4. Ensartar en palitos de anticucho con alternancia de corazón. 5. Asar en parrilla o plancha caliente 3 minutos por lado. 6. Pincelar con marinada durante cocción. 7. Servir con papa sancochada, choclo y salsa criolla. 8. Acompañar con chicha morada helada.',
240, 15, 6, 'medio', 'fusión andina', 'Chef Regional');

-- 2. Quinotto Risotto Andino
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Quinotto de Queso de Cabra', 
'Risotto de quinua real con queso de cabra andino y hierbas aromáticas. Innovación culinaria altiplánica.',
'1. Lavar quinua hasta agua clara, tostar ligeramente en sartén seca. 2. Calentar caldo de verduras con hierbas andinas. 3. Sofreír cebolla finamente picada en aceite de oliva. 4. Agregar quinua tostada, revolver 2 minutos. 5. Añadir caldo caliente de a poco, revolviendo constantemente. 6. Cocinar 18-20 minutos hasta cremoso. 7. Incorporar queso de cabra desmenuzado y mantequilla. 8. Decorar con muña fresca y servir inmediatamente.',
15, 25, 4, 'difícil', 'fusión andina', 'Innovación Culinaria');

-- 3. Pachamanca Moderna  
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Pachamanca Boliviana Moderna', 
'Carnes y tubérculos cocidos bajo tierra con piedras calientes. Técnica ancestral con toques modernos.',
'1. Calentar piedras volcánicas en fogata por 2 horas. 2. Sazonar carnes: llama, cordero, pollo con huacatay, ají, sal. 3. Envolver carnes en hojas de plátano o papel aluminio. 4. En hoyo de 50cm, colocar piedras calientes en base. 5. Acomodar carnes, papas nativas, choclo, habas. 6. Cubrir con más piedras calientes y tierra. 7. Cocinar enterrado 90 minutos. 8. Destapar y servir con salsas variadas.',
180, 90, 10, 'difícil', 'fusión andina', 'Tradición Ancestral');

-- 4. Ceviche de Surubí Amazónico
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Ceviche de Surubí con Motojobobo', 
'Surubí del río amazónico marinado en limón con frutas tropicales. Fusión amazónica refrescante.',
'1. Cortar surubí fresco en cubos de 2cm, sin espinas. 2. Marinar con jugo de limón ácido, sal, ají amarillo. 3. Dejar "cocinar" en limón por 15 minutos. 4. Agregar cebolla roja en juliana fina, cilantro. 5. Incorporar motojobobo en cubitos, achachairú. 6. Sazonar con sal, pimienta, un toque de azúcar. 7. Servir frío con patacones de plátano verde. 8. Decorar con cancha serrana y hojas de coca.',
30, 0, 4, 'medio', 'fusión amazónica', 'Cocina Tropical');

-- 5. Empanada Salteña-Argentina
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Empanada Salteña-Argentina', 
'Empanada horneada que fusiona la jugosidad salteña con el repulgue argentino. Lo mejor de ambos países.',
'1. Preparar masa: harina, grasa de cerdo, agua tibia, sal, azúcar. 2. Para relleno: carne picada a cuchillo, cebolla, ají molido. 3. Agregar papa en cubitos, huevo duro, aceitunas, pasas. 4. Cocinar hasta que carne esté sellada pero jugosa. 5. Enfriar relleno completamente antes de usar. 6. Armar empanadas con repulgue argentino (trenzado). 7. Pintar con huevo, hornear a 200°C por 18 minutos. 8. Servir calientes con chimichurri boliviano.',
60, 18, 12, 'medio', 'fusión rioplatense', 'Hermandad Culinaria');

-- 6. Asado Cruceño-Gaucho
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Asado Cruceño-Gaucho', 
'Parrillada que combina cortes criollos con técnicas gauchas. Carne a las brasas con salsas bolivianas.',
'1. Preparar cortes: asado de tira, vacío, chorizo cruceño, morcilla. 2. Encender parrilla con carbón, lograr brasas parejas. 3. Salar carnes 30 minutos antes de cocinar. 4. Cocinar chorizo y morcilla primero, 10 minutos. 5. Agregar cortes de res, cocinar según espesor. 6. Preparar salsas: llajwa, chimichurri, salsa golf. 7. Acompañar con mandioca hervida, ensalada mixta. 8. Servir en tabla de madera con pan casero.',
45, 60, 8, 'medio', 'fusión gaucha', 'Tradición Ganadera');

-- 7. Locro Fusion Andino
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Locro Andino Tricolor', 
'Locro que une tradiciones de Bolivia, Perú y Ecuador con quinua, zapallo y maíz gigante.',
'1. Remojar tarwi la noche anterior, hervir y pelar. 2. Cocinar zapallo hasta suave, hacer puré. 3. Sofreír cebolla, ajo, ají amarillo, comino. 4. Agregar caldo, puré de zapallo, maíz gigante. 5. Incorporar tarwi pelado, papa amarilla en cubos. 6. Cocinar quinua aparte hasta transparente. 7. Unir quinua al locro, sazonar con huacatay. 8. Servir con queso fresco y cancha serrana.',
720, 45, 6, 'medio', 'fusión andina', 'Tradición Tricolor');

-- 8. Tacu Tacu Boliviano
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Tacu Tacu Boliviano con Charque', 
'Arroz con frijoles refrito al estilo peruano pero con charque boliviano y ají colorado.',
'1. Cocinar frijoles negros hasta suaves, reservar. 2. Cocinar arroz blanco suelto, enfriar. 3. Remojar charque, desmenuzar finamente. 4. Sofreír cebolla, ajo, ají colorado molido. 5. Agregar charque desmenuzado, dorar bien. 6. Incorporar frijoles cocidos, aplastar parcialmente. 7. Añadir arroz frío, integrar y formar costra. 8. Servir con huevo frito, plátano maduro, salsa criolla.',
15, 25, 4, 'fácil', 'fusión criolla', 'Cocina de Aprovechamiento');

-- 9. Sopa Paraguaya Boliviana
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Sopa Paraguaya con Queso Boliviano', 
'Torta de maíz paraguaya enriquecida con queso fresco boliviano y choclo dulce.',
'1. Desgranar choclo fresco, licuar con poca leche. 2. Mezclar harina de maíz con queso fresco desmenuzado. 3. Batir huevos con leche, sal, pimienta blanca. 4. Incorporar choclo licuado a la mezcla de harina. 5. Agregar cebolla picada finamente, perejil. 6. Verter en molde engrasado, hornear a 180°C. 7. Cocinar 45 minutos hasta dorar superficie. 8. Servir tibio como acompañamiento o plato principal.',
20, 45, 8, 'fácil', 'fusión guaraní', 'Tradición Mestiza');

-- 10. Humita en Chala Mixta
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Humita Boliviano-Argentina', 
'Humita dulce y salada envuelta en chala, fusionando tradiciones del NOA con el altiplano.',
'1. Desgranar choclo tierno, rayar grueso. 2. Mezclar con quesillo boliviano desmenuzado. 3. Agregar cebolla de verdeo, ají amarillo molido. 4. Sazonar con sal, pimienta, azúcar, comino. 5. Batir clara de huevo a nieve, incorporar suavemente. 6. Rellenar chalas limpias con mezcla. 7. Atar chalas, cocinar al vapor 30 minutos. 8. Servir caliente con café con leche.',
30, 30, 8, 'medio', 'fusión NOA', 'Tradición Norteña');

-- 11. Mondongo Andino-Llanero
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Mondongo Andino-Llanero', 
'Mondongo con tubérculos andinos y yuca llanera. Encuentro de dos geografías en un plato.',
'1. Limpiar mondongo, hervir 2 horas hasta tiernizar. 2. Cortar en tiras, reservar caldo. 3. Sofreír sofrito: cebolla, ajo, ají, culantro. 4. Agregar mondongo cortado, dorar 10 minutos. 5. Incorporar papa, oca, yuca en cubos grandes. 6. Añadir caldo, garbanzos, maíz pelado. 7. Cocinar 40 minutos hasta que tubérculos estén suaves. 8. Rectificar sazón, servir con arepa o pan.',
30, 160, 8, 'difícil', 'fusión continental', 'Mestizaje Culinario');

-- 12. Chicharrón de Alpaca Gourmet
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Chicharrón de Alpaca con Reducción', 
'Chicharrón de alpaca con técnicas modernas, reducción de chicha y espuma de oca.',
'1. Cortar alpaca en cubos uniformes, sazonar 2 horas. 2. Cocinar en su grasa a fuego medio hasta dorar. 3. Para reducción: hervir chicha de jora hasta espesar. 4. Cocinar oca hasta suave, hacer espuma con batidora. 5. Freír camote en bastones hasta crocante. 6. Tostar cancha serrana con sal de mar. 7. Emplatar: chicharrón, espuma, reducción en gotas. 8. Decorar con microgreens de muña.',
150, 30, 4, 'difícil', 'fusión gourmet', 'Alta Cocina Andina');

-- 13. Mazamorra Morada Boliviana
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Mazamorra Morada con Tunta', 
'Postre peruano adaptado con maíz morado boliviano y tunta molida como espesante.',
'1. Hervir maíz morado con canela, clavo, cáscara de piña. 2. Colar líquido morado, volver a hervir. 3. Moler tunta finamente hasta polvo. 4. Disolver tunta molida en agua fría. 5. Agregar al líquido hirviendo, revolver constantemente. 6. Cocinar hasta espesar, endulzar con chancaca. 7. Agregar frutas: piña, membrillo, guinda. 8. Servir frío espolvoreado con canela.',
20, 45, 6, 'fácil', 'fusión dulcera', 'Tradición Morada');

-- 14. Arepa Andina de Quinua
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Arepa Andina de Quinua y Charque', 
'Arepa venezolana hecha con harina de quinua, rellena de charque desmenuzado.',
'1. Mezclar harina de quinua con harina de maíz precocida. 2. Agregar agua tibia con sal hasta formar masa. 3. Amasar hasta suave, reposar 15 minutos. 4. Para relleno: remojar charque, desmenuzar. 5. Sofreír con cebolla, tomate, ají amarillo. 6. Formar arepas, cocinar en plancha 8 minutos por lado. 7. Abrir, rellenar con charque guisado. 8. Servir con queso fresco y aguacate.',
30, 20, 6, 'fácil', 'fusión llanera', 'Innovación Nutritiva');

-- 15. Feijoada Amazónica
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Feijoada Amazónica con Pacu', 
'Feijoada brasileña adaptada con pacu ahumado y frijoles bolivianos de los llanos.',
'1. Remojar frijoles negros toda la noche. 2. Cocinar frijoles con laurel hasta suaves. 3. Ahumar pacu en carbón con madera de motacú. 4. Desmenuzar pacu ahumado, quitar espinas. 5. Sofreír cebolla, ajo, tomate, culantro. 6. Agregar pacu desmenuzado al sofrito. 7. Incorporar frijoles cocidos con su caldo. 8. Servir con farofa de mandioca, naranja, cachaza.',
720, 120, 8, 'medio', 'fusión tropical', 'Hermandad Amazónica');

-- 16. Pastel de Papa Andino
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Pastel de Papa con Tres Tubérculos', 
'Pastel chileno reinventado con papa, oca e isaño. Capas de sabor andino.',
'1. Hervir papas, oca, isaño por separado hasta suaves. 2. Hacer puré de cada tubérculo, sazonar diferente. 3. Preparar pino: carne molida, cebolla, comino, aceitunas. 4. Agregar huevo duro picado, pasas al pino. 5. En molde: capa de puré de papa, pino, oca. 6. Terminar con puré de isaño, pintar con huevo. 7. Hornear a 180°C por 30 minutos hasta dorar. 8. Reposar 10 minutos antes de cortar.',
45, 30, 8, 'medio', 'fusión sureña', 'Innovación Tubércula');

-- 17. Bandeja Paisa Boliviana
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Bandeja Paisa Boliviana', 
'Bandeja colombiana adaptada con productos bolivianos: frijol tarwi, chorizo chuquisaqueño.',
'1. Cocinar tarwi toda la noche, pelar y guisar. 2. Freír chorizo chuquisaqueño en rodajas. 3. Preparar carne molida con sofrito boliviano. 4. Freír plátano maduro hasta caramelizar. 5. Cocinar morcilla cruceña hasta crocante. 6. Freír huevos manteniendo yema líquida. 7. Acompañar con arroz blanco, arepa de maíz. 8. Servir todo en bandeja grande con aguacate.',
30, 45, 4, 'fácil', 'fusión cafetera', 'Abundancia Tropical');

-- 18. Caldo de Gallina Andino
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Caldo de Gallina con Quinua', 
'Caldo peruano enriquecido con quinua real y papas nativas del altiplano boliviano.',
'1. Cocinar gallina criolla hasta tiernizar completamente. 2. Desmenuzar carne, colar y aclarar caldo. 3. Lavar quinua hasta agua clara. 4. Hervir papa wayk''a, oca en el caldo. 5. Agregar quinua, cocinar 15 minutos más. 6. Incorporar carne desmenuzada, apio, zanahoria. 7. Sazonar con sal, pimienta, hierba buena. 8. Servir con huevo duro y ají amarillo molido.',
20, 90, 6, 'medio', 'fusión reconfortante', 'Tradición Nutritiva');

-- 19. Mote con Huesillo Boliviano
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Mote con Huesillo de Durazno', 
'Refresco chileno adaptado con mote boliviano y duraznos deshidratados del valle.',
'1. Cocer mote pelado hasta suave pero firme. 2. Remojar duraznos deshidratados en agua tibia. 3. Hervir agua con azúcar, canela, clavo de olor. 4. Agregar duraznos remojados, cocinar 20 minutos. 5. Enfriar almíbar completamente en refrigerador. 6. Servir en vaso: mote, durazno, almíbar frío. 7. Agregar hielo picado al momento de servir. 8. Decorar con hoja de menta fresca.',
30, 30, 4, 'fácil', 'fusión refrescante', 'Tradición Veraniega');

-- 20. Sancocho Amazónico
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Sancocho Amazónico Tricolor', 
'Sancocho caribeño con pescados amazónicos, yuca, plátano verde y ají charapita.',
'1. Cortar surubí y pacu en trozos grandes. 2. Sazonar pescado con limón, sal, ají charapita. 3. Sofreír sofrito: cebolla, ajo, cilantro, culantro. 4. Agregar agua, llevar a ebullición. 5. Incorporar yuca, plátano verde, ñame en trozos. 6. Cocinar 20 minutos hasta tubérculos suaves. 7. Agregar pescado, cocinar 10 minutos más. 8. Servir con arroz con coco y patacones.',
25, 35, 6, 'medio', 'fusión caribeña', 'Sabor Tropical');

-- 21. Chicha de Jora Gourmet
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Chicha de Jora Espumante', 
'Chicha ancestral fermentada con técnicas modernas, servida como aperitivo gourmet.',
'1. Germinar maíz amarillo en ambiente húmedo 3 días. 2. Secar al sol, moler grueso. 3. Hervir jora molida 3 horas, colar. 4. Fermentar líquido 5 días con levadura natural. 5. Filtrar, agregar miel de abeja, canela. 6. Segunda fermentación en botella 15 días. 7. Refrigerar, servir bien frío en copas. 8. Decorar con flores comestibles andinas.',
7200, 180, 8, 'difícil', 'fusión ancestral', 'Tradición Milenaria');

-- 22. Chupe de Quinua Marino
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Chupe de Quinua con Surubí', 
'Chupe peruano de camarones adaptado con quinua real y surubí del río Mamoré.',
'1. Lavar quinua hasta agua clara, reservar. 2. Preparar caldo con cabezas de surubí, cebolla, apio. 3. Colar caldo, llevarlo a ebullición. 4. Agregar quinua, cocinar 15 minutos. 5. Incorporar papa amarilla en cubos, choclo. 6. Añadir surubí en trozos, habas frescas. 7. Ligar con huevo batido, leche evaporada. 8. Servir con queso fresco y orégano.',
20, 35, 6, 'medio', 'fusión fluvial', 'Innovación Proteica');

-- 23. Tamales Oaxaqueños-Bolivianos
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Tamales de Chía con Mole Boliviano', 
'Tamales mexicanos con masa de chía boliviana y mole de ají colorado.',
'1. Remojar chía boliviana, moler con masa de maíz. 2. Batir masa con manteca hasta esponjosa. 3. Para mole: tostar ají colorado, almendras, ajonjolí. 4. Licuar con caldo, chocolate, especias. 5. Cocinar pollo en mole hasta tierno. 6. Extender masa en hoja de plátano. 7. Rellenar con pollo en mole, aceitunas. 8. Envolver, cocer al vapor 60 minutos.',
120, 90, 10, 'difícil', 'fusión mesoamericana', 'Encuentro Cultural');

-- 24. Coxinha de Llama
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Coxinha de Llama con Queso Andino', 
'Coxinha brasileña rellena de llama desmenuzada y queso de cabra andino.',
'1. Cocinar carne de llama hasta tiernizar completamente. 2. Desmenuzar finamente, sazonar con comino, ají. 3. Preparar masa con caldo de llama, harina, mantequilla. 4. Cocinar masa revolviendo hasta despegar de olla. 5. Enfriar, formar bolitas, rellenar con carne. 6. Moldear en forma de gota, pasar por harina. 7. Rebozar en huevo batido y pan molido. 8. Freír en aceite caliente hasta dorar.',
45, 20, 12, 'medio', 'fusión brasileña', 'Snack Andino');

-- 25. Ceviche de Quinua
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Ceviche de Quinua Tricolor', 
'Innovación vegana del ceviche usando quinua real, quinua roja y quinua negra.',
'1. Cocinar quinuas por separado hasta al dente. 2. Enfriar completamente las quinuas cocidas. 3. Preparar leche de tigre: limón, ají amarillo, apio. 4. Marinar quinuas en leche de tigre 20 minutos. 5. Agregar cebolla roja, cilantro, choclo. 6. Incorporar camote en cubitos, cancha tostada. 7. Sazonar con sal, pimienta, un toque de azúcar. 8. Servir frío con hojas de lechuga.',
30, 15, 4, 'fácil', 'fusión vegana', 'Innovación Sustentable');

-- 26. Ajiaco Santafereño-Andino
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Ajiaco con Tres Papas Andinas', 
'Ajiaco bogotano enriquecido con papa wayk''a, oca y papalisa del altiplano.',
'1. Cocinar pollo con agua, cebolla, ajo, apio. 2. Desmenuzar pollo, colar caldo. 3. Cocinar papa wayk''a hasta deshacer parcialmente. 4. Agregar oca, papalisa en trozos. 5. Incorporar choclo desgranado, alcaparras. 6. Añadir pollo desmenuzado, crema de leche. 7. Sazonar con guascas (o huacatay). 8. Servir con aguacate, crema, alcaparras.',
25, 45, 6, 'medio', 'fusión andina-cafetera', 'Cremosidad Altiplánica');

-- 27. Seco de Cabrito Norteño
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Seco de Cabrito con Chicha de Jora', 
'Seco norteño peruano cocido con chicha de jora boliviana y culantro amazónico.',
'1. Cortar cabrito en presas medianas, sazonar con comino, ajo. 2. Dorar carne en aceite caliente hasta sellar. 3. Licuar culantro con chicha de jora, cebolla, ají amarillo. 4. Agregar mezcla verde a la carne dorada. 5. Incorporar frijoles canarios remojados. 6. Cocinar a fuego lento 90 minutos hasta tiernizar. 7. Rectificar sazón, agregar yuca en trozos. 8. Servir con arroz graneado y salsa criolla.',
25, 105, 6, 'medio', 'fusión norteña', 'Tradición Cabrillera');

-- 28. Moloko de Plátano
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Moloko de Plátano Verde', 
'Puré dominicano de plátano adaptado con plátano verde boliviano y chicharrón de cerdo.',
'1. Hervir plátano verde pelado con sal hasta suave. 2. Escurrir reservando agua de cocción. 3. Hacer puré agregando agua de cocción gradualmente. 4. Sazonar con mantequilla, sal, pimienta blanca. 5. Freír chicharrón de cerdo hasta crocante. 6. Preparar cebollitas encurtidas en vinagre. 7. Servir mangú con chicharrón encima. 8. Acompañar con huevo frito y aguacate.',
15, 25, 4, 'fácil', 'fusión caribeña', 'Desayuno Tropical');

-- 29. Tortilla de Papa Andina
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Tortilla de Papas Nativas', 
'Tortilla española reinventada con papas nativas bolivianas y queso de cabra.',
'1. Pelar papa wayk''a, oca, cortar en láminas finas. 2. Freír en aceite a fuego medio hasta suaves. 3. Escurrir papas, reservar aceite. 4. Batir huevos con sal, pimienta, hierbas. 5. Mezclar papas con huevos, queso de cabra. 6. Cocinar en sartén con aceite reservado. 7. Voltear tortilla con plato cuando dore. 8. Servir tibia cortada en porciones.',
20, 15, 6, 'medio', 'fusión ibérica', 'Encuentro de Culturas');

-- 30. Helado de Cupuaçu Andino
INSERT INTO recipe (name, description, instructions, prep_time, cook_time, servings, difficulty, cuisine_type, author) VALUES 
('Helado de Cupuaçu con Coca', 
'Helado amazónico de cupuaçu con infusión de hoja de coca boliviana.',
'1. Preparar infusión concentrada de hoja de coca. 2. Colar y enfriar completamente la infusión. 3. Extraer pulpa de cupuaçu, licuar con azúcar. 4. Mezclar pulpa con leche condensada, crema. 5. Agregar infusión de coca gradualmente. 6. Batir hasta espumar, congelar en heladera. 7. Batir cada hora las primeras 3 horas. 8. Servir decorado con chocolate rallado.',
30, 10, 8, 'medio', 'fusión amazónica', 'Postre Ancestral');

-- Asociaciones de ingredientes para las nuevas recetas

-- Anticucho Boliviano-Peruano
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
((SELECT MAX(id) FROM recipe WHERE name = 'Anticucho Boliviano-Peruano'), (SELECT id FROM ingredient WHERE name = 'carne de res'), '800', 'g'),
((SELECT MAX(id) FROM recipe WHERE name = 'Anticucho Boliviano-Peruano'), (SELECT id FROM ingredient WHERE name = 'ají panca'), '3', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Anticucho Boliviano-Peruano'), (SELECT id FROM ingredient WHERE name = 'chicha morada'), '1', 'taza'),
((SELECT MAX(id) FROM recipe WHERE name = 'Anticucho Boliviano-Peruano'), (SELECT id FROM ingredient WHERE name = 'ajo'), '4', 'dientes'),
((SELECT MAX(id) FROM recipe WHERE name = 'Anticucho Boliviano-Peruano'), (SELECT id FROM ingredient WHERE name = 'comino'), '1', 'cdita'),
((SELECT MAX(id) FROM recipe WHERE name = 'Anticucho Boliviano-Peruano'), (SELECT id FROM ingredient WHERE name = 'papa'), '4', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Anticucho Boliviano-Peruano'), (SELECT id FROM ingredient WHERE name = 'choclo'), '2', 'piezas');

-- Quinotto de Queso de Cabra
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
((SELECT MAX(id) FROM recipe WHERE name = 'Quinotto de Queso de Cabra'), (SELECT id FROM ingredient WHERE name = 'quinua real'), '1.5', 'tazas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Quinotto de Queso de Cabra'), (SELECT id FROM ingredient WHERE name = 'queso de cabra andino'), '200', 'g'),
((SELECT MAX(id) FROM recipe WHERE name = 'Quinotto de Queso de Cabra'), (SELECT id FROM ingredient WHERE name = 'cebolla'), '1', 'pieza'),
((SELECT MAX(id) FROM recipe WHERE name = 'Quinotto de Queso de Cabra'), (SELECT id FROM ingredient WHERE name = 'aceite de oliva'), '3', 'cdas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Quinotto de Queso de Cabra'), (SELECT id FROM ingredient WHERE name = 'mantequilla'), '2', 'cdas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Quinotto de Queso de Cabra'), (SELECT id FROM ingredient WHERE name = 'muña'), '2', 'ramas');

-- Ceviche de Surubí con Motojobobo
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES
((SELECT MAX(id) FROM recipe WHERE name = 'Ceviche de Surubí con Motojobobo'), (SELECT id FROM ingredient WHERE name = 'surubí'), '600', 'g'),
((SELECT MAX(id) FROM recipe WHERE name = 'Ceviche de Surubí con Motojobobo'), (SELECT id FROM ingredient WHERE name = 'limón'), '8', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Ceviche de Surubí con Motojobobo'), (SELECT id FROM ingredient WHERE name = 'motojobobo'), '1', 'taza'),
((SELECT MAX(id) FROM recipe WHERE name = 'Ceviche de Surubí con Motojobobo'), (SELECT id FROM ingredient WHERE name = 'achachairú'), '6', 'piezas'),
((SELECT MAX(id) FROM recipe WHERE name = 'Ceviche de Surubí con Motojobobo'), (SELECT id FROM ingredient WHERE name = 'cebolla'), '1', 'pieza'),
((SELECT MAX(id) FROM recipe WHERE name = 'Ceviche de Surubí con Motojobobo'), (SELECT id FROM ingredient WHERE name = 'cilantro'), '1/2', 'taza'),
((SELECT MAX(id) FROM recipe WHERE name = 'Ceviche de Surubí con Motojobobo'), (SELECT id FROM ingredient WHERE name = 'cancha serrana'), '1/4', 'taza');

-- Información nutricional para recetas clave
INSERT INTO nutritional_info (
    recipe_id, calories_per_serving, protein, carbs, fat, fiber, sugar, sodium,
    vitamin_a, vitamin_c, iron, calcium
) VALUES 
((SELECT MAX(id) FROM recipe WHERE name = 'Anticucho Boliviano-Peruano'), 385, 28.5, 15.2, 22.8, 2.1, 3.5, 580, 95.2, 8.5, 4.2, 25.8),
((SELECT MAX(id) FROM recipe WHERE name = 'Quinotto de Queso de Cabra'), 420, 18.8, 58.5, 12.5, 4.8, 2.1, 520, 185.2, 5.2, 3.8, 295.8),
((SELECT MAX(id) FROM recipe WHERE name = 'Ceviche de Surubí con Motojobobo'), 185, 24.8, 8.5, 3.2, 2.8, 6.8, 320, 125.8, 85.2, 1.8, 45.2),
((SELECT MAX(id) FROM recipe WHERE name = 'Pachamanca Boliviana Moderna'), 485, 32.8, 28.5, 25.2, 5.8, 4.2, 620, 285.2, 15.8, 3.5, 85.2),
((SELECT MAX(id) FROM recipe WHERE name = 'Asado Cruceño-Gaucho'), 520, 35.8, 12.5, 35.2, 3.8, 2.1, 720, 85.2, 12.5, 4.8, 65.2);

-- Comentarios sobre las recetas regionales mixtas

-- Calificaciones de ejemplo para las nuevas recetas
INSERT INTO recipe_rating (user_id, recipe_id, rating, comment, created_at) VALUES
(1, (SELECT MAX(id) FROM recipe WHERE name = 'Anticucho Boliviano-Peruano'), 5, 'Fusión perfecta entre Bolivia y Perú. Sabores auténticos.', NOW()),
(2, (SELECT MAX(id) FROM recipe WHERE name = 'Quinotto de Queso de Cabra'), 4, 'Innovación culinaria excelente. La quinua como risotto es genial.', NOW()),
(1, (SELECT MAX(id) FROM recipe WHERE name = 'Ceviche de Surubí con Motojobobo'), 5, 'Ceviche amazónico refrescante. El surubí queda perfecto.', NOW()),
(2, (SELECT MAX(id) FROM recipe WHERE name = 'Pachamanca Boliviana Moderna'), 4, 'Técnica ancestral con toques modernos. Muy auténtico.', NOW()),
(1, (SELECT MAX(id) FROM recipe WHERE name = 'Asado Cruceño-Gaucho'), 5, 'Parrillada espectacular. Lo mejor de ambas tradiciones.', NOW()),
(2, (SELECT MAX(id) FROM recipe WHERE name = 'Tacu Tacu Boliviano'), 4, 'Aprovechamiento inteligente con sabor boliviano único.', NOW()),
(1, (SELECT MAX(id) FROM recipe WHERE name = 'Feijoada Amazónica'), 5, 'El pacu ahumado le da un toque especial increíble.', NOW()),
(2, (SELECT MAX(id) FROM recipe WHERE name = 'Ceviche de Quinua Tricolor'), 4, 'Alternativa vegana muy creativa y colorida.', NOW());

-- Sustituciones para ingredientes regionales específicos
INSERT INTO ingredient_substitution (recipe_id, original_ingredient_id, substitute_ingredient_id, conversion_ratio, notes, dietary_benefit) VALUES
-- Para Anticucho
((SELECT MAX(id) FROM recipe WHERE name = 'Anticucho Boliviano-Peruano'), (SELECT id FROM ingredient WHERE name = 'ají panca'), (SELECT id FROM ingredient WHERE name = 'ají colorado'), '1:1', 'Alternativa más picante', 'disponibilidad'),
((SELECT MAX(id) FROM recipe WHERE name = 'Anticucho Boliviano-Peruano'), (SELECT id FROM ingredient WHERE name = 'chicha morada'), (SELECT id FROM ingredient WHERE name = 'chicha de maíz'), '1:1', 'Chicha boliviana tradicional', 'local'),

-- Para Quinotto
((SELECT MAX(id) FROM recipe WHERE name = 'Quinotto de Queso de Cabra'), (SELECT id FROM ingredient WHERE name = 'queso de cabra andino'), (SELECT id FROM ingredient WHERE name = 'queso fresco boliviano'), '1:1', 'Queso más suave', 'disponibilidad'),

-- Para Ceviche Amazónico
((SELECT MAX(id) FROM recipe WHERE name = 'Ceviche de Surubí con Motojobobo'), (SELECT id FROM ingredient WHERE name = 'motojobobo'), (SELECT id FROM ingredient WHERE name = 'mango'), '1:1', 'Fruta tropical similar', 'disponibilidad'),
((SELECT MAX(id) FROM recipe WHERE name = 'Ceviche de Surubí con Motojobobo'), (SELECT id FROM ingredient WHERE name = 'achachairú'), (SELECT id FROM ingredient WHERE name = 'uva'), '1:1', 'Fruta ácida similar', 'disponibilidad'),

-- Para Pachamanca
((SELECT MAX(id) FROM recipe WHERE name = 'Pachamanca Boliviana Moderna'), (SELECT id FROM ingredient WHERE name = 'llama'), (SELECT id FROM ingredient WHERE name = 'carne de res'), '1:1', 'Carne más común', 'disponibilidad'),
((SELECT MAX(id) FROM recipe WHERE name = 'Pachamanca Boliviana Moderna'), (SELECT id FROM ingredient WHERE name = 'huacatay'), (SELECT id FROM ingredient WHERE name = 'hierba buena'), '1:1', 'Hierba aromática local', 'disponibilidad');
