from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json
from config import usuario, clave,token

app = Flask(__name__, template_folder='templates')

headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/losestudiantes")
def los_edificios():
    """
    """
    r = requests.get("http://127.0.0.1:8000/api/edificios/", headers=headers)
    edificios = json.loads(r.content)['results']
    numero_edificios = json.loads(r.content)['count']
    return render_template("losedificios.html", estudiantes=edificios,
    numero_estudiantes=numero_edificios)


@app.route("/losdepartamentos")
def los_departamentos():
    """
    """
    r = requests.get("http://127.0.0.1:8000/api/departamentos/",
            auth=(usuario, clave))
    datos = json.loads(r.content)['results']
    numero = json.loads(r.content)['count']
    return render_template("lostelefonos.html", datos=datos,
    numero=numero)

# funciones ayuda

def obtener_estudiante(url):
    """
    """
    r = requests.get(url, auth=(usuario, clave))
    nombre_estudiante = json.loads(r.content)['nombre']
    apellido_estudiante = json.loads(r.content)['apellido']
    cadena = "%s %s" % (nombre_estudiante, apellido_estudiante)
    return cadena


@app.route("/crear/estudiante", methods=['GET', 'POST'])
def agregar_estudiante():
    """
    """
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        correo = request.form['correo']

        # Datos a enviar a la API de Django
        estudiante_data = {
            'nombre': nombre,
            'apellido': apellido,
            'cedula': cedula,
            'correo': correo
        }


        # Realizar la petición POST a la API de Django
        r = requests.post("http://localhost:8000/api/estudiantes/",
                              json=estudiante_data, # 'json' serializa el diccionario a JSON automáticamente
                              headers=headers)


        print(f"Status Code (Crear Estudiante): {r.status_code}")
        # Si todo fue bien (código 201 Created), la API devuelve el objeto creado
        nuevo_estudiante = json.loads(r.content)
        flash(f"Estudiante '{nuevo_estudiante['nombre']} {nuevo_estudiante['apellido']}' creado exitosamente!", 'success')
        return redirect(url_for('los_estudiantes')) # Redirigir a la lista de estudiantes

    # Si es una petición GET o si hubo un error en POST, muestra el formulario
    return render_template("crear_estudiante.html")


@app.route("/crear/direccion", methods=['GET', 'POST'])
def crear_direccion():
    """
    """
    estudiantes_disponibles = []

    r_estudiantes = requests.get("http://localhost:8000/api/estudiantes/", headers=headers)
    estudiantes_disponibles = json.loads(r_estudiantes.content)['results']

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        tipo = request.form['tipo']

        estudiante_url = request.form['estudiante']

        direccion_data = {
            'descripcion': descripcion,
            'tipo': tipo,
            'estudiante': estudiante_url # Enviamos la URL del estudiante
        }

        r = requests.post("http://localhost:8000/api/direccion/",
                              json=direccion_data,
                              headers=headers)

        print(f"Status Code (Crear Direccion): {r.status_code}")

        direccion_nueva = json.loads(r.content)
        flash(f"Direccion '{direccion_nueva['descripcion']}' creado exitosamente para el estudiante!", 'success')
        return redirect(url_for('los_direcciones')) # Redirigir a la lista principal o a una de números

    return render_template("crear_direccion.html",
                           estudiantes=estudiantes_disponibles,
                           )

if __name__ == "__main__":
    app.run(debug=True)