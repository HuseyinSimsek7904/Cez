from libs import ai_lib, board_lib

ai = ai_lib.AI(7)
board = board_lib.Board()
board.load_fen("np4PN/pp4PP/8/8/8/8/PP4pp/NP4pn w")

found_lines, score = ai.calculate_best_move(board)

print(f"Score: {score}")
print(*found_lines, sep="\n")
