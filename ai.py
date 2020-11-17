import logic
import random

def generate_move(board):
    columns = len(board[0])
    move = False
    while True:
        move = random.randint(0, columns - 1)
        if logic.valid_move(2, move, board): break
    
    return move