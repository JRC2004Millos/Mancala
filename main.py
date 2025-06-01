from tablero import Tablero
from mancala import Interfaz
from juego import Juego

if __name__ == "__main__":
    tablero = Tablero()
    interfaz = Interfaz()
    juego = Juego(tablero, interfaz)
    juego.iniciarJuego()
