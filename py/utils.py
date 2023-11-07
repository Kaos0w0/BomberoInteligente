import js
import asyncio
import numpy as np
from main import obtener_solucion
from js import document, FileReader
from pyodide import create_proxy

matriz_juego = []

def formatear_matriz(matriz):
    global matriz_juego
    # Se oculta el seleccionador y se dibuja el mapa
    container = document.getElementById('container')
    container.style.display = 'none'
    juego_container = document.getElementById('juego-container')
    juego_container.style.display = 'flex'
    algoritmos_container = document.getElementById('algoritmos-container')
    algoritmos_container.style.display = 'block'
    body = document.getElementById('body')
    body.style.flexWrap = "wrap";
    js.dibujarMatriz(matriz)

    mapa = []
    matriz = matriz.split('/')
    for vector in matriz:
        mapa.append(vector.split(','))
    matriz = np.array(mapa, dtype=str)
    matriz = matriz.astype(int)

    matriz_juego = matriz

# Funcion que se ejecuta cuando el archivo carga
def lectura_completa(e):
    matriz = js.matrix_creator(e.target.result)
    matriz = formatear_matriz(matriz)
    
# Funcion que se ejecuta cuando se dropea un archivo
def leer_archivo(e):      
    matriz = e.target.value
    matriz = formatear_matriz(matriz)

# Funcion que lee el archivo
async def procesar_archivo(e):
    archivos = document.getElementById('fileInput').files
    for archivo in archivos:
        reader = FileReader.new()
    
        # Se crea un proxy que se ejecuta cuando el archivo carga
        onload_event = create_proxy(lectura_completa)
        
        reader.onload = onload_event
        reader.readAsText(archivo)
    
        return e

# Funcion que se ejecuta cuando se hace click en el boton de iniciar busqueda
def iniciar_busqueda(e):
    algoritmo = document.getElementById('algoritmo').value
    solucion = obtener_solucion(algoritmo, matriz_juego)
    if solucion[0] == "Sin solución":
        js.mostrarResultado(0,0,0,0,0)
    else:
        js.dibujar_solucion(solucion)

# Proxy que llama a la funcion que lee el archivo
file_event = create_proxy(procesar_archivo) # Si el archivo fue escogido por input file 
file_dropped = create_proxy(leer_archivo) # Si el archivo fue arrastrado y soltado
iniciarBusqueda = create_proxy(iniciar_busqueda) # Si se hace click en el boton de iniciar busqueda

# Se añade un listener al input file
e = document.getElementById("fileInput")
e.addEventListener("change", file_event, False)   

# Se añade un listener al input display area
e = document.getElementById("fileDisplayArea")
e.addEventListener("input", file_dropped)

# Se añade un listener al boton de iniciar busqueda
e = document.getElementById("iniciar-busqueda")
e.addEventListener("click", iniciarBusqueda)