import math
from config import *
from props import Bullet, Attack
from player_info import *
from other import defence
from items import Potion

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
        self.width, self.height = self.rect.size

        self.map_open = False
        self.map_open_pressed = False

        self.last_shooting = 1

        self.info_open = False
        self.info_open_pressed = False

        self.item_open = False
        self.item_open_pressed = False

        self.previous_mouse_pressed = False

        self.clicked_slot = None

        self.attack = 20
        self.hp = 100
        self.defense = 5
        self.range = 0.5
        self.attack_speed = 1
        self.movement_speed = PLAYER_SPEED

        self.current_hp = 100

        self.gold = 100000  # for testing

        self.items = []
        self.potions = [Potion("Healing potion", '../resources/health_potion.png', 'Heals 20 HP', 5, 100, 20)]

        self.has_heartguard = False
        self.has_wings = False
        self.has_vorpal = False
        self.has_thornforge = False
        self.has_retaliation = False
        self.retaliation_used_rooms = []
        self.has_phantom = False
        self.has_shield = False
        self.shield_used_rooms = []
        self.has_soulthirster = False
        self.has_disc = False
        self.has_amulet = False
        self.has_wyrmblade = False
        self.has_scythe = False
        self.scythe_used_on = []
        self.has_polearm = False
        self.has_edge = False

        self.boost_given = False


    def update(self):
        self.interaction()
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

    def interaction(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.y_change -= self.movement_speed
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += self.movement_speed
            self.facing = 'down'
        if keys[pygame.K_RIGHT]:
            self.x_change += self.movement_speed
            self.facing = 'right'
        if keys[pygame.K_LEFT]:
            self.x_change -= self.movement_speed
            self.facing = 'left'

        if self.x_change != 0 and self.y_change != 0:
            self.x_change /= math.sqrt(2)
            self.y_change /= math.sqrt(2)

        if keys[pygame.K_m] and not self.map_open_pressed:
            self.map_open_pressed = True
            self.map_open = not self.map_open
        elif not keys[pygame.K_m]:
            self.map_open_pressed = False

        if keys[pygame.K_TAB] and not self.info_open_pressed:
            self.info_open_pressed = True
            self.info_open = not self.info_open
        elif not keys[pygame.K_TAB]:
            self.info_open_pressed = False

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if mouse_buttons[0] and self.last_shooting > 20:
            Bullet(self.game, 8, pygame.mouse.get_pos())
            self.last_shooting = 1

        if self.previous_mouse_pressed:
            self.clicked_slot = self.get_clicked_inventory_slot(mouse_pos)
            if self.clicked_slot is not None:
                if not self.item_open_pressed:
                    self.item_open_pressed = True
                    self.item_open = not self.item_open
        else:
            self.item_open_pressed = False

        if keys[pygame.K_SPACE] and self.last_shooting > 20:
            Attack(self.game, self.rect.x, self.rect.y)
            self.last_shooting = 1

        self.previous_mouse_pressed = mouse_buttons[0]

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
        self.current_hp -= (damage * (1 - defence(self.defense)))
        if self.current_hp <= 0:
            self.game.playing = False

    def get_clicked_inventory_slot(self, mouse_pos):
        x, y = (WIN_WIDTH - PLAYER_INFO_WIDTH) / 2 + 20, (WIN_HEIGHT - PLAYER_INFO_HEIGHT) / 2 + 250

        for item_index in range(24):
            item_row = item_index // 8
            item_col = item_index % 8
            item_x = x + (GRID_CELL_SIZE + GRID_SPACING) * item_col
            item_y = y + (GRID_CELL_SIZE + GRID_SPACING) * item_row

            if item_x <= mouse_pos[0] <= item_x + GRID_CELL_SIZE and item_y <= mouse_pos[1] <= item_y + GRID_CELL_SIZE:
                return item_index

        for item_index in range(24, 30):
            item_row = (item_index - 24) // 2
            item_col = (item_index - 24) % 2 + 8
            item_x = x + (GRID_CELL_SIZE + GRID_SPACING) * item_col
            item_y = y + (GRID_CELL_SIZE + GRID_SPACING) * item_row

            if item_x <= mouse_pos[0] <= item_x + GRID_CELL_SIZE and item_y <= mouse_pos[1] <= item_y + GRID_CELL_SIZE:
                return item_index

        return None


def collide_blocks(sprite, direction):
    has_wings = getattr(sprite, 'has_wings', False)

    if has_wings:
        if (sprite.rect.x < TILE_SIZE or sprite.rect.right > WIN_WIDTH - TILE_SIZE or
                sprite.rect.y < TILE_SIZE or sprite.rect.bottom > WIN_HEIGHT - TILE_SIZE):
            handle_collision(sprite, direction)
    else:
        handle_collision(sprite, direction)


def handle_collision(sprite, direction):
    hits = pygame.sprite.spritecollide(sprite, sprite.game.walls, False)
    if hits:
        if direction == 'x':
            if sprite.x_change > 0:
                sprite.rect.x = hits[0].rect.left - sprite.rect.width
            elif sprite.x_change < 0:
                sprite.rect.x = hits[0].rect.right
            sprite.x = sprite.rect.x
        elif direction == 'y':
            if sprite.y_change > 0:
                sprite.rect.y = hits[0].rect.top - sprite.rect.height
            elif sprite.y_change < 0:
                sprite.rect.y = hits[0].rect.bottom
            sprite.y = sprite.rect.y
