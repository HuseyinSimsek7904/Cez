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


    ai = ai_lib.AI(6)

    while True:
        process.stdin.write()
        process.stdin.flush()

        game.board.load_fen("np4PN/pp4PP/8/8/8/8/PP4pp/NP4pn w")
