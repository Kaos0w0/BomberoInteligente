class Nodo: 
    def __init__(self, estado, nodo_padre, operacion_origen, profundidad, costo, heuristica, posiciones_de_fuegos):
        self.estado = estado
        self.nodo_padre = nodo_padre
        self.operacion_origen = operacion_origen
        self.profundidad = profundidad
        self.costo = costo
        self.heuristica = heuristica
        self.posiciones_de_fuegos = posiciones_de_fuegos

    def mover_bombero(self, direccion, accion):
        if accion != None and accion != 'caminar':
            operacion_origen = direccion + ' y ' + accion
        else:
            operacion_origen = direccion

        match direccion:
            case 'arriba': nueva_posicion = self.estado.posicion_actual.mover_bombero_arriba()
            case 'abajo': nueva_posicion = self.estado.posicion_actual.mover_bombero_abajo()
            case 'izquierda': nueva_posicion = self.estado.posicion_actual.mover_bombero_izquierda()
            case 'derecha': nueva_posicion = self.estado.posicion_actual.mover_bombero_derecha()

        distancia_de_manhattan = 0
        if len(self.posiciones_de_fuegos) == 1:
            distancia_de_manhattan += abs(self.posiciones_de_fuegos[0][0] - nueva_posicion.y) + abs(self.posiciones_de_fuegos[0][1] - nueva_posicion.x)
        elif len(self.posiciones_de_fuegos) == 2:
            fuego_1 = abs(self.posiciones_de_fuegos[0][0] - nueva_posicion.y) + abs(self.posiciones_de_fuegos[0][1] - nueva_posicion.x)
            fuego_2 = abs(self.posiciones_de_fuegos[1][0] - nueva_posicion.y) + abs(self.posiciones_de_fuegos[1][1] - nueva_posicion.x)
            distancia_de_manhattan += min(fuego_1, fuego_2)
            if fuego_1 < fuego_2:
                distancia_de_manhattan += abs(self.posiciones_de_fuegos[1][0] - self.posiciones_de_fuegos[0][0]) + abs(self.posiciones_de_fuegos[1][1] - self.posiciones_de_fuegos[0][1])
            else:
                distancia_de_manhattan += abs(self.posiciones_de_fuegos[0][0] - self.posiciones_de_fuegos[1][0]) + abs(self.posiciones_de_fuegos[0][1] - self.posiciones_de_fuegos[1][1])

        nueva_heuristica = (distancia_de_manhattan)

        nuevo_costo = self.costo + 1 + self.estado.estado_cubeta
        nuevo_estado = Estado(nueva_posicion, self.estado.numero_de_fuegos, self.estado.cubeta, self.estado.estado_cubeta)
        nuevo_nodo = Nodo(nuevo_estado, self, operacion_origen, self.profundidad + 1, nuevo_costo, nueva_heuristica, self.posiciones_de_fuegos.copy())
        nuevo_nodo.aplicar_accion(accion)

        return nuevo_nodo

    def aplicar_accion(nodo, accion):
        match accion:
            case 'llenar_cubeta': nodo.estado.llenar_cubeta()
            case 'apagar_fuego':
                if((nodo.estado.posicion_actual.y, nodo.estado.posicion_actual.x) in nodo.posiciones_de_fuegos):
                    nodo.estado.apagar_fuego()
                    nodo.posiciones_de_fuegos.remove((nodo.estado.posicion_actual.y, nodo.estado.posicion_actual.x))
            case 'recoger_cubeta_pequena': nodo.estado.cubeta = 1
            case 'recoger_cubeta_grande': nodo.estado.cubeta = 2

class Estado:
    def __init__(self, posicion_actual, numero_de_fuegos, cubeta, estado_cubeta):
        self.posicion_actual = posicion_actual
        self.numero_de_fuegos = numero_de_fuegos
        self.cubeta = cubeta
        self.estado_cubeta = estado_cubeta
    def obtener_estado(self):
        return ((self.posicion_actual.x, self.posicion_actual.y), self.numero_de_fuegos, self.cubeta, self.estado_cubeta)
    def apagar_fuego(self):
        self.numero_de_fuegos -= 1
        self.estado_cubeta -= 1
    def llenar_cubeta(self):
        self.estado_cubeta = self.cubeta

class Posicion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def mover_bombero_arriba(self):
        return Posicion(self.x, self.y - 1)
    def mover_bombero_abajo(self):
        return Posicion(self.x, self.y + 1)
    def mover_bombero_izquierda(self):
        return Posicion(self.x - 1, self.y)
    def mover_bombero_derecha(self):
        return Posicion(self.x + 1, self.y)