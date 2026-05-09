# Breakout Game

Juego arcade inspirado en Breakout, hecho con Python y Pygame. Controlas una paleta, mantienes la pelota en juego y rompes todos los ladrillos para avanzar de nivel.

## Caracteristicas

- Movimiento fluido con flechas o teclas `A` y `D`.
- Lanzamiento manual de la pelota con `Espacio`.
- Sistema de vidas, puntaje y niveles.
- Rebote dinamico: la direccion de la pelota cambia segun el punto donde golpea la paleta.
- Ladrillos con colores y valores de puntaje diferentes.
- Aumento progresivo de velocidad al romper ladrillos.
- Pantalla de pausa con la tecla `P`.
- Pantallas de victoria, derrota y reinicio.

## Requisitos

- Python 3.10 o superior
- Pygame

Instala la dependencia con:

```bash
pip install pygame
```

## Como jugar

Ejecuta el juego desde la carpeta del proyecto:

```bash
python Breakoout.py
```

Controles:

| Tecla | Accion |
| --- | --- |
| `Enter` | Iniciar o reiniciar partida |
| `Flecha izquierda` / `A` | Mover paleta a la izquierda |
| `Flecha derecha` / `D` | Mover paleta a la derecha |
| `Espacio` | Lanzar pelota |
| `P` | Pausar o continuar |
| `Esc` | Salir desde el menu o terminar la partida |

## Objetivo

Rompe todos los ladrillos sin quedarte sin vidas. El juego tiene 3 niveles; cada nuevo nivel reconstruye el muro y mantiene tu puntaje acumulado.

## Estructura

```text
Breakout-Game/
├── Breakoout.py   # Codigo principal del juego
└── README.md      # Documentacion del proyecto
```

## Mejoras aplicadas

- Se corrigio el conteo de vidas para que la derrota ocurra al llegar a `0`.
- Se cambio el control por eventos a lectura continua del teclado, lo que hace mas suave el movimiento.
- Se agrego un sistema de lanzamiento para evitar que la pelota empiece sin preparacion.
- Se mejoro la colision con la paleta para que el jugador tenga mas control.
- Se agregaron niveles, pausa, HUD y pantallas finales con puntaje.
