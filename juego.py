# -- juego.py --

import time
from jugadorHumano import JugadorHumano
from jugadorSintetico import JugadorSintetico

class Juego:
    def __init__(self, tablero, interfaz):
        self.tablero = tablero
        self.interfaz = interfaz
        self.estado = True        # Indica si el juego sigue en curso
        self.turno = 1            # 1 = Jugador 1, 2 = Jugador 2
        self.jugador1 = None      # Se asignará según el modo elegido
        self.jugador2 = None      # Se asignará según el modo elegido
        self.pause = False        # True si es Sintético vs Sintético

    def _seleccionarModo(self):
        """
        Al inicio, pregunta al usuario el modo de juego:
          1) Humano vs Humano
          2) Humano vs Sintético
          3) Sintético vs Sintético
        Configura self.jugador1 y self.jugador2 en consecuencia.
        """
        print("Elige modo de juego:")
        print("  1) Humano vs Humano")
        print("  2) Humano vs Sintético")
        print("  3) Sintético vs Sintético")

        while True:
            try:
                opcion = int(input("Opción (1-3): "))
                if opcion not in (1, 2, 3):
                    print("⛔ Debe ingresar 1, 2 o 3.")
                    continue

                if opcion == 1:
                    # Ambos jugadores humanos
                    self.jugador1 = JugadorHumano(1)
                    self.jugador2 = JugadorHumano(2)
                elif opcion == 2:
                    # Jugador 1 humano, Jugador 2 sintético
                    self.jugador1 = JugadorHumano(1)
                    self.jugador2 = JugadorSintetico(2)
                else:
                    # Ambos jugadores sintéticos
                    self.jugador1 = JugadorSintetico(1)
                    self.jugador2 = JugadorSintetico(2)
                    self.pause = True

                break

            except ValueError:
                print("⚠️ Entrada inválida. Debe ingresar un número entre 1 y 3.")

        print("")  # Línea en blanco tras elegir modo

    def iniciarJuego(self):
        # 1) Preguntar modo de juego y asignar jugadores
        self._seleccionarModo()

        # 2) Inicializar tablero y estado
        self.tablero.inicializar()
        self.estado = True
        self.turno = 1
        self.interfaz.mostrarBienvenida()

        while self.estado:
            # 3) Si es Sintético vs Sintético, pausas para que se vea el proceso
            if self.pause:
                time.sleep(1)

            # 4) Mostrar tablero actual
            agujeros, graneros = self.tablero.mostrar()
            self.interfaz.tableroJuego(agujeros, graneros, self.turno)

            # 5) Pedir al jugador activo que elija su hoyo
            if self.turno == 1:
                indice_real = self.jugador1.jugarTurno(self.tablero)
            else:
                indice_real = self.jugador2.jugarTurno(self.tablero)

            # 6) Si es Sintético vs Sintético, mostrar qué hoyo eligió y pausar
            if self.pause:
                # Convertir índice real (0–11) a número de hoyo (1–6) para mostrar
                if self.turno == 1:
                    hoyo_mostrar = indice_real + 1         # 0..5 → 1..6
                else:
                    hoyo_mostrar = 12 - indice_real        # 6..11 → 6..1
                print(f"\n🤖 Jugador {self.turno} sintético elige hoyo {hoyo_mostrar}")
                time.sleep(1)

            # 7) Repartir semillas y obtener posición lógica final (0–13)
            pos_final = self.tablero.actualizar(indice_real, self.turno)

            # 8) Comprobar si cayó en granero propio → turno adicional
            if (self.turno == 1 and pos_final == 6) or (self.turno == 2 and pos_final == 13):
                print(f"\n🎉 ¡El Jugador {self.turno} recibe turno adicional!")
                # No cambiamos self.turno, el mismo jugador juega otra vez

            else:
                # 9) Si no fue granero, intentar captura
                if self._esHoyoPropioYEraVacio(pos_final):
                    opp_pos = 12 - pos_final
                    idx_yo = self._posLogicaAIndice(pos_final)
                    idx_opp = self._posLogicaAIndice(opp_pos)

                    cantidad_opuesto = len(self.tablero.agujeros[idx_opp])
                    if cantidad_opuesto > 0:
                        total_captura = 1 + cantidad_opuesto
                        if self.turno == 1:
                            self.tablero.graneros[0] += total_captura
                        else:
                            self.tablero.graneros[1] += total_captura

                        # Vaciamos ambos hoyos
                        self.tablero.agujeros[idx_yo] = []
                        self.tablero.agujeros[idx_opp] = []
                        print(f"\n🪄 Captura! Jugador {self.turno} se lleva {total_captura} semillas "
                              f"(hoyos {pos_final} y {opp_pos}).")

                # 10) Cambiar turno si no hubo granero
                self.turno = 2 if self.turno == 1 else 1

            # 11) Verificar condición de fin de juego
            agujeros_act, _ = self.tablero.mostrar()
            # Si se vacían los hoyos 0–5 → Jugador 2 recoge lo que quede en 6–11 y termina
            if all(c == 0 for c in agujeros_act[0:6]):
                self._recogerRestantesYTerminar(lado_oponente=2, rango_oponente=range(6, 12))
                break

            # Si se vacían los hoyos 6–11 → Jugador 1 recoge lo que quede en 0–5 y termina
            if all(c == 0 for c in agujeros_act[6:12]):
                self._recogerRestantesYTerminar(lado_oponente=1, rango_oponente=range(0, 6))
                break

        # Fin de bucle principal

    def _recogerRestantesYTerminar(self, lado_oponente: int, rango_oponente):
        """
        Cuando un lado (0 o 1) se queda con todos sus 6 hoyos vacíos,
        el oponente recoge las semillas restantes en su granero y termina el juego.
        """
        agujeros_act, _ = self.tablero.mostrar()

        # Sumar todas las semillas que queden en el rango_oponente
        resto = sum(agujeros_act[i] for i in rango_oponente)
        if lado_oponente == 1:
            self.tablero.graneros[0] += resto
        else:
            self.tablero.graneros[1] += resto

        # Vaciar dichos hoyos
        for i in rango_oponente:
            self.tablero.agujeros[i] = []

        self.terminarJuego()

    def _posLogicaAIndice(self, pos: int) -> int:
        """
        Convierte una posición lógica (0..13) a índice real de self.tablero.agujeros (0..11).
        - Si pos ∈ [0..5], idx = pos.
        - Si pos ∈ [7..12], idx = pos - 1.
        (6 y 13 son graneros, no mapean a agujero).
        """
        if 0 <= pos <= 5:
            return pos
        elif 7 <= pos <= 12:
            return pos - 1
        else:
            raise ValueError(f"Posición lógica inválida para un hoyo: {pos}")

    def _esHoyoPropioYEraVacio(self, pos: int) -> bool:
        """
        Retorna True si 'pos' (lógica 0..13) corresponde a un hoyo propio (no granero)
        y justo después de repartir contiene exactamente 1 semilla (estaba vacío antes).
        """
        if self.turno == 1 and 0 <= pos <= 5:
            idx = pos
        elif self.turno == 2 and 7 <= pos <= 12:
            idx = pos - 1
        else:
            return False

        return len(self.tablero.agujeros[idx]) == 1

    def terminarJuego(self):
        self.estado = False
        print("\n🛑 Fin del juego.")
        _, graneros = self.tablero.mostrar()
        print(f"Granero Jugador 1: {graneros[0]}")
        print(f"Granero Jugador 2: {graneros[1]}")
        if graneros[0] > graneros[1]:
            print("🏆 ¡Gana el Jugador 1!")
        elif graneros[1] > graneros[0]:
            print("🏆 ¡Gana el Jugador 2!")
        else:
            print("🤝 ¡Empate!")