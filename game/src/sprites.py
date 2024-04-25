import pygame
from config import *
import random
import math
from items import Item
from player_info import *
from items import all_items


class SpriteSheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height, scaling=0):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return pygame.transform.scale(sprite, (TILE_SIZE * scaling, TILE_SIZE * scaling)) if scaling else \
            pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))


class Player(pygame.sprite.Sprite):
    def __init__(self, game, position, start):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.player_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x, self.y = position
        self.width, self.height = TILE_SIZE, TILE_SIZE
        self.room_x, self.room_y = start
        self.x_change, self.y_change = 0, 0
        self.facing = 'down'
        self.animation_loop = 1

        self.animation_positions = {
            'up': [self.game.character_sprite_sheet.get_sprite(3, 34, 32, 32),
                   self.game.character_sprite_sheet.get_sprite(35, 34, 32, 32),
                   self.game.character_sprite_sheet.get_sprite(68, 34, 32, 32)],
            'down': [self.game.character_sprite_sheet.get_sprite(3, 2, 32, 32),
                     self.game.character_sprite_sheet.get_sprite(35, 2, 32, 32),
                     self.game.character_sprite_sheet.get_sprite(68, 2, 32, 32)],
            'right': [self.game.character_sprite_sheet.get_sprite(3, 66, 32, 32),
                      self.game.character_sprite_sheet.get_sprite(35, 66, 32, 32),
                      self.game.character_sprite_sheet.get_sprite(68, 66, 32, 32)],
            'left': [self.game.character_sprite_sheet.get_sprite(3, 98, 32, 32),
                     self.game.character_sprite_sheet.get_sprite(35, 98, 32, 32),
                     self.game.character_sprite_sheet.get_sprite(68, 98, 32, 32)]
        }

        self.image = self.game.character_sprite_sheet.get_sprite(3, 2, 32, 32)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.map_open = False
        self.map_open_pressed = False

        self.last_shooting = 1

        self.info_open = False
        self.info_open_pressed = False

        self.item_open = False
        self.item_open_pressed = False

        self.clicked_slot = None

        self.attack = 20  
        self.hp = 100     
        self.defense = 5  
        self.range = 0.5
        self.attack_speed = 1
        self.movement_speed = PLAYER_SPEED

        self.current_hp = 100
        
        self.gold = 100000 #for testing

        self.inventory = []

    def update(self):
        self.movement()
        self.animate()

        self.x += self.x_change
        self.rect.x = self.x
        self.collide_blocks('x')
        self.y += self.y_change
        self.rect.y = self.y
        self.collide_blocks('y')

        self.x_change, self.y_change = 0, 0
        self.last_shooting += 1
        if self.last_shooting > 10000:
            self.last_shooting = 1

    def movement(self):
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
        
        if mouse_buttons[0] and self.last_shooting > 20:
            Bullet(self.game, 8, pygame.mouse.get_pos())
            self.last_shooting = 1
            
        if mouse_buttons[0]:
            mouse_pos = pygame.mouse.get_pos()
            self.clicked_slot = self.get_clicked_inventory_slot(mouse_pos)
            if self.clicked_slot is not None:
                if not self.item_open_pressed:
                    self.item_open_pressed = True
                    self.item_open = not self.item_open
        else:
            self.item_open_pressed = False

    def collide_blocks(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            if direction == 'x':
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                self.x = self.rect.x
            if direction == 'y':
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                self.y = self.rect.y

    def get_room(self):
        return self.room_x, self.room_y
    
    def get_clicked_inventory_slot(self, mouse_pos):
        x, y = (WIN_WIDTH - PLAYER_INFO_WIDTH) / 2 + 20, (WIN_HEIGHT - PLAYER_INFO_HEIGHT) / 2 + 250
        for item_index, item in enumerate(self.inventory):
            item_row = item_index // GRID_WIDTH
            item_col = item_index % GRID_WIDTH
            item_x = x + (GRID_CELL_SIZE + GRID_SPACING) * item_col
            item_y = y + (GRID_CELL_SIZE + GRID_SPACING) * item_row
            
            if item_x <= mouse_pos[0] <= item_x + GRID_CELL_SIZE and item_y <= mouse_pos[1] <= item_y + GRID_CELL_SIZE:
                return item_index
        return None

    def animate(self):
        if self.x_change == 0 and self.y_change == 0:
            self.image = self.animation_positions.get(self.facing)[0]
        else:
            self.image = self.animation_positions.get(self.facing)[int(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, speed, target):
        self.game = game
        self._layer = PROPS_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x, self.y = game.player.rect.x + game.player.width/2 - 10.5, game.player.rect.y + game.player.height/2 - 12

        self.animation_loop = 1
        self.animation_position = 0

        self.angle = math.atan2(target[1] - 12 - self.y, target[0] - 10.5 - self.x)
        self.degree = -self.angle * 180 / math.pi
        self.image = pygame.transform.rotate(
            pygame.transform.scale(self.game.bullets_sprite_sheet.get_sprite(0, 0, 7, 8), (21, 24)), self.degree)
        self.rect = self.image.get_rect()
        self.dx = math.cos(self.angle) * speed
        self.dy = math.sin(self.angle) * speed

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x
        self.rect.y = self.y
        self.collide_blocks()

        self.animation_loop += 1
        if self.animation_loop >= 10:
            self.image = pygame.transform.rotate(
                pygame.transform.scale(
                    self.game.bullets_sprite_sheet.get_sprite(self.animation_position, 0, 7, 8), (21, 24)), self.degree)
            self.animation_position += 8
            if self.animation_position == 32:
                self.animation_position = 0
            self.animation_loop = 1

    def collide_blocks(self):
        if self.rect.x < 0 or self.rect.x > WIN_WIDTH or self.rect.y < 0 or self.rect.y > WIN_HEIGHT:
            self.kill()
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            # animation
            self.kill()


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, *self.groups)

        self.x, self.y = x * TILE_SIZE, y * TILE_SIZE
        self.width, self.height = TILE_SIZE, TILE_SIZE

        tmp = 16 if random.randint(1, 10) > 8 else 0
        self.image = self.game.blocks_sprite_sheet.get_sprite(tmp, 0, 16, 16)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x, self.y = x * TILE_SIZE, y * TILE_SIZE
        self.width, self.height = TILE_SIZE, TILE_SIZE

        tmp = 48 if random.randint(1, 10) > 8 else 32
        self.image = self.game.blocks_sprite_sheet.get_sprite(tmp, 16, 16, 16)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y


class CobWeb(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PROPS_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = (x + random.randint(0, 5) / 10) * TILE_SIZE
        self.y = (y + random.randint(0, 5) / 10) * TILE_SIZE
        self.width, self.height = 16, 16

        self.image = self.game.blocks_sprite_sheet.get_sprite(64, 0, 16, 16, 0.5)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y


class Button:
    def __init__(self, center, size, fg, bg, content, fontsize):
        font = pygame.font.Font('../resources/chiller.ttf', fontsize)
        text = font.render(content, True, fg)
        text_rect = text.get_rect(center=(size[0] / 2, size[1] / 2))

        self.image = pygame.Surface(size)
        self.image.fill(bg)
        self.rect = self.image.get_rect(center=center)
        self.image.blit(text, text_rect)

    def is_pressed(self, pos, pressed):
        return self.rect.collidepoint(pos) and pressed

class ShopItem(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x, self.y = x * TILE_SIZE, y * TILE_SIZE
        self.width, self.height = TILE_SIZE, TILE_SIZE

        n = len(all_items)
        x = random.randint(0, n-1)
        self.item = all_items[x]

        background_image = self.game.blocks_sprite_sheet.get_sprite(0, 0, 16, 16)

        shield_image = pygame.image.load(self.item.image)
        shield_image = pygame.transform.scale(shield_image, (TILE_SIZE, TILE_SIZE))

        combined_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        combined_image.blit(background_image, (0, 0))
        combined_image.blit(shield_image, (0, 0))

        self.image = combined_image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def is_player_near(self, player):
        distance = math.sqrt((player.rect.centerx - self.rect.centerx)**2 + (player.rect.centery - self.rect.centery)**2)
        
        return distance <= 70
    
    def purchase_item(self, player):
        if player.gold >= self.item.price:
            player.gold -= self.item.price

            new_block = Block(self.game, self.x // TILE_SIZE, self.y // TILE_SIZE)

            self.kill()

            self.game.all_sprites.add(new_block)
            self.game.blocks.add(new_block)
