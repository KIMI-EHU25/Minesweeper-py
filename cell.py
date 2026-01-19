class Cell:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.is_mine = False
        self.adjacent_mines = 0
        self.revealed = False
        self.flagged = False

    def reveal(self):
        if not self.flagged:
            self.revealed = True

    def toggle_flag(self):
        if not self.revealed:
            self.flagged = not self.flagged