import random

from libs import ai_lib, game_lib
import pygame


def game_ended():
    if type(game.state) is game_lib.Mate:
        print(("Black", "White")[game.state.color] + " mated by " + game.state.by)

    elif type(game.state) is game_lib.Stalemate:
        print("Stalemate")

    game.dump_data()
    game.board.load_fen("np4PN/pp4PP/8/8/8/8/PP4pp/NP4pn w")


if __name__ == '__main__':
    pygame.init()

    game = game_lib.Game()
    game.board.load_fen("np4PN/pp4PP/8/8/8/8/PP4pp/NP4pn w")

    game.when_game_ended = game_ended

    ai = ai_lib.AI(5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        print("=" * 50)
        print("Calculating...")

        best_lines, best_score = ai.calculate_best_move(game.board)
        move = random.choice(best_lines)[-1]
        length = len(best_lines[0])

        print("All found alternatives:")
        for line in best_lines:
            print(*line[::-1], sep=", ")

        if best_score is None:
            print("Score is not calculated")

        else:
            print(f"Score: {-best_score}")

        print(f"Length: {length}")

        print(f"Gonna play {move}")

        game.make_move(move)
        game.draw()
