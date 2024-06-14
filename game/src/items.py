import json
import threading
import time

import pygame
from config import GRID_CELL_SIZE, ITEMS_DATA, POTION_DATA


class Item:
    def __init__(
        self,
        name,
        description,
        price,
        image,
        attack: float = 0,
        hp=0,
        defense=0,
        attack_range: float = 0,
        attack_speed: float = 0,
        movement_speed: float = 0,
    ):
        self.name = name
        self.description = description
        self.image = image
        self.price = price
        self.attack = attack
        self.hp = hp
        self.defense = defense
        self.range = attack_range
        self.attack_speed = attack_speed
        self.movement_speed = movement_speed
        self.ready_image = None

    @staticmethod
    def from_dict(data):
        return Item(
            name=data["name"],
            description=data["description"],
            image=data["image"],
            price=data["price"],
            attack=data["attack"],
            hp=data["hp"],
            defense=data["defense"],
            attack_range=data["range"],
            attack_speed=data["attack_speed"],
            movement_speed=data["movement_speed"],
        )

    def __str__(self):
        return f"{self.name}: {self.description}"


class Potion:
    def __init__(self, name, image, description, count, price, stat):
        self.name = name
        self.description = description
        self.image = image
        self.count = count
        self.price = price
        self.stat = stat
        self.ready_image = None

    @staticmethod
    def from_dict(data):
        return Potion(
            name=data["name"],
            description=data["description"],
            image=data["image"],
            count=data["count"],
            price=data["price"],
            stat=data["stat"],
        )

    @staticmethod
    def from_dict_to_player_on_start(data):
        potion = Potion(
            name=data["name"],
            description=data["description"],
            image=data["image"],
            count=data["start_count"],
            price=0,
            stat=data["stat"],
        )
        potion.ready_image = pygame.transform.scale(
            pygame.image.load(potion.image), (GRID_CELL_SIZE, GRID_CELL_SIZE)
        )
        return potion

    def use(self, player):
        self.count -= 1
        player.game.potions_used += 1
        match self.name:

            case "Healing potion":
                player.game.healing += min(self.stat, player.hp - player.current_hp)
                player.current_hp = min(player.current_hp + self.stat, player.hp)

            case "Defence potion":
                def remove_def():
                    time.sleep(180)
                    player.defense -= self.stat

                player.defense += self.stat
                threading.Thread(target=remove_def).start()

            case "Attack potion":
                def remove_atk():
                    time.sleep(180)
                    player.attack -= self.stat

                player.attack += self.stat
                threading.Thread(target=remove_atk).start()

            case "Regeneration potion":
                def regenerate():
                    for _ in range(60):
                        if player.current_hp < player.hp:
                            player.game.healing += self.stat
                        player.current_hp = min(player.current_hp + self.stat, player.hp)
                        time.sleep(1)

                threading.Thread(target=regenerate).start()


all_items = []

items = json.load(open(ITEMS_DATA))
for i in range(len(items)):
    all_items.append(Item.from_dict(items[i]))

potions = json.load(open(POTION_DATA))
for i in range(len(potions)):
    all_items.append(Potion.from_dict(potions[i]))
