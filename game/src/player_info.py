import pygame
from config import *
from items import Potion


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


def draw_segment_bar(surface: pygame.Surface, position: tuple[int, int], percentage: float):
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


def draw_inventory_grid(surface: pygame.Surface, position: tuple[int, int], player):
    x, y = position
    draw_grid_background(surface, x, y)
    draw_grid_items(surface, x, y, player)
    draw_grid_potions(surface, x, y, player)


def draw_grid_background(surface: pygame.Surface, x: int, y: int):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH - 2):
            draw_grid_cell(surface, (179, 179, 0, 230), x, y, row, col)
        for col in range(GRID_WIDTH - 2, GRID_WIDTH):
            draw_grid_cell(surface, (160, 160, 0, 230), x, y, row, col)


def draw_grid_cell(surface: pygame.Surface, color, x: int, y: int, row: int, col: int):
    pygame.draw.rect(
        surface,
        color,
        (
            x + (GRID_CELL_SIZE + GRID_SPACING) * col,
            y + (GRID_CELL_SIZE + GRID_SPACING) * row,
            GRID_CELL_SIZE,
            GRID_CELL_SIZE,
        ),
    )


def draw_grid_items(surface: pygame.Surface, x: int, y: int, player):
    for item_index, item in enumerate(player.items):
        item_row = item_index // (GRID_WIDTH - 2)
        item_col = item_index % (GRID_WIDTH - 2)
        item_x = x + (GRID_CELL_SIZE + GRID_SPACING) * item_col
        item_y = y + (GRID_CELL_SIZE + GRID_SPACING) * item_row
        surface.blit(load_and_scale_image(item.image, GRID_CELL_SIZE), (item_x, item_y))


def draw_grid_potions(surface: pygame.Surface, x: int, y: int, player):
    for item_index, potion in enumerate(player.potions):
        item_row = item_index // 2
        item_col = (item_index % 2) + GRID_WIDTH - 2
        item_x = x + (GRID_CELL_SIZE + GRID_SPACING) * item_col
        item_y = y + (GRID_CELL_SIZE + GRID_SPACING) * item_row
        surface.blit(load_and_scale_image(potion, GRID_CELL_SIZE), (item_x, item_y))


def load_and_scale_image(item, size: int):
    if item.ready_image is None:
        item.ready_image = pygame.transform.scale(pygame.image.load(item.image), (size, size))
    if item.ready_image.get_width() != size:
        return pygame.transform.scale(item.ready_image, (size, size))
    else:
        return item.ready_image


def create_rounded_surface(width: int, height: int, color, radius: int) -> pygame.Surface:
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    rect = surface.get_rect()
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    return surface


def draw_item(item, screen):
    rounded_surface, rounded_surface_rect = prepare_item_surface()
    draw_item_details(item, rounded_surface)
    screen.blit(*prepare_border_surface(rounded_surface))
    screen.blit(rounded_surface, rounded_surface_rect)


def prepare_item_surface() -> tuple[pygame.Surface, pygame.Rect]:
    rounded_surface = create_rounded_surface(ITEM_INFO_WIDTH, ITEM_INFO_HEIGHT, (153, 153, 102), radius=10)
    rounded_surface_rect = rounded_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 100))
    return rounded_surface, rounded_surface_rect


def draw_item_details(item, surface: pygame.Surface):
    font = pygame.font.Font(None, 32)
    y_offset = draw_text(surface, font, item.name, (0, 0, 0), 10, 10)
    y_offset += 10
    y_offset += draw_item_attributes(item, surface, y_offset)
    y_offset = max(y_offset, 100)
    draw_text(surface, pygame.font.Font(None, 24), "Description:", (0, 0, 0), 10, y_offset + 10)
    y_offset += 30
    draw_item_description(surface, item.description, y_offset)
    draw_item_image(surface, item.image, 10, 10)


def draw_text(surface: pygame.Surface, font, text: str, color, x: int, y: int):
    rendered_text = font.render(text, True, color)
    surface.blit(rendered_text, (x, y))
    return rendered_text.get_height()


