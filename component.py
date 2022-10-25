class Component:
    """ COMPONENT BASE CLASS """

    def __init__(self, owner: "Actor", update_order: int = 100) -> None:
        self._m_owner = owner
        self._m_update_order = update_order

        owner.add_component(self)

    # Redefine compare for bisect.insort
    def __lt__(self, other: "Component") -> bool:
        return self._m_update_order < other._m_update_order

    def delete(self) -> None:
        self._m_owner.remove_component(self)

    def update(self, dt: float) -> None:
        # Implementable
        pass

    def get_update_order(self) -> int:
        return self._m_update_order
