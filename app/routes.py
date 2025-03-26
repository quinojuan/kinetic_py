from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from . import app
from .db import pool
from datetime import datetime
import pandas as pd
from werkzeug.utils import secure_filename
import os

# Configuración para la carga de archivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Clase para las rutas de Pacientes
class PacientesRoutes:
    blueprint = Blueprint('pacientes', __name__)

    @staticmethod
    @blueprint.route('/pacientes', methods=['GET'])
    def listar_pacientes():
        try:
            # Obtener una conexión del pool
            connection = pool.connection()
            cursor = connection.cursor()
            
            # Ejecutar la consulta para obtener todos los pacientes
            query = "SELECT * FROM pacientes"
            cursor.execute(query)
            pacientes = cursor.fetchall()
            
            # Retornar los pacientes en formato JSON
            return jsonify(pacientes)
        except Exception as e:
            # Manejo de errores
            return jsonify({"error": str(e)}), 500
        finally:
            # Asegurarse de cerrar el cursor y la conexión
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

    @staticmethod
    @blueprint.route('/pacientes', methods=['POST'])
    def crear_paciente():
        # Lógica para crear un paciente
        return jsonify({"message": "Paciente creado"})

# Clase para las rutas de Médicas
class MedicasRoutes:
    blueprint = Blueprint('medicas', __name__)

    @staticmethod
    @blueprint.route('/medicas', methods=['GET'])
    def listar_medicas():
        # Lógica para listar médicas
        return jsonify({"message": "Lista de medicas"})

# Clase para las rutas de Citas
class CitasRoutes:
    blueprint = Blueprint('citas', __name__)

    @staticmethod
    @blueprint.route('/citas', methods=['GET'])
    def listar_citas():
        # Lógica para listar citas
        return jsonify({"message": "Lista de citas"})

# Clase para las rutas de Tratamientos y Diagnósticos
class TratamientosDiagnosticosRoutes:
    blueprint = Blueprint('tratamientos_diagnosticos', __name__)

    @staticmethod
    @blueprint.route('/tratamientos', methods=['GET'])
    def listar_tratamientos():
        # Lógica para listar tratamientos
        return jsonify({"message": "Lista de tratamientos"})

    @staticmethod
    @blueprint.route('/diagnosticos', methods=['GET'])
    def listar_diagnosticos():
        # Lógica para listar diagnósticos
        return jsonify({"message": "Lista de diagnósticos"})

# Clase para las rutas de Pagos
class PagosRoutes:
    blueprint = Blueprint('pagos', __name__)

    @staticmethod
    @blueprint.route('/pagos', methods=['GET'])
    def listar_pagos():
        # Lógica para listar pagos
        return jsonify({"message": "Lista de pagos"})

# Clase para las rutas de Estudios Previos
class EstudiosPreviosRoutes:
    blueprint = Blueprint('estudios_previos', __name__)

    @staticmethod
    @blueprint.route('/estudios_previos', methods=['GET'])
    def listar_estudios_previos():
        # Lógica para listar estudios previos
        return jsonify({"message": "Lista de estudios previos"})

# Clase para las rutas de Catálogos
class CatalogosRoutes:
    blueprint = Blueprint('catalogos', __name__)

    @staticmethod
    @blueprint.route('/catalogos/localidades', methods=['GET'])
    def listar_catalogos_localidades():
        try:
            # Obtener una conexión del pool
            connection = pool.connection()
            cursor = connection.cursor()
            
            # Ejecutar la consulta para obtener todos los pacientes
            query = "SELECT * FROM localidades"
            cursor.execute(query)
            localidades = cursor.fetchall()
            
            # Retornar los pacientes en formato JSON
            return jsonify(localidades)
        except Exception as e:
            # Manejo de errores
            return jsonify({"error": str(e)}), 500
        finally:
            # Asegurarse de cerrar el cursor y la conexión
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()
    
    @staticmethod
    @blueprint.route('/catalogos/obras-sociales', methods=['GET'])
    def listar_catalogos_obras_sociales():
        try:
            # Obtener una conexión del pool
            connection = pool.connection()
            cursor = connection.cursor()
            
            # Ejecutar la consulta para obtener todos los pacientes
            query = "SELECT * FROM obras_sociales"
            cursor.execute(query)
            obras_sociales = cursor.fetchall()
            
            # Retornar los pacientes en formato JSON
            return jsonify(obras_sociales)
        except Exception as e:
            # Manejo de errores
            return jsonify({"error": str(e)}), 500
        finally:
            # Asegurarse de cerrar el cursor y la conexión
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()
    
    @staticmethod
    @blueprint.route('/catalogos/medicos', methods=['GET'])
    def listar_catalogos_medicos():
        try:
            # Obtener una conexión del pool
            connection = pool.connection()
            cursor = connection.cursor()
            
            # Ejecutar la consulta para obtener todos los pacientes
            query = "SELECT * FROM medicos"
            cursor.execute(query)
            medicos = cursor.fetchall()
            
            # Retornar los pacientes en formato JSON
            return jsonify(medicos)
        except Exception as e:
            # Manejo de errores
            return jsonify({"error": str(e)}), 500
        finally:
            # Asegurarse de cerrar el cursor y la conexión
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

    @staticmethod
    @blueprint.route('/catalogos/tipos-estudios', methods=['GET'])
    def listar_catalogos_tipos_estudios():
        try:
            # Obtener una conexión del pool
            connection = pool.connection()
            cursor = connection.cursor()
            
            # Ejecutar la consulta para obtener todos los pacientes
            query = "SELECT * FROM tipos_estudios_previos"
            cursor.execute(query)
            tipos_estudios = cursor.fetchall()
            
            # Retornar los pacientes en formato JSON
            return jsonify(tipos_estudios)
        except Exception as e:
            # Manejo de errores
            return jsonify({"error": str(e)}), 500
        finally:
            # Asegurarse de cerrar el cursor y la conexión
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

