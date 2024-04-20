from Components.ComponentUtils import RGBColor


class EnemyType:
    radius: float
    health: float
    speed: float
    color: str
    weight: float


class DefaultEnemyType(EnemyType):
    radius: float = 30
    health: float = 20
    speed: float = 100
    color: str = RGBColor.RED.value
    weight: float = 1



