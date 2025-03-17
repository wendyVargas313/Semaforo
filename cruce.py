from threading import Thread, Lock
import time
import random
from semaforo import Semaforo

# Clase Cruce: Gestiona los semáforos de dos vías y controla el flujo de tráfico.
class Cruce:
    def __init__(self):
        self.semaforo_via1 = Semaforo("verde")  # Semáforo de la vía 1 (inicia en verde)
        self.semaforo_via2 = Semaforo("rojo")  # Semáforo de la vía 2 (inicia en rojo)
        self.lock = Lock()  # Lock para garantizar seguridad en entornos multihilo

    def cambiar_semaforos(self):
        with self.lock:
            # Alterna el estado de los semáforos entre verde y rojo
            if self.semaforo_via1.get_estado() == "verde":
                self.semaforo_via1.cambiar_estado("rojo")
                self.semaforo_via2.cambiar_estado("verde")
            else:
                self.semaforo_via1.cambiar_estado("verde")
                self.semaforo_via2.cambiar_estado("rojo")

    def puede_pasar(self, via):
        # Verifica si un coche o peatón puede pasar por la vía especificada
        if via == 1:
            return self.semaforo_via1.get_estado() == "verde"
        elif via == 2:
            return self.semaforo_via2.get_estado() == "verde"
        return False
