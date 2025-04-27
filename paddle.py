import pygame

class Paddle:
    def __init__(self, x, y):
        self.original_width = 100
        self.width = self.original_width
        self.height = 20
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)
        self.speed = 8
        self.color = (255, 255, 255)  # 흰색
        self.original_x = x
        self.original_y = y

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def expand(self):
        self.width = min(self.width + 20, 200)  # 최대 200픽셀
        self.rect.width = self.width
        self.rect.x = self.rect.centerx - self.width//2

    def shrink(self):
        self.width = max(self.width - 20, 50)  # 최소 50픽셀
        self.rect.width = self.width
        self.rect.x = self.rect.centerx - self.width//2

    def reset(self):
        self.width = self.original_width
        self.rect = pygame.Rect(self.original_x - self.width//2, self.original_y - self.height//2, 
                              self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect) 