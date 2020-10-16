# Tic-tac-toe's game v0.0.2
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
        Piece.__counter *= -1
        self.value = Piece.__counter
        self.symbol = ['O', 'X'][(self.value == -1) * -1 + 1]

    def symbol(self):
        """Represent a piece

        Args:
            None

        Returns:
            str: symbol than represents piece [ X or O ]
        """
        return self.symbol

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
        return ['O', 'X'][(self.value + 1)]


class Player(metaclass=ABCMeta):
    """Abstract class to represents a Player"""
    __counter = 0

    @abstractmethod
    def __init__(self):
        self.piece = None
        self.name = None

    @staticmethod
    def new_player():
        """The player

        Args:
            None

        Returns:
            int: Number's player
        """
        assert(Player.__counter < 2), "Player limit reached!"
        Player.__counter += 1
        return Player.__counter

    def __str__(self):
        """The player

        Args:
            None

        Returns:
            str: Name of player
        """
        return self.name


class Human(Player):
    """Concrete class to represents a Human Player"""
    def __init__(self):
        super().__init__()
        self.name = "Human " + str(self.new_player())


# WARNING!
# This implementation class is not work YET!
#
class Computer(Player):
    """Concrete class to represents a Computer Player"""
    def __init__(self):
        super().__init__()
        self.name = "Computer " + str(self.new_player())


class Board:
    """Tic-tac-toe Board"""
    def __init__(self):
        self.grid = [0] * 9
        # self.turn = True  # Max is true , Min is false

    def is_winner(self):
        sum3 = self.grid[0] + self.grid[4] + self.grid[8]                 # Diagonal 1
        sum4 = self.grid[2] + self.grid[4] + self.grid[6]                 # Diagonal 2
        if abs(sum3) == 3 or abs(sum4) == 3:
            return True
        for x in range(3):
            sum1 = self.grid[x*3] + self.grid[x*3+1] + self.grid[x*3+2]   # Horizontal
            sum2 = self.grid[x] + self.grid[x+3] + self.grid[x+6]         # Vertical
            if abs(sum1) == 3 or abs(sum2) == 3 or abs(sum3) == 3 or abs(sum4) == 3:
                return True
        return False

    def turn(self, player, position):
        if self.cell_is_empty(position):
            self.grid[position] = player.piece.value
            return True
        return False

    def board_is_full(self):
        return not self.grid.count(0)

    def board_is_empty(self):
        return self.grid.count(0) == 9

    def cell_is_empty(self, position):
        return self.grid[position] == 0

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
        self.player = []
        self.player_in_action = None
        self.winner = None

    def play(self):
        print("*" * 10 + ' Welcome TicTacToe ' + "*" * 10)
        auxiliary = 0
        watchdog = True
        while watchdog:
            print('(1) Human x Computer, (2) Human x Human or (3) Computer x Computer')
            auxiliary = input()
            if auxiliary.isdigit():
                if 0 < int(auxiliary) < 4:
                    watchdog = False
        if auxiliary == '1':
            self.set_player(Human())
            self.set_player(Computer())
        elif auxiliary == '2':
            self.set_player(Human())
            self.set_player(Human())
        elif auxiliary == '3':
            self.set_player(Computer())
            self.set_player(Computer())
        self.first_player()
        print("First player will be " + self.player_name() +
              ' - Your piece is (' + self.player_piece() + ')')
        watchdog = True
        while watchdog and not self.board.board_is_full():
            print(self.board)
            print(self.player_name(), "( ", self.player_piece(), " ) make your move, choose the board place (1-9): ")
            user_input = input()
            if user_input.isdigit():
                auxiliary = int(user_input)
                if 1 <= auxiliary <= 9:
                    auxiliary -= 1
                    if self.cell_is_empty(auxiliary):
                        self.board.turn(self.player_in_action, auxiliary)
                        if self.board.is_winner():
                            self.winner = self.player_name()
                            watchdog = False
                        else:
                            self.next_player()
                    else:
                        print('Invalid choose!')
        print(self.board)
        print("Game over!")
        if not not self.winner:
            print("The winner is ", self.winner)
        else:
            print('Draw!')

    def cell_is_empty(self, position):
        return self.board.cell_is_empty(position)

    def player_name(self):
        return self.player_in_action.name

    def player_piece(self):
        return self.player_in_action.piece.symbol

    def player_piece_value(self):
        return self.player_in_action.piece.value

    def next_player(self):
        if self.player_in_action == self.player[0]:
            self.player_in_action = self.player[1]
        else:
            self.player_in_action = self.player[0]

    def set_player(self, instance):
        if isinstance(instance, Human) or isinstance(instance, Computer):
            self.player.append(instance)
            self.player[len(self.player) - 1].piece = Piece()
        else:
            raise Exception("Sorry, you must setting a human or computer player")

    def first_player(self):
        """Choose first player randomily

        Args:
            None

        Returns:
            None
        """
        self.player_in_action = self.player[randint(0, 100) % 2]


# Main
a = Game()
watchdog = True
while watchdog:
    a.play()
    answer = input("Play again? (Y)es ou (N)ot ?")
    if answer.upper() == "N":
        watchdog = False

