import sys
import pygame
import random
import asteroidfield
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # --- Menu Screen ---
    font = pygame.font.Font(None, 74)
    title_text = font.render("Asteroids", True, "white")
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))

    start_text = font.render("Start", True, "white")
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5))

    quit_text = font.render("QUIT", True, "white")
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.7))

    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    in_menu = False
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill("black")
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()

    # GAME LOGIC

    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    player = Player(x, y)
    asteroidfield = AsteroidField()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for thing in updatable:
            thing.update(dt)

        screen.fill("black")

        for thing in drawable:
            thing.draw(screen)

        for asteroid in asteroids:
            if asteroid.collisions(player):
                print("Game over")
                sys.exit("bum")
            for shot in shots:
                if asteroid.collisions(shot):
                    # asteroid.kill()
                    asteroid.split()
                    shot.kill()

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
