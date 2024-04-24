import pygame
import math
from src.config import *
from src.sprites.props import Bullet, Attack


class Player(pygame.sprite.Sprite):
    def __init__(self, game, position, start_room_pos):
        self.game = game
        pygame.sprite.Sprite.__init__(self)

        self.x, self.y = position
        self.room_x, self.room_y = start_room_pos
        self.x_change, self.y_change = 0, 0
        self.facing = 'down'
        self.animation_loop = 1

        self.animation_positions = self.game.data.player_animation_positions

        self.image = self.game.data.player_animation_positions.get(self.facing)[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.width, self.height = self.rect.width, self.rect.height

        self.map_open = False
        self.map_open_pressed = False

        self.last_shooting = 1

        self.max_health = 30
        self.health = 30

    def update(self):
        self.keyboard_action()
        self.animate()

        self.x += self.x_change
        self.rect.x = self.x
        collide_blocks(self, 'x')
        self.y += self.y_change
        self.rect.y = self.y
        collide_blocks(self, 'y')

        self.x_change, self.y_change = 0, 0
        self.last_shooting += 1
        if self.last_shooting > 10000:
            self.last_shooting = 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        factor = self.health / self.max_health
        pygame.draw.rect(surface, (180, 0, 0), (14, WIN_HEIGHT - 34, 200, 20))
        pygame.draw.rect(surface, (0, 180, 0), (14, WIN_HEIGHT - 34, 200 * factor, 20))
        title = self.game.data.arial14.render(f'{self.health} / {self.max_health}', True, (0, 0, 0))
        title_rect = title.get_rect(center=(max(200 * factor - 12, 40), WIN_HEIGHT - 24))
        surface.blit(title, title_rect)

    def keyboard_action(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'

        if self.x_change != 0 and self.y_change != 0:
            self.x_change /= math.sqrt(2)
            self.y_change /= math.sqrt(2)

        if keys[pygame.K_m] and not self.map_open_pressed:
            self.map_open_pressed = True
            self.map_open = not self.map_open
        elif not keys[pygame.K_m]:
            self.map_open_pressed = False

        if pygame.mouse.get_pressed()[0] and self.last_shooting > 20:
            Bullet(self.game, 5, pygame.mouse.get_pos())
            self.last_shooting = 1

        if keys[pygame.K_SPACE] and self.last_shooting > 20:
            Attack(self.game, self.rect.x, self.rect.y)
            self.last_shooting = 1

    def get_room(self):
        return self.room_x, self.room_y

    def animate(self):
        if self.x_change == 0 and self.y_change == 0:
            self.image = self.animation_positions.get(self.facing)[0]
        else:
            self.image = self.animation_positions.get(self.facing)[int(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 1

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.game.playing = False


def collide_blocks(sprite, direction):
    hits = pygame.sprite.spritecollide(sprite, sprite.game.walls, False)
    if hits:
        if direction == 'x':
            if sprite.x_change > 0:
                sprite.rect.x = hits[0].rect.left - sprite.rect.width
            if sprite.x_change < 0:
                sprite.rect.x = hits[0].rect.right
            sprite.x = sprite.rect.x
        if direction == 'y':
            if sprite.y_change > 0:
                sprite.rect.y = hits[0].rect.top - sprite.rect.height
            if sprite.y_change < 0:
                sprite.rect.y = hits[0].rect.bottom
            sprite.y = sprite.rect.y
