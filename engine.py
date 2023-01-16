import chess 
import random
from stockfish import Stockfish
from nodo import Nodo

class Engine():

    def __init__(self) -> None:
        self.eng = Stockfish()
        self.nodos_terminales = {}
        self.posCont = 0

    # get_random_board -> devuelve una posición aleatoria de un tablero de ajedrez
    def get_random_board(self):
        n_moves = random.randint(100, 125)
        board = chess.Board()
        while n_moves > 0 and not board.is_game_over():
            choosen = random.choice(list(board.legal_moves))
            board.push(choosen)
            n_moves -= 1
        return board

    def stockfish_value(self, n):

        self.eng.set_fen_position(n.fen)
        eval   = self.eng.get_evaluation()
        best_m = self.eng.get_best_move()

        if n.terminal and n.fen not in self.nodos:
            self.nodos_terminales[n.fen] = eval

        if eval["type"] == "cp":
            return best_m, eval['value']/100

        elif eval["type"] == "mate":
            return best_m, eval['value']*100


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


    def heuristic_value(self, n):

        if n.terminal:
            res = n.board.outcome().result()
            if '/' in res:
                return 0
            else:
                return 100_000 if res[0] == '1' else -100_000

        # evaluación heurística de material
        return self.get_material_v(n.board)

    
    
    # alfa-beta prunning + memoization - LONG + FAST VERSION
    def minimax_ab(self, node, depth, maximize, alfa, beta):
        self.posCont += 1
        # check terminal o maxima alcanzada del minimax por ahora
        if node.terminal or depth == 0 or node.fen in self.nodos_terminales.keys():
            
            if node.fen not in self.nodos_terminales.keys():
                self.nodos_terminales[node.fen] = self.heuristic_value(node)
                # self.nodos[node.fen] = self.stockfish_value(node)[1]
            return self.nodos_terminales[node.fen]
            
        elif maximize:
            # estamos maximizando - actualizamos alfa
            act = -100_000
            for f in node.childs:
                hijo = Nodo(chess.Board(f))
                act  = max(act, self.minimax_ab(hijo, depth-1, False, alfa, beta))
                # cortamos cuando nuestro valor a_maximizar, sea mayor que el del minimizador - él siempre escogera este
                if act >= beta:
                    break
                alfa = max(alfa, act)
            return act
        else:
            # estamos minimizando - actualizamos alfa
            act = 100_000
            for f in node.childs:
                hijo = Nodo(chess.Board(f))
                act = min(act, self.minimax_ab(hijo, depth-1, True, alfa, beta))
                if act <= alfa:
                    break
                beta = min(beta, act)
            return act



    def get_move(self, board, depth=2,limit=None):

        self.posCont = 0

        # creamos el objeto tipo nodo con el board actual
        nodo = Nodo(board)
        move = None
         
        """
        print('Es el turno de:', ['Negras','Blancas'][maximize])
        print('El valor heurístico del nodo actual es: ', heuristic_value(nodo))
        print('Valor de stockfish calculado para el nodo: ', stockfish_value(nodo))
        """

        # A IMPLEMENTAR: GAMETREE CON memoization - almacenar los nodos recorridos en el mapa

        # recorremos los hijos del nodo actual
        maximize   = bool(board.turn)
        comparator = " < " if maximize else  " > " 
        v   = -100_000 if maximize else 100_000
        for m in nodo.child_moves:
            board.push(m)
            mmval = self.minimax_ab(Nodo(board), depth, not maximize, -100_000, 100_000)
            if eval(str(v)+comparator+str(mmval)) == True:
                v = mmval
                move = m
            board.pop()
        return move, v # if move != None else random.choice(list(board.legal_moves))