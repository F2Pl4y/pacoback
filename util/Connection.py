# conexion entre la aplicacion y la base de datos
from flaskext.mysql import MySQL
from util.Aplication import Aplication

class Connection():

    def __init__(self):
        aplication = Aplication()
        app = aplication.app
        self.mysql = MySQL()
        self.mysql.init_app(app)