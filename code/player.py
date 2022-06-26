import random
import pygame
import math
from settings import *
from entity import Entity


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
        sprite.set_colorkey((0, 0, 0))
        return sprite

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack):
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

        self.facing = 'down'
        self.attacking = False
        self.attack_cooldown = 1000
        self.attack_time = None

        # weapon
        self.create_attack = create_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        print(self.weapon)


        self.damaging = False
        self.damage_cooldown = 500

        self.animation_loop = 1

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
            self.create_attack()
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
