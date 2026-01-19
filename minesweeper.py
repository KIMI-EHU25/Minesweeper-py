import pygame
import random
import time
import math

def draw_glass_panel_from_bg(surface, blurred_bg, rect, radius=18, fog_alpha=100):
    """Draw a frosted Apple-like glass panel clipped from blurred background."""
    x, y, w, h = rect

    panel = pygame.Surface((w, h), pygame.SRCALPHA)

    panel.blit(blurred_bg, (0, 0), area=rect)

    frost = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(
        frost,
        (255, 255, 255, fog_alpha),
        (0, 0, w, h),
        border_radius=radius
    )
    panel.blit(frost, (0, 0))

    highlight = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(
        highlight,
        (255, 255, 255, 40),
        (0, 0, w, h//2),
        border_radius=radius
    )
    panel.blit(highlight, (0, 0))


    pygame.draw.rect(
        panel,
        (255, 255, 255, 180),
        (0, 0, w, h),
        width=2,
        border_radius=radius
    )

    surface.blit(panel, (x, y))

BEGINNER = (9, 9, 10)
INTERMEDIATE = (16, 16, 40)
EXPERT = (16, 30, 99)

CELL_SIZE = 28
BORDER = 12
TOP_PANEL = 50
BOTTOM_PANEL = 40
MIN_WINDOW_WIDTH = 420  


BG_TOP = (14, 18, 26)
BG_BOTTOM = (26, 32, 46)

BG_COLOR = BG_TOP
GRID_COLOR = (120, 130, 150)

CELL_DARK = (160, 160, 160)
CELL_LIGHT = (235, 240, 248)

NUMBER_COLORS = {
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 0, 0),
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128),
}

FACE_NEUTRAL = 0
FACE_WIN = 1
FACE_LOSE = 2
FACE_PRESSED = 3


def draw_seaside_background(surface, t: float) -> None:
    """
    Draw an animated seaside background: sky, ocean, sand, and moving waves.
    t = time in seconds (we'll use pygame.time.get_ticks inside draw_board).
    """
    w, h = surface.get_size()

    sky_h = int(h * 0.45)
    sea_h = int(h * 0.25)
    sand_h = h - sky_h - sea_h

    for y in range(sky_h):
        u = y / max(1, sky_h - 1)
        r = int(40 + 20 * u)
        g = int(120 + 60 * u)
        b = int(200 + 40 * u)
        pygame.draw.line(surface, (r, g, b), (0, y), (w, y))

    sea_top = sky_h
    for i in range(sea_h):
        u = i / max(1, sea_h - 1)
        r = int(10 + 20 * u)
        g = int(100 + 60 * u)
        b = int(150 + 80 * u)
        y = sea_top + i
        pygame.draw.line(surface, (r, g, b), (0, y), (w, y))

    sand_top = sky_h + sea_h
    for i in range(sand_h):
        u = i / max(1, sand_h - 1)
        r = int(220 + 10 * u)
        g = int(200 + 10 * u)
        b = int(170 + 5 * u)
        y = sand_top + i
        pygame.draw.line(surface, (r, g, b), (0, y), (w, y))

    shoreline_y = sand_top
    wave_amp = 6
    wave_len = 80
    wave_speed = 1.5

    for band in range(3):
        phase = t * wave_speed + band * 0.7
        pts = []
        for x in range(0, w, 4):
            offset = math.sin(2 * math.pi * (x / wave_len) + phase) * wave_amp
            y = shoreline_y - 4 - band * 4 + offset
            pts.append((x, y))
        if len(pts) > 1:
            pygame.draw.lines(surface, (245, 250, 255), False, pts, 2)


def blur_surface(source: pygame.Surface, scale_factor: float = 0.25) -> pygame.Surface:
    """
    Cheap blur: scale down then scale back up with smoothscale.
    """
    w, h = source.get_size()
    small_w = max(1, int(w * scale_factor))
    small_h = max(1, int(h * scale_factor))
    small = pygame.transform.smoothscale(source, (small_w, small_h))
    blurred = pygame.transform.smoothscale(small, (w, h))
    return blurred


