from app import db
from sqlalchemy.dialects.postgresql import JSONB

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50))
    es_alergeno = db.Column(db.Boolean, default=False)
    contiene_gluten = db.Column(db.Boolean, default=False)
    info_nutricional = db.Column(JSONB)
    
    # Relaciones
    recetas = db.relationship('RecetaIngrediente', back_populates='ingrediente')
    sustituciones_original = db.relationship('Sustitucion', 
                                            foreign_keys='Sustitucion.ingrediente_original_id',
                                            back_populates='ingrediente_original')
    sustituciones_sustituto = db.relationship('Sustitucion', 
                                            foreign_keys='Sustitucion.ingrediente_sustituto_id',
                                            back_populates='ingrediente_sustituto')
    
    def __repr__(self):
        return f'<Ingrediente {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'es_alergeno': self.es_alergeno,
            'contiene_gluten': self.contiene_gluten,
            'info_nutricional': self.info_nutricional
        }
    
    @staticmethod
    def buscar_por_nombre(nombre):
        return Ingrediente.query.filter(Ingrediente.nombre.ilike(f'%{nombre}%')).all()
    
    @staticmethod
    def obtener_por_categoria(categoria):
        return Ingrediente.query.filter_by(categoria=categoria).all()
    
    @staticmethod
    def obtener_alergenos():
        return Ingrediente.query.filter_by(es_alergeno=True).all()
    
    @staticmethod
    def obtener_sin_gluten():
        return Ingrediente.query.filter_by(contiene_gluten=False).all()