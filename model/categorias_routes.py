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
        sql = "SELECT idCategoria, nombreCategoria FROM categoria WHERE idCategoria != 1"
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
                    "nombreCategoria": fila[1]
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


@categorias.route("/categorias/update/<int:id>/", methods=["PUT"])
@categorias.route("/categorias/create/", methods=["POST"], defaults={"id":None})
def categoriasInsert(id):
    categoria = obtenerCategoria(id)
    try:
        nombreCategoria = request.form["txtNombreCategoria"]
        nombreCategoria = strip_tags(nombreCategoria)
        mensaje = ""
        if nombreCategoria != None:
            parametros = [nombreCategoria]
            if id == None:
                sql = "INSERT INTO categoria(nombreCategoria) VALUES (%s)"
                os.mkdir('upload/images/'+nombreCategoria)
            else:
                if id == 1:
                    mensaje = "Esta categoría no se puede modificar"
                else:
                    sql = "UPDATE categoria SET nombreCategoria = %s WHERE idCategoria = %s"
                    parametros.append(id)
                    os.rename("upload/images/"+categoria[0]["nombreCategoria"], "upload/images/"+nombreCategoria)
            conector = mysql.connect()
            cursor = conector.cursor()
            cursor.execute(sql,parametros)
            conector.commit()
            if id != None and id != 1:
                cambiarRutaFotoPlatillos(categoria)
        else:
            mensaje = "Debe insertar el nombre de la categoria"
    except Exception as ex:
        mensaje = "Ocurrio un error " + repr(ex)
    return jsonify({"mensaje": mensaje})