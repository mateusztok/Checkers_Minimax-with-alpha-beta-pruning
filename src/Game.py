from Interface import Interface
from Player import Player
from PlayerAI import PlayerAI
from Piece import Piece
import time

class Game:
    def __init__(self, root, level, first):
        self.level = level
        self.players = [PlayerAI("red"), Player("blue")]  # Przykładowa lista graczy
        self.board = [[None] * 8 for _ in range(8)]  # Początkowa macierz planszy
        self.root = root
        self.redscore = 0
        self.bluescore = 0

        if first == "First":
            self.current_player = self.players[1]
            self.next_player = self.players[0]
        else:
            self.current_player = self.players[0]
            self.next_player = self.players[1]

        self.game_window = Interface(self.root, self.current_player)
        self.initialize_pieces()
        self.root.bind("<Button-1>", self.check_click)
        self.click = [None, None]
        self.winner = None

        if self.current_player == self.players[0]:
            self.make_player_move()
        self.root.mainloop()

    def make_player_move(self):
        self.current_player.make_move(self.board, self.level, self.next_player.color)
        self.game_window.update_board(self.board, self.next_player)
        self.evaluate(self.board)
        print("Red", self.redscore, "\nBlue", self.bluescore)
        self.switch_players()

    def initialize_pieces(self):
        # Ustalanie początkowego układu pionków
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    if row < 3:
                        self.board[row][col] = Piece("red")
                    elif row > 4:
                        self.board[row][col] = Piece("blue")

    def check_click(self, event):
        if self.current_player == self.players[0]:
            return
        x = event.x
        y = event.y
        col = x // 50
        row = y // 50

        if self.click[0] is None:
            # Pierwsze kliknięcie
            if self.board[row][col] is not None and self.board[row][col].color == self.current_player.color:
                self.click[0] = row
                self.click[1] = col
                print("Wybrano pionek: ", row, col)
            else:
                print("Nieprawidłowy wybór pionka.")

        else:
            # Drugie kliknięcie
            direction_row = row
            direction_col = col
            print("Miejsce docelowe: ", direction_row, direction_col)
            if self.current_player.make_move(self.board, self.click, direction_row, direction_col):
                self.click = [None, None]
                self.game_window.update_board(self.board, self.next_player)
                self.evaluate(self.board)

                if self.is_game_over():
                    time.sleep(2)
                    self.end_game()
                    return
                else:
                    self.switch_players()
                    if self.current_player == self.players[0]:
                        if self.current_player.make_move(self.board, self.level, self.current_player.color):
                            self.game_window.update_board(self.board, self.next_player)
                            if self.is_game_over():
                                time.sleep(2)
                                self.end_game()
                                return
                            self.evaluate(self.board)
                            self.switch_players()
            else:
                print("Nieprawidłowy ruch.")
                self.click = [None, None]

    def is_game_over(self):
        if self.count_pieces(self.players[0]) == 0:
            self.winner = "niebieski"
            return True
        if self.count_pieces(self.players[1]) == 0:
            self.winner = "czerwony"
            return True
        if not self.can_any_player_move():
            return True

        return False

    def end_game(self):
        print("Koniec gry.\nWygrywa: ")
        self.root.unbind("<Button-1>")
        self.game_window.write_end(self.winner)
        from Menu import Menu
        menu = Menu(self.root)

    def can_any_player_move(self):
        if self.current_player == self.players[0]:
            if self.can_player_move(self.players[1]):
                return True
            else:
                self.winner = "czerwony"
                return False

        else:
            if self.can_player_move(self.players[0]):
                return True
            else:
                self.winner = "niebieski"
                return False

    def switch_players(self):
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
            self.next_player = self.players[0]

        else:
            self.current_player = self.players[0]
            self.next_player = self.players[1]

    def can_player_move(self, player):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is not None and piece.color == player.color:
                    possible_moves = self.get_possible_moves(row, col)
                    if len(possible_moves) > 0:
                        return True
        return False

    def get_possible_moves(self, row, col):
        piece = self.board[row][col]
        possible_moves = []
        if piece.is_king:
            for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for i in range(1, 8):
                    new_row = row + direction[0] * i
                    new_col = col + direction[1] * i
                    if not self.is_valid_position(new_row, new_col):
                        break
                    if self.board[new_row][new_col] is None:
                        possible_moves.append((new_row, new_col))
                    else:
                        jump_row = new_row + direction[0]
                        jump_col = new_col + direction[1]

                        if self.is_valid_position(jump_row, jump_col) and self.board[jump_row][jump_col] is None:
                            possible_moves.append((jump_row, jump_col))
                        break

        else:
            if piece.color == "red":
                if row < 7:
                    if col > 0 and self.board[row + 1][col - 1] is None:
                        possible_moves.append((row + 1, col - 1))
                    if col < 7 and self.board[row + 1][col + 1] is None:
                        possible_moves.append((row + 1, col + 1))

                if row < 6:
                    if col > 1 and self.board[row + 1][col - 1] is not None and self.board[row + 1][col - 1].color == "blue" and self.board[row + 2][col - 2] is None:
                        possible_moves.append((row + 2, col - 2))
                    if col < 6 and self.board[row + 1][col + 1] is not None and self.board[row + 1][col + 1].color == "blue" and self.board[row + 2][col + 2] is None:
                        possible_moves.append((row + 2, col + 2))

            elif piece.color == "blue":
                if row > 0:
                    if col > 0 and self.board[row - 1][col - 1] is None:
                        possible_moves.append((row - 1, col - 1))
                    if col < 7 and self.board[row - 1][col + 1] is None:
                        possible_moves.append((row - 1, col + 1))

                if row > 1:
                    if col > 1 and self.board[row - 1][col - 1] is not None and self.board[row - 1][col - 1].color == "red" and self.board[row - 2][col - 2] is None:
                        possible_moves.append((row - 2, col - 2))
                    if col < 6 and self.board[row - 1][col + 1] is not None and self.board[row - 1][col + 1].color == "red" and self.board[row - 2][col + 2] is None:
                        possible_moves.append((row - 2, col + 2))

        return possible_moves

    def is_valid_position(self, row, col):
        return row >= 0 and row < 8 and col >= 0 and col < 8

    def count_pieces(self, player):
        count = 0
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is not None and piece.color == player.color:
                    count += 1
        return count

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

                        red_score += self.calculate_mobility_and_capture_ability(board, row, col)

                    elif piece.color == "blue":
                        if piece.is_king:
                            blue_score += 1.5
                        else:
                            blue_score += 1

                        if self.is_in_center(row, col):
                            blue_score += 0.5

                        blue_score += self.calculate_mobility_and_capture_ability(board, row, col)
        print("Czerwony: %.1f" % red_score)
        print("Niebieski: %.1f" % blue_score)


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


