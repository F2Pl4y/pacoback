from datetime import datetime
import re
from flask import Blueprint, jsonify, request, make_response
from util.Connection import Connection

conexion = Connection()
ventas = Blueprint("ventas", __name__)
mysql = conexion.mysql

@ventas.route("/ventas/select/", methods=["GET"])
def ventasSelect():
    resultado = []
    exito = True
    try:
        sql = "SELECT idVenta, fecha, montoTotal FROM venta"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                venta = {
                    "idVenta": fila[0],
                    "fecha": fila[1],
                    "montoTotal": fila[2]
                }
                resultado.append(venta)
    except Exception as ex:
        resultado = "Ocurrio un error " + repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

def ventaActual():
    try:
        sql = "SELECT * FROM venta WHERE fecha = CURDATE()"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            resultado = [datos[0], datos[1], datos[2]]
        else:
            resultado = "No existe la fecha con la venta actual"
    except Exception as ex:
        resultado = "Ocurrio un error "+repr(ex)
    return resultado

def ventaInsert():
    try:
        sql = "INSERT INTO venta(fecha, montoTotal) VALUES(%s, %s)"
        fecha = datetime.today()
        montoTotal = 0
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, [fecha, montoTotal])
        conector.commit()
        mensaje = None
    except Exception as ex:
        mensaje = "Ocurrio un error "+repr(ex)
    return [mensaje]

def ventasAumento(subTotal):
    try:
        venta = ventaActual()
        venta[2] = venta[2] + subTotal
        sql = "UPDATE venta SET montoTotal = %s WHERE fecha = CURDATE()"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, venta[2])
        conector.commit()
        mensaje = None
    except Exception as ex:
        mensaje = "Error al realizar la consulta de ventas "+repr(ex)
    return mensaje