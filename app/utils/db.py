from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import psycopg2
from app.config import SQLALCHEMY_DATABASE_URI

db_session = None

def init_db(app):
    """
    Inicializa la conexión a la base de datos
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    global db_session
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    
    return db_session

def get_db_session():
    """
    Retorna una sesión de la base de datos
    """
    if db_session is None:
        raise RuntimeError("La base de datos no ha sido inicializada. Llama a init_db() primero.")
    return db_session

def close_db_session():
    """
    Cierra la sesión de la base de datos
    """
    if db_session is not None:
        db_session.remove()

def execute_query(query, params=None, fetch=True):
    """
    Ejecuta una consulta SQL directa
    """
    conn = psycopg2.connect(SQLALCHEMY_DATABASE_URI)
    cur = conn.cursor()
    
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        
        if fetch:
            result = cur.fetchall()
        else:
            result = None
            conn.commit()
            
        return result
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()