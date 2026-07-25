import pygame
import random

# Screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Alien size and speed
ALIEN_MIN_SPEED = 2
ALIEN_MAX_SPEED = 5
ALIEN_WIDTH = 34
ALIEN_HEIGHT = 26

# Spawn time
WAVE_INTERVAL_MS = 3000   
ALIENS_PER_WAVE = 5

class Alien(pygame.sprite.Sprite):
    def __init__(self, image_path="assets/images/alien.png"):
        super().__init__() 

        try:
            raw_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(raw_image, (ALIEN_WIDTH, ALIEN_HEIGHT))
        except:
            self.image = pygame.Surface((ALIEN_WIDTH, ALIEN_HEIGHT))
            self.image.fill((220, 40, 40))  # Red rectangle fallback

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height  
        self.speed = random.randint(ALIEN_MIN_SPEED, ALIEN_MAX_SPEED)

    def update(self):
        self.rect.y += self.speed


class EnemyManager:
    def __init__(self, alien_group, image_path="assets/images/alien.png",
                 wave_interval_ms=WAVE_INTERVAL_MS,
                 aliens_per_wave=ALIENS_PER_WAVE):
      
        self.alien_group = alien_group
        self.image_path = image_path
        self.wave_interval_ms = wave_interval_ms
        self.aliens_per_wave = aliens_per_wave
        self._last_wave_time = pygame.time.get_ticks()

    def spawn_wave(self):
        """Create a fresh batch of Alien sprites and drop them into the group."""
        for _ in range(self.aliens_per_wave):
            alien = Alien(self.image_path)
            self.alien_group.add(alien)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self._last_wave_time >= self.wave_interval_ms:
            self.spawn_wave()
            self._last_wave_time = now

        self.alien_group.update()