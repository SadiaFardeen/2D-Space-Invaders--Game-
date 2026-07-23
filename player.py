import pygame

class Player:

    def __init__(self,x,y):
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = 7
        self.powered = False

    def move(self,keys):

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

    def shoot(self):
        from bullet import Bullet
        return Bullet(self.rect.centerx,self.rect.top)

    def draw(self,screen):
        screen.blit(self.image,self.rect)