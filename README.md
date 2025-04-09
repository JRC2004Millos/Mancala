# 🏆 Proyecto Mancala en Consola

Este proyecto consiste en la implementación del clásico juego **Mancala**, desarrollado en Python y jugado mediante la consola. El objetivo es permitir partidas entre un jugador humano y un jugador sintético, el cual toma decisiones estratégicas basadas en una serie de heurísticas simples. El proyecto fue desarrollado como parte de la materia *Análisis y Diseño de Algoritmos*.

## 📌 Descripción General

Mancala es un juego de estrategia por turnos que consiste en mover semillas entre agujeros, con el fin de capturar la mayor cantidad posible. Esta implementación reproduce las reglas del juego y permite simular una partida entre un humano y un jugador artificial con distintos niveles de dificultad.

## 🧱 Arquitectura del Sistema

El sistema está estructurado en componentes principales:

- **Consola**: Interfaz en línea de comandos.
- **Juego**: Coordinador general del flujo del juego.
- **Tablero**: Modelo que representa los agujeros y graneros.
- **Ficha**: Representación de cada casilla con semillas.
- **Jugador Humano**: Recibe entrada desde la consola.
- **Jugador Sintético**: Toma decisiones de manera automática según una estrategia.

## 🧠 Estrategia del Jugador Sintético

El jugador automático elige su jugada siguiendo estas reglas (en orden de prioridad):

1. Captura de semillas enemigas.
2. Obtener un turno adicional si la jugada termina en el granero.
3. Evitar dejar vulnerables sus propios agujeros.
4. Elegir el agujero con mayor cantidad de semillas.

## 🚀 Ejecución

Para ejecutar el juego, asegúrate de tener Python 3 instalado y luego corre:

```bash
python mancala.py
```

## 🗂️ Estructura del Proyecto

```bash
mancala/
├── mancala.py              # Archivo principal
├── juego.py                # Clase Juego
├── tablero.py              # Clase Tablero y Ficha
├── jugador_humano.py       # Clase JugadorHumano
├── jugador_sintetico.py    # Clase JugadorSintético
├── consola.py              # Lógica de la interfaz en consola
├── README.md               # Este archivo
└── docs/
    └── diagrama_flujo_jugador_sintetico.png
```

## ✅ Funcionalidades
- Representación visual del tablero en consola.

- Validación de jugadas según reglas de Mancala.

- Jugador automático con lógica estratégica.

- Detección de fin del juego y cálculo del ganador.

## 🧪 Pruebas
El sistema ha sido probado con casos como:

- Jugadas válidas e inválidas.

- Capturas.

- Turnos extras.

- Fin de juego y conteo correcto de semillas.

## 📚 Créditos
Desarrollado por:

- Miguel Bayona Rivera

- Julián Rodríguez Céspedes

- Esteban Altamiranda Julio

Pontificia Universidad Javeriana — Abril de 2025
Materia: Análisis y Diseño de Algoritmos
