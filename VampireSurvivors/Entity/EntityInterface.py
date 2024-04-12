from pygame import Vector2

from Utils.RandomUtils import get_new_id


class EntityInterface:
    def __init__(self, health: float, color: str, position: Vector2, radius: float, speed: float, weight: float = 1.0):
        self.id: int = get_new_id()
        self.health: float = health
        self.color: str = color
        self.position: Vector2 = position
        self.radius: float = radius
        self.speed: float = speed
        self.weight: float = weight

    def __eq__(self, other):
        position_threshold = 0.01  # Adjust this threshold as needed
        return self.id == other.id and self.health == other.health and \
            self.color == other.color and \
            abs(self.position.x - other.position.x) < position_threshold and \
            abs(self.position.y - other.position.y) < position_threshold and \
            self.radius == other.radius and self.speed == other.speed

    def __hash__(self):
        return hash((self.id, self.health, self.color, self.position.x, self.position.y, self.radius, self.speed))

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen) -> None:
        pass

    def get_position(self) -> Vector2:
        return self.position

    def set_position(self, position: Vector2) -> None:
        self.position = position

    def get_health(self) -> float:
        return self.health

    def set_health(self, health: float) -> None:
        self.health = health

    def get_radius(self) -> float:
        return self.radius

    def set_radius(self, size: float) -> None:
        self.radius = size

    def get_speed(self) -> float:
        return self.speed

    def set_speed(self, speed: float) -> None:
        self.speed = speed

    def move(self, distance: Vector2):
        self.position += distance

    def __str__(self):
        return f"Entity at {self.position} with {self.health} health"

    def __repr__(self):
        return self.__str__()
