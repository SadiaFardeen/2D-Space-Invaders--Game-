import pygame
import random
#screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#alien size and speed
ALIEN_MIN_SPEED = 2
ALIEN_MAX_SPEED = 5
ALIEN_WIDTH = 34
ALIEN_HEIGHT = 26
#spawn time 
WAVE_INTERVAL_MS = 3000   
ALIENS_PER_WAVE = 5

class Alien(pygame.sprite.Sprite):
   
    def __init__(self, image_path="alien.png"):
        super().__init__() 

    #load the alien image 

        if image_path:
            raw_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(raw_image, (ALIEN_WIDTH, ALIEN_HEIGHT))
        else:
            self.image = pygame.Surface((ALIEN_WIDTH, ALIEN_HEIGHT))
            self.image.fill((220, 40, 40))  # plain red placeholder rectangle

        self.rect = self.image.get_rect()

        
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height  
        self.speed = random.randint(ALIEN_MIN_SPEED, ALIEN_MAX_SPEED)

    def update(self):
       
        self.rect.y += self.speed

      

class EnemyManager:
  

    def __init__(self, alien_group, image_path="alien.png",
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

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("enemy.py standalone test")
    clock = pygame.time.Clock()

    alien_group = pygame.sprite.Group()
    enemy_manager = EnemyManager(alien_group)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        enemy_manager.update()

        
        for alien in list(alien_group):
            if alien.rect.top > SCREEN_HEIGHT:
                alien.kill() 

        screen.fill((8, 8, 20))
        alien_group.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
