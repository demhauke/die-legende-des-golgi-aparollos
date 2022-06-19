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

class Playerspritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

        self.animation = [self.get_sprite(0, 0, TILESIZE, TILESIZE),
        self.get_sprite(TILESIZE, 0, TILESIZE, TILESIZE),
        self.get_sprite(TILESIZE * 2, 0, TILESIZE, TILESIZE),
        self.get_sprite(TILESIZE * 3, 0, TILESIZE, TILESIZE),
        self.get_sprite(0, TILESIZE, TILESIZE, TILESIZE)]

        self.attack_animation = [self.get_sprite(0, 0, TILESIZE, TILESIZE),
        self.get_sprite(TILESIZE, 0, TILESIZE, TILESIZE), 
        self.get_sprite(0, TILESIZE, TILESIZE, TILESIZE)]

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey('white')
        sprite.set_colorkey('black')
        return sprite

class Hitbox(pygame.sprite.Sprite):
    def __init__(self, pos, obstacle_sprites, width_height = (TILESIZE, TILESIZE)):
        super().__init__(obstacle_sprites)

        self.hitbox = pygame.Rect(pos, width_height)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)


        self.idle_down = Playerspritesheet('graphics\main character\_down idle.png')
        self.idle_up = Playerspritesheet('graphics\main character\_up idle.png')
        self.idle_side = Playerspritesheet('graphics\main character\_side idle.png')

        self.walk_down = Playerspritesheet('graphics\main character\_down walk.png')
        self.walk_up = Playerspritesheet('graphics\main character\_up walk.png')
        self.walk_side = Playerspritesheet('graphics\main character\_side walk.png')

        self.attack_down = Playerspritesheet('graphics\main character\_down attack.png')
        self.attack_up = Playerspritesheet('graphics\main character\_up attack.png')
        self.attack_side = Playerspritesheet('graphics\main character\_side attack.png')

        self.image = self.idle_down.get_sprite(0, 0, TILESIZE, TILESIZE)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-50, -38)

        self.direction = pygame.math.Vector2()
        self.facing = 'down'
        self.attacking = False
        self.attack_cooldown = 1000
        self.attack_time = None

        self.damaging = False
        self.damage_cooldown = 500

        self.animation_loop = 1

        self.frame_index = 0
        self.animation_speed = 0.2

        self.obstacle_sprites = obstacle_sprites

        # stats
        self.stats = {
            'hp': 100,
            'energy': 60,
            'speed': 5,
            'energy_regen': 2

        }
            # current stats
        self.hp = self.stats['hp']
        self.energy = self.stats['energy']
        self.energy_regen = self.stats['energy_regen']
        self.xp = 12
        self.speed = self.stats['speed']

    def input(self):
        keys = pygame.key.get_pressed()

        energy_moving_subtraction = 3

        # movement input
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.facing = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.facing = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing = 'left'
        else:
            self.direction.x = 0

        if self.energy > energy_moving_subtraction and self.direction != [0, 0]:
            if keys[pygame.K_LSHIFT]:
                self.running = True
            else:
                self.running = False
        else:
            self.running = False
        
        # attack input
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.damaging = True
            self.attack_time = pygame.time.get_ticks()
            print('attack')
            self.energy -= 20

        # magic input
        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attacking = True
            self.damaging = True
            self.attack_time = pygame.time.get_ticks()
            print('magic')

    def energy_managemant(self):
        if self.energy < self.stats['energy']:
            self.energy += self.stats['energy_regen']
        if self.running == True:
            self.energy -= 3

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        if self.running == True:
            speed += 5
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
        
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

        if self.damaging:
            if current_time - self.attack_time >= self.damage_cooldown:
                self.damaging = False

    def animations(self, direction, facing):
        idle = True
        if direction[0] == 0 and direction[1] == 0:
            idle = True
        else:
            idle = False

        if self.damaging == False:
            # the character is not moving?
            if idle == True:
                # moving right
                if facing == 'right':
                    self.image = pygame.transform.flip(self.idle_side.animation[math.floor(self.animation_loop)], True, False)
                    self.animation_loop += 0.2
                    if self.animation_loop >= 5:
                        self.animation_loop = 1
                # moving left
                if facing == 'left':
                    self.image = self.idle_side.animation[math.floor(self.animation_loop)]
                    self.animation_loop += 0.2
                    if self.animation_loop >= 5:
                        self.animation_loop = 1

                # moving down
                if facing == 'down':
                    self.image = self.idle_down.animation[math.floor(self.animation_loop)]
                    self.animation_loop += 0.2
                    if self.animation_loop >= 5:
                        self.animation_loop = 1
                # moving up
                if facing == 'up':
                    self.image = self.idle_up.animation[math.floor(self.animation_loop)]
                    self.animation_loop += 0.2
                    if self.animation_loop >= 5:
                        self.animation_loop = 1
            else: # the character is moving?
                # moving right
                if direction[0] > 0:
                    self.image = pygame.transform.flip(self.walk_side.animation[math.floor(self.animation_loop)], True, False)
                    self.animation_loop += 0.2
                    if self.animation_loop >= 5:
                        self.animation_loop = 1
                # moving left
                if direction[0] < 0:
                    self.image = self.walk_side.animation[math.floor(self.animation_loop)]
                    self.animation_loop += 0.2
                    if self.animation_loop >= 5:
                        self.animation_loop = 1

                # moving down
                if direction[1] > 0:
                    self.image = self.walk_down.animation[math.floor(self.animation_loop)]
                    self.animation_loop += 0.2
                    if self.animation_loop >= 5:
                        self.animation_loop = 1
                # moving up
                if direction[1] < 0:
                    self.image = self.walk_up.animation[math.floor(self.animation_loop)]
                    self.animation_loop += 0.2
                    if self.animation_loop >= 5:
                        self.animation_loop = 1
        else:
            if facing == 'right':
                animation = self.attack_side.attack_animation
                self.frame_index += self.animation_speed
                if self.frame_index >= len(animation):
                    self.frame_index = 0
                    self.damaging = False

                self.image = pygame.transform.flip(animation[int(self.frame_index)], True, False)
                self.rect = self.image.get_rect(center = self.hitbox.center)
            # moving left
            if facing == 'left':
                animation = self.attack_side.attack_animation
                self.frame_index += self.animation_speed
                if self.frame_index >= len(animation):
                    self.frame_index = 0
                    self.damaging = False

                self.image = animation[int(self.frame_index)]
                self.rect = self.image.get_rect(center = self.hitbox.center)

            # moving down
            if facing == 'down':
                animation = self.attack_down.attack_animation
                self.frame_index += self.animation_speed
                if self.frame_index >= len(animation):
                    self.frame_index = 0
                    self.damaging = False

                self.image = animation[int(self.frame_index)]
                self.rect = self.image.get_rect(center = self.hitbox.center)
            # moving up
            if facing == 'up':
                animation = self.attack_up.attack_animation
                self.frame_index += self.animation_speed
                if self.frame_index >= len(animation):
                    self.frame_index = 0
                    self.damaging = False

                self.image = animation[int(self.frame_index)]
                self.rect = self.image.get_rect(center = self.hitbox.center)

    def animate(self):
        animation = self.idle_down.animation
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.energy_managemant()
        self.cooldowns()
        self.move(self.speed)
        self.animations(self.direction, self.facing)



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

