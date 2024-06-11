import random

import pygame

from config import TILE_SIZE
from items import all_items
from sprites.blocks import Wall


class ShopItem(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.attacks, self.game.walls
        pygame.sprite.Sprite.__init__(self, *self.groups)

        self.item = all_items[random.randint(0, len(all_items) - 1)]

        combined_image = pygame.Surface((TILE_SIZE, TILE_SIZE)).convert()
        self.rect = combined_image.get_rect()
        self.rect.x, self.rect.y = x * TILE_SIZE, y * TILE_SIZE

        background_image = self.game.data.blocks[0]
        combined_image.blit(background_image, (0, 0))

        item_image = pygame.transform.scale(
            pygame.image.load(self.item.image), (TILE_SIZE, TILE_SIZE)
        )
        combined_image.blit(item_image, (0, 0))

        self.image = combined_image

    def is_player_near(self, player) -> bool:
        distance = (
            (player.rect.centerx - self.rect.centerx) ** 2
            + (player.rect.centery - self.rect.centery) ** 2
        ) ** 0.5
        return distance <= 70

    def purchase_item(self, player, game):
        if player.gold >= self.item.price:
            player.gold -= self.item.price
            game.items_bought += 1

            match self.item.name: 
                case "Sentinel Aegis":
                    player.has_shield = True
                case "Wings":
                    player.has_wings = True
                case "Thornforge Armor":
                    player.has_thornforge = True
                case "Wyrmblade":
                    player.has_wyrmblade = True
                case "Soulthirster Blade":
                    player.has_soulthirster = True
                case "Vorpal Shard":
                    player.has_vorpal = True
                case "Arcane Halo":
                    player.has_disc = True
                case "Healing amulet":
                    player.has_amulet = True
                case "Retaliation Raiment":
                    player.has_retaliation = True
                case "Heartguard":
                    player.has_heartguard = True
                case "Phantom boots":
                    player.has_phantom = True
                case "Scythe":
                    player.has_scythe = True
                case "Polearm":
                    player.has_polearm = True
                case "Guardian's Edge":
                    player.has_edge = True

            if player.has_vorpal and not player.boost_given:
                player.attack *= 1.2
                player.boost_given = True

            new_block = Wall(
                self.game, self.rect.x // TILE_SIZE, self.rect.y // TILE_SIZE
            )
            room = game.rooms[player.room_x][player.room_y]
            room[self.rect.y // TILE_SIZE] = (
                room[self.rect.y // TILE_SIZE][: self.rect.x // TILE_SIZE]
                + "B"
                + room[self.rect.y // TILE_SIZE][self.rect.x // TILE_SIZE + 1 :]
            )

            self.kill()

            self.game.attacks.add(new_block)
            self.game.walls.add(new_block)
