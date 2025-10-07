# Ejemplo de TP - Programación I

Este es un ejemplo de cómo empezar el TP de Programación I - 2do 2da

Se trata de un conjuntos de usuarios, cuyo rol puede ser `admin` o `user`

Cada usuario puede seguir a otros usuarios, tal como está definido en
`data/users.json`.

Un usuario puede ver los enlaces propios, y también los de aquellos usuarios que
sigue.

Un usuario con rol `user` solamente puede borrar enlaces propios. Un usuario
con rol `admin` puede borrar cualquier enlace.

Con el archivo `data/generar_usuarios.py` se puede generar los usuarios.

## Instalación

- Clonar el repositorio
- Crear entorno virtual con `python -m venv nombre_del_entorno` (o bien:
  `python3 -m venv nombre_del_entorno`
- Activar entorno virtual con `source nombre_del_entorno/bin/activate` (en
  GNU/Linux) o `.\nombre_del_entorno\Scripts\activate` (en Windows).
- Instalar las dependencias con `pip install flask flask-restful
  flask-jwt-extended bcrypt` (o bien: `pip3 install flask flask-restful
flask-jwt-extended bcrypt`)
- Generar el archivo de usuarios ingresando a la carpeta `data` y ejecutando
  `python generar_usuarios.py` (o bien: `python generar_usuarios.py`)
- Correr la aplicación con `python app.py` (o bien: `python3 app.py`)
- Acceder con el navegador a `localhost:5000` para utilizar la aplicación.
