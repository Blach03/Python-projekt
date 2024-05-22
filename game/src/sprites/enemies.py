import random
import threading
import time
import pygame

from player_info import trigger_ripple
from sprites.player import collide_blocks
from config import TILE_SIZE


class Spider(pygame.sprite.Sprite):
    def __init__(self, game, position):
        self.game = game
        self.x, self.y = position
        pygame.sprite.Sprite.__init__(self, self.game.enemies)

        self.image = self.game.data.spider.get("standing")[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.x_change, self.y_change = 0, 0
        self.start_health = (
            self.game.data.spider.get("start_health") * self.game.difficulty * 40
        )
        self.health = self.start_health
        self.facing = "right"

        self.damage = self.game.data.spider.get("damage") * self.game.difficulty

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
        collide_blocks(self, "x")
        self.y += self.y_change
        self.rect.y = self.y
        collide_blocks(self, "y")
        self.x_change, self.y_change = 0, 0

    def move(self):
        player_pos = self.game.player.rect.x, self.game.player.rect.y
        self.x_change += (
            1
            if player_pos[0] > self.rect.x
            else -1 if player_pos[0] < self.rect.x else 0
        )
        self.y_change += (
            1
            if player_pos[1] > self.rect.y
            else -1 if player_pos[1] < self.rect.y else 0
        )

        if self.x_change < 0:
            self.facing = "left"
        elif self.x_change > 0:
            self.facing = "right"

        self.x_change *= random.randint(5, 15) / 10
        self.y_change *= random.randint(5, 15) / 10

    def register_hit(self, player, damage):
        if player.has_scythe and self not in player.scythe_used_on:
            player.scythe_used_on.append(self)
            damage *= 3

        if player.has_polearm and random.randint(1, 10) < 4:
            damage *= 2

        if player.has_edge and player.current_hp > self.health:
            damage *= 1.25

        if player.has_wyrmblade:
            damage += self.health / 20

        if player.has_soulthirster:
            player.current_hp = min(player.hp, player.current_hp + damage / 20)

        self.health -= damage

        if self.health <= 0:
            self.kill()

            if player.has_heartguard:
                player.hp += 1
            if player.has_amulet:
                player.current_hp = min(player.hp, player.current_hp + 10)

    def draw(self, surface):
        if self.health != self.start_health:
            new_width: int = self.rect.width * (self.health / self.start_health)
            pygame.draw.rect(
                surface, (180, 0, 0), (self.rect.x, self.rect.y - 8, self.rect.width, 8)
            )
            pygame.draw.rect(
                surface, (0, 180, 0), (self.rect.x, self.rect.y - 8, new_width, 8)
            )
        surface.blit(self.image, self.rect, None, 0)

    def calculate_distance(self) -> float:
        distance = (
            (self.game.player.rect.centerx - self.rect.centerx) ** 2
            + (self.game.player.rect.centery - self.rect.centery) ** 2
        ) ** 0.5
        return distance < 100

    def damage_player(self):
        if self.calculate_distance() and self.damage_cooldown > 180:
            self.shooting = True
            self.animation_loop = 1
            self.animation_pos = 0

    def animate(self) -> None:

        if self.shooting:
            if self.animation_loop >= 10:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos >= len(self.game.data.spider.get("attacking")):
                    CobWeb(self.game, (self.x, self.y), self.damage, self)
                    self.damage_cooldown = 1
                    self.shooting = False
                    return
                self.image = (
                    self.game.data.spider.get("attacking")[self.animation_pos]
                    if self.facing == "left"
                    else pygame.transform.flip(
                        self.game.data.spider.get("attacking")[self.animation_pos],
                        True,
                        False,
                    )
                )
        elif (self.x_change == 0 and self.y_change == 0) or self.damage_cooldown < 120:
            if self.animation_loop >= 10:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos >= len(self.game.data.spider.get("standing")):
                    self.animation_pos = 0
            self.image = (
                self.game.data.spider.get("standing")[self.animation_pos]
                if self.facing == "left"
                else pygame.transform.flip(
                    self.game.data.spider.get("standing")[self.animation_pos],
                    True,
                    False,
                )
            )
        else:
            if self.animation_loop >= 10:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos >= len(self.game.data.spider.get("walking")):
                    self.animation_pos = 0
                self.image = (
                    self.game.data.spider.get("walking")[self.animation_pos]
                    if self.facing == "left"
                    else pygame.transform.flip(
                        self.game.data.spider.get("walking")[self.animation_pos],
                        True,
                        False,
                    )
                )


class CobWeb(pygame.sprite.Sprite):
    def __init__(self, game, position, damage, spider):
        self.game = game
        self.spider = spider
        pygame.sprite.Sprite.__init__(self, self.game.attacks)

        self.image = self.game.data.spider.get("web")[0]
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
                    room = self.game.player.get_room()
                    if (
                        room not in self.game.player.shield_used_rooms
                        and self.game.player.has_shield
                    ):
                        self.game.player.shield_used_rooms.append(room)
                    else:
                        if (
                            not self.game.player.has_phantom
                            or random.randint(1, 5) != 1
                        ):
                            self.game.player.take_damage(self.damage)
                    if self.game.player.has_thornforge:
                        self.spider.register_hit(self.game.player, self.damage * 0.3)
                    if self.game.player.has_retaliation:
                        if room not in self.game.player.retaliation_used_rooms:
                            self.game.player.retaliation_used_rooms.append(room)
                            trigger_ripple(
                                (self.game.player.x + 23, self.game.player.y + 23)
                            )
                            for enemy in self.game.enemies:
                                enemy.register_hit(self.game.player, self.damage * 5)
                self.kill()
                return
            self.image = self.game.data.spider.get("web")[self.animation_pos // 2]
            self.rect.x += self.h_x
            self.rect.y += self.h_y



class Boss(pygame.sprite.Sprite):
    def __init__(self, game, position):
        self.game = game
        self.x, self.y = position
        pygame.sprite.Sprite.__init__(self, self.game.enemies)

        self.image = self.game.data.boss.get("standing")[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.x_change, self.y_change = 0, 0
        self.start_health = self.game.data.boss.get("start_health") * self.game.difficulty * 20
        self.health = self.start_health
        self.facing = "right"

        self.damage = self.game.data.boss.get("damage") * self.game.difficulty

        self.shooting = False
        self.damage_cooldown = 121

        self.animation_loop = 1
        self.animation_pos = 1

        self.is_dead = False
        self.death_animation_done = False

    def update(self):
        if not self.is_dead:
            if not self.shooting:
                if self.damage_cooldown > 120:
                    self.move()
                self.damage_player()
            self.animate()
            self.damage_cooldown += 1
            self.animation_loop += 1

            self.x += self.x_change
            self.rect.x = self.x
            collide_blocks(self, "x")
            self.y += self.y_change
            self.rect.y = self.y
            collide_blocks(self, "y")
            self.x_change, self.y_change = 0, 0
        else:
            self.animate_death()

    def move(self):
        player_pos = self.game.player.rect.x, self.game.player.rect.y
        self.x_change += 1 if player_pos[0] > self.rect.x else -1 if player_pos[0] < self.rect.x else 0
        self.y_change += 1 if player_pos[1] > self.rect.y else -1 if player_pos[1] < self.rect.y else 0

        if self.x_change < 0:
            self.facing = "right"
        elif self.x_change > 0:
            self.facing = "left"

        self.x_change *= random.randint(5, 15) / 10
        self.y_change *= random.randint(5, 15) / 10

    def register_hit(self, player, damage):
        if player.has_scythe and self not in player.scythe_used_on:
            player.scythe_used_on.append(self)
            damage *= 3

        if player.has_polearm and random.randint(1, 10) < 4:
            damage *= 2

        if player.has_edge and player.current_hp > self.health:
            damage *= 1.25

        if player.has_wyrmblade:
            damage += self.health / 20

        if player.has_soulthirster:
            player.current_hp = min(player.hp, player.current_hp + damage / 20)

        self.health -= damage

        if self.health <= 0 and not self.is_dead:
            self.is_dead = True
            self.animation_loop = 1
            self.animation_pos = 0

            if player.has_heartguard:
                player.hp += 1
            if player.has_amulet:
                player.current_hp = min(player.hp, player.current_hp + 10)

    def draw(self, surface):
        if self.health != self.start_health:
            new_width: int = self.rect.width * (self.health / self.start_health)
            pygame.draw.rect(
                surface, (180, 0, 0), (self.rect.x, self.rect.y - 8, self.rect.width, 8)
            )
            pygame.draw.rect(
                surface, (0, 180, 0), (self.rect.x, self.rect.y - 8, new_width, 8)
            )
        surface.blit(self.image, self.rect, None, 0)

    def calculate_distance(self) -> float:
        distance = (
            (self.game.player.rect.centerx - self.rect.centerx) ** 2
            + (self.game.player.rect.centery - self.rect.centery) ** 2
        ) ** 0.5
        return distance < 400

    def damage_player(self):
        if self.calculate_distance() and self.damage_cooldown > 180:
            self.shooting = True
            self.animation_loop = 1
            self.animation_pos = 0

    def animate(self) -> None:
        if self.shooting:
            if self.animation_loop >= 10:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos >= len(self.game.data.boss.get("attacking")):
                    x = random.randint(0,2)
                    if x == 0:
                        spawn_fires(self.game, self, self.damage, (self.rect.centerx, self.rect.centery))
                    elif x == 1:
                        Ball(self.game, (self.x + 32, self.y + 32), self.damage, self)
                    else:
                        self.health = min(self.start_health, self.health + self.start_health/5)
                    self.spawn_balls()
                    self.damage_cooldown = 1
                    self.shooting = False
                    return
                self.image = (
                    self.game.data.boss.get("attacking")[self.animation_pos]
                    if self.facing == "left"
                    else pygame.transform.flip(
                        self.game.data.boss.get("attacking")[self.animation_pos],
                        True,
                        False,
                    )
                )
        elif (self.x_change == 0 and self.y_change == 0) or self.damage_cooldown < 120:
            if self.animation_loop >= 10:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos >= len(self.game.data.boss.get("standing")):
                    self.animation_pos = 0
            self.image = (
                self.game.data.boss.get("standing")[self.animation_pos]
                if self.facing == "left"
                else pygame.transform.flip(
                    self.game.data.boss.get("standing")[self.animation_pos],
                    True,
                    False,
                )
            )
        else:
            if self.animation_loop >= 10:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos >= len(self.game.data.boss.get("charge")):
                    self.animation_pos = 0
                self.image = (
                    self.game.data.boss.get("charge")[self.animation_pos]
                    if self.facing == "left"
                    else pygame.transform.flip(
                        self.game.data.boss.get("charge")[self.animation_pos],
                        True,
                        False,
                    )
                )

    def animate_death(self) -> None:
        if self.animation_loop >= 10:
            self.animation_loop = 1
            self.animation_pos += 1
            if self.animation_pos >= len(self.game.data.boss.get("death")):
                self.death_animation_done = True
                self.kill()
                return
        self.image = self.game.data.boss.get("death")[self.animation_pos]
        self.animation_loop += 1

    def spawn_balls(self):
        def create_ball(delay):
            time.sleep(delay)
            ball = Ball(self.game, (self.x + 32, self.y + 32), self.damage, self)
            self.game.attacks.add(ball)

        threading.Thread(target=create_ball, args=(0.8,)).start()
        threading.Thread(target=create_ball, args=(1.6,)).start()



class Ball(pygame.sprite.Sprite):
    def __init__(self, game, position, damage, boss, speed=0.2, size=(64, 64)):
        self.game = game
        self.boss = boss
        pygame.sprite.Sprite.__init__(self, self.game.attacks)

        self.damage = damage
        self.speed = speed
        self.size = size

        self.images = [pygame.transform.scale(sprite, self.size) for sprite in self.game.data.ball_flying]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

        self.h_x = (game.player.rect.x - position[0]) / (11 / self.speed)
        self.h_y = (game.player.rect.y - position[1]) / (11 / self.speed)

        self.animation_loop = 1
        self.animation_pos = 0

    def update(self):
        self.animate()
        self.rect.x += self.h_x
        self.rect.y += self.h_y
        self.check_collision()

    def animate(self):
        self.animation_loop += 1
        if self.animation_loop >= 4:
            self.animation_loop = 1
            self.animation_pos += 1
            if self.animation_pos >= len(self.images):
                self.animation_pos = 0
            self.image = self.images[self.animation_pos]

    def check_collision(self):
        if pygame.sprite.collide_rect(self, self.game.player):
            room = self.game.player.get_room()
            if (
                room not in self.game.player.shield_used_rooms
                and self.game.player.has_shield
            ):
                self.game.player.shield_used_rooms.append(room)
            else:
                if (
                    not self.game.player.has_phantom
                    or random.randint(1, 5) != 1
                ):
                    self.game.player.take_damage(self.damage)
            if self.game.player.has_thornforge:
                self.boss.register_hit(self.game.player, self.damage * 0.3)
            if self.game.player.has_retaliation:
                if room not in self.game.player.retaliation_used_rooms:
                    self.game.player.retaliation_used_rooms.append(room)
                    trigger_ripple(
                        (self.game.player.x + 23, self.game.player.y + 23)
                    )
                    for enemy in self.game.enemies:
                        enemy.register_hit(self.game.player, self.damage * 5)
            self.kill()

        if (self.rect.x < 0 or self.rect.x > self.game.screen.get_width() or 
            self.rect.y < 0 or self.rect.y > self.game.screen.get_height()):
            self.kill()


class Fire(pygame.sprite.Sprite):
    def __init__(self, game, position, damage, boss, duration=5, size=(48, 48)):
        self.game = game
        self.boss = boss
        pygame.sprite.Sprite.__init__(self, self.game.attacks)

        self.damage = damage
        self.size = size
        self.duration = duration
        self.images = [pygame.transform.scale(sprite, self.size) for sprite in self.game.data.fire]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

        self.animation_loop = 1
        self.animation_pos = 0

        self.spawn_time = pygame.time.get_ticks()
        self.last_damage_time = self.spawn_time

    def update(self):
        self.animate()
        self.check_damage()
        if pygame.time.get_ticks() - self.spawn_time > self.duration * 1000:
            self.kill()

    def animate(self):
        self.animation_loop += 1
        if self.animation_loop >= 4:
            self.animation_loop = 1
            self.animation_pos += 1
            if self.animation_pos >= len(self.images):
                self.animation_pos = 0
            self.image = self.images[self.animation_pos]

    def check_damage(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time >= 1000:
            if pygame.sprite.collide_rect(self, self.game.player):
                room = self.game.player.get_room()
                if (
                    room not in self.game.player.shield_used_rooms
                    and self.game.player.has_shield
                ):
                    self.game.player.shield_used_rooms.append(room)
                else:
                    if (
                        not self.game.player.has_phantom
                        or random.randint(1, 5) != 1
                    ):
                        self.game.player.take_damage(self.damage)
                if self.game.player.has_thornforge:
                    self.boss.register_hit(self.game.player, self.damage * 0.3)
                if self.game.player.has_retaliation:
                    if room not in self.game.player.retaliation_used_rooms:
                        self.game.player.retaliation_used_rooms.append(room)
                        trigger_ripple(
                            (self.game.player.x + 23, self.game.player.y + 23)
                        )
                        for enemy in self.game.enemies:
                            enemy.register_hit(self.game.player, self.damage * 5)
            self.last_damage_time = current_time

def spawn_fires(game, boss, damage, position, duration=5, size=(48, 48)):
    player_pos = game.player.rect.center
    boss_pos = position

    direction = pygame.math.Vector2(player_pos[0] - boss_pos[0], player_pos[1] - boss_pos[1]).normalize()
    
    perpendicular = pygame.math.Vector2(-direction.y, direction.x) * TILE_SIZE

    fire_positions = []
    current_position = pygame.math.Vector2(boss_pos[0] + TILE_SIZE / 2, boss_pos[1] + TILE_SIZE / 2)
    
    while True:
        current_position += direction * TILE_SIZE
        fire_positions.append((current_position.x, current_position.y))
        fire_positions.append((current_position.x + perpendicular.x, current_position.y + perpendicular.y))
        fire_positions.append((current_position.x - perpendicular.x, current_position.y - perpendicular.y))

        if (current_position.x < 0 or current_position.x > game.screen.get_width() or 
            current_position.y < 0 or current_position.y > game.screen.get_height()):
            break

    for fire_position in fire_positions:
        fire = Fire(game, fire_position, damage, boss, duration, size)
        game.attacks.add(fire)