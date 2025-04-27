import pygame
import sys
import random
import os
from paddle import Paddle
from ball import Ball
from brick import Brick
from powerup import PowerUp

# 초기화
pygame.init()
pygame.mixer.init()  # 사운드 초기화

# 사운드 로드
def load_sound(filename):
    return pygame.mixer.Sound(os.path.join('sounds', filename))

try:
    paddle_sound = load_sound('paddle_hit.wav')
    brick_sound = load_sound('brick_hit.wav')
    powerup_sound = load_sound('powerup.wav')
    game_over_sound = load_sound('game_over.wav')
    level_up_sound = load_sound('level_up.wav')
except:
    print("Warning: sound files not found")
    paddle_sound = brick_sound = powerup_sound = game_over_sound = level_up_sound = None

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Arkanoid')

# 게임 객체 생성
paddle = Paddle(WIDTH // 2, HEIGHT - 30)
ball = Ball(WIDTH // 2, HEIGHT - 50)
bricks = []
powerups = []

# 게임 상태
score = 0
lives = 3
game_over = False
level = 1

def create_bricks():
    bricks.clear()
    colors = [RED, GREEN, BLUE, YELLOW, PURPLE]
    for row in range(5):
        for col in range(10):
            brick = Brick(col * 80 + 10, row * 30 + 50, colors[row])
            bricks.append(brick)

def reset_game():
    global score, lives, game_over, level
    score = 0
    lives = 3
    game_over = False
    level = 1
    paddle.reset()
    ball.reset()
    create_bricks()
    powerups.clear()

# 초기 벽돌 생성
create_bricks()

# 게임 루프
clock = pygame.time.Clock()
running = True
game_over_sound_played = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()
                game_over_sound_played = False

    if not game_over:
        # 패들 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.rect.left > 0:
            paddle.move_left()
        if keys[pygame.K_RIGHT] and paddle.rect.right < WIDTH:
            paddle.move_right()

        # 공 이동
        ball.move()

        # 충돌 검사
        if ball.rect.colliderect(paddle.rect):
            ball.bounce_paddle(paddle.rect.centerx)
            if paddle_sound:
                paddle_sound.play()

        for brick in bricks[:]:
            if ball.rect.colliderect(brick.rect):
                ball.bounce()
                score += 10
                bricks.remove(brick)
                if brick_sound:
                    brick_sound.play()
                
                # 파워업 드롭 확률
                if random.random() < 0.2:  # 20% 확률
                    powerup = PowerUp(brick.rect.centerx, brick.rect.centery)
                    powerups.append(powerup)
                break

        # 파워업 처리
        for powerup in powerups[:]:
            powerup.move()
            if powerup.rect.colliderect(paddle.rect):
                powerup.apply_effect(paddle, ball)
                if powerup_sound:
                    powerup_sound.play()
                powerups.remove(powerup)
            elif powerup.rect.top > HEIGHT:
                powerups.remove(powerup)

        # 게임 오버 체크
        if ball.rect.bottom > HEIGHT:
            lives -= 1
            if lives <= 0:
                game_over = True
                if game_over_sound and not game_over_sound_played:
                    game_over_sound.play()
                    game_over_sound_played = True
            else:
                paddle.reset()
                ball.reset()

        # 레벨 클리어 체크
        if not bricks:
            level += 1
            create_bricks()
            paddle.reset()
            ball.reset()
            powerups.clear()
            if level_up_sound:
                level_up_sound.play()

    # 화면 그리기
    screen.fill(BLACK)
    paddle.draw(screen)
    ball.draw(screen)
    for brick in bricks:
        brick.draw(screen)
    for powerup in powerups:
        powerup.draw(screen)

    # 점수와 생명 표시
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    lives_text = font.render(f'Lives: {lives}', True, WHITE)
    level_text = font.render(f'Level: {level}', True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))
    screen.blit(level_text, (WIDTH // 2 - 50, 10))

    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over', True, RED)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, text_rect)
        
        restart_text = pygame.font.Font(None, 36).render('Press R to restart', True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit() 