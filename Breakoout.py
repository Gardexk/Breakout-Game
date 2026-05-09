import enum
import random
import sys

import pygame


class GameState(enum.Enum):
    HAVENT_PLAYED = 1
    WON = 2
    LOST = 3


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

PADDLE_WIDTH = 140
PADDLE_HEIGHT = 18
PADDLE_SPEED = 12

BALL_SIZE = 22
BALL_START_SPEED = 6
BALL_MAX_SPEED = 11

BRICK_COLUMNS = 13
BRICK_ROWS = 6
BRICK_WIDTH = 82
BRICK_HEIGHT = 28
BRICK_GAP = 12
BRICK_TOP = 82

BG_COLOR = (12, 15, 24)
PADDLE_COLOR = (82, 177, 255)
BALL_COLOR = (245, 247, 250)
TEXT_COLOR = (235, 239, 245)
MUTED_TEXT_COLOR = (150, 160, 176)
BRICK_COLORS = [
    (255, 91, 91),
    (255, 151, 76),
    (247, 202, 77),
    (90, 203, 143),
    (80, 163, 255),
    (165, 116, 255),
]


pygame.init()
FRAME_CLOCK = pygame.time.Clock()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Breakout")
FONT_LARGE = pygame.font.Font(None, 68)
FONT_SMALL = pygame.font.Font(None, 30)


def draw_centered_text(text, font, y, color=TEXT_COLOR):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WINDOW_WIDTH // 2, y))
    WINDOW.blit(surface, rect)


def build_wall(level):
    wall_width = (BRICK_COLUMNS * BRICK_WIDTH) + ((BRICK_COLUMNS - 1) * BRICK_GAP)
    start_x = (WINDOW_WIDTH - wall_width) // 2
    bricks = []

    for row in range(BRICK_ROWS):
        for column in range(BRICK_COLUMNS):
            x = start_x + column * (BRICK_WIDTH + BRICK_GAP)
            y = BRICK_TOP + row * (BRICK_HEIGHT + BRICK_GAP)
            rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
            color = BRICK_COLORS[(row + level - 1) % len(BRICK_COLORS)]
            points = BRICK_ROWS - row
            bricks.append({"rect": rect, "color": color, "points": points})

    return bricks


def reset_positions(paddle, ball):
    paddle.centerx = WINDOW_WIDTH // 2
    paddle.bottom = WINDOW_HEIGHT - 42
    ball.centerx = paddle.centerx
    ball.bottom = paddle.top - 8


def launch_ball(level):
    speed_y = -(BALL_START_SPEED + min(level - 1, 3))
    speed_x = random.choice([-4, -3, 3, 4])
    return pygame.Vector2(speed_x, speed_y)


def clamp_ball_speed(velocity):
    if velocity.length() > BALL_MAX_SPEED:
        velocity.scale_to_length(BALL_MAX_SPEED)
    return velocity


def bounce_from_paddle(ball, paddle, velocity):
    offset = (ball.centerx - paddle.centerx) / (paddle.width / 2)
    offset = max(-1, min(1, offset))
    velocity.x = offset * BALL_MAX_SPEED
    velocity.y = -abs(velocity.y)

    if velocity.length() < BALL_START_SPEED:
        velocity.scale_to_length(BALL_START_SPEED)

    ball.bottom = paddle.top - 1
    return clamp_ball_speed(velocity)


