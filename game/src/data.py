import json

import pygame
from config import *


from items import Potion


class SpriteSheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height, scaling=(TILE_SIZE, TILE_SIZE)):
        sprite = pygame.Surface((width, height)).convert()
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return pygame.transform.scale(sprite, scaling)


class Data:
    def __init__(self):
        self.player_animation_positions = None
        self.get_character_sprites()

        self.bullet_flying = None
        self.bullet_blowing = None
        self.get_bullet_sprites()

        self.attacks = None
        self.get_attacks_sprites()

        self.blocks = None
        self.get_blocks_sprites()

        self.spider = None
        self.get_spider_sprites()

        self.boss = None
        self.get_boss_sprites()

        self.potions = None
        self.get_potion_icons()

    def get_character_sprites(self):
        sprite_sheet = SpriteSheet(CHARACTER_SPRITE)
        xs = (0, 32, 65)
        self.player_animation_positions = {
            "up": [sprite_sheet.get_sprite(x, 32, 32, 32, PLAYER_SIZE) for x in xs],
            "down": [sprite_sheet.get_sprite(x, 0, 32, 32, PLAYER_SIZE) for x in xs],
            "right": [sprite_sheet.get_sprite(x, 64, 32, 32, PLAYER_SIZE) for x in xs],
            "left": [sprite_sheet.get_sprite(x, 96, 32, 32, PLAYER_SIZE) for x in xs],
        }

    def get_bullet_sprites(self):
        sprite_sheet = SpriteSheet(BULLET_SPRITE)
        self.bullet_flying = [
            sprite_sheet.get_sprite(i * 8, 0, 8, 7, (24, 21)) for i in range(4)
        ]
        self.bullet_blowing = [
            sprite_sheet.get_sprite(i * 8, 7, 8, 8, (24, 24)) for i in range(4)
        ]

    def get_attacks_sprites(self):
        sprite_sheet = SpriteSheet(ATTACK_SPRITE)
        self.attacks = [
            sprite_sheet.get_sprite(i * 32, 0, 32, 32) for i in range(4 + 1)
        ]

    def get_blocks_sprites(self):
        sprite_sheet = SpriteSheet(BLOCKS_SPRITE)
        self.blocks = (
            sprite_sheet.get_sprite(0, 0, 16, 16),  # dark brick
            sprite_sheet.get_sprite(16, 0, 16, 16),  # broken dark brick
            sprite_sheet.get_sprite(32, 16, 16, 16),  # cobblestone
            sprite_sheet.get_sprite(48, 16, 16, 16),  # mossy cobblestone
            sprite_sheet.get_sprite(64, 0, 16, 16, (16, 16)),  # cobweb
        )

    def get_spider_sprites(self):
        sprite_sheet = SpriteSheet(SPIDER_SPRITE)
        self.spider = {
            "start_health": 7,
            "damage": 10,
            "standing": [
                sprite_sheet.get_sprite(i * 15, 0, 14, 9, (42, 27)) for i in range(5)
            ],
            "walking": [
                sprite_sheet.get_sprite(i * 15, 10, 14, 9, (42, 27)) for i in range(6)
            ],
            "attacking": [
                sprite_sheet.get_sprite(i * 15, 20, 14, 9, (42, 27)) for i in range(4)
            ],
            "web": [
                sprite_sheet.get_sprite(1 + i * 24, 30, 23, 20, (46, 40))
                for i in range(6)
            ],
        }

    def get_boss_sprites(self):
        sprite_sheet = SpriteSheet(BOSS_SPRITE)
        self.boss = {
            "start_health": 70,
            "damage": 10,
            "standing": [
                sprite_sheet.get_sprite(i * 64, 0, 64, 64, (128, 128)) for i in range(6)
            ],
            "charge": [
                sprite_sheet.get_sprite(i * 64, 64, 64, 64, (128, 128)) for i in range(6)
            ],
            "attacking": [
                sprite_sheet.get_sprite(i * 64, 128, 64, 64, (128, 128)) for i in range(4)
            ],
            "death": [
                sprite_sheet.get_sprite(i * 64, 192, 64, 64, (128, 128)) for i in range(8)
            ],
        }


    def get_potion_icons(self):
        start_potions = json.load(open(POTION_DATA))
        self.potions: list[Potion] = [
            Potion.from_dict_to_player_on_start(start_potions[i]) for i in range(4)
        ]
