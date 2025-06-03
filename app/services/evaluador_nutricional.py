# app/services/evaluador_nutricional.py
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

from app import db
from app.models.receta import Receta, ValorNutricional
from app.models.ingrediente import Ingrediente

logger = logging.getLogger(__name__)

class EvaluadorNutricional:
    """
    Sistema avanzado de evaluación nutricional para recomendaciones personalizadas
    """
    
    def __init__(self):
        # Valores diarios recomendados (adulto promedio)
        self.vdr_base = {
            'calorias': 2000,
            'proteinas': 50,  # gramos
            'carbohidratos': 300,  # gramos
            'grasas': 65,  # gramos
            'fibra': 25,  # gramos
            'azucar': 50,  # gramos max
            'sodio': 2300,  # mg max
            'vitamina_a': 900,  # μg
            'vitamina_c': 90,  # mg
            'vitamina_d': 15,  # μg
            'vitamina_e': 15,  # mg
            'calcio': 1000,  # mg
            'hierro': 8,  # mg
            'potasio': 3500  # mg
        }
        
        # Perfiles nutricionales por objetivo
        self.perfiles_objetivos = {
            'perdida_peso': {
                'calorias_factor': 0.8,  # 20% menos calorías
                'proteinas_factor': 1.2,  # 20% más proteínas
                'carbohidratos_factor': 0.7,  # 30% menos carbohidratos
                'grasas_factor': 0.9,  # 10% menos grasas
                'fibra_factor': 1.3  # 30% más fibra
            },
            'ganancia_muscular': {
                'calorias_factor': 1.2,  # 20% más calorías
                'proteinas_factor': 1.5,  # 50% más proteínas
                'carbohidratos_factor': 1.3,  # 30% más carbohidratos
                'grasas_factor': 1.0,  # Igual grasas
                'fibra_factor': 1.1  # 10% más fibra
            },
            'mantenimiento': {
                'calorias_factor': 1.0,
                'proteinas_factor': 1.0,
                'carbohidratos_factor': 1.0,
                'grasas_factor': 1.0,
                'fibra_factor': 1.0
            },
            'salud_cardiovascular': {
                'calorias_factor': 0.9,  # 10% menos calorías
                'proteinas_factor': 1.0,
                'carbohidratos_factor': 1.1,  # 10% más carbohidratos complejos
                'grasas_factor': 0.8,  # 20% menos grasas
                'fibra_factor': 1.4,  # 40% más fibra
                'sodio_factor': 0.6  # 40% menos sodio
            },
            'diabetes': {
                'calorias_factor': 0.9,
                'proteinas_factor': 1.2,
                'carbohidratos_factor': 0.6,  # 40% menos carbohidratos
                'grasas_factor': 1.0,
                'fibra_factor': 1.5,  # 50% más fibra
                'azucar_factor': 0.3  # 70% menos azúcar
            }
        }
        
        # Factores de ajuste por edad y género
        self.factores_demograficos = {
            'edad': {
                (18, 30): 1.0,
                (31, 50): 0.95,
                (51, 70): 0.90,
                (71, 100): 0.85
            },
            'genero': {
                'masculino': 1.2,
                'femenino': 0.8,
                'otro': 1.0
            },
            'actividad': {
                'sedentario': 0.9,
                'ligero': 1.0,
                'moderado': 1.2,
                'intenso': 1.4,
                'muy_intenso': 1.6
            }
        }
    
    def calcular_vdr_personalizado(self, 
                                  edad: int = 30,
                                  genero: str = 'otro',
                                  nivel_actividad: str = 'moderado',
                                  objetivo: str = 'mantenimiento',
                                  peso: Optional[float] = None,
                                  altura: Optional[float] = None) -> Dict[str, float]:
        """
        Calcula valores diarios recomendados personalizados
        """
        vdr_personalizado = self.vdr_base.copy()
        
        # Factor por edad
        factor_edad = 1.0
        for rango_edad, factor in self.factores_demograficos['edad'].items():
            if rango_edad[0] <= edad <= rango_edad[1]:
                factor_edad = factor
                break
        
        # Factor por género
        factor_genero = self.factores_demograficos['genero'].get(genero, 1.0)
        
        # Factor por actividad
        factor_actividad = self.factores_demograficos['actividad'].get(nivel_actividad, 1.0)
        
        # Factor combinado demográfico
        factor_demografico = factor_edad * factor_genero * factor_actividad
        
        # Aplicar factores demográficos
        for nutriente in ['calorias', 'proteinas', 'carbohidratos', 'grasas']:
            vdr_personalizado[nutriente] *= factor_demografico
        
        # Aplicar perfil de objetivo
        if objetivo in self.perfiles_objetivos:
            perfil = self.perfiles_objetivos[objetivo]
            for nutriente, factor in perfil.items():
                nutriente_key = nutriente.replace('_factor', '')
                if nutriente_key in vdr_personalizado:
                    vdr_personalizado[nutriente_key] *= factor
        
        # Ajustes específicos por peso si está disponible
        if peso and objetivo == 'ganancia_muscular':
            # Proteínas: 1.6-2.2g por kg de peso corporal
            vdr_personalizado['proteinas'] = max(vdr_personalizado['proteinas'], peso * 1.8)
        elif peso and objetivo == 'perdida_peso':
            # Proteínas: 1.2-1.6g por kg de peso corporal
            vdr_personalizado['proteinas'] = max(vdr_personalizado['proteinas'], peso * 1.4)
        
        return vdr_personalizado
    
    def evaluar_receta_nutricional(self, 
                                  receta: Receta, 
                                  vdr_personalizado: Optional[Dict] = None,
                                  porciones_objetivo: int = 1) -> Dict:
        """
        Evalúa una receta desde el punto de vista nutricional
        """
        if vdr_personalizado is None:
            vdr_personalizado = self.vdr_base
        
        # Escalar nutrientes por porciones
        factor_porciones = porciones_objetivo / (receta.porciones or 1)
        
        nutrientes_receta = {
            'calorias': (receta.calorias or 0) * factor_porciones,
            'proteinas': (receta.proteinas or 0) * factor_porciones,
            'carbohidratos': (receta.carbohidratos or 0) * factor_porciones,
            'grasas': (receta.grasas or 0) * factor_porciones
        }
        
        # Agregar micronutrientes si están disponibles
        if receta.valor_nutricional:
            vn = receta.valor_nutricional
            nutrientes_receta.update({
                'vitamina_a': (vn.vitamina_a or 0) * factor_porciones,
                'vitamina_c': (vn.vitamina_c or 0) * factor_porciones,
                'vitamina_d': (vn.vitamina_d or 0) * factor_porciones,
                'vitamina_e': (vn.vitamina_e or 0) * factor_porciones,
                'calcio': (vn.calcio or 0) * factor_porciones,
                'hierro': (vn.hierro or 0) * factor_porciones,
                'potasio': (vn.potasio or 0) * factor_porciones
            })
        
        # Calcular porcentajes de VDR
        porcentajes_vdr = {}
        for nutriente, valor in nutrientes_receta.items():
            if nutriente in vdr_personalizado and vdr_personalizado[nutriente] > 0:
                porcentajes_vdr[nutriente] = (valor / vdr_personalizado[nutriente]) * 100
        
        # Calcular score nutricional general
        score_nutricional = self._calcular_score_nutricional(nutrientes_receta, vdr_personalizado)
        
        # Identificar fortalezas y debilidades
        fortalezas = []
        debilidades = []
        
        for nutriente, porcentaje in porcentajes_vdr.items():
            if porcentaje >= 25:  # Aporta al menos 25% del VDR
                fortalezas.append(f"Excelente fuente de {nutriente}")
            elif porcentaje >= 10:  # Aporta al menos 10% del VDR
                fortalezas.append(f"Buena fuente de {nutriente}")
            elif porcentaje < 5 and nutriente in ['proteinas', 'vitamina_c', 'calcio', 'hierro']:
                debilidades.append(f"Bajo en {nutriente}")
        
        # Evaluación de balance macronutrientes
        balance_macro = self._evaluar_balance_macronutrientes(nutrientes_receta)
        
        return {
            'nutrientes': nutrientes_receta,
            'porcentajes_vdr': porcentajes_vdr,
            'score_nutricional': score_nutricional,
            'fortalezas': fortalezas,
            'debilidades': debilidades,
            'balance_macronutrientes': balance_macro,
            'recomendacion_porciones': porciones_objetivo,
            'calorias_por_porcion': nutrientes_receta['calorias'] / porciones_objetivo if porciones_objetivo > 0 else 0
        }
    
    def _calcular_score_nutricional(self, nutrientes: Dict, vdr: Dict) -> float:
        """
        Calcula un score nutricional general (0-1)
        """
        scores = []
        
        # Score por macronutrientes (peso mayor)
        for macro in ['proteinas', 'carbohidratos', 'grasas']:
            if macro in nutrientes and macro in vdr:
                porcentaje = (nutrientes[macro] / vdr[macro]) * 100
                # Score óptimo entre 15-35% del VDR por comida
                if 15 <= porcentaje <= 35:
                    scores.append(1.0)
                elif 10 <= porcentaje <= 45:
                    scores.append(0.8)
                elif 5 <= porcentaje <= 60:
                    scores.append(0.6)
                else:
                    scores.append(0.3)
        
        # Score por micronutrientes (peso menor)
        micronutrientes = ['vitamina_a', 'vitamina_c', 'calcio', 'hierro']
        for micro in micronutrientes:
            if micro in nutrientes and micro in vdr:
                porcentaje = (nutrientes[micro] / vdr[micro]) * 100
                if porcentaje >= 20:
                    scores.append(0.8)
                elif porcentaje >= 10:
                    scores.append(0.6)
                elif porcentaje >= 5:
                    scores.append(0.4)
                else:
                    scores.append(0.2)
        
        # Score por calorías
        if 'calorias' in nutrientes and 'calorias' in vdr:
            porcentaje_cal = (nutrientes['calorias'] / vdr['calorias']) * 100
            # Para una comida, 20-35% de calorías diarias es apropiado
            if 20 <= porcentaje_cal <= 35:
                scores.append(1.0)
            elif 15 <= porcentaje_cal <= 45:
                scores.append(0.8)
            elif 10 <= porcentaje_cal <= 60:
                scores.append(0.6)
            else:
                scores.append(0.3)
        
        return np.mean(scores) if scores else 0.5
    
    def _evaluar_balance_macronutrientes(self, nutrientes: Dict) -> Dict:
        """
        Evalúa el balance de macronutrientes
        """
        calorias_proteinas = nutrientes.get('proteinas', 0) * 4
        calorias_carbohidratos = nutrientes.get('carbohidratos', 0) * 4
        calorias_grasas = nutrientes.get('grasas', 0) * 9
        
        total_macro_calorias = calorias_proteinas + calorias_carbohidratos + calorias_grasas
        
        if total_macro_calorias == 0:
            return {
                'proporcion_proteinas': 0,
                'proporcion_carbohidratos': 0,
                'proporcion_grasas': 0,
                'balance_score': 0,
                'recomendacion': 'No hay información nutricional suficiente'
            }
        
        prop_proteinas = calorias_proteinas / total_macro_calorias
        prop_carbohidratos = calorias_carbohidratos / total_macro_calorias
        prop_grasas = calorias_grasas / total_macro_calorias
        
        # Rangos ideales
        ideal_proteinas = (0.15, 0.35)
        ideal_carbohidratos = (0.35, 0.65)
        ideal_grasas = (0.15, 0.35)
        
        # Calcular score de balance
        score_proteinas = 1.0 if ideal_proteinas[0] <= prop_proteinas <= ideal_proteinas[1] else 0.5
        score_carbohidratos = 1.0 if ideal_carbohidratos[0] <= prop_carbohidratos <= ideal_carbohidratos[1] else 0.5
        score_grasas = 1.0 if ideal_grasas[0] <= prop_grasas <= ideal_grasas[1] else 0.5
        
        balance_score = (score_proteinas + score_carbohidratos + score_grasas) / 3
        
        # Generar recomendación
        recomendacion = ""
        if prop_proteinas < 0.15:
            recomendacion += "Considera agregar más proteínas. "
        elif prop_proteinas > 0.35:
            recomendacion += "Alto contenido de proteínas, ideal para deportistas. "
        
        if prop_carbohidratos < 0.35:
            recomendacion += "Bajo en carbohidratos, ideal para dietas keto. "
        elif prop_carbohidratos > 0.65:
            recomendacion += "Alto en carbohidratos, asegúrate de que sean complejos. "
        
        if prop_grasas > 0.35:
            recomendacion += "Alto contenido de grasas, verifica que sean saludables. "
        
        if not recomendacion:
            recomendacion = "Balance macronutrientes adecuado."
        
        return {
            'proporcion_proteinas': prop_proteinas,
            'proporcion_carbohidratos': prop_carbohidratos,
            'proporcion_grasas': prop_grasas,
            'balance_score': balance_score,
            'recomendacion': recomendacion.strip()
        }
    
    def planificar_menu_diario(self, 
                              recetas_disponibles: List[Receta],
                              vdr_personalizado: Optional[Dict] = None,
                              numero_comidas: int = 3) -> Dict:
        """
        Planifica un menú diario balanceado
        """
        if vdr_personalizado is None:
            vdr_personalizado = self.vdr_base
        
        # Distribución típica de calorías por comida
        distribucion_calorias = {
            3: [0.3, 0.4, 0.3],  # Desayuno, Almuerzo, Cena
            4: [0.25, 0.1, 0.35, 0.3],  # Desayuno, Snack, Almuerzo, Cena
            5: [0.2, 0.1, 0.3, 0.1, 0.3]  # Desayuno, Snack AM, Almuerzo, Snack PM, Cena
        }
        
        calorias_objetivo = vdr_personalizado['calorias']
        dist_cal = distribucion_calorias.get(numero_comidas, [1.0/numero_comidas] * numero_comidas)
        
        menu_planificado = []
        nutrientes_acumulados = {k: 0 for k in vdr_personalizado.keys()}
        
        for i in range(numero_comidas):
            calorias_comida = calorias_objetivo * dist_cal[i]
            
            # Buscar la mejor receta para esta comida
            mejor_receta = None
            mejor_score = -1
            
            for receta in recetas_disponibles:
                if receta.calorias and receta.calorias > 0:
                    # Calcular porciones necesarias para alcanzar calorías objetivo
                    porciones_necesarias = calorias_comida / (receta.calorias / (receta.porciones or 1))
                    
                    # Evaluar la receta para esta comida
                    evaluacion = self.evaluar_receta_nutricional(
                        receta, 
                        vdr_personalizado, 
                        max(1, int(porciones_necesarias))
                    )
                    
                    # Score basado en cercanía a calorías objetivo y calidad nutricional
                    diff_calorias = abs(evaluacion['calorias_por_porcion'] * porciones_necesarias - calorias_comida)
                    score_calorias = max(0, 1 - (diff_calorias / calorias_comida))
                    score_total = 0.6 * score_calorias + 0.4 * evaluacion['score_nutricional']
                    
                    if score_total > mejor_score:
                        mejor_score = score_total
                        mejor_receta = (receta, porciones_necesarias, evaluacion)
            
            if mejor_receta:
                receta, porciones, evaluacion = mejor_receta
                
                menu_planificado.append({
                    'comida': f"Comida {i+1}",
                    'receta': receta.to_dict(),
                    'porciones_recomendadas': porciones,
                    'evaluacion_nutricional': evaluacion
                })
                
                # Acumular nutrientes
                for nutriente, valor in evaluacion['nutrientes'].items():
                    if nutriente in nutrientes_acumulados:
                        nutrientes_acumulados[nutriente] += valor
        
        # Evaluar el menú completo
        evaluacion_diaria = self._evaluar_menu_diario(nutrientes_acumulados, vdr_personalizado)
        
        return {
            'menu_planificado': menu_planificado,
            'nutrientes_totales': nutrientes_acumulados,
            'evaluacion_diaria': evaluacion_diaria,
            'cumplimiento_vdr': {
                nutriente: (valor / vdr_personalizado[nutriente]) * 100
                for nutriente, valor in nutrientes_acumulados.items()
                if nutriente in vdr_personalizado and vdr_personalizado[nutriente] > 0
            }
        }
    
    def _evaluar_menu_diario(self, nutrientes_totales: Dict, vdr: Dict) -> Dict:
        """
        Evalúa un menú diario completo
        """
        cumplimientos = {}
        deficiencias = []
        excesos = []
        
        for nutriente, valor_total in nutrientes_totales.items():
            if nutriente in vdr and vdr[nutriente] > 0:
                porcentaje = (valor_total / vdr[nutriente]) * 100
                cumplimientos[nutriente] = porcentaje
                
                if porcentaje < 70:
                    deficiencias.append(f"{nutriente}: {porcentaje:.1f}% del VDR")
                elif porcentaje > 150 and nutriente in ['sodio', 'azucar', 'grasas']:
                    excesos.append(f"{nutriente}: {porcentaje:.1f}% del VDR")
        
        # Score general del menú
        scores_individuales = []
        for nutriente in ['calorias', 'proteinas', 'carbohidratos', 'grasas']:
            if nutriente in cumplimientos:
                porcentaje = cumplimientos[nutriente]
                if 80 <= porcentaje <= 120:
                    scores_individuales.append(1.0)
                elif 70 <= porcentaje <= 140:
                    scores_individuales.append(0.8)
                elif 60 <= porcentaje <= 160:
                    scores_individuales.append(0.6)
                else:
                    scores_individuales.append(0.3)
        
        score_menu = np.mean(scores_individuales) if scores_individuales else 0.5
        
        # Generar recomendaciones
        recomendaciones = []
        if deficiencias:
            recomendaciones.append(f"Considera agregar alimentos ricos en: {', '.join([d.split(':')[0] for d in deficiencias])}")
        
        if excesos:
            recomendaciones.append(f"Modera el consumo de: {', '.join([e.split(':')[0] for e in excesos])}")
        
        if score_menu >= 0.8:
            recomendaciones.append("¡Excelente planificación nutricional!")
        elif score_menu >= 0.6:
            recomendaciones.append("Buena planificación con algunas áreas de mejora")
        else:
            recomendaciones.append("El menú necesita mejoras nutricionales significativas")
        
        return {
            'score_general': score_menu,
            'deficiencias': deficiencias,
            'excesos': excesos,
            'recomendaciones': recomendaciones,
            'cumplimiento_macronutrientes': {
                'proteinas': cumplimientos.get('proteinas', 0),
                'carbohidratos': cumplimientos.get('carbohidratos', 0),
                'grasas': cumplimientos.get('grasas', 0)
            }
        }
    
    def sugerir_mejoras_nutricionales(self, 
                                    receta: Receta,
                                    objetivo_nutricional: str = 'mantenimiento') -> List[str]:
        """
        Sugiere mejoras nutricionales específicas para una receta
        """
        sugerencias = []
        
        evaluacion = self.evaluar_receta_nutricional(receta)
        balance = evaluacion['balance_macronutrientes']
        
        # Sugerencias basadas en el objetivo
        if objetivo_nutricional == 'perdida_peso':
            if evaluacion['calorias_por_porcion'] > 500:
                sugerencias.append("Reduce las porciones o sustituye ingredientes altos en calorías")
            
            if balance['proporcion_proteinas'] < 0.25:
                sugerencias.append("Agrega más proteínas magras para mayor saciedad")
            
            if balance['proporcion_grasas'] > 0.3:
                sugerencias.append("Reduce las grasas usando métodos de cocción más saludables")
        
        elif objetivo_nutricional == 'ganancia_muscular':
            if balance['proporcion_proteinas'] < 0.3:
                sugerencias.append("Incrementa el contenido de proteínas agregando carnes magras, huevos o legumbres")
            
            if evaluacion['calorias_por_porcion'] < 400:
                sugerencias.append("Aumenta las calorías con carbohidratos complejos y grasas saludables")
        
        elif objetivo_nutricional == 'salud_cardiovascular':
            if balance['proporcion_grasas'] > 0.3:
                sugerencias.append("Sustituye grasas saturadas por aceites vegetales y aguacate")
            
            sugerencias.append("Agrega más vegetales ricos en fibra y antioxidantes")
            sugerencias.append("Reduce el sodio usando hierbas y especias para saborizar")
        
        # Sugerencias generales basadas en deficiencias
        for debilidad in evaluacion['debilidades']:
            if 'proteinas' in debilidad:
                sugerencias.append("Considera agregar: huevos, pescado, legumbres o frutos secos")
            elif 'vitamina_c' in debilidad:
                sugerencias.append("Añade: pimientos, cítricos, brócoli o fresas")
            elif 'calcio' in debilidad:
                sugerencias.append("Incluye: productos lácteos, vegetales de hoja verde o almendras")
            elif 'hierro' in debilidad:
                sugerencias.append("Agrega: carnes rojas magras, espinacas o legumbres")
        
        return sugerencias[:5]  # Limitar a 5 sugerencias máximo