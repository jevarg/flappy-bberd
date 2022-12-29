import pygame
from Obstacle import Obstacle

class ObstacleGroup(pygame.sprite.Group):
    def __init__(self, x, win_height, hole_y, hole_height=100) -> None:
        super().__init__()
        self._top_obstacle = Obstacle(hole_y)
        self._top_obstacle.pos[0] = x
        
        self._bottom_obstacle = Obstacle(win_height - hole_y + hole_height)
        self._bottom_obstacle.pos[0] = x
        self._bottom_obstacle.pos[1] = hole_y + hole_height

        self._score_trigger = pygame.sprite.Sprite()
        self._score_trigger.rect = pygame.rect.Rect(self._top_obstacle.rect.centerx, hole_y, 1, hole_height)
        self._score_trigger.image = pygame.surface.Surface((0, 0))
        
        # DEBUG draw the trigger
        # self._score_trigger.image = pygame.surface.Surface(self._score_trigger.rect.size)
        # self._score_trigger.image.fill((255, 255, 0))


        self.add(self._top_obstacle)
        self.add(self._bottom_obstacle)
        self.add(self._score_trigger)

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        self._score_trigger.rect.x = self._top_obstacle.rect.centerx