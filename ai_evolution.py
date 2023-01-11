import random

from libs import ai_lib, game_lib
import pygame


def game_ended():
    global ai_white, ai_black

    if type(game.state) is game_lib.Mate:
        print(("Black", "White")[game.state.color] + " mated by " + game.state.by)

        if game.state.color:
            ai_black = ai_white.copy()
            ai_black.mutate()

        else:
            ai_white = ai_black.copy()
            ai_white.mutate()

    elif type(game.state) is game_lib.Stalemate:
        print("Stalemate")

    game.dump_data()
    game.board.load_fen("np4PN/pp4PP/8/8/8/8/PP4pp/NP4pn w")


if __name__ == '__main__':
    pygame.init()

    game = game_lib.Game()
    game.board.load_fen("np4PN/pp4PP/8/8/8/8/PP4pp/NP4pn w")

    game.when_game_ended = game_ended

    ai_white = ai_lib.AI()
    ai_black = ai_lib.AI()

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
        best_lines, best_score = (ai_black, ai_white)[game.board.color].calculate_best_move(game.board)

        print("All found alternatives:")
        for line in best_lines:
            print(*line[::-1], sep=", ")

        print(f"Score: {best_score} (for {('black', 'white')[game.board.color]})")

        move = random.choice(best_lines)
        print(f"Gonna play {move[::-1]}")

        game.make_move(move[-1])

        game.draw()
