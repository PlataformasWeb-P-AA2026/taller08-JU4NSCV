# migrate.py
import pandas as pd
from sqlalchemy.orm import sessionmaker
from clases import get_engine, Continente, Pais, Jugador

# Diccionario de soporte para clasificar los países del CSV en sus respectivos continentes
MAPEO_CONTINENTES = {
    # Sudamérica
    'Argentina': 'América del Sur', 'Brasil': 'América del Sur', 'Uruguay': 'América del Sur',
    'Colombia': 'América del Sur', 'Chile': 'América del Sur', 'Ecuador': 'América del Sur',
    'Perú': 'América del Sur', 'Paraguay': 'América del Sur', 'Venezuela': 'América del Sur',
    'Bolivia': 'América del Sur',
    # Europa
    'España': 'Europa', 'Francia': 'Europa', 'Italia': 'Europa', 'Alemania': 'Europa',
    'Inglaterra': 'Europa', 'Portugal': 'Europa', 'Países Bajos': 'Europa', 'Bélgica': 'Europa',
    'Croacia': 'Europa', 'Ucrania': 'Europa', 'Suiza': 'Europa',
    # Norte y Centroamérica
    'México': 'América del Norte', 'Estados Unidos': 'América del Norte', 'Canadá': 'América del Norte',
    'Costa Rica': 'América Central', 'Panamá': 'América Central',
    # África
    'Camerún': 'África', 'Senegal': 'África', 'Ghana': 'África', 'Marruecos': 'África', 'Nigeria': 'África',
    # Asia y Oceanía
    'Japón': 'Asia', 'Corea del Sur': 'Asia', 'Australia': 'Oceanía', 'Nueva Zelanda': 'Oceanía'
}

def migrar_datos():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    # Leer el CSV original con las columnas reales que mencionas
    df = pd.read_csv('data/jugadores_futbol.csv')

    print("Migrando datos con asignación de continentes, por favor espera...")

    for index, row in df.iterrows():
        nombre_pais_nac = row['pais_nacimiento']
        
        # 1. --- CONTINENTE ---
        # Buscamos el continente en nuestro diccionario. Si no existe, por defecto será 'Otros'
        nombre_continente = MAPEO_CONTINENTES.get(nombre_pais_nac, 'Otros')
        
        continente = session.query(Continente).filter_by(nombre=nombre_continente).first()
        if not continente:
            continente = Continente(nombre=nombre_continente)
            session.add(continente)
            session.commit()  # Commit para generar el ID del continente

        # 2. --- PAÍS NACIMIENTO ---
        pais_nac = session.query(Pais).filter_by(nombre=nombre_pais_nac).first()
        if not pais_nac:
            pais_nac = Pais(nombre=nombre_pais_nac, continente_id=continente.id)
            session.add(pais_nac)
            session.commit()

        # 3. --- PAÍS DONDE JUEGA ---
        nombre_pais_juega = row['pais_donde_juega']
        pais_juega = session.query(Pais).filter_by(nombre=nombre_pais_juega).first()
        if not pais_juega:
            # También le asignamos continente al país destino si existe en el mapeo
            nombre_cont_juega = MAPEO_CONTINENTES.get(nombre_pais_juega, 'Otros')
            continente_juega = session.query(Continente).filter_by(nombre=nombre_cont_juega).first()
            if not continente_juega:
                continente_juega = Continente(nombre=nombre_cont_juega)
                session.add(continente_juega)
                session.commit()
                
            pais_juega = Pais(nombre=nombre_pais_juega, continente_id=continente_juega.id)
            session.add(pais_juega)
            session.commit()

        # 4. --- JUGADOR ---
        jugador = Jugador(
            nombre=row['nombre_jugador'],
            pais_nacimiento_id=pais_nac.id,
            pais_donde_juega_id=pais_juega.id,
            posicion=row['posicion'],
            edad=row['edad'],
            partidos_seleccion=row['numero_partidos_seleccion'],
            goles_seleccion=row['goles_seleccion']
        )
        session.add(jugador)

    # Guardar todos los jugadores en la base de datos
    session.commit()
    session.close()
    print("Migración completada exitosamente con relaciones de continente.")

if __name__ == "__main__":
    migrar_datos()