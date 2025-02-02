import random

from libs import game_lib, move_lib
import pygame
import math
import datetime
import subprocess
import sys


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

    fen = "np4PN/pp4PP/8/8/8/8/PP4pp/NP4pn w"

    game = game_lib.Game()
    game.board.load_fen(fen)

    process = subprocess.Popen(('stdbuf', '-o0') + ('./main', '-d%', 'aitime 1000', f'loadfen "{fen}"'),
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=sys.stderr,
                               text=True)

    game.when_game_ended = game_ended
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        mouse_pos = game_lib.get_position_from_rect(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_ended()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_ended()

                elif event.key == pygame.K_u:
                    process.stdin.write(f"undomove\nsavefen\n")
                    process.stdin.flush()

                    jazz_fen = process.stdout.readline()
                    print(jazz_fen[:-1])
                    game.board.load_fen(jazz_fen[:-1])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = game_lib.get_position_from_rect(event.pos)
                if pos.is_valid:
                    game.held = pos

            elif event.type == pygame.MOUSEBUTTONUP:
                for move in game.board.possible_moves:
                    if game.held and move.from_ == game.held and move.to == mouse_pos:
                        game.make_move(move)
                        process.stdin.write(f"makemove {move}\n")
                        process.stdin.flush()
                        game.held = None
                        game.draw()

                        process.stdin.write("evaluate -r\n")
                        try:
                            process.stdin.flush()
                        except Exception:
                            input("fuck, waiting for enter")

                        print("Asked jazz for the move, waiting...")
                        jazz_txt = process.stdout.readline()
                        jazz = move_lib.from_text(jazz_txt)

                        print(f"Got {jazz} from jazz, making...")
                        game.make_move(jazz)
                        process.stdin.write(f"makemove {jazz}\n")
                        process.stdin.flush()

                game.held = None

        game.draw()
