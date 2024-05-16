import pygame
from game.src.items import Item, Potion
from config import WIN_WIDTH, WIN_HEIGHT
from player_info import create_rounded_surface, ITEM_INFO_HEIGHT, ITEM_INFO_WIDTH


def display_shop_item(game_, shop_item):
    item = shop_item.item
    screen = game_.screen

    font = pygame.font.Font(None, 32)

    name_text = font.render(f"{item.name}", True, (0, 0, 0))
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

    button_surface = None

    if isinstance(item, Item):

        attributes_text = [
            font.render(f"{attribute}: {getattr(item, attribute)}", True, (0, 0, 0))
            for attribute in ["attack", "hp", "defense", "range", "attack_speed", "movement_speed"]
            if getattr(item, attribute) != 0
        ]

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

        if game_.player.gold < item.price:
            button_surface.fill((160, 0, 0))

        purchase_text = font.render(f"Purchase ({item.price} Gold)", True, (0, 0, 0))

        text_rect = purchase_text.get_rect(center=button_surface.get_rect().center)
        button_surface.blit(purchase_text, text_rect)

        screen.blit(button_surface, (rounded_surface_rect.left + 50, rounded_surface_rect.top + 230))

        rounded_surface.blit(item_image, (rounded_surface.get_width() - item_image.get_width() - 10, 10))

        screen.blit(border_surface,
                    ((WIN_WIDTH - border_surface.get_width()) // 2,
                     (WIN_HEIGHT - border_surface.get_height()) // 2 - 100))

        screen.blit(rounded_surface, rounded_surface_rect)

    elif isinstance(item, Potion):
        count_text = font.render(f"Count: {item.count}", True, (0, 0, 0))

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

        if game_.player.gold < item.price:
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
                    ((WIN_WIDTH - border_surface.get_width()) // 2,
                     (WIN_HEIGHT - border_surface.get_height()) // 2 - 100))

        screen.blit(rounded_surface, rounded_surface_rect)

    mouse_pos = pygame.mouse.get_pos()
    rect = button_surface.get_rect()
    rect.x = rounded_surface_rect.left + 50
    rect.y = rounded_surface_rect.top + 230
    if rect.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            if game_.player.gold >= item.price:
                if isinstance(item, Item):
                    game_.player.items.append(item)
                add_stats(game_.player, item)
                shop_item.purchase_item(game_.player, game_)


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