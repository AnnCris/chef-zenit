from app import db
from sqlalchemy.dialects.postgresql import ARRAY

class PreferenciaUsuario(db.Model):
    __tablename__ = 'preferencias_usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100))
    restricciones_dieteticas = db.Column(ARRAY(db.Integer))
    alergias = db.Column(ARRAY(db.Integer))
    ingredientes_favoritos = db.Column(ARRAY(db.Integer))
    ingredientes_evitados = db.Column(ARRAY(db.Integer))
    
    def __repr__(self):
        return f'<PreferenciaUsuario {self.session_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'restricciones_dieteticas': self.restricciones_dieteticas,
            'alergias': self.alergias,
            'ingredientes_favoritos': self.ingredientes_favoritos,
            'ingredientes_evitados': self.ingredientes_evitados
        }
    
    @staticmethod
    def obtener_por_session(session_id):
        """
        Obtiene las preferencias de un usuario por su session_id
        """
        return PreferenciaUsuario.query.filter_by(session_id=session_id).first()
    
    @staticmethod
    def crear_o_actualizar(session_id, restricciones=None, alergias=None, 
                           favoritos=None, evitados=None):
        """
        Crea o actualiza las preferencias de un usuario
        """
        preferencia = PreferenciaUsuario.obtener_por_session(session_id)
        
        if preferencia is None:
            preferencia = PreferenciaUsuario(
                session_id=session_id,
                restricciones_dieteticas=restricciones or [],
                alergias=alergias or [],
                ingredientes_favoritos=favoritos or [],
                ingredientes_evitados=evitados or []
            )
            db.session.add(preferencia)
        else:
            if restricciones is not None:
                preferencia.restricciones_dieteticas = restricciones
            if alergias is not None:
                preferencia.alergias = alergias
            if favoritos is not None:
                preferencia.ingredientes_favoritos = favoritos
            if evitados is not None:
                preferencia.ingredientes_evitados = evitados
                
        db.session.commit()
        return preferencia