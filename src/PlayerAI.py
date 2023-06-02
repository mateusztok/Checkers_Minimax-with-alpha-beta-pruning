from math import inf
import copy
import time
class PlayerAI:
    def __init__(self, color):
        self.color = color
        self.redscore = 0
        self.bluescore = 0

    def make_move(self, board, level, color):
        # = time.time()
        value, best_move = self.minimax(board, self.color, color, -inf, inf, level)
        #end_time = time.time()
        #execution_time = end_time - start_time
        #print("Czas wykonania:", execution_time, "sekundy")

        click_row, click_col, direction_row, direction_col = best_move
        self.move_piece(board, click_row, click_col, direction_row, direction_col)
        return True

    def minimax(self, board, current_color, maximizing_color, alpha, beta, depth):
        if depth == 0 or self.is_game_over(board, current_color):
            if self.is_game_over(board, current_color):
                if current_color == maximizing_color:
                    return -inf, None
                else:
                    return inf, None
            else:
                return self.evaluate(board), None

        possible_moves = self.get_all_moves(board, current_color)
        if current_color == maximizing_color:
            best_value = -inf
            best_move = None
            for move in possible_moves:
                click_row, click_col, target_row, target_col = move
                new_board = self.simulate_move(board, click_row, click_col, target_row, target_col)
                value, _ = self.minimax(new_board, self.opposite_color(current_color), maximizing_color, alpha, beta, depth - 1)
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break  # Cięcie
            return best_value, best_move
        else:
            best_value = inf
            best_move = None
            for move in possible_moves:
                click_row, click_col, target_row, target_col = move
                new_board = self.simulate_move(board, click_row, click_col, target_row, target_col)
                value, _ = self.minimax(new_board, self.opposite_color(current_color), maximizing_color, alpha, beta, depth - 1)
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)
                if alpha >= beta:
                    break  # Cięcie
            return best_value, best_move

    def evaluate(self, board):

        red_score = 0
        blue_score = 0

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None:
                    if piece.color == "red":
                        if piece.is_king:
                            red_score += 1.5
                        else:
                            red_score += 1

                        if self.is_in_center(row, col):
                            red_score += 0.5

                        red_score += self. calculate_mobility_and_capture_ability(board, row, col)

                    elif piece.color == "blue":
                        if piece.is_king:
                            blue_score += 1.5
                        else:
                            blue_score += 1

                        if self.is_in_center(row, col):
                            blue_score += 0.5

                        blue_score += self. calculate_mobility_and_capture_ability(board, row, col)
        self.redscore = red_score
        self.bluescore = blue_score
        return red_score - blue_score

    def calculate_mobility_and_capture_ability(self, board, row, col):
        piece = board[row][col]
        mobility = 0
        capture_ability = 0

        if piece is None:
            return mobility, capture_ability

        if piece.is_king:
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for direction in directions:
                for i in range(1, 8):
                    new_row = row + direction[0] * i
                    new_col = col + direction[1] * i

                    if not self.is_valid_position(new_row, new_col):
                        break

                    if board[new_row][new_col] is None:
                        mobility += 0.2
                    else:
                        jump_row = new_row + direction[0]
                        jump_col = new_col + direction[1]

                        if self.is_valid_position(jump_row, jump_col) and board[jump_row][jump_col] is None:
                            capture_ability += 0.8

        else:
            if piece.color == "red":
                if row < 7:
                    if col > 0 and board[row + 1][col - 1] is None:
                        mobility += 0.2
                    if col < 7 and board[row + 1][col + 1] is None:
                        mobility += 0.2

                if row < 6:
                    if col > 1 and board[row + 1][col - 1] is not None and board[row + 1][col - 1].color == "blue" and board[row + 2][col - 2] is None:
                        capture_ability += 0.8
                    if col < 6 and board[row + 1][col + 1] is not None and board[row + 1][col + 1].color == "blue" and board[row + 2][col + 2] is None:
                        capture_ability += 0.8
                if row > 1:
                    if col > 1 and board[row - 1][col - 1] is not None and board[row - 1][col - 1].color == "blue" and board[row - 2][col - 2] is None:
                        capture_ability += 0.8
                    if col < 6 and board[row - 1][col + 1] is not None and board[row - 1][col + 1].color == "blue" and board[row - 2][col + 2] is None:
                        capture_ability += 0.8

            elif piece.color == "blue":
                if row > 0:
                    if col > 0 and board[row - 1][col - 1] is None:
                        mobility += 0.2
                    if col < 7 and board[row - 1][col + 1] is None:
                        mobility += 0.2

                if row > 1:
                    if col > 1 and board[row - 1][col - 1] is not None and board[row - 1][col - 1].color == "red" and board[row - 2][col - 2] is None:
                        capture_ability += 0.8
                    if col < 6 and board[row - 1][col + 1] is not None and board[row - 1][col + 1].color == "red" and board[row - 2][col + 2] is None:
                        capture_ability += 0.8
                if row < 6:
                    if col > 1 and board[row - 1][col - 1] is not None and board[row - 1][col - 1].color == "blue" and board[row - 2][col - 2] is None:
                        capture_ability += 0.8
                    if col < 6 and board[row - 1][col + 1] is not None and board[row - 1][col + 1].color == "blue" and board[row - 2][col + 2] is None:
                        capture_ability += 0.8

        return mobility + capture_ability

    def is_in_center(self, row, col):
        center_rows = [3, 4]
        center_cols = [3, 4]
        return row in center_rows and col in center_cols

    def is_game_over(self, board, current_color):
        if self.count_pieces("red", board) == 0 or self.count_pieces("blue", board) == 0:
            return True
        if not self.can_any_player_move(current_color, board):
            return True
        return False

    def count_pieces(self, color, board):
        count = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None and piece.color == color:
                    count += 1
        return count

    def get_all_moves(self, board, color):
        moves = []

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None and piece.color == color:
                    moves.extend(self.get_valid_moves(board, row, col, color))

        return moves

    def get_valid_moves(self, board, row, col, color):
        piece = board[row][col]
        valid_moves = []

        if piece.is_king:
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for direction in directions:
                for i in range(1, 8):
                    new_row = row + direction[0] * i
                    new_col = col + direction[1] * i

                    if not self.is_valid_position(new_row, new_col):
                        break

                    if board[new_row][new_col] is not None:
                        if not board[new_row][new_col].color == color:
                            jump_row = new_row + direction[0]
                            jump_col = new_col + direction[1]

                            if self.is_valid_position(jump_row, jump_col) and board[jump_row][jump_col] is None:
                                valid_moves.append((row, col, jump_row, jump_col))

                        break
                    else:
                        valid_moves.append((row, col, new_row, new_col))
        else:
            if piece.color == "red":
                if col > 0 and board[row + 1][col - 1] is None:
                    valid_moves.append((row, col, row + 1, col - 1))
                else:
                    if row < 6 and col > 1 and board[row + 1][col - 1].color == "blue" and board[row + 2][col - 2] is None:
                        valid_moves.append((row, col, row + 2, col - 2))

                if col < 7 and board[row + 1][col + 1] is None:
                    valid_moves.append((row, col, row + 1, col + 1))
                else:
                    if row < 6 and col < 6 and board[row + 1][col + 1].color == "blue" and board[row + 2][col + 2] is None:
                        valid_moves.append((row, col, row + 2, col + 2))
                if col > 1 and row > 1 and board[row - 1][col - 1] is not None and board[row - 1][col - 1].color == "blue" and board[row - 2][col - 2] is None:
                    valid_moves.append((row, col, row - 2, col - 2))
                if col < 6 and row > 1 and board[row - 1][col + 1] is not None and board[row - 1][col + 1].color == "blue" and board[row - 2][col + 2] is None:
                    valid_moves.append((row, col, row - 2, col + 2))

            elif piece.color == "blue":
                if col > 0 and board[row - 1][col - 1] is None:
                    valid_moves.append((row, col, row - 1, col - 1))
                else:
                    if row > 1 and col > 1 and board[row - 1][col - 1].color == "red" and board[row - 2][col - 2] is None:
                        valid_moves.append((row, col, row - 2, col - 2))
                if col < 7 and board[row - 1][col + 1] is None:
                    valid_moves.append((row, col, row - 1, col + 1))
                else:
                    if row > 1 and col < 6 and board[row - 1][col + 1].color == "red" and board[row - 2][col + 2] is None:
                        valid_moves.append((row, col, row - 2, col + 2))
                if col > 1 and row < 6 and board[row + 1][col - 1] is not None and board[row + 1][col - 1].color == "red" and board[row + 2][col - 2] is None:
                    valid_moves.append((row, col, row + 2, col - 2))
                if col < 6 and row < 6 and board[row + 1][col + 1] is not None and board[row + 1][col + 1].color == "red" and board[row + 2][col + 2] is None:
                    valid_moves.append((row, col, row + 2, col + 2))

        return valid_moves

    def is_valid_position(self, row, col):
        return row >= 0 and row < 8 and col >= 0 and col < 8

    def simulate_move(self, board, click_row, click_col, target_row, target_col):
        new_board = copy.deepcopy(board)
        piece = new_board[click_row][click_col]
        new_board[click_row][click_col] = None
        new_board[target_row][target_col] = piece

        if piece.is_king:
            row_direction = 1 if target_row > click_row else -1
            col_direction = 1 if target_col > click_col else -1
            current_row = click_row + row_direction
            current_col = click_col + col_direction
            while current_row != target_row and current_col != target_col:
                if board[current_row][current_col] is not None:
                    new_board[current_row][current_col] = None
                current_row += row_direction
                current_col += col_direction
            return new_board

        if abs(target_row-click_row) == 2:
            captured_row = (click_row + target_row) // 2
            captured_col = (click_col + target_col) // 2
            new_board[captured_row][captured_col] = None

        if not piece.is_king:
            if piece.color == "red" and target_row == 7:
                new_board[target_row][target_col].is_king = True
            elif piece.color == "blue" and target_row == 0:
                new_board[target_row][target_col].is_king = True

        return new_board

    def move_piece(self, board, click_row, click_col, target_row, target_col):
        piece = board[click_row][click_col]
        board[click_row][click_col] = None
        board[target_row][target_col] = piece

        if piece.is_king:
            row_direction = 1 if target_row > click_row else -1
            col_direction = 1 if target_col > click_col else -1
            current_row = click_row + row_direction
            current_col = click_col + col_direction
            while current_row != target_row and current_col != target_col:
                if board[current_row][current_col] is not None:
                    board[current_row][current_col] = None
                current_row += row_direction
                current_col += col_direction
            return board

        if abs(target_row - click_row) == 2:
            captured_row = (click_row + target_row) // 2
            captured_col = (click_col + target_col) // 2
            board[captured_row][captured_col] = None

        if not piece.is_king:
            if piece.color == "red" and target_row == 7:
                board[target_row][target_col].is_king = True
            elif piece.color == "blue" and target_row == 0:
                board[target_row][target_col].is_king = True

        return board

    def opposite_color(self, color):
        if color == "red":
            return "blue"
        else:
            return "red"

    def can_any_player_move(self, current_color, board):
        if self.can_player_move(self.opposite_color(current_color), board):
            return True
        else:
            return False

    def can_player_move(self, color, board):
        possible_moves = self.get_all_moves(board, color)
        if possible_moves is []:
            return False
        return True
