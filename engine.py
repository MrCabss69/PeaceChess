# -*- coding: utf-8 -*-



# from stockfish import Stockfish
from tabla import Tabla, BestMove
import time
import chess
import random
random.seed(10)


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



class Engine():

    # constructor
    def __init__(self, depth=3) -> None:
        # self.eng = Stockfish()
        self.depth = depth
        self.posCont = 0
        self.tabla = Tabla()
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

    def rate_move(self, board, move):

        # guardamos el valor antes del movimiento
        v = 0.
        ov = self.heuristic_value(board)

        # hacemos el movimiento
        board.push(move)

        # aplicar heurística de material

        # aplicar heurística de jaques
        if board.is_check():
            v += 1.5

        # aplicar heurística de capturas
        # TODO: REFACTOR - PSEUDO MVP-LVP
        nv = self.heuristic_value(board)
        piece_moved = board.piece_at(move.from_square)
        if piece_moved:
            piece_moved_val = chess.PIECE_TYPES[piece_moved.piece_type-1]
            if nv > ov:
                # cuanto más vale la pieza que captura, menos vale la captura
                v += abs(nv-ov) * (1 / piece_moved_val)
            elif nv < ov:
                v -= abs(nv-ov) * (1 / piece_moved_val)

        # aplicar heuristica de control de casillas
        #     - libres
        #     - en territorio enemigo
        #     - centrales

        # deshacemos el movimiento y devolvemos el valor 'a pripri'
        board.pop()
        return v

    def get_childs(self, board):
        to_explore = list(board.legal_moves)
        # no te olvides del reverse = True, melón
        to_explore.sort(key=lambda x: self.rate_move(board, x), reverse=True)
        moves = []
        hash = zoibrist_hash(self.tabla, board)
        if hash in self.d.keys() and self.d[hash] != None:
            moves.append(self.d[hash].move)

        for m in to_explore:
            board.push(m)
            if board.is_valid():
                moves.append(m)
            board.pop()
        return moves

    # alfa-beta prunning + memoization - LONG + "FAST" VERSION

    def minimax_ab(self, board, depth, maxim, alfa, beta, moves=[]):

        self.posCont += 1

        if depth == 0 or board.is_game_over():
            return self.heuristic_value(board)

        hash = zoibrist_hash(self.tabla, board)
        anterior = None

        if maxim:
            # estamos maximizando - actualizamos alfa
            act = -100_000

            for f in self.get_childs(board):
                board.push(f)
                act2 = act - 1 + 1  # chorrada para evitar copia directa
                act = max(act, self.minimax_ab(
                    board, depth-1, False, alfa, beta))
                if anterior == None or act > act2:
                    anterior = f
                    self.d[hash] = BestMove(anterior, act, depth)
                board.pop()
                # cortamos cuando nuestro valor_a_maximizar sea mayor que el del minimizador
                # el adversario (mimizador) siempre escogera el menor en su turno
                if act >= beta:
                    break
                alfa = max(alfa, act)
            return act
        else:
            # estamos minimizando - actualizamos alfa
            act = 100_000
            for f in self.get_childs(board):
                board.push(f)
                act2 = act - 1 + 1
                act = min(act, self.minimax_ab(
                    board, depth-1, True, alfa, beta))
                if anterior == None or act < act2:
                    anterior = f
                    self.d[hash] = BestMove(anterior, act, depth)
                # cortamos cuando nuestro valor_a_minimizar sea menor que el del adversario
                # él como maximizador siempre escogera el mayor de los valores en su turno
                board.pop()
                if act <= alfa:
                    break
                beta = min(beta, act)
        return act

    def get_move(self, board):

        # TABLA DE TRANSPOSICIONES - ZOIBRIST HASHING
        hash = zoibrist_hash(self.tabla, board)

        if not hash in self.d.keys() or self.d[hash].depth < self.depth:
            maxim = board.turn == chess.WHITE
            best_v = -100_000 if maxim else 100_000
            best_m = None
            for m in self.get_childs(board):
                board.push(m)
                val = self.minimax_ab(
                    board, self.depth, not maxim, -100_000, 100_000)
                if (maxim and best_v < val) or (not maxim and best_v > val):
                    best_v, best_m = val, m
                    self.d[hash] = BestMove(best_m, best_v, self.depth)
                board.pop()

        return self.d[hash]

    def solve_position(self, fen, max_d):
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



    # stockfish_value -> devuelve la evaluación de stockfish para un bord dado em la forma (best_move,board_eval)
    def stockfish_value(self, board):

        self.eng.set_fen_position(board.fen())
        eval = self.eng.get_evaluation()
        best_m = self.eng.get_best_move()

        if board.is_game_over() and board.fen() not in self.ter:
            self.ter[board.fen()] = eval

        if eval["type"] == "cp":
            return best_m, eval['value']/100

        elif eval["type"] == "mate":
            return best_m, 100_000 if eval['value'] > 0 else best_m, -100_000



# EJEMPLOS - solo cuando se ejecute directamnte engine.py

if __name__ == "main":

    # Example 1 - solve a forced mate in 2
    t = time.time()
    eng = Engine()
    fen = '8/5p2/7k/p1p3Rp/1pPr1q2/1P1P3R/P3r3/1K6 w - - 0 49'
    bm = eng.solve_position(fen, 3)
    print(bm)
    print(len(eng.d.keys()))
    print(time.time()-t)


    # Example 2 - playing 5 turns exploring moves for both players
    e = Engine(3)
    b = chess.Board()
    cont = 10
    while cont > 0 and b.is_valid() and not b.is_game_over():
        print(b, '\n', '\n')
        print('Turno de negras:', b.turn == chess.BLACK)
        bm = e.get_move(b).move
        b.push(bm)
        cont -= 1
    print(b,'\n')
    print('Number of stored hashes: ', len(e.d.keys()))
