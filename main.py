from sb3_contrib import RecurrentPPO
import pygame
import sys
import random
import math
import numpy as np
# from stable_baselines3.common.envs import make_vec_env
from gym import spaces

EPOCHS = 1000
character_states = {

}

game_state = {

}

game_settings = {
    "screen_width": 800,
    "screen_height": 600,
    "fps": 60,
    "background_color": (0, 0, 0),
    "char_count": 5,
    "char_speed": 5,
    "char_size": (50, 50),
}

weapons = {
    "sword": {
        "damage": 10,
        "range": 50,
        "cooldown": 1.0
    },
    "bow": {
        "damage": 5,
        "range": 200,
        "cooldown": 0.5
    }
}

# Character observable states
health_state_dict = {
    "Healthy": 0,
    "Injured": 1,
    "Critical": 2,
    "Dead": 3
}

# Character class
class Character:
    def __init__(self, id, x, y):
        self.pos = pygame.Vector2(x, y)
        self.radius = 15
        self.speed = 3
        self.weapon = random.choice(list(weapons.keys()))
        self.health = 100
        self.facing_angle = random.uniform(0, 2 * math.pi)
        self.turn_speed = 5  # Degrees per frame
        self.score = 0
        self.state = "Healthy"
        self.id = id

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), self.radius)

        facing_vector = pygame.Vector2(math.cos(self.facing_angle), math.sin(self.facing_angle)) * self.radius
        
        end_point = self.pos + facing_vector * self.radius
        pygame.draw.line(screen, (0, 255, 0), (int(self.pos.x), int(self.pos.y)), (int(end_point.x), int(end_point.y)), 2)

    def draw_vision_cone(self, screen, vision_surface):
        cone_angle = math.radians(60)
        left_angle = self.facing_angle - cone_angle / 2
        right_angle = self.facing_angle + cone_angle / 2
        left_vector = pygame.Vector2(math.cos(left_angle), math.sin(left_angle)) * self.radius * 20
        right_vector = pygame.Vector2(math.cos(right_angle), math.sin(right_angle)) * self.radius * 20
        cone_points = [
            self.pos,
            self.pos + left_vector,
            self.pos + right_vector
        ]
        color = (0, 0, 255, 100)  # Semi-transparent blue
        pygame.draw.polygon(vision_surface, color, [(int(p.x), int(p.y)) for p in cone_points])
        pygame.draw.polygon(screen, (0, 0, 255), [(int(p.x), int(p.y)) for p in cone_points], 1)


    def move(self, direction):
        if direction == "up":
            self.pos.y -= self.speed
        elif direction == "down":
            self.pos.y += self.speed
        elif direction == "left":
            self.pos.x -= self.speed
        elif direction == "right":
            self.pos.x += self.speed

        # Ensures the character stays within the screen bounds
        self.pos.x = max(0, min(self.pos.x, game_settings["screen_width"]))
        self.pos.y = max(0, min(self.pos.y, game_settings["screen_height"]))

# Function to create a number of characters
def create_characters():
    characters = []
    for i in range(game_settings["char_count"]):
        x = i * (game_settings["screen_width"] // game_settings["char_count"]) + 50
        y = game_settings["screen_height"] // 2
        characters.append(Character(i, x, y))
    return characters

# Draws all characters and their vision cones on the screen
def draw_characters(screen, vision_surface, characters):
    # Drawing out each character in their position
    for char in characters:
        char.draw(screen)
        # Sketching the vision cone for each character
        char.draw_vision_cone(screen, vision_surface)

    # Drawing all the transparent vision cones at once
    screen.blit(vision_surface, (0, 0))

def main():
    print("Hello World!")

    # Initialize Pygame
    pygame.init()

    screen = pygame.display.set_mode((game_settings["screen_width"], game_settings["screen_height"]))

    pygame.display.set_caption("Survival of the Fittest")

    vision_surface = pygame.Surface((game_settings["screen_width"], game_settings["screen_height"]), pygame.SRCALPHA)
    

    clock = pygame.time.Clock()

    for i in range(EPOCHS):

        characters = create_characters()

        running = True
        while running:
            screen.fill(game_settings["background_color"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fills the screen with the background color
            screen.fill(game_settings["background_color"])

            # Resets the vision surface
            vision_surface.fill((0, 0, 0, 0))

            # Draws characters
            draw_characters(screen, vision_surface, characters)

            pygame.display.flip()
            clock.tick(game_settings["fps"])

        pygame.quit()
if __name__ == "__main__":
    main()