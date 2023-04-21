import re
from flask import Blueprint, jsonify, request
from jinja2 import Undefined
from util.Connection import Connection
conexion = Connection()
empleados = Blueprint("empleados", __name__)
mysql = conexion.mysql

def empleadosQuitarCargo(idCargo):
    try:
        if id !=1 :
            sql = "UPDATE empleado SET idCargo = 1 WHERE idCargo=%s and idCargo != 2"
            conector = mysql.connect()
            cursor = conector.cursor()
            cursor.execute(sql, idCargo)
            conector.commit()
            
            mensaje = "El metodo delete se ha ejecutado exitosamente"
            exito = True
        else:
            mensaje = "El cargo con el id "+id+" no se puede eliminar"
            exito = False
    except Exception as ex:
        mensaje = "Ocurrio un error al eliminar el empleado gg"+repr(ex)
        exito = False
    return [mensaje, exito]


@empleados.route("/empleados/getCargo/<int:id>/", methods=["GET"])
def empleadoObtenerCargo(id):
    exito = True
    resultado = []
    try:
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, estado, idCargo FROM empleado WHERE idCargo = %s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                Datosempleados = {
                    "idEmpleado": fila[0],
                    "nombreEmpleado": fila[1],
                    "correoEmpleado": fila[2],
                    "estado": fila[3],
                    "idCargo": fila[4]
                }
                resultado.append(Datosempleados)
    except Exception as ex:
        resultado = "Ocurrio un error al realizar la consulta: " + repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

# LISTO
@empleados.route("/empleados/select/", methods=["GET"])
def empleadoSel():
    resultado = []
    exito = True
    try:
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, e.estado, c.nombreCargo FROM empleado as e INNER JOIN cargo as c ON e.idCargo = c.idCargo WHERE e.idCargo != 2 AND e.estado = 1;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                Datosempleados = {
                    "idEmpleado": fila[0],
                    "nombreEmpleado": fila[1],
                    "correoEmpleado": fila[2],
                    "estado": fila[3],
                    "nombreCargo": fila[4]
                }
                resultado.append(Datosempleados)
    except Exception as ex:
        resultado = "Ocurrio un error en la realizacion de la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})


@empleados.route("/admins/select/", methods=["GET"])
def empleadoAdminSel():
    resultado = []
    exito = True
    try:
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, estado, idCargo FROM empleado WHERE idCargo = 2 and estado = 1;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                Datosempleados = {
                    "idEmpleado": fila[0],
                    "nombreEmpleado": fila[1],
                    "correoEmpleado": fila[2],
                    "estado": fila[3],
                    "idCargo": fila[4]
                }
                resultado.append(Datosempleados)
    except Exception as ex:
        resultado = "Ocurrio un error en la realizacion de la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

def empleadoObtener(id):
    exito = True
    try:
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, estado, idCargo FROM empleado WHERE idEmpleado=%s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        dato = cursor.fetchone()
        if dato != None:
            resultado = {
                "idEmpleado": dato[0],
                "nombreEmpleado": dato[1],
                "correoEmpleado": dato[2],
                "estado": dato[3],
                "idCargo": dato[4],
            }
        else:
            resultado = "No se ha encontrado al empleado"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error al realizar la consulta"
        exito = False
    return [resultado, exito]

# LISTO
@empleados.route("/empleados/get/<int:id>/", methods=["GET"])
def empleadoGet(id):
    objeto = empleadoObtener(id)
    resultado = objeto[0]
    exito = objeto[1]
    return jsonify({"resultado": resultado, "exito": exito})

# LISTO
@empleados.route("/empleados/corroborar/", methods=["POST"])
def empleadoCorroborar():
    exito = True
    id = request.form["id"]
    passwordEmpleado = strip_tags(request.form["password"])
    try:
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, idCargo FROM empleado WHERE idEmpleado = %s and passwordEmpleado = AES_ENCRYPT(%s, %s);"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, [id, passwordEmpleado, passwordEmpleado])
        dato = cursor.fetchone()
        if dato != None:
            resultado = {
                "idEmpleado": dato[0],
                "nombreEmpleado": dato[1],
                "correoEmpleado": dato[2],
                "idCargo": dato[3],
            }
        else:
            resultado = "Contraseña incorrecta"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error al realizar la consulta "+repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})


