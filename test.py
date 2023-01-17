#!/usr/bin/env python3

# IMPORTS
from engine import Engine
import chess
import time


# CONSTANTS

# victory heuristic value
C = 100_000

# timestamp
ts = time.time()

DEPTH = 3
engine, reinicios = Engine(), 0
nodos_terminales, posCont, v = {}, 0, -1 
while abs(v) != C: 
    reinicios += 1
    rand_board = engine.get_random_board(100)
    while rand_board.outcome() != None:
        reinicios += 1
        rand_board = engine.get_random_board(100)
    m, v  = engine.get_move(rand_board, DEPTH)
    if abs(v) == C:
        post_board = chess.Board(rand_board.fen())
        post_board.push(m)
        break


print('Board escogido: ', '\n', rand_board, '\n')
print('Fen inicial: ', rand_board.fen(), '\n')
print('Movimiento escogido: ', m, '\n')
print('Numero de posiciones recorridas: ', engine.posCont, '\n')
print('Veces que se ha reinciado el board: ',reinicios)
print('Tiempo de ejecución: ', str(time.time()-ts))