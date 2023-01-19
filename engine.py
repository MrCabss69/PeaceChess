# -*- coding: utf-8 -*-
import time
import chess
import random
random.seed(10)

from tabla import Tabla, BestMove
tabla = Tabla()


indices = ['P', 'R', 'N', 'B', 'Q', 'K']
indices += [l.lower() for l in indices]
indices = {v: k for k, v in enumerate(indices)}



def zoibrist_hash(table, board):
    global indices
    table.black_to_move = int(board.turn == chess.BLACK)
    h = 0
    if board.turn == chess.BLACK:
        h = h ^ table.black_not_castle
        h = h ^ table.black_to_move
    else:
        h = h ^ table.white_not_castle
    for i in range(64):
        p = board.piece_at(i)
        if p != None:
            h = h ^ table.tab[i][indices[p.symbol()]]
    return h


def fn(x,m): return max(x[0],x[1]) if m else min(x[0],x[1])


class Engine():
    
    global fn, tabla


    # constructor
    def __init__(self, depth=3) -> None:
        # self.eng = Stockfish()
        self.tabla = tabla
        self.depth = depth
        self.d = {}


    # get_material_v -> devuelve como valor numérico el desequilibrio material
    def get_material_v(self, board):
        v = 0
        for i in range(64):
            piece = board.piece_at(i)
            if piece:
                piece_value = chess.PIECE_TYPES[piece.piece_type-1]
                if piece.color == chess.WHITE:
                    v += piece_value
                else:
                    v -= piece_value
        return v


    # heuristic_value -> devuelve un valor heurístico para un nodo dado
    def heuristic_value(self, board):
        # tablero terminal
        if board.is_game_over():
            res = board.outcome().result()
            if '/' in res:
                return 0
            else:
                return 100_000 if res[0] == '1' else -100_000
        # evaluación heurística de material
        else:
            return self.get_material_v(board)


    # rate_move -> devuelve un valor de cuán bueno es un movimiento 'a primeras'
    def rate_move(self, board, move, depth):

        # calculate the hash
        hash = zoibrist_hash(self.tabla, board)
        if hash in self.d.keys() and self.d[hash].depth >= depth:
          # mejor hijo precalculado - recorrerlo este hijo sí o sí
          return 99_000 
      
        # hacemos el movimiento
        board.push(move)

        v = 0.
        ov = self.heuristic_value(board)
        
        # aplicar heurística de jaques
        if board.is_check():
            v += 1.5


        # aplicar heurística de material + capturas
        # TODO: REFACTOR - PSEUDO MVP-LVP
        
        nv = self.heuristic_value(board)
        piece_moved = board.piece_at(move.from_square)
        if piece_moved:
            piece_v = chess.PIECE_TYPES[piece_moved.piece_type-1]
            if nv > ov:
                # cuanto más vale la pieza que captura, menos vale la captura
                v += abs(nv-ov) * (1 / piece_v)
            elif nv < ov:
                v -= abs(nv-ov) * (1 / piece_v)

        # aplicar heuristica de control de casillas
        #     - libres
        #     - en territorio enemigo
        #     - centrales

        # deshacemos el movimiento y devolvemos el valor 'a pripri'
        board.pop()
        return v

    
    # get_childs -> devuelve los nodos hijos ordenados
    def get_childs(self, board, depth):
        
        # hash de la posición
        hash = zoibrist_hash(self.tabla, board)
        
        # no te olvides del reverse = True, melón
        to_explore = list(board.legal_moves).sort(key=lambda x: self.rate_move(board, x,depth), reverse=True)
        
        # comprobamos si ya tenemos la evaluación
        if hash in self.d.keys() and self.d[hash] != None:
            if self.d[hash].depth >= depth:
                return [self.d[hash].move]
            moves = [ self.d[hash].move ]
        else: 
            moves = []
        
        # añadimos los hijos en orden de exploración
        for m in to_explore:
            board.push(m)
            if board.is_valid():
                moves.append(m)
            board.pop()
        return moves



    # alfa-beta prunning + memoization - LONG + "FAST" VERSION
    def minimax_ab(self, board, depth, maxim, alfa, beta, moves=[]):

        # check si fin de evaluación o nodo terminal
        if depth == 0 or board.is_game_over():
            return self.heuristic_value(board)

        hash = zoibrist_hash(self.tabla, board)
        
        # check si el nodo está en las tablas Zoibrist
        if hash in self.d.keys() and self.d[hash].depth >= depth:
          return self.d[hash].val
        
        v_act    = -100_000 if maxim else 100_000
        anterior = None
        
        # exploramos la rama
        for f in self.get_childs(board,depth):
          v_ant = v_act + 0 
          board.push(f)
          v_act = fn( [ v_act, self.minimax_ab(board, depth-1, False if maxim else True, alfa, beta) ] , maxim)
          board.pop()
          # si hemos actualizado el valor para el nodo
          # => store into hash_dict
          if anterior == None or v_act != v_ant:
            anterior = f
            self.d[hash] = BestMove(anterior, v_act, depth)
          if maxim:
            # cortamos cuando nuestro valor_a_maximizar sea mayor que el del minimizador
            # el adversario (mimizador) siempre escogera el menor en su turno
            if v_act >= beta: break
            alfa = max(alfa, v_act)
          else:
            # cortamos cuando nuestro valor_a_minimizar sea menor que el del adversario
            # él como maximizador siempre escogera el mayor de los valores en su turno
            if v_act <= alfa: break
            beta = min(beta, v_act)
        return v_act


    # get_move -> devuelve un movimiento en un board en base a la busqueda
    def get_move(self, board):

        # TABLA DE TRANSPOSICIONES - ZOIBRIST HASHING
        hash = zoibrist_hash(self.tabla, board)

        # si la entrada no está o tiene menor profunidad - se recalcula la rama
        if not hash in self.d.keys() or self.d[hash].depth < self.depth:
            maxim          = board.turn == chess.WHITE
            best_v, best_m = (-100_000 if maxim else 100_000, None)
            for m in self.get_childs(board, self.depth):
                board.push(m)
                val = self.minimax_ab(board, self.depth, not maxim, -100_000, 100_000)
                if (maxim and best_v < val) or (not maxim and best_v > val):
                    best_v, best_m = val, m
                    self.d[hash] = BestMove(best_m, best_v, self.depth)
                board.pop()
                
        # devuelve la entrada de la tabla
        return self.d[hash]


    def solve_position(self, fen, max_d):
        # resuelve una posición de profunidad 4 (mates, ejercicios, etc..)
        self.depth = max_d
        return self.get_move(chess.Board(fen))


    # get_random_board -> devuelve una posición aleatoria de un tablero de ajedrez
    def get_random_board(self, n_moves=100):
        board = chess.Board()
        while n_moves > 0 and not board.is_game_over():
            choosen = random.choice(list(board.legal_moves))
            board.push(choosen)
            if not board.is_valid():
                board.pop()
            n_moves -= 1
        return board






