import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
DARK_RED = (180, 0, 0)
GREEN = (50, 255, 100)
DARK_GREEN = (0, 180, 50)
BLUE = (30, 30, 60)
YELLOW = (255, 255, 100)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def create_gradient_surface(width, height, color1, color2):
    """Create a surface with vertical gradient"""
    surface = pygame.Surface((width, height))
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    return surface


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.lifetime = 30
        self.color = color
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.vy += 0.2  # Gravity

    def render(self, surface):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / 30))
            color_with_alpha = (*self.color, alpha)
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, color_with_alpha, (self.size, self.size), self.size)
            surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))


class Snake:
    def __init__(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.particles = []

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)

        if len(self.positions) > 2 and new in self.positions[2:]:
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

        # Update particles
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()

        return True

    def create_eat_effect(self, x, y):
        """Create particle effect when eating food"""
        for _ in range(15):
            self.particles.append(Particle(x, y, YELLOW))

    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.particles = []

    def render(self, surface):
        # Render particles first (behind snake)
        for particle in self.particles:
            particle.render(surface)

        # Render snake with gradient effect
        for i, p in enumerate(self.positions):
            ratio = i / max(len(self.positions) - 1, 1)

            # Color gradient from bright to dark
            r = int(GREEN[0] * (1 - ratio * 0.6))
            g = int(GREEN[1] * (1 - ratio * 0.4))
            b = int(GREEN[2] * (1 - ratio * 0.6))
            color = (r, g, b)

            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))

            # Draw rounded rectangle
            pygame.draw.rect(surface, color, rect, border_radius=5)

            # Add highlight effect on head
            if i == 0:
                highlight_rect = pygame.Rect(
                    rect.x + 2, rect.y + 2, rect.width - 4, rect.height // 2 - 2
                )
                pygame.draw.rect(surface, (150, 255, 150), highlight_rect, border_radius=3)

            # Draw border
            pygame.draw.rect(surface, DARK_GREEN, rect, 2, border_radius=5)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        self.pulse = 0

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1),
                         random.randint(0, GRID_HEIGHT - 1))
        self.pulse = 0

    def update(self):
        self.pulse += 0.1

    def render(self, surface):
        # Pulsing effect
        pulse_size = int(2 * math.sin(self.pulse))

        rect = pygame.Rect(
            (self.position[0] * GRID_SIZE - pulse_size,
             self.position[1] * GRID_SIZE - pulse_size),
            (GRID_SIZE + pulse_size * 2, GRID_SIZE + pulse_size * 2)
        )

        # Draw glowing effect
        glow_surface = pygame.Surface((GRID_SIZE + 10, GRID_SIZE + 10), pygame.SRCALPHA)
        glow_color = (*RED, 100)
        pygame.draw.circle(glow_surface, glow_color,
                           (GRID_SIZE // 2 + 5, GRID_SIZE // 2 + 5),
                           GRID_SIZE // 2 + 5)
        surface.blit(glow_surface,
                     (self.position[0] * GRID_SIZE - 5,
                      self.position[1] * GRID_SIZE - 5))

        # Draw food with gradient
        pygame.draw.rect(surface, RED, rect, border_radius=8)

        # Add highlight
        highlight_rect = pygame.Rect(
            rect.x + 3, rect.y + 3, rect.width - 6, rect.height // 2 - 3
        )
        pygame.draw.rect(surface, (255, 150, 150), highlight_rect, border_radius=5)

        pygame.draw.rect(surface, DARK_RED, rect, 2, border_radius=8)


def draw_text(surface, text, size, x, y, color=WHITE, shadow=True):
    font = pygame.font.Font(None, size)

    # Draw shadow
    if shadow:
        shadow_surface = font.render(text, True, BLACK)
        shadow_rect = shadow_surface.get_rect()
        shadow_rect.midtop = (x + 2, y + 2)
        surface.blit(shadow_surface, shadow_rect)

    # Draw main text
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_grid(surface):
    """Draw subtle grid lines"""
    grid_color = (20, 20, 40)
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, grid_color, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, grid_color, (0, y), (WINDOW_WIDTH, y))


def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Game - Enhanced')

    # Create gradient background
    background = create_gradient_surface(WINDOW_WIDTH, WINDOW_HEIGHT,
                                         (10, 10, 30), (30, 30, 60))

    snake = Snake()
    food = Food()

    running = True
    game_over = False

    while running:
        clock.tick(10)

        if not game_over:
            snake.handle_keys()

            if not snake.update():
                game_over = True

            food.update()

            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 10

                # Create particle effect
                px = food.position[0] * GRID_SIZE + GRID_SIZE // 2
                py = food.position[1] * GRID_SIZE + GRID_SIZE // 2
                snake.create_eat_effect(px, py)

                food.randomize_position()
                while food.position in snake.positions:
                    food.randomize_position()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        food.randomize_position()
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

        # Draw background
        screen.blit(background, (0, 0))
        draw_grid(screen)

        # Draw game objects
        snake.render(screen)
        food.render(screen)

        # Draw score with fancy styling
        draw_text(screen, f'SCORE: {snake.score}', 42, WINDOW_WIDTH // 2, 15, YELLOW)

        if game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            draw_text(screen, 'GAME OVER!', 80, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80, RED)
            draw_text(screen, f'Final Score: {snake.score}', 50, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WHITE)
            draw_text(screen, 'Press SPACE to play again', 36, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60, GREEN)
            draw_text(screen, 'Press ESC to quit', 36, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100, (150, 150, 150))

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
