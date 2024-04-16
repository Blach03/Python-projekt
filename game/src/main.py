import sys
import pygame

from config import *
from sprites import SpriteSheet, Player, Button
from generate import generate_map, generate_rooms
from tile_builder import build_tile, tile_to_change
from map import update_map, draw_map


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_sprite_sheet = SpriteSheet('../resources/character.png')
        self.blocks_sprite_sheet = SpriteSheet('../resources/blocks.png')
        self.overlay_image = None

        self.dark_overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        self.dark_overlay.fill((0, 0, 0, 100))

        self.player = None
        self.playing = False
        self.all_sprites = None
        self.blocks = None
        self.enemies = None
        self.attacks = None
        self.player_sprite = None

        self.map, self.start, self.end = None, None, None
        self.rooms = None

    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.player_sprite = pygame.sprite.LayeredUpdates()

        self.map, self.start, self.end = generate_map()
        self.rooms = generate_rooms(self.map)

        self.player = Player(self, (9.5 * TILE_SIZE, 7 * TILE_SIZE), self.start)
        build_tile(self, self.rooms[self.start[0]][self.start[1]])

        update_map(self, self.start, self.start)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                break

        tile_to_change(self)

    def update(self):
        self.player_sprite.update()
        self.all_sprites.update()

    def draw(self):
        self.all_sprites.draw(self.screen)
        self.player_sprite.draw(self.screen)
        self.screen.blit(self.dark_overlay, (0, 0))
        self.clock.tick(FPS)
        draw_map(self)

        pygame.display.flip()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        intro = True

        intro_background = pygame.image.load('../resources/intro_background.jpg')
        intro_background = pygame.transform.scale(intro_background, (1440, 720))

        title_font = pygame.font.Font('../resources/chiller.ttf', 80)
        title = title_font.render('Dungeon Adventure', True, MID_RED)
        title_rect = title.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT*0.42))

        play_button = Button((WIN_WIDTH/2, WIN_HEIGHT*0.58), (120, 60), BLACK, MID_RED, 'Play', 40)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            if play_button.is_pressed(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]):
                intro = False

            self.screen.blit(intro_background, (-240, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(60)
            pygame.display.update()


game = Game()
game.intro_screen()
game.new()

while game.running:
    game.main()
    game.game_over()

pygame.quit()
sys.exit()