# EJEMPLOS - solo cuando se ejecute directamnte engine.py
if __name__ == "__main__":

    # Example 1 - solve a forced mate in 2
    t = time.time()
    eng = Engine()
    fen = '8/5p2/7k/p1p3Rp/1pPr1q2/1P1P3R/P3r3/1K6 w - - 0 49'
    board = chess.Board(fen)
    print('Board en el que encontrar el mate','\n',board)
    
    bm = eng.solve_position(fen, 3)
    board.push(bm.move)
    print('Tiempo usado para resolver la posición:',time.time()-t)
    print('Comienzo del patrón de mate: ',bm.move.uci(),'\n', board)
    print(bm)
    print(len(eng.d.keys()))
    
    """
    print()
    print()
    # Example 2 - playing 5 turns exploring moves for both players
    t = time.time()
    e = Engine(3)
    b = chess.Board()
    cont = 5
    print('Simulando partida..')
    while cont > 0 and b.is_valid() and not b.is_game_over():
        print('Movimiento ', 4-cont)
        print(b, '\n', '\n')
        #print('Turno de negras:', b.turn == chess.BLACK)
        bm = e.get_move(b).move
        b.push(bm)
        cont -= 1
    print(b,'\n')
    print('Number of stored hashes: ', len(e.d.keys()))
    """
