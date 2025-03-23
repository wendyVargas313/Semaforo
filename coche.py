from threading import Thread, Lock
import time
import random

# Clase Coche: Representa un coche que intenta cruzar el cruce.
class Coche(Thread):
    def __init__(self, id, via, cruce):
        Thread.__init__(self)
        self.id = id  # Identificador único del coche
        self.via = via  # Vía por la que el coche intenta cruzar (1 o 2)
        self.cruce = cruce  # Objeto Cruce que gestiona los semáforos

    def run(self):
        print(f"Coche {self.id} en la vía {self.via} esperando para cruzar")
        while not self.cruce.puede_pasar(self.via, self.id):  # Espera si hay otro coche en el cruce
            time.sleep(1)  # para hacer más rápido el cruce
        print(f"Coche {self.id} en la vía {self.via} está cruzando")
        time.sleep(random.randint(1, 3))  # Simula el tiempo de cruce
        print(f"Coche {self.id} en la vía {self.via} ha cruzado")
        
        self.cruce.liberar_cruce()  # Libera el cruce después de cruzar
