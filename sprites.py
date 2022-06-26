import random
import pygame
import math
from settings import *

class button():
    def __init__(self, x,y,width,height, text='', color = 'gray'):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outlinecolor=None, border = 5):
        #Call this method to draw the button on the screen
        if outlinecolor:
            pygame.draw.rect(win, outlinecolor, (self.x-2,self.y-2,self.width+4,self.height+4), border)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey((0, 0, 0))
        return sprite

class Hitbox(pygame.sprite.Sprite):
    def __init__(self, pos, obstacle_sprites, width_height = (TILESIZE, TILESIZE)):
        super().__init__(obstacle_sprites)

        self.hitbox = pygame.Rect(pos, width_height)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, image = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)

class Grass(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.sheet = Spritesheet('graphics\Pixel Art Top Down - Basic\TX Tileset Grass.png')
        self.image_list = [self.sheet.get_sprite(0, 0, TILESIZE, TILESIZE), self.sheet.get_sprite(TILESIZE, 0, TILESIZE, TILESIZE), self.sheet.get_sprite(0, TILESIZE, TILESIZE, TILESIZE), self.sheet.get_sprite(TILESIZE, TILESIZE, TILESIZE, TILESIZE), 
            self.sheet.get_sprite(TILESIZE * 2, 0, TILESIZE, TILESIZE), self.sheet.get_sprite(TILESIZE * 3, 0, TILESIZE, TILESIZE), self.sheet.get_sprite(TILESIZE * 2, TILESIZE, TILESIZE, TILESIZE), self.sheet.get_sprite(TILESIZE * 3, TILESIZE, TILESIZE, TILESIZE)]
        self.image = random.choice(self.image_list)
        self.rect = self.image.get_rect(topleft = pos)

class Baum(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.sheet = Spritesheet('graphics\Pixel Art Top Down - Basic\TX Plant.png')
        self.image_list = [self.sheet.get_sprite(0, 0, TILESIZE * 2, TILESIZE * 3), self.sheet.get_sprite(TILESIZE * 2, 0, TILESIZE * 2, TILESIZE * 3), self.sheet.get_sprite(TILESIZE * 4, 0, TILESIZE * 2, TILESIZE * 3), False]
        self.image = random.choice(self.image_list)
        if self.image == False:
            self.kill()
        else:
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - 2 * TILESIZE))
            self.hitbox = self.rect


