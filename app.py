from flask import Flask, send_from_directory
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta

# Importamos los resources refiriendo al nuevo destino:
from resources.auth import Registro, Login
from resources.users import SoloParaUsuarios, SoloParaDocentes

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
api.add_resource(SoloParaUsuarios, "/soloparausuarios") # Ruta por GET para cualquier usuario autenticado
api.add_resource(SoloParaDocentes, "/soloparadocentes") # Ruta por GET para usuarios con role = "docente"

# Rutas estáticas:
@app.route("/")
def serve_index():
    return send_from_directory("static", "login.html")

@app.route("/usuarios")
def serve_usuarios():
    return send_from_directory("static", "usuarios.html")

@app.route("/docentes")
def serve_docentes():
    return send_from_directory("static", "docentes.html")

if __name__ == "__main__":
    app.run(debug=True)
