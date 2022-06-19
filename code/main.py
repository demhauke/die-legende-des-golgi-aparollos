import pygame, sys
from settings import *
from game_data import * 
from level import *
from start_screen import *
 
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        self.width = self.screen.get_width()
        pygame.display.set_caption('Die Legende des Golgi Apparillo')
        self.clock = pygame.time.Clock()

        # self.level = Level(level_0)

        self.type = 'start_screen'

    def start_screen(self):
        intro_screen = True
        grass = pygame.sprite.Group()

        play_button = button(self.screen.get_width() / 2 - 3 * TILESIZE, self.screen.get_height() / 2, 6 * TILESIZE, TILESIZE, 'Starte Spiel')

        random_dungeon_button = button(self.screen.get_width() / 2 - 3 * TILESIZE, self.screen.get_height() / 2 + 2 * TILESIZE, 6 * TILESIZE, TILESIZE, 'random Level')

        # (109, 219, 62) (35, 100, 0)
        for row_index, row in enumerate(import_csv_layout(level_0['Grass'])):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        Grass((x, y), [grass])

        while intro_screen:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.isOver(mouse_pos) == True:
                if mouse_pressed[0] == True:
                    intro_screen = False
                    for sprite in grass:
                        sprite.kill()
                    self.type = 'level'
                    self.level = Level(level_0)

            if random_dungeon_button.isOver(mouse_pos) == True:
                if mouse_pressed[0] == True:
                    intro_screen = False
                    for sprite in grass:
                        sprite.kill()
                    self.type = 'level'
                    self.level = Level(level_0, True)
                
            grass.draw(self.screen)
            play_button.draw(self.screen)
            random_dungeon_button.draw(self.screen)
            pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # if event.type == pygame.MOUSEWHEEL:
                #     if self.level.visable_sprites.zoom_scale <= 0.55:
                #         if event.y > 0:
                #             self.level.visable_sprites.zoom_scale += event.y * 0.05
                #     else:
                #         self.level.visable_sprites.zoom_scale += event.y * 0.05
   
            if self.type == 'start_screen':
                self.start_screen()
            else:
                self.screen.fill('black')
                self.level.run()
                pygame.display.update()
                self.clock.tick(FPS)
 
if __name__ == '__main__':
    game = Game()
    game.run()