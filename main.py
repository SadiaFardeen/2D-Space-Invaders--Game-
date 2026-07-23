import pygame
import sys
import random

# from player import Player, Bullet
# from enemy import EnemyManager

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Space Invaders!")

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.SysFont("Arial", 28)
large_font = pygame.font.SysFont("Arial", 50)
small_font = pygame.font.SysFont("Arial", 20)

game_state = "START_MENU"
score = 0
lives = 3

stars = []
for _ in range(70):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    speed = random.choice([1, 2, 3])
    stars.append([x, y, speed])

def draw_stars():
    for star in stars:
        star[1] += star[2]
        if star[1] > SCREEN_HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, SCREEN_WIDTH)
        color = (255, 255, 255) if star[2] == 3 else (150, 150, 180)
        pygame.draw.circle(screen, color, (star[0], star[1]), star[2])

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
                game_state = "PLAYING"
                score = 0
                lives = 3
            elif game_state == "PLAYING" and event.key == pygame.K_p:
                game_state = "PAUSED"
            elif game_state == "PAUSED" and event.key == pygame.K_p:
                game_state = "PLAYING"
            elif game_state == "GAME_OVER" and event.key == pygame.K_RETURN:
                game_state = "PLAYING"
                score = 0
                lives = 3

  
    if game_state == "START_MENU":
        title_text = large_font.render("SPACE INVADERS", True, (0, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2 - 120))

        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2, 240, 50)
        
        if button_rect.collidepoint(mouse_pos):
            button_color = (0, 200, 255)
            text_color = (10, 10, 30)
            if mouse_click:
                game_state = "PLAYING"
                score = 0
                lives = 3
        else:
            button_color = (20, 40, 80)
            text_color = (255, 255, 255)

        pygame.draw.rect(screen, button_color, button_rect, border_radius=12)
        pygame.draw.rect(screen, (0, 255, 255), button_rect, 2, border_radius=12)
        
        btn_text = font.render("PLAY GAME", True, text_color)
        screen.blit(btn_text, (button_rect.x + 45, button_rect.y + 8))

        info_text = small_font.render("Press ENTER to Start | Press 'P' to Pause", True, (180, 180, 200))
        screen.blit(info_text, (SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 + 100))

  
    elif game_state == "PLAYING":
        score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_surf = font.render(f"Lives: {lives}", True, (255, 50, 50))
        screen.blit(score_surf, (15, 15))
        screen.blit(lives_surf, (SCREEN_WIDTH - 120, 15))

  
    elif game_state == "PAUSED":
        pause_text = large_font.render("GAME PAUSED", True, (255, 255, 0))
        sub_text = font.render("Press 'P' to Resume", True, (255, 255, 255))
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 - 50))
        screen.blit(sub_text, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 20))


    elif game_state == "GAME_OVER":
        over_text = large_font.render("GAME OVER", True, (255, 50, 50))
        final_score = font.render(f"Final Score: {score}", True, (255, 255, 255))
        restart_text = small_font.render("Press ENTER to Play Again", True, (0, 255, 0))
        
        screen.blit(over_text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 80))
        screen.blit(final_score, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 40))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
