# Tic-tac-toe's game v0.0.1
# 
# Python 3.8.3
#
#

from abc import ABCMeta, abstractmethod
from random import randint

class Piece:
    """Represents a piece on the board"""
    __counter = -1
    def __init__(self):
        """Init piece

        Args:
            None

        Returns:
            None
        """
        # The piece values could be -1 or 1
        self.value = Piece.__counter
        Piece.__counter += 2
        if Piece.__counter > 1:
            Piece.__counter -= 4

    def piece(self):
        """Represent a piece

        Args:
            None

        Returns:
            int: value from piece
        """
        return self.value

    def __str__(self):
        """The piece

        Args:
            None

        Returns:
            str: represents the piece ('O' or 'X')
        """
        return ['O', 'X'][(self.value + 1) // 2]


class Player(metaclass=ABCMeta):
    """Abstract class to represents a Player"""
    def __init__(self, board, name=None):
        self.board = board
        self.piece = None
        if name is not None:
            self.name = name
        else:
            self.name = "Player " + str(randint(1, 100000))

    def __str__(self):
        return self.name

    def set_piece(self):
        self.piece = Piece()
        print(self.name, " your piece will be ", self.piece)

    @abstractmethod
    def set_name(self):
        pass

    @abstractmethod
    def get_move(self):
        pass


class HumanPlayer(Player):
    """Concrete class to represents a Human Player"""
    def __init__(self, board, name=None):
        super().__init__(board, name=None)

    def set_name(self):
        print(self, ", What's is your name ? [ENTER] You will be ", self)
        auxiliary = input()
        if len(auxiliary) != 0:
            self.name = auxiliary
        self.set_piece()

    def get_move(self):
        watchdog = True
        while watchdog:
            print(self.name, "( ", self.piece, " ) make your move, choose the board place (1-9): ")
            user_input = input()
            if user_input.isdigit():
                auxiliary = int(user_input)
                if 1 <= auxiliary <= 9:
                    auxiliary -= 1
                    if self.board.cell_is_empty(auxiliary):
                        self.board.add_move(auxiliary, self.piece.value)
                        watchdog = False
                    else:
                        print('Invalid entry!')

class AIPlayer(Player):
    """Concrete class to represents a Computer Player"""
    def __init__(self, board, name=None):
        super().__init__(board, name=None)

    def set_name(self):
        self.name = "Joshua Falken"
        self.set_piece()

    def get_move(self):
        print(self.name, "( ", self.piece, " ) make his movement!")
        if self.board.board_is_empty():
            position = randint(0, 89)//10
            self.board.add_move(position, self.piece.value)
        else:
            board = self.board
            position = self.minimax(board, 0, self.board.turn, 0, 9)
            self.board.add_move(position, self.piece.value)

    def minimax(self, board, depth, max_turn, scores, target_depth):
        for x in range(9):
            if board[x] == 0:
                board[x] = self.piece.value
        return x

    def best_move(self, board, ):
        pass

    def find_best_move(self):
        pass


class Board:
    """Tic-tac-toe Board"""
    def __init__(self):
        self.grid = [0] * 9
        self.turn = True  # Max is true , Min is false

    def add_move(self, position, value):
        self.grid[position] = value
        self.turn = not self.turn

    def cell_is_empty(self, position):
        return self.grid[position] == 0

    def board_is_full(self):
        return not self.grid.count(0)
        # if not self.grid.count(0):
        #     return True
        # return False

    def board_is_empty(self):
        return self.grid.count(0) == 9

    def __str__(self):
        string = ""
        for x in range(9):
            if self.grid[x] == 0:
                string = string + str(x+1)
            else:
                string = string + ['O', 'X'][(self.grid[x] + 1) // 2]
            if x != 0 and (x+1) % 3 == 0 and (x+1) != 9:
                string = string + "\n-----\n"
            elif (x+1) != 9:
                string = string + "|"
        return string


class Game:
    """Game's logic"""
    def __init__(self):
        self.board = Board()
        self.player1 = HumanPlayer(self.board)
        self.player2 = None
        self.next_player = None
        self.winner = None

    def is_winner(self):
        sum3 = self.board.grid[0] + self.board.grid[4] + self.board.grid[8]                 # Diagonal 1
        sum4 = self.board.grid[2] + self.board.grid[4] + self.board.grid[6]                 # Diagonal 2
        for x in range(3):
            sum1 = self.board.grid[x*3] + self.board.grid[x*3+1] + self.board.grid[x*3+2]   # Horizontal
            sum2 = self.board.grid[x] + self.board.grid[x+3] + self.board.grid[x+6]         # Vertical
            if abs(sum1) == 3 or abs(sum2) == 3 or abs(sum3) == 3 or abs(sum4) == 3:
                self.winner = self.next_player
                return

    # Choose first player randomily
    def first_player(self):
        auxiliary = randint(0, 100)
        if (auxiliary / 2) == (auxiliary // 2):
            self.next_player = self.player1
        else:
            self.next_player = self.player2
        print('The first player will be ', self.next_player)


    def play(self):
        print('******* Welcome TicTacToe *******')
        watchdog = True
        while watchdog:
            print('You will play against another human(H) or computer(C)?')
            auxiliary = input()
            if auxiliary.isalpha():
                auxiliary = auxiliary.upper()
                if auxiliary == "H" or auxiliary == "C":
                    watchdog = False
                # if auxiliary == "C":
                #     print("AI not implemented yet!")

        if auxiliary == "H":
            self.player2 = HumanPlayer(self.board)
            self.next_player = self.player1
            for _ in range(2):
                self.next_player.set_name()
                self.next_player = self.player2
        else:       # If player will be an AI
            self.player1.set_name()
            self.player2 = AIPlayer(self.board)
            self.player2.set_name()
            self.next_player = self.player1

        self.first_player()

        watchdog = True
        while watchdog:
            print(self.board)
            self.next_player.get_move()
            self.is_winner()
            if self.winner is not None:
                print(self.board)
                print("The winner is ", self.winner, "(", self.next_player.piece, ")")
                watchdog = False
            elif self.board.board_is_full():
                watchdog = False
                print(self.board)
            self.next_player = self.player2 if self.next_player == self.player1 else self.player1
        if self.winner is None:
            print("DRAW!")
        print("Game over!")


# Main
a = Game()
a.play()
