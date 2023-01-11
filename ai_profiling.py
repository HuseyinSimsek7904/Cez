from libs import board_lib, ai_lib
import cProfile
import pstats

game_board = board_lib.Board()
game_board.load_fen("np4PN/pp4PP/8/8/8/8/PP4pp/NP4pn w")
ai = ai_lib.AI()

profiler = cProfile.Profile()
profiler.enable()

ai.calculate_best_move(game_board, 4)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats(pstats.SortKey.TIME)
stats.print_stats()
stats.dump_stats(filename="profile.prof")
