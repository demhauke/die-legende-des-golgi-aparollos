import pygame
import random
from settings import * 
from entity import Entity

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites):
        super().__init__(groups)

        self.sprite_type = 'enemy'

        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect

        self.obstacle_sprites = obstacle_sprites

        self.speed = 2

        self.movement_loop = 0
        self.max_travel = random.randint(7, 20)

        self.status = 'idle'
        self.facing = 'down'



    def direction(self):
        if self.status == 'idle':
            if self.facing == 'down':
                pass

            

    def update(self):
        self.move(self.speed)