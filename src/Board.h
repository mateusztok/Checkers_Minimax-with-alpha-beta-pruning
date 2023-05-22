class Piece :
    def __init__(self, color, is_king = False) :
    self.color = color
    self.is_king = is_king

    def make_king(self) :
    self.is_king = True

class Board :
    def __init__(self) :
        self.board = [[None]* 8 for _ in range(8)]

    def initialize_pieces(self) :
        # Inicjalizacja pionków na planszy
        # Przyk³ad dla dwóch graczy
        for row in range(3) :
            for col in range(8) :
                if (row + col) % 2 == 0 :
                    self.board[row][col] = Piece('black')

        for row in range(5, 8) :
            for col in range(8) :
                if (row + col) % 2 == 0 :
                    self.board[row][col] = Piece('white')

def is_valid_move(self, start_row, start_col, end_row, end_col) :
    # Sprawdzanie poprawnoœci ruchu
    if (
        start_row < 0 or start_row >= 8 or
        start_col < 0 or start_col >= 8 or
        end_row < 0 or end_row >= 8 or
        end_col < 0 or end_col >= 8 or
        self.board[start_row][start_col] is None or
        self.board[end_row][end_col] is not None
       ) :
        return False

    piece = self.board[start_row][start_col]
        if not piece.is_king :
            if piece.color == 'black' and end_row <= start_row :
                return False
            if piece.color == 'white' and end_row >= start_row :
                return False

        if abs(start_row - end_row) != 1 or abs(start_col - end_col) != 1 :
            return False

        return True

    def make_move(self, start_row, start_col, end_row, end_col) :
        # Wykonanie ruchu na planszy
        if self.is_valid_move(start_row, start_col, end_row, end_col) :
            piece = self.board[start_row][start_col]
            self.board[start_row][start_col] = None
            self.board[end_row][end_col] = piece

    def print_board(self) :
        # Wyœwietlanie planszy
        for row in range(8) :
            for col in range(8) :
                piece = self.board[row][col]
                if piece is None :
                    print('-', end = ' ')
                else :
                    symbol = 'K' if piece.is_king else 'O'
                    print(symbol, end = ' ')
                print()
