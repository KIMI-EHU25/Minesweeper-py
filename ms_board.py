import random
from cell import Cell


class Board:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines_count = mines

        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.game_over = False
        self.victory = False

        self._place_mines()
        self._compute_adjacencies()

    def _cells_iter(self):
        for r in range(self.rows):
            for c in range(self.cols):
                yield self.grid[r][c]

    def _place_mines(self):
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        random.shuffle(all_positions)
        for r, c in all_positions[: self.mines_count]:
            self.grid[r][c].is_mine = True

    def _neighbors(self, row: int, col: int):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    yield self.grid[nr][nc]

    def _compute_adjacencies(self):
        for cell in self._cells_iter():
            if cell.is_mine:
                cell.adjacent_mines = -1
                continue
            count = 0
            for n in self._neighbors(cell.row, cell.col):
                if n.is_mine:
                    count += 1
            cell.adjacent_mines = count


    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def reveal_cell(self, row: int, col: int):
        """Reveal a cell and flood-fill if it's a zero. Handle game over/win."""
        if not self.in_bounds(row, col):
            return

        cell = self.grid[row][col]
        if cell.revealed or cell.flagged or self.game_over:
            return

        cell.reveal()

        if cell.is_mine:
            self.game_over = True
            self.victory = False
            return

        if cell.adjacent_mines == 0:
            self._flood_fill(row, col)

        if self._check_victory():
            self.game_over = True
            self.victory = True

    def _flood_fill(self, row: int, col: int):
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            cell = self.grid[r][c]

            for neighbor in self._neighbors(r, c):
                if neighbor.revealed or neighbor.flagged:
                    continue
                if neighbor.is_mine:
                    continue
                neighbor.reveal()
                if neighbor.adjacent_mines == 0:
                    stack.append((neighbor.row, neighbor.col))

    def toggle_flag(self, row: int, col: int):
        if not self.in_bounds(row, col) or self.game_over:
            return
        self.grid[row][col].toggle_flag()

    def chord(self, row: int, col: int):
        """
        Windows-style 'chord':
        If you're on a revealed number cell and the number of
        flagged neighbors equals that number, reveal all other
        neighbors. If any of those are mines -> you die.
        """
        if not self.in_bounds(row, col) or self.game_over:
            return

        cell = self.grid[row][col]
        if not cell.revealed or cell.adjacent_mines <= 0:
            return

        flagged_count = sum(1 for n in self._neighbors(row, col) if n.flagged)

        if flagged_count != cell.adjacent_mines:
            return

        for n in self._neighbors(row, col):
            if n.flagged or n.revealed:
                continue
            if n.is_mine:
                n.revealed = True
                self.game_over = True
                self.victory = False
            else:
                self.reveal_cell(n.row, n.col)

    def _check_victory(self) -> bool:
        for cell in self._cells_iter():
            if not cell.is_mine and not cell.revealed:
                return False
        return True
