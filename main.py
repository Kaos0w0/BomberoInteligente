import time
import numpy as np
from itertools import count
from classes import Posicion, Nodo, Estado
from queue import Queue, PriorityQueue, LifoQueue

matriz_de_juego = np.ones((10, 10), dtype=int)

# Función que checa si se puede realizar una acción en una casilla, y en caso de ser así, cual será la acción
def obtener_accion(x, y, cubeta, litros_agua, matriz):
    if x <= 9 and y <= 9 and x >= 0 and y >= 0:
        match matriz[y][x]:
            case 1: return None                                         # Si es un muro no se puede realizar ninguna acción
            case 2 if litros_agua == 0: return None                     # Si no tiene agua no apaga el fuego
            case 2 if litros_agua != 0: return 'apagar_fuego'           # Si tiene agua apaga el fuego
            case 3 if cubeta == False: return 'recoger_cubeta_pequena'  # Si no tiene cubeta, la recoge (pequeña)
            case 4 if cubeta == False: return 'recoger_cubeta_grande'       # Si no tiene cubeta, la recoge (grande)
            case 6 if litros_agua == 0 and cubeta: return 'llenar_cubeta'   # Si no tiene agua y tiene cubeta, la llena
            case _: return 'caminar'                                    # Si no se cumple ninguna condición, camina
    else:
        return None  # Si se sale del mapa no se puede realizar ninguna acción
    
# Función que simula la condición "Evite devolverse al estado anterior" si el tipo es "evite_devolverse"
# o la condición "Evite ciclos" si el tipo es "evite_ciclos"
def cumple_restriccion(nodo, nodo_padre, restriccion='evite_devolverse'):
    if restriccion == 'evite_devolverse':
        if(nodo.estado.obtener_estado() == nodo_padre.estado.obtener_estado()): return False
        return True
    
    # Recorre cada nodo hasta la raíz y verifica que no se haya pasado por el mismo estado actual
    elif restriccion == 'evite_ciclos':
        while nodo_padre.nodo_padre != None:
            if(nodo.estado.obtener_estado() == nodo_padre.estado.obtener_estado()):
                return False
            nodo_padre = nodo_padre.nodo_padre
        return True
    
# Función que checa los movimientos posibles que puede realizar el bombero
def obtener_movimientos_posibles(nodo, restriccion='evite_devolverse'):
    direcciones=['derecha', 'abajo', 'izquierda', 'arriba']
    movimientos = []
    x = nodo.estado.posicion_actual.x
    y = nodo.estado.posicion_actual.y
    litros_agua = nodo.estado.estado_cubeta   
    tiene_cubeta = (nodo.estado.cubeta != 0)
    
    if nodo.nodo_padre == None: nodo_padre = nodo
    else: nodo_padre = nodo.nodo_padre    

    accion_arriba = obtener_accion(x, y - 1, tiene_cubeta, litros_agua, matriz_de_juego)
    accion_abajo = obtener_accion(x, y + 1, tiene_cubeta, litros_agua, matriz_de_juego)
    accion_izquierda = obtener_accion(x - 1, y, tiene_cubeta, litros_agua, matriz_de_juego)
    accion_derecha = obtener_accion(x + 1, y, tiene_cubeta, litros_agua, matriz_de_juego)
    acciones = [accion_derecha, accion_abajo, accion_izquierda, accion_arriba]

    for i in range(0, 4):
        nuevo_nodo = nodo.mover_bombero(direcciones[i], acciones[i])
        if acciones[i] != None and cumple_restriccion(nuevo_nodo, nodo_padre, restriccion):
            movimientos.append([direcciones[i], acciones[i]])

    return movimientos

