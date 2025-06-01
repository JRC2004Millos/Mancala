# -- juego.py --

import time
from jugadorHumano import JugadorHumano
from jugadorSintetico import JugadorSintetico

class Juego:
    def __init__(self, tablero, interfaz):
        self.tablero = tablero
        self.interfaz = interfaz
        self.estado = True        
        self.turno = 1            
        self.jugador1 = None      
        self.jugador2 = None     
        self.pause = False        

    def _seleccionarModo(self):
        
        print("Elige modo de juego:")
        print("  1) Humano vs Humano")
        print("  2) Humano vs Sintético")
        print("  3) Sintético vs Sintético")

        while True:
            try:
                opcion = int(input("Opción (1-3): "))
                if opcion not in (1, 2, 3):
                    print("Debe ingresar 1, 2 o 3.")
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
                print("Entrada inválida. Debe ingresar un número entre 1 y 3.")

        print("") 

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
                
                if self.turno == 1:
                    hoyo_mostrar = indice_real + 1         
                else:
                    hoyo_mostrar = 12 - indice_real      
                print(f"\n🤖 Jugador {self.turno} sintético elige hoyo {hoyo_mostrar}")
                time.sleep(1)

            # 7) Repartir semillas y obtener posición lógica final (0–13)
            pos_final = self.tablero.actualizar(indice_real, self.turno)

            # 8) Comprobar si cayó en granero propio → turno adicional
            if (self.turno == 1 and pos_final == 6) or (self.turno == 2 and pos_final == 13):
                print(f"\n🎉 ¡El Jugador {self.turno} recibe turno adicional!")
              

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

                        self.tablero.agujeros[idx_yo] = []
                        self.tablero.agujeros[idx_opp] = []
                        print(f"\n🪄 Captura! Jugador {self.turno} se lleva {total_captura} semillas "
                              f"(hoyos {pos_final} y {opp_pos}).")

                # 10) Cambiar turno si no hubo granero
                self.turno = 2 if self.turno == 1 else 1

            # 11) Verificar condición de fin de juego
            agujeros_act, _ = self.tablero.mostrar()
          
            if all(c == 0 for c in agujeros_act[0:6]):
                self._recogerRestantesYTerminar(lado_oponente=2, rango_oponente=range(6, 12))
                break

            if all(c == 0 for c in agujeros_act[6:12]):
                self._recogerRestantesYTerminar(lado_oponente=1, rango_oponente=range(0, 6))
                break


    def _recogerRestantesYTerminar(self, lado_oponente: int, rango_oponente):
       
        agujeros_act, _ = self.tablero.mostrar()

        resto = sum(agujeros_act[i] for i in rango_oponente)
        if lado_oponente == 1:
            self.tablero.graneros[0] += resto
        else:
            self.tablero.graneros[1] += resto

        for i in rango_oponente:
            self.tablero.agujeros[i] = []

        self.terminarJuego()

    def _posLogicaAIndice(self, pos: int) -> int:
    
        if 0 <= pos <= 5:
            return pos
        elif 7 <= pos <= 12:
            return pos - 1
        else:
            raise ValueError(f"Posición lógica inválida para un hoyo: {pos}")

    def _esHoyoPropioYEraVacio(self, pos: int) -> bool:
        
        if self.turno == 1 and 0 <= pos <= 5:
            idx = pos
        elif self.turno == 2 and 7 <= pos <= 12:
            idx = pos - 1
        else:
            return False

        return len(self.tablero.agujeros[idx]) == 1

    def terminarJuego(self):
        self.estado = False
        print("\nFin del juego.")
        _, graneros = self.tablero.mostrar()
        print(f"Granero Jugador 1: {graneros[0]}")
        print(f"Granero Jugador 2: {graneros[1]}")
        if graneros[0] > graneros[1]:
            print("🏆 ¡Gana el Jugador 1!")
        elif graneros[1] > graneros[0]:
            print("🏆 ¡Gana el Jugador 2!")
        else:
            print("🤝 ¡Empate!")