class EnemyType:
    radius: float
    health: float
    speed: float
    color: str


class DefaultEnemyType(EnemyType):
    radius: float = 10
    health: float = 20
    speed: float = 50
    color: str = "red"
