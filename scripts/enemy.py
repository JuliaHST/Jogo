import pygame
import random

class Enemy:
    def __init__(self, x, y, width, height, speed, image_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def reset_position(self, screen_width):
        self.x = random.randint(0, screen_width - self.width)
        self.y = random.randint(-100, -40)
