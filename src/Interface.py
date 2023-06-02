import time
import tkinter as tk

class Interface:
    def __init__(self, master, current_player):
        self.master = master
        self.master.title("Warcaby")
        self.canvas = tk.Canvas(self.master, width=400, height=450)
        self.canvas.pack()
        self.draw_board()
        self.current_player_label = self.canvas.create_text(200, 425, text="Ruch gracza: " + current_player.color, fill="black", font=("Arial", 14))
        self.current_player = None

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = "white"
                else:
                    color = "black"
                self.canvas.create_rectangle(i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, fill=color, tags="board")

        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 0:
                    self.draw_piece(row, col, "red")

        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    self.draw_piece(row, col, "blue")
        self.canvas.update()

    def draw_piece(self, row, col, color):
        x = col * 50 + 25
        y = row * 50 + 25
        radius = 20
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, tags="piece")

    def draw_king(self, row, col, color):
        x = col * 50 + 25
        y = row * 50 + 25
        radius = 20
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, tags="piece")
        self.canvas.create_text(x, y, text="K", fill="black", font=("Arial", 14), tags="piece")

    def write_end(self, winner):
        self.canvas.delete("piece")
        self.canvas.delete("board")
        self.canvas.create_text(200, 200, text="Koniec gry\nWygrywa: " + winner, fill="black", font=("Arial", 20))
        self.canvas.update()
        time.sleep(2)
        self.canvas.destroy()

    def update_board(self, board, current_player):
        self.canvas.delete("piece")

        for row in range(8):
            for col in range(8):
                if board[row][col] is not None:
                    color = board[row][col].color
                    if board[row][col].is_king:
                        self.draw_king(row, col, color)
                    else:
                        self.draw_piece(row, col, color)

        self.canvas.delete(self.current_player_label)
        self.current_player = current_player
        self.current_player_label = self.canvas.create_text(200, 425, text="Ruch gracza: " + current_player.color, fill="black", font=("Arial", 14))
        self.canvas.update()
        return True


