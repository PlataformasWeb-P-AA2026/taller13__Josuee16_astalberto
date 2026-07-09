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

@app.route("/crear/edificio", methods=['GET', 'POST'])
def crear_edificio():
    """
    """
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        tipo = request.form['tipo']

        # Datos a enviar a la API de Django
        edificio_data = {
            'nombre': nombre,
            'direccion': direccion,
            'ciudad': ciudad,
            'tipo': tipo
        }


        # Realizar la petición POST a la API de Django
        r = requests.post("http://localhost:8000/api/edificio/",
                              json=edificio_data, # 'json' serializa el diccionario a JSON automáticamente
                              headers=headers)


        print(f"Status Code (Crear Estudiante): {r.status_code}")
        # Si todo fue bien (código 201 Created), la API devuelve el objeto creado
        nuevo_edificio = json.loads(r.content)
        flash(f"Edificio '{nuevo_edificio['nombre']}' creado exitosamente!", 'success')
        return redirect(url_for('los_edificios')) 

    # Si es una petición GET o si hubo un error en POST, muestra el formulario
    return render_template("crear_edificio.html")


@app.route("/crear/departamento", methods=['GET', 'POST'])
def crear_departamento():
    """
    """
    edificios_disponibles = []

    r_edificios = requests.get("http://localhost:8000/api/estudiantes/", headers=headers)
    edificios_disponibles = json.loads(r_edificios.content)['results']

    if request.method == 'POST':
        nombre = request.form['nombre']
        costo = request.form['costo']
        numero_cuartos = request.form['numero_cuartos']
        edificios_url = request.form['edificio']

        departamento_data = {
            'nombre': nombre,
            'costo': costo,
            'numero_cuartos': numero_cuartos,
            'edificio': edificios_url # Enviamos la URL del estudiante
        }

        r = requests.post("http://localhost:8000/api/direccion/",
                              json=departamento_data,
                              headers=headers)

        print(f"Status Code (Crear Direccion): {r.status_code}")

        edificio_nuevo = json.loads(r.content)
        flash(f"Departamento '{edificio_nuevo['nombre']}' creado exitosamente para el edificio!", 'success')
        return redirect(url_for('los_departamentos')) # Redirigir a la lista principal o a una de números

    return render_template("crear_direccion.html",
                           edificios=edificios_disponibles,
                           )

if __name__ == "__main__":
    app.run(debug=True)