import copy
from typing import List

from tablero import Tablero

class JugadorSintetico:
   
    def __init__(self, lado: int, max_depth: int = 5):
        
        self.lado = lado
        self.max_depth = max_depth

    def jugarTurno(self, tablero) -> int:
       
        mejor_score = None
        mejor_hoyo = None

        
        if self.lado == 1:
            rangos = list(range(0, 6))
        else:
            rangos = list(range(6, 12))

        hoyos_validos = [i for i in rangos if len(tablero.agujeros[i]) > 0]
        if not hoyos_validos:
            return rangos[0]

        
        for hoyo in hoyos_validos:
            copia_tablero = copy.deepcopy(tablero)
            copia_graneros = copy.deepcopy(tablero.graneros)

            pos_final = copia_tablero.actualizar(hoyo, self.lado)
            self._intentar_captura_en_copia(copia_tablero, pos_final, self.lado)

            # Decidir siguiente jugador (turno extra = si cayó en mi granero)
            siguiente_jugador = self.lado
            if not ((self.lado == 1 and pos_final == 6) or (self.lado == 2 and pos_final == 13)):
                siguiente_jugador = 2 if self.lado == 1 else 1

            score = self._minimax(
                copia_tablero,
                copia_graneros,
                siguiente_jugador,
                depth=1
            )

            if mejor_score is None:
                mejor_score = score
                mejor_hoyo = hoyo
            else:
                if self.lado == 1:
                    if score > mejor_score:
                        mejor_score = score
                        mejor_hoyo = hoyo
                else:
                    if score < mejor_score:
                        mejor_score = score
                        mejor_hoyo = hoyo

        return mejor_hoyo

    def _minimax(
        self,
        tablero_sim: "Tablero",
        graneros_sim: List[int],
        jugador_actual: int,
        depth: int
    ) -> int:
       
        hoyos, graneros = tablero_sim.mostrar()
        if all(c == 0 for c in hoyos[0:6]) or all(c == 0 for c in hoyos[6:12]):
            
            if all(c == 0 for c in hoyos[0:6]):
                resto = sum(hoyos[6:12])
                graneros_sim[1] += resto
            else:
                resto = sum(hoyos[0:6])
                graneros_sim[0] += resto
            diff = graneros_sim[0] - graneros_sim[1]
            return diff if self.lado == 1 else -diff

        
        if depth > self.max_depth:
            diff = graneros_sim[0] - graneros_sim[1]
            return diff if self.lado == 1 else -diff

        
        if jugador_actual == 1:
            rangos = list(range(0, 6))
        else:
            rangos = list(range(6, 12))
        legal_moves = [i for i in rangos if len(tablero_sim.agujeros[i]) > 0]
        if not legal_moves:
            
            siguiente = 2 if jugador_actual == 1 else 1
            return self._minimax(tablero_sim, graneros_sim, siguiente, depth + 1)

       
        if jugador_actual == self.lado:
            mejor = -float("inf")
            for move in legal_moves:
                copia_t = copy.deepcopy(tablero_sim)
                copia_g = copy.deepcopy(graneros_sim)

                pos_f = copia_t.actualizar(move, jugador_actual)
                self._intentar_captura_en_copia(copia_t, pos_f, jugador_actual)

                next_player = jugador_actual
                if not ((jugador_actual == 1 and pos_f == 6) or (jugador_actual == 2 and pos_f == 13)):
                    next_player = 2 if jugador_actual == 1 else 1

                score = self._minimax(copia_t, copia_g, next_player, depth + 1)
                mejor = max(mejor, score)
            return mejor
        else:
            peor = float("inf")
            for move in legal_moves:
                copia_t = copy.deepcopy(tablero_sim)
                copia_g = copy.deepcopy(graneros_sim)

                pos_f = copia_t.actualizar(move, jugador_actual)
                self._intentar_captura_en_copia(copia_t, pos_f, jugador_actual)

                next_player = jugador_actual
                if not ((jugador_actual == 1 and pos_f == 6) or (jugador_actual == 2 and pos_f == 13)):
                    next_player = 2 if jugador_actual == 1 else 1

                score = self._minimax(copia_t, copia_g, next_player, depth + 1)
                peor = min(peor, score)
            return peor

    def _intentar_captura_en_copia(self, tablero_sim, pos_final: int, jugador: int) -> None:
        if jugador == 1 and 0 <= pos_final <= 5:
            idx_yo = pos_final
        elif jugador == 2 and 7 <= pos_final <= 12:
            idx_yo = pos_final - 1
        else:
            return

        if len(tablero_sim.agujeros[idx_yo]) != 1:
            return

        opp_pos = 12 - pos_final
        if 0 <= opp_pos <= 5:
            idx_opp = opp_pos
        elif 7 <= opp_pos <= 12:
            idx_opp = opp_pos - 1
        else:
            return

        cantidad_op = len(tablero_sim.agujeros[idx_opp])
        if cantidad_op == 0:
            return

        total = 1 + cantidad_op
        if jugador == 1:
            tablero_sim.graneros[0] += total
        else:
            tablero_sim.graneros[1] += total

        tablero_sim.agujeros[idx_yo] = []
        tablero_sim.agujeros[idx_opp] = []
