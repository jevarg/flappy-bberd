import pygame
import random
from Player import Player
from ObstacleGroup import ObstacleGroup
from pygame.locals import *
from enum import Enum
 
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
TRANSPARENT = pygame.Color(0, 0, 0, 0)

class GameState(Enum):
    NOT_RUNNING = 0,
    RUNNING = 1,
    GAME_OVER = 2,

class App:
    def __init__(self):
        self._display_surf = None
        self._needs_exit = False
        self._game_state = GameState.NOT_RUNNING
        self.size = self.width, self.height = 640, 400
        self._max_num_obstacles = 2
        self._min_spacing = 190
        self._player = Player()
        self._player.rect.x = 40
        self._player.rect.y = 0
        self._sprites = pygame.sprite.Group()
        self._obstacles = list()

        self._sprites.add(self._player)
 
    def on_init(self):
        pygame.init()
        font = pygame.font.SysFont(None, 48)
        self._game_over_img = font.render('Game Over', False, WHITE, TRANSPARENT)
        self._display_surf = pygame.display.set_mode(self.size)
        self._game_state = GameState.RUNNING
 
    def on_event(self, event: pygame.event):
        match event.type:
            case pygame.QUIT:
                self._needs_exit = True
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        self._needs_exit = True
                    case pygame.K_SPACE:
                        self._player.jump()

    def on_loop(self):
        if self._game_state == GameState.GAME_OVER:
            return

        if self._player.pos[1] > self.height - 32:
            self._game_state = GameState.GAME_OVER

        num_obstacles = len(self._obstacles)
        if num_obstacles < self._max_num_obstacles:
            height = random.randint(0, self.height - 200)
            self._obstacles.append(ObstacleGroup(self.width + (num_obstacles * random.randint(self._min_spacing, 300)), self.height, height))

        to_remove = list()
        for o in self._obstacles:
            if len(o):
                collision = pygame.sprite.groupcollide(self._sprites, o, False, False)
                if len(collision) > 0:
                    print('Game Over')
                    self._game_state = GameState.GAME_OVER
                o.update(1)
            else:
                to_remove.append(o)

        for o in to_remove:
            self._obstacles.remove(o)

        self._sprites.update()

    def on_render(self):
        for o in self._obstacles:
            o.draw(self._display_surf)
        self._sprites.draw(self._display_surf)

        if self._game_state == GameState.GAME_OVER:
            r = self._game_over_img.get_rect()
            r.center = (self.width / 2, self.height / 2)
            self._display_surf.blit(self._game_over_img, r)

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._game_state = False
 
        while not self._needs_exit:
            self._display_surf.fill(0)

            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

            pygame.display.flip()
        self.on_cleanup()
 
if __name__ == "__main__" :
    random.seed()
    theApp = App()
    theApp.on_execute()

