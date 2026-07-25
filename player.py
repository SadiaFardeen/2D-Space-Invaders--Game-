import pygame

class Player:
    def __init__(self, x, y):
        try:
            self.image = pygame.image.load("assets/images/player.png")
            self.image = pygame.transform.scale(self.image, (50, 40))
        except:
            self.image = pygame.Surface((50, 40), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (0, 255, 255), [(25, 0), (0, 40), (50, 40)])
            
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7
        self.powered = False

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed

    def shoot(self):
        from bullet import Bullet
        return Bullet(self.rect.centerx, self.rect.top)

    def draw(self, screen):
        screen.blit(self.image, self.rect)