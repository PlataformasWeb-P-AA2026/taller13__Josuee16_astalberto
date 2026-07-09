from flask import Flask, render_template
import requests
import json
from config import usuario, clave

app = Flask(__name__, template_folder='templates')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/losestudiantes")
def los_estudiantes():
    """
    """
    r = requests.get("http://127.0.0.1:8000/api/estudiantes/",
            auth=(usuario, clave))
    estudiantes = json.loads(r.content)['results']
    numero_estudiantes = json.loads(r.content)['count']
    return render_template("losestudiantes.html", estudiantes=estudiantes,
    numero_estudiantes=numero_estudiantes)


@app.route("/lostelefonos")
def los_telefonos():
    """
    """
    r = requests.get("http://127.0.0.1:8000/api/numerost/",
            auth=(usuario, clave))
    datos = json.loads(r.content)['results']
    numero = json.loads(r.content)['count']
    return render_template("lostelefonos.html", datos=datos,
    numero=numero)


@app.route("/lostelefonosdos")
def los_telefonos_dos():
    """
    """
    r = requests.get("http://127.0.0.1:8000/api/numerost/",
            auth=(usuario, clave))
    datos = json.loads(r.content)['results']
    numero = json.loads(r.content)['count']
    datos2 = []
    for d in datos:
        datos2.append({'telefono':d['telefono'], 'tipo':d['tipo'],
        'estudiante': obtener_estudiante(d['estudiante'])})
    return render_template("lostelefonosdos.html", datos=datos2,
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
