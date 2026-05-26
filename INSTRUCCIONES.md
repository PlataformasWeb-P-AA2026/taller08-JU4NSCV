# Taller 08: Integración de Datos y Uso de ORM ⚽

Este proyecto realiza la migración de un archivo CSV con datos de jugadores de fútbol hacia una base de datos relacional normalizada (**Continente**, **País**, **Jugador**) utilizando **SQLAlchemy** (ORM). Permite alternar de manera flexible entre **SQLite**, **MySQL** y **MariaDB**, e incluye un dashboard interactivo construido con **Streamlit** para visualizar las estadísticas en tiempo real.

---

## 🛠️ Tecnologías y Librerías Utilizadas

* **Python 3.8+**
* **Pandas** — Lectura y procesamiento eficiente del archivo CSV.
* **SQLAlchemy** — ORM moderno para el modelado relacional y manejo de la base de datos.
* **PyMySQL** — Driver de conexión con los motores MySQL y MariaDB.
* **Streamlit** — Frontend interactivo y elegante para la visualización de datos.
* **Docker & Docker Compose** — Contenerización de los motores de base de datos MySQL y MariaDB.

---

## 📁 Estructura del Proyecto

```text
taller08-JU4NSCV/
├── data/
│   └── jugadores_futbol.csv  # Archivo CSV de origen con los datos de los jugadores
├── clases.py                 # Definición del ORM (Modelos de BD) y creación de tablas
├── config.py                 # Centralización de la configuración y switch de la BD activa
├── docker-compose.yml        # Configuración de servicios Docker para MySQL y MariaDB
├── importacion.py            # Script de lectura del CSV, mapeo de continentes y migración a la BD
└── app.py                    # Frontend web interactivo con Streamlit
```

---

## 🚀 Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes componentes en tu sistema:
1. **Python 3.8 o superior**
2. **Docker Desktop** (o Docker Engine junto con Docker Compose)

---

## ⚙️ Instalación y Configuración

### 1. Instalar Dependencias de Python
Abre una terminal en la raíz del proyecto y ejecuta el siguiente comando para instalar las librerías necesarias:

```bash
pip install pandas sqlalchemy streamlit pymysql
```

### 2. Levantar los Motores de Base de Datos
El proyecto incluye un entorno preconfigurado con MySQL y MariaDB. Para iniciarlos en segundo plano, ejecuta:

```bash
docker-compose up -d
```

> [!NOTE]
> Este comando creará automáticamente una base de datos llamada `paises` en ambos motores, exponiendo los siguientes puertos locales:
> * **MySQL:** Puerto `3307`
> * **MariaDB:** Puerto `3308`

---

## 🏃‍♂️ Instrucciones de Ejecución (Paso a Paso)

### Paso 1: Seleccionar la Base de Datos Activa
Abre el archivo `config.py` y edita el valor de la variable `DB_ACTIVA` según el motor de base de datos que desees utilizar:

```python
# Opciones válidas: 'sqlite', 'mysql', 'mariadb'
DB_ACTIVA = 'sqlite'  # Cambia este valor al motor que prefieras
```

### Paso 2: Inicializar el Esquema de la Base de Datos
Ejecuta el script de clases para que SQLAlchemy genere la estructura de tablas (`continente`, `pais` y `jugador`) en la base de datos seleccionada:

```bash
python clases.py
```

### Paso 3: Ejecutar la Migración de Datos
Corre el script de importación para procesar el CSV, clasificar automáticamente los continentes y poblar las tablas relacionadas utilizando el ORM:

```bash
python importacion.py
```

### Paso 4: Lanzar la Aplicación Streamlit
Finalmente, levanta el frontend interactivo para visualizar los datos migrados de forma gráfica y amigable:

```bash
streamlit run app.py
```

---

## 🔍 Comandos Útiles para Verificación (Evidencias)

Si necesitas comprobar de forma directa el estado de los datos dentro de tus contenedores Docker, puedes acceder a la consola interactiva usando los siguientes comandos:

### 🐬 Para MySQL
```bash
docker exec -it orm_mysql_taller mysql -u user -ppassword paises
```

### 🦭 Para MariaDB
```bash
docker exec -it orm_mariadb_taller mysql -u user -ppassword paises
```

Una vez que te encuentres dentro del cliente interactivo de base de datos, puedes ejecutar las siguientes consultas de prueba:

```sql
-- Listar las tablas creadas por el ORM
SHOW TABLES;

-- Verificar los primeros jugadores migrados
SELECT COUNT(*) FROM jugador;
```