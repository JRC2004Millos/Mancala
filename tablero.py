import copy
from ficha import Ficha

class Tablero:
    def __init__(self):
        # 12 hoyos: índices 0–11; graneros: [jugador1, jugador2]
        self.agujeros = [[Ficha(1) for _ in range(4)] for _ in range(12)]
        self.graneros = [0, 0]

    def inicializar(self):
        self.agujeros = [[Ficha(1) for _ in range(4)] for _ in range(12)]
        self.graneros = [0, 0]

    def actualizar(self, posicion: int, jugador: int) -> int:
        semillas = len(self.agujeros[posicion])
        self.agujeros[posicion] = []

        if posicion < 6:
            pos = posicion
        else:
            pos = posicion + 1

        while semillas > 0:
            pos = (pos + 1) % 14

            if jugador == 1 and pos == 6:
                self.graneros[0] += 1
                semillas -= 1
            elif jugador == 2 and pos == 13:
                self.graneros[1] += 1
                semillas -= 1
            elif pos == 6 or pos == 13:
                continue
            else:
                if pos < 6:
                    idx = pos
                elif 7 <= pos <= 12:
                    idx = pos - 1
                else:
                    continue

                self.agujeros[idx].append(Ficha(1))
                semillas -= 1

        return pos

    def mostrar(self):
        agujeros_con_cantidades = [len(hoyo) for hoyo in self.agujeros]
        return agujeros_con_cantidades, self.graneros

    def __deepcopy__(self, memo):
        """
        Permite que copy.deepcopy(tablero) funcione correctamente en Minimax.
        Clona cada Ficha usando su 'cantidad'.
        """
        nueva = Tablero()
        nueva.agujeros = []
        for hoyo in self.agujeros:
            # Cada 'hoyo' es una lista de objetos Ficha; copiamos usando getCantidad()
            nueva_hoyo = [Ficha(fich.getCantidad()) for fich in hoyo]
            nueva.agujeros.append(nueva_hoyo)

        nueva.graneros = self.graneros.copy()
        return nueva
