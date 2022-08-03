from re import S
import pygame
from enemy import Enemy
from ui import UI
from sprites import * 
from player import * 
from settings import *
from support import *
from weapon import *
from game_data import *

class Level:
    def __init__(self, level_data, random=None):

        self.display_surface = pygame.display.get_surface()
        
        self.visable_sprites = YSortCamaraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()


        self.level_data = level_data

        self.player_count = 0

        if random:
            self.create_random_map()
        else:
            self.create_map(self.level_data)

        self.ui = UI()

    def create_random_map(self, max_rooms=20):

        room = {
            'Grass' : room_template['Grass'],
            'Wall_up' : room_template['Wall_up'],
            'Wall_leftright' : room_template['Wall_leftright'],
            'pfeile' : room_template['pfeile'],
            'Struct' : room_template['Struct'],
            'Props' : room_template['Props'],
            'Plant' : room_template['Plant'],
            'player' : room_template['leere'],
            'enemies' : room_template['leere']
        }
        map_direction = (True, True, True, True)

        count = 0

        x = 0
        y = 0

        pos_log = []

        diretion = random.choice(['left', 'right', 'up', 'down'])

        while max_rooms > count:
            possible_directions = []

            self.create_map(room, (x, y), map_direction)
            pos_log.append([x, y])

            for pos in pos_log:
                print(pos)

                if pos != [x, y] + pygame.math.Vector2(1, 0):
                    possible_directions.append('right')

                if pos != [x, y] + pygame.math.Vector2(-1, 0):
                    possible_directions.append('left')

                if pos != [x, y] + pygame.math.Vector2(0, 1):
                    possible_directions.append('down')

                if pos != [x, y] + pygame.math.Vector2(0, -1):
                    possible_directions.append('up')
                
            print(possible_directions)
            diretion = random.choice(possible_directions)
            print(diretion)

            if diretion == 'right':
                x += 1

            if diretion == 'left':
                x -= 1

            if diretion == 'down':
                y += 1

            if diretion == 'up':
                y -= 1

            


            count += 1

        print(pos_log)

        room = {
            'Grass' : room_template['leere'],
            'Wall_up' : room_template['leere'],
            'Wall_leftright' : room_template['leere'],
            'pfeile' : room_template['leere'],
            'Struct' : room_template['leere'],
            'Props' : room_template['leere'],
            'Plant' : room_template['leere'],
            'player' : room_template['player'],
            'enemies' : room_template['leere']
        }
        self.create_map(room, (0, 0))

    def create_map(self, level_data, pos=(0, 0), direction=(False, False, True, False)):
        sprite_group = pygame.sprite.Group()
        layouts = {
            'Grass': import_csv_layout(level_data['Grass']),
            'Wall_up': import_csv_layout(level_data['Wall_up']),
            'Wall_leftright': import_csv_layout(level_data['Wall_leftright']),
            'Struct': import_csv_layout(level_data['Struct']),
            'Props': import_csv_layout(level_data['Props']),
            'Plant': import_csv_layout(level_data['Plant']),
            'player': import_csv_layout(level_data['player']),
            'enemies': import_csv_layout(level_data['enemies']),
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

                        if style == 'enemies':
                            Enemy((x, y), [self.visable_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_player)

                        if style == 'player':
                            self.player = Player((x, y), [self.visable_sprites], self.obstacle_sprites, self.create_attack)     

    def create_attack(self):
        Weapon(self.player, [self.visable_sprites, self.attack_sprites])

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player, attack_sprite.type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.hp -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def run(self):
        self.visable_sprites.custom_draw(self.player)
        self.visable_sprites.update()
        self.visable_sprites.enemy_update(self.player)
        self.player_attack_logic()
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

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)