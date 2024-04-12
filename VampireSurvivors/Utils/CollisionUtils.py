from Entity.AbstractEntity import AbstractEntity


class CollisionObject:
    def __init__(self, e1: AbstractEntity, e2: AbstractEntity):
        if e1.id < e2.id:
            self.e1 = e1
            self.e2 = e2
        else:
            self.e1 = e2
            self.e2 = e1

    def __eq__(self, other):
        out = False
        if self.e1 == other.e1 and self.e2 == other.e2:
            out = True
        if self.e1 == other.e2 and self.e2 == other.e1:
            out = True
        return out

    def __hash__(self):
        return hash((self.e1, self.e2))

    def __str__(self):
        return f"CollisionObject between {self.e1} and {self.e2}"

    def __repr__(self):
        return self.__str__()


def entities_collide(e1: AbstractEntity, e2: AbstractEntity) -> bool:
    if e1 == e2:
        return False
    elif e1 is None or e2 is None:
        return False
    elif (e1.get_position().distance_to(e2.get_position())) < (e1.get_radius() + e2.get_radius()):
        return True

    return False


def get_collisions(entities: list[AbstractEntity]) -> set[CollisionObject]:
    """Returns a set of tuples containing colliding entities. (Currently n^2 runtime)"""
    collisions: set[CollisionObject] = set()
    for entity in entities:
        if entity is None:
            continue
        for other_entity in entities:
            if entity == other_entity:
                continue
            if entities_collide(entity, other_entity):
                collisions.add(CollisionObject(entity, other_entity))

    return collisions


def get_colliding_distance(e1: AbstractEntity, e2: AbstractEntity) -> float:
    e1_pos = e1.get_position()
    e2_pos = e2.get_position()
    combined_radius = e1.get_radius() + e2.get_radius()
    colliding_distance = e1_pos.distance_to(e2_pos) - combined_radius
    return colliding_distance
