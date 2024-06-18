import random
import threading
import time
import pygame
from enum import Enum

from player_info import trigger_ripple
from sprites.player import handle_collision
from config import TILE_SIZE, WIN_WIDTH
from sprites.blocks import Ground


def register_hit(enemy, player, damage: float):
    if player.has_scythe and enemy not in player.scythe_used_on:
        player.scythe_used_on.append(enemy)
        damage *= 3
    if player.has_polearm and random.randint(1, 10) < 4:
        damage *= 2
    if player.has_edge and player.current_hp > enemy.health:
        damage *= 1.25
    if player.has_wyrmblade:
        damage += enemy.health / 20
    if player.has_soulthirster:
        player.current_hp = min(player.hp, player.current_hp + damage / 20)

    enemy.health -= damage
    enemy.game.damage_dealt += damage

    if enemy.health <= 0:
        enemy.register_death()
        enemy.game.enemies_killed += 1
        enemy.game.player.gold += enemy.game.data.spider.get("gold")
        enemy.game.gold_earned += enemy.game.data.spider.get("gold")
        if player.has_heartguard:
            player.hp += 1
        if player.has_amulet:
            player.current_hp = min(player.hp, player.current_hp + 10)


def draw_enemy(enemy, surface: pygame.Surface):
    if enemy.health != enemy.start_health:
        new_width: int = enemy.rect.width * (enemy.health / enemy.start_health)
        pygame.draw.rect(surface, (180, 0, 0), (enemy.rect.x, enemy.rect.y - 8, enemy.rect.width, 8))
        pygame.draw.rect(surface, (0, 180, 0), (enemy.rect.x, enemy.rect.y - 8, new_width, 8))
    surface.blit(enemy.image, enemy.rect, None, 0)


def register_movement(enemy, collision):
    enemy.x += enemy.x_change
    enemy.rect.x = enemy.x
    if collision:
        handle_collision(enemy, "x")
    enemy.y += enemy.y_change
    enemy.rect.y = enemy.y
    if collision:
        handle_collision(enemy, "y")
    enemy.x_change, enemy.y_change = 0, 0


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
                self.game.data.spider.get("start_health") * self.game.difficulty
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

        register_movement(self, collision=True)

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

    def register_hit(self, player, damage: float):
        register_hit(self, player, damage)

    def register_death(self):
        self.kill()

    def draw(self, surface: pygame.Surface):
        draw_enemy(self, surface)

    def calculate_distance(self) -> bool:
        """Returns True if the player is near a spider"""
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
                    self.animation_pos = 0
                    self.damage_cooldown = 1
                    self.shooting = False
                    return
                self.image = self.game.data.spider.get("attacking")[self.animation_pos] if self.facing == "left" else \
                    pygame.transform.flip(self.game.data.spider.get("attacking")[self.animation_pos], True, False)
        elif (self.x_change == 0 and self.y_change == 0) or self.damage_cooldown < 120:
            if self.animation_loop >= 10:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos >= len(self.game.data.spider.get("standing")):
                    self.animation_pos = 0
            length = len(self.game.data.spider.get("standing"))
            self.image = self.game.data.spider.get("standing")[self.animation_pos % length] if self.facing == "left" else \
                pygame.transform.flip(self.game.data.spider.get("standing")[self.animation_pos % length], True, False)
        else:
            if self.animation_loop >= 10:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos >= len(self.game.data.spider.get("walking")):
                    self.animation_pos = 0
                self.image = self.game.data.spider.get("walking")[self.animation_pos] if self.facing == "left" else \
                    pygame.transform.flip(self.game.data.spider.get("walking")[self.animation_pos], True, False)


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
        self.start_health = self.game.data.boss.get("start_health") * self.game.difficulty
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

            register_movement(self, collision=False)
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

    def register_hit(self, player, damage: float):
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
            player.game.healing += min(player.hp - player.current_hp, damage / 20)
            player.current_hp = min(player.hp, player.current_hp + damage / 20)

        self.health -= damage
        self.game.damage_dealt += damage

        if self.health <= 0 and not self.is_dead:
            self.is_dead = True
            self.game.enemies_killed += 1
            self.animation_loop = 1
            self.animation_pos = 0

            if player.has_heartguard:
                player.hp += 1
            if player.has_amulet:
                player.game.healing += min(player.hp - player.current_hp, 10)
                player.current_hp = min(player.hp, player.current_hp + 10)

    def draw(self, surface: pygame.Surface):
        draw_enemy(self, surface)

    def calculate_distance(self) -> bool:
        """Returns True if the player is near a boss"""
        distance = (
                           (self.game.player.rect.centerx - self.rect.centerx) ** 2
                           + (self.game.player.rect.centery - self.rect.centery) ** 2
                   ) ** 0.5
        return distance < 500

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
                    x = random.randint(0, 2)
                    if x == 0:
                        spawn_fires(self.game, self, self.damage, (self.rect.centerx, self.rect.centery))
                    elif x == 1:
                        Ball(self.game, (self.x + 32, self.y + 32), self.damage, self)
                        self.spawn_balls()
                    else:
                        self.health = min(self.start_health, self.health + self.start_health / 5)
                        trigger_multiple_ripples((self.rect.centerx, self.rect.centery))
                        self.game.player.take_damage(self.game.player.hp / 10)
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
                self.game.show_statistics_screen()
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

        self.damage = damage * 5
        self.speed = speed
        self.size = size

        try:
            self.images = [pygame.transform.scale(sprite, self.size) for sprite in self.game.data.ball_flying]
            self.image = self.images[0]
        except Exception as e:
            print(f"Error loading Ball images: {e}")
            self.images = []
            self.image = pygame.Surface(self.size)

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
        try:
            self.animation_loop += 1
            if self.animation_loop >= 4:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos >= len(self.images):
                    self.animation_pos = 0
                self.image = self.images[self.animation_pos]
        except AttributeError:
            pass

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
        super().__init__()
        self.game = game
        self.boss = boss
        pygame.sprite.Sprite.__init__(self, self.game.ground)

        self.damage = damage
        self.size = size
        self.duration = duration

        try:
            self.images = [pygame.transform.scale(sprite, self.size) for sprite in self.game.data.fire]
            self.image = self.images[0]
        except Exception as e:
            print(f"Error loading Fire images: {e}")
            self.images = []
            self.image = pygame.Surface(self.size)

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
        try:
            self.animation_loop += 1
            if self.animation_loop >= 4:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos >= len(self.images):
                    self.animation_pos = 0
                self.image = self.images[self.animation_pos]
        except AttributeError:
            pass

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


