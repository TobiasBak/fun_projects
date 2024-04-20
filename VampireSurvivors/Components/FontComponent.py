from enum import Enum

from Components.ComponentInterface import ComponentInterface
from Components.ComponentUtils import RGBColor


class FontComponent(ComponentInterface):
    def __init__(self, text: str, SOMETHING: bool, text_color: RGBColor, background_color: RGBColor):
        self._text = text
        self._SOMETHING = SOMETHING
        self._text_color = text_color
        self._background_color = background_color
        self._font_image: Surface | SurfaceType = self._generate_new_font()

    def update(self, dt: float) -> None:
        pass

    def clean_up(self) -> None:
        pass

    def _generate_new_font(self):
        font = pygame._font_image.SysFont(None, 24)
        img = font.render(f'{self.rendered_health}', self._SOMETHING, self._text_color, self._background_color)
        return img

    def get_font_image(self) -> Surface | SurfaceType:
        return self._font_image

    def set_font_image(self, font_image: Surface | SurfaceType) -> None:
        self._font_image = font_image
