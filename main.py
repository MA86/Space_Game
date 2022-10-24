from game import *


def main():
    game = Game()
    if game.initialize():
        game.run_loop()
    game.shutdown()


if __name__ == "__main__":
    main()
