from ficha import Ficha

class Tablero:
    def __init__(self):
        self.agujeros = [[Ficha(1) for _ in range(4)] for _ in range(12)]  # 12 hoyos con 4 fichas cada uno
        self.graneros = [0, 0]  # [jugador 1, jugador 2]

    def inicializar(self):
        self.agujeros = [[Ficha(1) for _ in range(4)] for _ in range(12)]
        self.graneros = [0, 0]

    def actualizar(self, posicion: int, jugador: int):
        semillas = len(self.agujeros[posicion])
        self.agujeros[posicion] = []
        pos = posicion

        while semillas > 0:
            pos = (pos + 1) % 13  # incluir granero como posición virtual

            # Si cae en el granero del jugador actual
            if (jugador == 1 and pos == 6) or (jugador == 2 and pos == 12):
                self.graneros[jugador - 1] += 1
                semillas -= 1
            elif pos != 6 and pos != 12:  # evita poner en granero del oponente
                index = pos if pos < 6 else pos - 1  # ajustar índice para 0-11
                self.agujeros[index % 12].append(Ficha(1))
                semillas -= 1


    def mostrar(self):
        agujeros_con_cantidades = [len(hoyo) for hoyo in self.agujeros]
        return agujeros_con_cantidades, self.graneros
