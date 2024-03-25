import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import pygame


def figure_to_pygame_image(figure):
    buffer = BytesIO()
    figure.savefig(buffer, format='png')
    buffer.seek(0)
    image = Image.open(buffer)
    return pygame.image.fromstring(image.tobytes(), image.size, image.mode)


def update_map(game, before, after):
    game.map[before[0]][before[1]] = 1
    game.map[after[0]][after[1]] = 3
    plt.imshow(game.map, cmap='gray', interpolation='nearest')
    pygame_image = figure_to_pygame_image(plt.gcf())
    game.overlay_image = pygame_image
    pygame.display.flip()


def draw_map(game):
    if game.player.map_open:
        game.screen.blit(game.overlay_image, (100, 100))
