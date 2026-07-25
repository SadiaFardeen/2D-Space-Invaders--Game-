import pygame

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 3, y, 6, 15)
        self.speed = 8

    def move(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), self.rect)


class Player:
    def __init__(self, x, y):
        self.width = 50
        self.height = 40
        self.rect = pygame.Rect(x - self.width // 2, y, self.width, self.height)
        self.speed = 6

    def move(self, keys):
        # Full Left to Right movement fix
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top)

    def draw(self, surface):
        # Draw Space Ship
        pygame.draw.polygon(surface, (0, 255, 128), [
            (self.rect.centerx, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom)
        ])