import pygame

game_speed = 0.5
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, height) -> None:
        super().__init__()
        # self.image = pygame.image.load('assets/obstacle.png')
        self.image = pygame.Surface([32, height])
        self.image.fill(pygame.Color(0, 255, 0))
        self.rect = self.image.get_rect()
        self.pos = [0, 0]

    def update(self, dt) -> None:
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        self.pos[0] -= game_speed * dt

        if self.pos[0] + 32 < 0:
            self.kill()
