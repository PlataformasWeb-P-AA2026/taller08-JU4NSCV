# app.py
import streamlit as st
import pandas as pd
from sqlalchemy import text
from clases import get_engine

st.set_page_config(page_title="Taller 08 - Jugadores", layout="wide")

# Conexión a la base de datos (puedes cambiar esta URL para MySQL después)
engine = get_engine()

st.title("Dashboard de Jugadores de Fútbol ⚽")

# TABLA 1: Información general
st.subheader("1. Información Detallada de Jugadores")
query_jugadores = """
    SELECT 
        j.nombre AS nombre_jugador,
        pn.nombre AS pais_nacimiento,
        pj.nombre AS pais_donde_juega,
        j.posicion,
        j.edad,
        j.partidos_seleccion AS numero_partidos_seleccion,
        j.goles_seleccion,
        c.nombre AS continente
    FROM jugador j
    JOIN pais pn ON j.pais_nacimiento_id = pn.id
    JOIN pais pj ON j.pais_donde_juega_id = pj.id
    LEFT JOIN continente c ON pn.continente_id = c.id
"""
df_jugadores = pd.read_sql(text(query_jugadores), engine.connect())
st.dataframe(df_jugadores)

# TABLA 2: Agrupación por Continente
st.subheader("2. Estadísticas por Continente")
query_continente = """
    SELECT 
        c.nombre AS continente,
        COUNT(j.id) AS numero_jugadores,
        SUM(j.goles_seleccion) AS total_goles
    FROM jugador j
    JOIN pais pn ON j.pais_nacimiento_id = pn.id
    JOIN continente c ON pn.continente_id = c.id
    GROUP BY c.nombre
    ORDER BY numero_jugadores DESC
"""
df_continente = pd.read_sql(text(query_continente), engine.connect())
st.dataframe(df_continente)

# TABLA 3: Agrupación por País (Nacimiento)
st.subheader("3. Estadísticas por País de Nacimiento")
query_pais = """
    SELECT 
        pn.nombre AS pais,
        COUNT(j.id) AS numero_jugadores,
        SUM(j.goles_seleccion) AS total_goles
    FROM jugador j
    JOIN pais pn ON j.pais_nacimiento_id = pn.id
    GROUP BY pn.nombre
    ORDER BY numero_jugadores DESC
"""
df_pais = pd.read_sql(text(query_pais), engine.connect())
st.dataframe(df_pais)