from random import randint

import pygame

from config import *


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, breakable=False):
        self.game = game
        self.groups = self.game.ground, self.game.walls
        pygame.sprite.Sprite.__init__(self, *self.groups)
        self.image = game.data.blocks[1 if randint(1, 10) > 8 else 0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * TILE_SIZE, y * TILE_SIZE
        self.breakable = breakable


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.ground
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = game.data.blocks[3 if randint(1, 10) > 8 else 2]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * TILE_SIZE, y * TILE_SIZE


class CobWeb(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.ground
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = game.data.blocks[4]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (x + randint(0, 5) / 10) * TILE_SIZE, (
            y + randint(0, 5) / 10
        ) * TILE_SIZE
