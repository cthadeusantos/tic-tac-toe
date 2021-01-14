# Tic-tac-toe's game v0.0.3
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
        return self.symbol


class PlayerFactory:
    @staticmethod
    def new(is_type):
        #self.new(is_type.lower())
        if is_type == 'human':
            return Human()
        elif is_type == 'computer':
            return Computer()
        else:
            raise Exception("Sorry, you must setting a human or computer player!")


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

    def add_piece(self, piece):
        if isinstance(piece, Piece):
            self.piece = piece
        else:
            raise Exception("Sorry, you cannot set piece!")

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

    def next_turn(self, board, maximizing_value):
        return self.minimax(board, maximizing_value)

    def minimax(self, board, maximizing_value):
        return 1


class Board:
    """Tic-tac-toe Board"""
    def __init__(self):
        self.grid = [0] * 9

    def board_is_full(self):
        return not self.grid.count(0)

    def board_is_empty(self):
        return self.grid.count(0) == 9

    def cell_is_empty(self, position):
        return self.grid[position] == 0

    def check_winner(self):
        sum3 = self.grid[0] + self.grid[4] + self.grid[8]                 # Diagonal 1
        sum4 = self.grid[2] + self.grid[4] + self.grid[6]                 # Diagonal 2
        if abs(sum3) == 3 or abs(sum4) == 3:
            return (sum3 == -3 or sum4 == -3)*-1 or (sum3 == 3 or sum4 == 3)*1
        for x in range(3):
            sum1 = self.grid[x*3] + self.grid[x*3+1] + self.grid[x*3+2]   # Horizontal
            sum2 = self.grid[x] + self.grid[x+3] + self.grid[x+6]         # Vertical
            if abs(sum1) == 3 or abs(sum2) == 3:
                return (sum1 == -3 or sum2 == -3)*-1 or (sum1 == 3 or sum2 == 3)*1
        return 0

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
        self.current_player = None
        self.winner = None

    def turn(self, player, position=None):
        if isinstance(player, Computer):
            position = player.next_turn(self.board, player.piece)

        if self.cell_is_empty(position):
            self.board.grid[position] = player.piece.value
            return True
        return False

    def play(self):
        print("*" * 10 + ' Welcome TicTacToe ' + "*" * 10)
        auxiliary = 0
        watchdog = True
        while watchdog:
            print('(1) Human x Computer, (2) Human x Human or (3) Computer x Computer')
            auxiliary = input()
            if auxiliary.isdigit():
                # if 0 < int(auxiliary) < 4:
                #     watchdog = False
                if auxiliary == '1':
                    print("Not implemented yet!")
                    # self.new_player('human')
                    # self.new_player('computer')
                elif auxiliary == '2':
                    watchdog = False
                    self.new_player('human')
                    self.new_player('human')
                elif auxiliary == '3':
                    print("Not implemented yet!")
                    # self.new_player('computer')
                    # self.new_player('computer')
        self.first_player()     # select who will play first
        print("First player will be " + self.player_name() +
              ' - Your piece is (' + self.player_piece() + ')')
        watchdog = True
        while watchdog and self.is_board_full:
            print(self.board)
            print(self.player_name(), "( ", self.player_piece(), " ) make your move, choose the board place (1-9): ")
            user_input = input()
            if user_input.isdigit():
                position = int(user_input)
                if 1 <= position <= 9:
                    position -= 1
                    if self.cell_is_empty(position):
                        self.turn(self.current_player, position)
                        if self.board.check_winner():
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

    def is_board_full(self):
        return self.board.board_is_full()

    def cell_is_empty(self, position):
        return self.board.cell_is_empty(position)

    def player_name(self):
        return self.current_player.name

    def player_piece(self):
        return self.current_player.piece.symbol

    def next_player(self):
        self.current_player = self.player[1] if self.current_player == self.player[0] else self.player[0]

    def new_player(self, is_type):
        self.player.append(PlayerFactory.new(is_type))
        self.player[len(self.player) - 1].add_piece(Piece())

    def first_player(self):
        """Choose first player randomily

        Args:
            None

        Returns:
            None
        """
        self.current_player = self.player[randint(0, 100) % 2]


# Main
a = Game()
watchdog = True
while watchdog:
    a.play()
    answer = input("Play again? (Y)es ou (N)ot ?")
    if answer.upper() == "N":
        watchdog = False

