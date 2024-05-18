# GAME CONFIGURATION
WIN_WIDTH, WIN_HEIGHT = 960, 720
TILE_SIZE = 48
FPS = 60
OVERLAY_COVERAGE = 100  # [0, 255]

# MAP CONFIGURATION
MAP_TILE_SIZE = 32
MAP_BORDER_SIZE = 8
MAP_IMAGE_PATHS = (
    (0, "../resources/imgs/empty_icon.png"),
    (1, "../resources/imgs/room_icon.png"),
    (1.2, "../resources/imgs/shop_icon.png"),
    (2, "../resources/imgs/boss_icon.png"),
    (3, "../resources/imgs/player_icon.png"),
)

ITEMS_DATA = "../resources/json/items.json"
POTION_DATA = "../resources/json/potions.json"
ROOMS_DATA = "../resources/json/rooms.json"

CHARACTER_SPRITE = "../resources/imgs/character.png"
BLOCKS_SPRITE = "../resources/imgs/blocks.png"
SPIDER_SPRITE = "../resources/imgs/spider.png"
BULLET_SPRITE = "../resources/imgs/bullets.png"
ATTACK_SPRITE = "../resources/imgs/attack.png"

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
MID_RED = (150, 0, 0)
RED = (255, 0, 0)

# PLAYER CONFIGURATION
PLAYER_SPEED = 4
PLAYER_SIZE = (46, 46)

PLAYER_INFO_WIDTH = 585
PLAYER_INFO_HEIGHT = 430
PLAYER_INFO_COLOR = (153, 153, 102, 200)

SEGMENT_BAR_WIDTH = 20
SEGMENT_BAR_HEIGHT = 20
SEGMENT_BAR_SPACING = 3
SEGMENT_BAR_COLOR = (0, 255, 0, 200)

GRID_WIDTH = 10
GRID_HEIGHT = 3
GRID_CELL_SIZE = 50
GRID_SPACING = 5

ITEM_INFO_WIDTH = 300
ITEM_INFO_HEIGHT = 200
