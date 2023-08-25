import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHAPE_COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (128, 128, 128)]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]
# ...

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Initialize clock
clock = pygame.time.Clock()

# Initialize game variables
current_shape = None
current_shape_x = 0
current_shape_y = 0
score = 0


# Functions
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, SHAPE_COLORS[grid[y][x]], pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

def new_shape():
    shape = random.choice(SHAPES)
    return shape

def draw_shape(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] != 0:
                pygame.draw.rect(screen, SHAPE_COLORS[shape[row][col]], pygame.Rect((x + col) * GRID_SIZE, (y + row) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

def collision(x, y, shape):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] != 0:
                if y + row >= GRID_HEIGHT or x + col < 0 or x + col >= GRID_WIDTH or grid[y + row][x + col] != 0:
                    return True
    return False

def place_shape(x, y, shape):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] != 0:
                grid[y + row][x + col] = shape[row][col]

def clear_lines():
    global score
    lines_cleared = 0
    for row in range(GRID_HEIGHT):
        if all(grid[row]):
            grid.pop(row)
            grid.insert(0, [0] * GRID_WIDTH)
            lines_cleared += 1
    score += lines_cleared * 100

# Game states
STATE_STARTUP = "startup"
STATE_GAME = "game"
STATE_TOPSCORE = "topscore"
STATE_CONFIGURE = "configure"
current_state = STATE_STARTUP

def draw_startup_page():
    screen.fill(BLACK)

    # Draw title
    title_font = pygame.font.Font(None, 100)
    title_text = title_font.render("TETRIS", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 77))
    screen.blit(title_text, title_rect)

    # Draw year and course code
    info_font = pygame.font.Font(None, 24)
    year_text = info_font.render("Year: 2023", True, WHITE)
    course_text = info_font.render("Course Code: 7805ICT_3235", True, WHITE)
    year_rect = year_text.get_rect(center=(WIDTH // 2, 160))
    course_rect = course_text.get_rect(center=(WIDTH // 2, 200))
    screen.blit(year_text, year_rect)
    screen.blit(course_text, course_rect)

    # Draw students list
    students_list = ["Sterin Thomas", "Irene Priya Jose", "Bhavya Thalath", "Aparna Jyothi"]  # Replace with your actual student names
    students_font = pygame.font.Font(None, 20)
    students_text = ", ".join(students_list)
    students_rendered = students_font.render(students_text, True, WHITE)
    students_rect = students_rendered.get_rect(center=(WIDTH // 2, 280))
    screen.blit(students_rendered, students_rect)

    # Draw buttons
    buttons = [
        (exit_button, "Exit"),
        (score_button, "Top Scores"),
        (configure_button, "Configure")
    ]
    for button, text in buttons:
        pygame.draw.rect(screen, WHITE, button)
        button_text = info_font.render(text, True, BLACK)
        button_rect = button_text.get_rect(center=button.center)
        screen.blit(button_text, button_rect)


def draw_topscore_page():
    screen.fill(BLACK)

    # Draw top score title
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Top Scores", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 44))
    screen.blit(title_text, title_rect)

    # Simulated top scores data
    top_scores_data = [
        ("Player 1", 1000),
        ("Player 2", 800),
        ("Player 3", 600),
        ("Player 4", 500),
        ("Player 5", 400),
        ("Player 6", 300),
        ("Player 7", 200),
        ("Player 8", 100),
        ("Player 9", 50),
        ("Player 10", 10)
    ]

    # Draw top scores list
    info_font = pygame.font.Font(None, 24)
    y_position = 90
    for player, score in top_scores_data:
        score_text = f"{player}: {score}"
        score_rendered = info_font.render(score_text, True, WHITE)
        score_rect = score_rendered.get_rect(center=(WIDTH // 2, y_position))
        screen.blit(score_rendered, score_rect)
        y_position += 40

    # Draw close button
    pygame.draw.rect(screen, WHITE, close_button)
    close_text = info_font.render("Close", True, BLACK)
    close_rect = close_text.get_rect(center=close_button.center)
    screen.blit(close_text, close_rect)


def draw_configure_page():
    screen.fill(BLACK)

    # Draw configure title
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Configure", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    # Draw configure items
    info_font = pygame.font.Font(None, 24)
    y_position = 180
    game_level_options = ["High", "Medium", "Low"]
    selected_game_level = game_level_options[1]  # Default value is "High"
    field_length_input=10
    field_width_input=20
    configure_items = [
        ("Size of the field:", f"{field_length_input} x {field_width_input}"),
        ("Game level:", selected_game_level),
        ("Normal or extended game:", "Normal"),
        ("Player or AI game mode:", "Player")
    ]

    for item_name, item_value in configure_items:
        item_text = f"{item_name} {item_value}"
        item_rendered = info_font.render(item_text, True, WHITE)
        item_rect = item_rendered.get_rect(center=(WIDTH // 2, y_position))
        screen.blit(item_rendered, item_rect)
        y_position += 40

    # Draw close button
    pygame.draw.rect(screen, WHITE, close_button)
    close_text = info_font.render("Close", True, BLACK)
    close_rect = close_text.get_rect(center=close_button.center)
    screen.blit(close_text, close_rect)




button_width = 200
button_height = 50
button_y = 400

exit_button = pygame.Rect((WIDTH - button_width) // 2, button_y, button_width, button_height)
score_button = pygame.Rect((WIDTH - button_width) // 2, button_y + 70, button_width, button_height)
configure_button = pygame.Rect((WIDTH - button_width) // 2, button_y + 140, button_width, button_height)
close_button = pygame.Rect((WIDTH - button_width) // 2, button_y + 70, button_width, button_height)




# Game loop
while True:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if current_state == STATE_STARTUP:
                if exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif score_button.collidepoint(mouse_pos):
                    current_state = STATE_TOPSCORE
                elif configure_button.collidepoint(mouse_pos):
                    current_state = STATE_CONFIGURE

            elif current_state == STATE_TOPSCORE:
                if close_button.collidepoint(mouse_pos):
                    current_state = STATE_STARTUP

            elif current_state == STATE_CONFIGURE:
                if close_button.collidepoint(mouse_pos):
                    current_state = STATE_STARTUP

    if current_state == STATE_STARTUP:
        draw_startup_page()

    elif current_state == STATE_TOPSCORE:
        draw_topscore_page()

    elif current_state == STATE_CONFIGURE:
        draw_configure_page()

    pygame.display.flip()
    clock.tick(30)

# Clean up
pygame.quit()
sys.exit()