def draw_glass_tile_from_bg(surface: pygame.Surface,
                            blurred_bg: pygame.Surface,
                            rect: pygame.Rect,
                            cell) -> None:
    """
    Improved Apple glass tile renderer:
    - unrevealed: darker, heavier frost, more opaque
    - revealed blank (adj = 0): bright translucent glass
    - revealed number: same but with text
    """
    x, y, w, h = rect
    tile = pygame.Surface((w, h), pygame.SRCALPHA)

    tile.blit(blurred_bg, (0, 0), area=rect)

    if not cell.revealed:
        fog_alpha = 160
        highlight_alpha = 70
        shadow_alpha = 90
        border_alpha = 180
        border_color = (255, 255, 255, border_alpha)

    else:
        if cell.adj == 0:
            fog_alpha = 60
            highlight_alpha = 130
            shadow_alpha = 40
            border_alpha = 220
            border_color = (255, 255, 255, border_alpha)
        else:
            fog_alpha = 80
            highlight_alpha = 120
            shadow_alpha = 60
            border_alpha = 220
            border_color = (255, 255, 255, border_alpha)

    fog = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(fog, (255, 255, 255, fog_alpha), fog.get_rect(), border_radius=8)
    tile.blit(fog, (0, 0))

    highlight_rect = pygame.Rect(0, 0, w, h // 2)
    pygame.draw.rect(tile, (255, 255, 255, highlight_alpha),
                     highlight_rect, border_radius=8)
    shadow_rect = pygame.Rect(0, h // 3, w, h * 2 // 3)
    pygame.draw.rect(tile, (0, 0, 0, shadow_alpha),
                     shadow_rect, border_radius=8)

    pygame.draw.rect(tile, border_color, tile.get_rect(),
                     width=1, border_radius=8)

    surface.blit(tile, (x, y))


def draw_glass_tile_from_bg(surface: pygame.Surface,
                            blurred_bg: pygame.Surface,
                            rect: pygame.Rect,
                            revealed: bool) -> None:
    """
    Misty Apple-glass tile: shows a blurred version of the seaside behind it.
    You can roughly see shapes but not clearly.
    """
    x, y, w, h = rect
    tile = pygame.Surface((w, h), pygame.SRCALPHA)

    tile.blit(blurred_bg, (0, 0), area=rect)

    fog_alpha = 150 if not revealed else 100
    fog = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(fog, (255, 255, 255, fog_alpha),
                     fog.get_rect(), border_radius=8)
    tile.blit(fog, (0, 0))

    highlight_rect = pygame.Rect(0, 0, w, h // 2)
    pygame.draw.rect(tile, (255, 255, 255, 120),
                     highlight_rect, border_radius=8)

    shadow_rect = pygame.Rect(0, h // 3, w, h * 2 // 3)
    pygame.draw.rect(tile, (0, 0, 0, 60),
                     shadow_rect, border_radius=8)

    pygame.draw.rect(tile, (255, 255, 255, 220),
                     tile.get_rect(), width=1, border_radius=8)

    surface.blit(tile, (x, y))

class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.is_mine = False
        self.adj = 0
        self.revealed = False
        self.flagged = False

    def reset(self):
        self.is_mine = False
        self.adj = 0
        self.revealed = False
        self.flagged = False


class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines_count = mines
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.mines_placed = False
        self.game_over = False
        self.victory = False

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if self.in_bounds(nr, nc):
                    yield self.grid[nr][nc]

    def _compute_adjacencies(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.is_mine:
                    cell.adj = -1
                    continue
                cell.adj = sum(1 for n in self.neighbors(r, c) if n.is_mine)

    def place_mines(self, safe_r, safe_c):
        """
        Windows-7-style: first click is guaranteed a 0.
        We generate mines AFTER the first click, and ensure that
        the clicked cell and its neighbors have no mines.
        """
        forbidden = {(safe_r, safe_c)}
        for n in self.neighbors(safe_r, safe_c):
            forbidden.add((n.r, n.c))

        positions = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) not in forbidden
        ]
        random.shuffle(positions)
        for r, c in positions[: self.mines_count]:
            self.grid[r][c].is_mine = True

        self._compute_adjacencies()
        self.mines_placed = True
        assert self.grid[safe_r][safe_c].adj == 0

    def reveal(self, r, c):
        if not self.in_bounds(r, c) or self.game_over:
            return

        cell = self.grid[r][c]

        if not self.mines_placed:
            self.place_mines(r, c)

        if cell.revealed or cell.flagged:
            return

        cell.revealed = True

        if cell.is_mine:
            self.game_over = True
            self.victory = False
            return

        if cell.adj == 0:
            self._flood_fill(r, c)

        if self._check_win():
            self.game_over = True
            self.victory = True

    def _flood_fill(self, r, c):
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            cell = self.grid[cr][cc]
            for n in self.neighbors(cr, cc):
                if n.revealed or n.flagged or n.is_mine:
                    continue
                n.revealed = True
                if n.adj == 0:
                    stack.append((n.r, n.c))

    def toggle_flag(self, r, c):
        if not self.in_bounds(r, c) or self.game_over:
            return
        cell = self.grid[r][c]
        if cell.revealed:
            return
        cell.flagged = not cell.flagged

    def chord(self, r, c):
        """
        Windows-style chord:
        If we are on a revealed number and the number of
        flagged neighbors equals that number, reveal the others.
        """
        if not self.in_bounds(r, c) or self.game_over:
            return
        cell = self.grid[r][c]
        if not cell.revealed or cell.adj <= 0:
            return

        neigh = list(self.neighbors(r, c))
        flagged = sum(1 for n in neigh if n.flagged)

        if flagged != cell.adj:
            return

        for n in neigh:
            if n.flagged or n.revealed:
                continue
            n.revealed = True
            if n.is_mine:
                self.game_over = True
                self.victory = False
            elif n.adj == 0:
                self._flood_fill(n.r, n.c)

        if self._check_win():
            self.game_over = True
            self.victory = True

    def remaining_mines_estimate(self):
        flags = sum(1 for row in self.grid for c in row if c.flagged)
        return max(0, self.mines_count - flags)

    def _check_win(self):
        for row in self.grid:
            for c in row:
                if not c.is_mine and not c.revealed:
                    return False
        return True

def reveal_all_cells(board):
    """Reveal every cell on the board (used after loss banner)."""
    for row in board.grid:
        for cell in row:
            cell.revealed = True

def calc_window_size(rows, cols):
    width = max(cols * CELL_SIZE + BORDER * 2, MIN_WINDOW_WIDTH)
    height = rows * CELL_SIZE + BORDER * 2 + TOP_PANEL + BOTTOM_PANEL
    return width, height

def draw_3d_rect(surface, rect, raised=True, fill=None):
    x, y, w, h = rect
    if fill:
        pygame.draw.rect(surface, fill, rect)

    light = (255, 255, 255)
    dark = (128, 128, 128)

    if raised:
        tl = light
        br = dark
    else:
        tl = dark
        br = light

    pygame.draw.line(surface, tl, (x, y), (x + w - 1, y))
    pygame.draw.line(surface, tl, (x, y), (x, y + h - 1))
    pygame.draw.line(surface, br, (x, y + h - 1), (x + w - 1, y + h - 1))
    pygame.draw.line(surface, br, (x + w - 1, y), (x + w - 1, y + h - 1))

def fill_vertical_gradient(surface, top_color, bottom_color):
    """Fill entire surface with a top-to-bottom linear gradient."""
    width, height = surface.get_size()
    if height <= 1:
        surface.fill(top_color)
        return

    r1, g1, b1 = top_color
    r2, g2, b2 = bottom_color
    for y in range(height):
        t = y / (height - 1)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))


def draw_liquid_panel(surface, rect, tint=(255, 255, 255), alpha=80,
                      highlight_alpha=140, radius=20):
    """Large rounded 'liquid glass' panel with tint, highlight, and shadow."""
    x, y, w, h = rect

    # Soft drop shadow behind panel
    shadow = pygame.Surface((w + 6, h + 6), pygame.SRCALPHA)
    pygame.draw.rect(
        shadow,
        (0, 0, 0, 90),
        shadow.get_rect(),
        border_radius=radius + 4,
    )
    surface.blit(shadow, (x + 2, y + 3))

    # Panel surface
    glass = pygame.Surface((w, h), pygame.SRCALPHA)

    # Base tinted glass
    base_color = (*tint, alpha)
    pygame.draw.rect(glass, base_color, glass.get_rect(), border_radius=radius)

    # Top highlight band (gives thickness / lensing feel)
    highlight_rect = pygame.Rect(0, 0, w, h // 2)
    pygame.draw.rect(
        glass,
        (255, 255, 255, highlight_alpha),
        highlight_rect,
        border_radius=radius,
    )

    # Slight inner darkening at bottom for depth
    shadow_rect = pygame.Rect(0, h // 3, w, h * 2 // 3)
    pygame.draw.rect(
        glass,
        (0, 0, 0, 55),
        shadow_rect,
        border_radius=radius,
    )

    # Bright edge
    pygame.draw.rect(
        glass,
        (255, 255, 255, 200),
        glass.get_rect(),
        width=1,
        border_radius=radius,
    )

    surface.blit(glass, (x, y))


def draw_liquid_tile(surface, rect, revealed, pressed=False):
    """Single cell tile styled like a tiny piece of liquid glass."""
    w, h = rect.size
    tile = pygame.Surface((w, h), pygame.SRCALPHA)

    if revealed:
        base = (242, 246, 255, 170)   # brighter, clearer
    else:
        base = (210, 220, 240, 120)   # more frosted

    pygame.draw.rect(tile, base, tile.get_rect(), border_radius=8)

    # Top highlight
    highlight_rect = pygame.Rect(0, 0, w, h // 2)
    pygame.draw.rect(
        tile,
        (255, 255, 255, 150),
        highlight_rect,
        border_radius=8,
    )

    # Inner bottom shadow
    shadow_rect = pygame.Rect(0, h // 3, w, h * 2 // 3)
    pygame.draw.rect(
        tile,
        (0, 0, 0, 50),
        shadow_rect,
        border_radius=8,
    )

    # Edge: brighter when pressed (we can hook into this later if you want)
    border_alpha = 220 if not pressed else 255
    pygame.draw.rect(
        tile,
        (255, 255, 255, border_alpha),
        tile.get_rect(),
        width=1,
        border_radius=8,
    )

    surface.blit(tile, rect.topleft)


def draw_counter(surface, rect, value, font):
    """Draw red 3-digit counter on black background."""
    pygame.draw.rect(surface, (0, 0, 0), rect)
    text = f"{value:03d}"[-3:]
    surf = font.render(text, True, (255, 0, 0))
    text_rect = surf.get_rect(center=rect.center)
    surface.blit(surf, text_rect)


def draw_face(surface, rect, state):
    cx = rect.centerx
    cy = rect.centery
    radius = rect.width // 2 - 4

    fill = (255, 255, 0)
    border = (0, 0, 0)

    pygame.draw.circle(surface, fill, (cx, cy), radius)
    pygame.draw.circle(surface, border, (cx, cy), radius, 2)

    eye_offset_x = radius // 3
    eye_offset_y = radius // 3
    eye_r = 2
    pygame.draw.circle(surface, border, (cx - eye_offset_x, cy - eye_offset_y), eye_r)
    pygame.draw.circle(surface, border, (cx + eye_offset_x, cy - eye_offset_y), eye_r)

    if state == FACE_NEUTRAL:
        start_angle, end_angle = 3.5, 5.8
    elif state == FACE_WIN:
        start_angle, end_angle = 0.8, 2.3
    elif state == FACE_LOSE:
        start_angle, end_angle = 0.8, 2.3
        cy += radius // 2
    else:
        start_angle, end_angle = 3.5, 5.8

    import math
    points = []
    r_mouth = radius // 2
    for i in range(20):
        t = start_angle + (end_angle - start_angle) * i / 19
        x = cx + int(r_mouth * math.cos(t))
        y = cy + int(r_mouth * math.sin(t))
        points.append((x, y))
    pygame.draw.lines(surface, border, False, points, 2)


def draw_board(surface, board, font, mine_font, elapsed, face_state,
               banner_text=None, show_quit_button=False):
    rows, cols = board.rows, board.cols
    width, height = surface.get_size()

    bg = pygame.Surface((width, height))
    t = pygame.time.get_ticks() / 1000.0
    draw_seaside_background(bg, t)

    blurred_bg = blur_surface(bg, scale_factor=0.2)

    surface.blit(bg, (0, 0))

    top_rect = pygame.Rect(
        BORDER,
        BORDER,
        width - 2 * BORDER,
        TOP_PANEL - 10,
    )
    draw_glass_panel_from_bg(surface, blurred_bg, top_rect, radius=18)

    digit_font = mine_font
    counter_rect = pygame.Rect(
        top_rect.left + 16,
        top_rect.top + 8,
        60,
        30,
    )
    timer_rect = pygame.Rect(
        top_rect.right - 16 - 60,
        top_rect.top + 8,
        60,
        30,
    )
    face_rect = pygame.Rect(
        (width - 36) // 2,
        top_rect.top + 4,
        36,
        36,
    )

    draw_counter(surface, counter_rect, board.remaining_mines_estimate(), digit_font)
    draw_counter(surface, timer_rect, int(elapsed), digit_font)
    draw_face(surface, face_rect, face_state)

    grid_w = cols * CELL_SIZE
    grid_h = rows * CELL_SIZE
    grid_x = (width - grid_w) // 2
    grid_y = BORDER + TOP_PANEL

    board_rect = pygame.Rect(
        grid_x - 14,
        grid_y - 14,
        grid_w + 28,
        grid_h + 28,
    )
    draw_glass_panel_from_bg(surface, blurred_bg, board_rect, radius=26)

    for r in range(rows):
        for c in range(cols):
            cell = board.grid[r][c]
            x = grid_x + c * CELL_SIZE
            y = grid_y + r * CELL_SIZE

            tile_rect = pygame.Rect(
                x + 2,
                y + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4,
            )

            draw_glass_tile_from_bg(surface, blurred_bg, tile_rect, cell)

            if cell.revealed:
                if cell.is_mine:
                    pygame.draw.circle(
                        surface,
                        (0, 0, 0),
                        tile_rect.center,
                        CELL_SIZE // 5,
                    )
                elif cell.adj > 0:
                    color = NUMBER_COLORS.get(cell.adj, (0, 0, 0))
                    text = font.render(str(cell.adj), True, color)
                    trect = text.get_rect(center=tile_rect.center)
                    surface.blit(text, trect)
            else:
                if cell.flagged:
                    pole_x = tile_rect.left + tile_rect.w // 3
                    pole_y1 = tile_rect.top + tile_rect.h // 5
                    pole_y2 = tile_rect.bottom - tile_rect.h // 6
                    pygame.draw.line(
                        surface,
                        (20, 20, 20),
                        (pole_x, pole_y1),
                        (pole_x, pole_y2),
                        2,
                    )
                    flag_points = [
                        (pole_x, pole_y1),
                        (pole_x + tile_rect.w // 2, pole_y1 + tile_rect.h // 5),
                        (pole_x, pole_y1 + tile_rect.h // 2),
                    ]
                    pygame.draw.polygon(surface, (255, 90, 90), flag_points)

    quit_rect = None
    if banner_text:
        banner_font = pygame.font.SysFont("SF Pro Display", 14, bold=True)
        text_surf = banner_font.render(banner_text, True, (0, 0, 0))
        text_w, text_h = text_surf.get_size()

        max_banner_w = width - 2 * BORDER - 20
        banner_w = min(max_banner_w, text_w + 40)
        banner_h = text_h + 24

        banner_x = (width - banner_w) // 2
        banner_y = (height - banner_h) // 2

        banner_rect = pygame.Rect(banner_x, banner_y, banner_w, banner_h)
        draw_glass_panel_from_bg(surface, blurred_bg, banner_rect, radius=14)

        fog = pygame.Surface((banner_w, banner_h), pygame.SRCALPHA)
        pygame.draw.rect(fog, (255, 255, 255, 200),
                         fog.get_rect(), border_radius=14)
        surface.blit(fog, (banner_x, banner_y))

        text_rect = text_surf.get_rect(center=banner_rect.center)
        surface.blit(text_surf, text_rect)

    if show_quit_button:
        btn_w, btn_h = 88, 32
        btn_x = width - BORDER - btn_w
        btn_y = height - BORDER - btn_h
        quit_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

        draw_glass_panel_from_bg(surface, blurred_bg, quit_rect, radius=16)

        fog = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
        pygame.draw.rect(fog, (255, 255, 255, 180),
                         fog.get_rect(), border_radius=16)
        surface.blit(fog, (btn_x, btn_y))

        q_surf = font.render("Quit", True, (0, 0, 0))
        q_rect = q_surf.get_rect(center=quit_rect.center)
        surface.blit(q_surf, q_rect)

    return face_rect, (grid_x, grid_y), quit_rect

def cell_from_pos(pos, board, grid_origin):
    gx, gy = grid_origin
    x, y = pos
    if x < gx or y < gy:
        return None
    col = (x - gx) // CELL_SIZE
    row = (y - gy) // CELL_SIZE
    if 0 <= row < board.rows and 0 <= col < board.cols:
        return row, col
    return None

def run_game(rows, cols, mines):
    pygame.display.set_caption("Minesweeper")
    width, height = calc_window_size(rows, cols)
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    font = pygame.font.SysFont("consolas", 18, bold=True)
    digit_font = pygame.font.SysFont("consolas", 22, bold=True)

    board = Board(rows, cols, mines)
    clock = pygame.time.Clock()

    running = True
    face_state = FACE_NEUTRAL
    start_time = None
    last_time = 0.0

    banner_start_time = None
    banner_text = None
    banner_done = False
    quit_button_visible = False

    while running:
        dt = clock.tick(60) / 1000.0
        if start_time is not None and not board.game_over:
            last_time = time.time() - start_time

        width, height = screen.get_size()
        rows, cols = board.rows, board.cols

        available_w = width - 2 * BORDER
        available_h = height - TOP_PANEL - BOTTOM_PANEL - 2 * BORDER

        new_cell_size = min(available_w // cols, available_h // rows)

        new_cell_size = max(16, new_cell_size)
        global CELL_SIZE
        CELL_SIZE = new_cell_size
        if board.game_over and not board.victory:
            if banner_start_time is None:
                banner_start_time = time.time()

        if banner_start_time is not None and not banner_done:
            elapsed_banner = time.time() - banner_start_time
            if elapsed_banner < 5.0:
                banner_text = "GG, next time u should try better!"
                quit_button_visible = False
            else:
                banner_text = None
                banner_done = True
                reveal_all_cells(board)
                quit_button_visible = True
        elif banner_done:
            banner_text = None
            quit_button_visible = True

        mouse_pressed = pygame.mouse.get_pressed(3)
        if mouse_pressed[0] and mouse_pressed[2] and not board.game_over:
            face_state = FACE_PRESSED
        else:
            if board.game_over:
                face_state = FACE_WIN if board.victory else FACE_LOSE
            else:
                face_state = FACE_NEUTRAL

        face_rect, grid_origin, quit_rect = draw_board(
            screen, board, font, digit_font, last_time, face_state,
            banner_text=banner_text,
            show_quit_button=quit_button_visible,
        )
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                continue
            
            if banner_start_time is not None and not banner_done:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and not board.game_over:
                buttons = pygame.mouse.get_pressed(3)
                pos = event.pos
                cell_pos = cell_from_pos(pos, board, grid_origin)
                if cell_pos and buttons[0] and buttons[2]:
                    r, c = cell_pos
                    if start_time is None:
                        start_time = time.time()
                    board.chord(r, c)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if quit_rect and quit_button_visible and quit_rect.collidepoint(event.pos):
                        return "quit"

                    if face_rect.collidepoint(event.pos) and not (banner_start_time and not banner_done):
                        board = Board(rows, cols, mines)
                        start_time = None
                        last_time = 0.0
                        banner_start_time = None
                        banner_text = None
                        banner_done = False
                        quit_button_visible = False
                        continue

                    cell_pos = cell_from_pos(event.pos, board, grid_origin)
                    if cell_pos and not board.game_over:
                        r, c = cell_pos
                        if start_time is None:
                            start_time = time.time()
                        board.reveal(r, c)

                elif event.button == 3 and not board.game_over:
                    cell_pos = cell_from_pos(event.pos, board, grid_origin)
                    if cell_pos:
                        r, c = cell_pos
                        board.toggle_flag(r, c)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key == pygame.K_F2 and not (banner_start_time and not banner_done):
                    board = Board(rows, cols, mines)
                    start_time = None
                    last_time = 0.0
                    banner_start_time = None
                    banner_text = None
                    banner_done = False
                    quit_button_visible = False

    return "quit"


def difficulty_menu():
    """Very simple text-based difficulty menu in terminal."""
    print("Minesweeper difficulty:")
    print("1) Beginner   (9x9, 10 mines)")
    print("2) Intermediate (16x16, 40 mines)")
    print("3) Expert     (16x30, 99 mines)")
    print("4) Custom")

    choice = input("Choose 1-4 (Enter for Beginner): ").strip()
    if choice == "2":
        return INTERMEDIATE
    if choice == "3":
        return EXPERT
    if choice == "4":
        try:
            rows = int(input("Rows (max 24): "))
            cols = int(input("Cols (max 30): "))
            mines = int(input("Mines: "))
        except ValueError:
            print("Invalid input, using Beginner.")
            return BEGINNER
        rows = max(1, min(24, rows))
        cols = max(1, min(30, cols))
        mines = max(1, min(rows * cols - 1, mines))
        return rows, cols, mines
    return BEGINNER


def main():
    pygame.init()
    rows, cols, mines = difficulty_menu()

    while True:
        result = run_game(rows, cols, mines)
        if result == "quit":
            break

    pygame.quit()


if __name__ == "__main__":
    main()
