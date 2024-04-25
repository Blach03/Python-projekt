import pygame
from src.config import *


class DrawSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def draw(self, surface, bgsurf=None, special_flags=0):
        for sprite in self.sprites():
            sprite.draw(surface)


class DarkOverlay:
    def __init__(self):
        self.image = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, OVERLAY_COVERAGE))
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, (0, 0))


class Button:
    def __init__(self, center, size, fg, bg, content, fontsize):
        font = pygame.font.Font('../resources/chiller.ttf', fontsize)
        text = font.render(content, True, fg)
        text_rect = text.get_rect(center=(size[0] / 2, size[1] / 2))

        self.image = pygame.Surface(size)
        self.image.fill(bg)
        self.rect = self.image.get_rect(center=center)
        self.image.blit(text, text_rect)
        self.clicked = True

    def is_pressed(self, pos, pressed):
        is_pressed = self.rect.collidepoint(pos) and pressed and not self.clicked
        self.clicked = True
        if not pressed:
            self.clicked = False
        return is_pressed
