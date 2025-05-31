from jugadorHumano import JugadorHumano

class Juego:
    def __init__(self, tablero, interfaz):
        self.tablero = tablero        # Consulta estado del juego
        self.interfaz = interfaz      # Muestra el tablero
        self.estado = True            # Indica si el juego sigue activo
        self.turno = 1                # 1 = Jugador 1, 2 = Jugador 2
        self.jugador1 = JugadorHumano(1)
        self.jugador2 = JugadorHumano(2)

    def iniciarJuego(self):
        self.tablero.inicializar()
        self.estado = True
        self.turno = 1
        self.interfaz.mostrarBienvenida()
        self.gestionarTurnos()

    def gestionarTurnos(self):
        while self.estado:
            agujeros_actualizados, graneros_actualizados = self.tablero.mostrar()
            self.interfaz.tableroJuego(agujeros_actualizados, graneros_actualizados, self.turno)


            # Delegar la jugada al jugador correspondiente
            if self.turno == 1:
                posicion = self.jugador1.jugarTurno(self.tablero)
            else:
                posicion = self.jugador2.jugarTurno(self.tablero)

            self.actualizarTablero(posicion, self.turno)

            if self.verificarFinDeJuego():
                self.terminarJuego()
            else:
                self.turno = 2 if self.turno == 1 else 1


    def actualizarTablero(self, posicion: int, jugador: int):
        self.tablero.actualizar(posicion, jugador)

    def verificarFinDeJuego(self):
        lado1_vacio = all(len(hoyo) == 0 for hoyo in self.tablero.agujeros[:6])
        lado2_vacio = all(len(hoyo) == 0 for hoyo in self.tablero.agujeros[6:])
        return lado1_vacio or lado2_vacio

    def terminarJuego(self):
        self.estado = False
        print("\n🛑 Fin del juego.")
        agujeros, graneros = self.tablero.mostrar()
        print(f"Granero Jugador 1: {graneros[0]}")
        print(f"Granero Jugador 2: {graneros[1]}")

        if graneros[0] > graneros[1]:
            print("🏆 ¡Gana el Jugador 1!")
        elif graneros[1] > graneros[0]:
            print("🏆 ¡Gana el Jugador 2!")
        else:
            print("🤝 ¡Empate!")
