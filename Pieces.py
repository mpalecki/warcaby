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
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

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

    def clear_capture_fields(self):
        self.capture_fields.clear()


class Man(Piece):

    def can_capture(self, board):
        for x, y in self.directions:
            try:
                enemy_x = self.current_position_x + x
                enemy_y = self.current_position_y + y
                enemy_field = board[enemy_x][enemy_y]
                landing_x = self.current_position_x + x * 2
                landing_y = self.current_position_y + y * 2
                landing_field = board[landing_x][landing_y]
                if enemy_field is not None and enemy_field.color != self.color and landing_field is None:
                    add_to_list(self.capture_fields, landing_x, landing_y)
            except IndexError:
                continue

    def check_possible_moves(self, board):
        moves = []
        directions_for_colors = {
            Color.White: [(-1, -1), (1, -1)],
            Color.Black: [(-1, 1), (1, 1)]
        }
        try:
            self.can_capture(board)
            directions = directions_for_colors[self.color]
            for x, y in directions:
                target_x = self.current_position_x + x
                target_y = self.current_position_y + y
                if board[target_x][target_y] is None:
                    add_to_list(moves, target_x, target_y)
            self.can_capture(board)
        except IndexError:
            pass
        return moves + self.capture_fields


class King(Piece):

    def check_possible_moves(self, board):
        moves = []
        for x, y in self.directions:
            for i in range(1, 8):
                try:
                    target_x = self.current_position_x + x * i
                    target_y = self.current_position_y + y * i
                    target_field = board[target_x][target_y]
                    if target_field is None:
                        add_to_list(moves, target_x, target_y)
                    else:
                        if target_field.color == self.color:
                            break
                        if board[target_x + x][target_y + y] is None:
                            add_to_list(self.capture_fields, target_x + x, target_y + y)
                        break
                except IndexError:
                    break
        return moves + self.capture_fields