def spawn_fires(game, boss: Boss, damage: float, position: tuple[int, int], duration=5, size=(48, 48)):
    player_pos = game.player.rect.center
    boss_pos = position

    direction = pygame.math.Vector2(player_pos[0] - boss_pos[0], player_pos[1] - boss_pos[1]).normalize()

    opposite_direction = -direction

    perpendicular = pygame.math.Vector2(-direction.y, direction.x) * TILE_SIZE

    fire_positions = generate_fire_positions(boss_pos, direction, perpendicular, game)

    opposite_fire_positions = generate_fire_positions(boss_pos, opposite_direction, perpendicular, game)

    positions = fire_positions + opposite_fire_positions
    for index, fire_position in enumerate(positions):
        threading.Thread(target=create_fire,
                         args=(game, fire_position, damage, boss, duration, size, index * 0.02)).start()


def generate_fire_positions(
        start_pos: tuple[int, int],
        direction: pygame.math.Vector2,
        perpendicular: pygame.math.Vector2,
        game
) -> list[tuple[float, float]]:
    fire_positions = []
    current_position = pygame.math.Vector2(start_pos[0] + TILE_SIZE / 2, start_pos[1] + TILE_SIZE / 2)

    fire_positions.append((current_position.x, current_position.y))
    fire_positions.append((current_position.x + perpendicular.x, current_position.y + perpendicular.y))
    fire_positions.append((current_position.x - perpendicular.x, current_position.y - perpendicular.y))

    while True:
        current_position += direction * TILE_SIZE
        fire_positions.append((current_position.x, current_position.y))
        fire_positions.append((current_position.x + perpendicular.x, current_position.y + perpendicular.y))
        fire_positions.append((current_position.x - perpendicular.x, current_position.y - perpendicular.y))

        if (current_position.x < 0 or current_position.x > game.screen.get_width() or
                current_position.y < 0 or current_position.y > game.screen.get_height()):
            break

    return fire_positions


def create_fire(game, position: tuple[int, int], damage: float, boss: Boss, duration: int, size: tuple[int, int],
                delay: float):
    time.sleep(delay)
    fire = Fire(game, position, damage, boss, duration, size)
    game.ground.add(fire)


ripples = []


def trigger_ripple(center: tuple[int, int], delay=0.):
    def create_ripple():
        time.sleep(delay)
        ripples.append([center, 0, 255])

    threading.Thread(target=create_ripple).start()


