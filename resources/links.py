import json
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

archivo_de_usuarios = "data/users.json"
archivo_de_enlaces = "data/enlaces.json"

# Funciones auxiliares
def cargar_archivo(archivo):
    '''Interpreta el contenido de un archivo json y lo retorna'''
    with open(archivo, "r") as f:
        return json.load(f)

def guardar_enlaces(enlaces):
    '''Escribe el contenido de los enlaces en el archivo'''
    with open(archivo_de_enlaces, "w") as f:
        json.dump(enlaces, f, indent=4, ensure_ascii = False)

def obtener_siguiente_id(enlaces):
    '''Indica cuál es el id del próximo enlace a guardar (el id más grande del
    archivo más 1)'''
    ids = []
    for e in enlaces:
        ids.append(e.get("id"))
    return max(ids) + 1

def puede_borrar_enlace(enlace, usuario):
    '''Retorna True si el usuario puede borrar en enlace, False si no puede. Un
    usuario puede borrar un enlace cuando es el autor, o cuando tiene rol admin'''
    if usuario.get('role') == 'admin':
        return True
    elif usuario.get('username') == enlace.get('autor'):
        return True
    else:
        return False

# Resource Links:
class Links(Resource):
    @jwt_required()
    def get(self):
        """Retorna una lista de los links a mostrar"""
        usuario_logueado = get_jwt_identity()
        nombre_usuario = usuario_logueado.get("username")

        try:
            usuarios = cargar_archivo(archivo_de_usuarios)
            usuarios_que_sigue = usuarios.get(nombre_usuario).get("sigue_a")

            enlaces = cargar_archivo(archivo_de_enlaces)
        except:
            return {"message": "Error al leer los archivos"}, 500

        enlaces_a_retornar = []
        for e in enlaces:
            if e.get("autor") in usuarios_que_sigue:
                # Determinamos si el usuario actual puede borrar este enlace:
                e['borrable'] = puede_borrar_enlace(e, usuario_logueado)
                # y lo agregamos a la lista de enlaces a retornar
                enlaces_a_retornar.append(e)

        return {"enlaces": enlaces_a_retornar}, 200

    @jwt_required()
    def post(self):
        '''Genera un nuevo enlace según lo recibido por POST en el body. El
        autor del enlace será el usuario logueado'''

        # Recibimos el body del POST y lo guardamos en variables:
        data = request.get_json()
        url = data.get("url")
        titulo = data.get("titulo")
        descripcion = data.get("descripcion")

        # Si la URL o el título están vacíos, falla:
        if not url or not titulo:
            return {"message": "Debe incluir título y URL"}, 400

        # Obtenemos la identidad del usuario logueado para guardar como autor:
        usuario_logueado = get_jwt_identity()
        autor = usuario_logueado.get("username")
        
        # Cargamos el archivo con los enlaces
        try:
            enlaces = cargar_archivo(archivo_de_enlaces)
        except:
            return {"message": "Error al acceder al archivo de enlaces"}, 500

        # Obtenemos el próximo id
        siguiente_id = obtener_siguiente_id(enlaces)

        # Agregamos a la lista de enlaces obtenida el enlace recibido por POST:
        enlaces.append({
            "id": siguiente_id,
            "url": url,
            "titulo": titulo,
            "descripcion": descripcion,
            "autor": autor
        })

        # Escribimos en el archivo de enlaces y retornamos el mensaje de éxito
        try:
            guardar_enlaces(enlaces)
            return {"message": "Enlace registrado"}, 201
        except:
            return {"message": "Error al escribir el archivo de enlaces"}, 500

    @jwt_required()
    def delete(self, id_enlace):
        '''Elimina el enlace cuyo id recibimos. Esta función requiere que el
        request llegue por DELETE con un id enlace para borrar.'''

        # Obtenemos el nombre del usuario logueado
        current_user = get_jwt_identity()

        # Cargamos el archivo con los enlaces:
        try:
            enlaces = cargar_archivo(archivo_de_enlaces)
        except:
            return {"message": "Error al acceder al archivo de enlaces"}, 500

        # Buscamos cuál es el enlace que se quiere eliminar:
        enlace_a_eliminar = None
        for enlace in enlaces:
            if enlace.get("id") == id_enlace:
                enlace_a_eliminar = enlace
                break

        # Si no encontramos el enlace, indicamos el error 404
        if not enlace_a_eliminar:
            return {"message": "No se encontró en enlace a eliminar"}, 404

        # Validamos que el usuario pueda borrar:
        if puede_borrar_enlace(enlace_a_eliminar, current_user):
            # Eliminamos el enlace ...
            enlaces.remove(enlace)
            # ...y escribimos el archivo con la lista, que tendrá un elemento menos
            try:
                guardar_enlaces(enlaces)
                return {"message": "Enlace eliminado correctamente"}, 204
            except:
                return {"message": "Error al escribir el archivo de enlaces"}, 500
        else:
            # Si no tenemos permiso de eliminar, retornamos 403
            return {"message": "No tiene permiso para eliminar el mensaje"}, 403

