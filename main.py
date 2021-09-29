import pygame
from Pieces import *

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILESIZE = 70


def is_piece_field(x, y):
    if x % 2 == 0:
        return y % 2 != 0
    else:
        return y % 2 == 0


def is_end(board):
    white = black = False
    for x in range(8):
        for y in range(8):
            if board[x][y] is not None:
                if board[x][y].color == Color.White:
                    white = True
                else:
                    black = True

    if not white:
        print("Black wins")
    elif not black:
        print("White wins")


def place_pieces(board):
    for x in range(8):
        for y in range(3):
            if is_piece_field(x, y):
                board[x][y] = Man(Color.Black, x, y, board)
        for y in range(5, 8):
            if is_piece_field(x, y):
                board[x][y] = Man(Color.White, x, y, board)


def create_board_surf():
    board_surf = pygame.Surface((TILESIZE * 8, TILESIZE * 8))
    is_gray = False
    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(board_surf, pygame.Color('gray' if is_gray else 'white'), rect)
            is_gray = not is_gray
        is_gray = not is_gray
    return board_surf


def create_board():
    return [[None for _ in range(8)] for _ in range(8)]


def check_promotion(board):
    for i in range(1, 8, 2):
        if board[i][0] is not None and board[i][0].color == Color.White and type(board[i][0]) == Man:
            return board[i][0]
    for i in range(0, 8, 2):
        if board[i][7] is not None and board[i][7].color == Color.Black and type(board[i][7]) == Man:
            return board[i][7]


def promote(board):
    piece = check_promotion(board)
    if piece is not None:
        pos_x = piece.current_position_x
        pos_y = piece.current_position_y
        board[pos_x][pos_y] = King(piece.color, pos_x, pos_y, board)


def draw_pieces(board_surf, board):
    img_dict = {
        Man: {
            Color.White: pygame.image.load("figury/white pawn.png"),
            Color.Black: pygame.image.load("figury/black pawn.png")
        },
        King: {
            Color.White: pygame.image.load("figury/white queen.png"),
            Color.Black: pygame.image.load("figury/black queen.png")
        }
    }
    for i in range(8):
        for j in range(8):
            field = board[i][j]
            if field is not None:
                board_surf.blit(img_dict[type(field)][field.color], (i * TILESIZE, j * TILESIZE))


def is_click_on_board(x, y):
    return 360 <= x <= 920 and 80 <= y <= 640


def take_piece(board, current_turn):
    pos = pygame.mouse.get_pos()
    x = (pos[0] - 360) // TILESIZE
    y = (pos[1] - 80) // TILESIZE
    if is_click_on_board(pos[0], pos[1]) and board[x][y] is not None and current_turn == board[x][y].color:
        return board[x][y]


def move_piece(board, held_piece, possible_moves, current_turn, double_capture):
    pos = pygame.mouse.get_pos()
    x = (pos[0] - 360) // TILESIZE
    y = (pos[1] - 80) // TILESIZE
    if not is_click_on_board(pos[0], pos[1]) or double_capture and [x, y] not in held_piece.capture_fields:
        return None, current_turn, double_capture
    if board[x][y] is not None:
        return board[x][y], current_turn, double_capture
    if not held_piece.capture_fields and [x, y] in possible_moves:
        held_piece.move(x, y, board)
        current_turn = -current_turn
    elif [x, y] in held_piece.capture_fields:
        held_piece.move(x, y, board)
        held_piece.clear_capture_fields()
        held_piece.check_possible_moves(board)
        if held_piece.capture_fields:
            double_capture = True
            return None, current_turn, double_capture
        else:
            current_turn = -current_turn
            double_capture = False
    return board[x][y], current_turn, double_capture


def main():
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    board = create_board()
    place_pieces(board)
    current_turn = Color.White
    double_capture = False
    held_piece = None
    clock = pygame.time.Clock()
    possible_moves = []
    while True:
        board_surf = create_board_surf()
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.QUIT:
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and held_piece is None:
                    held_piece = take_piece(board, current_turn)
                    if held_piece is not None:
                        possible_moves = held_piece.check_possible_moves(board)
                elif pygame.mouse.get_pressed()[0]:
                    piece, current_turn, double_capture = move_piece(board, held_piece, possible_moves, current_turn,
                                                                     double_capture)
                    if double_capture:
                        continue
                    if piece is not None and piece != held_piece and piece.color == held_piece.color:
                        held_piece = piece
                        held_piece.clear_capture_fields()
                        possible_moves = held_piece.check_possible_moves(board)
                        continue
                    held_piece.clear_capture_fields()
                    held_piece = None
                    is_end(board)

        win.fill((254, 172, 0))
        pygame.draw.rect(win, (189, 111, 12), (0, 640, 1280, 80))
        pygame.draw.rect(win, (189, 111, 12), (0, 0, 1280, 80))
        if not double_capture:
            promote(board)
        if held_piece is not None:
            pygame.draw.rect(board_surf, (0, 255, 0), (
                held_piece.current_position_x * TILESIZE, held_piece.current_position_y * TILESIZE, TILESIZE, TILESIZE))
        else:
            possible_moves.clear()
        if held_piece is not None and held_piece.capture_fields:
            for x, y in held_piece.capture_fields:
                pygame.draw.circle(board_surf, 'brown', [x * TILESIZE + TILESIZE / 2, y * TILESIZE + TILESIZE / 2], 10)
        else:
            for x, y in possible_moves:
                pygame.draw.circle(board_surf, 'brown', [x * TILESIZE + TILESIZE / 2, y * TILESIZE + TILESIZE / 2], 10)
        draw_pieces(board_surf, board)
        win.blit(board_surf, (360, 80))
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
