import pygame
import time
import threading
from config import WIN_WIDTH, WIN_HEIGHT
from player_info import create_rounded_surface, ITEM_INFO_HEIGHT, ITEM_INFO_WIDTH


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




def display_shop_item(game, shop_item):
    item = shop_item.item
    screen = game.screen

    font = pygame.font.Font(None, 32)

    if isinstance(item, Item):

        name_text = font.render(f"{item.name}", True, (0, 0, 0))
        font = pygame.font.Font(None, 24)
        attributes_text = [
            font.render(f"{attribute}: {getattr(item, attribute)}", True, (0, 0, 0))
            for attribute in ["attack", "hp", "defense", "range", "attack_speed", "movement_speed"]
            if getattr(item, attribute) != 0
        ]

        description_lines = item.description.split('\n')
        description_text = font.render("Description:", True, (0, 0, 0))

        item_image = pygame.image.load(item.image)
        item_image = pygame.transform.scale(item_image, (100, 100))

        rounded_surface = create_rounded_surface(ITEM_INFO_WIDTH, ITEM_INFO_HEIGHT, (153, 153, 102), radius=10)
        rounded_surface_rect = rounded_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 100))

        border_width = 5
        border_surface = create_rounded_surface(rounded_surface.get_width() + 2 * border_width,
                                                rounded_surface.get_height() + 2 * border_width,
                                                (51, 51, 0), radius=10)

        border_surface.blit(rounded_surface, (border_width, border_width))

        y_offset = 10
        rounded_surface.blit(name_text, (10, y_offset))
        y_offset += name_text.get_height() + 10

        for text in attributes_text:
            rounded_surface.blit(text, (10, y_offset))
            y_offset += text.get_height()

        y_offset = max(y_offset, 100)

        rounded_surface.blit(description_text, (10, y_offset + 10))

        y_offset += 30

        for line in description_lines:
            text_surface = font.render(line, True, (0, 0, 0))
            rounded_surface.blit(text_surface, (10, y_offset))
            y_offset += text_surface.get_height()

        button_x = (rounded_surface.get_width() - 150) + 50
        button_y = rounded_surface.get_height() - 150

        button_surface = create_rounded_surface(button_x, button_y, (0, 160, 0), radius=10)

        if game.player.gold < item.price:
            button_surface.fill((160, 0, 0))

        purchase_text = font.render(f"Purchase ({item.price} Gold)", True, (0, 0, 0))

        text_rect = purchase_text.get_rect(center=button_surface.get_rect().center)
        button_surface.blit(purchase_text, text_rect)

        screen.blit(button_surface, (rounded_surface_rect.left + 50, rounded_surface_rect.top + 230))

        rounded_surface.blit(item_image, (rounded_surface.get_width() - item_image.get_width() - 10, 10))

        screen.blit(border_surface,
                    ((WIN_WIDTH - border_surface.get_width()) // 2, (WIN_HEIGHT - border_surface.get_height()) // 2 - 100))

        screen.blit(rounded_surface, rounded_surface_rect)

    elif isinstance(item, Potion):
    
        name_text = font.render(f"{item.name}", True, (0, 0, 0))
        count_text = font.render(f"Count: {item.count}", True, (0, 0, 0))
        font = pygame.font.Font(None, 24)

        description_lines = item.description.split('\n')
        description_text = font.render("Description:", True, (0, 0, 0))

        item_image = pygame.image.load(item.image)
        item_image = pygame.transform.scale(item_image, (100, 100))

        rounded_surface = create_rounded_surface(ITEM_INFO_WIDTH, ITEM_INFO_HEIGHT, (153, 153, 102), radius=10)
        rounded_surface_rect = rounded_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 100))

        border_width = 5
        border_surface = create_rounded_surface(rounded_surface.get_width() + 2 * border_width,
                                                rounded_surface.get_height() + 2 * border_width,
                                                (51, 51, 0), radius=10)

        border_surface.blit(rounded_surface, (border_width, border_width))

        y_offset = 10
        rounded_surface.blit(name_text, (10, y_offset))
        y_offset += name_text.get_height() + 10

        rounded_surface.blit(count_text, (10, y_offset))
        y_offset += name_text.get_height() + 10

        y_offset = max(y_offset, 100)

        rounded_surface.blit(description_text, (10, y_offset + 10))

        y_offset += 30

        for line in description_lines:
            text_surface = font.render(line, True, (0, 0, 0))
            rounded_surface.blit(text_surface, (10, y_offset))
            y_offset += text_surface.get_height()

        button_x = (rounded_surface.get_width() - 150) + 50
        button_y = rounded_surface.get_height() - 150

        button_surface = create_rounded_surface(button_x, button_y, (0, 160, 0), radius=10)

        if game.player.gold < item.price:
            button_surface.fill((160, 0, 0))

        purchase_text = font.render(f"Purchase ({item.price} Gold)", True, (0, 0, 0))

        text_rect = purchase_text.get_rect(center=button_surface.get_rect().center)
        button_surface.blit(purchase_text, text_rect)

        screen.blit(button_surface, (rounded_surface_rect.left + 50, rounded_surface_rect.top + 230))

        rounded_surface.blit(item_image, (rounded_surface.get_width() - item_image.get_width() - 10, 10))

        screen.blit(border_surface, (
            (WIN_WIDTH - border_surface.get_width()) // 2, (WIN_HEIGHT - border_surface.get_height()) // 2 - 100))

        screen.blit(rounded_surface, rounded_surface_rect)


        rounded_surface.blit(item_image, (rounded_surface.get_width() - item_image.get_width() - 10, 10))

        screen.blit(border_surface,
                    ((WIN_WIDTH - border_surface.get_width()) // 2, (WIN_HEIGHT - border_surface.get_height()) // 2 - 100))

        screen.blit(rounded_surface, rounded_surface_rect)

            

    mouse_pos = pygame.mouse.get_pos()
    rect = button_surface.get_rect()
    rect.x = rounded_surface_rect.left + 50
    rect.y = rounded_surface_rect.top + 230
    if rect.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            if game.player.gold >= item.price:
                if isinstance(item, Item):
                    game.player.items.append(item)
                add_stats(game.player, item)
                shop_item.purchase_item(game.player, game)


def add_stats(player, item):
    if isinstance(item, Item):
        attributes = ["attack", "hp", "defense", "range", "attack_speed", "movement_speed"]
        if player.has_vorpal:
            player.attack = player.attack / 1.2
        for attribute in attributes:
            setattr(player, attribute, getattr(player, attribute) + getattr(item, attribute))
        if player.has_vorpal:
            player.attack = player.attack * 1.2
    elif isinstance(item, Potion):
        for potion in player.potions:
            if potion.name == item.name:
                potion.count += item.count


all_items = [Item("Sentinel Aegis", "Prevents first incoming \nstrike in every room", 1500, '../resources/shield.png',
                  defense=10, hp=30),
             Item("Sword", "Does nothing", 1000, '../resources/sword.png', attack=10, hp=10, attack_speed=0.2),
             Item("Thornforge Armor", "Damages enemies for 30% damage \ndealt to you", 2000,
                  '../resources/thornforge.png', defense=15, movement_speed=-1),
             Item("Wings", "Allows flying over terrain", 5000, '../resources/wings.png', movement_speed=1),
             Item("Soulthirster Blade", "Heals for 5% of damage dealt", 2500, '../resources/soulthirster.png',
                  attack=20),
             Item("Vorpal Shard", "Gives additional 20% attack", 3000, '../resources/dagger.png', attack=20,
                  movement_speed=0.5),
             Item("Wyrmblade", "Deals additional 5% max health \nper hit (1% to bosses)", 2000, '../resources/wyrmblade.png', attack=15, hp=20, attack_range=0.2,
                  movement_speed=- 0.5),
             Item("Guardian's Edge", "Deals more damage to enemies \nwith lower health than you", 2000, '../resources/guardians edge.png', attack=10, hp=20, defense=10),
             Item("Arcane Halo", "Deals damage around you", 1800, '../resources/disc.png', attack=5, hp=20),
             Item("Scythe", "Deals triple damage \non the first strike", 2800, '../resources/scythe.png', attack=35),
             Item("Healing amulet", "Heals some missing health \nafter killing enemy", 1200, '../resources/amulet.png',
                  defense=5, hp=20),
             Item("Polearm", "Has 30% chance to deal \ndouble damage", 2000, '../resources/polearm.png', attack=20, attack_speed=0.3,
                  movement_speed=0.5),
             Item("Retaliation Raiment", "Once per room after getting damaged \ndeals damage to all enemies", 2200,
                  '../resources/retaliation.png', hp=30),
             Item("Heartguard", "After each enemy killed \ngives you 1 HP", 3000,
                  '../resources/heartguard.png', hp=40),
             Item("Phantom boots", "Has 20% chance \nto dodge an attack", 2600,
                  '../resources/phantom.png', hp=10, defense = 10),

            
             Potion("Healing potion", '../resources/health_potion.png', 'Heals 50 HP', 5, 750, 50),
             Potion("Defence potion", '../resources/defence_potion.png', 'Gives 20 defence for 3 min', 3, 750, 20), 
             Potion("Attack potion", '../resources/attack_potion.png', 'Gives 30 attack for 3 min', 3, 750, 30), 
             Potion("Regeneration potion", '../resources/regen_potion.png', 'Restores 1 HP per secound for 1 min', 3, 750, 1)
             ]
