import pygame
from ms_board import Board

MARGIN = 30
TOP_UI = 60

BG_COLOR = (245, 245, 245)
GRID_COLOR = (180, 180, 180)
REVEALED_COLOR = (220, 220, 220)
HIDDEN_COLOR = (200, 200, 200)
TEXT_COLOR = (20, 20, 20)

NUMBER_COLORS = {
    1: (25, 118, 210),
    2: (56, 142, 60),
    3: (211, 47, 47),
    4: (123, 31, 162),
    5: (255, 143, 0),
    6: (0, 151, 167),
    7: (66, 66, 66),
    8: (158, 158, 158),
}

MAX_WINDOW_WIDTH = 1000
MAX_WINDOW_HEIGHT = 800


def compute_geometry(rows: int, cols: int):
    """Pick a cell size so the board fits nicely in the window."""
    cell_size = min(
        40,
        (MAX_WINDOW_WIDTH - 2 * MARGIN) // cols,
        (MAX_WINDOW_HEIGHT - (MARGIN + TOP_UI) - MARGIN) // rows,
    )
    width = cols * cell_size + 2 * MARGIN
    height = rows * cell_size + TOP_UI + MARGIN
    return cell_size, width, height


def load_images(cell_size: int):
    mine_img = pygame.image.load("assets/mine.png").convert_alpha()
    flag_img = pygame.image.load("assets/flag.png").convert_alpha()

    size = cell_size - 8
    mine_img = pygame.transform.smoothscale(mine_img, (size, size))
    flag_img = pygame.transform.smoothscale(flag_img, (size, size))
    return mine_img, flag_img


def draw_game(screen, font, board: Board, mine_img, flag_img, cell_size: int):
    screen.fill(BG_COLOR)
    width, _ = screen.get_size()

    top_text_y = 15
    grid_top = MARGIN + 30
    if board.game_over:
        status = "You Win! 🎉" if board.victory else "Boom! 💥"
    else:
        status = "Left-click: reveal | Right-click: flag | Hover + C: chord"

    text_surf = font.render(status, True, TEXT_COLOR)
    screen.blit(text_surf, (MARGIN, top_text_y))

    button_font = pygame.font.SysFont("consolas", 20)
    btn_w, btn_h = 90, 30
    quit_rect = pygame.Rect(width - MARGIN - btn_w, top_text_y - 5, btn_w, btn_h)
    menu_rect = pygame.Rect(width - MARGIN - 2 * btn_w - 10, top_text_y - 5, btn_w, btn_h)

    for rect, label in ((menu_rect, "Menu"), (quit_rect, "Quit")):
        pygame.draw.rect(screen, (230, 230, 230), rect, border_radius=6)
        pygame.draw.rect(screen, (160, 160, 160), rect, 1, border_radius=6)
        label_surf = button_font.render(label, True, (30, 30, 30))
        label_rect = label_surf.get_rect(center=rect.center)
        screen.blit(label_surf, label_rect)

    left_offset = MARGIN
    for r in range(board.rows):
        for c in range(board.cols):
            cell = board.grid[r][c]
            x = left_offset + c * cell_size
            y = grid_top + r * cell_size
            rect = pygame.Rect(x, y, cell_size, cell_size)
            color = REVEALED_COLOR if cell.revealed else HIDDEN_COLOR
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)
            if cell.revealed:
                if cell.is_mine:
                    img_rect = mine_img.get_rect(center=rect.center)
                    screen.blit(mine_img, img_rect)
                elif cell.adjacent_mines > 0:
                    num = cell.adjacent_mines
                    color = NUMBER_COLORS.get(num, TEXT_COLOR)
                    num_surf = font.render(str(num), True, color)
                    num_rect = num_surf.get_rect(center=rect.center)
                    screen.blit(num_surf, num_rect)
            else:
                if cell.flagged:
                    img_rect = flag_img.get_rect(center=rect.center)
                    screen.blit(flag_img, img_rect)

    pygame.display.flip()
    return {"menu": menu_rect, "quit": quit_rect, "grid_top": grid_top}


