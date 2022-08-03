import pygame
import random
from settings import * 
from entity import Entity

class Enemy(Entity):
    def __init__(self, pos, groups, obstacle_sprites, damage_player):
        super().__init__(groups)

        self.health = 100
        self.max_health = self.health

        self.sprite_type = 'enemy'

        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect

        self.obstacle_sprites = obstacle_sprites

        self.attack_radius = 30
        self.notice_radius = 300

        self.resistance = 1.5
        self.attack_damage = 10
        self.speed = 2

        self.movement_loop = 0
        self.max_travel = random.randint(5, 20)

        self.player_range = 15

        self.status = 'idle'
        self.facing = 'left'

        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 1000

        self.damage_player = damage_player

        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def actions(self, player):
        if self.status == 'idle':
            if self.facing == 'left':
                self.direction.x = -1
                self.movement_loop -= 1
                if self.movement_loop <= - self.max_travel:
                    self.facing = 'right'

            if self.facing == 'right':
                self.direction.x = 1
                self.movement_loop += 1
                if self.movement_loop >= self.max_travel:
                    self.facing = 'left'

        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]

        else:
            self.direction = pygame.math.Vector2()

            if self.can_attack:
                self.damage_player(self.attack_damage, '...')

                self.can_attack = False
                self.attack_time = pygame.time.get_ticks()


    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()


        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()

            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= - self.resistance


    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.cooldowns()
        self.check_death()
        

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
