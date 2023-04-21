import re
from flask import Blueprint, jsonify, request, make_response
from model.venta_routes import ventaInsert, ventaActual, ventasAumento
from model.platillos_routes import platilloGetInterno
from util.Connection import Connection

conexion = Connection()
pedido = Blueprint("pedido", __name__)
mysql = conexion.mysql

def detallePedidoDelete(idPedido):
    try:
        sql = "DELETE FROM detallePedido WHERE idPedido = %s"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, idPedido)
        conector.commit()
        mensaje = "El metodo delete se ha ejecutado exitosamente"
        exito = True
    except Exception as ex:
        mensaje = "Ocurrio un error al eliminar los detalles pedido "+repr(ex)
        exito = False
    return [mensaje, exito]

@pedido.route("/pedido/selectEmp/<int:id>/", methods=["GET"])
def pedidoEmpleado(id):
    resultado = []
    exito = True
    try:
        sql = "SELECT idPedido, nombreCliente, estado, costoTotal, idEmpleado, p.idVenta FROM pedido as p inner join venta as v on p.idVenta = v.idVenta WHERE v.fecha = curdate() and idEmpleado = %s"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                venta = {
                    "idPedido": fila[0],
                    "nombreCliente": fila[1],
                    "estado": fila[2],
                    "costoTotal": fila[3],
                    "idEmpleado": fila[4],
                    "idVenta": fila[5]
                }
                resultado.append(venta)
    except Exception as ex:
        resultado = "Ocurrio un error " + repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

@pedido.route("/pedido/delete/<int:idPedido>/", methods=["DELETE"])
def pedidoDelete(idPedido):
    try:
        resultado = detallePedidoDelete(idPedido)
        if resultado[1] == True:
            sql = "DELETE FROM pedido WHERE idPedido = %s"
            conector = mysql.connect()
            cursor = conector.cursor()
            cursor.execute(sql, idPedido)
            conector.commit()
            mensaje = "El metodo delete se ha ejecutado exitosamente"
            exito = True
        else:
            mensaje = resultado[0]
            exito = resultado[1]
    except Exception as ex:
        mensaje = "Ocurrio un error al eliminar el pedido "+repr(ex)
        exito = False
    return jsonify({"resultado": mensaje, "exito": exito})

def pedidoInsert(detalle, cliente, idEmpleado):
    try:
        mensaje = None
        venta = ventaActual()
        if type(venta) == str:
            mensaje = ventaInsert()
            venta = ventaActual()

        costoTotal = 0
        detalle = detalle.split(",")
        for i in range(len(detalle)):
            if i % 2 != 0:
                continue
            platillo = platilloGetInterno(detalle[i])
            costoTotal += platillo[0]["precio"] * int(detalle[i+1])
        idVenta = venta[0]
        sql = "INSERT INTO pedido(nombreCliente, costoTotal, idEmpleado, idVenta) VALUES (%s, %s, %s, %s)"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, [cliente, costoTotal, idEmpleado, idVenta])
        conn.commit()
        mensaje = None
        exito = True
    except Exception as ex:
        mensaje = "Ocurrio un error al insertar el pedido "+repr(ex)
        exito = False
    return [mensaje, exito]

@pedido.route("/pedido/update/<int:idPedido>/", methods=["PUT"])
def pedidoUpdate(idPedido):
    try:
        sql = "SELECT costoTotal FROM pedido WHERE idPedido = %s"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, idPedido)
        costo = cursor.fetchone()
        mensaje = ventasAumento(costo[0])

        if mensaje == None:
            sql = "UPDATE pedido SET estado = 1 WHERE idPedido = %s"
            cursor.execute(sql, idPedido)
            conn.commit()
    except Exception as ex:
        mensaje = "Error al actualizar el pedido "+repr(ex)
    return jsonify({"mensaje":mensaje})
