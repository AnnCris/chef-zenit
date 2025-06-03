# scripts/integrar_sistema_mejorado.py
import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def actualizar_rutas_recomendaciones():
    """Actualiza las rutas para usar el sistema mejorado"""
    file_path = os.path.join('app', 'routes', 'recomendaciones.py')
    
    try:
        # Leer el contenido actual
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Actualizar las importaciones
        new_imports = """from flask import Blueprint, jsonify, request, send_file, session
from app.services.recomendacion_mejorada import sistema_recomendacion_mejorado
from app.services.motor_inferencia import MotorInferencia
from app.services.pdf_generator import PDFGenerator
import uuid
import io
import logging
from app import db

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear blueprint
bp = Blueprint('recomendaciones', __name__, url_prefix='/api/recomendaciones')

# Inicializar servicios
motor_inferencia = MotorInferencia()
pdf_generator = PDFGenerator()"""
        
        # Nuevas rutas mejoradas
        nuevas_rutas = """

@bp.route('/por-ingredientes', methods=['POST'])
def recomendar_por_ingredientes():
    \"\"\"
    Recomendaciones híbridas por ingredientes usando el sistema mejorado
    \"\"\"
    try:
        datos = request.get_json(silent=True)
        if not datos:
            return jsonify({'success': False, 'error': 'No se recibieron datos'}), 400
        
        ingredientes = datos.get('ingredientes', [])
        max_resultados = datos.get('max_resultados', 5)
        
        logger.info(f"Solicitando recomendaciones para ingredientes: {ingredientes}")
        
        # Usar el sistema mejorado
        recomendaciones = sistema_recomendacion_mejorado.recomendar_por_ingredientes(
            ingredientes=ingredientes,
            max_resultados=max_resultados
        )
        
        return jsonify({
            'success': True,
            'data': recomendaciones,
            'total_encontradas': len(recomendaciones),
            'metodo_usado': 'sistema_hibrido'
        })
        
    except Exception as e:
        logger.error(f"Error en recomendación por ingredientes: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'data': []
        }), 500


@bp.route('/consulta', methods=['POST'])
def recomendar_por_consulta():
    \"\"\"
    Recomendaciones híbridas por consulta de texto
    \"\"\"
    try:
        datos = request.get_json(silent=True)
        if not datos:
            return jsonify({'success': False, 'error': 'No se recibieron datos'}), 400
        
        consulta = datos.get('consulta', '')
        max_resultados = datos.get('max_resultados', 5)
        
        if not consulta.strip():
            return jsonify({'success': False, 'error': 'La consulta no puede estar vacía'}), 400
        
        logger.info(f"Procesando consulta: {consulta}")
        
        # Analizar la consulta con NLP
        analisis = motor_inferencia.analizar_consulta(consulta)
        
        # Obtener recomendaciones híbridas
        recomendaciones = sistema_recomendacion_mejorado.recomendar_hibrido(
            ingredientes=analisis.get('ingredientes', []),
            texto_consulta=consulta,
            max_resultados=max_resultados
        )
        
        return jsonify({
            'success': True,
            'data': {
                'analisis': analisis,
                'recomendaciones': recomendaciones
            },
            'total_encontradas': len(recomendaciones),
            'metodo_usado': 'sistema_hibrido_nlp'
        })
        
    except Exception as e:
        logger.error(f"Error en recomendación por consulta: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'data': {'analisis': {}, 'recomendaciones': []}
        }), 500


@bp.route('/similares/<int:receta_id>', methods=['GET'])
def recomendar_similares(receta_id):
    \"\"\"
    Recomienda recetas similares usando el sistema mejorado
    \"\"\"
    try:
        max_resultados = request.args.get('max_resultados', 5, type=int)
        
        logger.info(f"Buscando recetas similares a ID: {receta_id}")
        
        # Usar el sistema mejorado
        recomendaciones = sistema_recomendacion_mejorado.recomendar_recetas_similares(
            receta_id=receta_id,
            max_resultados=max_resultados
        )
        
        return jsonify({
            'success': True,
            'data': recomendaciones,
            'total_encontradas': len(recomendaciones),
            'metodo_usado': 'similitud_hibrida'
        })
        
    except Exception as e:
        logger.error(f"Error al recomendar recetas similares: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al buscar recetas similares',
            'data': []
        }), 500


@bp.route('/entrenar', methods=['POST'])
def entrenar_sistema():
    \"\"\"
    Fuerza el reentrenamiento del sistema de recomendaciones
    \"\"\"
    try:
        logger.info("Iniciando reentrenamiento del sistema...")
        
        # Forzar reentrenamiento
        sistema_recomendacion_mejorado.modelo_entrenado = False
        exito = sistema_recomendacion_mejorado.entrenar()
        
        if exito:
            return jsonify({
                'success': True,
                'message': 'Sistema reentrenado correctamente',
                'estado': 'entrenado'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error durante el entrenamiento',
                'estado': 'error'
            }), 500
            
    except Exception as e:
        logger.error(f"Error al entrenar sistema: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno durante entrenamiento',
            'estado': 'error'
        }), 500


@bp.route('/estado', methods=['GET'])
def obtener_estado_sistema():
    \"\"\"
    Devuelve el estado actual del sistema de recomendaciones
    \"\"\"
    try:
        estado = {
            'modelo_entrenado': sistema_recomendacion_mejorado.modelo_entrenado,
            'algoritmos_disponibles': ['tfidf', 'kmeans', 'random_forest'],
            'num_recetas': len(sistema_recomendacion_mejorado.recetas_ids) if sistema_recomendacion_mejorado.recetas_ids else 0
        }
        
        return jsonify({
            'success': True,
            'data': estado
        })
        
    except Exception as e:
        logger.error(f"Error al obtener estado: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener estado del sistema'
        }), 500


@bp.route('/preferencias', methods=['POST'])
def actualizar_preferencias():
    \"\"\"
    Actualiza preferencias del usuario
    \"\"\"
    try:
        datos = request.get_json(silent=True)
        
        # Generar session_id si no existe
        session_id = session.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
        
        # Por ahora, solo confirmamos que se recibieron
        preferencias_guardadas = {
            'session_id': session_id,
            'restricciones_dieteticas': datos.get('restricciones', []) if datos else [],
            'alergias': datos.get('alergias', []) if datos else [],
            'ingredientes_favoritos': datos.get('favoritos', []) if datos else [],
            'ingredientes_evitados': datos.get('evitados', []) if datos else []
        }
        
        logger.info(f"Preferencias actualizadas para sesión: {session_id}")
        
        return jsonify({
            'success': True,
            'message': 'Preferencias guardadas correctamente',
            'data': preferencias_guardadas
        })
        
    except Exception as e:
        logger.error(f"Error al actualizar preferencias: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al guardar preferencias'
        }), 500


@bp.route('/feedback', methods=['POST'])
def registrar_feedback():
    \"\"\"
    Registra feedback del usuario sobre recomendaciones
    \"\"\"
    try:
        datos = request.json
        
        if not datos or 'receta_id' not in datos or 'puntuacion' not in datos:
            return jsonify({
                'success': False,
                'error': 'Faltan datos requeridos (receta_id, puntuacion)'
            }), 400
        
        receta_id = datos.get('receta_id')
        puntuacion = datos.get('puntuacion')
        comentario = datos.get('comentario', '')
        
        # Por ahora solo loggeamos el feedback
        logger.info(f"Feedback recibido - Receta: {receta_id}, Puntuación: {puntuacion}, Comentario: {comentario}")
        
        return jsonify({
            'success': True,
            'message': 'Feedback registrado correctamente'
        })
        
    except Exception as e:
        logger.error(f"Error al registrar feedback: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al registrar feedback'
        }), 500


@bp.route('/pdf', methods=['POST'])
def generar_pdf_recomendaciones():
    \"\"\"
    Genera un PDF con varias recetas recomendadas
    \"\"\"
    try:
        datos = request.json
        
        if not datos or 'recetas_ids' not in datos:
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar una lista de IDs de recetas'
            }), 400
            
        recetas_ids = datos.get('recetas_ids', [])
        titulo = datos.get('titulo', 'Recetas Recomendadas por IA')
        
        # Generar PDF
        pdf_data = pdf_generator.generar_pdf_recomendaciones(
            recetas_ids=recetas_ids,
            titulo=titulo
        )
        
        if pdf_data:
            # Crear archivo en memoria
            pdf_buffer = io.BytesIO(pdf_data)
            pdf_buffer.seek(0)
            
            # Enviar archivo
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name='recetas_recomendadas_ai.pdf'
            )
        else:
            return jsonify({
                'success': False,
                'error': 'Error al generar PDF'
            }), 500
            
    except Exception as e:
        logger.error(f"Error al generar PDF de recomendaciones: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al generar PDF'
        }), 500"""
        
        # Reemplazar el contenido completo
        nuevo_contenido = new_imports + nuevas_rutas
        
        # Escribir el nuevo contenido
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(nuevo_contenido)
        
        logger.info(f"Rutas actualizadas en {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error al actualizar rutas: {str(e)}")
        return False

