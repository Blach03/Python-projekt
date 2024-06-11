import pygame
from config import WIN_HEIGHT, WIN_WIDTH
from player_info import (ITEM_INFO_HEIGHT, ITEM_INFO_WIDTH,
                         create_rounded_surface)

from items import Item, Potion


def load_font(size: int):
    return pygame.font.Font(None, size)

def render_text(font, text: str, color):
    return font.render(text, True, color)

def load_and_scale_image(image_path, size):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, size)

def draw_item_attributes(font, surface: pygame.Surface, item: Item, y_offset: int) -> int:
    attributes = ["attack", "hp", "defense", "range", "attack_speed", "movement_speed"]
    for attribute in attributes:
        if getattr(item, attribute) != 0:
            text = render_text(font, f"{attribute}: {getattr(item, attribute)}", (0, 0, 0))
            surface.blit(text, (10, y_offset))
            y_offset += text.get_height()
    return y_offset

def draw_description(font, surface: pygame.Surface, description_lines: list[str], y_offset: int) -> int:
    description_text = render_text(font, "Description:", (0, 0, 0))
    surface.blit(description_text, (10, y_offset + 10))
    y_offset += 30
    for line in description_lines:
        text_surface = render_text(font, line, (0, 0, 0))
        surface.blit(text_surface, (10, y_offset))
        y_offset += text_surface.get_height()
    return y_offset

def create_button_surface(font, item: Item, player_gold: int) -> pygame.Surface:
    button_surface = create_rounded_surface(180, 50, (0, 160, 0), radius=10)
    if player_gold < item.price:
        button_surface.fill((160, 0, 0))
    purchase_text = render_text(font, f"Purchase ({item.price} Gold)", (0, 0, 0))
    text_rect = purchase_text.get_rect(center=button_surface.get_rect().center)
    button_surface.blit(purchase_text, text_rect)
    return button_surface

def draw_item_details(screen, font, rounded_surface: pygame.Surface, item: Item, y_offset: int) -> int:
    description_lines = item.description.split("\n")
    y_offset = draw_item_attributes(font, rounded_surface, item, y_offset)
    y_offset = max(y_offset, 100)
    y_offset = draw_description(font, rounded_surface, description_lines, y_offset)
    return y_offset

def display_item(screen, item, player_gold: int, font, rounded_surface: pygame.Surface, rounded_surface_rect: tuple[int,int]) -> pygame.Surface:
    y_offset = 10
    name_text = render_text(load_font(30), item.name, (0, 0, 0))
    rounded_surface.blit(name_text, (10, y_offset))
    y_offset += name_text.get_height() + 10

    y_offset = draw_item_details(screen, font, rounded_surface, item, y_offset)

    button_surface = create_button_surface(font, item, player_gold)

    button_x = (rounded_surface.get_width() - button_surface.get_width()) // 2

    screen.blit(
        button_surface,
        (rounded_surface_rect.left + button_x, rounded_surface_rect.top + 230),
    )

    item_image = load_and_scale_image(item.image, (100, 100))
    rounded_surface.blit(item_image, (rounded_surface.get_width() - item_image.get_width() - 10, 10))

    return button_surface

def display_potion_details(screen, item: Potion, player_gold: int, font, rounded_surface: pygame.Surface, rounded_surface_rect: tuple[int,int]) -> pygame.Surface:
    y_offset = 10
    name_text = render_text(load_font(30), item.name, (0, 0, 0))
    rounded_surface.blit(name_text, (10, y_offset))
    y_offset += name_text.get_height() + 10

    count_text = render_text(font, f"Count: {item.count}", (0, 0, 0))
    rounded_surface.blit(count_text, (10, y_offset))
    y_offset += count_text.get_height() + 10

    description_lines = item.description.split("\n")
    y_offset = max(y_offset, 100)
    y_offset = draw_description(font, rounded_surface, description_lines, y_offset)

    button_surface = create_button_surface(font, item, player_gold)

    button_x = (rounded_surface.get_width() - button_surface.get_width()) // 2

    screen.blit(
        button_surface,
        (rounded_surface_rect.left + button_x, rounded_surface_rect.top + 230),
    )

    item_image = load_and_scale_image(item.image, (100, 100))
    rounded_surface.blit(item_image, (rounded_surface.get_width() - item_image.get_width() - 10, 10))

    return button_surface

def display_shop_item(game_, shop_item):
    item = shop_item.item
    screen = game_.screen

    font_small = load_font(24)

    rounded_surface = create_rounded_surface(
        ITEM_INFO_WIDTH, ITEM_INFO_HEIGHT, (153, 153, 102), radius=10
    )
    rounded_surface_rect = rounded_surface.get_rect(
        center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 100)
    )

    border_width = 5
    border_surface = create_rounded_surface(
        rounded_surface.get_width() + 2 * border_width,
        rounded_surface.get_height() + 2 * border_width,
        (51, 51, 0),
        radius=10,
    )

    border_surface.blit(rounded_surface, (border_width, border_width))

    if isinstance(item, Item):
        button_surface = display_item(screen, item, game_.player.gold, font_small, rounded_surface, rounded_surface_rect)
    elif isinstance(item, Potion):
        button_surface = display_potion_details(screen, item, game_.player.gold, font_small, rounded_surface, rounded_surface_rect)

    screen.blit(
        border_surface,
        (
            (WIN_WIDTH - border_surface.get_width()) // 2,
            (WIN_HEIGHT - border_surface.get_height()) // 2 - 100,
        ),
    )
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
        attributes = [
            "attack",
            "hp",
            "defense",
            "range",
            "attack_speed",
            "movement_speed",
        ]
        if player.has_vorpal:
            player.attack /= 1.2
        for attribute in attributes:
            setattr(
                player, attribute, getattr(player, attribute) + getattr(item, attribute)
            )
        if player.has_vorpal:
            player.attack *= 1.2
    elif isinstance(item, Potion):
        for potion in player.potions:
            if potion.name == item.name:
                potion.count += item.count
