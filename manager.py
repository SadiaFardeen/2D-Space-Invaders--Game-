# manager.py
class CollisionManager:
    def _init_(self):
        self.collision_count = 0
    
    def check_collision(self, rect1, rect2):
        """Check if two rectangles collide"""
        return rect1.colliderect(rect2)
    
    def check_bullet_enemy_collision(self, bullets, enemies):
        """Check collision between bullets and enemies"""
        destroyed_enemies = []
        
        for bullet in bullets[:]:  # Iterate over a copy of the list
            for enemy in enemies[:]:
                if self.check_collision(bullet.rect, enemy.rect):
                    # Remove bullet and enemy
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if enemy in enemies:
                        enemies.remove(enemy)
                    destroyed_enemies.append(enemy)
                    self.collision_count += 1
                    break  # Bullet destroyed, move to next bullet
        
        return destroyed_enemies
    
    def check_player_enemy_collision(self, player, enemies):
        """Check collision between player and enemies"""
        for enemy in enemies[:]:
            if self.check_collision(player.rect, enemy.rect):
                return True
        return False
    
    def check_enemy_bottom_collision(self, enemies, screen_height):
        """Check if any enemy has reached the bottom of the screen"""
        for enemy in enemies:
            if enemy.rect.bottom >= screen_height:
                return True
        return False
    
    def reset_collision_count(self):
        """Reset the collision counter"""
        self.collision_count = 0


class EnemyManager:
    def _init_(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemies = []
        self.move_direction = 1  # 1 for right, -1 for left
        self.move_down_amount = 20
        self.move_speed = 2
        self.enemy_rows = 5
        self.enemy_cols = 8
        self.enemy_spacing_x = 60
        self.enemy_spacing_y = 50
        self.start_x = 50
        self.start_y = 60
    
    def create_enemies(self, enemy_class):
        """Create a grid of enemies"""
        self.enemies = []
        for row in range(self.enemy_rows):
            for col in range(self.enemy_cols):
                x = self.start_x + col * self.enemy_spacing_x
                y = self.start_y + row * self.enemy_spacing_y
                enemy = enemy_class(x, y, row, col)
                self.enemies.append(enemy)
        return self.enemies
    
    def update(self):
        """Update enemy positions"""
        # Check if any enemy hits the edge
        edge_reached = False
        for enemy in self.enemies:
            if enemy.rect.right >= self.screen_width and self.move_direction > 0:
                edge_reached = True
                break
            if enemy.rect.left <= 0 and self.move_direction < 0:
                edge_reached = True
                break
        
        # Change direction and move down if edge reached
        if edge_reached:
            self.move_direction *= -1
            for enemy in self.enemies:
                enemy.rect.y += self.move_down_amount
        
        # Move all enemies
        for enemy in self.enemies:
            enemy.rect.x += self.move_speed * self.move_direction
    
    def get_random_enemy(self):
        """Get a random enemy to shoot from"""
        if self.enemies:
            return random.choice(self.enemies)
        return None
    
    def is_empty(self):
        """Check if all enemies are destroyed"""
        return len(self.enemies) == 0
    
    def reset(self):
        """Reset enemy manager"""
        self.enemies = []
        self.move_direction = 1
        self.collision_count = 0


class ScoreManager:
    def _init_(self):
        self.score = 0
        self.high_score = 0
        self.combo = 0
        self.max_combo = 0
    
    def add_score(self, points, combo_multiplier=1):
        """Add points to score with combo multiplier"""
        bonus = points * combo_multiplier
        self.score += bonus
        self.combo += 1
        if self.combo > self.max_combo:
            self.max_combo = self.combo
        return bonus
    
    def reset_combo(self):
        """Reset combo counter"""
        self.combo = 0
    
    def get_score(self):
        """Return current score"""
        return self.score
    
    def get_high_score(self):
        """Return high score"""
        return self.high_score
    
    def update_high_score(self):
        """Update high score if current score is higher"""
        if self.score > self.high_score:
            self.high_score = self.score
    
    def reset(self):
        """Reset score manager"""
        self.score = 0
        self.combo = 0
    
    def get_combo_multiplier(self):
        """Get current combo multiplier (starts at 1, increases with combo)"""
        return min(1 + self.combo // 5, 5)  # Max multiplier of 5


class GameManager:
    def _init_(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lives = 3
        self.max_lives = 5
        self.score_manager = ScoreManager()
        self.collision_manager = CollisionManager()
        self.enemy_manager = EnemyManager(screen_width, screen_height)
        self.game_state = "START_MENU"  # START_MENU, PLAYING, PAUSED, GAME_OVER
        self.level = 1
        self.enemy_speed_multiplier = 1.0
        self.shield_active = False
        self.shield_timer = 0
    
    def lose_life(self):
        """Decrease lives by 1"""
        self.lives -= 1
        self.score_manager.reset_combo()
        if self.lives <= 0:
            self.game_state = "GAME_OVER"
            self.score_manager.update_high_score()
            return True
        return False
    
    def add_life(self):
        """Add a life (max cap)"""
        if self.lives < self.max_lives:
            self.lives += 1
            return True
        return False
    
    def increase_level(self):
        """Increase game level and difficulty"""
        self.level += 1
        self.enemy_speed_multiplier = 1 + (self.level - 1) * 0.1
        # Reset enemy manager with increased difficulty
        self.enemy_manager.move_speed = 2 * self.enemy_speed_multiplier
        self.enemy_manager.move_down_amount = 20 + (self.level - 1) * 2
    
    def reset_game(self):
        """Reset entire game"""
        self.lives = 3
        self.level = 1
        self.enemy_speed_multiplier = 1.0
        self.enemy_manager.reset()
        self.score_manager.reset()
        self.collision_manager.reset_collision_count()
        self.shield_active = False
        self.shield_timer = 0
    
    def update(self):
        """Update game state"""
        if self.game_state == "PLAYING":
            self.enemy_manager.update()
            
            # Check if all enemies are destroyed
            if self.enemy_manager.is_empty():
                self.increase_level()
                # Recreate enemies with new difficulty
                # This will be handled by the main game loop
                return "LEVEL_COMPLETE"
        
        return None
    
    def get_enemy_speed(self):
        """Get current enemy speed based on level and direction"""
        return self.enemy_manager.move_speed * self.enemy_speed_multiplier
    
    def activate_shield(self, duration=300):
        """Activate player shield for duration (in frames)"""
        self.shield_active = True
        self.shield_timer = duration
    
    def update_shield(self):
        """Update shield timer"""
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
