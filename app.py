from flask import Flask, render_template, jsonify
import threading
import time
from cruce import Cruce
from coche import Coche

app = Flask(__name__)

# Crear una instancia del cruce
cruce = Cruce()

# Lista global de coches en el cruce
coches_en_cruce = []

# variable global
simulacion_en_ejecucion = False

def cambiar_semaforos(): #Función que cambia los semáforos periódicamente
    global simulacion_en_ejecucion 
    while simulacion_en_ejecucion:
        time.sleep(5)
        cruce.cambiar_semaforos()  # Ahora usamos la clase Cruce

# Ruta para obtener el estado de los coches en el cruce
@app.route("/coches")
def obtener_coches():
    return jsonify(coches_en_cruce), 200

# Rutas de Flask
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start") #Inicia la simulación si aún no ha comenzado
def start_simulation():
    global simulacion_en_ejecucion
    if not simulacion_en_ejecucion:
        simulacion_en_ejecucion = True
        thread = threading.Thread(target=cambiar_semaforos, daemon=True)
        thread.start()
        
        #Crear coches que intentan cruzar
        for i in range(2):  # Crear 5 coches
            via = (i % 2) + 1  # Alternar entre las dos vías
            coche = Coche(i, via, cruce)
            coches_en_cruce.append({"id": i, "via": via, "estado": "esperando"})
            coche.start()

        print("Simulación iniciada.")
    return jsonify({"status": "Simulación ya está en ejecución"})

@app.route("/estado") #Devuelve el estado actual de los semáforos
def estado():
    
    return jsonify({
        "semaforo1": cruce.semaforo_via1.get_estado(),
        "semaforo2": cruce.semaforo_via2.get_estado()
    }), 200

if __name__ == "__main__":
    cruce = Cruce()
    app.run(debug=True)