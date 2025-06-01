class Interfaz:
    def __init__(self):
        pass  

    def mostrarBienvenida(self):
        print("\n" + "=" * 56)
        print("        BIENVENIDO AL JUEGO DE MANCALA         ")
        print("=" * 56 + "\n")

    def tableroJuego(self, agujeros, graneros, turno):
        print(f"Granero J2:|--------- {graneros[1]} ---------|")

        print("Jugador 2: ", end="")
        for i in range(11, 5, -1):
            print(f"[{agujeros[i]}]", end=" ")
        print()

        print("Jugador 1: ", end="")
        for i in range(0, 6):
            print(f"[{agujeros[i]}]", end=" ")
        print()

        print(f"Granero J1:|--------- {graneros[0]} ---------|")
        print(f"\nTurno del jugador {turno}")
