import re
from flask import Blueprint, jsonify, request, make_response
from util.Connection import Connection
import os
conexion = Connection()
platillos = Blueprint("platillos", __name__)
mysql = conexion.mysql


def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)


def platilloGetInterno(id):
    exito = True
    try:
        sql = "SELECT idProducto, nombreProducto, precio, imagen, descripcion, idCategoria FROM producto WHERE estado = 1 AND idProducto = %s"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        dato = cursor.fetchone()
        if dato != None:
            resultado = {
                "idProducto": dato[0],
                "nombreProducto": dato[1],
                "precio": dato[2],
                "imagen": dato[3],
                "descripcion": dato[4],
                "idCategoria": dato[5]
            }
        else:
            resultado = "No se ha encontrado el producto"
            exito = False
    except Exception as ex:
        resultado = "Ocurrio un error: "+repr(ex)
        exito = False
    return [resultado, exito]


@platillos.route("/platillos/selectCateg/<int:idCateg>/", methods=["GET"])
def platillosSelectCateg(idCateg):
    resultado = []
    exito = True
    try:
        sql = "SELECT idProducto, nombreProducto, precio, imagen, descripcion, idCategoria FROM producto WHERE estado = 1 and idCategoria = %s"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, idCateg)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                DatosProducto = {
                    "idProducto": fila[0],
                    "nombreProducto": fila[1],
                    "precio": fila[2],
                    "imagen": fila[3],
                    "descripcion": fila[4],
                    "idCategoria": fila[5]
                }
                resultado.append(DatosProducto)
    except Exception as ex:
        resultado = "Ocurrio un error " + repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})


@platillos.route("/platillos/select/", methods=["GET"])
def platillosSelect():
    resultado = []
    exito = True
    try:
        sql = "SELECT idProducto, nombreProducto, precio, imagen, descripcion, idCategoria FROM producto WHERE estado = 1;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                DatosProducto = {
                    "idProducto": fila[0],
                    "nombreProducto": fila[1],
                    "precio": fila[2],
                    "imagen": fila[3],
                    "descripcion": fila[4],
                    "idCategoria": fila[5]
                }
                resultado.append(DatosProducto)
    except Exception as ex:
        resultado = "Ocurrio un error " + repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})


@platillos.route("/platillos/get/<int:id>", methods=["GET"])
def platilloGet(id):
    dato = platilloGetInterno(id)
    return jsonify({"resultado": dato[0], "exito": dato[1]})


# cree la linea 107 15/04/23
CARPETAUP = os.path.join(r'../pacoback/upload/images/')
#
# CARPETAUP = os.path.join(r'upload/images/Piqueos/rolls.png')
# image_data = open("upload/images/"+categoria+"/"+imagen, "rb").read()+categoria+"/"+imagen
# @platillos.route("/platillos/foto/<string:categoria>/<string:imagen>", methods = ['GET'])
# acabo de crear la linea 108 15/4/23


@platillos.route("/platillos/foto/<string:categoria>/<string:imagen>", methods=['GET'])
# @platillos.route("/platillos/fotssso/", methods = ['GET'])
# def cargarImagenPlatillo(categoria, imagen):
# cree la linea 112 15/4/23
def cargarImagenPlatillo(categoria, imagen):
    # def cargarImagenPlatillo():
    try:
        # image_data = open("D:/Repositorios/itdFinalBack/upload/images/Piqueos/rolls.png", "rb").read()
        # image_data = open('itdFinalBack/upload/images/Piqueos/rolls.png', "rb").read()
        # image_data = open('D:/Repositorios/mibackEnd/upload/images/5/rolls.png', "rb").read()
        # image_data = open('upload/images/Piqueos/rolls.png', "rb").read()
        # image_data = open(CARPETAUP, "rb").read()
        # image_data = open('../mibackEnd/upload/images/Piqueos/rolls.png', "rb").read()
        # image_data = open('../upload/images/5/rolls.png', "rb").read()
        # resultado = make_response(image_data)
        # resultado.headers['Content-Type'] = 'image/png'
        # return resultado
        image_data = open(CARPETAUP+categoria+'/'+imagen, "rb").read()
        resultado = make_response(image_data)
        resultado.headers['Content-Type'] = 'image/png'
        return resultado
        # image_data = open('upload/images/5/rolls.png', "rb").read()
        # resultado = make_response(image_data)
        # resultado.headers['Content-Type'] = 'image/png'
        # return resultado
    except Exception as ex:
        return "falla: " + repr(ex)


