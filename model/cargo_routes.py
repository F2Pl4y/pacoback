import re
from flask import Blueprint, jsonify, request
from util.Connection import Connection
from model.empleados_routes import empleadosQuitarCargo
conexion = Connection()
cargos = Blueprint("cargos", __name__)
mysql = conexion.mysql

# MI SELECT DEBE DE TENER PARA AUQELLOS QUE EL ESTADO SEA 1(OSEA ACTIVO)
# LISTO
def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)

@cargos.route("/cargos/delete/<int:id>/", methods=["DELETE"])
def cargosDelete(id):
    try:
        if id != 1:
            resultado = empleadosQuitarCargo(id)
            if resultado[1] == True:
                sql = "DELETE FROM cargo WHERE idCargo = %s"
                conector = mysql.connect()
                cursor = conector.cursor()
                cursor.execute(sql, id)
                conector.commit()
                mensaje = "El metodo delete se ha ejecutado exitosamente"
                exito = True
            else:
                mensaje = resultado[0]
        else:
            mensaje = "El cargo con el id "+id+" no se puede eliminar"
    except Exception as ex:
        mensaje = "Ocurrio un error al eliminar el cargo "+repr(ex)
        exito = False
    return jsonify({"resultado": mensaje, "exito": exito})

@cargos.route("/cargos/comprobar/<int:id>/", methods=["GET"])
def cargosComprobar(id):
    exito = True
    resultado = []
    try:
        sql = "SELECT * FROM cargo WHERE idCargo = %s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            resultado = "Si existen"
            exito = True
    except Exception as ex:
        resultado = "Ocurrio un error al realizar la consulta: " + repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

@cargos.route("/cargos/select/", methods=["GET"])
def cargosSel():
    resultado = []
    exito = True
    try:
        sql = "SELECT * FROM cargo"
        # conectarme a la BD
        conector = mysql.connect()
        # almacenar informacion
        cursor = conector.cursor()
        # ejecutar la sentencia
        cursor.execute(sql)
        # me duelve la informacion para poder imprimirla en donde necesite, por ejemplo en la terminal con un print(datos)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                Datosempleados = {
                    "idCargo": fila[0],
                    "nombreCargo": fila[1],
                }
                resultado.append(Datosempleados)
    except Exception as ex:
        resultado = "Ocurrio un error en la realizacion de la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

@cargos.route("/cargos/get/<int:id>/", methods=["GET"])
def cargosGet(id):
    exito = True
    try:
        sql = "SELECT idCargo, nombreCargo FROM cargo WHERE idCargo=%s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        dato = cursor.fetchone()
        if dato != None:
            resultado = {
                "idCargo2": dato[0],
                "nombreCargo2": dato[1]
            }
        else:
            resultado = "No se ha encontrado al empleado"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error al realizar la consulta"
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

@cargos.route("/cargos/create/", methods=["POST"], defaults={"id": None})
def cargosInsert(id):
    try:
        nombreCargo = request.form["txtnombreCargo"]
        nombreCargo = strip_tags(nombreCargo)
        datos = [
            nombreCargo
        ]
        mensaje = ""
        sql = ""
        if id == None:
            sql = "INSERT INTO cargo(nombreCargo) VALUES(%s);"
            mensaje = "Insertado correctamente"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
    except Exception as ex:
        mensaje = "Error en la ejecucion"
    return jsonify({"mensaje": mensaje})

@cargos.route("/cargos/update/<int:id>/", methods=["PUT"])
def cargosUpdate(id):
    try:
        nombreCargo = request.form["txtnombreCargo2"]
        nombreCargo = strip_tags(nombreCargo)
        datos = [
            nombreCargo,
        ]
        datos.append(id)
        mensaje = ""
        sql = ""
        sql = "UPDATE cargo SET nombreCargo = %s WHERE idCargo=%s;"
        mensaje = "Actualizado correctamente"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
    except Exception as ex:
        mensaje = "Error en la ejecucion"
    return jsonify({"mensaje": mensaje})