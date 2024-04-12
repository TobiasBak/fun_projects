import pygame
from pygame import Surface, SurfaceType

from Components.ComponentInterface import ComponentInterface
from Components.HealthComponent import HealthComponent

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)


class HealthBarComponent(ComponentInterface):
    def __init__(self, entity):
        super().__init__(entity)
        self.rendered_health: int | None = None
        self.health_img: Surface | SurfaceType | None = None

    def render(self, screen: Surface | SurfaceType):
        health_component = self.owner.get_component(HealthComponent)
        if health_component is not None:
            self._render_health_bar(screen, health_component)

    def _should_update_health_img(self, health_component: HealthComponent) -> bool:
        if self.rendered_health is None:
            self.rendered_health = health_component.get_health()
            return True
        elif health_component.get_health() != self.rendered_health:
            self.rendered_health = health_component.get_health()
            return True
        return False

    def _generate_new_health_img(self):
        font = pygame.font.SysFont(None, 24)
        img = font.render(f'{self.rendered_health}', True, RED, BLACK)
        return img

    def _render_health_bar(self, screen, health_component: HealthComponent):
        if self._should_update_health_img(health_component) or self.health_img is None:
            self.health_img = self._generate_new_health_img()

        entity_pos = self.owner.get_position()
        entity_radius = self.owner.get_radius()
        text_x = entity_pos.x - self.health_img.get_width() // 2
        offset_y = 20
        text_y = entity_pos.y - entity_radius - offset_y

        screen.blit(self.health_img, (text_x, text_y))
