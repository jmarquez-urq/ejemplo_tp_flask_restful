from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

class SoloParaUsuarios(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {
            "message": f"Hola {current_user['username']}, este es un dato secreto para usuarios autenticados."
        }, 200

class SoloParaDocentes(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user["role"] != "docente":
            return {"message": "Acceso denegado: solo docentes"}, 403
        return {"message": "Bienvenido, profe."}, 200
