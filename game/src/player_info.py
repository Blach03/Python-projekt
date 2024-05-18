import pygame
from config import *
from game.src.items import Item, Potion


def draw_player_info(game):
    if game.player.info_open:
        player_info_surface = pygame.Surface(
            (PLAYER_INFO_WIDTH, PLAYER_INFO_HEIGHT), pygame.SRCALPHA
        )
        player_info_surface.fill(PLAYER_INFO_COLOR)

        font = pygame.font.Font(None, 32)
        y_offset = 10
        x_offset = 20

        def blit_attribute_bar(stat_name, value, max_value):
            nonlocal y_offset
            player_info_surface.blit(
                font.render(f"{stat_name}: {value}", True, (0, 0, 0)),
                (x_offset, y_offset),
            )
            y_offset += 35
            draw_segment_bar(
                player_info_surface, (x_offset, y_offset), min(1, value / max_value)
            )
            y_offset += SEGMENT_BAR_HEIGHT + SEGMENT_BAR_SPACING

        player_info_surface.blit(
            font.render("Player Attributes:", True, (0, 0, 0)), (10, y_offset)
        )
        y_offset += 35

        blit_attribute_bar("Attack", game.player.attack, 200)
        blit_attribute_bar("HP", game.player.hp, 1000)
        blit_attribute_bar("Defense", game.player.defense, 50)
        y_offset = 45
        x_offset = 320
        blit_attribute_bar("Range", game.player.range, 2)
        blit_attribute_bar("Attack Speed", game.player.attack_speed, 3)
        blit_attribute_bar("Movement Speed", game.player.movement_speed, 8)

        player_info_surface.blit(
            font.render("Inventory:", True, (0, 0, 0)), (10, y_offset)
        )
        y_offset += 30

        draw_inventory_grid(player_info_surface, (20, y_offset), game.player)

        total_surface_width = PLAYER_INFO_WIDTH + 20
        total_surface_height = PLAYER_INFO_HEIGHT + 20
        total_surface = pygame.Surface(
            (total_surface_width, total_surface_height), pygame.SRCALPHA
        )

        total_surface.fill((51, 51, 0, 230))

        total_surface.blit(player_info_surface, (10, 10))

        pygame.draw.rect(total_surface, (20, 20, 0, 200), total_surface.get_rect(), 2)

        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        total_surface_x = (screen_width - total_surface_width) // 2
        total_surface_y = (screen_height - total_surface_height) // 2

        game.screen.blit(total_surface, (total_surface_x, total_surface_y))


def draw_segment_bar(surface, position, percentage):
    x, y = position
    for i in range(10):
        color = SEGMENT_BAR_COLOR if i < percentage * 10 else (0, 0, 0, 200)
        pygame.draw.rect(
            surface,
            color,
            (
                x + (SEGMENT_BAR_WIDTH + SEGMENT_BAR_SPACING) * i,
                y - 10,
                SEGMENT_BAR_WIDTH,
                SEGMENT_BAR_HEIGHT,
            ),
        )


