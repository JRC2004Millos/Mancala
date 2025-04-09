class InterfazTerminal:
    def __init__(self):
        # Estado inicial fijo (puedes conectarlo a lógica después)
        self.agujeros = [4] * 12
        self.graneros = [0, 0]
        self.turno = 1

    def tableroJuego(self):
        print("\n")
        print("========================================================")
        print("        BIENVENIDO AL JUEGO DE MANCALA         ")
        print("========================================================")
        print("\n")
        print(f"Granero J2:|--------- {self.graneros[1]} ---------|")

        # Los hoyos del jugador dos van de derecha a izquierda
        print("Jugador 2: ", end="")
        for i in range(11, 5, -1):
            print(f"[{self.agujeros[i]}]", end=" ")
        print()

        print("Jugador 1: ", end="")
        for i in range(0, 6):
            print(f"[{self.agujeros[i]}]", end=" ")
        print()

        print(f"Granero J1:|--------- {self.graneros[0]} ---------|")
        print(f"\nTurno del jugador {self.turno}")


if __name__ == "__main__":
    interfaz = InterfazTerminal()
    interfaz.tableroJuego()
