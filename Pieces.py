from abc import ABC, abstractmethod
from enum import Enum
from numpy import *


class Color(Enum):
    White = 1
    Black = 2

    def __neg__(self):
        return Color.White if self == Color.Black else Color.Black


def add_to_list(arr, x, y):
    if 0 <= x <= 7 and 0 <= y <= 7:
        arr.append([x, y])


class Piece(ABC):
    color = None
    current_position_x = None
    current_position_y = None
    capture_fields = []

    def __init__(self, color: Color, current_position_x, current_position_y, board):
        self.color = color
        self.current_position_x = current_position_x
        self.current_position_y = current_position_y
        board[self.current_position_x][self.current_position_y] = self

    def move(self, new_position_x, new_position_y, board):
        difference_in_x = self.current_position_x - new_position_x
        difference_in_y = self.current_position_y - new_position_y
        board[self.current_position_x][self.current_position_y] = None
        if [new_position_x, new_position_y] in self.capture_fields:
            board[new_position_x + sign(difference_in_x)][new_position_y + sign(difference_in_y)] = None
        self.current_position_x = new_position_x
        self.current_position_y = new_position_y
        board[new_position_x][new_position_y] = self
        self.capture_fields.clear()

    @abstractmethod
    def check_possible_moves(self, board):
        pass


class Man(Piece):

    def can_capture(self, board):
        moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for x, y in moves:
            try:
                if board[self.current_position_x + x][self.current_position_y + y] is not None and \
                        board[self.current_position_x + x][self.current_position_y + y].color != self.color and \
                        board[self.current_position_x + x * 2][self.current_position_y + y * 2] is None:
                    add_to_list(self.capture_fields, self.current_position_x + x * 2, self.current_position_y + y * 2)
            except IndexError:
                continue

    def check_possible_moves(self, board):
        moves = []
        try:
            self.can_capture(board)
            if self.color == Color.White:
                if board[self.current_position_x - 1][self.current_position_y - 1] is None:
                    add_to_list(moves, self.current_position_x - 1, self.current_position_y - 1)
                if board[self.current_position_x + 1][self.current_position_y - 1] is None:
                    add_to_list(moves, self.current_position_x + 1, self.current_position_y - 1)
            else:
                if board[self.current_position_x - 1][self.current_position_y + 1] is None:
                    add_to_list(moves, self.current_position_x - 1, self.current_position_y + 1)
                if board[self.current_position_x + 1][self.current_position_y + 1] is None:
                    add_to_list(moves, self.current_position_x + 1, self.current_position_y + 1)
            self.can_capture(board)
        except IndexError:
            pass
        return moves + self.capture_fields


class King(Piece):

    def check_possible_moves(self, board):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        moves = []
        for x, y in directions:
            for i in range(1, 8):
                try:
                    if board[self.current_position_x + x * i][self.current_position_y + y * i] is None:
                        add_to_list(moves, self.current_position_x + x * i, self.current_position_y + y * i)
                    else:
                        if board[self.current_position_x + x * i][self.current_position_y + y * i].color == self.color:
                            break
                        if board[self.current_position_x + x * i + x][self.current_position_y + y * i + y] is None:
                            add_to_list(self.capture_fields, self.current_position_x + x * i + x, self.current_position_y + y * i + y)
                            break
                except IndexError:
                    break
        return moves + self.capture_fields
