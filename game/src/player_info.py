import pygame

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
        
        draw_inventory_grid(player_info_surface, (20, y_offset))

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


def draw_inventory_grid(surface, position):
    x, y = position
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            pygame.draw.rect(surface, (179, 179, 0, 230), (x + (GRID_CELL_SIZE + GRID_SPACING) * col, y + (GRID_CELL_SIZE + GRID_SPACING) * row, GRID_CELL_SIZE, GRID_CELL_SIZE))


