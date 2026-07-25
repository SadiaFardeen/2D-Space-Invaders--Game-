import os
import time

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