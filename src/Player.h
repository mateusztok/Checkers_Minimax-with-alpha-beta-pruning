class Player :
    def __init__(self, name, color) :
         self.name = name
         self.color = color

    def make_move(self, board) :
        # Implementacja podejmowania decyzji dotycz¹cych ruchu
        valid_moves = self.get_valid_moves(board)

        if len(valid_moves) == 0:
            print("Brak mo¿liwych ruchów. Koniec gry!")
            return

        print("Dostêpne ruchy:")
        for move in valid_moves :
            print(f"{move[0]} -> {move[1]}")

        while True :
            move_str = input("Wybierz ruch (start_row,start_col -> end_row,end_col): ")
            move_parts = move_str.split("->")
            if len(move_parts) != 2 :
                print("B³êdny format ruchu. Spróbuj ponownie.")
                continue

            start_pos = move_parts[0].strip().split(",")
            end_pos = move_parts[1].strip().split(",")

            if len(start_pos) != 2 or len(end_pos) != 2:
                print("B³êdny format pozycji. Spróbuj ponownie.")
                continue

            try :
                start_row = int(start_pos[0])
                start_col = int(start_pos[1])
                end_row = int(end_pos[0])
                end_col = int(end_pos[1])
            except ValueError :
print("Niepoprawne wartoœci pozycji. Spróbuj ponownie.")
continue

if (start_row, start_col, end_row, end_col) not in valid_moves :
print("Nieprawid³owy ruch. Spróbuj ponownie.")
continue

board.make_move(start_row, start_col, end_row, end_col)
break

def get_valid_moves(self, board) :
    valid_moves = []
    for row in range(8) :
        for col in range(8) :
            piece = board.board[row][col]
            if piece is not None and piece.color == self.color :
                if piece.is_king :
                    self.get_valid_king_moves(row, col, board, valid_moves)
                else :
                    self.get_valid_regular_moves(row, col, board, valid_moves)
                    return valid_moves

                    def get_valid_king_moves(self, row, col, board, valid_moves) :
                    # Logika sprawdzania mo¿liwych ruchów dla damki(pionka, który sta³ siê królem)

                    def get_valid_regular_moves(self, row, col, board, valid_moves) :
                    # Logika sprawdzania mo¿liwych ruchów dla zwyk³ego pionka

