from flask import Blueprint, jsonify, request, send_file, session
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
pdf_generator = PDFGenerator()

@bp.route('/por-ingredientes', methods=['POST'])
def recomendar_por_ingredientes():
    """
    Recomendaciones híbridas por ingredientes usando el sistema mejorado
    """
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
    """
    Recomendaciones híbridas por consulta de texto
    """
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
    """
    Recomienda recetas similares usando el sistema mejorado
    """
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
    """
    Fuerza el reentrenamiento del sistema de recomendaciones
    """
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
    """
    Devuelve el estado actual del sistema de recomendaciones
    """
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
    """
    Actualiza preferencias del usuario
    """
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
    """
    Registra feedback del usuario sobre recomendaciones
    """
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
    """
    Genera un PDF con varias recetas recomendadas
    """
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
        }), 500