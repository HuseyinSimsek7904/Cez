import subprocess
import sys

import random

from libs import ai_lib, game_lib, move_lib
import pygame


def game_ended():
    if type(game.state) is game_lib.Mate:
        print(("Black", "White")[game.state.color] + " mated by " + game.state.by)

    elif type(game.state) is game_lib.Stalemate:
        print("Stalemate")

    while True:
        game.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()


if __name__ == '__main__':
    pygame.init()

    process = subprocess.Popen(('stdbuf', '-o0') + ('./main', '-s'),
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=sys.stderr,
                               text=True)

    game = game_lib.Game()
    game.board.load_fen("np4PN/pp4PP/8/8/8/8/PP4pp/NP4pn w")

    game.when_game_ended = game_ended

    ai = ai_lib.AI(6)

    while True:
        game.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        process.stdin.write("evaluate -r\n")
        try:
            process.stdin.flush()
        except Exception:
            input()
        print("Asked jazz for the move, waiting...")
        jazz = move_lib.from_text(process.stdout.readline())

        print(f"Got {jazz} from jazz, making...")
        game.make_move(jazz)
        process.stdin.write(f"makemove {jazz}\n")
        process.stdin.flush()