def draw_hud(score, lives, level, paused, waiting_to_launch):
    score_surface = FONT_SMALL.render(f"Puntos: {score}", True, TEXT_COLOR)
    lives_surface = FONT_SMALL.render(f"Vidas: {lives}", True, TEXT_COLOR)
    level_surface = FONT_SMALL.render(f"Nivel: {level}", True, TEXT_COLOR)
    WINDOW.blit(score_surface, (24, 18))
    WINDOW.blit(lives_surface, (24, 48))
    WINDOW.blit(level_surface, (WINDOW_WIDTH - 125, 18))

    if waiting_to_launch:
        draw_centered_text("Presiona ESPACIO para lanzar", FONT_SMALL, WINDOW_HEIGHT - 86, MUTED_TEXT_COLOR)

    if paused:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 145))
        WINDOW.blit(overlay, (0, 0))
        draw_centered_text("Pausa", FONT_LARGE, WINDOW_HEIGHT // 2 - 20)
        draw_centered_text("Presiona P para continuar", FONT_SMALL, WINDOW_HEIGHT // 2 + 38, MUTED_TEXT_COLOR)


def draw_game(paddle, ball, bricks, score, lives, level, paused, waiting_to_launch):
    WINDOW.fill(BG_COLOR)

    for brick in bricks:
        pygame.draw.rect(WINDOW, brick["color"], brick["rect"], border_radius=4)

    pygame.draw.rect(WINDOW, PADDLE_COLOR, paddle, border_radius=9)
    pygame.draw.ellipse(WINDOW, BALL_COLOR, ball)
    draw_hud(score, lives, level, paused, waiting_to_launch)

    pygame.display.flip()


def menu_screen(state, score=0, level=1):
    while True:
        WINDOW.fill(BG_COLOR)

        title = "BREAKOUT"
        subtitle = "Rompe todos los ladrillos y evita perder la pelota"
        action = "Enter: jugar   |   Flechas/A-D: mover   |   P: pausa"

        if state == GameState.WON:
            title = "Ganaste"
            subtitle = f"Puntaje final: {score}  |  Nivel alcanzado: {level}"
            action = "Enter: jugar otra vez"
        elif state == GameState.LOST:
            title = "Perdiste"
            subtitle = f"Puntaje final: {score}  |  Nivel alcanzado: {level}"
            action = "Enter: intentar de nuevo"

        draw_centered_text(title, FONT_LARGE, WINDOW_HEIGHT // 2 - 95)
        draw_centered_text(subtitle, FONT_SMALL, WINDOW_HEIGHT // 2 - 20, MUTED_TEXT_COLOR)
        draw_centered_text(action, FONT_SMALL, WINDOW_HEIGHT // 2 + 42, TEXT_COLOR)
        draw_centered_text("Esc: salir", FONT_SMALL, WINDOW_HEIGHT // 2 + 90, MUTED_TEXT_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        FRAME_CLOCK.tick(FPS)


def game_loop():
    paddle = pygame.Rect(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)

    level = 1
    lives = 3
    score = 0
    paused = False
    waiting_to_launch = True
    velocity = pygame.Vector2(0, 0)
    bricks = build_wall(level)
    reset_positions(paddle, ball)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameState.LOST, score, level
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_SPACE and waiting_to_launch and not paused:
                    velocity = launch_ball(level)
                    waiting_to_launch = False

        keys = pygame.key.get_pressed()

        if not paused:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                paddle.x -= PADDLE_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                paddle.x += PADDLE_SPEED

            paddle.clamp_ip(WINDOW.get_rect())

            if waiting_to_launch:
                ball.centerx = paddle.centerx
                ball.bottom = paddle.top - 8
            else:
                ball.x += round(velocity.x)
                ball.y += round(velocity.y)

                if ball.left <= 0:
                    ball.left = 0
                    velocity.x = abs(velocity.x)
                elif ball.right >= WINDOW_WIDTH:
                    ball.right = WINDOW_WIDTH
                    velocity.x = -abs(velocity.x)

                if ball.top <= 0:
                    ball.top = 0
                    velocity.y = abs(velocity.y)

                if ball.colliderect(paddle) and velocity.y > 0:
                    velocity = bounce_from_paddle(ball, paddle, velocity)

                hit_brick = None
                for brick in bricks:
                    if ball.colliderect(brick["rect"]):
                        hit_brick = brick
                        break

                if hit_brick:
                    bricks.remove(hit_brick)
                    velocity.y *= -1
                    velocity *= 1.02
                    velocity = clamp_ball_speed(velocity)
                    score += hit_brick["points"] * 10

                    if not bricks:
                        level += 1
                        if level > 3:
                            return GameState.WON, score, level - 1
                        bricks = build_wall(level)
                        waiting_to_launch = True
                        reset_positions(paddle, ball)
                        velocity = pygame.Vector2(0, 0)

                if ball.top > WINDOW_HEIGHT:
                    lives -= 1
                    if lives <= 0:
                        return GameState.LOST, score, level
                    waiting_to_launch = True
                    reset_positions(paddle, ball)
                    velocity = pygame.Vector2(0, 0)

        draw_game(paddle, ball, bricks, score, lives, level, paused, waiting_to_launch)
        FRAME_CLOCK.tick(FPS)


game_state = GameState.HAVENT_PLAYED
last_score = 0
last_level = 1

while True:
    menu_screen(game_state, last_score, last_level)
    game_state, last_score, last_level = game_loop()
