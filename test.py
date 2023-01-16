#!/usr/bin/env python3

# IMPORTS
from nodo import v, Nodo
import pandas as pd
import numpy as np
import chess
import random
import sys
import os
import time

# timestamp
ts = time.time()

# get_random_board -> devuelve una posición aleatoria de un tablero de ajedrez
def get_random_board():
    n_moves = random.randint(25, 125)
    board = chess.Board()
    while n_moves > 0 and not board.is_game_over():
        choosen = random.choice(list(board.legal_moves))
        board.push(choosen)
        n_moves -= 1
    return board



# hval -> valor heurístico del nodo
def hval(nodo):
    global v
    if nodo.board.outcome() != None:
        # si la partida ya ha terminado
        res = nodo.board.outcome().result()
        if '/' in res:
            return 0
        else:
            return float('inf') if res[0] == '1' else float('-inf')
    return sum([v[l] for l in nodo.board.fen().split(" ")[0] if l in v.keys()])



def get_openings():

    df = pd.read_csv('./resources/openings.csv',index_col=0)
    df = df.loc[:, ['moves']]
    df = df.applymap(lambda x: x.split(" "))
    print(df)
# get_openings()

# minimax, memoization y diccionario: fen-valor
nodos = {}
def minimax_ab(node, depth, maximize, alfa, beta):
    global nodos
    print(node.board,'\n',depth,maximize,alfa,beta,'\n\n\n\n\n')
    if depth < 0:
        pass
    elif depth == 0:
        if node.fen in nodos.keys():
            to_compare = [nodos[node.fen],hval(node)]
            nodos[node.fen] = max(to_compare) if maximize else min(to_compare)
            return nodos[node.fen]
    if node.terminal:
        if not node.fen in nodos.keys(): 
            nodos[node.fen] = hval(node)
        return nodos[node.fen]
        
    if maximize:
        # actualizar alfa
        act = float('-inf')
        for _, h in node.get_childs().items():
            act = max(act, minimax_ab(h, depth-1, False, alfa, beta))
            if act >= beta:
                break
            alfa = max(alfa, act)
    else:
        # actualizar beta
        act = float('inf')
        for _, h in node.get_childs().items():
            act = min(act, minimax_ab(h, depth-1, True, alfa, beta))
            if act <= beta:
                break
            beta = min(beta, act)
    if node.fen in nodos.keys():
        if maximize:
            nodos[node.fen] = max(nodos[node.fen],act)
        else:
            nodos[node.fen] = min(nodos[node.fen],act)
    else:
        nodos[node.fen] = act
    return nodos[node.fen]

rand_board = get_random_board()
while rand_board.outcome() != None:
    rand_board = get_random_board()
n = Nodo(rand_board)

print('Board escogido ', rand_board,'\n')

print('Minimax: ','\n')

minimax_ab(n,1,bool(rand_board.turn),float('-inf'), float('inf'))

print()
print()
print()
print()
print('Nodos resultado: ')
for k, v in nodos.items():
    print(v.board)
    print()
    print()

""" 
# RECORREMOS NODOS ALEATORIOS Y ALMACENAMOS LOS VALORES HEURÍSTICOS
r = {}
for _ in range(1000):

    # creamos un board aleatorio
    b = get_random_board()

    # añadimos el nodo al mapa recorrido
    if b.fen() not in r.keys():
        new_nodo   = Nodo(b)
        r[b.fen()] = (Nodo(b), hval(new_nodo))



for key, val in r.items():
    node, v = val[:]



print('Nodos encontrados: ', len(r.keys()))
print('Execution timestap: ', time.time()-ts)
"""
