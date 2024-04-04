from typing import Any
import pygame
from utils import *

class PLAYER(pygame.sprite.Sprite):
    def __init__(self, position, width, height, img_path):
        super().__init__()
        self.image = load_image(img_path, (width, height))
        self.rect = self.image.get_rect(topleft = position)
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.positionplayer = pygame.math.Vector2(position)
        self.initial_jump = -11
        self.speed = 5
        self.on_ground = True
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.positionplayer.y += self.direction.y
        self.rect.y = self.positionplayer.y

    def update(self):
        self.direction.x = self.speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.on_ground:
            self.direction.y = self.initial_jump
            self.on_ground = False