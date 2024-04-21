import pygame

from Factories.EntityFactory import PlayerFactory
from Systems.SystemFactory import InitialSystems
from World.World import World
from settings import FPS_LIMIT
from Screen import get_screen

# pygame setup
pygame.init()
screen = get_screen()
clock = pygame.time.Clock()


class AbstractInterface:
    pass


def main():
    running = True

    InitialSystems().create_and_add_systems()

    world: World = World.get_world()
    player = PlayerFactory().create_entity()
    world.add_player(player)

    print_count = 0

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(FPS_LIMIT) / 1000
        world.update(dt)

        # flip() the display to put your work on screen
        pygame.display.flip()

        print_count += 1

        if print_count % 60 == 0:
            print(world)
            print(f"FPS: {clock.get_fps()}")

    pygame.quit()


if __name__ == "__main__":
    main()
