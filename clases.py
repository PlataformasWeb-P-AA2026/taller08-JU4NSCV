# models.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from config import obtener_url_base_datos

Base=declarative_base()

class Continente(Base):
    __tablename__ = 'continente'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    
    # Relación uno a muchos con Pais
    paises = relationship("Pais", back_populates="continente")

class Pais(Base):
    __tablename__ = 'pais'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    continente_id = Column(Integer, ForeignKey('continente.id'), nullable=True)
    
    continente = relationship("Continente", back_populates="paises")

class Jugador(Base):
    __tablename__ = 'jugador'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    pais_nacimiento_id = Column(Integer, ForeignKey('pais.id'))
    pais_donde_juega_id = Column(Integer, ForeignKey('pais.id'))
    posicion = Column(String(100))
    edad = Column(Integer)
    partidos_seleccion = Column(Integer)
    goles_seleccion = Column(Integer)

    # Relaciones para poder acceder al nombre de los países fácilmente
    pais_nacimiento = relationship("Pais", foreign_keys=[pais_nacimiento_id])
    pais_donde_juega = relationship("Pais", foreign_keys=[pais_donde_juega_id])

# URL de conexión por defecto a SQLite
DATABASE_URL = obtener_url_base_datos()

def get_engine(db_url=DATABASE_URL):
    # Usamos la URL actual que viene de config.py
    return create_engine(db_url)

def init_db(engine):
    Base.metadata.create_all(engine)
    print(f"Base de datos y tablas creadas con éxito usando la configuración activa.")

if __name__ == "__main__":
    engine = get_engine()
    init_db(engine)