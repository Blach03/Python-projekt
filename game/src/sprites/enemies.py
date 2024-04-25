import random

import pygame
from src.sprites.player import collide_blocks


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, position):
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.game.enemies)

        self.image = self.game.data.enemies[0]
        self.rect = self.image.get_rect()
        self.x, self.y = position
        self.rect.x, self.rect.y = position

        self.x_change, self.y_change = 0, 0
        self.start_health = 7
        self.health = self.start_health
        self.facing = 'right'

        self.damage = 1
        self.damage_cooldown = 1

        self.animation_loop = 1
        self.animation_pos = 1

    def update(self):
        self.move()
        self.damage_player()
        self.damage_cooldown += 1
        self.animation_loop += 1

    def move(self):
        player_pos = self.game.player.rect.x, self.game.player.rect.y
        self.x_change += 1 if player_pos[0] > self.rect.x else -1 if player_pos[0] < self.rect.x else 0
        self.y_change += 1 if player_pos[1] > self.rect.y else -1 if player_pos[1] < self.rect.y else 0

        if self.x_change < 0:
            self.facing = 'left'
        elif self.x_change > 0:
            self.facing = 'right'
        self.animate()

        self.x_change *= random.randint(5, 15) / 10
        self.y_change *= random.randint(5, 15) / 10

        self.x += self.x_change
        self.rect.x = self.x
        collide_blocks(self, 'x')
        self.y += self.y_change
        self.rect.y = self.y
        collide_blocks(self, 'y')
        self.x_change, self.y_change = 0, 0

    def register_hit(self):
        self.health -= 1
        if self.health == 0:
            self.kill()

    def draw(self, surface):
        if self.health != self.start_health:
            pygame.draw.rect(surface, (180, 0, 0),
                             (self.rect.x, self.rect.y - 8, self.rect.width, 8))
            pygame.draw.rect(surface, (0, 180, 0),
                             (self.rect.x, self.rect.y - 8, self.rect.width * (self.health / self.start_health), 8))
        surface.blit(self.image, self.rect, None, 0)

    def damage_player(self):
        if self.damage_cooldown > 60 and pygame.sprite.collide_rect(self, self.game.player):
            self.game.player.take_damage(3)
            self.damage_cooldown = 1

    def animate(self):
        if self.x_change == 0 and self.y_change == 0:
            if self.facing == 'right':
                self.image = pygame.transform.flip(self.game.data.enemies[0], True, False)
            else:
                self.image = self.game.data.enemies[0]
        else:
            if self.animation_loop >= 10:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos == len(self.game.data.enemies):
                    self.animation_pos = 0
                if self.facing == 'right':
                    self.image = pygame.transform.flip(self.game.data.enemies[self.animation_pos], True, False)
                else:
                    self.image = self.game.data.enemies[self.animation_pos]

