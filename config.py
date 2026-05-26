# config.py

# Diccionario con todas las cadenas de conexión configuradas previamente
DATABASE_CONFIGS = {
    'sqlite': 'sqlite:///paises.db',
    'mysql': 'mysql+pymysql://user:password@localhost:3307/paises',
    'mariadb': 'mysql+pymysql://user:password@localhost:3308/paises'
}

# --- CAMBIA ESTE VALOR PARA ALTERNAR ENTRE BASES DE DATOS ---
# Opciones válidas: 'sqlite', 'mysql', 'mariadb'
DB_ACTIVA = 'mariadb'

def obtener_url_base_datos():
    """Retorna la URL de la base de datos seleccionada."""
    try:
        return DATABASE_CONFIGS[DB_ACTIVA]
    except KeyError:
        raise ValueError(f"La base de datos '{DB_ACTIVA}' no está configurada en DATABASE_CONFIGS.")