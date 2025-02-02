from libs import board_lib

board = board_lib.Board()
board.load_fen("np4PN/pp4PP/8/8/8/8/PP4pp/NP4pn w")

def list_depth(board, depth):
    if depth == 0: return 1

    leaves = 0
    for move in board.possible_moves:
        new_board = board.copy()
        new_board.make_move(move)
        leaves += list_depth(new_board, depth - 1)

    return leaves

print(list_depth(board, int(input("depth: "))))