@platillos.route("/platillos/delete/<int:id>/", methods=['PUT'])
def platillosDelete(id):
    try:
        sql = "UPDATE producto SET estado = 0 WHERE idProducto=%s;"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        conector.commit()
        mensaje = ""
        exito = True
    except Exception as ex:
        mensaje = "Ocurrio un error "+repr(ex)
        exito = False
    return jsonify({"resultado": mensaje, "exito": exito})


def platillosGetCategoria(id):
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


@platillos.route("/platillos/create/", methods=["POST"])
def platilloInsert():
    try:
        nombrePlatillo = request.form["txtNombrePlatillo"]
        precio = request.form["txtPrecio"]
        imagen = request.files['imagenPlatillo']
        descripcion = request.form["txtDescripcion"]
        idCategoria = request.form["txtIdCategoria"]

        nombrePlatillo = strip_tags(nombrePlatillo)
        precio = strip_tags(precio)
        descripcion = strip_tags(descripcion)
        idCategoria = strip_tags(idCategoria)

        if 'imagenPlatillo' in request.files:
            nombreCategoria = platillosGetCategoria(
                idCategoria)[0]["nombreCategoria"]
            ruta = nombreCategoria+"/"+imagen.filename
            imagen.save("upload/images/"+ruta)
            sql = "INSERT INTO producto(nombreProducto, precio, imagen, descripcion, idCategoria) VALUES (%s, %s, %s, %s, %s)"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, [nombrePlatillo, precio,
                           ruta, descripcion, idCategoria])
            conn.commit()
            mensaje = ""
        else:
            mensaje = "Es necesario que insertes una imagen"
    except Exception as ex:
        mensaje = "Error en la ejecucion "+repr(ex)
    return jsonify({"mensaje": mensaje})


@platillos.route("/platillos/update/<int:id>", methods=["PUT"])
def platilloUpdate(id):
    try:
        nombrePlatillo = request.form["txtNombrePlatillo"]
        precio = request.form["txtPrecio"]
        descripcion = request.form["txtDescripcion"]
        idCategoria = request.form["txtIdCategoria"]

        nombrePlatillo = strip_tags(nombrePlatillo)
        precio = strip_tags(precio)
        descripcion = strip_tags(descripcion)
        idCategoria = strip_tags(idCategoria)

        nombreCategoria = platillosGetCategoria(
            idCategoria)[0]["nombreCategoria"]
        if 'imagenPlatillo' in request.files:
            imagen = request.files['imagenPlatillo']
            sql = "UPDATE producto SET nombreProducto=%s, precio=%s, imagen=%s, descripcion=%s,idCategoria=%s WHERE idProducto=%s"
            ruta = nombreCategoria+"/"+imagen.filename
            datos = [nombrePlatillo, precio, ruta,
                     descripcion, idCategoria, id]
            imagen.save("upload/images/"+ruta)
        else:
            sql = "UPDATE producto SET nombreProducto=%s,precio=%s,descripcion=%s, idCategoria=%s WHERE idProducto=%s"
            datos = [nombrePlatillo, precio, descripcion, idCategoria, id]
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
        mensaje = ""
    except Exception as ex:
        mensaje = "Error en la ejecucion "+repr(ex)
    return jsonify({"mensaje": mensaje})
