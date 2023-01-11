import random

from libs import ai_lib, game_lib
import pygame
import math
import datetime


def game_ended():
    if type(game.state) is game_lib.Mate:
        print(("Black", "White")[game.state.color] + " mated by " + game.state.by)

    elif type(game.state) is game_lib.Stalemate:
        print("Stalemate")

    game.dump_data()
    pygame.quit()

    quit()


if __name__ == '__main__':
    pygame.init()

    game = game_lib.Game()
    game.board.load_fen("np4PN/pp4PP/8/8/8/8/PP4pp/NP4pn w")

    game.when_game_ended = game_ended

    ai = ai_lib.AI(5)

    while True:
        mouse_pos = game_lib.get_position_from_rect(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_ended()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_ended()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = game_lib.get_position_from_rect(event.pos)
                if pos.is_valid:
                    game.held = pos

            elif event.type == pygame.MOUSEBUTTONUP:
                for move in game.board.possible_moves:
                    if game.held and move.from_ == game.held and move.to == mouse_pos:
                        game.make_move(move)

                        game.held = None
                        game.draw()

                        print("=" * 50)
                        print("Calculating...")
                        start = datetime.datetime.now()

                        best_lines, best_score = ai.calculate_best_move(game.board)
                        move = random.choice(best_lines)[-1]
                        length = len(best_lines[0])

                        print("All found alternatives:")
                        for line in best_lines:
                            print(*line[::-1], sep=", ")

                        print(f"Calculated in {datetime.datetime.now() - start}")

                        if best_score is None:
                            print("Score is not calculated")

                        else:
                            print(f"Score: {-best_score}")

                        print(f"Length: {length}")

                        print(f"Gonna play {move}")

                        game.make_move(move)

                        if best_score == math.inf:
                            print("I already won, just stop playing.")

                        elif best_score == -math.inf:
                            print("Well, if you can play perfect you can win.")

                        break

                game.held = None

        game.draw()