@empleados.route("/empleados/delete/<int:id>/", methods=["PUT"])
def empleadoDelete(id):
    try:
        sql = "UPDATE empleado SET estado = 0, idCargo = 1 WHERE idEmpleado = %s"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        conector.commit()
        mensaje = "El metodo delete se ha ejecutado exitosamente"
        exito = True
    except Exception as ex:
        mensaje = "Ocurrio un error al eliminar el empleado ddd"+repr(ex)
        exito = False
    return jsonify({"resultado": mensaje, "exito": exito})

# MI SELECT DEBE DE TENER PARA AUQELLOS QUE EL ESTADO SEA 1(OSEA ACTIVO)
# LISTO
def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)

@empleados.route("/empleados/create/", methods=["POST"], defaults={"id":None})
@empleados.route("/empleados/create/<int:id>/", methods=["POST"])
def empleadoInsert(id):
    try:
        if id != None:
            idCargo = 2
        else:
            idCargo = request.form["txtidCargo2"]
        nombreEmpleado = request.form["txtnombreEmpleado2"]
        correoEmpleado = request.form["txtcorreoEmpleado2"]
        passwordEmpleado = request.form["txtpasswordEmpleado2"]
        
        nombreEmpleado = strip_tags(nombreEmpleado)
        correoEmpleado = strip_tags(correoEmpleado)
        passwordEmpleado = strip_tags(passwordEmpleado)
        datos = [
            nombreEmpleado,
            correoEmpleado,
            passwordEmpleado,
            passwordEmpleado,
            idCargo,
        ]
        mensaje = ""
        sql = "INSERT INTO empleado(nombreEmpleado, correoEmpleado, passwordEmpleado, idCargo) VALUES(%s, %s, AES_ENCRYPT(%s,%s), %s);"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
        mensaje = "Insertado correctamente"
    except Exception as ex:
        mensaje = "Error en la ejecucion "+repr(ex)
    return jsonify({"mensaje": mensaje})


@empleados.route("/empleados/update/<int:id>/", methods=["PUT"])
def empleadoUpdate(id):
    try:
        nombreEmpleado = request.form["txtnombreEmpleado"]
        correoEmpleado = request.form["txtcorreoEmpleado"]
        passwordEmpleado = request.form["txtpasswordEmpleado"]
        idCargo = request.form["txtidCargo"]

        nombreEmpleado = strip_tags(nombreEmpleado)
        correoEmpleado = strip_tags(correoEmpleado)

        datos = [
            nombreEmpleado,
            correoEmpleado,
            idCargo,
            id
        ]

        sql = "UPDATE empleado SET nombreEmpleado = %s, correoEmpleado = %s,"

        if passwordEmpleado.strip() != "":
            passwordEmpleado = strip_tags(passwordEmpleado)
            sql += "passwordEmpleado = AES_ENCRYPT(%s, %s),"
            datos.insert(2, passwordEmpleado)
            datos.insert(2,passwordEmpleado)
        
        sql += "idCargo = %s WHERE idEmpleado=%s;"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
        mensaje = ""
    except Exception as ex:
        mensaje = "Error en la ejecucion" + repr(ex)
    return jsonify({"mensaje": mensaje})


@empleados.route("/empleados/loginget/<int:id>/", methods=["GET"])
def empleadoLoginGet(id):
    exito = True
    try:
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, e.estado, nombreCargo FROM empleado as e INNER JOIN cargo as c ON e.idCargo = c.idCargo WHERE idEmpleado=%s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        dato = cursor.fetchone()
        if dato != None:
            resultado = {
                "idEmpleado": dato[0],
                "nombreEmpleado": dato[1],
                "correoEmpleado": dato[2],
                "estado": dato[3],
                "nombreCargo": dato[4],
            }
        else:
            resultado = "No se ha encontrado al empleado"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error al realizar la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

@empleados.route('/empleados/login/', methods = ['POST'])
def loginCreate():
    exito = True
    try:
        _correo = request.form['txtCorreo']
        _correo = strip_tags(_correo)
        _password = request.form['txtPassword']
        _password = strip_tags(_password)
        sql = "SELECT idEmpleado, nombreEmpleado, correoEmpleado, idCargo FROM empleado WHERE correoEmpleado = %s AND passwordEmpleado = AES_ENCRYPT(%s, %s);"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, (_correo, _password, _password))
        dato = cursor.fetchone()
        if dato != None:
            resultado = {
                "idEmpleado": dato[0],
                "nombreEmpleado": dato[1],
                "correoEmpleado": dato[2],
                "idCargo": dato[3]
            }
        else:
            resultado = "Usuario o contraseña incorrecta"
            exito = False
    except Exception as ex:
        exito = False
        resultado = "Ocurrio un error al consultar el empleado"
    return jsonify({'resultado':resultado, 'exito':exito})