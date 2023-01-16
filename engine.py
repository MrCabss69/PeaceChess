#!/usr/bin/env python3
import os
import sys
import time
import random
import chess
import copy
from stockfish import Stockfish
from nodo import v, Nodo

def stockfish_value(n):
    eng    = Stockfish()
    eng.set_fen_position(n.fen)
    eval   = eng.get_evaluation()
    best_m = eng.get_best_move()
    if eval["type"] == "cp":
        return best_m, eval['value']/100
    elif eval["type"] == "mate":
        return best_m, eval['value']*100
    
def heuristic_value(n):
    global v
    if n.terminal:
        res = n.board.outcome().result()
        if '/' in res:
            return 0
        else:
            return float('inf') if res[0] == '1' else float('-inf')
    return sum([v[l] for l in n.board.fen().split(" ")[0] if l in v.keys()])


def minimax_ab(node, depth, maximize, alfa, beta):
    if node.terminal or depth == 0:
        return heuristic_value(node)
    elif maximize:
        # actualizar alfa
        act = float('-inf')
        for _, h in node.get_childs().items():
            act = max(act, minimax_ab(h, depth-1, False, alfa, beta))
            if act >= beta:
                break
            alfa = max(alfa, act)
        return act
    else:
        # actualizar beta
        act = float('inf')
        for _, h in node.get_childs().items():
            act = min(act, minimax_ab(h, depth-1, True, alfa, beta))
            if act <= beta:
                break
            beta = min(beta, act)
        return act

def get_move(board, limit=None):

    # TODO: almacenamos el nodo en el mapa
    nodo, legals = Nodo(board), list(board.legal_moves)
    maximize     = bool(board.turn)

    print('Es el turno de:', ['Negras','Blancas'][maximize])
    print('El valor heurístico del nodo actual es: ', heuristic_value(nodo))
    print('Valor de stockfish calculado para el nodo: ', stockfish_value(nodo))

    # recorremos una parte de los hijos
    vals       = {}
    for exp in random.sample(legals, random.randint(1,len(legals)):
        board.push(exp)
        vals[exp.uci()] = minimax_ab(Nodo(board), 4, maximize, float('-inf'), float('inf'))
        board.pop()
    if maximize:
        res = max(vals, key=vals.get)
    else:
        res = min(vals, key=vals.get)
    print(res)
    return res


if __name__ == "__main__":
    board = chess.Board()
    print('\n', 'Board and starting position setted')
    print(board)

    while 1:

        
        cmd = input().split(" ")

        if cmd[0] == "show":
            print(board.legal_moves)
            print(board)

        elif cmd[0] == "go":
            t = time.time()
            move = get_move(board)
            board.push(chess.Move.from_uci(move))
            print('Time to make the move: ', time.time()-t)
            print(board)

        elif cmd[0] == 'move':
            try:
                
                board.push_san(cmd[1])
                print(board)
            except:
                print('Wrong move format, try again')

        elif cmd[0] == 'eval':
            print(stockfish_value(Nodo(board)))
        
        elif cmd[0] == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
