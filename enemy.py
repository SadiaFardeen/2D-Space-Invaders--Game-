import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((35, 25))
        self.image.fill((220, 40, 40))  # Red alien box
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_dropping = False
        self.drop_speed = 3

    def update(self):
        if self.is_dropping:
            self.rect.y += self.drop_speed


class EnemyManager:
    def __init__(self, group):
        self.group = group
        self.direction = 1
        self.speed = 2
        self.spawn_wave()

    def spawn_wave(self):
        self.group.empty()
        for row in range(3):
            for col in range(8):
                x = 100 + col * 70
                y = 50 + row * 40
                alien = Alien(x, y)
                self.group.add(alien)

    def update(self):
        move_down = False
        
        for alien in self.group:
            if not alien.is_dropping:
                alien.rect.x += self.speed * self.direction
                if alien.rect.right >= SCREEN_WIDTH - 20 or alien.rect.left <= 20:
                    move_down = True
            
            alien.update()

        if move_down:
            self.direction *= -1
            for alien in self.group:
                if not alien.is_dropping:
                    alien.rect.y += 12

        # Randomly drop an alien
        if len(self.group) > 0 and random.random() < 0.015:
            normal_aliens = [a for a in self.group if not a.is_dropping]
            if normal_aliens:
                chosen_alien = random.choice(normal_aliens)
                chosen_alien.is_dropping = True

        if len(self.group) == 0:
            self.spawn_wave()