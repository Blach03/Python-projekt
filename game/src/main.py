import sys
from sprites import *
from config import *
from generate import *
from player_info import *
from items import *


from map import update_map, draw_map
from tile_builder import build_tile, tile_to_change


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_sprite_sheet = SpriteSheet('../resources/character.png')
        self.blocks_sprite_sheet = SpriteSheet('../resources/blocks.png')
        self.overlay_image = None

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
        self.clock.tick(FPS)
        draw_map(self)
        display_player_info(self)
        display_item_information(self)
        display_gold_hp(self)
        shop_item = self.player_near_shop_item()
        if shop_item != None:
            display_shop_item(self, shop_item)

        pygame.display.flip()

    def player_near_shop_item(self):
        for shop_item in self.all_sprites:
            if isinstance(shop_item, ShopItem) and shop_item.is_player_near(self.player):
                return shop_item
        return None


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
