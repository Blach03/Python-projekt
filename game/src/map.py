import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
from config import WIN_WIDTH, WIN_HEIGHT, YELLOW
import pygame

TILE_SIZE = 32
BORDER_SIZE = 8

__image_pos = 0
plt.figure(facecolor='yellow')
plt.axis('off')
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)


def figure_to_pygame_image(figure):
    global __image_pos
    buffer = BytesIO()
    figure.savefig(buffer, format='png')
    buffer.seek(0)
    image = Image.open(buffer)
    __image_pos = ((WIN_WIDTH - image.size[0]) / 2, (WIN_HEIGHT - image.size[1]) / 2)
    return pygame.image.frombuffer(image.tobytes(), image.size, "RGBA").convert()


def update_map(game, before, after):
    game.map[before[0]][before[1]] = 1
    game.map[after[0]][after[1]] = 3
    plt.imshow(game.map, cmap='gray')
    pygame_image = figure_to_pygame_image(plt.gcf())
    pygame_image.set_colorkey(YELLOW)
    game.overlay_image = pygame_image
    pygame.display.update(pygame_image.get_rect())


def draw_map(game):
    if game.player.map_open:
        game.screen.blit(combine_images(game.map), __image_pos)


image_paths = {
    0: "../resources/empty_icon.png",
    1: "../resources/room_icon.png",
    1.2: "../resources/shop_icon.png",
    2: "../resources/boss_icon.png",
    3: "../resources/player_icon.png"
}


images = {}
for index, path in image_paths.items():
    image = pygame.image.load(path)
    images[index] = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))


def combine_images(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    combined_width = cols * TILE_SIZE + 2 * BORDER_SIZE
    combined_height = rows * TILE_SIZE + 2 * BORDER_SIZE
    combined_surface = pygame.Surface((combined_width, combined_height)).convert_alpha()

    background_color = (255, 255, 255, 0)
    combined_surface.fill(background_color)

    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            image = images.get(value)
            if image:
                combined_surface.blit(image, (x * TILE_SIZE + BORDER_SIZE, y * TILE_SIZE + BORDER_SIZE))

    border_color = (81, 81, 81)
    pygame.draw.rect(combined_surface, border_color, combined_surface.get_rect(), BORDER_SIZE)

    return combined_surface

# add map resizing and image pos
