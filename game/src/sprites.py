import pygame
from config import *
import math
import random

random.seed(101)


class SpriteSheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height, scaling=0):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return pygame.transform.scale(sprite, (TILE_SIZE * scaling, TILE_SIZE * scaling)) if scaling else \
            pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'

        self.image = self.game.character_sprite_sheet.get_sprite(3, 2, 32, 32)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change, self.y_change = 0, 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_blocks(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            if direction == 'x':
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
            if direction == 'y':
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        tmp = 16 if random.randint(1, 10) > 8 else 0
        self.image = self.game.blocks_sprite_sheet.get_sprite(tmp, 0, 16, 16)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        tmp = 48 if random.randint(1, 10) > 8 else 32
        self.image = self.game.blocks_sprite_sheet.get_sprite(tmp, 16, 16, 16)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class CobWeb(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = PROPS_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = (x + random.randint(0, 5) / 10) * TILE_SIZE
        self.y = (y + random.randint(0, 5) / 10) * TILE_SIZE
        self.width = 16
        self.height = 16

        self.image = self.game.blocks_sprite_sheet.get_sprite(64, 0, 16, 16, 0.5)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y