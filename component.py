class Component:
    """ COMPONENT BASE CLASS """

    def __init__(self, owner: "Actor", update_order: int = 100) -> None:
        self._m_owner: "Actor" = owner
        self._m_update_order: int = update_order

        # Add self to owner's list
        owner.add_component(self)

    def delete(self) -> None:
        self._m_owner.remove_component(self)

    def update(self, dt: float) -> None:
        # Implementable
        pass

    def get_update_order(self) -> int:
        return self._m_update_order
