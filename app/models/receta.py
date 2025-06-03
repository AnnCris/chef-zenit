from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class Receta(db.Model):
    __tablename__ = 'recetas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    tiempo_preparacion = db.Column(db.Integer)  # en minutos
    porciones = db.Column(db.Integer)
    dificultad = db.Column(db.String(20))
    imagen_url = db.Column(db.String(255))
    categoria = db.Column(db.String(50))
    calorias = db.Column(db.Integer)
    proteinas = db.Column(db.Float)
    carbohidratos = db.Column(db.Float)
    grasas = db.Column(db.Float)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    ingredientes = db.relationship('RecetaIngrediente', back_populates='receta')
    pasos = db.relationship('PasoPreparacion', back_populates='receta', order_by='PasoPreparacion.numero_paso')
    valor_nutricional = db.relationship('ValorNutricional', back_populates='receta', uselist=False)
    restricciones = db.relationship('RestriccionDietetica', secondary='receta_restricciones')
    historico = db.relationship('HistoricoRecomendacion', back_populates='receta')
    
    def __repr__(self):
        return f'<Receta {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tiempo_preparacion': self.tiempo_preparacion,
            'porciones': self.porciones,
            'dificultad': self.dificultad,
            'imagen_url': self.imagen_url,
            'categoria': self.categoria,
            'calorias': self.calorias,
            'proteinas': self.proteinas,
            'carbohidratos': self.carbohidratos,
            'grasas': self.grasas,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
    
    def to_dict_full(self):
        ingredientes_dict = [
            {
                'id': ri.ingrediente.id,
                'nombre': ri.ingrediente.nombre,
                'cantidad': ri.cantidad,
                'unidad': ri.unidad,
                'es_opcional': ri.es_opcional
            } for ri in self.ingredientes
        ]
        
        pasos_dict = [
            {
                'numero': paso.numero_paso,
                'descripcion': paso.descripcion
            } for paso in self.pasos
        ]
        
        nutricion = {}
        if self.valor_nutricional:
            nutricion = {
                'vitamina_a': self.valor_nutricional.vitamina_a,
                'vitamina_c': self.valor_nutricional.vitamina_c,
                'vitamina_d': self.valor_nutricional.vitamina_d,
                'vitamina_e': self.valor_nutricional.vitamina_e,
                'calcio': self.valor_nutricional.calcio,
                'hierro': self.valor_nutricional.hierro,
                'potasio': self.valor_nutricional.potasio,
                'otros_nutrientes': self.valor_nutricional.otros_nutrientes
            }
        
        restricciones_dict = [
            {
                'id': r.id,
                'nombre': r.nombre,
                'descripcion': r.descripcion
            } for r in self.restricciones
        ]
        
        receta_dict = self.to_dict()
        receta_dict.update({
            'ingredientes': ingredientes_dict,
            'pasos': pasos_dict,
            'valor_nutricional': nutricion,
            'restricciones': restricciones_dict
        })
        
        return receta_dict
    
    @staticmethod
    def buscar_por_nombre(nombre):
        return Receta.query.filter(Receta.nombre.ilike(f'%{nombre}%')).all()
    
    @staticmethod
    def obtener_por_categoria(categoria):
        return Receta.query.filter_by(categoria=categoria).all()
    
    @staticmethod
    def obtener_por_dificultad(dificultad):
        return Receta.query.filter_by(dificultad=dificultad).all()
    
    @staticmethod
    def obtener_por_tiempo_max(tiempo_max):
        return Receta.query.filter(Receta.tiempo_preparacion <= tiempo_max).all()
    
    @staticmethod
    def obtener_recientes(limite=10):
        return Receta.query.order_by(Receta.fecha_creacion.desc()).limit(limite).all()


class RecetaIngrediente(db.Model):
    __tablename__ = 'receta_ingredientes'
    
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'))
    cantidad = db.Column(db.Float)
    unidad = db.Column(db.String(30))
    es_opcional = db.Column(db.Boolean, default=False)
    
    # Relaciones
    receta = db.relationship('Receta', back_populates='ingredientes')
    ingrediente = db.relationship('Ingrediente', back_populates='recetas')
    
    def __repr__(self):
        return f'<RecetaIngrediente {self.receta_id}-{self.ingrediente_id}>'


class PasoPreparacion(db.Model):
    __tablename__ = 'pasos_preparacion'
    
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
    numero_paso = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    
    # Relaciones
    receta = db.relationship('Receta', back_populates='pasos')
    
    def __repr__(self):
        return f'<PasoPreparacion {self.receta_id}-{self.numero_paso}>'


class ValorNutricional(db.Model):
    __tablename__ = 'valor_nutricional'
    
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
    vitamina_a = db.Column(db.Float)
    vitamina_c = db.Column(db.Float)
    vitamina_d = db.Column(db.Float)
    vitamina_e = db.Column(db.Float)
    calcio = db.Column(db.Float)
    hierro = db.Column(db.Float)
    potasio = db.Column(db.Float)
    otros_nutrientes = db.Column(JSONB)
    
    # Relación
    receta = db.relationship('Receta', back_populates='valor_nutricional')
    
    def __repr__(self):
        return f'<ValorNutricional {self.receta_id}>'


class Sustitucion(db.Model):
    __tablename__ = 'sustituciones'
    
    id = db.Column(db.Integer, primary_key=True)
    ingrediente_original_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'))
    ingrediente_sustituto_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'))
    tipo_sustitucion = db.Column(db.String(50))
    notas = db.Column(db.Text)
    
    # Relaciones
    ingrediente_original = db.relationship('Ingrediente', foreign_keys=[ingrediente_original_id], back_populates='sustituciones_original')
    ingrediente_sustituto = db.relationship('Ingrediente', foreign_keys=[ingrediente_sustituto_id], back_populates='sustituciones_sustituto')
    
    def __repr__(self):
        return f'<Sustitucion {self.ingrediente_original_id}-{self.ingrediente_sustituto_id}>'


class RestriccionDietetica(db.Model):
    __tablename__ = 'restricciones_dieteticas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    
    def __repr__(self):
        return f'<RestriccionDietetica {self.nombre}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }


# Tabla de asociación entre recetas y restricciones dietéticas
receta_restricciones = db.Table('receta_restricciones',
    db.Column('receta_id', db.Integer, db.ForeignKey('recetas.id'), primary_key=True),
    db.Column('restriccion_id', db.Integer, db.ForeignKey('restricciones_dieteticas.id'), primary_key=True)
)


class HistoricoRecomendacion(db.Model):
    __tablename__ = 'historico_recomendaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100))
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'))
    fecha_recomendacion = db.Column(db.DateTime, default=datetime.utcnow)
    feedback = db.Column(db.Integer)  # escala del 1-5
    
    # Relación
    receta = db.relationship('Receta', back_populates='historico')
    
    def __repr__(self):
        return f'<HistoricoRecomendacion {self.session_id}-{self.receta_id}>'