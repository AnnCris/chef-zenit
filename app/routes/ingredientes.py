from flask import Blueprint, jsonify, request
from app.models.ingrediente import Ingrediente
from app import db
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear blueprint
bp = Blueprint('ingredientes', __name__, url_prefix='/api/ingredientes')

@bp.route('/', methods=['GET'])
def obtener_ingredientes():
    """
    Obtiene todos los ingredientes o filtra por categoría
    """
    try:
        categoria = request.args.get('categoria')
        nombre = request.args.get('nombre')
        
        query = Ingrediente.query
        
        if categoria:
            query = query.filter_by(categoria=categoria)
            
        if nombre:
            query = query.filter(Ingrediente.nombre.ilike(f'%{nombre}%'))
            
        ingredientes = query.all()
        return jsonify({
            'success': True,
            'data': [i.to_dict() for i in ingredientes]
        })
    except Exception as e:
        logger.error(f"Error al obtener ingredientes: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener ingredientes'
        }), 500

@bp.route('/<int:id>', methods=['GET'])
def obtener_ingrediente(id):
    """
    Obtiene un ingrediente por su ID
    """
    try:
        ingrediente = Ingrediente.query.get(id)
        if ingrediente:
            return jsonify({
                'success': True,
                'data': ingrediente.to_dict()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Ingrediente no encontrado'
            }), 404
    except Exception as e:
        logger.error(f"Error al obtener ingrediente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener ingrediente'
        }), 500

@bp.route('/alergenos', methods=['GET'])
def obtener_alergenos():
    """
    Obtiene todos los ingredientes que son alérgenos
    """
    try:
        alergenos = Ingrediente.obtener_alergenos()
        return jsonify({
            'success': True,
            'data': [a.to_dict() for a in alergenos]
        })
    except Exception as e:
        logger.error(f"Error al obtener alérgenos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener alérgenos'
        }), 500

@bp.route('/sin-gluten', methods=['GET'])
def obtener_sin_gluten():
    """
    Obtiene todos los ingredientes sin gluten
    """
    try:
        sin_gluten = Ingrediente.obtener_sin_gluten()
        return jsonify({
            'success': True,
            'data': [i.to_dict() for i in sin_gluten]
        })
    except Exception as e:
        logger.error(f"Error al obtener ingredientes sin gluten: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener ingredientes sin gluten'
        }), 500

@bp.route('/categorias', methods=['GET'])
def obtener_categorias():
    """
    Obtiene todas las categorías de ingredientes
    """
    try:
        categorias = db.session.query(Ingrediente.categoria).distinct().all()
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