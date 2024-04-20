import pygame
from pygame import Surface, SurfaceType

import Screen
from Components.ComponentInterface import ComponentInterface
from Components.ComponentUtils import RGBColor
from Components.FontComponent import FontComponent
from Components.HealthComponent import HealthComponent
from Components.PosComponent import PosComponent


class HealthBarComponent(ComponentInterface):
    def __init__(self, health_component: HealthComponent, pos_component: PosComponent):
        self._health_component: HealthComponent = health_component
        self._pos_component: PosComponent = pos_component
        self._text_color: RGBColor = RGBColor.RED
        self._text_background: RGBColor = RGBColor.BLACK
        self._rendered_health: float | None = None
        self._font_component: FontComponent | None = None
        self._screen: Surface | SurfaceType = Screen.get_screen()

    def update(self, dt: float):
        if self._health_component is None:
            print(f" HEALTH COMPONENT IS NONE")
            return
        self._render_health_bar()
        pass

    def _should_update_health_img(self) -> bool:
        if self._rendered_health is None:
            self._rendered_health = self._health_component.get_health()
            return True
        elif self._health_component.get_health() != self._rendered_health:
            self._rendered_health = self._health_component.get_health()
            return True
        return False

    def _render_health_bar(self):
        if self._should_update_health_img() or self._font_component is None:
            self._font_component = FontComponent(f"{self._health_component.get_health()}", True, self._text_color,
                                                 self._text_background)

        entity_pos = self._pos_component.get_pos()
        entity_radius = self._pos_component.get_size()
        text_x = entity_pos.x - self._font_component.get_font_image().get_width() // 2
        offset_y = 20
        text_y = entity_pos.y - entity_radius - offset_y

        self._screen.blit(self._font_component.get_font_image(), (text_x, text_y))
