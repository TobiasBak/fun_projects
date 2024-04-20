from enum import Enum, auto

from Components.ComponentInterface import ComponentInterface


class EntityType(Enum):
    PLAYER = auto()
    ENEMY = auto()
    BULLET = auto()


class EntityInterface:
    def update(self, dt: float) -> None:
        pass

    def clean_up(self) -> None:
        pass

    def get_component(self, component_name: ComponentInterface.__class__):
        pass

    def add_component(self, component: ComponentInterface) -> None:
        pass

    def add_list_of_components(self, components: list[ComponentInterface]) -> None:
        pass

    def remove_component(self, component_name: ComponentInterface.__class__) -> None:
        pass

    def get_id(self):
        pass

    def set_id(self, new_id: int):
        pass

    def get_type(self) -> EntityType:
        pass

    def set_type(self, new_type: EntityType):
        pass

    def _create_and_add_to_world(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}"

    def __repr__(self):
        return self.__str__()
