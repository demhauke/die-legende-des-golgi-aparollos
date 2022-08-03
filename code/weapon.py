from cmath import rect
import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.type = 'weapon'
        direction = player.facing

        # graphic
        # self.image = pygame.image.load('graphics\weapons\swort.png').convert_alpha()
        self.image = pygame.Surface((64, 64))

        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(- 20, 0))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(+ 20, 0))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom)
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop)

        self.start_time = pygame.time.get_ticks()

        self.exist_time = 400

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.exist_time:
            self.kill()
