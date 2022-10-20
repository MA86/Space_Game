import bisect
from enum import Enum
from vector2d import Vector2D


class State(Enum):
    eALIVE = 1
    ePAUSED = 2
    eDEAD = 3


class Actor:
    """ ACTOR BASE CLASS """

    def __init__(self, game: "Game") -> None:
        self._m_state = State.eALIVE

        # Transform
        self._m_position: Vector2D = Vector2D(0.0, 0.0)
        self._m_scale: float = 1.0
        self._m_rotation: float = 0.0

        # Components (sorted)
        self._m_components = []

        self._m_game = game

        # Add to Game's actors-list
        game.add_actor(self)  # TODO

    def delete(self) -> None:
        self._m_game.remove_actor(self)  # TODO
        while len(self._m_components) != 0:
            c = self._m_components.pop()
            c.delete()

    def update(self, dt: float) -> None:
        if self._m_state == State.eALIVE:
            self.update_components(dt)
            self.update_actor(dt)

    def update_components(self, dt: float) -> None:
        for c in self._m_components:
            c.update(dt)  # TODO

    def update_actor(self, dt: float) -> None:
        # Overridable
        pass

    def add_component(self, component: "Component") -> None:
        # Add based on update order
        bisect.insort_left(self._m_components, component)

    def remove_component(self, component: "Component") -> None:
        self._m_components.remove(component)
