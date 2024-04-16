import pygame
from config import *

PLAYER_INFO_WIDTH = 585
PLAYER_INFO_HEIGHT = 430
PLAYER_INFO_COLOR = (153, 153, 102, 200)

SEGMENT_BAR_WIDTH = 20
SEGMENT_BAR_HEIGHT = 20
SEGMENT_BAR_SPACING = 3
SEGMENT_BAR_COLOR = (0, 255, 0, 200)

GRID_WIDTH = 10
GRID_HEIGHT = 3
GRID_CELL_SIZE = 50
GRID_SPACING = 5

ITEM_INFO_WIDTH = 300
ITEM_INFO_HEIGHT = 200

def display_player_info(game):
    if game.player.info_open:
        player_info_surface = pygame.Surface((PLAYER_INFO_WIDTH, PLAYER_INFO_HEIGHT), pygame.SRCALPHA)
        player_info_surface.fill(PLAYER_INFO_COLOR)

        font = pygame.font.Font(None, 32)
        y_offset = 10

        text = font.render("Player Attributes:", True, (0, 0, 0))
        player_info_surface.blit(text, (10, y_offset))
        y_offset += 35
        
        text = font.render("Attack: {}".format(game.player.attack), True, (0, 0, 0))
        player_info_surface.blit(text, (20, y_offset))
        y_offset += 35
        
        draw_segment_bar(player_info_surface, (20, y_offset), min(1, game.player.attack / 100))
        y_offset += SEGMENT_BAR_HEIGHT + SEGMENT_BAR_SPACING
        
        text = font.render("HP: {}".format(game.player.hp), True, (0, 0, 0))
        player_info_surface.blit(text, (20, y_offset))
        y_offset += 35
        
        draw_segment_bar(player_info_surface, (20, y_offset), min(1, game.player.hp / 1000))
        y_offset += SEGMENT_BAR_HEIGHT + SEGMENT_BAR_SPACING
        
        text = font.render("Defense: {}".format(game.player.defense), True, (0, 0, 0))
        player_info_surface.blit(text, (20, y_offset))
        y_offset += 35
 
        draw_segment_bar(player_info_surface, (20, y_offset), min(1, game.player.defense / 50))
        y_offset += SEGMENT_BAR_HEIGHT + SEGMENT_BAR_SPACING
        
        y_offset = 45
        text = font.render("Range: {}".format(game.player.range), True, (0, 0, 0))
        player_info_surface.blit(text, (320, y_offset))
        y_offset += 35
        
        draw_segment_bar(player_info_surface, (320, y_offset), min(1, game.player.range / 2))
        y_offset += SEGMENT_BAR_HEIGHT + SEGMENT_BAR_SPACING
        
        text = font.render("Attack Speed: {}".format(game.player.attack_speed), True, (0, 0, 0))
        player_info_surface.blit(text, (320, y_offset))
        y_offset += 35

        draw_segment_bar(player_info_surface, (320, y_offset), min(1, game.player.range / 3))
        y_offset += SEGMENT_BAR_HEIGHT + SEGMENT_BAR_SPACING

        y_offset += SEGMENT_BAR_HEIGHT + SEGMENT_BAR_SPACING + 35

        text = font.render("Inventory:", True, (0, 0, 0))
        player_info_surface.blit(text, (10, y_offset))
        y_offset += 30
        
        draw_inventory_grid(player_info_surface, (20, y_offset), game.player)

        total_surface_width = PLAYER_INFO_WIDTH + 20
        total_surface_height = PLAYER_INFO_HEIGHT + 20
        total_surface = pygame.Surface((total_surface_width, total_surface_height), pygame.SRCALPHA)
        
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
        pygame.draw.rect(surface, color, (x + (SEGMENT_BAR_WIDTH + SEGMENT_BAR_SPACING) * i, y - 10, SEGMENT_BAR_WIDTH, SEGMENT_BAR_HEIGHT))


def draw_inventory_grid(surface, position, player):
    x, y = position
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            pygame.draw.rect(surface, (179, 179, 0, 230), (x + (GRID_CELL_SIZE + GRID_SPACING) * col, y + (GRID_CELL_SIZE + GRID_SPACING) * row, GRID_CELL_SIZE, GRID_CELL_SIZE))

    for item_index, item in enumerate(player.inventory):
        if hasattr(item, 'image'):
            item_image = pygame.image.load(item.image)
            item_image = pygame.transform.scale(item_image, (GRID_CELL_SIZE, GRID_CELL_SIZE))
            
            item_row = item_index // GRID_WIDTH
            item_col = item_index % GRID_WIDTH
            item_x = x + (GRID_CELL_SIZE + GRID_SPACING) * item_col
            item_y = y + (GRID_CELL_SIZE + GRID_SPACING) * item_row
            
            surface.blit(item_image, (item_x, item_y))

def create_rounded_surface(width, height, color, radius):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    rect = surface.get_rect()
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    return surface

def display_item_information(game):
    if game.player.item_open and game.player.info_open:
        screen = game.screen
        item_slot = game.player.clicked_slot
        if item_slot is not None:
            item = game.player.inventory[item_slot]

            font = pygame.font.Font(None, 24)

            name_text = font.render(f"Name: {item.name}", True, (0, 0, 0))
            attributes_text = [font.render(f"{attribute}: {value}", True, (0, 0, 0)) for attribute, value in item.attributes.items()]
            description_text = font.render(f"Description: {item.description}", True, (0, 0, 0))

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

            y_offset += 30

            rounded_surface.blit(description_text, (10, y_offset + 10))

            rounded_surface.blit(item_image, (rounded_surface.get_width() - item_image.get_width() - 10, 10))

            screen.blit(border_surface, ((WIN_WIDTH - border_surface.get_width()) // 2, (WIN_HEIGHT - border_surface.get_height()) // 2 - 100))

            screen.blit(rounded_surface, rounded_surface_rect)
            