class Player:
    def __init__(self, color):
        self.color = color

    def make_move(self, board, click, target_row, target_col):
        start_row, start_col = click[0], click[1]

        if not self.is_within_board(target_row, target_col):
            print("Nieprawidłowy ruch.")
            return False

        if board[target_row][target_col] is not None:
            print("Nieprawidłowy ruch. Pole jest zajęte.")
            return False

        if board[start_row][start_col].is_king:
            direction_row = target_row - start_row
            direction_col = target_col - start_col
            if abs(direction_row) == abs(direction_col):
                step_row = 1 if direction_row > 0 else -1
                step_col = 1 if direction_col > 0 else -1
                current_row = start_row + step_row
                current_col = start_col + step_col
                while current_row != target_row and current_col != target_col:
                    if board[current_row][current_col] is not None:
                        if board[current_row][current_col].color != self.color:
                            captured_row = current_row + step_row
                            captured_col = current_col + step_col
                            if board[captured_row][captured_col] is None and captured_row == target_row and captured_col == target_col:
                                board[current_row][current_col] = None
                            else:
                                return False
                        else:
                            return False

                    current_row += step_row
                    current_col += step_col

                board[target_row][target_col] = board[start_row][start_col]
                board[start_row][start_col] = None
                return True

            else:
                return False

        else:
            if abs(target_row-start_row) != 1 or abs(target_col-start_col) != 1:
                if abs(target_row - start_row) == 2 and abs(target_col - start_col) == 2:
                    captured_row = (start_row + target_row) // 2
                    captured_col = (start_col + target_col) // 2

                    if board[captured_row][captured_col] is None or board[captured_row][captured_col].color == self.color:
                        print("Nieprawidłowy ruch.")
                        return False

                    board[captured_row][captured_col] = None
                else:
                    print("Nieprawidłowy ruch.")
                    return False
            else:
                if board[start_row][start_col].color == "blue":
                    if target_row != start_row - 1:
                        print("Nieprawidłowy ruch.")
                        return False
                else:
                    if target_row != start_row + 1:
                        print("Nieprawidłowy ruch.")
                        return False

        board[target_row][target_col] = board[start_row][start_col]
        board[start_row][start_col] = None

        if self.color == "blue" and target_row == 0:
            board[target_row][target_col].is_king = True
        elif self.color == "red" and target_row == 7:
            board[target_row][target_col].is_king = True

        return True

    def is_within_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
