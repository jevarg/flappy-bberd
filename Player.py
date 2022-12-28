import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface([32, 32])
        self.image.fill(pygame.Color(255, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = [64, 0]
        self.gravity = 3
        self.velocity = 0.1
        self._jump_force = 0.1

    def update(self, dt):
        self.rect.y = self.pos[1]
        self.pos[1] += self.gravity * self.velocity * dt
        
        if self.velocity < 1:
            self.velocity += 0.007

    def jump(self):
        self.velocity = -self._jump_force
        pass
