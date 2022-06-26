from cmath import rect
import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.facing

        # graphic
        self.image = pygame.image.load('graphics\weapons\swort.png').convert_alpha()

        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(- 20, 0))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(+ 20, 0))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom)
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop)
