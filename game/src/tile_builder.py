import random

from config import *
from map import update_map
from sprites.blocks import CobWeb, Ground, Wall
from sprites.enemies import Spider
from sprites.shopItem import ShopItem


def build_tile(game, tile: list[list[int]]) -> None:
    for i, row in enumerate(tile):
        for j, elem in enumerate(row):
            if elem == ".":
                Ground(game, j, i)
            elif elem == "B" or elem == "P":
                Wall(game, j, i)
            elif elem == "I":
                ShopItem(game, j, i)
            elif elem == "M":
                Ground(game, j, i)
                Spider(game, (j * TILE_SIZE, i * TILE_SIZE))
            if random.randint(1, 10) > 9 and elem != "I":
                CobWeb(game, j, i)


def tile_to_change(game) -> None:

    def change_tile(
        tile_before: list[list[int]], room_x: int, room_y: int, x: int, y: int
    ) -> None:
        game.enemies.empty()
        game.ground.empty()
        game.walls.empty()
        game.attacks.empty()
        game.player.room_x += room_x
        game.player.room_y += room_y
        after = game.player.get_room()
        game.player.x = x
        game.player.rect.x = x
        game.player.y = y
        game.player.rect.y = y
        build_tile(game, game.rooms[after[0]][after[1]])
        update_map(game, tile_before, after)

    if game.player.rect.y > WIN_HEIGHT:  # go down
        before = game.player.get_room()
        change_tile(before, 1, 0, game.player.rect.x, -TILE_SIZE)

    elif game.player.rect.y < -TILE_SIZE:  # go up
        before = game.player.get_room()
        change_tile(before, -1, 0, game.player.rect.x, WIN_HEIGHT)

    elif game.player.rect.x < -TILE_SIZE:  # go left
        before = game.player.get_room()
        change_tile(before, 0, -1, WIN_WIDTH, game.player.rect.y)

    elif game.player.rect.x > WIN_WIDTH:  # go right
        before = game.player.get_room()
        change_tile(before, 0, 1, -TILE_SIZE, game.player.rect.y)
