

class DefaultBulletConfig:
    damage: float = 10
    speed: float = 500
    radius: float = 50
    color: str = "red"
    lifetime: float = 1


class BulletConfigSword(DefaultBulletConfig):
    speed = 0
    color = "blue"



