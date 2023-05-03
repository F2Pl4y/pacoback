import re
from flask import Blueprint, jsonify, request
from util.Connection import Connection
import os

conexion = Connection()
categorias = Blueprint("categorias", __name__)
mysql = conexion.mysql

def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)

@categorias.route("/categorias/select/", methods = ["GET"])
def categoriasSelect():
    resultado = []
    exito = True
    try:
        sql = "SELECT idCategoria, nombreCategoria, estado FROM categoria WHERE idCategoria != 1 and estado = 1;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                categoria = {
                    "idCategoria": fila[0],
                    "nombreCategoria": fila[1],
                    "estado": fila[2]
                }
                resultado.append(categoria)
    except Exception as ex:
        resultado = "Ocurrio un error: " + repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

@categorias.route("/categorias/get/<int:id>/", methods=["GET"])
def cargosGet(id):
    resultado = obtenerCategoria(id)
    return jsonify({"resultado": resultado[0], "exito": resultado[1]})

def obtenerCategoria(id):
    exito = True
    try:
        sql = "SELECT idCategoria, nombreCategoria FROM categoria WHERE idCategoria=%s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        dato = cursor.fetchone()
        if dato != None:
            resultado = {
                "idCategoria": dato[0],
                "nombreCategoria": dato[1]
            }
        else:
            resultado = "No se ha encontrado al empleado"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error: "+repr(ex)
        exito = False
    return [resultado, exito]


def cambiarRutaFotoPlatillos(categoria):
    print(categoria["nombreCategoria"])


@categorias.route("/categorias/create/", methods=["POST"])
# @categorias.route("/categorias/create/", methods=["POST"], defaults={"id":None})
# @categorias.route("/categorias/create/<int:id>/", methods=["POST"])
# def empleadoInsert(id):
def empleadoInsert():
    try:
        # if id != None:
        #     idCargo = 2
        # else:
        #     idCargo = request.form["txtidCargo2"]
        nombreCategoria = request.form["txtnombreCategoriaInsert"]
        
        nombreCategoria = strip_tags(nombreCategoria)
        datos = [
            nombreCategoria
        ]
        mensaje = ""
        sql = "INSERT INTO categoria(nombreCategoria) VALUES(%s);"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
        mensaje = "Insertado correctamente"
    except Exception as ex:
        mensaje = "Error en la ejecucion listcateg "+repr(ex)
    return jsonify({"mensaje": mensaje})

@categorias.route("/categorias/update/<int:id>/", methods=["PUT"])
def empleadoUpdate(id):
    try:
        UPDcategoria1 = request.form["txtnombreCategoria"]
        UPDcategoria1 = strip_tags(UPDcategoria1)

        datos = [
            UPDcategoria1,
            id
        ]

        sql = "UPDATE categoria SET nombreCATEGORIA = %s WHERE idCategoria=%s;"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
        mensaje = "creo que funciono xd"
    except Exception as ex:
        mensaje = "Error en la ejecucion" + repr(ex)
    return jsonify({"mensaje": mensaje})

@categorias.route("/categorias/disable/<int:id>/", methods=["PUT"])
def empleadoDisable(id):
    try:
        # UPDcategoria1 = request.form["txtnombreCategoria"]
        # UPDcategoria1 = strip_tags(UPDcategoria1)

        datos = [
            # UPDcategoria1,
            id
        ]

        sql = "UPDATE categoria SET estado = 0 WHERE idCategoria=%s;"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
        mensaje = "creo que funciono xd"
    except Exception as ex:
        mensaje = "Error en la ejecucion" + repr(ex)
    return jsonify({"mensaje": mensaje})

@categorias.route("/categorias/corroborar/", methods=["POST"])
def empleadoCorroborar():
    exito = True
    id = request.form["id"]
    # passwordEmpleado = strip_tags(request.form["password"])
    try:
        sql = "SELECT idCategoria, nombreCategoria, estado FROM categoria WHERE idCategoria = %s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        dato = cursor.fetchone()
        if dato != None:
            resultado = {
                "idCategoria": dato[0],
                "nombreCategoria": dato[1],
                "estado": dato[2],
            }
        else:
            resultado = "datos categoria corroborar ERROR"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error al realizar la consulta "+repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})