def draw_item_attributes(item, surface: pygame.Surface, y_offset: int) -> int:
    font = pygame.font.Font(None, 24)
    attributes = ["attack", "hp", "defense", "range", "attack_speed", "movement_speed"]
    for attribute in attributes:
        if getattr(item, attribute) != 0:
            y_offset += draw_text(surface, font, f"{attribute}: {getattr(item, attribute)}", (0, 0, 0), 10, y_offset)
    return y_offset


def draw_item_description(surface: pygame.Surface, description: str, y_offset: int):
    font = pygame.font.Font(None, 24)
    for line in description.split("\n"):
        y_offset += draw_text(surface, font, line, (0, 0, 0), 10, y_offset)


def draw_item_image(surface: pygame.Surface, image_path, x: int, y: int):
    item_image = load_and_scale_image(image_path, 100)
    surface.blit(item_image, (surface.get_width() - item_image.get_width() - x, y))


def prepare_border_surface(rounded_surface: pygame.Surface) -> tuple[pygame.Surface, tuple[int, int]]:
    border_width = 5
    border_surface = create_rounded_surface(
        rounded_surface.get_width() + 2 * border_width,
        rounded_surface.get_height() + 2 * border_width,
        (51, 51, 0),
        radius=10,
    )
    border_surface.blit(rounded_surface, (border_width, border_width))
    border_position = (
        (WIN_WIDTH - border_surface.get_width()) // 2,
        (WIN_HEIGHT - border_surface.get_height()) // 2 - 100,
    )
    return border_surface, border_position


def draw_potion(potion: Potion, screen: pygame.Surface, player):
    rounded_surface, rounded_surface_rect = prepare_potion_surface()
    draw_potion_details(potion, rounded_surface)
    draw_use_button(potion, rounded_surface, rounded_surface_rect, player)
    screen.blit(*prepare_border_surface(rounded_surface))
    screen.blit(rounded_surface, rounded_surface_rect)


def prepare_potion_surface() -> tuple[pygame.Surface, pygame.Rect]:
    rounded_surface = create_rounded_surface(ITEM_INFO_WIDTH, ITEM_INFO_HEIGHT, (153, 153, 102), radius=10)
    rounded_surface_rect = rounded_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 100))
    return rounded_surface, rounded_surface_rect


def draw_potion_details(potion: Potion, surface: pygame.Surface):
    font = pygame.font.Font(None, 32)
    y_offset = draw_text(surface, font, potion.name, (0, 0, 0), 10, 10)
    y_offset += draw_text(surface, font, f"Count: {potion.count}", (0, 0, 0), 10, y_offset + 10)
    y_offset = max(y_offset, 100)
    draw_text(surface, pygame.font.Font(None, 24), "Description:", (0, 0, 0), 10, y_offset + 10)
    y_offset += 30
    draw_item_description(surface, potion.description, y_offset)
    draw_item_image(surface, potion.image, 10, 10)


def draw_use_button(potion: Potion, rounded_surface: pygame.Surface, rounded_surface_rect: pygame.Rect, player):
    button_surface = create_use_button_surface(potion)
    draw_use_button_text(button_surface)
    button_x, button_y = get_button_position(rounded_surface_rect)
    rounded_surface.blit(button_surface, (button_x - rounded_surface_rect.left, button_y - rounded_surface_rect.top))
    button_rect = button_surface.get_rect(topleft=(button_x, button_y))
    if button_clicked(button_rect) and potion.count > 0:
        potion.use(player)


def create_use_button_surface(potion: Potion) -> pygame.Surface:
    button_surface = create_rounded_surface(150, 50, (0, 160, 0) if potion.count > 0 else (160, 0, 0), radius=10)
    return button_surface


def draw_use_button_text(surface: pygame.Surface):
    font = pygame.font.Font(None, 24)
    use_text = font.render("Use", True, (0, 0, 0))
    surface.blit(use_text, use_text.get_rect(center=surface.get_rect().center))


def get_button_position(rounded_surface_rect: pygame.Rect) -> tuple[int, int]:
    button_x = rounded_surface_rect.width - 220
    button_y = rounded_surface_rect.height - 50
    return rounded_surface_rect.left + button_x, rounded_surface_rect.top + button_y


def button_clicked(button_rect: pygame.Rect):
    return button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]


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


def trigger_ripple(center: tuple[int, int]):
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