def get_cell_from_mouse(pos, board: Board, cell_size: int, grid_top: int):
    x, y = pos
    left_offset = MARGIN

    if x < left_offset or y < grid_top:
        return None

    col = (x - left_offset) // cell_size
    row = (y - grid_top) // cell_size

    if 0 <= row < board.rows and 0 <= col < board.cols:
        return int(row), int(col)
    return None


def run_game(rows: int, cols: int, mines: int) -> str:
    """
    Runs one game.
    Returns:
        "menu" if player clicked Menu
        "quit" if player clicked Quit / closed window
    """
    cell_size, width, height = compute_geometry(rows, cols)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Minesweeper")

    font = pygame.font.SysFont("consolas", 22)
    clock = pygame.time.Clock()
    mine_img, flag_img = load_images(cell_size)

    board = Board(rows, cols, mines)

    running = True
    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        draw_info = draw_game(screen, font, board, mine_img, flag_img, cell_size)
        grid_top = draw_info["grid_top"]
        menu_rect = draw_info["menu"]
        quit_rect = draw_info["quit"]

        hover_cell = get_cell_from_mouse(mouse_pos, board, cell_size, grid_top)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if menu_rect.collidepoint(event.pos):
                        return "menu"
                    if quit_rect.collidepoint(event.pos):
                        return "quit"

                    cell_pos = get_cell_from_mouse(event.pos, board, cell_size, grid_top)
                    if cell_pos and not board.game_over:
                        r, c = cell_pos
                        board.reveal_cell(r, c)

                elif event.button == 3:
                    cell_pos = get_cell_from_mouse(event.pos, board, cell_size, grid_top)
                    if cell_pos and not board.game_over:
                        r, c = cell_pos
                        board.toggle_flag(r, c)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "quit"
                if event.key == pygame.K_m:
                    return "menu"
                if event.key == pygame.K_r:
                    board = Board(rows, cols, mines)
                if event.key == pygame.K_c and hover_cell and not board.game_over:
                    r, c = hover_cell
                    board.chord(r, c)

    return "quit"

def run_menu() -> tuple[int, int, int] | None:
    """
    Show a simple menu.
    Returns (rows, cols, mines) or None if user quits.
    """
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Minesweeper – Menu")

    font_title = pygame.font.SysFont("consolas", 32)
    font_btn = pygame.font.SysFont("consolas", 24)
    clock = pygame.time.Clock()
    options = [
        ("Easy 9 x 9", 9, 9, 10),
        ("Medium 20 x 20", 20, 20, 60),
        ("Hard 50 x 80", 50, 80, 400),
        ("Custom", None, None, None),
    ]

    btn_rects = []
    for idx, (label, *_rest) in enumerate(options):
        btn_w, btn_h = 260, 40
        x = (width - btn_w) // 2
        y = 120 + idx * 60
        btn_rects.append((pygame.Rect(x, y, btn_w, btn_h), label))

    while True:
        clock.tick(60)
        screen.fill(BG_COLOR)

        title_surf = font_title.render("Minesweeper", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(width // 2, 60))
        screen.blit(title_surf, title_rect)

        for rect, label in btn_rects:
            pygame.draw.rect(screen, (230, 230, 230), rect, border_radius=8)
            pygame.draw.rect(screen, (160, 160, 160), rect, 1, border_radius=8)
            text_surf = font_btn.render(label, True, (30, 30, 30))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for (rect, label), opt in zip(btn_rects, options):
                    if rect.collidepoint(event.pos):
                        name, r, c, m = opt
                        if name != "Custom":
                            return r, c, m
                        else:
                            try:
                                rows = int(input("Rows (1–600): "))
                                cols = int(input("Cols (1–600): "))
                            except ValueError:
                                print("Invalid input; using 9x9.")
                                rows, cols = 9, 9

                            rows = max(1, min(600, rows))
                            cols = max(1, min(600, cols))
                            mines = max(1, (rows * cols) // 6)
                            return rows, cols, mines


def main():
    pygame.init()

    while True:
        choice = run_menu()
        if choice is None:
            break
        rows, cols, mines = choice
        result = run_game(rows, cols, mines)
        if result == "quit":
            break

    pygame.quit()


if __name__ == "__main__":
    main()
