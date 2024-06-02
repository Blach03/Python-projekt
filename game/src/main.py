import sys

import pygame
from config import *
from data import Data
from generate import generate_map, generate_rooms
from items_interaction import display_shop_item
from map import draw_map, update_map
from player_info import (draw_circle, draw_gold_hp, draw_item_info,
                         draw_player_info, draw_ripples)
from sprites.other import Button, DarkOverlay, DrawSpriteGroup
from sprites.player import Player
from sprites.shopItem import ShopItem
from tile_builder import build_tile, tile_to_change
from sprites.enemies import draw_ripples_boss


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
        self.damage_frame_counter = 0
        
        #stats
        self.enemies_killed = 0
        self.gold_earned = 0
        self.damage_dealt = 0
        self.damage_taken = 0
        self.damage_blocked = 0
        self.bullets_shot = 0
        self.items_bought = 0
        self.potions_used = 0
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0
        self.score = 0
        self.healing = 0


    def new(self):
        self.map, self.start, self.end = generate_map()
        self.rooms = generate_rooms(self.map)
        build_tile(self, self.rooms[self.start[0]][self.start[1]])
        update_map(self, self.start, self.start)

        self.playing = True
        self.player = Player(self, (9.5 * TILE_SIZE, 7 * TILE_SIZE), self.start)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tile_to_change(self)

    def update(self):
        self.player.update()
        self.attacks.update()
        try:
            self.ground.update()
        except AttributeError:
            pass
        self.enemies.update()
        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000

    def draw(self):
        try:
            self.ground.draw(self.screen)
        except AttributeError:
            pass
        self.overlay.draw(self.screen)
        self.player.draw(self.screen)
        self.enemies.draw(self.screen)
        self.attacks.draw(self.screen)
        draw_map(self)
        draw_player_info(self)
        draw_item_info(self)
        draw_gold_hp(self)
        draw_circle(self)
        draw_ripples(self)
        draw_ripples_boss(self)
        shop_item = self.player_near_shop_item()
        if shop_item is not None:
            display_shop_item(self, shop_item)

        self.clock.tick(FPS)

        pygame.display.flip()

    def player_near_shop_item(self) -> ShopItem or None:
        for shop_item in self.attacks:
            if isinstance(shop_item, ShopItem) and shop_item.is_player_near(
                self.player
            ):
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

        intro_background = pygame.image.load("../resources/imgs/intro_background.jpg")
        intro_background = pygame.transform.scale(intro_background, (1440, 720))

        title_font = pygame.font.SysFont("chiller", 120)
        title = title_font.render("Dungeon Adventure", True, MID_RED)
        title_rect = title.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT * 0.42))

        play_button = Button(
            (WIN_WIDTH / 2, WIN_HEIGHT * 0.58), (120, 60), BLACK, MID_RED, "Play", 40
        )

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            if play_button.is_pressed(
                pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]
            ):
                intro = False

            self.screen.blit(intro_background, (-240, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(60)
            pygame.display.update()

    def game_over(self):
        global play_again
        outro = True
        background = pygame.image.load("../resources/imgs/end_background.png")
        title_font = pygame.font.SysFont("chiller", 120)
        title = title_font.render("Game over", True, MID_RED)
        title_rect = title.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT * 0.35))

        play_button = Button(
            (WIN_WIDTH / 2, WIN_HEIGHT * 0.55),
            (160, 60),
            MID_RED,
            BLACK,
            "New game",
            40,
        )
        quit_button = Button(
            (WIN_WIDTH / 2, WIN_HEIGHT * 0.65),
            (160, 60),
            MID_RED,
            BLACK,
            "Quit game",
            40,
        )

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

    def show_statistics_screen(self):
        self.playing = False
        outro = True

        background_image = pygame.image.load("../resources/imgs/stat_screen.jpg")
        background_image = pygame.transform.scale(background_image, self.screen.get_size())

        while outro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: 
                        outro = False
                        self.running = False

            self.screen.blit(background_image, (0, 0))

            stats_font = pygame.font.SysFont("Times New Roman", 40)
            elapsed_minutes = self.elapsed_time // 60
            elapsed_seconds = self.elapsed_time % 60
            self.score = max(0, 1000 - self.elapsed_time) * 80
            if self.enemies_killed < 100:
                penalty = 0
                for i in range(self.enemies_killed):
                    self.score += 1000 - penalty
                    penalty += 10
            else:
                self.score += 50500
            stats = [
                f"Enemies killed: {self.enemies_killed}",
                f"Gold earned: {self.gold_earned}",
                f"Damage dealt: {self.damage_dealt}",
                f"Healing done: {self.healing}",
                f"Bullets shot: {self.bullets_shot}",
                f"Items bought: {self.items_bought}",
                f"Potions used: {self.potions_used}",
                f"Time: {elapsed_minutes}m {elapsed_seconds}s",
                f"Score: {self.score}",
                "Press Enter to exit..."
            ]

            for i, stat in enumerate(stats):
                stat_text = stats_font.render(stat, True, (0, 0, 0)) 
                text_rect = stat_text.get_rect(center=(self.screen.get_width() / 2, 180 + i * 45))
                self.screen.blit(stat_text, text_rect)

            pygame.display.flip()
            self.clock.tick(60)


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
