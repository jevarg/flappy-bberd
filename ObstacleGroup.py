import pygame
from Obstacle import Obstacle

class ObstacleGroup(pygame.sprite.Group):
    def __init__(self, x, win_height, hole_y, hole_height=200) -> None:
        super().__init__()
        self._top_obstacle = Obstacle(hole_y)
        self._top_obstacle.pos[0] = x
        
        test = win_height - (hole_y + hole_height)
        self._bottom_obstacle = Obstacle(test)
        self._bottom_obstacle.pos[0] = x
        self._bottom_obstacle.pos[1] = hole_y + hole_height

        self.add(self._top_obstacle)
        self.add(self._bottom_obstacle)
