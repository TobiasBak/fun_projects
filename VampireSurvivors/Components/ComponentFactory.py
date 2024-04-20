from pygame import Vector2

from Components.CollisionComponent import CollisionComponent
from Components.ComponentInterface import ComponentInterface
from Components.ComponentUtils import RGBColor, GeometryType
from Components.GeometrySpriteComponent import GeometrySpriteComponent
from Components.HealthBarComponent import HealthBarComponent
from Components.HealthComponent import HealthComponent
from Components.MoveToTargetComponent import MoveToTargetComponent
from Components.PosComponent import PosComponent
from Components.WASDComponent import WASDComponent
from Entity.EnemyTypes import EnemyType

from GameConfig import GameConfig
from World.World import World


class ComponentFactory:
    def create_components(self, owner_id: int, pos: Vector2) -> list[ComponentInterface]:
        pass


class PlayerComponentFactory(ComponentFactory):
    def create_components(self, owner_id: int, pos: Vector2) -> list[ComponentInterface]:
        game_config = GameConfig.get_gameconfig()
        pos_component = PosComponent(game_config.PLAYER_START_POS, game_config.PLAYER_SIZE)
        health_component = HealthComponent(game_config.PLAYER_START_HEALTH)
        return [
            pos_component,
            WASDComponent(pos_component, game_config.PLAYER_SPEED),
            GeometrySpriteComponent(GeometryType.Circle, pos_component, RGBColor.BLACK),
            health_component,
            HealthBarComponent(health_component, pos_component),
            CollisionComponent(owner_id, pos_component, game_config.PLAYER_WEIGHT),
        ]


class EnemyComponentFactory(ComponentFactory):
    def __init__(self, enemy_type: EnemyType):
        self.enemy_type = enemy_type

    def create_components(self, owner_id: int, pos: Vector2) -> list[ComponentInterface]:
        pos_component = PosComponent(pos, self.enemy_type.radius)
        health_component = HealthComponent(self.enemy_type.health)
        player_pos_component = World.get_world().get_player().get_component(PosComponent)
        return [
            pos_component,
            health_component,
            MoveToTargetComponent(pos_component, player_pos_component, self.enemy_type.speed),
            GeometrySpriteComponent(GeometryType.Circle, pos_component, RGBColor.RED),
            HealthBarComponent(health_component, pos_component),
            CollisionComponent(owner_id, pos_component, self.enemy_type.weight),
        ]


class BulletEntityComponentFactory(ComponentFactory):
    # def __init__(self):
    #     super().__init__()
    #
    # def create_components(self, owner: AbstractEntity) -> None:
    #     CollisionComponent(owner, owner.radius, owner.weight)
    pass
