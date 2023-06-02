import tkinter as tk
from Game import Game
class Menu:
    def __init__(self, root):
        self.level = None
        self.root = root
        self.root.title("Warcaby")
        self.root.geometry("400x450")

        self.label_description = tk.Label(self.root, text="Wybierz poziom gry", font=("Arial", 20))
        self.button_easy = tk.Button(self.root, text="Łatwy", font=("Arial", 10), command=lambda: self.set_level(1), width=13, height=4)
        self.button_medium = tk.Button(self.root, text="Średni", font=("Arial", 10), command=lambda: self.set_level(3), width=13, height=4)
        self.button_hard = tk.Button(self.root, text="Trudny", font=("Arial", 10), command=lambda: self.set_level(5), width=13, height=4)
        self.quit_button = tk.Button(self.root, text="Zakończ", font=("Arial", 10), command=self.root.destroy, width=8, height=4)
        self.choose_blue = None
        self.choose_red = None
        self.label_description.grid(row=0, column=0, columnspan=3, pady=10)
        self.button_easy.grid(row=1, column=0, padx=10, pady=10)
        self.button_medium.grid(row=1, column=1, padx=10, pady=10)
        self.button_hard.grid(row=1, column=2, padx=10, pady=10)
        self.quit_button.grid(row=2, column=1, pady=10)

        self.root.mainloop()

    def set_level(self, level):
        self.level = level
        for child in self.root.winfo_children():
            child.destroy()

        self.label_description = tk.Label(self.root, text="Chcesz zaczynać?", font=("Arial", 20))
        self.choose_blue = tk.Button(self.root, text="Tak", font=("Arial", 10), command=lambda: self.start_game("First"), width=13, height=4)
        self.choose_red = tk.Button(self.root, text="Nie", font=("Arial", 10), command=lambda: self.start_game("Second"), width=13, height=4)
        self.label_description.grid(row=0, column=0, columnspan=3, pady=10)
        self.choose_blue.grid(row=1, column=0, padx=10, pady=10)
        self.choose_red.grid(row=1, column=2, padx=10, pady=10)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def start_game(self, first):
        for child in self.root.winfo_children():
            child.destroy()
        Game(self.root, self.level, first)

if __name__ == "__main__":
    root = tk.Tk()
    main_menu = Menu(root)
