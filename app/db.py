import pymysql
from dbutils.pooled_db import PooledDB
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno
DB_HOST = os.getenv('DB_HOST')  
DB_USER = os.getenv('DB_USER')  
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')  

# Crear un pool de conexiones
pool = PooledDB(
    creator=pymysql,
    maxconnections=5,  # Número máximo de conexiones en el pool
    mincached=1,       # Número mínimo de conexiones ociosas
    maxcached=3,       # Número máximo de conexiones ociosas
    blocking=True,     # Esperar si no hay conexiones disponibles
    host=DB_HOST or 'localhost',
    user=DB_USER or 'root',
    password=DB_PASSWORD or '123456',
    database=DB_NAME or 'kinetic_clinic',
    cursorclass=pymysql.cursors.DictCursor
)