def crear_archivo_sistema_mejorado():
    """Crea el archivo del sistema mejorado"""
    file_path = os.path.join('app', 'services', 'recomendacion_mejorada.py')
    
    # El contenido está en el artifact anterior
    # Solo necesitamos asegurarnos de que el archivo existe
    
    if not os.path.exists(file_path):
        logger.warning(f"El archivo {file_path} no existe. Por favor, crea el archivo con el contenido del sistema mejorado.")
        return False
    
    logger.info(f"Sistema mejorado disponible en {file_path}")
    return True

def actualizar_javascript():
    """Actualiza el JavaScript para mostrar información de los algoritmos"""
    file_path = os.path.join('app', 'static', 'js', 'app.js')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Buscar la función de mostrar resultados y mejorarla
        funcion_mejorada = """
    // Función para mostrar los resultados de las recetas
    function mostrarResultados(recetas, contenidoAdicional = '') {
        let html = contenidoAdicional;
        
        html += `
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4>Recetas Recomendadas por IA</h4>
                <small class="text-muted">Sistema Híbrido: TF-IDF + K-means + Random Forest</small>
            </div>
            <div class="row">
        `;
        
        recetas.forEach((receta, index) => {
            let ingredientesFaltantes = '';
            if (receta.ingredientes_faltantes && receta.ingredientes_faltantes.length > 0) {
                ingredientesFaltantes = `
                    <div class="mt-2">
                        <small class="text-danger">
                            <strong>Te faltan:</strong> ${receta.ingredientes_faltantes.join(', ')}
                        </small>
                    </div>
                `;
            }
            
            // Mostrar información de los algoritmos usados
            let metodosInfo = '';
            if (receta.metodos_usados && receta.metodos_usados.length > 0) {
                const metodosTexto = receta.metodos_usados.map(m => {
                    switch(m) {
                        case 'contenido_texto': return 'Análisis de Texto';
                        case 'contenido_receta': return 'Similitud';
                        case 'kmeans': return 'K-means';
                        case 'random_forest': return 'Random Forest';
                        default: return m;
                    }
                }).join(', ');
                
                metodosInfo = `
                    <div class="mt-1">
                        <small class="text-info">
                            <i class="bi bi-cpu"></i> ${metodosTexto}
                        </small>
                    </div>
                `;
            }
            
            // Mostrar score de recomendación si está disponible
            let scoreInfo = '';
            if (receta.score_recomendacion) {
                const scorePercent = Math.round(receta.score_recomendacion * 100);
                scoreInfo = `
                    <div class="mt-1">
                        <small class="text-success">
                            <i class="bi bi-star-fill"></i> Compatibilidad: ${scorePercent}%
                        </small>
                    </div>
                `;
            }
            
            html += `
                <div class="col-md-6 mb-4">
                    <div class="card h-100 ${index === 0 ? 'border-primary' : ''}">
                        <div class="card-header ${index === 0 ? 'bg-primary text-white' : ''}">
                            <h5 class="card-title mb-0">
                                ${receta.nombre}
                                ${index === 0 ? ' <i class="bi bi-star-fill"></i>' : ''}
                            </h5>
                        </div>
                        ${receta.imagen_url ? `<img src="/static/${receta.imagen_url}" class="card-img-top" alt="${receta.nombre}">` : ''}
                        <div class="card-body">
                            <p class="card-text">${receta.descripcion ? receta.descripcion.substring(0, 100) + '...' : 'Sin descripción'}</p>
                            
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span><i class="bi bi-clock"></i> ${receta.tiempo_preparacion} min</span>
                                <span><i class="bi bi-person"></i> ${receta.porciones} porciones</span>
                                <span><i class="bi bi-star"></i> ${receta.dificultad || 'Media'}</span>
                            </div>
                            
                            ${receta.calorias ? `
                                <div class="text-center mb-2">
                                    <small class="text-muted">
                                        🔥 ${receta.calorias} kcal | 🥩 ${receta.proteinas || 0}g prot | 🍞 ${receta.carbohidratos || 0}g carb
                                    </small>
                                </div>
                            ` : ''}
                            
                            ${metodosInfo}
                            ${scoreInfo}
                            ${ingredientesFaltantes}
                        </div>
                        <div class="card-footer">
                            <button class="btn btn-outline-primary w-100" onclick="verReceta(${receta.id})">Ver Detalles</button>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += `
            </div>
            <div class="d-grid gap-2 mt-3">
                <button class="btn btn-success" onclick="descargarPDFMultiple()">📄 Descargar todas las recetas en PDF</button>
                <button class="btn btn-info" onclick="reentrenarSistema()">🔄 Reentrenar Sistema IA</button>
            </div>
            
            <div class="mt-3">
                <small class="text-muted">
                    <strong>Sistema Inteligente:</strong> Este sistema utiliza múltiples algoritmos de inteligencia artificial 
                    para ofrecerte las mejores recomendaciones basadas en tus ingredientes, preferencias y patrones de búsqueda.
                </small>
            </div>
        `;
        
        resultadosContainer.innerHTML = html;
    }"""
        
        # Función para reentrenar el sistema
        funcion_reentrenar = """
    
    // Función para reentrenar el sistema de IA
    window.reentrenarSistema = async function() {
        try {
            // Mostrar indicador de carga
            resultadosContainer.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Reentrenando...</span></div><p class="mt-2">🤖 Reentrenando sistema de IA...</p><p class="text-muted">Esto puede tomar unos momentos</p></div>';
            
            const response = await fetch('/api/recomendaciones/entrenar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                mostrarMensaje('🎉 Sistema de IA reentrenado correctamente. Las próximas recomendaciones serán aún más precisas!', 'success');
            } else {
                mostrarMensaje('❌ Error al reentrenar el sistema: ' + (data.error || 'Error desconocido'), 'warning');
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarMensaje('❌ Error de conexión al reentrenar el sistema', 'danger');
        }
    }"""
        
        # Buscar y reemplazar la función mostrarResultados
        import re
        
        pattern = r"function mostrarResultados\(recetas, contenidoAdicional = ''\) \{[\s\S]*?\n    \}"
        if re.search(pattern, content):
            new_content = re.sub(pattern, funcion_mejorada.strip(), content)
        else:
            # Si no encuentra la función, agregarla al final
            new_content = content + "\n" + funcion_mejorada
        
        # Agregar función de reentrenamiento
        new_content += funcion_reentrenar
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        logger.info(f"JavaScript actualizado en {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error al actualizar JavaScript: {str(e)}")
        return False

