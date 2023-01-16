#!/usr/bin/env python3
import os
import sys
import time
import random
import chess
import copy
from stockfish import Stockfish
from nodo import v, Nodo

class Engine():
    def __init__(self) -> None:
        self.eng = Stockfish()
        self.nodos = {}

    def stockfish_value(self, n):
        self.eng.set_fen_position(n.fen)
        eval   = self.eng.get_evaluation()
        best_m = self.eng.get_best_move()
        if n.fen not in self.nodos:
            self.nodos[n.fen] = eval

        if eval["type"] == "cp":
            return best_m, eval['value']/100
        elif eval["type"] == "mate":
            return best_m, eval['value']*100
    """
    def heuristic_value(self,n):
        global v
        if n.terminal:
            res = n.board.outcome().result()
            if '/' in res:
                return 0
            else:
                return float('inf') if res[0] == '1' else float('-inf')
        return sum([v[l] for l in n.board.fen().split(" ")[0] if l in v.keys()])
    """

    def minimax_ab(self, node, depth, maximize, alfa, beta):
        if node.terminal or depth == 0:
            
            if node.fen not in self.nodos.keys():
                # return self.heuristic_value(node)
                self.nodos[node.fen] = self.stockfish_value(node)[1]
            return self.nodos[node.fen]
            
        if node.fen in self.nodos.keys():
            return self.nodos[node.fen]
        elif maximize:
            # estamos maximizando - actualizamos alfa
            act = float('-inf')
            for f in node.childs:
                act = max(act, self.minimax_ab(Nodo(chess.Board(f)), depth-1, False, alfa, beta))
                # cortamos cuando nuestro valor a_maximizar, sea mayor que el del minimizador - él siempre escogera este
                if act >= beta:
                    break
                alfa = max(beta, act)
            return act
        else:
            # estamos minimizando - actualizamos alfa
            act = float('inf')
            for f in node.childs:
                act = min(act, self.minimax_ab(Nodo(chess.Board(f)), depth-1, True, alfa, beta))
                if act <= beta:
                    break
                beta = min(alfa, act)
            return act

    def get_move(self, board, limit=None):

        nodo, legals = Nodo(board), list(board.legal_moves)
        maximize     = bool(board.turn)

        # memoization - almacenamos el nodo en el map
        if nodo.fen in self.nodos.keys():
            return self.nodos[nodo.fen]

        """
        print('Es el turno de:', ['Negras','Blancas'][maximize])
        print('El valor heurístico del nodo actual es: ', heuristic_value(nodo))
        print('Valor de stockfish calculado para el nodo: ', stockfish_value(nodo))
        """

        # recorremos los hijos del nodo actual
        for p in nodo.childs:
            board = chess.Board(p)
            if board.fen() not in self.nodos.keys():
                self.nodos[board.fen()] = self.minimax_ab(Nodo(board), 2, maximize, float('-inf'), float('inf'))
            act = max(act,self.nodos[board.fen()]) if maximize else min(act,self.nodos[board.fen()])
        return act


e = Engine()
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
            move = e.get_move(board)
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
            print('Stockfish_val:',e.stockfish_value(Nodo(board)))
            # print(heuristic_value(Nodo(board)))
        
        elif cmd[0] == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')