import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        print(f"Creating asteroid at ({x}, {y}) with radius {radius}")

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            self.random_angle = random.uniform(20, 50)
            self.first_vector = pygame.math.Vector2.rotate(
                self.velocity, self.random_angle
            )
            self.second_vector = pygame.math.Vector2.rotate(
                self.velocity, -(self.random_angle)
            )
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            first_asteroid.velocity = self.first_vector
            first_asteroid.velocity *= 1.2
            second_asteroid.velocity = self.second_vector
            second_asteroid.velocity *= 1.2
