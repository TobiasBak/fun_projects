from World.CollisionObject import CollisionObject


class CollisionCell:
    _cell_capacity = 4
    _max_cell_index = _cell_capacity - 1

    def __init__(self, index: (int, int), width: float, height: float):
        self.index = index
        self.width = width
        self.height = height
        self.object_count = 0
        self.collision_objects: dict[int, CollisionObject] = {}

    def add_collision_object(self, co: CollisionObject):
        self.collision_objects[self.object_count] = co
        self.object_count += 1 < self._cell_capacity

    def get_collision_objects(self):
        return self.collision_objects.values()

    def clear(self):
        self.collision_objects.clear()


class CollisionGrid:
    def __init__(self, width: float, height: float, cell_size: float):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid_width = int(width / cell_size)
        self.grid_height = int(height / cell_size)
        self.grid: dict[(int, int), CollisionCell] = {}
        self._create_grid()

    def _create_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                self.grid[(x, y)] = CollisionCell((x, y), self.cell_size, self.cell_size)

    def add_collision_object(self, co: CollisionObject):
        x = int(co.pos.x / self.cell_size)
        y = int(co.pos.y / self.cell_size)
        if self.grid_width - 1 > x > 0 and self.grid_height - 1 > y > 0:
            self.grid[(x, y)].add_collision_object(co)

    def add_list_of_collision_objects(self, collision_objects: list[CollisionObject]):
        self.clear()
        for co in collision_objects:
            self.add_collision_object(co)

    def get_cell(self, co: CollisionObject):
        x = int(co.pos.x / self.cell_size)
        y = int(co.pos.y / self.cell_size)
        return self.grid[(x, y)]

    def clear(self):
        for cell in self.grid.values():
            cell.clear()
