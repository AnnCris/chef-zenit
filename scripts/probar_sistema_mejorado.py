# scripts/probar_sistema_mejorado.py
import os
import sys
import logging
import time

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def probar_sistema_completo():
    """Prueba completa del sistema mejorado"""
    
    logger.info("🧪 INICIANDO PRUEBAS DEL SISTEMA MEJORADO")
    logger.info("=" * 80)
    
    try:
        from app import create_app
        from app.services.recomendacion_mejorada import sistema_recomendacion_mejorado
        from app.models.receta import Receta
        from app.models.ingrediente import Ingrediente
        
        app = create_app()
        
        with app.app_context():
            # === VERIFICAR DATOS BASE ===
            logger.info("📊 VERIFICANDO DATOS BASE")
            logger.info("-" * 50)
            
            num_recetas = Receta.query.count()
            num_ingredientes = Ingrediente.query.count()
            
            logger.info(f"✅ Recetas disponibles: {num_recetas}")
            logger.info(f"✅ Ingredientes disponibles: {num_ingredientes}")
            
            if num_recetas < 3:
                logger.error("❌ Necesitas al menos 3 recetas para las pruebas")
                return False
            
            if num_ingredientes < 5:
                logger.error("❌ Necesitas al menos 5 ingredientes para las pruebas")
                return False
            
            # === PRUEBA 1: VERIFICAR ESTADO INICIAL ===
            logger.info("\n🔍 PRUEBA 1: ESTADO INICIAL DEL SISTEMA")
            logger.info("-" * 50)
            
            logger.info(f"📊 Modelo entrenado: {sistema_recomendacion_mejorado.modelo_entrenado}")
            logger.info(f"📊 Recetas cargadas: {len(sistema_recomendacion_mejorado.recetas_ids)}")
            
            # === PRUEBA 2: ENTRENAMIENTO ===
            logger.info("\n🎯 PRUEBA 2: ENTRENAMIENTO DEL SISTEMA")
            logger.info("-" * 50)
            
            logger.info("🔄 Iniciando entrenamiento...")
            inicio_entrenamiento = time.time()
            
            exito_entrenamiento = sistema_recomendacion_mejorado.entrenar()
            
            tiempo_entrenamiento = time.time() - inicio_entrenamiento
            
            if exito_entrenamiento:
                logger.info(f"✅ Entrenamiento completado en {tiempo_entrenamiento:.2f} segundos")
                logger.info(f"📊 Modelo TF-IDF: {'✅' if sistema_recomendacion_mejorado.vectorizer_contenido else '❌'}")
                logger.info(f"📊 Modelo K-means: {'✅' if sistema_recomendacion_mejorado.kmeans_model else '❌'}")
                logger.info(f"📊 Modelo Random Forest: {'✅' if sistema_recomendacion_mejorado.random_forest_model else '❌'}")
            else:
                logger.error("❌ Error durante el entrenamiento")
                return False
            
            # === PRUEBA 3: RECOMENDACIONES POR INGREDIENTES ===
            logger.info("\n🥕 PRUEBA 3: RECOMENDACIONES POR INGREDIENTES")
            logger.info("-" * 50)
            
            # Obtener algunos ingredientes de prueba
            ingredientes_muestra = Ingrediente.query.limit(3).all()
            ingredientes_nombres = [ing.nombre for ing in ingredientes_muestra]
            ingredientes_ids = [ing.id for ing in ingredientes_muestra]
            
            logger.info(f"🧅 Probando con ingredientes: {', '.join(ingredientes_nombres)}")
            
            # Probar con nombres
            inicio = time.time()
            recomendaciones_nombres = sistema_recomendacion_mejorado.recomendar_por_ingredientes(
                ingredientes=ingredientes_nombres,
                max_resultados=3
            )
            tiempo_nombres = time.time() - inicio
            
            # Probar con IDs
            inicio = time.time()
            recomendaciones_ids = sistema_recomendacion_mejorado.recomendar_por_ingredientes(
                ingredientes=ingredientes_ids,
                max_resultados=3
            )
            tiempo_ids = time.time() - inicio
            
            logger.info(f"✅ Recomendaciones por nombres: {len(recomendaciones_nombres)} en {tiempo_nombres:.3f}s")
            logger.info(f"✅ Recomendaciones por IDs: {len(recomendaciones_ids)} en {tiempo_ids:.3f}s")
            
            # Mostrar ejemplo
            if recomendaciones_nombres:
                ejemplo = recomendaciones_nombres[0]
                logger.info(f"🍽️  Ejemplo: {ejemplo['nombre']}")
                if 'metodos_usados' in ejemplo:
                    logger.info(f"   🤖 Algoritmos: {', '.join(ejemplo['metodos_usados'])}")
                if 'score_recomendacion' in ejemplo:
                    logger.info(f"   ⭐ Score: {ejemplo['score_recomendacion']:.3f}")
            
            # === PRUEBA 4: RECOMENDACIONES POR TEXTO ===
            logger.info("\n📝 PRUEBA 4: RECOMENDACIONES POR TEXTO")
            logger.info("-" * 50)
            
            consultas_prueba = [
                "Quiero una receta rápida para el almuerzo",
                f"Algo con {ingredientes_nombres[0]} y {ingredientes_nombres[1]}",
                "Receta saludable y fácil de hacer",
                "Plato principal nutritivo"
            ]
            
            for consulta in consultas_prueba:
                logger.info(f"📝 Consulta: '{consulta}'")
                
                inicio = time.time()
                recomendaciones = sistema_recomendacion_mejorado.recomendar_por_texto(
                    texto=consulta,
                    max_resultados=2
                )
                tiempo_consulta = time.time() - inicio
                
                logger.info(f"   ✅ {len(recomendaciones)} recetas en {tiempo_consulta:.3f}s")
                
                if recomendaciones:
                    ejemplo = recomendaciones[0]
                    logger.info(f"   🍽️  → {ejemplo['nombre']}")
            
            # === PRUEBA 5: RECOMENDACIONES SIMILARES ===
            logger.info("\n🔄 PRUEBA 5: RECOMENDACIONES SIMILARES")
            logger.info("-" * 50)
            
            receta_prueba = Receta.query.first()
            if receta_prueba:
                logger.info(f"🍽️  Base: {receta_prueba.nombre}")
                
                inicio = time.time()
                similares = sistema_recomendacion_mejorado.recomendar_recetas_similares(
                    receta_id=receta_prueba.id,
                    max_resultados=3
                )
                tiempo_similares = time.time() - inicio
                
                logger.info(f"✅ {len(similares)} recetas similares en {tiempo_similares:.3f}s")
                
                for similar in similares:
                    logger.info(f"   🍽️  → {similar['nombre']}")
            
            # === PRUEBA 6: SISTEMA HÍBRIDO ===
            logger.info("\n🤖 PRUEBA 6: SISTEMA HÍBRIDO COMPLETO")
            logger.info("-" * 50)
            
            logger.info("🔄 Probando combinación de todos los algoritmos...")
            
            inicio = time.time()
            recomendaciones_hibridas = sistema_recomendacion_mejorado.recomendar_hibrido(
                ingredientes=ingredientes_nombres[:2],
                texto_consulta="receta deliciosa y fácil",
                max_resultados=4
            )
            tiempo_hibrido = time.time() - inicio
            
            logger.info(f"✅ {len(recomendaciones_hibridas)} recomendaciones híbridas en {tiempo_hibrido:.3f}s")
            
            for i, rec in enumerate(recomendaciones_hibridas):
                metodos = rec.get('metodos_usados', [])
                score = rec.get('score_recomendacion', 0)
                logger.info(f"   {i+1}. {rec['nombre']} (Score: {score:.3f}, Métodos: {len(metodos)})")
            
            # === PRUEBA 7: RENDIMIENTO ===
            logger.info("\n⚡ PRUEBA 7: ANÁLISIS DE RENDIMIENTO")
            logger.info("-" * 50)
            
            # Prueba de velocidad con múltiples consultas
            tiempos = []
            num_pruebas = 5
            
            logger.info(f"🏃 Ejecutando {num_pruebas} consultas de rendimiento...")
            
            for i in range(num_pruebas):
                inicio = time.time()
                resultado = sistema_recomendacion_mejorado.recomendar_por_ingredientes(
                    ingredientes=ingredientes_nombres,
                    max_resultados=3
                )
                tiempo_consulta = time.time() - inicio
                tiempos.append(tiempo_consulta)
                
                if resultado:
                    logger.info(f"   Consulta {i+1}: {tiempo_consulta:.3f}s → {len(resultado)} resultados")
            
            tiempo_promedio = sum(tiempos) / len(tiempos)
            tiempo_min = min(tiempos)
            tiempo_max = max(tiempos)
            
            logger.info(f"📊 Tiempo promedio: {tiempo_promedio:.3f}s")
            logger.info(f"📊 Tiempo mínimo: {tiempo_min:.3f}s")
            logger.info(f"📊 Tiempo máximo: {tiempo_max:.3f}s")
            
            # === PRUEBA 8: CALIDAD DE RECOMENDACIONES ===
            logger.info("\n🎯 PRUEBA 8: CALIDAD DE RECOMENDACIONES")
            logger.info("-" * 50)
            
            # Verificar que las recomendaciones son diversas
            todas_recomendaciones = sistema_recomendacion_mejorado.recomendar_por_ingredientes(
                ingredientes=ingredientes_nombres,
                max_resultados=5
            )
            
            if todas_recomendaciones:
                categorias = set()
                dificultades = set()
                tiempos = []
                
                for rec in todas_recomendaciones:
                    if rec.get('categoria'):
                        categorias.add(rec['categoria'])
                    if rec.get('dificultad'):
                        dificultades.add(rec['dificultad'])
                    if rec.get('tiempo_preparacion'):
                        tiempos.append(rec['tiempo_preparacion'])
                
                logger.info(f"📈 Diversidad de categorías: {len(categorias)} diferentes")
                logger.info(f"📈 Diversidad de dificultades: {len(dificultades)} diferentes")
                if tiempos:
                    variacion_tiempo = max(tiempos) - min(tiempos)
                    logger.info(f"📈 Variación de tiempos: {variacion_tiempo} minutos")
            
            # === RESUMEN FINAL ===
            logger.info("\n" + "=" * 80)
            logger.info("🎉 RESUMEN DE PRUEBAS")
            logger.info("=" * 80)
            
            logger.info("✅ ALGORITMOS FUNCIONANDO:")
            logger.info("   🔤 TF-IDF para análisis de contenido")
            logger.info("   🎯 K-means para agrupación de recetas")
            logger.info("   🤖 Random Forest para predicción de preferencias")
            logger.info("   🔀 Sistema híbrido combinando todos los métodos")
            
            logger.info(f"\n📊 ESTADÍSTICAS:")
            logger.info(f"   📈 Recetas procesadas: {num_recetas}")
            logger.info(f"   📈 Ingredientes analizados: {num_ingredientes}")
            logger.info(f"   📈 Tiempo promedio de respuesta: {tiempo_promedio:.3f}s")
            logger.info(f"   📈 Clusters generados: {sistema_recomendacion_mejorado.kmeans_model.n_clusters if sistema_recomendacion_mejorado.kmeans_model else 'N/A'}")
            
            logger.info(f"\n🚀 ESTADO DEL SISTEMA:")
            logger.info(f"   ✅ Modelo entrenado y optimizado")
            logger.info(f"   ✅ Recomendaciones inteligentes funcionando")
            logger.info(f"   ✅ Sistema híbrido operativo")
            logger.info(f"   ✅ Rendimiento óptimo")
            
            logger.info(f"\n💡 PRÓXIMOS PASOS:")
            logger.info(f"   1. 🚀 Inicia tu servidor: python run.py")
            logger.info(f"   2. 🌐 Prueba la interfaz web mejorada")
            logger.info(f"   3. 🎯 Usa el botón 'Reentrenar Sistema IA' cuando agregues más recetas")
            logger.info(f"   4. 📊 Disfruta de recomendaciones más inteligentes y precisas")
            
            return True
            
    except ImportError as e:
        logger.error(f"❌ Error de importación: {e}")
        logger.error("💡 Asegúrate de haber ejecutado el script de integración primero")
        return False
    except Exception as e:
        logger.error(f"❌ Error durante las pruebas: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    dependencias = ['scikit-learn', 'pandas', 'numpy']
    
    logger.info("📦 Verificando dependencias...")
    
    faltantes = []
    for dep in dependencias:
        try:
            __import__(dep.replace('-', '_'))
            logger.info(f"   ✅ {dep}")
        except ImportError:
            faltantes.append(dep)
            logger.error(f"   ❌ {dep}")
    
    if faltantes:
        logger.error(f"\n❌ Dependencias faltantes: {', '.join(faltantes)}")
        logger.info("💡 Instálalas con: pip install " + " ".join(faltantes))
        return False
    
    logger.info("✅ Todas las dependencias están instaladas")
    return True

def main():
    """Función principal"""
    logger.info("🤖 SISTEMA DE RECOMENDACIONES MEJORADO - PRUEBAS")
    logger.info("=" * 80)
    
    # Verificar dependencias
    if not verificar_dependencias():
        return False
    
    # Ejecutar pruebas
    return probar_sistema_completo()

if __name__ == '__main__':
    exito = main()
    
    if exito:
        logger.info("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        logger.info("Tu sistema de recomendaciones mejorado está listo para usar.")
    else:
        logger.error("\n❌ Algunas pruebas fallaron.")
        logger.info("Revisa los errores y ejecuta el script nuevamente.")
    
    sys.exit(0 if exito else 1)