from pygame import draw

import Screen
import settings
from Components.ComponentInterface import ComponentInterface
from Components.ComponentUtils import GeometryType, RGBColor
from Components.PosComponent import PosComponent


class GeometrySpriteComponent(ComponentInterface):
    def __init__(self, geometry_type: GeometryType, pos_component: PosComponent, color: RGBColor):
        self._geometry_type: GeometryType = geometry_type
        self._pos_component: PosComponent = pos_component
        self._color: RGBColor = color

    def update(self, dt: float) -> None:
        if not settings.RENDER_HITBOXES:
            return

        match self._geometry_type:
            case GeometryType.Circle:
                draw.circle(Screen.get_screen(), self._color.value, self._pos_component.get_pos(), self._pos_component.get_size())
            case _:
                return
