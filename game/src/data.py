import pygame
from config import TILE_SIZE, BLACK, PLAYER_SIZE


class SpriteSheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height, scaling=(TILE_SIZE, TILE_SIZE)):
        sprite = pygame.Surface((width, height)).convert()
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return pygame.transform.scale(sprite, scaling)


class Data:
    def __init__(self):
        self.arial14 = pygame.font.Font('../resources/arial.ttf', 14)

        self.character_sprite_sheet = SpriteSheet('../resources/character.png')
        self.blocks_sprite_sheet = SpriteSheet('../resources/blocks.png')
        self.enemy_sprite_sheet = SpriteSheet('../resources/spider2.png')
        self.bullets_sprite_sheet = SpriteSheet('../resources/bullets.png')
        self.attack_sprite_sheet = SpriteSheet('../resources/attack.png')

        self.player_animation_positions = {
            'up': [self.character_sprite_sheet.get_sprite(0, 32, 32, 32, PLAYER_SIZE),
                   self.character_sprite_sheet.get_sprite(32, 32, 32, 32, PLAYER_SIZE),
                   self.character_sprite_sheet.get_sprite(65, 32, 32, 32, PLAYER_SIZE)],
            'down': [self.character_sprite_sheet.get_sprite(0, 0, 32, 32, PLAYER_SIZE),
                     self.character_sprite_sheet.get_sprite(32, 0, 32, 32, PLAYER_SIZE),
                     self.character_sprite_sheet.get_sprite(65, 0, 32, 32, PLAYER_SIZE)],
            'right': [self.character_sprite_sheet.get_sprite(0, 64, 32, 32, PLAYER_SIZE),
                      self.character_sprite_sheet.get_sprite(32, 64, 32, 32, PLAYER_SIZE),
                      self.character_sprite_sheet.get_sprite(65, 64, 32, 32, PLAYER_SIZE)],
            'left': [self.character_sprite_sheet.get_sprite(0, 96, 32, 32, PLAYER_SIZE),
                     self.character_sprite_sheet.get_sprite(32, 96, 32, 32, PLAYER_SIZE),
                     self.character_sprite_sheet.get_sprite(65, 96, 32, 32, PLAYER_SIZE)]
        }

        self.bullet_flying = (
            self.bullets_sprite_sheet.get_sprite(0, 0, 8, 7, (24, 21)),
            self.bullets_sprite_sheet.get_sprite(8, 0, 8, 7, (24, 21)),
            self.bullets_sprite_sheet.get_sprite(16, 0, 8, 7, (24, 21)),
            self.bullets_sprite_sheet.get_sprite(24, 0, 8, 7, (24, 21)),
        )
        self.bullet_blowing = (
            self.bullets_sprite_sheet.get_sprite(0, 7, 8, 8, (24, 24)),
            self.bullets_sprite_sheet.get_sprite(8, 7, 8, 8, (24, 24)),
            self.bullets_sprite_sheet.get_sprite(16, 7, 8, 8, (24, 24)),
            self.bullets_sprite_sheet.get_sprite(24, 7, 8, 8, (24, 24))
        )

        self.attacks = (
            self.attack_sprite_sheet.get_sprite(0, 0, 32, 32),
            self.attack_sprite_sheet.get_sprite(32, 0, 32, 32),
            self.attack_sprite_sheet.get_sprite(64, 0, 32, 32),
            self.attack_sprite_sheet.get_sprite(96, 0, 32, 32),
            self.attack_sprite_sheet.get_sprite(128, 0, 32, 32)
        )

        self.blocks = (
            self.blocks_sprite_sheet.get_sprite(0, 0, 16, 16),    # dark brick
            self.blocks_sprite_sheet.get_sprite(16, 0, 16, 16),   # broken dark brick
            self.blocks_sprite_sheet.get_sprite(32, 16, 16, 16),  # cobblestone
            self.blocks_sprite_sheet.get_sprite(48, 16, 16, 16),  # mossy cobblestone
            self.blocks_sprite_sheet.get_sprite(64, 0, 16, 16, (16, 16))  # cobweb
        )

        self.enemies = (
            self.enemy_sprite_sheet.get_sprite(0, 0, 13, 9, (39, 27)),
            self.enemy_sprite_sheet.get_sprite(0, 10, 13, 9, (39, 27)),
            self.enemy_sprite_sheet.get_sprite(14, 10, 13, 9, (39, 27)),
            self.enemy_sprite_sheet.get_sprite(29, 10, 13, 9, (39, 27)),
            self.enemy_sprite_sheet.get_sprite(44, 10, 13, 9, (39, 27)),
            self.enemy_sprite_sheet.get_sprite(59, 10, 13, 9, (39, 27)),
            self.enemy_sprite_sheet.get_sprite(74, 10, 13, 9, (39, 27))
        )
