import sys


from items import *
from config import *
from player_info import draw_player_info, draw_item_info, draw_gold_hp
from src.sprites.player import Player
from src.sprites.other import DrawSpriteGroup, Button, DarkOverlay
from src.sprites.enemies import Spider
from src.sprites.shopItem import ShopItem
from generate import generate_map, generate_rooms
from tile_builder import build_tile, tile_to_change
from map import update_map, draw_map
from data import Data


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = None
        self.playing = False
        self.ground = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.enemies = DrawSpriteGroup()
        self.attacks = pygame.sprite.Group()

        self.map, self.start, self.end = None, None, None
        self.rooms = None

        self.overlay = DarkOverlay()
        self.data = Data()

        self.difficulty = 1

    def new(self):
        self.map, self.start, self.end = generate_map()
        self.rooms = generate_rooms(self.map)
        build_tile(self, self.rooms[self.start[0]][self.start[1]])
        update_map(self, self.start, self.start)

        self.playing = True
        self.player = Player(self, (9.5 * TILE_SIZE, 7 * TILE_SIZE), self.start)

        # TESTOWANIE PRZECIWNIKÓW (dodać generowanie i zapisywanie przeciwników do mapy)
        Spider(self, (12 * TILE_SIZE, 12 * TILE_SIZE))
        Spider(self, (14 * TILE_SIZE, 2 * TILE_SIZE))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tile_to_change(self)

    def update(self):
        self.player.update()
        self.attacks.update()
        self.ground.update()
        self.enemies.update()

    def draw(self):
        self.ground.draw(self.screen)
        self.overlay.draw(self.screen)
        self.player.draw(self.screen)
        self.enemies.draw(self.screen)
        self.attacks.draw(self.screen)
        draw_map(self)
        draw_player_info(self)
        draw_item_info(self)
        draw_gold_hp(self)
        shop_item = self.player_near_shop_item()
        if shop_item is not None:
            display_shop_item(self, shop_item)

        self.clock.tick(FPS)

        pygame.display.flip()

    def player_near_shop_item(self):
        for shop_item in self.attacks:
            if isinstance(shop_item, ShopItem) and shop_item.is_player_near(self.player):
                return shop_item
        return None

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

        self.running = False

    def intro_screen(self):
        intro = True

        intro_background = pygame.image.load('../resources/intro_background.jpg')
        intro_background = pygame.transform.scale(intro_background, (1440, 720))

        title_font = pygame.font.SysFont('chiller', 120)
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

    def game_over(self):
        global play_again
        outro = True
        background = pygame.image.load('../resources/end_background.png')
        title_font = pygame.font.SysFont('chiller', 120)
        title = title_font.render('Game over', True, MID_RED)
        title_rect = title.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT * 0.35))

        play_button = Button((WIN_WIDTH / 2, WIN_HEIGHT * 0.55), (160, 60), MID_RED, BLACK, 'New game', 40)
        quit_button = Button((WIN_WIDTH / 2, WIN_HEIGHT * 0.65), (160, 60), MID_RED, BLACK, 'Quit game', 40)

        while outro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    outro = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_left_click = pygame.mouse.get_pressed()[0]

            if quit_button.is_pressed(mouse_pos, mouse_left_click):
                outro = False

            if play_button.is_pressed(mouse_pos, mouse_left_click):
                outro = False
                play_again = True

            self.screen.blit(background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            self.clock.tick(60)
            pygame.display.update()


play_again = True

while play_again:
    game = Game()
    game.intro_screen()
    game.new()
    play_again = False

    while game.running:
        game.main()
        game.game_over()

pygame.quit()
sys.exit()
