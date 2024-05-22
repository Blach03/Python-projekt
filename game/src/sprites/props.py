import math

import pygame

from config import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, speed, target):
        self.game = game
        game.bullets_shot += 1
        self.groups = self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x, self.y = (
            game.player.rect.x + game.player.width / 2 - 12,
            game.player.rect.y + game.player.height / 2 - 10.5,
        )

        self.animation_loop = 1
        self.animation_position = 0

        self.angle = math.atan2(target[1] - 12 - self.y, target[0] - 10.5 - self.x)
        self.degree = -self.angle * 180 / math.pi
        self.image = pygame.transform.rotate(
            self.game.data.bullet_flying[0], self.degree
        )
        self.rect = self.image.get_rect(size=(20, 20))
        self.dx = math.cos(self.angle) * speed
        self.dy = math.sin(self.angle) * speed
        self.x += math.cos(self.angle) * TILE_SIZE / 2
        self.y += math.sin(self.angle) * TILE_SIZE / 2
        self.speed = speed
        self.blowing = False

    def update(self):
        self.animation_loop += 1
        if not self.blowing:
            self.x += self.dx
            self.y += self.dy
            self.rect.x = self.x
            self.rect.y = self.y
            self.collide_blocks()
            if self.animation_loop >= 10:
                self.image = pygame.transform.rotate(
                    self.game.data.bullet_flying[self.animation_position], self.degree
                )
                self.animation_position += 1
                if self.animation_position == 4:
                    self.animation_position = 0
                self.animation_loop = 1
        else:
            if self.animation_loop >= 10:
                self.image = self.game.data.bullet_blowing[self.animation_position]
                self.animation_position += 1
            if self.animation_position == 4:
                self.kill()

    def collide_blocks(self):

        def register_hit():
            self.x += 15 * self.dx / self.speed
            self.y += 15 * self.dy / self.speed
            self.rect.x = self.x
            self.rect.y = self.y
            self.blowing = True
            self.animation_loop = 1
            self.animation_position = 1
            self.image = self.game.data.bullet_blowing[0]

        if (
            self.rect.x < 0
            or self.rect.x > WIN_WIDTH
            or self.rect.y < 0
            or self.rect.y > WIN_HEIGHT
        ):
            self.kill()
        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            register_hit()

        enemy_hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if enemy_hits:
            for enemy in enemy_hits:
                enemy.register_hit(self.game.player, self.game.player.attack * 2)
            register_hit()


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        direction = self.game.player.facing
        if direction == "up":
            self.angle = 90
            self.x, self.y = x, y - TILE_SIZE
        elif direction == "down":
            self.angle = -90
            self.x, self.y = x, y + TILE_SIZE
        elif direction == "left":
            self.angle = 180
            self.x, self.y = x - TILE_SIZE, y
        elif direction == "right":
            self.angle = 0
            self.x, self.y = x + TILE_SIZE, y

        self.width, self.height = 32, 32
        self.animation_loop = 0
        self.image = pygame.transform.rotate(self.game.data.attacks[0], self.angle)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.groups = self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.collided = False

    def update(self):
        self.animate()
        if not self.collided:
            self.collide()

    def animate(self):
        self.image = pygame.transform.rotate(
            self.game.data.attacks[int(self.animation_loop)], self.angle
        )
        self.animation_loop += 0.5
        if self.animation_loop >= 5:
            self.kill()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.collided = True
            for enemy in hits:
                enemy.register_hit(self.game.player, self.game.player.attack)
