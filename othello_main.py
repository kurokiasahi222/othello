from OTHELLO_CLASS import Othello


def main():
    othello = Othello(8)
    print("Game begins...")
    othello.white_or_black()
    print(othello)

    while not othello.game_over():
        othello.move()
        print(othello)
    print("Game ends")
    if othello.get_winner() == "Tie":
        print("Draw. No winner")
    else:
        print("Winner: {}".format(othello.get_winner()))


if __name__ == '__main__':
    main()
