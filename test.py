#!/usr/bin/env python3

# IMPORTS
from engine import Engine
import pandas as pd
import random
import copy
import time


# CONSTANTS

# victory heuristic value
C = 100_000
# timestamp
ts = time.time()

"""
def get_openings():
    df = pd.read_csv('./resources/openings.csv',index_col=0)
    df = df.loc[:, ['moves']]
    df = df.applymap(lambda x: x.split(" "))
    print(df)
get_openings()
"""

       
engine = Engine()
nodos_terminales, posCont, v = {}, 0, -1 
while abs(v) > 0.9*C: 
    rand_board = engine.get_random_board(100)
    while rand_board.outcome() != None:
        rand_board = engine.get_random_board(100)
    m, v  = engine.get_move(rand_board, 3)
    if abs(v) > 0.9*C:
        post_board = copy.deepcopy(rand_board)
        post_board.push(m)
        break


print('Board escogido: ', '\n', rand_board, '\n')
print('Fen inicial: ', rand_board.fen(), '\n')
print('Movimiento escogido: ', m, '\n')
print('Numero de posiciones recorridas: ', engine.posCont, '\n')
print('Tiempo de ejecución: ', str(time.time()-ts))