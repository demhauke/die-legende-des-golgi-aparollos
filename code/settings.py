import pygame
# game setup
WIDTH    = 1280 
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

MODULE_WIDTH_AND_HEIGHT = 7 * TILESIZE
 
# ui
BAR_HEIGHT = 20
HP_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT_SIZE = 18
# UI_FONT = pygame.font.SysFont('comicsans', UI_FONT_SIZE)

# colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui color
HP_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# weapons
# weapon_data = {
#     'swort': {},
#     'lance': {},
#     'axe': {},
#     'rapier': {},
#     'sai': {}
# }

weapon_data = {
    'swort': {'cooldown': 300, 'damage': 20, 'graphic': 'graphics\weapons\swort.png'},
}

# enemy
monster_data = {
    '1': {'health': 100, 'exp': 100, 'damage': 10, 'attack_type': '...', 'attack_sound': '', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360}
}

