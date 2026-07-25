import pygame

class Bullet:
    def __init__(self, x, y):
        try:
            self.image = pygame.image.load("assets/images/bullet.png")
            self.image = pygame.transform.scale(self.image, (6, 15))
        except:
            self.image = pygame.Surface((6, 15))
            self.image.fill((255, 255, 0))
            
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def move(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)