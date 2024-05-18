import time
import threading
import json
from config import ITEMS_DATA, POTION_DATA


class Item:
    def __init__(self, name, description, price, image, attack: float = 0, hp=0, defense=0,
                 attack_range: float = 0, attack_speed: float = 0, movement_speed: float = 0):
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

    @staticmethod
    def from_dict(data):
        return Item(
            name=data['name'],
            description=data['description'],
            image=data['image'],
            price=data['price'],
            attack=data['attack'],
            hp=data['hp'],
            defense=data['defense'],
            attack_range=data['range'],
            attack_speed=data['attack_speed'],
            movement_speed=data['movement_speed']
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

    @staticmethod
    def from_dict(data):
        return Potion(
            name=data['name'],
            description=data['description'],
            image=data['image'],
            count=data['count'],
            price=data['price'],
            stat=data['stat']
        )

    @staticmethod
    def from_dict_to_player_on_start(data):
        return Potion(
            name=data['name'],
            description=data['description'],
            image=data['image'],
            count=data['start_count'],
            price=0,
            stat=data['stat']
        )

    def use(self, player):
        self.count -= 1
        if self.name == "Healing potion":
            player.current_hp = min(player.current_hp + self.stat, player.hp)
        elif self.name == "Defence potion":
            player.defense += self.stat

            def remove_def():
                time.sleep(180)
                player.defense -= self.stat

            threading.Thread(target=remove_def).start()

        elif self.name == "Attack potion":
            player.attack += self.stat

            def remove_atk():
                time.sleep(180)
                player.attack -= self.stat

            threading.Thread(target=remove_atk).start()

        elif self.name == "Regeneration potion":
            def regenerate():
                for _ in range(60):
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
