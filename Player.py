import pygame

max_rot = 140
max_velocity = 1

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self._base_img = pygame.image.load('assets/player.png')
        self.image = self._base_img
        self.rect = self.image.get_rect()
        self.pos = [64, 0]
        self.gravity = 2
        self.velocity = 0.1
        self._jump_force = 0.1

    def update(self, dt):
        self.rect.y = self.pos[1]
        self.pos[1] += self.gravity * self.velocity * dt
        
        self.velocity = min(self.velocity + 0.007, max_velocity)
        self.image = pygame.transform.rotate(self._base_img, -(max_rot * self.velocity))

    def jump(self):
        self.velocity = -self._jump_force
        pass