# Clase para las rutas de Órdenes Médicas
class OrdenesRoutes:
    blueprint = Blueprint('ordenes', __name__)

    @staticmethod
    @blueprint.route('/ordenes', methods=['GET'])
    def formulario_crear_orden():
        # Renderizar el formulario para crear una nueva orden
        return render_template('crear_orden.html')

    @staticmethod
    @blueprint.route('/ordenes/<int:id>', methods=['GET'])
    def detalle_orden(id):
        try:
            connection = pool.connection()
            cursor = connection.cursor()

            # Obtener detalle de la orden
            query_orden = "SELECT * FROM ordenes WHERE id = %s"
            cursor.execute(query_orden, (id,))
            orden = cursor.fetchone()

            if not orden:
                return jsonify({"error": "Orden no encontrada"}), 404

            # Obtener citas asociadas
            query_citas = "SELECT * FROM citas WHERE orden_id = %s"
            cursor.execute(query_citas, (id,))
            citas = cursor.fetchall()

            return jsonify({"orden": orden, "citas": citas})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

    @staticmethod
    @blueprint.route('/ordenes', methods=['POST'])
    def crear_orden():
        try:
            data = request.json
            connection = pool.connection()
            cursor = connection.cursor()

            # Insertar nueva orden
            query = """
                INSERT INTO ordenes (paciente_id, fecha, descripcion, cantidad_sesiones)
                VALUES (%s, %s, %s, %s) RETURNING id
            """
            cursor.execute(query, (data['paciente_id'], data['fecha'], data['descripcion'], data['cantidad_sesiones']))
            orden_id = cursor.fetchone()[0]

            # Generar citas automáticamente si cantidad_sesiones > 0
            if data['cantidad_sesiones'] > 0:
                fecha_base = datetime.strptime(data['fecha'], '%Y-%m-%d')
                for i in range(data['cantidad_sesiones']):
                    fecha_cita = fecha_base.strftime('%Y-%m-%d')
                    query_cita = """
                        INSERT INTO citas (orden_id, fecha, estado)
                        VALUES (%s, %s, 'pendiente')
                    """
                    cursor.execute(query_cita, (orden_id, fecha_cita))
                    fecha_base += pd.Timedelta(days=7)  # Incrementar por 7 días

            connection.commit()
            return jsonify({"message": "Orden creada", "orden_id": orden_id})
        except Exception as e:
            connection.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

    @staticmethod
    @blueprint.route('/ordenes/<int:id>', methods=['PUT'])
    def editar_orden(id):
        try:
            data = request.json
            connection = pool.connection()
            cursor = connection.cursor()

            # Validar si ya hay citas generadas
            query_citas = "SELECT COUNT(*) FROM citas WHERE orden_id = %s"
            cursor.execute(query_citas, (id,))
            citas_count = cursor.fetchone()[0]

            if citas_count > 0:
                return jsonify({"error": "No se puede editar la orden porque ya hay citas generadas"}), 400

            # Actualizar la orden
            query = """
                UPDATE ordenes
                SET paciente_id = %s, fecha = %s, descripcion = %s, cantidad_sesiones = %s
                WHERE id = %s
            """
            cursor.execute(query, (data['paciente_id'], data['fecha'], data['descripcion'], data['cantidad_sesiones'], id))
            connection.commit()

            return jsonify({"message": "Orden actualizada"})
        except Exception as e:
            connection.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

    @staticmethod
    @blueprint.route('/ordenes/<int:id>', methods=['DELETE'])
    def anular_orden(id):
        try:
            connection = pool.connection()
            cursor = connection.cursor()

            # Cancelar citas pendientes asociadas a la orden
            query_citas = "UPDATE citas SET estado = 'cancelada' WHERE orden_id = %s AND estado = 'pendiente'"
            cursor.execute(query_citas, (id,))

            # Anular la orden
            query = "DELETE FROM ordenes WHERE id = %s"
            cursor.execute(query, (id,))
            connection.commit()

            return jsonify({"message": "Orden anulada y citas pendientes canceladas"})
        except Exception as e:
            connection.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

# Registro de blueprints en la aplicación
app.register_blueprint(PacientesRoutes.blueprint)
app.register_blueprint(MedicasRoutes.blueprint)
app.register_blueprint(CitasRoutes.blueprint)
app.register_blueprint(TratamientosDiagnosticosRoutes.blueprint)
app.register_blueprint(PagosRoutes.blueprint)
app.register_blueprint(EstudiosPreviosRoutes.blueprint)
app.register_blueprint(CatalogosRoutes.blueprint)
app.register_blueprint(OrdenesRoutes.blueprint)

@app.route('/')
def index():
    return render_template('index.html')