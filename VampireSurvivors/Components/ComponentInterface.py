from pygame import Vector2


class ComponentInterface:
    def update(self, dt):
        pass

    def render(self, screen):
        pass

    def clean_up(self):
        pass

    def get_owner_id(self) -> id:
        pass

    def get_pos(self) -> Vector2:
        pass
