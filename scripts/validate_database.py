#!/usr/bin/env python3
# scripts/validate_database.py

import os
import sys
import logging
from collections import defaultdict, Counter

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.ingrediente import Ingrediente
from app.models.receta import (Receta, RecetaIngrediente, PasoPreparacion, 
                              ValorNutricional, RestriccionDietetica, 
                              Sustitucion, receta_restricciones)

def validate_database():
    """
    Valida la integridad y completitud de la base de datos
    """
    app = create_app()

    with app.app_context():
        logger.info("🔍 Iniciando validación de la base de datos")
        logger.info("=" * 80)
        
        # === ESTADÍSTICAS GENERALES ===
        logger.info("📊 ESTADÍSTICAS GENERALES")
        logger.info("=" * 80)
        
        ingredientes_count = Ingrediente.query.count()
        recetas_count = Receta.query.count()
        restricciones_count = RestriccionDietetica.query.count()
        sustituciones_count = Sustitucion.query.count()
        pasos_count = PasoPreparacion.query.count()
        valores_nutricionales_count = ValorNutricional.query.count()
        
        logger.info(f"🥕 Total de ingredientes: {ingredientes_count}")
        logger.info(f"🍽️  Total de recetas: {recetas_count}")
        logger.info(f"🚫 Total de restricciones dietéticas: {restricciones_count}")
        logger.info(f"🔄 Total de sustituciones: {sustituciones_count}")
        logger.info(f"📝 Total de pasos de preparación: {pasos_count}")
        logger.info(f"🧮 Total de valores nutricionales: {valores_nutricionales_count}")
        
        # === ANÁLISIS DE INGREDIENTES ===
        logger.info("\n" + "=" * 80)
        logger.info("🥕 ANÁLISIS DE INGREDIENTES")
        logger.info("=" * 80)
        
        ingredientes = Ingrediente.query.all()
        categorias_ingredientes = Counter([ing.categoria for ing in ingredientes if ing.categoria])
        alergenos = [ing for ing in ingredientes if ing.es_alergeno]
        con_gluten = [ing for ing in ingredientes if ing.contiene_gluten]
        
        logger.info("📈 Ingredientes por categoría:")
        for categoria, count in categorias_ingredientes.most_common():
            logger.info(f"  • {categoria}: {count} ingredientes")
        
        logger.info(f"\n⚠️  Ingredientes alérgenos: {len(alergenos)}")
        for alergeno in alergenos[:10]:  # Mostrar solo los primeros 10
            logger.info(f"  • {alergeno.nombre}")
        if len(alergenos) > 10:
            logger.info(f"  ... y {len(alergenos) - 10} más")
        
        logger.info(f"\n🌾 Ingredientes con gluten: {len(con_gluten)}")
        for gluten in con_gluten:
            logger.info(f"  • {gluten.nombre}")
        
        # === ANÁLISIS DE RECETAS ===
        logger.info("\n" + "=" * 80)
        logger.info("🍽️  ANÁLISIS DE RECETAS")
        logger.info("=" * 80)
        
        recetas = Receta.query.all()
        categorias_recetas = Counter([rec.categoria for rec in recetas if rec.categoria])
        dificultades = Counter([rec.dificultad for rec in recetas if rec.dificultad])
        
        logger.info("📈 Recetas por categoría:")
        for categoria, count in categorias_recetas.most_common():
            logger.info(f"  • {categoria}: {count} recetas")
        
        logger.info("\n📈 Recetas por dificultad:")
        for dificultad, count in dificultades.most_common():
            logger.info(f"  • {dificultad}: {count} recetas")
        
        # Análisis de tiempos de preparación
        tiempos = [rec.tiempo_preparacion for rec in recetas if rec.tiempo_preparacion]
        if tiempos:
            tiempo_promedio = sum(tiempos) / len(tiempos)
            tiempo_min = min(tiempos)
            tiempo_max = max(tiempos)
            
            logger.info(f"\n⏱️  Tiempos de preparación:")
            logger.info(f"  • Promedio: {tiempo_promedio:.1f} minutos")
            logger.info(f"  • Mínimo: {tiempo_min} minutos")
            logger.info(f"  • Máximo: {tiempo_max} minutos")
        
        # === VALIDACIÓN DE INTEGRIDAD ===
        logger.info("\n" + "=" * 80)
        logger.info("🔍 VALIDACIÓN DE INTEGRIDAD")
        logger.info("=" * 80)
        
        # Recetas sin ingredientes
        recetas_sin_ingredientes = []
        for receta in recetas:
            if not receta.ingredientes:
                recetas_sin_ingredientes.append(receta.nombre)
        
        if recetas_sin_ingredientes:
            logger.warning(f"⚠️  Recetas sin ingredientes ({len(recetas_sin_ingredientes)}):")
            for nombre in recetas_sin_ingredientes:
                logger.warning(f"  • {nombre}")
        else:
            logger.info("✅ Todas las recetas tienen ingredientes")
        
        # Recetas sin pasos
        recetas_sin_pasos = []
        for receta in recetas:
            if not receta.pasos:
                recetas_sin_pasos.append(receta.nombre)
        
        if recetas_sin_pasos:
            logger.warning(f"⚠️  Recetas sin pasos de preparación ({len(recetas_sin_pasos)}):")
            for nombre in recetas_sin_pasos:
                logger.warning(f"  • {nombre}")
        else:
            logger.info("✅ Todas las recetas tienen pasos de preparación")
        
        # Recetas sin valor nutricional
        recetas_sin_nutricion = []
        for receta in recetas:
            if not receta.valor_nutricional:
                recetas_sin_nutricion.append(receta.nombre)
        
        if recetas_sin_nutricion:
            logger.warning(f"⚠️  Recetas sin valor nutricional ({len(recetas_sin_nutricion)}):")
            for nombre in recetas_sin_nutricion[:10]:  # Mostrar solo las primeras 10
                logger.warning(f"  • {nombre}")
            if len(recetas_sin_nutricion) > 10:
                logger.warning(f"  ... y {len(recetas_sin_nutricion) - 10} más")
        else:
            logger.info("✅ Todas las recetas tienen valor nutricional")
        
        # === ANÁLISIS DE RESTRICCIONES DIETÉTICAS ===
        logger.info("\n" + "=" * 80)
        logger.info("🚫 ANÁLISIS DE RESTRICCIONES DIETÉTICAS")
        logger.info("=" * 80)
        
        restricciones = RestriccionDietetica.query.all()
        
        # Contar recetas por restricción
        restricciones_recetas = {}
        for restriccion in restricciones:
            query = db.session.query(Receta).join(
                receta_restricciones, Receta.id == receta_restricciones.c.receta_id
            ).filter(receta_restricciones.c.restriccion_id == restriccion.id)
            
            count = query.count()
            restricciones_recetas[restriccion.nombre] = count
        
        logger.info("📈 Recetas por restricción dietética:")
        for restriccion, count in sorted(restricciones_recetas.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  • {restriccion}: {count} recetas")
        
        # === ANÁLISIS DE SUSTITUCIONES ===
        logger.info("\n" + "=" * 80)
        logger.info("🔄 ANÁLISIS DE SUSTITUCIONES")
        logger.info("=" * 80)
        
        sustituciones = Sustitucion.query.all()
        tipos_sustitucion = Counter([sust.tipo_sustitucion for sust in sustituciones if sust.tipo_sustitucion])
        
        logger.info("📈 Sustituciones por tipo:")
        for tipo, count in tipos_sustitucion.most_common():
            logger.info(f"  • {tipo}: {count} sustituciones")
        
        # Ingredientes más sustituidos
        ingredientes_originales = Counter([sust.ingrediente_original_id for sust in sustituciones])
        logger.info(f"\n🔄 Ingredientes más sustituidos:")
        
        for ing_id, count in ingredientes_originales.most_common(10):
            ingrediente = Ingrediente.query.get(ing_id)
            if ingrediente:
                logger.info(f"  • {ingrediente.nombre}: {count} sustitutos")
        
        # === RECOMENDACIONES DE MEJORA ===
        logger.info("\n" + "=" * 80)
        logger.info("💡 RECOMENDACIONES DE MEJORA")
        logger.info("=" * 80)
        
        recomendaciones = []
        
        if recetas_count < 50:
            recomendaciones.append("Agregar más recetas para mejorar las recomendaciones")
        
        if len(categorias_recetas) < 8:
            recomendaciones.append("Diversificar las categorías de recetas")
        
        if sustituciones_count < 30:
            recomendaciones.append("Agregar más sustituciones de ingredientes")
        
        if len([r for r in restricciones_recetas.values() if r == 0]) > 0:
            recomendaciones.append("Algunas restricciones dietéticas no tienen recetas asociadas")
        
        # Verificar balance nutricional
        recetas_con_calorias = [r for r in recetas if r.calorias and r.calorias > 0]
        if len(recetas_con_calorias) < recetas_count * 0.8:
            recomendaciones.append("Completar información calórica de las recetas")
        
        if recomendaciones:
            for i, rec in enumerate(recomendaciones, 1):
                logger.info(f"{i}. {rec}")
        else:
            logger.info("✅ La base de datos está bien estructurada!")
        
        # === EJEMPLOS DE RECETAS COMPLETAS ===
        logger.info("\n" + "=" * 80)
        logger.info("🏆 EJEMPLOS DE RECETAS COMPLETAS")
        logger.info("=" * 80)
        
        recetas_completas = []
        for receta in recetas:
            if (receta.ingredientes and receta.pasos and receta.valor_nutricional 
                and receta.calorias and len(receta.ingredientes) >= 3):
                recetas_completas.append(receta)
        
        logger.info(f"📊 Recetas completas: {len(recetas_completas)} de {recetas_count}")
        
        for receta in recetas_completas[:3]:  # Mostrar 3 ejemplos
            logger.info(f"\n🍽️  {receta.nombre}")
            logger.info(f"   📂 {receta.categoria} | ⏱️  {receta.tiempo_preparacion} min | 👥 {receta.porciones} porciones")
            logger.info(f"   🔥 {receta.calorias} kcal | 🥩 {receta.proteinas}g prot | 🍞 {receta.carbohidratos}g carb")
            
            ingredientes_lista = [f"{ri.ingrediente.nombre} ({ri.cantidad} {ri.unidad})" 
                                for ri in receta.ingredientes[:4]]
            if len(receta.ingredientes) > 4:
                ingredientes_lista.append(f"... y {len(receta.ingredientes) - 4} más")
            
            logger.info(f"   🥕 Ingredientes: {', '.join(ingredientes_lista)}")
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ VALIDACIÓN COMPLETADA")
        logger.info("=" * 80)
        
        return {
            'ingredientes': ingredientes_count,
            'recetas': recetas_count,
            'restricciones': restricciones_count,
            'sustituciones': sustituciones_count,
            'recetas_completas': len(recetas_completas),
            'recomendaciones': recomendaciones
        }

if __name__ == '__main__':
    validate_database()