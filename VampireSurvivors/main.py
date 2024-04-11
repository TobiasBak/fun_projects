import pygame

from Entity.EntityFactory import DefaultPlayerFactory
from Entity.EntityInterface import EntityInterface
from Systems.SystemFactory import InitialSystems
from World.World import World
from screen import get_screen

# pygame setup
pygame.init()
screen = get_screen()
clock = pygame.time.Clock()


class AbstractInterface:
    pass


def main():
    running = True
    print(f"screen width: {screen.get_width()} height: {screen.get_height()}")

    InitialSystems().create_and_add_system()

    world: World = World.get_world()
    player: EntityInterface = DefaultPlayerFactory().create_entity()
    world.add_player(player)

    dt = 0

    print_count = 0

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        # RENDER YOUR GAME HERE
        world.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
        world.update(dt)

        print_count += 1

        if print_count % 60 == 0:
            print(world)

    pygame.quit()


if __name__ == "__main__":
    main()