def busqueda(algoritmo, matriz):
    # Inicialización de variables del juego
    start_time = time.time()            # Tiempo de inicio
    continuar_expansion = True          # Variable que indica si se debe continuar con la expansion de nodos
    nodos_expandidos = 0                # Variable que cuenta el numero de nodos expandidos
    numero_de_fuegos = 0                # Variable que cuenta el numero de fuegos
    posiciones_de_fuegos = []           # Lista que guarda las posiciones de los fuegos

    # Se recorre la matriz para buscar elementos de interes (bombero y fuegos)
    for i in range(0,10):
        for j in range(0,10):
            if matriz[j][i] == 5:
                # Se busca la posicion del bombero
                posicion_bombero = Posicion(i, j)
            if matriz[j][i] == 2:
                # Se cuentan los fuegos y se guardan sus posiciones
                numero_de_fuegos += 1
                posiciones_de_fuegos.append((j, i))

    # Se el estado inicial (posicion del bombero, numero de fuegos, cubeta, estado de la cubeta)
    estado_inicial = Estado(posicion_bombero, numero_de_fuegos, 0, 0)
    # Se crea el nodo inicial (estado inicial, padre, operacion, profundidad, costo, heuristica, posiciones de fuegos)
    nodo_raiz = Nodo(estado_inicial, None, None, 0, 0, 0, posiciones_de_fuegos)

    # Se crea un valor unico para cada nodo, de manera que si sus heuristicas o costos son iguales, se pueda comparar
    # Se usa la libreria itertools para crear un contador que se incrementa cada vez que se crea un nodo
    valor_unico = count()

    # Se crea la cola o pila dependiendo del algoritmo de busqueda
    # Se nombra arbol haciendo referencia al arbol de busqueda
    # Queue es cola, LifoQueue es pila y PriorityQueue es cola de prioridad
    match algoritmo:
        case 'Busqueda por amplitud':
            arbol = Queue()
            arbol.put(nodo_raiz)
        case 'Busqueda por coste uniforme':
            arbol = PriorityQueue()
            arbol.put((nodo_raiz.costo, next(valor_unico), nodo_raiz))
        case 'Busqueda por profundidad':
            arbol = LifoQueue()
            arbol.put(nodo_raiz)
        case 'Busqueda avara':
            arbol = PriorityQueue()
            arbol.put((nodo_raiz.heuristica, next(valor_unico), nodo_raiz))
        case 'Busqueda por A*':
            arbol = PriorityQueue()
            arbol.put((nodo_raiz.costo + nodo_raiz.heuristica, next(valor_unico), nodo_raiz))

    # Se crea la lista donde se guardará la solución
    solucion = []

    # Ejecución del ciclo que expande los nodos
    while(continuar_expansion):
        if arbol.empty():
            # Si la cola o pila esta vacia, se termina el ciclo
            continuar_expansion = False
            return "Sin solución", 0, 0, 0, 0
        else:
            match algoritmo:
                case 'Busqueda por amplitud' | 'Busqueda por profundidad':
                    # Se obtiene el primer nodo de la cola | pila
                    nodo_actual = arbol.get()
                case 'Busqueda por coste uniforme' | 'Busqueda avara' | 'Busqueda por A*':
                    # Se obtiene el primer nodo de la cola de prioridad
                    nodo_actual = arbol.get()[2]

            nodos_expandidos += 1 # Se aumenta el numero de nodos expandidos

            if nodo_actual.estado.numero_de_fuegos == 0:
                # Si el nodo actual es el estado final (fuegos apagados), se termina el ciclo
                continuar_expansion = False
                costo = nodo_actual.costo
                profundidad = nodo_actual.profundidad
                # Se obtiene la solución
                while nodo_actual.nodo_padre != None:
                    solucion.append(nodo_actual.operacion_origen)
                    nodo_actual = nodo_actual.nodo_padre
                solucion.reverse()
                # Se obtiene el tiempo de ejecución
                tiempo_ejecucion = time.time() - start_time

                return solucion, tiempo_ejecucion, nodos_expandidos, costo, profundidad
            else:
                # Si el nodo actual no es el estado final, se obtienen los movimientos posibles
                if algoritmo == 'Busqueda por profundidad' or algoritmo == 'Busqueda avara':
                    # Se obtienen los movimientos posibles de manera que se evite devolverse a estados anteriores
                    movimientos_posibles = obtener_movimientos_posibles(nodo_actual, 'evite_ciclos')
                else:
                    movimientos_posibles = obtener_movimientos_posibles(nodo_actual)
                # Se agregan los nodos hijos a la cola o pila dependiendo del algoritmo
                for movimiento in movimientos_posibles:
                    nuevo_nodo = nodo_actual.mover_bombero(movimiento[0], movimiento[1])

                    match algoritmo:
                        case 'Busqueda por amplitud':
                            arbol.put(nuevo_nodo)
                        case 'Busqueda por coste uniforme':
                            arbol.put((nuevo_nodo.costo, next(valor_unico), nuevo_nodo))
                        case 'Busqueda por profundidad':
                            arbol.put(nuevo_nodo)
                        case 'Busqueda avara':
                            arbol.put((nuevo_nodo.heuristica, next(valor_unico), nuevo_nodo))
                        case 'Busqueda por A*':
                            arbol.put((nuevo_nodo.costo + nuevo_nodo.heuristica, next(valor_unico), nuevo_nodo))

def obtener_solucion(algoritmo='Busqueda por amplitud', matriz = matriz_de_juego):
    global matriz_de_juego 
    matriz_de_juego = matriz

    return busqueda(algoritmo, matriz_de_juego)