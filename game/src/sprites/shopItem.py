import pygame
import random
from src.config import TILE_SIZE
from src.items import all_items
from src.sprites.blocks import Wall


class ShopItem(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.attacks, self.game.walls
        pygame.sprite.Sprite.__init__(self, *self.groups)

        self.item = all_items[random.randint(0, len(all_items) - 1)]

        background_image = self.game.data.blocks[0]
        shield_image = pygame.transform.scale(pygame.image.load(self.item.image), (TILE_SIZE, TILE_SIZE))

        combined_image = pygame.Surface((TILE_SIZE, TILE_SIZE)).convert()
        combined_image.blit(background_image, (0, 0))
        combined_image.blit(shield_image, (0, 0))

        self.image = combined_image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * TILE_SIZE, y * TILE_SIZE

    def is_player_near(self, player):
        distance = ((player.rect.centerx - self.rect.centerx) ** 2 +
                    (player.rect.centery - self.rect.centery) ** 2) ** 0.5

        return distance <= 70

    def purchase_item(self, player):
        if player.gold >= self.item.price:
            player.gold -= self.item.price

            new_block = Wall(self.game, self.rect.x // TILE_SIZE, self.rect.y // TILE_SIZE)

            self.kill()

            self.game.attacks.add(new_block)
            self.game.walls.add(new_block)
