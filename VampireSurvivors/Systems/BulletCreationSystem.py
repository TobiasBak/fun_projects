from Entity.EntityFactory import BulletFactory
from Events.Events import BulletEvent
from Systems.SystemInterface import SystemInterface


class BulletCreationSystem(SystemInterface):
    def __init__(self):
        super().__init__()
        self.event_manager.add_listener(BulletEvent, self._create_bullet)

    def _create_bullet(self, event: BulletEvent):
        print("Creating bullet")
        source = event.source
        pos = source.get_pos().copy()
        bullet_config = event.bullet_config
        BulletFactory(bullet_config).create_entity(pos)