def draw_ripples_boss(game):
    for ripple in ripples[:]:
        _, radius, alpha = ripple
        if alpha <= 0:
            ripples.remove(ripple)
            continue
        new_radius = radius + 10
        new_alpha = max(alpha - 4, 0)
        surface = pygame.Surface((new_radius * 2, new_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            surface, (255, 165, 0, new_alpha), (new_radius, new_radius), new_radius
        )
        surface_rect = surface.get_rect(center=ripple[0])
        game.screen.blit(surface, surface_rect)
        ripple[1] = new_radius
        ripple[2] = new_alpha


def trigger_multiple_ripples(center: tuple[int, int]):
    for i in range(3):
        trigger_ripple(center, delay=i * 0.1)


class EnemyState(Enum):
    STANDING = 0
    WALKING = 1
    ATTACKING = 2
    DYING = 3

    def get_name(self) -> str:
        return self.name.lower()


class BlueBlob(pygame.sprite.Sprite):
    def __init__(self, game, position):
        self.game = game
        self.x, self.y = position
        pygame.sprite.Sprite.__init__(self, self.game.enemies)

        self.data: dict = self.game.data.blue_blob
        self.image = self.data.get("walking")[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.x_change, self.y_change = 0, 0
        self.start_health = self.data.get("start_health") * self.game.difficulty
        self.health = self.start_health
        self.facing = "right"

        self.damage = self.data.get("damage") * self.game.difficulty
        self.damage_cooldown = 0

        self.animation_loop = 1
        self.animation_pos = 0
        self.animation_frequency = 10

        self.state = EnemyState.WALKING

    def register_hit(self, player, damage: float):
        if not self.state == EnemyState.DYING:
            register_hit(self, player, damage)

    def register_death(self):
        self.state = EnemyState.DYING
        self.animation_pos = 0
        self.animation_frequency = 2

    def draw(self, surface: pygame.Surface):
        draw_enemy(self, surface)

    def update(self):
        if self.state == EnemyState.WALKING:
            self.move()
        self.attack()
        self.animate()

        register_movement(self, collision=False)

    def move(self):
        player_pos = self.game.player.rect.x, self.game.player.rect.y
        spd = 0.8
        self.x_change += (spd if player_pos[0] > self.rect.x else -spd if player_pos[0] < self.rect.x else 0)
        self.y_change += (spd if player_pos[1] > self.rect.y else -spd if player_pos[1] < self.rect.y else 0)
        if self.x_change < 0:
            self.facing = "left"
        elif self.x_change > 0:
            self.facing = "right"
        self.x_change *= random.randint(5, 15) / 10
        self.y_change *= random.randint(5, 15) / 10

    def attack(self):
        self.damage_cooldown += 1
        if self.rect.colliderect(self.game.player) and self.damage_cooldown > 60:
            self.state = EnemyState.ATTACKING
            self.animation_pos = 0
            self.damage_cooldown = 1

    def animate(self):
        if self.animation_loop < self.animation_frequency:
            self.animation_loop += 1
        else:
            self.animation_loop = 1
            self.animation_pos += 1
            if self.animation_pos >= len(self.data.get(self.state.get_name())):
                self.animation_pos = 0
                if self.state == EnemyState.DYING:
                    self.kill()
                    return
                elif self.state == EnemyState.ATTACKING:
                    self.game.player.take_damage(self.damage)
                    self.state = EnemyState.WALKING
            self.image = self.data.get(self.state.get_name())[self.animation_pos] if self.facing == "right" \
                else pygame.transform.flip(self.data.get(self.state.get_name())[self.animation_pos], True, False)


class RedDevil(pygame.sprite.Sprite):
    def __init__(self, game, position: tuple[int, int]):
        self.game = game
        self.x, self.y = position
        pygame.sprite.Sprite.__init__(self, self.game.enemies)

        self.data: dict = self.game.data.red_devil
        self.image = self.data.get("standing")[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.x_change, self.y_change = 0, 0
        self.start_health = self.data.get("start_health") * self.game.difficulty
        self.health = self.start_health
        self.facing = "right"

        self.damage = self.data.get("damage") * self.game.difficulty
        self.damage_cooldown = 121

        self.animation_loop = 1
        self.animation_pos = 0
        self.animation_frequency = 10

        self.state = EnemyState.STANDING

    def register_hit(self, player, damage: float):
        if not self.state == EnemyState.DYING:
            register_hit(self, player, damage)

    def register_death(self):
        self.state = EnemyState.DYING
        self.animation_pos = 0

    def draw(self, surface: pygame.Surface):
        draw_enemy(self, surface)

    def update(self):
        if self.state != EnemyState.DYING:
            is_near_player = self.near_player((self.game.player.rect.x, self.game.player.rect.y))
            player_pos = self.game.player.rect.x, self.game.player.rect.y
            if not is_near_player and self.state != EnemyState.ATTACKING and self.damage_cooldown > 120:
                if self.state != EnemyState.WALKING:
                    self.state = EnemyState.WALKING
                    self.animation_pos = 0
                self.move(player_pos)
            self.facing = "right" if player_pos[0] > self.rect.x else "left"

            register_movement(self, collision=True)

            self.attack(is_near_player)

        self.animate()

    def move(self, player_pos: tuple[int, int]):
        spd = 1.2
        x_distance = abs(player_pos[0] - self.rect.x)
        if x_distance > TILE_SIZE * 2:
            self.x_change += (spd if player_pos[0] > self.rect.x else -spd if player_pos[0] < self.rect.x else 0)
            self.x_change *= random.randint(5, 15) / 10
        self.y_change += (spd if player_pos[1] > self.rect.y else -spd if player_pos[1] < self.rect.y else 0)
        self.y_change *= random.randint(5, 15) / 10

    def near_player(self, player_pos) -> bool:
        return abs(player_pos[0] - self.rect.x) <= 4 * TILE_SIZE and abs(player_pos[1] - self.rect.y) <= 0.3 * TILE_SIZE

    def attack(self, is_near_player):
        self.damage_cooldown += 1
        if is_near_player and self.damage_cooldown > 120:
            self.state = EnemyState.ATTACKING
            self.animation_pos = 0
            self.damage_cooldown = 1
            Projectile(self.game, self.facing, self.rect.center, self.damage)

    def animate(self):
        if self.animation_loop < self.animation_frequency:
            self.animation_loop += 1
        else:
            self.animation_loop = 1
            self.animation_pos += 1
            if self.animation_pos >= len(self.data.get(self.state.get_name())):
                self.animation_pos = 0
                if self.state == EnemyState.DYING:
                    self.kill()
                    return
                elif self.state == EnemyState.ATTACKING:
                    self.state = EnemyState.STANDING
            self.image = self.data.get(self.state.get_name())[self.animation_pos] if self.facing == "right" \
                else pygame.transform.flip(self.data.get(self.state.get_name())[self.animation_pos], True, False)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, direction, position, damage):
        self.game = game
        pygame.sprite.Sprite.__init__(self, game.enemies)
        self.direction = direction
        self.position = position
        self.damage = damage
        self.images = self.game.data.red_devil.get("bullet")
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.width = 3
        self.rect.height = 3
        self.rect.x = position[0]
        self.rect.y = position[1]

        self.animation_pos = 0
        self.animation_loop = 1

        self.exploding = False

    def update(self):
        self.animation_loop += 1
        if not self.exploding:
            self.rect.x += 3 if self.direction == "right" else -3
            if self.animation_loop > 10:
                self.animation_loop = 1
                self.animation_pos += 1
                if self.animation_pos >= 5:
                    self.animation_pos = 3
                self.image = self.images[self.animation_pos] if self.direction == "right" \
                    else pygame.transform.flip(self.images[self.animation_pos], True, False)
            if pygame.sprite.collide_rect(self, self.game.player):
                self.game.player.take_damage(self.damage)
                self.explode()
            if self.rect.x < 0 or self.rect.x > self.game.screen.get_width():
                self.kill()
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if hits[0].breakable:
                    hits[0].kill()
                    Ground(self.game, hits[0].rect.x // TILE_SIZE, hits[0].rect.y // TILE_SIZE)
                self.explode()
        else:
            if self.animation_loop > 10:
                if self.animation_pos >= 7:
                    self.kill()
                    return
                self.image = self.images[6] if self.direction == "right" \
                    else pygame.transform.flip(self.images[6], True, False)
                self.animation_loop = 1
                self.animation_pos += 1

    def explode(self):
        self.exploding = True
        self.animation_loop = 1
        self.image = self.images[5] if self.direction == "right" \
            else pygame.transform.flip(self.images[5], True, False)
        self.animation_pos = 6

    def draw(self, surface: pygame.Surface):
        position = [self.rect.x, self.rect.y - self.image.get_rect().height // 2 + 1]
        if self.direction == "right":
            position[0] += 3 - self.image.get_rect().width
        surface.blit(self.image, position, None, 0)

    def register_hit(self, player, damage):
        self.kill()
