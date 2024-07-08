import pygame

pygame.init()

# Визначаємо константи
WIDTH, HEIGHT = 1000, 800
CELL_SIZE = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font("arial-unicode-ms.ttf", 30)
screen = 'menu'

class Button:
    def __init__(self, text, position, font, color, text_color, action, width_color, hover_color, size=(200, 50)):
        self.text = text
        self.position = position
        self.font = font
        self.color = color
        self.text_color = text_color
        self.action = action
        self.width_color = width_color
        self.hover_color = hover_color
        self.size = size
        self.label = self.font.render(self.text, True, self.text_color)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.visible = True
        self.is_hovered = False

    def draw(self, window):
        if self.visible:
            color = self.hover_color if self.is_hovered else self.color
            pygame.draw.rect(window, color, self.rect, border_radius=10)
            pygame.draw.rect(window, self.width_color, self.rect, width=5)
            label_pos = (self.rect.centerx - self.label.get_width() // 2, self.rect.centery - self.label.get_height() // 2)
            window.blit(self.label, label_pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

def start_game():
    global screen
    screen = "game"

# Встановлюємо розмір кнопки 300х100 пікселів
game_start_btn = Button("Start game", (350, 170), font, (255, 255, 255), (0, 0, 0), start_game, (96, 96, 96), (200, 200, 200), size=(300, 100))

menu_buttons = [game_start_btn]

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()
grid = [[0] * (WIDTH // CELL_SIZE) for _ in range(HEIGHT // CELL_SIZE)]
game_running = False

def count_neighbors(x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if 0 <= x + i < len(grid[0]) and 0 <= y + j < len(grid):
                count += grid[y + j][x + i]
    return count

def update_grid():
    global grid
    new_grid = [[0] * (WIDTH // CELL_SIZE) for _ in range(HEIGHT // CELL_SIZE)]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            neighbors = count_neighbors(x, y)
            if grid[y][x] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = 1
            else:
                if neighbors == 3:
                    new_grid[y][x] = 1
    grid = new_grid

def clear_grid():
    global grid
    grid = [[0] * (WIDTH // CELL_SIZE) for _ in range(HEIGHT // CELL_SIZE)]

run = True
while run:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if screen == "menu":
                pygame.quit()
                run = False
            else:
                screen = "menu"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if screen == 'menu':
                for button in menu_buttons:
                    if button.is_clicked(mouse_pos):
                        button.action()
            else:
                x, y = pygame.mouse.get_pos()
                x //= CELL_SIZE
                y //= CELL_SIZE
                grid[y][x] = 1 if not grid[y][x] else 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_running = not game_running
            elif event.key == pygame.K_c:
                clear_grid()

    if screen == 'game':
        window.fill(WHITE)
        if game_running:
            update_grid()
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 1:
                    pygame.draw.rect(window, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(window, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        pygame.display.flip()
        clock.tick(10)
    elif screen == 'menu':
        window.fill((160, 160, 160))
        font_text = pygame.font.Font("arial-unicode-ms.ttf", 22)
        menu_text = font_text.render("Press SPACE to Start/Stop, Press C to Clear, Click to Toggle Cells, Rress X to Return to the Menu", True, BLACK)
        window.blit(menu_text, (20, 100))
        for button in menu_buttons:
            button.update(mouse_pos)
            button.draw(window)
        pygame.display.flip()
        clock.tick(90)
  #lesbian massage sex with gymnastic girl