def draw_inventory_grid(surface, position, player):
    x, y = position

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH - 2):
            pygame.draw.rect(
                surface,
                (179, 179, 0, 230),
                (
                    x + (GRID_CELL_SIZE + GRID_SPACING) * col,
                    y + (GRID_CELL_SIZE + GRID_SPACING) * row,
                    GRID_CELL_SIZE,
                    GRID_CELL_SIZE,
                ),
            )

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH - 2, GRID_WIDTH):
            pygame.draw.rect(
                surface,
                (160, 160, 0, 230),
                (
                    x + (GRID_CELL_SIZE + GRID_SPACING) * col,
                    y + (GRID_CELL_SIZE + GRID_SPACING) * row,
                    GRID_CELL_SIZE,
                    GRID_CELL_SIZE,
                ),
            )

    for item_index, item in enumerate(player.items):
        if hasattr(item, "image"):
            item_image = pygame.image.load(item.image)
            item_image = pygame.transform.scale(
                item_image, (GRID_CELL_SIZE, GRID_CELL_SIZE)
            )

            item_row = item_index // (GRID_WIDTH - 2)
            item_col = item_index % (GRID_WIDTH - 2)
            item_x = x + (GRID_CELL_SIZE + GRID_SPACING) * item_col
            item_y = y + (GRID_CELL_SIZE + GRID_SPACING) * item_row

            surface.blit(item_image, (item_x, item_y))

    for item_index, potion in enumerate(player.potions):
        potion_image = potion.ready_image
        if potion.ready_image is None:
            potion_image = pygame.image.load(potion.image)
            potion_image = pygame.transform.scale(
                potion_image, (GRID_CELL_SIZE, GRID_CELL_SIZE)
            )

        item_row = item_index // 2
        item_col = (item_index % 2) + GRID_WIDTH - 2
        item_x = x + (GRID_CELL_SIZE + GRID_SPACING) * item_col
        item_y = y + (GRID_CELL_SIZE + GRID_SPACING) * item_row

        surface.blit(potion_image, (item_x, item_y))


def create_rounded_surface(width, height, color, radius):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    rect = surface.get_rect()
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    return surface


def draw_item(item: Item, screen: pygame.Surface) -> None:
    font = pygame.font.Font(None, 32)

    name_text = font.render(item.name, True, (0, 0, 0))
    font = pygame.font.Font(None, 24)
    attributes_text = [
        font.render(
            f"{attribute}: {getattr(item, attribute)}", True, (0, 0, 0)
        )
        for attribute in [
            "attack",
            "hp",
            "defense",
            "range",
            "attack_speed",
            "movement_speed",
        ]
        if getattr(item, attribute) != 0
    ]

    description_lines = item.description.split("\n")
    description_text = font.render("Description:", True, (0, 0, 0))

    item_image = pygame.image.load(item.image)
    item_image = pygame.transform.scale(item_image, (100, 100))

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

    rounded_surface.blit(
        item_image,
        (rounded_surface.get_width() - item_image.get_width() - 10, 10),
    )

    screen.blit(
        border_surface,
        (
            (WIN_WIDTH - border_surface.get_width()) // 2,
            (WIN_HEIGHT - border_surface.get_height()) // 2 - 100,
        ),
    )

    screen.blit(rounded_surface, rounded_surface_rect)


def draw_potion(item: Potion, screen: pygame.Surface, player) -> None:
    font = pygame.font.Font(None, 32)

    name_text = font.render(f"{item.name}", True, (0, 0, 0))
    count_text = font.render(f"Count: {item.count}", True, (0, 0, 0))
    font = pygame.font.Font(None, 24)

    description_lines = item.description.split("\n")
    description_text = font.render("Description:", True, (0, 0, 0))

    item_image = pygame.image.load(item.image)
    item_image = pygame.transform.scale(item_image, (100, 100))

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

    rounded_surface.blit(
        item_image,
        (rounded_surface.get_width() - item_image.get_width() - 10, 10),
    )

    screen.blit(
        border_surface,
        (
            (WIN_WIDTH - border_surface.get_width()) // 2,
            (WIN_HEIGHT - border_surface.get_height()) // 2 - 100,
        ),
    )

    screen.blit(rounded_surface, rounded_surface_rect)

    button_x = (rounded_surface.get_width() - 150) + 50
    button_y = rounded_surface.get_height() - 150

    button_surface = create_rounded_surface(
        button_x, button_y, (0, 160, 0), radius=10
    )

    if item.count == 0:
        button_surface.fill((160, 0, 0))

    use_text = font.render(f"Use", True, (0, 0, 0))

    text_rect = use_text.get_rect(center=button_surface.get_rect().center)
    button_surface.blit(use_text, text_rect)

    screen.blit(
        button_surface,
        (rounded_surface_rect.left + 50, rounded_surface_rect.top + 230),
    )

    rounded_surface.blit(
        item_image,
        (rounded_surface.get_width() - item_image.get_width() - 10, 10),
    )

    screen.blit(
        border_surface,
        (
            (WIN_WIDTH - border_surface.get_width()) // 2,
            (WIN_HEIGHT - border_surface.get_height()) // 2 - 100,
        ),
    )

    screen.blit(rounded_surface, rounded_surface_rect)

    rect = button_surface.get_rect()
    rect.x = rounded_surface_rect.left + 50
    rect.y = rounded_surface_rect.top + 230
    if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and item.count > 0:
        item.use(player)


