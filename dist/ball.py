import pygame
import math

class Ball:
    def __init__(self, x, y):
        self.radius = 10
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        self.original_speed = 5
        self.speed = self.original_speed
        self.dx = self.speed
        self.dy = -self.speed
        self.color = (255, 255, 255)  # 흰색
        self.original_x = x
        self.original_y = y

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # 벽 충돌 체크
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.dx *= -1
        if self.rect.top <= 0:
            self.dy *= -1

    def bounce(self):
        self.dy *= -1

    def bounce_paddle(self, paddle_center):
        # 패들과의 충돌 위치에 따라 공의 방향 변경
        relative_intersect_x = (paddle_center - self.rect.centerx) / (100 / 2)
        bounce_angle = relative_intersect_x * (math.pi / 3)  # 최대 60도 각도
        
        self.dx = self.speed * math.sin(bounce_angle)
        self.dy = -self.speed * math.cos(bounce_angle)

    def speed_up(self):
        self.speed = min(self.speed + 2, 10)  # 최대 10
        self.update_direction()

    def slow_down(self):
        self.speed = max(self.speed - 2, 3)  # 최소 3
        self.update_direction()

    def update_direction(self):
        # 현재 방향을 유지하면서 속도만 변경
        magnitude = math.sqrt(self.dx**2 + self.dy**2)
        if magnitude > 0:
            self.dx = (self.dx / magnitude) * self.speed
            self.dy = (self.dy / magnitude) * self.speed

    def reset(self):
        self.speed = self.original_speed
        self.rect = pygame.Rect(self.original_x - self.radius, self.original_y - self.radius, 
                              self.radius * 2, self.radius * 2)
        self.dx = self.speed
        self.dy = -self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius) 