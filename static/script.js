
document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM completamente cargado y procesado");

document.getElementById("startSimulation").addEventListener("click", () => {
    fetch("/start")
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Simulación iniciada:", data);
            })
            .catch(error => console.error("Error al iniciar la simulación:", error));
    });

// Función para actualizar los semáforos visualmente
function actualizarSemaforos(semaforo1, semaforo2) {
    document.getElementById("semaforo1").className = `luz ${semaforo1}`;
    document.getElementById("semaforo2").className = `luz ${semaforo2}`;
    document.getElementById("semaforo3").className = `luz ${semaforo2}`; // Sincroniza con la vía opuesta
    document.getElementById("semaforo4").className = `luz ${semaforo1}`; // Invertir el estado

    moverCarros(semaforo1, semaforo2); // Llamamos a la función de movimiento
}

 // Función para actualizar la posición de los coches desde el backend
function actualizarCoches() {
    fetch("/coches")
        .then(response => response.json())
        .then(coches => {
            let cocheEnCruce = null;  // Para rastrear si hay un coche cruzando
            
            coches.forEach(coche => {
                let cocheElemento = document.getElementById(`coche-${coche.id}`);
                
                // Si el coche no existe en el DOM, crearlo
                if (!cocheElemento) {
                    let nuevoCoche = document.createElement("div");
                    nuevoCoche.classList.add(coche.via === 1 ? "carroV" : "carroH");
                    nuevoCoche.id = `coche-${coche.id}`;

                    // Posiciones iniciales dependiendo de la vía
                    if (coche.via === 1) {
                        nuevoCoche.style.left = "210px"; // Alineado con el carril vertical
                        nuevoCoche.style.top = "30px"; // Inicio arriba
                    } else {
                        nuevoCoche.style.top = "220px"; // Alineado con el carril horizontal
                    }

                    document.querySelector(".cruce").appendChild(nuevoCoche);
                }
                
                 // Verifica si el coche está cruzando y que no haya otro coche en el cruce
                    if (coche.estado === "cruzando") {
                        if (!cocheEnCruce || cocheEnCruce === coche.id) {
                            cocheEnCruce = coche.id;  // Bloquea el cruce para otros coches

                        if (coche.via === 1) {
                            cocheElemento.style.transition = "transform 3s linear"; //Tiempo de animación
                            cocheElemento.style.transform = "translateY(150px)"; // Se mueve hacia abajo
                        } else {
                            cocheElemento.style.transition = "transform 3s linear";
                            cocheElemento.style.transform = "translateX(150px)"; // Se mueve hacia la derecha
                        }
                    }
                }
            });
        })
        .catch(error => console.error("Error al obtener los coches:", error));
}

// Función para mover los carros
function moverCarros(semaforo1, semaforo2) {
    let carrosVerticales = document.querySelectorAll(".carroV");
    let carrosHorizontales = document.querySelectorAll(".carroH");

    // Si el semáforo de la vía vertical está en verde, mueve los carros verticales
    if (semaforo1 === "verde") {
        carrosVerticales.forEach(carro => {
            carro.style.transition = "transform 3s linear";
            carro.style.transform = "translateY(300px)"; // Se mueve hacia abajo
        });
    } else {
        carrosVerticales.forEach(carro => {
            carro.style.transition = "none";
            carro.style.transform = "translateY(0)"; // Se queda en su posición
        });
    }

    // Si el semáforo de la vía horizontal está en verde, mueve los carros horizontales
    if (semaforo2 === "verde") {
        carrosHorizontales.forEach(carro => {
            carro.style.transition = "transform 3s linear";
            carro.style.transform = "translateX(300px)"; // Se mueve hacia la derecha
        });
    } else {
        carrosHorizontales.forEach(carro => {
            carro.style.transition = "none";
            carro.style.transform = "translateX(0)"; // Se queda en su posición
        });
    }
}

 // Consultar el estado de los semáforos cada segundo
 setInterval(() => {
    fetch("/estado")
        .then(response => response.json())
        .then(data => {
            console.log("Estado de los semáforos recibido:", data);
            actualizarSemaforos(data.semaforo1, data.semaforo2);
        })
        .catch(error => console.error("Error al obtener el estado del semáforo:", error));
}, 1000);

// Consultar el estado de los coches cada segundo
setInterval(actualizarCoches, 1000);
});