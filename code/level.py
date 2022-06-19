import imp
from itertools import count
from re import S
from tkinter.tix import Tree
import pygame
from ui import UI
from sprites import * 
from settings import *
from support import *
from debug import debug
from random_level import *

class Level:
    def __init__(self, level_data, random=None):

        # get the display surface
        self.display_surface = pygame.display.get_surface()
        
        self.visable_sprites = YSortCamaraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()

        self.level_data = level_data

        self.player_count = 0

        if random:
            self.create_random_map()
        else:
            self.create_map(self.level_data)

        self.ui = UI()

    def create_random_map(self, max_rooms=5):
        count = 0
        x = 0
        y = 0

        position_list = []

        left = False
        right = False
        up = True
        down = False

        visuel_left = False
        visuel_right = False
        visuel_up = True
        visuel_down = False

        direction = (False, False, True, False)
        visual_direction = (left, right, up, down)

        room = {
            'Grass' : room_template['Grass'],
            'Wall_up' : room_template['Wall_up'],
            'Wall_leftright' : room_template['Wall_leftright'],
            'pfeile' : room_template['pfeile'],
            'Struct' : room_template['Struct'],
            'Props' : room_template['Props'],
            'Plant' : room_template['Plant'],
            'player' : room_template['leere'],
        }

        # room = first_room

        self.create_map(room, (x,y), visual_direction)
        position_list.append((x, y))

        while count < max_rooms - 1:

            room = {
            'Grass' : room_template['Grass'],
            'Wall_up' : room_template['Wall_up'],
            'Wall_leftright' : room_template['Wall_leftright'],
            'pfeile' : room_template['pfeile'],
            'Struct' : room_template['Struct'],
            'Props' : room_template['Props'],
            'Plant' : random.choice((room_template['Plant'], room_template['leere'])),
            'player' : room_template['leere'],
            }

            # direction = (left, right, up, down)

            # self.create_map(room, (x,y), visual_direction)

            for index, val in enumerate(direction):
                if val == True:
                    if index == 0:
                        #left = True
                        x += -1
                        visuel_right = True

                    if index == 1:
                        #right = True
                        x += 1
                        visuel_left = True

                    if index == 2:
                        #up = True
                        y += -1
                        visuel_down = True

                    if index == 3:
                        #down = True
                        y += 1
                        visuel_up = True
                else:
                    if index == 0:
                        #left = False
                        visuel_right = False

                    if index == 1:
                        #right = False
                        visuel_left = False

                    if index == 2:
                        #up = False
                        visuel_down = False

                    if index == 3:
                        #down = False
                        visuel_up = False

            for pos in position_list:
                
                posible_directions = []

                if not (x + 1, y) == pos:
                    posible_directions.append('right')

                if not (x - 1, y) == pos:
                    posible_directions.append('left')

                if not (x, y + 1) == pos:
                    posible_directions.append('down')

                if not (x, y - 1) == pos:
                    posible_directions.append('up')


            if count != max_rooms -2:
                if visuel_down == True:
                    down = False
                    visual_next = random.choice(('up', 'left', 'right'))

                if visuel_up == True:
                    up = False
                    visual_next = random.choice(('down', 'left', 'right'))

                if visuel_left == True:
                    left = False
                    visual_next = random.choice(('up', 'down', 'right'))

                if visuel_right == True:
                    right = False
                    visual_next = random.choice(('up', 'down', 'left'))

                visual_next = random.choice(posible_directions)


                if visual_next == 'left':
                    left = True
                    visuel_left = True
                    direction = (True, False, False, False)

                if visual_next == 'right':
                    right = True
                    visuel_right = True
                    direction = (False, True, False, False)

                if visual_next == 'up':
                    up = True
                    visuel_up = True
                    direction = (False, False, True, False)

                if visual_next == 'down':
                    down = True
                    visuel_down = True
                    direction = (False, False, False, True)

            visual_direction = (visuel_left, visuel_right, visuel_up, visuel_down)
            self.create_map(room, (x,y), visual_direction)
            position_list.append((x, y))


            # direction = (random.choice((True, False)), random.choice((True, False)), random.choice((True, False)), random.choice((True, False)),)

            # room['player'] = room['null']
            player = False

            # if random.choice(('x', 'y')) == 'x':
            #     x += random.choice((-1, 1))
            # else:
            #     y += random.choice((-1, 1))

            count += 1

        print(position_list)


        room = {
            'Grass' : room_template['leere'],
            'Wall_up' : room_template['leere'],
            'Wall_leftright' : room_template['leere'],
            'pfeile' : room_template['leere'],
            'Struct' : room_template['leere'],
            'Props' : room_template['leere'],
            'Plant' : room_template['leere'],
            'player' : room_template['player'],
        }
        self.create_map(room, (0,0))


        # self.create_map(first_room)
        # self.create_map(first_room, pos=(0, 1))

    def create_map(self, level_data, pos=(0, 0), direction=(False, False, False, False)):
        sprite_group = pygame.sprite.Group()
        layouts = {
            'Grass': import_csv_layout(level_data['Grass']),
            'Wall_up': import_csv_layout(level_data['Wall_up']),
            'Wall_leftright': import_csv_layout(level_data['Wall_leftright']),
            'Struct': import_csv_layout(level_data['Struct']),
            'Props': import_csv_layout(level_data['Props']),
            'Plant': import_csv_layout(level_data['Plant']),
            'player': import_csv_layout(level_data['player']),
            'pfeile': import_csv_layout(level_data['pfeile'])
        }
        graphics = {
            'Grass': '[get_sprite()]'
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILESIZE + pos[0] * MODULE_WIDTH_AND_HEIGHT
                        y = row_index * TILESIZE + pos[1] * MODULE_WIDTH_AND_HEIGHT

                        if style == 'Grass':
                            if float(val) <= 7:
                                Grass((x, y), [self.visable_sprites])
                            if val == '9':
                                SnO_StraßenachOben((x, y), [self.visable_sprites])
                            if val == '8':
                                Straße((x, y), [self.visable_sprites])
                            if val == '10':
                                SnS_StraßenachSeite((x, y), [self.visable_sprites])

                        if style == 'Props':
                            if val == '8':
                                Door((x,y), [self.visable_sprites], self)
                            if val == '32':
                                Tk_Tempelkreis((x,y), [self.visable_sprites], self)
                            
                        if style == 'Wall_up':
                            if val == '16':
                                WnO_Wandnachoben((x, y), [self.visable_sprites, self.obstacle_sprites])
                            if val == '32':
                                WnU_WandnachUnten((x, y), [self.visable_sprites, self.obstacle_sprites])

                        if style == 'Wall_leftright':
                            if val == '4':
                                WnL_WandnachLinks((x, y), [self.visable_sprites, self.obstacle_sprites])
                            if val == '5':
                                WnR_WandnachRechts((x, y), [self.visable_sprites, self.obstacle_sprites])

                        if style == 'pfeile':
                            if int(val) >= 0 and int(val) <= 3:

                                if direction[int(val)] == False:
                                    if val == '0':
                                        WnL_WandnachLinks((x, y), [self.visable_sprites, self.obstacle_sprites])

                                    if val == '1':
                                        WnR_WandnachRechts((x, y), [self.visable_sprites, self.obstacle_sprites])

                                    if val == '2':
                                        WnO_Wandnachoben((x, y), [self.visable_sprites, self.obstacle_sprites])

                                    if val == '3':
                                        WnU_WandnachUnten((x, y), [self.visable_sprites, self.obstacle_sprites])


                        if style == 'Struct':
                            if val == '4':
                                Tor((x, y), [self.visable_sprites, self.obstacle_sprites])
                            if val == '0':
                                TnO_TreppenachOben((x, y), [self.visable_sprites], self)

                        if style == 'Plant':
                            if val == '16':
                                Baum((x, y), [self.visable_sprites])


                        if style == 'player':
                            self.player = Player((x, y), [self.visable_sprites], self.obstacle_sprites)     

    def run(self):
        self.visable_sprites.custom_draw(self.player)
        self.visable_sprites.update()
        self.ui.display(self.player)

class YSortCamaraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.zoom_scale = 3
        self.internal_surf_size = (2500, 2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center = (self.half_width, self.half_height))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_width
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_height

    def custom_draw(self, player):

        # self.zoom_keyboard_control()

        # self.internal_surf.fill('black')
        self.display_surface.fill('black')

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # for sprite in self.sprites():
        # for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset # + self.internal_offset
            self.display_surface.blit(sprite.image, offset_pos)

        # scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surface_size_vector * self.zoom_scale)
        # scaled_rect = scaled_surf.get_rect(center = (self.half_width, self.half_height))
        
        # self.display_surface.blit(scaled_surf, scaled_rect)

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom_scale += 0.1
        if keys[pygame.K_e]:
            if self.zoom_scale >= 0.55:
                self.zoom_scale -= 0.1