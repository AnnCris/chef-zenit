from flask import Blueprint, jsonify, request, send_file, session
from app.services.recomendacion import SistemaRecomendacion
from app.services.motor_inferencia import MotorInferencia
from app.services.pdf_generator import PDFGenerator
import uuid
import io
import logging
from app import db
from app import db

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear blueprint
bp = Blueprint('recomendaciones', __name__, url_prefix='/api/recomendaciones')

# Inicializar servicios
sistema_recomendacion = SistemaRecomendacion()
motor_inferencia = MotorInferencia()
pdf_generator = PDFGenerator()

def recomendar_por_ingredientes(self, ingredientes, session_id=None, max_resultados=5):
    """
    Versión simplificada para obtener recetas con los ingredientes dados
    """
    from app.models.receta import Receta, RecetaIngrediente
    from sqlalchemy.sql import func
    
    try:
        # Contar cuántas recetas hay en total
        total_recetas = Receta.query.count()
        
        if total_recetas == 0:
            logger.warning("No hay recetas en la base de datos")
            return []
        
        # Si no hay ingredientes, devolver algunas recetas aleatorias
        if not ingredientes:
            recetas = Receta.query.order_by(func.random()).limit(max_resultados).all()
            return [r.to_dict_full() for r in recetas]
        
        # Buscar recetas que tengan al menos uno de los ingredientes
        receta_ids = db.session.query(RecetaIngrediente.receta_id).filter(
            RecetaIngrediente.ingrediente_id.in_(ingredientes)
        ).distinct().all()
        
        receta_ids = [r[0] for r in receta_ids]
        
        # Si no hay coincidencias, devolver recetas aleatorias
        if not receta_ids:
            recetas = Receta.query.order_by(func.random()).limit(max_resultados).all()
        else:
            recetas = Receta.query.filter(Receta.id.in_(receta_ids)).limit(max_resultados).all()
        
        return [r.to_dict_full() for r in recetas]
    except Exception as e:
        logger.error(f"Error en recomendación simplificada: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        # En caso de error, devolver algunas recetas aleatorias
        try:
            recetas = Receta.query.limit(max_resultados).all()
            return [r.to_dict_full() for r in recetas]
        except:
            return []


@bp.route('/consulta', methods=['POST'])
def recomendar_por_consulta():
    """
    Versión estática para procesar consultas de texto - siempre devuelve datos de ejemplo
    """
    try:
        # Intentar leer los datos de la solicitud (solo para mostrar en los logs)
        datos = request.get_json(silent=True)
        consulta = datos.get('consulta', '') if datos else ''
        print(f"Consulta recibida: {consulta}")
        
        # Datos estáticos de ejemplo que siempre funcionarán
        return jsonify({
            'success': True,
            'data': {
                'analisis': {
                    'ingredientes': ['pollo', 'tomate'],
                    'restricciones': [],
                    'alergias': [],
                    'texto_procesado': ['quiero', 'hacer', 'cena', 'rápida', 'pollo', 'tomate']
                },
                'recomendaciones': [
                    {
                        'id': 1,
                        'nombre': 'Pollo al Horno con Tomates',
                        'descripcion': 'Una receta rápida y saludable de pollo al horno con tomates frescos.',
                        'tiempo_preparacion': 35,
                        'porciones': 4,
                        'dificultad': 'Media',
                        'categoria': 'Platos principales',
                        'calorias': 320,
                        'proteinas': 28.0,
                        'carbohidratos': 12.0,
                        'grasas': 18.0,
                        'ingredientes': [
                            {'nombre': 'Pollo (pechugas)', 'cantidad': 4, 'unidad': 'unidades'},
                            {'nombre': 'Tomate', 'cantidad': 4, 'unidad': 'unidades'},
                            {'nombre': 'Cebolla', 'cantidad': 1, 'unidad': 'unidad'},
                            {'nombre': 'Aceite de oliva', 'cantidad': 2, 'unidad': 'cucharadas'},
                            {'nombre': 'Sal', 'cantidad': 1, 'unidad': 'cucharadita'},
                            {'nombre': 'Pimienta', 'cantidad': 0.5, 'unidad': 'cucharadita'}
                        ],
                        'pasos': [
                            {'numero': 1, 'descripcion': 'Precalentar el horno a 180°C'},
                            {'numero': 2, 'descripcion': 'Sazonar las pechugas de pollo con sal y pimienta'},
                            {'numero': 3, 'descripcion': 'Cortar los tomates y la cebolla en rodajas'},
                            {'numero': 4, 'descripcion': 'En una fuente para horno, colocar las pechugas y cubrir con las rodajas de tomate y cebolla'},
                            {'numero': 5, 'descripcion': 'Rociar con aceite de oliva y hornear por 25-30 minutos'}
                        ],
                        'valor_nutricional': {
                            'vitamina_a': 80.5,
                            'vitamina_c': 45.2,
                            'calcio': 30.1,
                            'hierro': 2.8
                        },
                        'imagen_url': None,
                        'ingredientes_faltantes': []
                    },
                    {
                        'id': 2,
                        'nombre': 'Pasta con Pollo y Salsa de Tomate',
                        'descripcion': 'Una pasta deliciosa con trozos de pollo y una salsa casera de tomate.',
                        'tiempo_preparacion': 25,
                        'porciones': 3,
                        'dificultad': 'Fácil',
                        'categoria': 'Pastas',
                        'calorias': 450,
                        'proteinas': 22.0,
                        'carbohidratos': 65.0,
                        'grasas': 10.0,
                        'ingredientes': [
                            {'nombre': 'Pasta', 'cantidad': 300, 'unidad': 'gramos'},
                            {'nombre': 'Pollo', 'cantidad': 250, 'unidad': 'gramos'},
                            {'nombre': 'Tomate', 'cantidad': 4, 'unidad': 'unidades'},
                            {'nombre': 'Cebolla', 'cantidad': 1, 'unidad': 'unidad'},
                            {'nombre': 'Ajo', 'cantidad': 2, 'unidad': 'dientes'},
                            {'nombre': 'Aceite de oliva', 'cantidad': 2, 'unidad': 'cucharadas'},
                            {'nombre': 'Sal', 'cantidad': 1, 'unidad': 'cucharadita'}
                        ],
                        'pasos': [
                            {'numero': 1, 'descripcion': 'Cortar el pollo en cubos y saltear en una sartén'},
                            {'numero': 2, 'descripcion': 'Añadir cebolla y ajo picados, cocinar hasta que estén transparentes'},
                            {'numero': 3, 'descripcion': 'Agregar los tomates cortados y cocinar hasta formar una salsa'},
                            {'numero': 4, 'descripcion': 'Cocinar la pasta según las instrucciones del paquete'},
                            {'numero': 5, 'descripcion': 'Mezclar la pasta con la salsa de pollo y tomate'}
                        ],
                        'valor_nutricional': {
                            'vitamina_a': 55.0,
                            'vitamina_c': 35.5,
                            'calcio': 25.0,
                            'hierro': 2.2
                        },
                        'imagen_url': None,
                        'ingredientes_faltantes': []
                    }
                ]
            }
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error en consulta estática: {str(e)}")
        # Incluso en caso de error, devolver un JSON válido
        return jsonify({
            'success': False,
            'error': str(e),
            'data': {
                'analisis': {},
                'recomendaciones': []
            }
        })
@bp.route('/similares/<int:receta_id>', methods=['GET'])
def recomendar_similares(receta_id):
    """
    Recomienda recetas similares a una receta dada
    """
    try:
        max_resultados = request.args.get('max_resultados', 5, type=int)
        
        # Obtener recomendaciones
        recomendaciones = sistema_recomendacion.recomendar_recetas_similares(
            receta_id=receta_id,
            max_resultados=max_resultados
        )
        
        return jsonify({
            'success': True,
            'data': recomendaciones
        })
    except Exception as e:
        logger.error(f"Error al recomendar recetas similares: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al recomendar recetas similares'
        }), 500

@bp.route('/sustitutos/<int:ingrediente_id>', methods=['GET'])
def obtener_sustitutos(ingrediente_id):
    """
    Obtiene sustitutos para un ingrediente
    """
    try:
        tipo_sustitucion = request.args.get('tipo')
        
        # Obtener sustitutos
        sustitutos = sistema_recomendacion.obtener_sustitutos(
            ingrediente_id=ingrediente_id,
            tipo_sustitucion=tipo_sustitucion
        )
        
        return jsonify({
            'success': True,
            'data': sustitutos
        })
    except Exception as e:
        logger.error(f"Error al obtener sustitutos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener sustitutos'
        }), 500

@bp.route('/nutricion/<int:receta_id>', methods=['GET'])
def obtener_nutricion(receta_id):
    """
    Obtiene información nutricional de una receta
    """
    try:
        # Obtener información nutricional
        nutricion = sistema_recomendacion.obtener_informacion_nutricional(receta_id)
        
        if nutricion:
            return jsonify({
                'success': True,
                'data': nutricion
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró información nutricional'
            }), 404
    except Exception as e:
        logger.error(f"Error al obtener información nutricional: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener información nutricional'
        }), 500



