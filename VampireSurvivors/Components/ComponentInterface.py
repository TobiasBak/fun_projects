
class ComponentInterface:
    def update(self, dt: float) -> None:
        pass

    def get_owner_id(self) -> int:
        pass

    def set_owner_id(self, owner_id: int) -> None:
        pass

    def __str__(self):
        return f"{self.__class__.__name__}"

    def __repr__(self):
        return self.__str__()

