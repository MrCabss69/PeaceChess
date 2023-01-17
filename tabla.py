import random

def rand_bitstring(l=64):
    return random.randint(1, (2**l)-1)

class BestMove():

    def __init__(self, move, val, depth):
        self.move = move
        self.val = val
        self.depth = depth

    def __str__(self):
        return str(self.move) + ' - ' + str(self.val) + ' - ' + str(self.depth)
    
class Tabla():
    def __init__(self):
        self.tab = [[rand_bitstring() for j in range(12)] for _ in range(64)]
        self.black_to_move = 0

        # usar los siguientes campos
        self.black_not_castle = 0
        self.white_not_castle = 0

        # fill w/ best-move during minimax_ab execution
        self.best_move = BestMove(None, None, None)