from sprites import *
from player_info import create_rounded_surface, ITEM_INFO_HEIGHT, ITEM_INFO_WIDTH

class Item:
    def __init__(self, name, description, price, image, attack = 0, hp = 0, defense = 0, range =0, attack_speed = 0, movement_speed = 0):
        self.name = name
        self.description = description
        self.image = image
        self.price = price
        self.attack = attack 
        self.hp = hp   
        self.defense = defense
        self.range = range
        self.attack_speed = attack_speed
        self.movement_speed = movement_speed
    
    def __str__(self):
        return f"{self.name}: {self.description}"
    


def display_shop_item(game, shop_item):
    item = shop_item.item
    screen = game.screen

    font = pygame.font.Font(None, 32)

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

    screen.blit(border_surface, ((WIN_WIDTH - border_surface.get_width()) // 2, (WIN_HEIGHT - border_surface.get_height()) // 2 - 100))

    screen.blit(rounded_surface, rounded_surface_rect)

    mouse_pos = pygame.mouse.get_pos()
    rect = button_surface.get_rect()
    rect.x = rounded_surface_rect.left + 50
    rect.y = rounded_surface_rect.top + 230
    if rect.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            if game.player.gold >= item.price:
                game.player.inventory.append(item)
                add_stats(game.player, item)
                shop_item.purchase_item(game.player)


def add_stats(player, item):
    attributes = ["attack", "hp", "defense", "range", "attack_speed", "movement_speed"]
    for attribute in attributes:
        setattr(player, attribute, getattr(player, attribute) + getattr(item, attribute))


all_items = [Item("Sentinel Aegis", "Prevents first incoming \nstrike in every room", 1500, '../resources/shield.png', defense=10, hp=30), 
             Item("Sword", "somethin", 1000, '../resources/sword.png', attack=10, hp=10, attack_speed = 0.2),
             Item("Thornforge Armor", "Damages enemies for 20% damage \ndealt to you", 2000, '../resources/thornforge.png', defense=15, movement_speed = -1),
             Item("Wings", "Allows flying over terrain", 5000, '../resources/wings.png', movement_speed = 1), #might be hard to implement
             Item("Soulthirster Blade", "Heals for 5% of damage dealt", 2500, '../resources/soulthirster.png', attack=20),
             Item("Vorpal Shard", "Gives additional 20% attack", 3000, '../resources/dagger.png', attack=20, movement_speed = 0.5),
             Item("Wyrmblade", "somethin", 2000, '../resources/wyrmblade.png', attack=15, hp=20, range = 0.2, movement_speed = - 0.5),
             Item("Guardian's Edge", "somethin", 2000, '../resources/guardians edge.png', attack=10, hp=20, defense = 10),
             Item("Arcane Halo", "Deals damage around you", 1800, '../resources/disc.png', attack=5, hp=20),
             Item("Scythe", "somethin", 2800, '../resources/sword.png', attack=35),
             Item("Healing amulet", "Heals some missing health \nafter clearing a room", 1200, '../resources/sword.png', defense=5, hp=20),
             Item("Polearm", "somethin", 2000, '../resources/sword.png', attack=20, attack_speed = 0.3, movement_speed = 0.5)
             #more defensive items
             #add space for usable items in inventory (potions etc)
             ]  
             
