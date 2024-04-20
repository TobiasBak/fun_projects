from Components.ComponentInterface import ComponentInterface
from Entity.EntityInterface import EntityInterface
from Utils.RandomUtils import get_new_id
from World.World import World


class Entity(EntityInterface):
    def __init__(self):
        self._id: int = get_new_id()
        self._components: dict[ComponentInterface.__class__, ComponentInterface] = {}

    def update(self, dt: float) -> None:
        for component in self._components.values():
            component.update(dt)

    def clean_up(self) -> None:
        World.get_world().remove_entity(self)

    def get_component(self, component_name: ComponentInterface.__class__):
        return self._components[component_name]

    def add_component(self, component: ComponentInterface) -> None:
        self._components[component.__class__] = component

    def add_list_of_components(self, components: list[ComponentInterface]) -> None:
        for component in components:
            self.add_component(component)

    def remove_component(self, component_name: ComponentInterface.__class__) -> None:
        del self._components[component_name]

    def get_id(self):
        return self._id

    def set_id(self, new_id: int):
        self._id = new_id
