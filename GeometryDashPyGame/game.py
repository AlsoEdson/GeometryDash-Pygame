import pygame, os
from utils import *
from player import *

#pygame setup
pygame.init()
WIDTH, HEIGHT = 928, 480;  """MULTIPLO DE 34X34 PORQUE ES EL TAMAÑO DEL PJ"""
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60
RUNNING = True
TILE_SIZE = 32

class BLOCK(pygame.sprite.Sprite):
    def __init__(self, position, width, height, img_path):
        super().__init__()
        self.image = load_image(img_path, (width, height))
        self.rect = self.image.get_rect(topleft = position)

class CAMERA:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def apply(self, target_rect):
        return pygame.Rect(target_rect.x + self.rect.x, target_rect.y + self.rect.y, target_rect.width, target_rect.height)
    
    def update(self, target_rect):
        x = -target_rect.centerx + WIDTH//2
        y = -target_rect.centery + HEIGHT//2
        self.rect = pygame.Rect(x, y, self.width, self.height)

class GAME:
    def __init__(self, map_path):
        self.blocks = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.map = self.read_file(map_path)
        self.load_map()

    def horizontal_movement(self):
        self.player.sprite.positionplayer.x += self.player.sprite.direction.x
        self.player.sprite.rect.x = self.player.sprite.positionplayer.x
        for BLOCK in self.blocks:
            if BLOCK.rect.colliderect(self.player.sprite.rect):
                self.player.sprite.rect.right = BLOCK.rect.left
                self.player.sprite.positionplayer.x = self.player.sprite.rect.x
    
    def vertical_movement(self):
        self.player.sprite.apply_gravity()
        for BLOCK in self.blocks:
            if BLOCK.rect.colliderect(self.player.sprite.rect):
                if self.player.sprite.direction.y < 0:
                    self.player.sprite.rect.top = BLOCK.rect.bottom
                    self.player.sprite.positionplayer.y = self.player.sprite.rect.y
                    self.player.sprite.direction.y = 0
                if self.player.sprite.direction.y > 0:
                    self.player.sprite.rect.bottom = BLOCK.rect.top
                    self.player.sprite.on_ground = True
                    self.player.sprite.positionplayer.y = self.player.sprite.rect.y
                    self.player.sprite.direction.y = 0
                if self.player.sprite.on_ground and self.player.sprite.direction.y < 0 or self.player.sprite.direction.y > 0:
                    self.player.sprite.on_ground = False

    def update(self):
        self.horizontal_movement()
        self.vertical_movement()
        self.player.update()

    def read_file(self, path):
        file = ''
        with open(path, 'r') as f:
            file = f.read().splitlines()
        return file
    
    def load_map(self):
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if char == 'B':
                    self.blocks.add(BLOCK((x*TILE_SIZE, y*TILE_SIZE), TILE_SIZE, TILE_SIZE, os.path.join('images', 'blockbase.png')))
                if char == 'P':
                    self.player.add(PLAYER((x*TILE_SIZE, y*TILE_SIZE), TILE_SIZE, TILE_SIZE, os.path.join('images', 'tigerblockplayer.png')))
    
    def draw(self, surface):
        self.blocks.draw(surface)
        self.player.draw(surface)

#Draw Grid
def draw_grid(surface):
    for y in range(TILE_SIZE, WIDTH, TILE_SIZE):
        pygame.draw.line(surface, "blue", (y, 0), (y, HEIGHT))
    for x in range(TILE_SIZE, HEIGHT, TILE_SIZE):
        pygame.draw.line(surface, "red", (0, x), (WIDTH, x))

game = GAME('resources\\map.txt')

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    SCREEN.fill((255, 255, 255))
    #SCREEN.fill("purple")
    game.update()
    game.draw(SCREEN)
    draw_grid(SCREEN)
    CLOCK.tick(FPS)
    pygame.display.update()
    
pygame.quit()