import math
import random

import pygame

import settings


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, obj):
        return (self.x - self.w / 2 <= obj.position[0] <= self.x + self.w / 2 and
                self.y - self.h / 2 <= obj.position[1] <= self.y + self.h / 2)

    def intersects(self, range):
        return not (range.x - range.w / 2 > self.x + self.w / 2 or
                    range.x + range.w / 2 < self.x - self.w / 2 or
                    range.y - range.h / 2 > self.y + self.h / 2 or
                    range.y + range.h / 2 < self.y - self.h / 2)


class Circle:
    def __init__(self, position, radius, speed, weight):
        self.position = position
        self.radius = radius
        self.speed = speed
        self.weight = weight
        self.velocity = [0, 0]  # Initialize velocity to [0, 0]
        self.direction = None
        self.distance = None

    def move(self, delta_time):
        self.position = [self.position[i] + self.velocity[i] * delta_time for i in
                         range(2)]  # Update position based on velocity and delta_time

    def move_towards(self, target, delta_time):
        direction = [target[i] - self.position[i] for i in range(2)]
        distance = math.hypot(*direction)
        if distance > 0: direction = [i / distance for i in direction]
        self.velocity = [direction[i] * self.speed for i in range(2)]  # Update velocity based on direction and speed
        self.move(delta_time)

    def collides_with(self, other):
        self.direction = [other.position[i] - self.position[i] for i in range(2)]
        self.distance = math.hypot(*self.direction)
        return self.distance < self.radius + other.radius

    def handle_collision(self, other):
        if self.distance > 0: self.direction = [i / self.distance for i in self.direction]
        colliding_distance = self.radius + other.radius - self.distance
        if colliding_distance > 0:
            # Calculate the overlap and move the entities away from each other
            overlap = 0.5 * (colliding_distance + 1)
            self.position = [self.position[i] - overlap * self.direction[i] for i in range(2)]
            other.position = [other.position[i] + overlap * self.direction[i] for i in range(2)]


class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.objects = []
        self.divided = False

    def insert(self, obj):
        if not self.boundary.contains(obj):
            return False

        if len(self.objects) < self.capacity:
            self.objects.append(obj)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northwest.insert(obj):
                return True
            elif self.northeast.insert(obj):
                return True
            elif self.southwest.insert(obj):
                return True
            elif self.southeast.insert(obj):
                return True

    def subdivide(self):
        nw = Rectangle(self.boundary.x - self.boundary.w / 4, self.boundary.y - self.boundary.h / 4,
                       self.boundary.w / 2, self.boundary.h / 2)
        ne = Rectangle(self.boundary.x + self.boundary.w / 4, self.boundary.y - self.boundary.h / 4,
                       self.boundary.w / 2, self.boundary.h / 2)
        sw = Rectangle(self.boundary.x - self.boundary.w / 4, self.boundary.y + self.boundary.h / 4,
                       self.boundary.w / 2, self.boundary.h / 2)
        se = Rectangle(self.boundary.x + self.boundary.w / 4, self.boundary.y + self.boundary.h / 4,
                       self.boundary.w / 2, self.boundary.h / 2)

        self.northwest = QuadTree(nw, self.capacity)
        self.northeast = QuadTree(ne, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)

        self.divided = True

    def query(self, range, found):
        if not self.boundary.intersects(range):
            return found
        else:
            for obj in self.objects:
                if range.contains(obj):
                    found.append(obj)

            if self.divided:
                self.northwest.query(range, found)
                self.northeast.query(range, found)
                self.southwest.query(range, found)
                self.southeast.query(range, found)

        return found


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    player = Circle([200, 200], settings.PLAYER_SIZE, settings.PLAYER_SPEED, settings.PLAYER_WEIGHT)
    enemies = [Circle([random.randint(0, settings.SCREEN_WIDTH), random.randint(0, settings.SCREEN_HEIGHT)],
                      settings.ENEMY_SIZE, settings.ENEMY_SPEED, settings.ENEMY_WEIGHT) for _ in
               range(settings.ENEMY_AMOUNT)]
    entities = [player] + enemies
    boundary = Rectangle(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2, settings.SCREEN_WIDTH,
                         settings.SCREEN_HEIGHT)
    clock = pygame.time.Clock()
    time_prev = pygame.time.get_ticks()

    while True:
        time_curr = pygame.time.get_ticks()
        delta_time = (time_curr - time_prev) / 1000.0  # Convert to seconds
        time_prev = time_curr
        if pygame.event.get(pygame.QUIT): break

        substeps = 8
        for _ in range(substeps):
            quadtree = QuadTree(boundary, 4)  # Create a new quadtree for each frame
            for entity in entities:
                quadtree.insert(entity)  # Insert the entities into the quadtree

            for entity in entities:
                range_ = Rectangle(entity.position[0], entity.position[1], entity.radius * 2 * 2, entity.radius * 2 * 2)
                nearby_enemies = quadtree.query(range_, [])
                for other in nearby_enemies:
                    if entity != other and entity.collides_with(other):
                        entity.handle_collision(other)

        for enemy in enemies:
            enemy.move_towards(player.position, delta_time)

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
