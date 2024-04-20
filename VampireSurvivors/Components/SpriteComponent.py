import Screen
from Components.ComponentInterface import ComponentInterface
from Components.PosComponent import PosComponent


class SpriteComponent(ComponentInterface):
    def __init__(self, path: str, pos_component: PosComponent):
        self.path = path
        self.pos_component = pos_component
        self.image = None
        self._screen = Screen.get_screen()

    def update(self, dt: float) -> None:
        self._screen.blit(self.image, self.pos_component.get_pos() - Vector2(self.radius / 2, self.radius / 2))

    def _generate_new_img(self):
        img = pygame.image.load(self.path)
        img = self._scale_image_to_size(img, self.pos_component.get_size())
        return img

    def _scale_image_to_size(self, img, size: float):
        return transform.scale(img, (int(size), int(size)))

    def get_path(self) -> str:
        return self.path

    def set_path(self, new_path: str):
        self.path = new_path


