from model.empleados_routes import empleados
from model.categorias_routes import categorias
from model.platillos_routes import platillos
from model.cargo_routes import cargos
from model.venta_routes import ventas
from model.pedido_routes import pedido
from model.detallepedido_routes import detallepedido
from util.Aplication import Aplication

aplication = Aplication()
app = aplication.app
app.register_blueprint(empleados)
app.register_blueprint(categorias)
app.register_blueprint(platillos)
app.register_blueprint(cargos)
app.register_blueprint(ventas)
app.register_blueprint(pedido)
app.register_blueprint(detallepedido)

def pagina_no_encontrada(error):
    return "<h1>Método no encontrado</h1>"
    
@app.route("/")
def ingreso():
    return "<h1>corriendo :)</h1>"

if __name__ == "__main__":
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)
