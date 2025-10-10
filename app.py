from flask import Flask, send_from_directory
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta

# Importamos los resources refiriendo al nuevo destino:
from resources.auth import Registro, Login
from resources.links import Links

app = Flask(__name__)
api = Api(app)

# Generamos una clave secreta para encriptar, y un tiempo de expiración de token
# Esto no debería estar aquí, sino en un archivo .env
app.config["JWT_SECRET_KEY"] = "supersecreto"  
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config['JWT_VERIFY_SUB'] = False

# Generamos un gestor de claves JWT con nuestra app.
jwt = JWTManager(app)

# Rutas:
api.add_resource(Registro, "/registro") # Ruta para cualquier request por post
api.add_resource(Login, "/login")       # Ruta para cualquier request por post

# Agregamos una nueva ruta. Acepta dos variantes: con o sin parámetro id_enlace
api.add_resource(Links, "/links", "/links/<int:id_enlace>")

# Rutas estáticas:
@app.route("/")
def serve_index():
    return send_from_directory("static", "login.html")

# Agregamos las dos nuevas direcciones de enrutamiento estático:
@app.route("/guardar_enlace")
def serve_guardar_enlace():
    return send_from_directory("static", "guardar_enlace.html")

@app.route("/enlaces")
def serve_enlaces():
    return send_from_directory("static", "enlaces.html")

if __name__ == "__main__":
    app.run(debug=True)
