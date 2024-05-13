import pygame
import random
from config import TILE_SIZE
from items import all_items
from blocks import Wall


class ShopItem(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.attacks, self.game.walls
        pygame.sprite.Sprite.__init__(self, *self.groups)

        self.item = all_items[random.randint(0, len(all_items) - 1)]

        background_image = self.game.data.blocks[0]
        item_image = pygame.transform.scale(pygame.image.load(self.item.image), (TILE_SIZE, TILE_SIZE))

        combined_image = pygame.Surface((TILE_SIZE, TILE_SIZE)).convert()
        combined_image.blit(background_image, (0, 0))
        combined_image.blit(item_image, (0, 0))

        self.image = combined_image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * TILE_SIZE, y * TILE_SIZE

    def is_player_near(self, player):
        distance = ((player.rect.centerx - self.rect.centerx) ** 2 +
                    (player.rect.centery - self.rect.centery) ** 2) ** 0.5

        return distance <= 70

    def purchase_item(self, player, game):
        if player.gold >= self.item.price:
            player.gold -= self.item.price

            if self.item.name == "Sentinel Aegis":
                player.has_shield = True

            if self.item.name == "Wings":
                player.has_wings = True

            if self.item.name == "Thornforge Armor":
                player.has_thornforge = True

            if self.item.name == "Wyrmblade":
                player.has_wyrmblade = True

            if self.item.name == "Soulthirster Blade":
                player.has_soulthirster = True

            if self.item.name == "Vorpal Shard":
                player.has_vorpal = True

            if self.item.name == "Arcane Halo":
                player.has_disc = True

            if self.item.name == "Healing amulet":
                player.has_amulet = True

            if self.item.name == "Retaliation Raiment":
                player.has_retaliation = True

            if self.item.name == "Heartguard":
                player.has_heartguard = True

            if self.item.name == "Phantom boots":
                player.has_phantom = True

            if player.has_vorpal and not player.boost_given:
                player.attack = player.attack * 1.2
                player.boost_given = True

            new_block = Wall(self.game, self.rect.x // TILE_SIZE, self.rect.y // TILE_SIZE)
            x, y = player.room_x, player.room_y
            room = game.rooms[x][y]
            room[self.rect.y // TILE_SIZE] = room[self.rect.y // TILE_SIZE][:self.rect.x // TILE_SIZE] + "B" +  room[self.rect.y // TILE_SIZE][self.rect.x // TILE_SIZE + 1:]

            self.kill()

            self.game.attacks.add(new_block)
            self.game.walls.add(new_block)
