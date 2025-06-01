class JugadorHumano:
    def __init__(self, lado: int):
        self.lado = lado  

    def jugarTurno(self, tablero) -> int:
        while True:
            try:
                seleccion = int(input(f"Jugador {self.lado}, elige un hoyo (1-6): ")) - 1
                print("\n")
                print("\n")

                if not 0 <= seleccion < 6:
                    print("Entrada fuera de rango. Debe ser un número entre 1 y 6.")
                    continue

                if self.lado == 1:
                    indice_real = seleccion
                else:
                    indice_real = 11 - seleccion  

                if len(tablero.agujeros[indice_real]) == 0:
                    print("Ese hoyo está vacío. Elige otro.")
                    continue

                return indice_real  

            except ValueError:
                print("Entrada inválida. Ingresa un número.")
