import pygame
import random

class PowerUp:
    def __init__(self, x, y):
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)
        self.speed = 3
        self.type = random.choice(['expand', 'shrink', 'fast', 'slow', 'extra_life'])
        
        # 파워업 타입에 따른 색상 설정
        self.colors = {
            'expand': (255, 255, 0),    # 노란색
            'shrink': (255, 0, 255),    # 마젠타
            'fast': (0, 255, 255),      # 시안
            'slow': (255, 165, 0),      # 주황색
            'extra_life': (255, 0, 0)   # 빨간색
        }
        self.color = self.colors[self.type]

    def move(self):
        self.rect.y += self.speed

    def apply_effect(self, paddle, ball):
        if self.type == 'expand':
            paddle.expand()
        elif self.type == 'shrink':
            paddle.shrink()
        elif self.type == 'fast':
            ball.speed_up()
        elif self.type == 'slow':
            ball.slow_down()
        elif self.type == 'extra_life':
            pass  # 생명 추가는 main.py에서 처리

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect) 