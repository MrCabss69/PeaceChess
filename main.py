#!/usr/bin/env python3
import os
import time
import chess
from engine import Engine


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
            t, e  = time.time(), Engine()
            move,val  = e.get_move(board)
            try:
                print('\n',val,'\n')
                board.push(move)
            except:
                try:
                    print('\n',val,'\n')
                    board.push(chess.Move.from_uci(move))
                except:
                    print('Try again')
            
            print(board)
            print('Time to make the move: ', time.time()-t)
            print('Analized positions: ',e.posCont)
            
        elif cmd[0] == 'move':
            try:
                board.push_san(cmd[1])
                print(board)
            except:
                print('Wrong move format, try again')

        elif cmd[0] == 'eval':
            e = Engine()
            print('Stockfish_val:', e.stockfish_value(board))
            # print(heuristic_value(Nodo(board)))
        
        elif cmd[0] == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')