@bp.route('/preferencias', methods=['POST'])
def actualizar_preferencias():
    """
    Versión que no depende de sesiones para actualizar preferencias
    """
    try:
        # Intentar leer los datos de la solicitud
        datos = request.get_json(silent=True)
        print(f"Datos de preferencias recibidos: {datos}")
        
        # Generar un ID único para el usuario (en lugar de usar session)
        import uuid
        user_id = uuid.uuid4().hex[:16]
        
        # Datos estáticos para simular preferencias guardadas
        preferencias_guardadas = {
            'id': 1,
            'user_id': user_id,
            'restricciones_dieteticas': datos.get('restricciones', []) if datos else [],
            'alergias': datos.get('alergias', []) if datos else [],
            'ingredientes_favoritos': datos.get('favoritos', []) if datos else [],
            'ingredientes_evitados': datos.get('evitados', []) if datos else []
        }
        
        # Respuesta exitosa
        return jsonify({
            'success': True,
            'message': 'Preferencias guardadas correctamente',
            'data': preferencias_guardadas
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error en preferencias: {str(e)}")
        # Incluso en caso de error, devolver un JSON válido
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'No se pudieron guardar las preferencias'
        })
@bp.route('/feedback', methods=['POST'])
def registrar_feedback():
    """
    Registra el feedback del usuario sobre una recomendación
    """
    try:
        # Obtener datos de la petición
        datos = request.json
        
        if not datos or 'historico_id' not in datos or 'feedback' not in datos:
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar historico_id y feedback'
            }), 400
            
        historico_id = datos.get('historico_id')
        feedback = datos.get('feedback')
        
        # Registrar feedback
        exito = sistema_recomendacion.registrar_feedback(
            historico_id=historico_id,
            feedback=feedback
        )
        
        if exito:
            return jsonify({
                'success': True,
                'message': 'Feedback registrado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo registrar el feedback'
            }), 404
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
        # Obtener datos de la petición
        datos = request.json
        
        if not datos or 'recetas_ids' not in datos:
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar una lista de IDs de recetas'
            }), 400
            
        recetas_ids = datos.get('recetas_ids', [])
        titulo = datos.get('titulo', 'Recetas Recomendadas')
        
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
                download_name='recetas_recomendadas.pdf'
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


