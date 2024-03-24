import sys
import pygame
from sprites import *
from config import *
from generate import *
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_sprite_sheet = SpriteSheet('../resources/character.png')
        self.blocks_sprite_sheet = SpriteSheet('../resources/blocks.png')
        self.overlay_image = None

    def create_tilemap(self, tilemap, room_position):
        global player
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
                    player = Player(self, j, i, room_position)
                

    def new(self, start):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_tilemap(rooms[start[0]][start[1]], start)

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
        global player
        while self.playing:
            if player.map_open: 
                game.screen.blit(game.overlay_image, (100, 100))
                pygame.display.flip()
            
            if player.rect.y > WIN_HEIGHT:
                player.room_x += 1
                row = list(rooms[player.room_x][player.room_y][0])
                i, k = 0, 0
                while k < player.rect.x:
                    k += TILE_SIZE
                    i += 1
                row[i] = 'P'
                rooms[player.room_x][player.room_y][0] = ''.join(row)
                self.all_sprites = pygame.sprite.LayeredUpdates()
                self.blocks = pygame.sprite.LayeredUpdates()
                game.create_tilemap(rooms[player.room_x][player.room_y], [player.room_x,player.room_y])
                row[i] = '.'
                rooms[player.room_x][player.room_y][0] = ''.join(row)
                map[player.room_x-1][player.room_y] = 1
                map[player.room_x][player.room_y] = 3
                update_map()

            if player.rect.y < 0:
                player.room_x -= 1
                row = list(rooms[player.room_x][player.room_y][-1])
                i, k = 0, 0
                while k < player.rect.x:
                    k += TILE_SIZE
                    i += 1
                row[i] = 'P'
                rooms[player.room_x][player.room_y][-1] = ''.join(row)
                self.all_sprites = pygame.sprite.LayeredUpdates()
                self.blocks = pygame.sprite.LayeredUpdates()
                game.create_tilemap(rooms[player.room_x][player.room_y], [player.room_x,player.room_y])
                row[i] = '.'
                rooms[player.room_x][player.room_y][-1] = ''.join(row)
                map[player.room_x+1][player.room_y] = 1
                map[player.room_x][player.room_y] = 3
                update_map()

            if player.rect.x < 0:
                player.room_y -= 1
                i, k = 0, 0
                while k < player.rect.y:
                    k += TILE_SIZE
                    i += 1
                row = list(rooms[player.room_x][player.room_y][i])
                row[-1] = 'P'
                rooms[player.room_x][player.room_y][i] = ''.join(row)
                self.all_sprites = pygame.sprite.LayeredUpdates()
                self.blocks = pygame.sprite.LayeredUpdates()
                game.create_tilemap(rooms[player.room_x][player.room_y], [player.room_x,player.room_y])
                row[-1] = '.'
                rooms[player.room_x][player.room_y][i] = ''.join(row)
                map[player.room_x][player.room_y+1] = 1
                map[player.room_x][player.room_y] = 3
                update_map()

            if player.rect.x > WIN_WIDTH:
                player.room_y += 1
                i, k = 0, 0
                while k < player.rect.y:
                    k += TILE_SIZE
                    i += 1
                row = list(rooms[player.room_x][player.room_y][i])
                row[0] = 'P'
                rooms[player.room_x][player.room_y][i] = ''.join(row)
                self.all_sprites = pygame.sprite.LayeredUpdates()
                self.blocks = pygame.sprite.LayeredUpdates()
                game.create_tilemap(rooms[player.room_x][player.room_y], [player.room_x,player.room_y])
                row[0] = '.'
                rooms[player.room_x][player.room_y][i] = ''.join(row)
                map[player.room_x][player.room_y-1] = 1
                map[player.room_x][player.room_y] = 3
                update_map()


            self.events()
            self.update()
            self.draw()

        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass



def figure_to_pygame_image(figure):
        buffer = BytesIO()
        figure.savefig(buffer, format='png')
        buffer.seek(0)
        image = Image.open(buffer)
        return pygame.image.fromstring(image.tobytes(), image.size, image.mode)

def update_map():
    plt.imshow(map, cmap='gray', interpolation='nearest')
    pygame_image = figure_to_pygame_image(plt.gcf())
    game.overlay_image = pygame_image  
    pygame.display.flip()

player = 0
map,start,end = generate_map()
rooms = generate_rooms(map, start)

game = Game()
game.intro_screen()
game.new(start)
update_map()

row = list(rooms[start[0]][start[1]][7])
row[9] = "."
rooms[start[0]][start[1]][7] = ''.join(row)

while game.running:
    game.main()
    game.game_over()

pygame.quit()
sys.exit()
