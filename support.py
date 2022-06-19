from csv import reader
from os import walk

import pygame

from settings import TILESIZE

def import_csv_layout(path):
    terrain_map = []

    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def get_sprite(path, x, y, width, height):
    sheet = pygame.image.load(path).convert()
    sprite = pygame.Surface([width, height])
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    sprite.convert_alpha()
    return sprite

def import_folder(path):
    for data in walk(path):
        print(data)


# def import_cut_graphic(path):
#     surface = pygame.image.load(path).convert_alpha()
#     tile_num_x = int(surface.get_size()[0] / TILESIZE)
#     tile_num_y = int(surface.get_size()[1] / TILESIZE)

#     cut_tiles = []
#     for row in range(tile_num_y):
#         for col in range(tile_num_x):
#             x = col * TILESIZE
#             y = row * TILESIZE
#             new_surf = pygame.Surface((TILESIZE, TILESIZE))
#             new_surf.blit(surface, (x,y), pygame.Rect(x, y, TILESIZE, TILESIZE))
#             cut_tiles.append(new_surf)

#     return cut_tiles
