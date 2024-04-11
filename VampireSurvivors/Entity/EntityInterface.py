from pygame import Vector2


class EntityInterface:
    def __init__(self, health: float, color: str, position: Vector2, size: float, speed: float):
        self.health: float = health
        self.color: str = color
        self.position: Vector2 = position
        self.size: float = size
        self.speed: float = speed

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

    def get_size(self) -> float:
        return self.size

    def set_size(self, size: float) -> None:
        self.size = size

    def get_speed(self) -> float:
        return self.speed

    def set_speed(self, speed: float) -> None:
        self.speed = speed

    def __str__(self):
        return f"Entity at {self.position} with {self.health} health"

    def __repr__(self):
        return self.__str__()
