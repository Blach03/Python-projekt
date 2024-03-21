import sys
import pygame
from sprites import *
from config import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_sprite_sheet = SpriteSheet('../resources/character.png')
        self.blocks_sprite_sheet = SpriteSheet('../resources/blocks.png')

    def create_tilemap(self):
        for i, row in enumerate(tilemap):
            for j, object in enumerate(row):
                if random.randint(1, 10) > 9:
                    CobWeb(self, j, i)
                if object == '.':
                    Ground(self, j, i)
                elif object == 'B':
                    Block(self, j, i)
                elif object == 'P':
                    Ground(self, j, i)
                    Player(self, j, i)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_tilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                break

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass


game = Game()
game.intro_screen()
game.new()
while game.running:
    game.main()
    game.game_over()

pygame.quit()
sys.exit()
