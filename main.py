import pygame
import sys
import random
import os
import time 
from manager import GameManager

class GameManager:
    def __init__(self):
        self.lives = 3
        self.start_time = 0
        self.current_survive_time = 0
        self.high_time = self.load_high_time()

    def get_lives(self):
        return self.lives

    def lose_life(self):
        self.lives -= 1
        return self.lives <= 0 

    def start_timer(self):
        self.start_time = time.time()
        self.current_survive_time = 0

    def update_timer(self):
        self.current_survive_time = round(time.time() - self.start_time, 1)
        if self.current_survive_time > self.high_time:
            self.high_time = self.current_survive_time
            self.save_high_time()

    def get_current_time(self):
        return self.current_survive_time

    def get_high_time(self):
        return self.high_time

    def load_high_time(self):
        if os.path.exists("high_time.txt"):
            try:
                with open("high_time.txt", "r") as file:
                    return float(file.read().strip())
            except ValueError:
                return 0.0
        return 0.0

    def save_high_time(self):
        with open("high_time.txt", "w") as file:
            file.write(str(self.high_time))

    def reset(self):
        self.lives = 3
        self.start_timer()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 40
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 255, 150)) 
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 10:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 790:
            self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top)



class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 2, y, 4, 10)
        self.speed = 8

    def move(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), self.rect)  


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((35, 25))
        self.image.fill((220, 40, 40))  
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_dropping = False
        self.drop_speed = 4

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
        
        for alien in self.group:
            if not alien.is_dropping:
                alien.rect.x += self.speed * self.direction
                if alien.rect.right >= 780 or alien.rect.left <= 20:
                    self.direction *= -1

            alien.update()

        
        if len(self.group) > 0 and random.random() < 0.025:
            normal_aliens = [a for a in self.group if not a.is_dropping]
            if normal_aliens:
                chosen_alien = random.choice(normal_aliens)
                chosen_alien.is_dropping = True

        
        if len(self.group) == 0:
            self.spawn_wave()

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders - Survival Mode")

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 48)
small_font = pygame.font.SysFont("Arial", 18)

game_state = "START_MENU"

stars = [[random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.choice([1, 2, 3])] for _ in range(70)]

def draw_stars():
    for star in stars:
        star[1] += star[2]
        if star[1] > SCREEN_HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, SCREEN_WIDTH)
        color = (255, 255, 255) if star[2] == 3 else (150, 150, 180)
        pygame.draw.circle(screen, color, (star[0], star[1]), star[2])


player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)
bullets = []

alien_group = pygame.sprite.Group()
enemy_manager = EnemyManager(alien_group)
game_manager = GameManager()

def reset_game():
    global bullets
    game_manager.reset()
    bullets.clear()
    enemy_manager.spawn_wave()
    player.rect.centerx = SCREEN_WIDTH // 2
    player.rect.bottom = SCREEN_HEIGHT - 20

running = True
while running:
    screen.fill((10, 10, 30))
    draw_stars()

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_click = True

        if event.type == pygame.KEYDOWN:
            if game_state == "START_MENU" and event.key == pygame.K_RETURN:
                reset_game()
                game_state = "PLAYING"
            elif game_state == "PLAYING":
                if event.key == pygame.K_p:
                    game_state = "PAUSED"
                elif event.key == pygame.K_SPACE:
                    bullets.append(player.shoot())
            elif game_state == "PAUSED" and event.key == pygame.K_p:
                
                game_manager.start_time = time.time() - game_manager.get_current_time()
                game_state = "PLAYING"
            elif game_state == "GAME_OVER" and event.key == pygame.K_RETURN:
                reset_game()
                game_state = "PLAYING"

    if game_state == "START_MENU":
        title_text = large_font.render("SPACE INVADERS", True, (0, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 140))

        best_time_text = font.render(f"Highest Survival Record: {game_manager.get_high_time()}s", True, (255, 215, 0))
        screen.blit(best_time_text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 70))

        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2, 240, 50)
        
        if button_rect.collidepoint(mouse_pos):
            button_color = (0, 200, 255)
            text_color = (10, 10, 30)
            if mouse_click:
                reset_game()
                game_state = "PLAYING"
        else:
            button_color = (20, 40, 80)
            text_color = (255, 255, 255)

        pygame.draw.rect(screen, button_color, button_rect, border_radius=12)
        pygame.draw.rect(screen, (0, 255, 255), button_rect, 2, border_radius=12)
        
        btn_text = font.render("PLAY GAME", True, text_color)
        screen.blit(btn_text, (button_rect.x + 55, button_rect.y + 10))

        info_text = small_font.render("Press ENTER to Start | SPACE to Shoot | 'P' to Pause", True, (180, 180, 200))
        screen.blit(info_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 100))

    elif game_state == "PLAYING":
        game_manager.update_timer()

        keys = pygame.key.get_pressed()
        player.move(keys)
        player.draw(screen)

        enemy_manager.update()
        alien_group.draw(screen)

        # Bullets Movement
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw(screen)
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        for bullet in bullets[:]:
            hit_aliens = [alien for alien in alien_group if bullet.rect.colliderect(alien.rect)]
            if hit_aliens:
                for alien in hit_aliens:
                    alien.kill()
                if bullet in bullets:
                    bullets.remove(bullet)

        # Alien Collision Logic
        for alien in list(alien_group):
            if alien.rect.colliderect(player.rect):
                alien.kill()
                is_game_over = game_manager.lose_life()
                if is_game_over:
                    game_state = "GAME_OVER"

            elif alien.rect.top >= SCREEN_HEIGHT:
                alien.kill()

        # Display Stats (Lives, Current Survival Time, Best Time)
        lives_surf = font.render(f"Lives: {game_manager.get_lives()}", True, (255, 50, 50))
        time_surf = font.render(f"Time: {game_manager.get_current_time()}s", True, (255, 255, 255))
        high_surf = font.render(f"Best: {game_manager.get_high_time()}s", True, (255, 215, 0))

        screen.blit(lives_surf, (20, 15))
        screen.blit(time_surf, (SCREEN_WIDTH // 2 - 40, 15))
        screen.blit(high_surf, (SCREEN_WIDTH - 140, 15))

    elif game_state == "PAUSED":
        player.draw(screen)
        alien_group.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        pause_text = large_font.render("GAME PAUSED", True, (255, 255, 0))
        sub_text = font.render("Press 'P' to Resume", True, (255, 255, 255))
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        screen.blit(sub_text, (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 20))

    elif game_state == "GAME_OVER":
        over_text = large_font.render("GAME OVER", True, (255, 50, 50))
        survived_text = font.render(f"You Survived: {game_manager.get_current_time()}s", True, (255, 255, 255))
        high_text = font.render(f"Highest Record: {game_manager.get_high_time()}s", True, (255, 215, 0))
        restart_text = small_font.render("Press ENTER to Try Again", True, (0, 255, 0))
        
        screen.blit(over_text, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 100))
        screen.blit(survived_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30))
        screen.blit(high_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 10))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()