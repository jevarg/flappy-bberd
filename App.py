import pygame
import random
from Player import Player
from ObstacleGroup import ObstacleGroup
from Obstacle import Obstacle
from pygame.locals import *
from enum import Enum
 
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
TRANSPARENT = pygame.Color(0, 0, 0, 0)

display_scale = 3

class GameState(Enum):
    NOT_RUNNING = 0,
    RUNNING = 1,
    GAME_OVER = 2,

class App:
    def __init__(self):
        self._surface = None
        self._needs_exit = False
        self._game_state = GameState.NOT_RUNNING
        self.width, self.height = 320, 240
        self.size = self.width * display_scale, self.height * display_scale
        self._max_num_obstacles = 2
        self._min_spacing = 190
        self._player = Player()
        self._player.rect.x = 40
        self._player.rect.y = 0
        self._sprites = pygame.sprite.Group()
        self._obstacles = list()
        self._background_img = pygame.image.load("assets/background.png")
        self._game_over_img = pygame.image.load("assets/game-over.png")
        self._score = 0

        self._sprites.add(self._player)
 
    def on_init(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont("assets/opensans-regular.ttf", 48)
        self._surface = pygame.surface.Surface([self.width, self.height])
        self._display = pygame.display.set_mode(self.size)
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

    def on_loop(self, dt):
        if self._game_state == GameState.GAME_OVER:
            return

        if self._player.pos[1] > self.height - 32:
            self._game_state = GameState.GAME_OVER

        num_obstacles = len(self._obstacles)
        if num_obstacles < self._max_num_obstacles:
            height = random.randint(0, self.height - 100)
            self._obstacles.append(ObstacleGroup(self.width + (num_obstacles * random.randint(self._min_spacing, self.width)), self.height, height))

        to_remove = list()
        for o in self._obstacles:
            if len(o):
                collision = pygame.sprite.groupcollide(self._sprites, o, False, False)
                if self._player in collision:
                    if isinstance(collision[self._player][0], Obstacle):
                        print('Game Over')
                        self._game_state = GameState.GAME_OVER
                    else:
                        self._score += 1
                        collision[self._player][0].kill()
                o.update(dt)
            else:
                to_remove.append(o)

        for o in to_remove:
            self._obstacles.remove(o)

        self._sprites.update(dt)

    def on_render(self):
        for o in self._obstacles:
            o.draw(self._surface)
        self._sprites.draw(self._surface)

        if self._game_state == GameState.GAME_OVER:
            self._surface.blit(self._game_over_img, (0, 0))

        score_surface = self._font.render(str(self._score), False, WHITE)
        self._surface.blit(score_surface, (2, 0))

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._game_state = False
 
        while not self._needs_exit:
            dt = self._clock.tick(60)
            self._surface.blit(self._background_img, (0, 0))

            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop(dt)
            self.on_render()

            scaled_surf = pygame.transform.scale(self._surface, self.size)
            self._display.blit(scaled_surf, (0, 0))

            pygame.display.flip()
        self.on_cleanup()
 
if __name__ == "__main__" :
    random.seed()
    theApp = App()
    theApp.on_execute()

