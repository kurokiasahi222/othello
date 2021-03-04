import random


# initialize the board and print the board
class Othello:
    # constructor
    def __init__(self, m):
        self.board = []  # array for board
        self.boardSize = m
        self.human = ''
        self.robot = ''
        self.turn = 'W'
        self.winner = ''
        for i in range(8):
            row = []
            for j in range(8):
                row.append("_")
            self.board.append(row)
        self.W = "⚪"
        self.B = "⚫"
        self.board[3][3] = self.W
        self.board[4][4] = self.W
        self.board[4][3] = self.B
        self.board[3][4] = self.B

    # check if the move is not out of bounds
    def on_Board(self, x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

    # Check the valid move
    # this function is used to get the list of valid moves
    # also this function is used to get the list of tiles to filp
    def check_valid_moves(self, xStart, yStart):
        # ERROR if the tile is already occupied or out of bounds
        if self.board[xStart][yStart] != "_" or not self.on_Board(xStart, yStart):
            return False

        if self.turn == 'W':
            myTile = self.W
            yourTile = self.B
        else:
            myTile = self.B
            yourTile = self.W

        tiles_flip = []
        # checks all the direction on the board
        for vertical, horizontal in [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1],
                                     [-1, 1], [-1, 0]]:
            x = xStart
            y = yStart
            x += vertical
            y += horizontal

            # if there is an opponents piece next to my piece
            while self.on_Board(x, y) and self.board[x][y] == yourTile:
                x += vertical
                y += horizontal
                if self.on_Board(x, y) and self.board[x][y] == myTile:
                    # Flip tiles between reached myTile and initial myTile
                    # We do this by going back to the opposite direction
                    while True:
                        x -= vertical
                        y -= horizontal
                        if x == xStart and y == yStart:
                            break
                        tiles_flip.append([x, y])
        # no tiles were flipped => not a valid move
        if len(tiles_flip) == 0:
            return False
        return tiles_flip

    def get_Valid_Moves(self):
        m = self.boardSize
        validMoves = []
        for x in range(m):
            for y in range(m):
                if self.check_valid_moves(x, y):
                    validMoves.append([x, y])
        return validMoves

    def flip_tiles(self, xStart, yStart):
        flip_tiles = self.check_valid_moves(xStart, yStart)

        # return false if check_valid_move is False
        if not flip_tiles:
            return False

        if self.turn == 'W':
            myTile = self.W

        else:
            myTile = self.B

        self.board[xStart][yStart] = myTile
        for x, y in flip_tiles:
            self.board[x][y] = myTile
        return True

    # input function
    def get_input(self):
        moves = self.get_Valid_Moves()
        prompt = 'Please enter you choice: {} \n"[vertical, horizontal])" \n' \
                 'Enter with a space and no comma (ex: 0 0) : '.format(moves)
        user_input = input(prompt)
        input_lst = [int(item) for item in user_input.split(" ")]
        while input_lst not in moves:
            print("Error!")
            prompt = 'Please enter you choice: {} \n"[vertical, horizontal])" \n' \
                     'Enter with a space and no comma (ex: "0 0") : '.format(moves)
            user_input = input(prompt)
            input_lst = [int(item) for item in user_input.split(" ")]
        return tuple(input_lst)

    def move(self):
        next = None
        if self.turn == 'W' and self.human == 'W':
            next = self.get_input()
            print("\nYour move")
        elif self.turn == 'W' and self.robot == 'W':
            input('Press Enter to see the computer\'s move.')
            print("\nComputer move")
            next = self.get_random()
        elif self.turn == 'B' and self.human == 'B':
            next = self.get_input()
            print("\nYour move")
        else:
            input('Press Enter to see the computer\'s move.')
            print("\nComputer move")
            next = self.get_random()
        i, j = next
        self.flip_tiles(i, j)
        # self.board[i][j] = self.turn
        if self.game_over():
            return
        self.toggle()
        return next

    # computer agent
    def get_random(self):
        moves = self.get_Valid_Moves()
        corner_choice = []
        for x, y in moves:
            if self.get_Corner(x, y):
                corner_choice.extend([x, y])
                return corner_choice

        random_choice = random.choice(moves)
        print(random_choice)
        return random_choice
        # return random.choice(moves)

    # get a corner function
    def get_Corner(self, x, y):
        return (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or \
               (x == 7 and y == 7)

    # Check if its game over or not
    # It is game-over when the board is fulled
    # We check this using count
    # if board[i][j] == W, we add 1 to count; if count is 64, W won => return True
    # if board[i][j] == B, we subtract 1 to count; if count is -64, B won => return True
    # else return False
    def game_over(self):
        m = self.boardSize
        count_white = 0
        count_black = 0
        for i in range(m):
            for j in range(m):
                if self.board[i][j] == self.W:
                    count_white += 1
                elif self.board[i][j] == self.B:
                    count_black += 1
        if count_white > count_black and count_black + count_white == 64:
            self.winner = 'White'
            return True
        elif count_white < count_black and count_black + count_white == 64:
            self.winner = 'Black'
            return True
        elif count_white == count_black and count_black + count_white == 64:
            self.winner = "Tie"
            return True
        else:
            return False

    # get the winner
    def get_winner(self):
        return self.winner

    # alternates players turn
    def toggle(self):
        if self.turn == 'W':
            self.turn = 'B'
        else:
            self.turn = 'W'

    def white_or_black(self):
        prompt = ('Choose White or Black\n'
                  'White will go first and Black will go next\n'
                  'Enter "W" for White and "B" for Black: ')
        user_input = input(prompt)
        while user_input != 'W' and user_input != 'B':
            user_input = input("Error! Enter \"W\" for White and \"B\" for Black")

        if user_input == 'W':
            print("You will be White, you will make the move first")
            self.human = 'W'
            self.robot = 'B'
        else:
            print("You will be Black, computer will make the move first")
            self.human = 'B'
            self.robot = 'W'

    # Print function
    def __str__(self):
        m = self.boardSize
        output = ""
        for i in (range(m)):
            output += "\n"
            output += str(i)
            output += "\t"
            output += "\t".join(self.board[i])
            output += "\n"
        output += "\n"
        output += "\t"
        output += "\t".join([str(i) for i in range(8)])
        return output
