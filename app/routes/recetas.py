from flask import Blueprint, jsonify, request, send_file
from app.models.receta import Receta
from app.services.pdf_generator import PDFGenerator
from app import db
import io
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear blueprint
bp = Blueprint('recetas', __name__, url_prefix='/api/recetas')

# Inicializar generador de PDFs
pdf_generator = PDFGenerator()

@bp.route('/', methods=['GET'])
def obtener_recetas():
    """
    Obtiene todas las recetas o filtra por categoría, dificultad, etc.
    """
    try:
        categoria = request.args.get('categoria')
        dificultad = request.args.get('dificultad')
        tiempo_max = request.args.get('tiempo_max')
        nombre = request.args.get('nombre')
        
        query = Receta.query
        
        if categoria:
            query = query.filter_by(categoria=categoria)
            
        if dificultad:
            query = query.filter_by(dificultad=dificultad)
            
        if tiempo_max and tiempo_max.isdigit():
            query = query.filter(Receta.tiempo_preparacion <= int(tiempo_max))
            
        if nombre:
            query = query.filter(Receta.nombre.ilike(f'%{nombre}%'))
            
        recetas = query.all()
        return jsonify({
            'success': True,
            'data': [r.to_dict() for r in recetas]
        })
    except Exception as e:
        logger.error(f"Error al obtener recetas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener recetas'
        }), 500

@bp.route('/<int:id>', methods=['GET'])
def obtener_receta(id):
    """
    Obtiene una receta por su ID
    """
    try:
        receta = Receta.query.get(id)
        if receta:
            return jsonify({
                'success': True,
                'data': receta.to_dict_full()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Receta no encontrada'
            }), 404
    except Exception as e:
        logger.error(f"Error al obtener receta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener receta'
        }), 500

@bp.route('/categorias', methods=['GET'])
def obtener_categorias():
    """
    Obtiene todas las categorías de recetas
    """
    try:
        categorias = db.session.query(Receta.categoria).distinct().all()
        # Filtrar valores None
        categorias = [c[0] for c in categorias if c[0]]
        return jsonify({
            'success': True,
            'data': categorias
        })
    except Exception as e:
        logger.error(f"Error al obtener categorías: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener categorías'
        }), 500

@bp.route('/dificultad', methods=['GET'])
def obtener_dificultades():
    """
    Obtiene todas las dificultades de recetas
    """
    try:
        dificultades = db.session.query(Receta.dificultad).distinct().all()
        # Filtrar valores None
        dificultades = [d[0] for d in dificultades if d[0]]
        return jsonify({
            'success': True,
            'data': dificultades
        })
    except Exception as e:
        logger.error(f"Error al obtener dificultades: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener dificultades'
        }), 500

@bp.route('/recientes', methods=['GET'])
def obtener_recientes():
    """
    Obtiene las recetas más recientes
    """
    try:
        limite = request.args.get('limite', 10, type=int)
        recetas = Receta.obtener_recientes(limite)
        return jsonify({
            'success': True,
            'data': [r.to_dict() for r in recetas]
        })
    except Exception as e:
        logger.error(f"Error al obtener recetas recientes: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener recetas recientes'
        }), 500

@bp.route('/<int:id>/pdf', methods=['GET'])
def obtener_receta_pdf(id):
    """
    Genera y devuelve un PDF con la información de la receta
    """
    try:
        include_nutrition = request.args.get('include_nutrition', 'true').lower() == 'true'
        include_substitutes = request.args.get('include_substitutes', 'true').lower() == 'true'
        
        # Verificar que la receta existe
        receta = Receta.query.get(id)
        if not receta:
            return jsonify({
                'success': False,
                'error': 'Receta no encontrada'
            }), 404
        
        # Generar PDF
        pdf_data = pdf_generator.generar_pdf_receta(
            receta_id=id,
            include_nutrition=include_nutrition,
            include_substitutes=include_substitutes
        )
        
        if pdf_data:
            # Crear archivo en memoria
            pdf_buffer = io.BytesIO(pdf_data)
            pdf_buffer.seek(0)
            
            # Nombre del archivo
            filename = f"receta_{receta.nombre.replace(' ', '_')}.pdf"
            
            # Enviar archivo
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )
        else:
            return jsonify({
                'success': False,
                'error': 'Error al generar PDF'
            }), 500
    except Exception as e:
        logger.error(f"Error al generar PDF: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al generar PDF'
        }), 500