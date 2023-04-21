import re
from flask import Blueprint, jsonify, request
from model.pedido_routes import pedidoInsert
from model.platillos_routes import platilloGetInterno
from util.Connection import Connection

conexion = Connection()
detallepedido = Blueprint("detallepedido", __name__)
mysql = conexion.mysql


@detallepedido.route("/detallepedido/selectDetallePedido/<int:id>/", methods=["GET"])
def pedidoEmpleado(id):
    resultado = []
    exito = True
    try:
        sql = "SELECT idPedido, cantidad, CostoDetalle, p.nombreProducto, p.imagen FROM detallepedido as dp INNER JOIN producto as p ON dp.idProducto = p.idProducto WHERE idPedido = %s"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql, id)
        datos = cursor.fetchall()
        if datos.count == 0:
            resultado = "No existen datos en la tabla"
            exito = False
        else:
            for fila in datos:
                detallepedido = {
                    "idPedido": fila[0],
                    "cantidad": fila[1],
                    "costodetalle": fila[2],
                    "nombreProducto": fila[3],
                    "imagen": fila[4]
                }
                resultado.append(detallepedido)
    except Exception as ex:
        resultado = "Ocurrio un error " + repr(ex)
        exito = False
    return jsonify({"resultado": resultado, "exito": exito})

@detallepedido.route("/detallepedido/carritoDetalle/", methods=["POST"])
def detalleCarrito():
    arreglo = request.form["carrito"]
    lista = arreglo.split(",")
    resultado = []
    elemento = []
    for i in range(len(lista)):
        if i % 2 == 0:
            producto = platilloGetInterno(lista[i])
            elemento.append(producto[0]["idProducto"])
            elemento.append(producto[0]["nombreProducto"])
            elemento.append(producto[0]["imagen"])
            elemento.append(float(producto[0]["precio"]))
        else:
            elemento.append(int(lista[i]))
            precioTotal = elemento[4] * elemento[3]
            elemento.append(round(precioTotal, 2))
            resultado.append(elemento)
            elemento = []
    return jsonify({"resultado": resultado})


@detallepedido.route("/detallepedido/insert/", methods=["POST"])
def detalleInsert():
    try:
        detallePedido = []
        cliente = request.form["txtNombreCliente"]

        detalle = request.form["carrito"]
        idEmpleado = request.form["txtIdEmpleado"]

        mensaje = pedidoInsert(detalle, cliente, idEmpleado)

        detalle = detalle.split(",")

        # Obtener idPedido
        sql = "SELECT idPedido FROM pedido WHERE idEmpleado = %s ORDER BY idPedido DESC LIMIT 1"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, idEmpleado)
        idPedido = cursor.fetchone()

        print(type(idPedido[0]))

        # Obtener idProducto y cantidad
        for i in range(len(detalle)):
            print(detalle[i])
            if i % 2 != 0:
                continue
            elemento = [idPedido[0]]
            elemento.append(int(detalle[i]))
            elemento.append(int(detalle[i+1]))
            producto = platilloGetInterno(int(detalle[i]))
            costoDetalle = producto[0]["precio"] * int(detalle[i+1])
            elemento.append(costoDetalle)
            detallePedido.append(elemento)
        
        print(detallePedido)
        sql = "INSERT INTO detallepedido(idPedido, idProducto, cantidad, costoDetalle) VALUES (%s, %s, %s, %s)"
        for valor in detallePedido:
            cursor.execute(sql, valor)
        conn.commit()
        mensaje = "Se insertó el pedido exitosamente"
    except Exception as ex:
        mensaje = "Error en la insercion de detalle "+repr(ex)
    return jsonify({"mensaje": mensaje})
