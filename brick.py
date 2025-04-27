import pygame

class Brick:
    def __init__(self, x, y, color):
        self.width = 70
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect) 