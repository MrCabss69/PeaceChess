#!/usr/bin/env python3

# IMPORTS
from nodo import Nodo
from engine import Engine
import pandas as pd
import copy
import time

# timestamp
ts = time.time()


def get_openings():
    df = pd.read_csv('./resources/openings.csv',index_col=0)
    df = df.loc[:, ['moves']]
    df = df.applymap(lambda x: x.split(" "))
    print(df)
# get_openings()

       
engine = Engine()
nodos_terminales, posCont, v = {}, 0, -1 
while abs(v) != 100_000: 
    rand_board = engine.get_random_board()
    while rand_board.outcome() != None or not rand_board.is_valid():
        rand_board = engine.get_random_board()
    m, v   = engine.get_move(rand_board,2)
    if abs(v) == 100_000:
        post_board = copy.deepcopy(rand_board)
        post_board.push(m)
        break


print('Board escogido; ','\n', rand_board,'\n')
print('Numero de posiciones recorridas: ', engine.posCont,'\n')
print('Movimiento escogido: ', m,'\n')
print('Board de jaque mate: ','\n', post_board)