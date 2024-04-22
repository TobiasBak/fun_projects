import math
import random

import pygame

import settings


class Circle:
    def __init__(self, position, radius, speed, weight):
        self.position = position
        self.radius = radius
        self.speed = speed
        self.weight = weight

    def move(self, direction, delta_time):
        self.position = [self.position[i] + direction[i] * self.speed * delta_time for i in range(2)]

    def handle_collision(self, other):
        direction = [other.position[i] - self.position[i] for i in range(2)]
        distance = math.hypot(*direction)
        if distance > 0: direction = [i / distance for i in direction]
        colliding_distance = self.radius + other.radius - distance
        displacement = [i * colliding_distance for i in direction]
        self.position = [self.position[i] - displacement[i] * self.weight / (self.weight + other.weight) for i in range(2)]
        other.position = [other.position[i] + displacement[i] * other.weight / (self.weight + other.weight) for i in range(2)]

def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    player = Circle([200, 200], settings.PLAYER_SIZE, settings.PLAYER_SPEED, settings.PLAYER_WEIGHT)
    enemies = [Circle([random.randint(0, settings.SCREEN_WIDTH), random.randint(0, settings.SCREEN_HEIGHT)], settings.ENEMY_SIZE, settings.ENEMY_SPEED, settings.ENEMY_WEIGHT) for _ in range(settings.ENEMY_AMOUNT)]
    clock = pygame.time.Clock()
    time_prev = pygame.time.get_ticks()

    while True:
        time_curr = pygame.time.get_ticks()
        delta_time = (time_curr - time_prev) / 1000.0  # Convert to seconds
        time_prev = time_curr

        if pygame.event.get(pygame.QUIT): break

        for enemy in enemies:
            direction = [player.position[0] - enemy.position[0], player.position[1] - enemy.position[1]]
            distance = math.hypot(*direction)
            if distance > 0: direction = [i / distance for i in direction]
            enemy.move(direction, delta_time)
            if distance < player.radius + enemy.radius:
                player.handle_collision(enemy)

        sub_steps = 8
        for _ in range(sub_steps):
            for i in range(len(enemies)):
                for j in range(i + 1, len(enemies)):
                    direction = [enemies[j].position[0] - enemies[i].position[0], enemies[j].position[1] - enemies[i].position[1]]
                    distance = math.hypot(*direction)
                    if distance < enemies[i].radius + enemies[j].radius:
                        enemies[i].handle_collision(enemies[j])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]: player.position[1] -= player.speed * delta_time
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: player.position[0] -= player.speed * delta_time
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: player.position[1] += player.speed * delta_time
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: player.position[0] += player.speed * delta_time

        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (255, 0, 0), player.position, player.radius)
        for enemy in enemies:
            pygame.draw.circle(screen, (0, 255, 0), enemy.position, enemy.radius)
        pygame.display.flip()
        clock.tick(settings.FPS_LIMIT)
        print(clock.get_fps())

    pygame.quit()

if __name__ == "__main__":
    main()