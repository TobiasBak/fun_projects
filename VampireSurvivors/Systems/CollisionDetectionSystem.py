import settings
from Events.EventManager import EventManager
from Events.Events import FindCollisionEvent, CollisionEvent
from Systems.CollisionGrid import CollisionCell, CollisionGrid
from Systems.SystemInterface import SystemInterface
from World.CollisionObject import CollisionPair, CollisionObject
from World.World import World


class CollisionDetectionSystem(SystemInterface):
    def __init__(self):
        self._event_manager = EventManager.get_instance()
        self._event_manager.add_listener(FindCollisionEvent, self._find_collisions)
        self.world = World.get_world()
        self.collision_objects = []
        self.largets_radius = 0
        self.collision_grid: CollisionGrid = None
        self.create_new_grid = False

    def update(self, dt: float):
        self.collision_objects = self.world.get_collision_objects()
        if len(self.collision_objects) == 0:
            return
        self._create_new_grid_if_necessary()
        self.update_with_sub_steps(dt, 8)

    def _create_new_grid_if_necessary(self):
        for collision_object in self.collision_objects:
            if collision_object.radius > self.largets_radius:
                self.largets_radius = collision_object.radius
                self.create_new_grid = True
        if self.collision_grid is None or self.create_new_grid:
            self.collision_grid = CollisionGrid(settings.GAME_WIDTH, settings.GAME_HEIGHT, self.largets_radius * 2)
            self.create_new_grid = False
            print("CREATED NEW GRID, SHOULD HAPPEN RARELY")

    def update_with_sub_steps(self, dt: float, sub_steps: int):
        sub_dt = dt / sub_steps
        for _ in range(sub_steps):
            self.collision_grid.add_list_of_collision_objects(self.collision_objects)
            self._event_manager.dispatch_event(FindCollisionEvent(sub_dt))

    def _find_collisions(self, event: FindCollisionEvent):
        for cell in self.collision_grid.grid.values():
            self.processCell(cell, cell.index)

    def processCell(self, collision_cell: CollisionCell, index: (int, int)):
        collision_objects = collision_cell.get_collision_objects()
        for collision_object in collision_objects:
            for x in range(index[0] - 1, index[0] + 2):
                for y in range(index[1] - 1, index[1] + 2):
                    self.check_collisions(collision_object, self.collision_grid.grid[(x, y)])

    def check_collisions(self, co: CollisionObject, cell: CollisionCell):
        for other_co in cell.get_collision_objects():
            if co.collides_with(other_co):
                self._event_manager.dispatch_event(CollisionEvent(CollisionPair(co, other_co)))