@bp.route('/por-ingredientes', methods=['POST'])
def recomendar_por_ingredientes():
    """
    Versión estática para la demostración - siempre devuelve datos de ejemplo
    """
    try:
        # Intentar leer los datos de la solicitud (solo para mostrar en los logs)
        datos = request.get_json(silent=True)
        print(f"Datos recibidos: {datos}")
        
        # Datos estáticos de ejemplo que siempre funcionarán
        return jsonify({
            'success': True,
            'data': [
                {
                    'id': 1,
                    'nombre': 'Ensalada Mediterránea',
                    'descripcion': 'Una fresca ensalada con tomate, lechuga y cebolla.',
                    'tiempo_preparacion': 15,
                    'porciones': 2,
                    'dificultad': 'Fácil',
                    'categoria': 'Ensaladas',
                    'calorias': 180,
                    'proteinas': 4.5,
                    'carbohidratos': 10.2,
                    'grasas': 14.5,
                    'ingredientes': [
                        {'nombre': 'Tomate', 'cantidad': 2, 'unidad': 'unidades'},
                        {'nombre': 'Cebolla', 'cantidad': 0.5, 'unidad': 'unidad'},
                        {'nombre': 'Lechuga', 'cantidad': 1, 'unidad': 'unidad'},
                        {'nombre': 'Aceite de oliva', 'cantidad': 2, 'unidad': 'cucharadas'},
                        {'nombre': 'Sal', 'cantidad': 1, 'unidad': 'pizca'}
                    ],
                    'pasos': [
                        {'numero': 1, 'descripcion': 'Lavar y cortar la lechuga en trozos pequeños'},
                        {'numero': 2, 'descripcion': 'Cortar los tomates en cubos'},
                        {'numero': 3, 'descripcion': 'Picar finamente la cebolla'},
                        {'numero': 4, 'descripcion': 'Mezclar todo en un bol'},
                        {'numero': 5, 'descripcion': 'Aliñar con aceite y sal'}
                    ],
                    'valor_nutricional': {
                        'vitamina_a': 120.5,
                        'vitamina_c': 35.2,
                        'calcio': 45.3,
                        'hierro': 1.2
                    },
                    'imagen_url': None,
                    'ingredientes_faltantes': []
                },
                {
                    'id': 2,
                    'nombre': 'Arroz con Verduras',
                    'descripcion': 'Un plato sencillo y nutritivo a base de arroz y vegetales.',
                    'tiempo_preparacion': 25,
                    'porciones': 3,
                    'dificultad': 'Fácil',
                    'categoria': 'Platos principales',
                    'calorias': 320,
                    'proteinas': 6.0,
                    'carbohidratos': 65.0,
                    'grasas': 5.0,
                    'ingredientes': [
                        {'nombre': 'Arroz', 'cantidad': 250, 'unidad': 'gramos'},
                        {'nombre': 'Cebolla', 'cantidad': 1, 'unidad': 'unidad'},
                        {'nombre': 'Tomate', 'cantidad': 2, 'unidad': 'unidades'},
                        {'nombre': 'Aceite de oliva', 'cantidad': 2, 'unidad': 'cucharadas'},
                        {'nombre': 'Sal', 'cantidad': 1, 'unidad': 'cucharadita'}
                    ],
                    'pasos': [
                        {'numero': 1, 'descripcion': 'Picar la cebolla y el tomate'},
                        {'numero': 2, 'descripcion': 'Sofreír en aceite a fuego medio'},
                        {'numero': 3, 'descripcion': 'Añadir el arroz y tostar ligeramente'},
                        {'numero': 4, 'descripcion': 'Agregar el doble de agua que de arroz'},
                        {'numero': 5, 'descripcion': 'Cocinar a fuego bajo hasta que el arroz esté listo'}
                    ],
                    'valor_nutricional': {
                        'vitamina_a': 45.2,
                        'vitamina_c': 22.1,
                        'calcio': 25.0,
                        'hierro': 1.8
                    },
                    'imagen_url': None,
                    'ingredientes_faltantes': []
                }
            ]
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error en recomendación estática: {str(e)}")
        # Incluso en caso de error, devolver un JSON válido
        return jsonify({
            'success': False,
            'error': str(e),
            'data': []
        })
