from threading import Thread, Lock
import time
import random

# Clase Semaforo: Representa un semáforo con dos estados (verde y rojo).
class Semaforo:
    def __init__(self, estado_inicial="rojo"):
        self.estado = estado_inicial  # Estado inicial del semáforo
        self.lock = Lock()  # Lock para garantizar seguridad en entornos multihilo

    def cambiar_estado(self, nuevo_estado):
        with self.lock:
            self.estado = nuevo_estado  # Cambia el estado del semáforo
            print(f"Semáforo cambió a {nuevo_estado}")

    def get_estado(self):
        with self.lock:
            return self.estado  # Devuelve el estado actual del semáforo
