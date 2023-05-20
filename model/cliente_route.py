from flask import Blueprint, jsonify, request
from util.Connection import Connection

conexion = Connection()
cliente = Blueprint('cliente', __name__)
mysql = conexion.mysql

'''
Esta función lista todos los clientes del restaurante
Parámetros:
Retorna:
    json: Listado de clientes
'''
@cliente.route("/cliente/sel/", methods=["GET"])
def clienteSel():
    resultado = []
    exito = False
    try:
        sql = "SELECT CodCliente, CorreoCliente, DNI, NomCliente, TelefonoCliente  FROM cliente"
        conector = mysql.connect()
        cursor = conector.cursor()
        cursor.execute(sql)
        arreglo = cursor.fetchall()
        if arreglo.count == 0:
            resultado = "No hay datos en la tabla Cliente"
        else:
            for fila in arreglo:
                DatosCliente = {
                    "CodCliente": fila[0],
                    "CorreoCliente": fila[1],
                    "DNI": fila[2],
                    "NomCliente": fila[3],
                    "TelefonoCliente": fila[4]
                }
                resultado.append(DatosCliente)
            exito = True
    except Exception as e:
        resultado = f"Error: {e.__str__()}"
    return jsonify({"resultado": resultado, "exito": exito})