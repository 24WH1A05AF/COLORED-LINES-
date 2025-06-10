import tkinter as tk
from tkinter import messagebox
import random
from collections import deque

GRID = 9
BALLS = 3
LINE = 5
COLORS = ["red", "blue", "green", "yellow", "purple", "orange", "cyan"]

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Bubble Breaker")

        self.canvas = tk.Canvas(root, width=540, height=540, bg="white")
        self.canvas.pack()

        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 14))
        self.score_label.pack()

        self.rules_button = tk.Button(root, text="Show Rules", command=self.show_rules)
        self.rules_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit Game", command=self.exit_game)
        self.exit_button.pack(pady=5)

        self.size = 60
        self.board = [[None for _ in range(GRID)] for _ in range(GRID)]
        self.selected = None
        self.score = 0

        self.canvas.bind("<Button-1>", self.handle_click)

        self.draw_board()
        self.add_random_balls(BALLS)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(GRID):
            for col in range(GRID):
                x1 = col * self.size
                y1 = row * self.size
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

                color = self.board[row][col]
                if color:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill=color)

        if self.selected:
            r, c = self.selected
            x1 = c * self.size
            y1 = r * self.size
            x2 = x1 + self.size
            y2 = y1 + self.size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="gold", width=3)

    def handle_click(self, event):
        row = event.y // self.size
        col = event.x // self.size

        if row >= GRID or col >= GRID:
            return

        if self.board[row][col]:
            self.selected = (row, col)
        elif self.selected:
            if self.valid_move(self.selected, (row, col)):
                self.move(self.selected, (row, col))
                if not self.check_lines():
                    self.add_random_balls(BALLS)
                    self.check_lines()
                self.selected = None

        self.draw_board()

        if self.is_full():
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            self.canvas.create_text(width // 2, height // 2, text="Game Over", font=("Arial", 30), fill="black")

    def move(self, start, end):
        sr, sc = start
        er, ec = end
        self.board[er][ec] = self.board[sr][sc]
        self.board[sr][sc] = None

    def add_random_balls(self, count):
        empty_cells = [(r, c) for r in range(GRID) for c in range(GRID) if self.board[r][c] is None]
        for _ in range(min(count, len(empty_cells))):
            r, c = random.choice(empty_cells)
            empty_cells.remove((r, c))
            self.board[r][c] = random.choice(COLORS)

    def valid_move(self, start, end):
        sr, sc = start
        er, ec = end
        visited = [[False]*GRID for _ in range(GRID)]
        queue = deque([start])
        visited[sr][sc] = True

        while queue:
            r, c = queue.popleft()
            if (r, c) == end:
                return True
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID and 0 <= nc < GRID and not visited[nr][nc]:
                    if self.board[nr][nc] is None:
                        visited[nr][nc] = True
                        queue.append((nr, nc))
        return False

    def check_lines(self):
        found = set()
        directions = [(1,0), (0,1), (1,1), (1,-1)]

        for r in range(GRID):
            for c in range(GRID):
                color = self.board[r][c]
                if not color:
                    continue
                for dr, dc in directions:
                    line = []
                    nr, nc = r, c
                    while 0 <= nr < GRID and 0 <= nc < GRID and self.board[nr][nc] == color:
                        line.append((nr, nc))
                        nr += dr
                        nc += dc
                    if len(line) >= LINE:
                        found.update(line)

        for r, c in found:
            self.board[r][c] = None

        if found:
            self.score += len(found) * 2
            self.score_label.config(text=f"Score: {self.score}")
        return bool(found)

    def is_full(self):
        return all(self.board[r][c] for r in range(GRID) for c in range(GRID))

    def show_rules(self):
        rules = (
            "GAME RULES\n\n"
            "• Move the balls from cell to cell to group them into lines of the same color.\n"
            "• After each move, the computer adds three more balls to the board.\n"
            "• To avoid filling up the board, gather balls into lines of 5 or more.\n"
            "• When a complete line is formed, the balls are removed and your score increases.\n"
            "• If a line is removed, new balls are not added—giving you another move instead.\n"
            "• Scoring: Each removed ball gives 2 points, with bonuses for removing more at once.\n"
            "• The game ends when the board is completely filled with balls.\n"
            "• Goal: Stay in the game as long as possible and beat your high score!"
        )

        popup = tk.Toplevel(self.root)
        popup.title("Game Rules")
        popup.geometry("500x300")
        popup.resizable(False, False)

        text = tk.Text(popup, wrap="word", font=("Arial", 10))
        text.insert("1.0", rules)
        text.config(state="disabled")
        text.pack(expand=True, fill="both", padx=10, pady=10)

        ok_button = tk.Button(popup, text="Close", command=popup.destroy)
        ok_button.pack(pady=5)

    def exit_game(self):
        result = messagebox.askyesno("Exit Game", "Are you sure you want to exit?")
        if result:
            messagebox.showinfo("Final Score", f"Your final score is: {self.score}")
            self.root.destroy()


# Run the game
root = tk.Tk()
game = Game(root)
root.iconbitmap("C:/Users/A Shaveta/Downloads/bubble-breaker-free-screenshot.ico")
root.mainloop()
