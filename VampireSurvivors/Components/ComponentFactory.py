from pygame import Vector2

from Components.CollisionComponent import CollisionComponent
from Components.ComponentInterface import ComponentInterface
from Components.ComponentUtils import RGBColor, GeometryType
from Components.GeometrySpriteComponent import GeometrySpriteComponent
from Components.HealthBarComponent import HealthBarComponent
from Components.HealthComponent import HealthComponent
from Components.PosComponent import PosComponent
from Components.WASDComponent import WASDComponent
from Components.WeaponCollisionComponent import CollisionWeaponComponent
from Components.WeaponSwordComponent import SwordWeaponComponent

from GameConfig import GameConfig


class ComponentFactory:
    def create_components(self) -> list[ComponentInterface]:
        pass


class DefaultLivingEntityComponentFactory(ComponentFactory):
    def __init__(self, health: float = 100):
        self.health = health

    def create_components(self) -> list[ComponentInterface]:
        pass


class DefaultPlayerComponentFactory(ComponentFactory):
    def create_components(self) -> list[ComponentInterface]:
        game_config = GameConfig.get_gameconfig()
        pos_component = PosComponent(game_config.PLAYER_START_POS, game_config.PLAYER_SIZE)
        return [
            pos_component,
            WASDComponent(pos_component, game_config.PLAYER_SPEED),
            GeometrySpriteComponent(GeometryType.Circle, pos_component, RGBColor.BLACK),
        ]


class DefaultEnemyComponentFactory(DefaultLivingEntityComponentFactory):
    # def __init__(self, health: float = 20, damage: float = 2):
    #     super().__init__(health, damage)
    pass


class DefaultBulletEntityComponentFactory(ComponentFactory):
    # def __init__(self):
    #     super().__init__()
    #
    # def create_components(self, owner: AbstractEntity) -> None:
    #     CollisionComponent(owner, owner.radius, owner.weight)
    pass