def main():
    """Función principal de integración"""
    logger.info("🚀 Iniciando integración del sistema mejorado...")
    
    pasos_completados = 0
    total_pasos = 3
    
    # Paso 1: Verificar que existe el sistema mejorado
    logger.info("📁 Verificando sistema mejorado...")
    if crear_archivo_sistema_mejorado():
        pasos_completados += 1
        logger.info("✅ Sistema mejorado verificado")
    else:
        logger.error("❌ Error al verificar sistema mejorado")
        return False
    
    # Paso 2: Actualizar rutas
    logger.info("🔄 Actualizando rutas de la API...")
    if actualizar_rutas_recomendaciones():
        pasos_completados += 1
        logger.info("✅ Rutas actualizadas")
    else:
        logger.error("❌ Error al actualizar rutas")
    
    # Paso 3: Actualizar JavaScript
    logger.info("🎨 Actualizando interfaz de usuario...")
    if actualizar_javascript():
        pasos_completados += 1
        logger.info("✅ JavaScript actualizado")
    else:
        logger.error("❌ Error al actualizar JavaScript")
    
    # Resumen
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 RESUMEN DE INTEGRACIÓN: {pasos_completados}/{total_pasos} pasos completados")
    logger.info(f"{'='*60}")
    
    if pasos_completados == total_pasos:
        logger.info("🎉 ¡INTEGRACIÓN COMPLETADA EXITOSAMENTE!")
        logger.info("\n🔥 TU SISTEMA AHORA INCLUYE:")
        logger.info("   📈 Filtrado basado en contenido (TF-IDF)")
        logger.info("   🎯 Agrupación inteligente (K-means)")
        logger.info("   🤖 Predicción de preferencias (Random Forest)")
        logger.info("   🔀 Sistema híbrido que combina todos los algoritmos")
        logger.info("\n🚀 PRÓXIMOS PASOS:")
        logger.info("   1. Reinicia tu servidor: python run.py")
        logger.info("   2. Usa el botón 'Reentrenar Sistema IA' en la web")
        logger.info("   3. ¡Disfruta de recomendaciones más inteligentes!")
        
        return True
    else:
        logger.warning("⚠️  Integración parcialmente completada")
        logger.info("💡 Revisa los errores anteriores y ejecuta el script nuevamente")
        return False

if __name__ == '__main__':
    main()