def draw_item_info(game):
    if game.player.item_open and game.player.info_open:
        item_slot = game.player.clicked_slot
        if item_slot is not None and item_slot < 24:
            if item_slot < len(game.player.items):
                item = game.player.items[item_slot]
                draw_item(item, game.screen)

        elif item_slot is not None and item_slot >= 24:
            if item_slot - 24 < len(game.player.potions):
                item = game.player.potions[item_slot - 24]
                draw_potion(item, game.screen, game.player)


def draw_gold_hp(game):
    current_hp = game.player.current_hp
    hp = game.player.hp
    gold = game.player.gold

    hp_percentage = min(current_hp / hp, 1.0)

    font = pygame.font.Font(None, 24)

    hp_text = font.render(f"HP: {round(current_hp)} / {hp}", True, (255, 255, 255))
    gold_text = font.render(f"Gold: {gold}", True, (255, 255, 255))

    health_bar_width = int(200 * hp_percentage)

    health_bar_surface = pygame.Surface((200, 20), pygame.SRCALPHA)
    health_bar_surface.fill((255, 0, 0, 200))
    pygame.draw.rect(health_bar_surface, (0, 255, 0, 200), (0, 0, health_bar_width, 20))

    info_surface = pygame.Surface((220, 80), pygame.SRCALPHA)
    info_surface.fill((40, 40, 40, 200))
    info_surface.blit(hp_text, (10, 10))
    info_surface.blit(gold_text, (10, 60))
    info_surface.blit(health_bar_surface, (10, 30))

    game.screen.blit(info_surface, (0, 0))


def draw_circle(game):
    screen = game.screen
    center = (game.player.x + 23, game.player.y + 23)
    radius = 120

    temp_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)

    if game.player.has_disc:

        for i in range(radius, 0, -1):
            color = (255, 255, 0, max(0, (i * 50 // radius)))
            pygame.draw.circle(temp_surface, color, center, i)

        screen.blit(temp_surface, (0, 0))

        if game.damage_frame_counter % 40 == 0:
            for enemy in game.enemies:
                distance = pygame.math.Vector2(
                    enemy.rect.centerx - center[0], enemy.rect.centery - center[1]
                ).length()
                if distance < radius:
                    enemy.register_hit(game.player, game.player.attack / 3)

        game.damage_frame_counter += 1

    if game.player.has_shield:
        room = game.player.get_room()
        if room not in game.player.shield_used_rooms:
            radius = 50
            for i in range(radius, 0, -1):
                color = (255, 255, 255, max(0, (i * 50 // radius)))
                pygame.draw.circle(temp_surface, color, center, i)

            screen.blit(temp_surface, (0, 0))


ripples = []


def trigger_ripple(center):
    ripples.append([center, 0, 255])


def draw_ripples(game):
    for ripple in ripples[:]:
        _, radius, alpha = ripple
        if alpha <= 0:
            ripples.remove(ripple)
            continue
        new_radius = radius + 10
        new_alpha = max(alpha - 4, 0)
        surface = pygame.Surface((new_radius * 2, new_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            surface, (255, 0, 0) + (new_alpha,), (new_radius, new_radius), new_radius
        )
        surface_rect = surface.get_rect(center=ripple[0])
        game.screen.blit(surface, surface_rect)
        ripple[1] = new_radius
        ripple[2] = new_alpha
