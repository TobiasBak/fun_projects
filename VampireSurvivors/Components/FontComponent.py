from enum import Enum

from pygame import Surface, SurfaceType, font

from Components.ComponentInterface import ComponentInterface
from Components.ComponentUtils import RGBColor


class FontComponent(ComponentInterface):
    def __init__(self, text: str, text_color: RGBColor, background_color: RGBColor, anti_alias: bool = True):
        self._text = text
        self._anti_alias = anti_alias
        self._text_color = text_color
        self._background_color = background_color
        self._font_image: Surface | SurfaceType = self._generate_new_font()

    def update(self, dt: float) -> None:
        pass

    def clean_up(self) -> None:
        pass

    def _generate_new_font(self):
        _font = font.SysFont(None, 24)
        img = _font.render(f'{self._text}', self._anti_alias, self._text_color.value, self._background_color.value)
        return img

    def get_font_image(self) -> Surface | SurfaceType:
        return self._font_image

    def set_font_image(self, font_image: Surface | SurfaceType) -> None:
        self._font_image = font_image
