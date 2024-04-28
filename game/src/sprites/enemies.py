import random

import pygame
from src.sprites.player import collide_blocks


class Spider(pygame.sprite.Sprite):
    def __init__(self, game, position):
        self.game = game
        self.x, self.y = position
        pygame.sprite.Sprite.__init__(self, self.game.enemies)

        self.image = self.game.data.spider.get('standing')[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.x_change, self.y_change = 0, 0
        self.start_health = self.game.data.spider.get('start_health') * self.game.difficulty
        self.health = self.start_health
        self.facing = 'right'

        self.damage = self.game.data.spider.get('damage') * self.game.difficulty

        self.shooting = False
        self.damage_cooldown = 121

        self.animation_loop = 1
        self.animation_pos = 1

    def update(self):
        if not self.shooting:
            if self.damage_cooldown > 120:
                self.move()
            self.damage_player()
        self.animate()
        self.damage_cooldown += 1
        self.animation_loop += 1

        self.x += self.x_change
        self.rect.x = self.x
        collide_blocks(self, 'x')
        self.y += self.y_change
        self.rect.y = self.y
        collide_blocks(self, 'y')
        self.x_change, self.y_change = 0, 0

    def move(self):
        player_pos = self.game.player.rect.x, self.game.player.rect.y
        self.x_change += 1 if player_pos[0] > self.rect.x else -1 if player_pos[0] < self.rect.x else 0
        self.y_change += 1 if player_pos[1] > self.rect.y else -1 if player_pos[1] < self.rect.y else 0

        if self.x_change < 0:
            self.facing = 'left'
        elif self.x_change > 0:
            self.facing = 'right'

        self.x_change *= random.randint(5, 15) / 10
        self.y_change *= random.randint(5, 15) / 10

    def register_hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()

    def draw(self, surface):
        if self.health != self.start_health:
            new_width: int = self.rect.width * (self.health / self.start_health)
            pygame.draw.rect(surface, (180, 0, 0), (self.rect.x, self.rect.y - 8, self.rect.width, 8))
            pygame.draw.rect(surface, (0, 180, 0), (self.rect.x, self.rect.y - 8, new_width, 8))
        surface.blit(self.image, self.rect, None, 0)

    def calculate_distance(self):
        distance = ((self.game.player.rect.centerx - self.rect.centerx) ** 2 +
                    (self.game.player.rect.centery - self.rect.centery) ** 2) ** 0.5
        return distance < 100

    def damage_player(self):
        if self.calculate_distance() and self.damage_cooldown > 180:
            self.shooting = True
            self.animation_loop = 1
            self.animation_pos = 0

    def animate(self):

        if self.shooting:
            if self.animation_loop >= 10:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos == len(self.game.data.spider.get('attacking')):
                    CobWeb(self.game, (self.x, self.y), self.damage)
                    self.damage_cooldown = 1
                    self.shooting = False
                    return
                self.image = self.game.data.spider.get('attacking')[self.animation_pos] if self.facing == 'left' else \
                    pygame.transform.flip(self.game.data.spider.get('attacking')[self.animation_pos], True, False)
        elif (self.x_change == 0 and self.y_change == 0) or self.damage_cooldown < 120:
            if self.animation_loop >= 10:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos == 5:
                    self.animation_pos = 0
            self.image = self.game.data.spider.get('standing')[self.animation_pos] if self.facing == 'left' else \
                pygame.transform.flip(self.game.data.spider.get('standing')[self.animation_pos], True, False)
        else:
            if self.animation_loop >= 10:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos == 6:
                    self.animation_pos = 0
                self.image = self.game.data.spider.get('walking')[self.animation_pos] if self.facing == 'left' else \
                    pygame.transform.flip(self.game.data.spider.get('walking')[self.animation_pos], True, False)


class CobWeb(pygame.sprite.Sprite):
    def __init__(self, game, position, damage):
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.game.attacks)

        self.image = self.game.data.spider.get('web')[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.damage = damage

        self.h_x = (game.player.rect.x - position[0]) / 11
        self.h_y = (game.player.rect.y - position[1]) / 11

        self.animation_loop = 1
        self.animation_pos = 0

    def update(self):
        self.animate()

    def animate(self):
        self.animation_loop += 1
        if self.animation_loop >= 4:
            self.animation_loop = 1
            self.animation_pos += 1
            if self.animation_pos == 11:
                if pygame.sprite.collide_rect(self, self.game.player):
                    self.game.player.take_damage(self.damage)
                self.kill()
                return
            self.image = self.game.data.spider.get('web')[self.animation_pos // 2]
            self.rect.x += self.h_x
            self.rect.y += self.h_y
