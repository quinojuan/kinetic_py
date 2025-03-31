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
    @blueprint.route('/pacientes/crear', methods=['GET'])
    def formulario_crear_paciente():
        # Renderizar el formulario para crear un nuevo paciente
        return render_template('crear_paciente.html')

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
        try:
            # Obtener los datos del paciente desde el cuerpo de la solicitud
            data = request.json
            print("DATA DEL FORMULARIO: ", data)  # Depuración
            required_fields = ['dni', 'nombre', 'apellido']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({"error": f"El campo '{field}' es obligatorio"}), 400

            # Conexión a la base de datos
            connection = pool.connection()
            cursor = connection.cursor()

            # Insertar el nuevo paciente
            query = """
                INSERT INTO pacientes (
                    id_obra_social, dni, nombre, segundo_nombre, apellido, telefono, 
                    id_localidad, actividad_laboral, fecha_nacimiento
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data.get('id_obra_social'), data['dni'], data['nombre'], data.get('segundo_nombre'),
                data['apellido'], data.get('telefono'), data.get('id_localidad'),
                data.get('actividad_laboral'), data.get('fecha_nacimiento')
            ))
            
            # Obtener el ID del último registro insertado
            id_paciente = cursor.lastrowid
            print(id_paciente)  # Depuración
            connection.commit()
            return jsonify({"message": "Paciente creado", "id_paciente": id_paciente}), 201
        except Exception as e:
            if 'connection' in locals() and connection:
                connection.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

    @staticmethod
    @blueprint.route('/pacientes/buscar', methods=['GET'])
    def buscar_paciente_por_dni():
        try:
            # Obtener el parámetro de búsqueda (DNI)
            dni = request.args.get('dni', '').strip()
            if not dni:
                return jsonify({"error": "Debe proporcionar un DNI"}), 400

            # Conexión a la base de datos
            connection = pool.connection()
            cursor = connection.cursor()

            # Consulta SQL para buscar el paciente por DNI
            query = """
                SELECT id_paciente, id_obra_social, dni, nombre, segundo_nombre, apellido, 
                       telefono, id_localidad, actividad_laboral, fecha_nacimiento
                FROM pacientes
                WHERE dni = %s
            """
            cursor.execute(query, (dni,))
            paciente = cursor.fetchone()

            # Si no se encuentra el paciente, retornar un mensaje
            if not paciente:
                return jsonify({"message": "Paciente no encontrado"}), 404

            # Retornar los datos del paciente
            return jsonify({
                "id_paciente": paciente[0],
                "id_obra_social": paciente[1],
                "dni": paciente[2],
                "nombre": paciente[3],
                "segundo_nombre": paciente[4],
                "apellido": paciente[5],
                "telefono": paciente[6],
                "id_localidad": paciente[7],
                "actividad_laboral": paciente[8],
                "fecha_nacimiento": paciente[9]
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

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
    def listar_diagnostioos():
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

    @staticmethod
    @blueprint.route('/catalogos/diagnosticos', methods=['GET'])
    def listar_catalogos_diagnosticos():
        try:
            # Obtener el parámetro de búsqueda
            query_param = request.args.get('q', '').lower()
            print("Término de búsqueda recibido:", query_param)  # Depuración
            if not query_param:
                return jsonify([])  # Retornar una lista vacía si no hay término de búsqueda

            # Formatear el término de búsqueda con comodines
            search_term = f"%{query_param}%"
            print("Término de búsqueda con comodines:", search_term)  # Depuración

            # Conexión a la base de datos
            connection = pool.connection()
            print("Conexión al pool establecida correctamente")  # Depuración
            cursor = connection.cursor()

            # Consulta SQL con placeholders
            query = """
                SELECT id_diagnostico_cie10, codigo_diagnostico, nombre
                FROM diagnosticos_cie10
                WHERE LOWER(nombre) LIKE %s OR LOWER(codigo_diagnostico) LIKE %s
                LIMIT 20
            """
            print("Consulta SQL:", query)  # Depuración
            print("Parámetros:", (search_term, search_term))  # Depuración

            # Ejecutar la consulta
            cursor.execute(query, (search_term, search_term))
            diagnosticos = cursor.fetchall()
            print("Resultados de la consulta:", diagnosticos)  # Depuración

            # Manejo de resultados
            if not diagnosticos:
                return jsonify({"message": "No se encontraron diagnósticos"}), 404

            # Retornar los resultados
            return jsonify(diagnosticos)
        except Exception as e:
            # Manejo de errores
            print("Error específico:", type(e).__name__, str(e))  # Depuración
            return jsonify({"error": str(e)}), 500
        finally:
            # Cerrar cursor y conexión
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

    @staticmethod
    @blueprint.route('/catalogos/pacientes', methods=['GET'])
    def listar_catalogos_pacientes():
        try:
            # Obtener el parámetro de búsqueda
            query_param = request.args.get('q', '').lower()
            if not query_param:
                return jsonify([])  # Retornar una lista vacía si no hay término de búsqueda

            # Formatear el término de búsqueda con comodines
            search_term = f"%{query_param}%"

            # Conexión a la base de datos
            connection = pool.connection()
            cursor = connection.cursor()

            # Consulta SQL para buscar pacientes por nombre o apellido
            query = """
                SELECT id_paciente, nombre, apellido
                FROM pacientes
                WHERE LOWER(nombre) LIKE %s OR LOWER(apellido) LIKE %s
                LIMIT 20
            """
            cursor.execute(query, (search_term, search_term))
            pacientes = cursor.fetchall()
            print("Resultados de la consulta:", pacientes)  # Depuración

            return jsonify(pacientes)
        except Exception as e:
            print("Error en listar_catalogos_pacientes:", str(e))  # Depuración
            return jsonify({"error": str(e)}), 500
        finally:
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
        connection = None  # Inicializar la variable connection
        cursor = None  # Inicializar la variable cursor
        try:
            data = request.json
            print("DATA DEL FORMULARIO: ", data)  # Depuración

            # Obtener una conexión del pool
            connection = pool.connection()
            cursor = connection.cursor()

            # Insertar nueva orden
            query = """
                INSERT INTO ordenes (
                    id_paciente, fecha, descripcion, cantidad_sesiones, 
                    id_medico_solicitante, id_diagnostico_cie10, aplica_obra_social, 
                    fecha_lesion, fecha_cirugia, tipo_de_lesion, trajo_orden
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data['id_paciente'], data['fecha'], data['descripcion'], data['cantidad_sesiones'],
                data['id_medico_solicitante'], data['id_diagnostico_cie10'], data['aplica_obra_social'],
                data['fecha_lesion'], data['fecha_cirugia'], data['tipo_de_lesion'], data['trajo_orden']
            ))

            # Obtener el ID del último registro insertado
            cursor.execute("SELECT LAST_INSERT_ID()")
            orden_id = cursor.fetchone()[0]

            connection.commit()
            return jsonify({"message": "Orden creada", "orden_id": orden_id})
        except Exception as e:
            if connection:
                connection.rollback()  # Revertir cambios si ocurre un error
            print("Error en crear_orden:", str(e))  # Depuración
            return jsonify({"error": str(e)}), 500
        finally:
            # Cerrar cursor y conexión si existen
            if cursor:
                cursor.close()
            if connection:
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