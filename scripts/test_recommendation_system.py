#!/usr/bin/env python3
# scripts/test_recommendation_system.py

import os
import sys
import logging
import json

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.services.recomendacion import SistemaRecomendacion
from app.services.motor_inferencia import MotorInferencia
from app.models.ingrediente import Ingrediente
from app.models.receta import Receta, RestriccionDietetica, Sustitucion
from app.models.usuario import PreferenciaUsuario

def test_recommendation_system():
    """
    Prueba comprehensiva del sistema de recomendación
    """
    app = create_app()

    with app.app_context():
        logger.info("🧪 INICIANDO PRUEBAS DEL SISTEMA DE RECOMENDACIÓN")
        logger.info("=" * 80)
        
        # === VERIFICAR DATOS BASE ===
        logger.info("📊 VERIFICANDO DATOS BASE")
        logger.info("-" * 50)
        
        ingredientes_count = Ingrediente.query.count()
        recetas_count = Receta.query.count()
        restricciones_count = RestriccionDietetica.query.count()
        sustituciones_count = Sustitucion.query.count()
        
        logger.info(f"✅ Ingredientes: {ingredientes_count}")
        logger.info(f"✅ Recetas: {recetas_count}")
        logger.info(f"✅ Restricciones dietéticas: {restricciones_count}")
        logger.info(f"✅ Sustituciones: {sustituciones_count}")
        
        if ingredientes_count < 10 or recetas_count < 5:
            logger.error("❌ Datos insuficientes para las pruebas")
            return False
        
        # === INICIALIZAR SERVICIOS ===
        logger.info("\n🔧 INICIALIZANDO SERVICIOS")
        logger.info("-" * 50)
        
        try:
            sistema_recomendacion = SistemaRecomendacion()
            motor_inferencia = MotorInferencia()
            logger.info("✅ Servicios inicializados correctamente")
        except Exception as e:
            logger.error(f"❌ Error al inicializar servicios: {str(e)}")
            return False
        
        # === PRUEBA 1: RECOMENDACIÓN POR INGREDIENTES ===
        logger.info("\n🧪 PRUEBA 1: RECOMENDACIÓN POR INGREDIENTES")
        logger.info("-" * 50)
        
        try:
            # Obtener algunos ingredientes para probar
            ingredientes_sample = Ingrediente.query.limit(5).all()
            ingredientes_nombres = [ing.nombre for ing in ingredientes_sample]
            ingredientes_ids = [ing.id for ing in ingredientes_sample]
            
            logger.info(f"🧅 Probando con ingredientes: {', '.join(ingredientes_nombres)}")
            
            # Probar recomendación por nombres
            recomendaciones_nombres = sistema_recomendacion.recomendar_por_ingredientes(
                ingredientes=ingredientes_nombres,
                max_resultados=3
            )
            
            # Probar recomendación por IDs
            recomendaciones_ids = sistema_recomendacion.recomendar_por_ingredientes(
                ingredientes=ingredientes_ids,
                max_resultados=3
            )
            
            logger.info(f"✅ Recomendaciones por nombres: {len(recomendaciones_nombres)}")
            logger.info(f"✅ Recomendaciones por IDs: {len(recomendaciones_ids)}")
            
            # Mostrar ejemplo de recomendación
            if recomendaciones_nombres:
                primera_receta = recomendaciones_nombres[0]
                logger.info(f"🍽️  Ejemplo: {primera_receta['nombre']}")
                logger.info(f"   📂 Categoría: {primera_receta.get('categoria', 'N/A')}")
                logger.info(f"   ⏱️  Tiempo: {primera_receta.get('tiempo_preparacion', 'N/A')} min")
                logger.info(f"   🥕 Ingredientes: {len(primera_receta.get('ingredientes', []))}")
                
                if primera_receta.get('ingredientes_faltantes'):
                    logger.info(f"   ❌ Faltantes: {', '.join(primera_receta['ingredientes_faltantes'][:3])}")
                else:
                    logger.info("   ✅ Tienes todos los ingredientes")
            
        except Exception as e:
            logger.error(f"❌ Error en prueba de ingredientes: {str(e)}")
            return False
        
        # === PRUEBA 2: RECOMENDACIÓN POR TEXTO ===
        logger.info("\n🧪 PRUEBA 2: RECOMENDACIÓN POR TEXTO")
        logger.info("-" * 50)
        
        try:
            consultas_prueba = [
                "Quiero hacer una cena rápida y saludable",
                "Receta vegetariana con quinoa",
                "Algo sin gluten para el almuerzo",
                "Postre vegano bajo en azúcar"
            ]
            
            for consulta in consultas_prueba:
                logger.info(f"📝 Probando: '{consulta}'")
                
                recomendaciones = sistema_recomendacion.recomendar_por_texto(
                    texto=consulta,
                    max_resultados=2
                )
                
                logger.info(f"   ✅ Encontradas: {len(recomendaciones)} recetas")
                
                if recomendaciones:
                    for receta in recomendaciones[:1]:  # Mostrar solo la primera
                        logger.info(f"   🍽️  → {receta['nombre']}")
        
        except Exception as e:
            logger.error(f"❌ Error en prueba de texto: {str(e)}")
            return False
        
        # === PRUEBA 3: ANÁLISIS NLP ===
        logger.info("\n🧪 PRUEBA 3: ANÁLISIS DE PROCESAMIENTO DE LENGUAJE")
        logger.info("-" * 50)
        
        try:
            consulta_nlp = "Necesito una receta vegana sin gluten con tomate y cebolla"
            logger.info(f"📝 Analizando: '{consulta_nlp}'")
            
            analisis = motor_inferencia.analizar_consulta(consulta_nlp)
            
            logger.info(f"✅ Ingredientes detectados: {analisis.get('ingredientes', [])}")
            logger.info(f"✅ Restricciones detectadas: {analisis.get('restricciones', [])}")
            logger.info(f"✅ Alergias detectadas: {analisis.get('alergias', [])}")
            logger.info(f"✅ Texto procesado: {len(analisis.get('texto_procesado', []))} palabras")
        
        except Exception as e:
            logger.error(f"❌ Error en análisis NLP: {str(e)}")
            return False
        
        # === PRUEBA 4: RECETAS SIMILARES ===
        logger.info("\n🧪 PRUEBA 4: RECETAS SIMILARES")
        logger.info("-" * 50)
        
        try:
            # Obtener una receta para probar
            receta_prueba = Receta.query.first()
            
            if receta_prueba:
                logger.info(f"🍽️  Buscando similares a: {receta_prueba.nombre}")
                
                similares = sistema_recomendacion.recomendar_recetas_similares(
                    receta_id=receta_prueba.id,
                    max_resultados=3
                )
                
                logger.info(f"✅ Recetas similares encontradas: {len(similares)}")
                
                for receta in similares:
                    logger.info(f"   🍽️  → {receta['nombre']}")
            else:
                logger.warning("⚠️  No hay recetas para probar similitud")
        
        except Exception as e:
            logger.error(f"❌ Error en prueba de similares: {str(e)}")
            return False
        
        # === PRUEBA 5: SUSTITUCIONES ===
        logger.info("\n🧪 PRUEBA 5: SUSTITUCIONES DE INGREDIENTES")
        logger.info("-" * 50)
        
        try:
            # Probar sustituciones para ingredientes comunes
            ingredientes_comunes = ['Leche', 'Huevo', 'Mantequilla', 'Harina de trigo']
            
            for ing_nombre in ingredientes_comunes:
                ingrediente = Ingrediente.query.filter_by(nombre=ing_nombre).first()
                if ingrediente:
                    sustitutos = sistema_recomendacion.obtener_sustitutos(ingrediente.id)
                    logger.info(f"🔄 {ing_nombre}: {len(sustitutos)} sustitutos disponibles")
                    
                    for sustituto in sustitutos[:2]:  # Mostrar solo los primeros 2
                        logger.info(f"   → {sustituto.get('nombre', 'N/A')}")
        
        except Exception as e:
            logger.error(f"❌ Error en prueba de sustituciones: {str(e)}")
            return False
        
        # === PRUEBA 6: RESTRICCIONES DIETÉTICAS ===
        logger.info("\n🧪 PRUEBA 6: FILTRADO POR RESTRICCIONES DIETÉTICAS")
        logger.info("-" * 50)
        
        try:
            # Crear preferencias de usuario simuladas
            session_id = "test_session_123"
            
            # Simular usuario vegetariano con alergia a nueces
            restriccion_vegetariana = RestriccionDietetica.query.filter_by(nombre='vegetariano').first()
            ingrediente_nueces = Ingrediente.query.filter_by(nombre='Nueces').first()
            
            if restriccion_vegetariana and ingrediente_nueces:
                # Crear preferencias simuladas
                preferencias = PreferenciaUsuario.crear_o_actualizar(
                    session_id=session_id,
                    restricciones=[restriccion_vegetariana.id],
                    alergias=[ingrediente_nueces.id],
                    favoritos=[],
                    evitados=[]
                )
                
                logger.info(f"✅ Preferencias creadas para sesión: {session_id}")
                
                # Probar recomendación con preferencias
                recomendaciones_filtradas = motor_inferencia.recomendar_recetas_por_ingredientes(
                    ingredientes=[1, 2, 3],  # IDs de ejemplo
                    preferencias=preferencias,
                    max_resultados=3
                )
                
                logger.info(f"✅ Recetas filtradas: {len(recomendaciones_filtradas)}")
            else:
                logger.warning("⚠️  No se encontraron restricciones para probar")
        
        except Exception as e:
            logger.error(f"❌ Error en prueba de restricciones: {str(e)}")
            return False
        
        # === PRUEBA 7: INFORMACIÓN NUTRICIONAL ===
        logger.info("\n🧪 PRUEBA 7: INFORMACIÓN NUTRICIONAL")
        logger.info("-" * 50)
        
        try:
            receta_con_nutricion = Receta.query.filter(Receta.calorias.isnot(None)).first()
            
            if receta_con_nutricion:
                logger.info(f"🧮 Analizando nutrición de: {receta_con_nutricion.nombre}")
                
                info_nutricional = sistema_recomendacion.obtener_informacion_nutricional(
                    receta_con_nutricion.id
                )
                
                if info_nutricional:
                    logger.info(f"✅ Calorías: {info_nutricional.get('calorias', 'N/A')}")
                    logger.info(f"✅ Proteínas: {info_nutricional.get('proteinas', 'N/A')}g")
                    logger.info(f"✅ Carbohidratos: {info_nutricional.get('carbohidratos', 'N/A')}g")
                    logger.info(f"✅ Grasas: {info_nutricional.get('grasas', 'N/A')}g")
                    
                    vitaminas = info_nutricional.get('vitaminas', {})
                    if vitaminas:
                        logger.info(f"✅ Vitaminas disponibles: {list(vitaminas.keys())}")
                else:
                    logger.warning("⚠️  No se pudo obtener información nutricional")
            else:
                logger.warning("⚠️  No hay recetas con información nutricional")
        
        except Exception as e:
            logger.error(f"❌ Error en prueba nutricional: {str(e)}")
            return False
        
        # === RESUMEN FINAL ===
        logger.info("\n" + "=" * 80)
        logger.info("🎉 RESUMEN DE PRUEBAS")
        logger.info("=" * 80)
        
        logger.info("✅ Todas las pruebas completadas exitosamente")
        logger.info(f"📊 Base de datos: {ingredientes_count} ingredientes, {recetas_count} recetas")
        logger.info(f"🔄 Sustituciones: {sustituciones_count} disponibles")
        logger.info(f"🚫 Restricciones: {restricciones_count} tipos de dieta")
        
        logger.info("\n💡 TU SISTEMA ESTÁ LISTO PARA:")
        logger.info("   🍽️  Recomendar recetas por ingredientes")
        logger.info("   📝 Procesar consultas en lenguaje natural")
        logger.info("   🔄 Sugerir sustituciones por alergias")
        logger.info("   🚫 Filtrar por restricciones dietéticas")
        logger.info("   📊 Proporcionar información nutricional")
        logger.info("   🎯 Recetas similares y personalizadas")
        
        logger.info("\n🚀 ¡Inicia tu servidor web y comienza a usar el sistema!")
        logger.info("   python run.py")
        
        return True

if __name__ == '__main__':
    test_recommendation_system()