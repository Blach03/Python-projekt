import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
from config import WIN_WIDTH, WIN_HEIGHT, YELLOW
import pygame

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
        game.screen.blit(game.overlay_image, __image_pos)
