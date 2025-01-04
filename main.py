import sys
import pygame
import random

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
    def show_menu():
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

    # --- Game Over Screen ---
    def show_game_over():
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over", True, "white")
        game_over_rect = game_over_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        )

        main_menu_text = font.render("Main Menu", True, "white")
        main_menu_rect = main_menu_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5)
        )

        quit_text = font.render("QUIT", True, "white")
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.7))

        in_game_over = True
        while in_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if main_menu_rect.collidepoint(event.pos):
                        in_game_over = False
                        return True  # Return True to restart the game
                    if quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            screen.fill("black")
            screen.blit(game_over_text, game_over_rect)
            screen.blit(main_menu_text, main_menu_rect)
            screen.blit(quit_text, quit_rect)
            pygame.display.flip()
        return False  # Return False to quit the game

    # --- Game Loop ---
    while True:
        show_menu()  # Show the menu initially

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

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            for thing in updatable:
                thing.update(dt)

            screen.fill("black")

            for thing in drawable:
                thing.draw(screen)

            for asteroid in asteroids:
                if asteroid.collisions(player):
                    print("Game over")
                    running = False  # End the current game loop
                    break  # Exit the asteroid collision loop
                for shot in shots:
                    if asteroid.collisions(shot):
                        asteroid.split()
                        shot.kill()

            pygame.display.flip()
            dt = clock.tick(60) / 1000

        if (
            not show_game_over()
        ):  # Show game over screen and check if restart is clicked
            break  # Exit the main game loop if not restarting


if __name__ == "__main__":
    main()