class SnO_StraßenachOben(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.sheet = Spritesheet('graphics\Pixel Art Top Down - Basic\TX Tileset Grass.png')
        self.image_list = [self.sheet.get_sprite(1 * TILESIZE, 2 * TILESIZE, TILESIZE, TILESIZE), self.sheet.get_sprite(TILESIZE, 3 * TILESIZE, TILESIZE, TILESIZE)]
        self.image = random.choice(self.image_list)
        self.rect = self.image.get_rect(topleft = pos)

class SnS_StraßenachSeite(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.sheet = Spritesheet('graphics\Pixel Art Top Down - Basic\TX Tileset Grass.png')
        self.image_list = [self.sheet.get_sprite(2 * TILESIZE, 2 * TILESIZE, TILESIZE, TILESIZE), self.sheet.get_sprite(3 * TILESIZE, 2 * TILESIZE, TILESIZE, TILESIZE)]
        self.image = random.choice(self.image_list)
        self.rect = self.image.get_rect(topleft = pos)

class Straße(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.sheet = Spritesheet('graphics\Pixel Art Top Down - Basic\TX Tileset Grass.png')
        self.image_list = [self.sheet.get_sprite(0 * TILESIZE, 2 * TILESIZE, TILESIZE, TILESIZE), self.sheet.get_sprite(0, 3 * TILESIZE, TILESIZE, TILESIZE)]
        self.image = random.choice(self.image_list)
        self.rect = self.image.get_rect(topleft = pos)

class WnO_Wandnachoben(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.sheet = Spritesheet('graphics\Pixel Art Top Down - Basic\TX Tileset Wall_2.png')
        self.image_list = [self.sheet.get_sprite(0, 2 * TILESIZE, TILESIZE, TILESIZE), self.sheet.get_sprite(1 * TILESIZE, 2 * TILESIZE, TILESIZE, TILESIZE), self.sheet.get_sprite(0, 3 * TILESIZE, TILESIZE, TILESIZE), self.sheet.get_sprite(1 * TILESIZE, 3 * TILESIZE, TILESIZE, TILESIZE) ]
        self.image = random.choice(self.image_list)
        self.rect = self.image.get_rect(topleft = pos)
        # self.hitbox = self.rect.inflate(0, -40)
        self.hitbox = pygame.Rect(pos, (TILESIZE, TILESIZE -25))

class WnU_WandnachUnten(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.sheet = Spritesheet('graphics\Pixel Art Top Down - Basic\TX Tileset Wall_2.png')
        self.image_list = [self.sheet.get_sprite(0, 4 * TILESIZE, TILESIZE, TILESIZE), self.sheet.get_sprite(1 * TILESIZE, 4 * TILESIZE, TILESIZE, TILESIZE), self.sheet.get_sprite(2 * TILESIZE, 4 * TILESIZE, TILESIZE, TILESIZE)]
        self.image = random.choice(self.image_list)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(pos[0], pos[1] + TILESIZE - 10, TILESIZE, 10)

class WnL_WandnachLinks(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.sheet = Spritesheet('graphics\Pixel Art Top Down - Basic\TX Tileset Wall_2.png')
        self.image_list = [self.sheet.get_sprite(4 * TILESIZE, 0 * TILESIZE, TILESIZE, TILESIZE), self.sheet.get_sprite(4 * TILESIZE, 1 * TILESIZE, TILESIZE, TILESIZE), self.sheet.get_sprite(4 * TILESIZE, 2 * TILESIZE, TILESIZE, TILESIZE)]
        self.image = random.choice(self.image_list)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(pos, (8, TILESIZE))

class WnR_WandnachRechts(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.sheet = Spritesheet('graphics\Pixel Art Top Down - Basic\TX Tileset Wall_2.png')
        self.image_list = [self.sheet.get_sprite(5 * TILESIZE, 0 * TILESIZE, TILESIZE, TILESIZE), self.sheet.get_sprite(5 * TILESIZE, 1 * TILESIZE, TILESIZE, TILESIZE), self.sheet.get_sprite(5 * TILESIZE, 2 * TILESIZE, TILESIZE, TILESIZE)]
        self.image = random.choice(self.image_list)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(pos[0] + TILESIZE - 8, pos[1], 8, TILESIZE)

class Door(pygame.sprite.Sprite):
    def __init__(self, pos, groups, level, type = 'close'):
        super().__init__(groups)

        self.level = level

        if type == 'close':
            self.type = type
        if type == 'open':
            self.type = type

        self.sheet = Spritesheet('graphics\Pixel Art Top Down - Basic\TX Props_2.png')
        self.image = self.sheet.get_sprite(0, 1 * TILESIZE, TILESIZE, TILESIZE)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.hitbox = self.rect.inflate(0, 0)

    def draw(self):
        if self.type == 'close':
            self.image = self.sheet.get_sprite(0, 1 * TILESIZE, TILESIZE, TILESIZE)
        if self.type == 'open':
            self.image = self.sheet.get_sprite(0, 2 * TILESIZE, TILESIZE, TILESIZE)
    
    def collide_player(self, player):
        if self.hitbox.colliderect(player.hitbox):
            self.type = 'open'
        else:
            self.type = 'close'
    def update(self):
        self.collide_player(self.level.player)
        self.draw()

class Tor(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.sheet = Spritesheet('graphics\Pixel Art Top Down - Basic\TX Struct.png')
        self.image_list = [self.sheet.get_sprite(4 * TILESIZE, 0, TILESIZE, TILESIZE), self.sheet.get_sprite(4 * TILESIZE, 1 * TILESIZE, TILESIZE, TILESIZE)]
        self.image = random.choice(self.image_list)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(pos, (TILESIZE, TILESIZE -25))

class TnO_TreppenachOben(pygame.sprite.Sprite):
    def __init__(self, pos, groups, level):
        super().__init__(groups)

        self.level = level

        self.sheet = Spritesheet('graphics\Pixel Art Top Down - Basic\TX Struct.png')
        self.image_list = [self.sheet.get_sprite(0 * TILESIZE, 0 * TILESIZE, TILESIZE, 2 * TILESIZE), self.sheet.get_sprite(1 * TILESIZE, 0 * TILESIZE, TILESIZE, 2 * TILESIZE), self.sheet.get_sprite(2 * TILESIZE, 0 * TILESIZE, TILESIZE, 2 * TILESIZE),
            self.sheet.get_sprite(0 * TILESIZE, 2 * TILESIZE, TILESIZE, 2 * TILESIZE), self.sheet.get_sprite(1 * TILESIZE, 2 * TILESIZE, TILESIZE, 2 * TILESIZE), self.sheet.get_sprite(2 * TILESIZE, 2 * TILESIZE, TILESIZE, 2 * TILESIZE)]
        self.image = random.choice(self.image_list)
        self.rect = self.image.get_rect(topleft = pos)

        Hitbox((pos[0], pos[1]), self.level.obstacle_sprites, (1, 1.5 * TILESIZE))
        Hitbox((pos[0] + TILESIZE, pos[1]), self.level.obstacle_sprites, (1, 1.5 * TILESIZE))

class Tk_Tempelkreis(pygame.sprite.Sprite):
    def __init__(self, pos, groups, level):
        super().__init__(groups)

        self.level = level

        self.width = 94
        self.height = 328 - 256 # 72

        self.sheet = Spritesheet('graphics\Pixel Art Top Down - Basic\TX Props_2.png')
        self.image = self.sheet.get_sprite(0, 4 * TILESIZE, self.width, self.height)
        self.rect = self.image.get_rect(topleft = (pos[0] - (self.width - TILESIZE) / 2, pos[1] - (self.height - TILESIZE) / 2))
        self.hitbox = self.rect

    def player_collide(self):
        if self.level.player.hitbox.colliderect(self.hitbox): 
            print('collide')

            # if self.level.ui.draw_button()


    def update(self):
        self.player_collide()

