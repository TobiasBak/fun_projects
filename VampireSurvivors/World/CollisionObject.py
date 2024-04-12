

class CollisionObject:
    """ All entities and components can create CollisionObjects to check for collisions."""
    def __init__(self, owner_id: int, pos, pos_offset, radius, ):
        self.owner_id = owner_id
        self.x = pos[0] + pos_offset[0]
        self.y = pos[1] + pos_offset[1]
        self.radius = radius

    def draw(self, screen):
        pass

    def _check_collision(self, other):
        if self.x < other.x + other.width and self.x + self.width > other.x and self.y < other.y + other.height and self.y + self.height > other.y:
            return True
        return False