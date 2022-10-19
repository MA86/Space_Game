from enum import Enum
from vector2d import Vector2D


class Actor:
    """ ACTOR BASE CLASS """

    def __init__(self, game: "Game") -> None:
        class State(Enum):
            eALIVE = 1
            ePAUSED = 2
            eDEAD = 3
        self._m_state = State.eALIVE

        # Transform
        self._m_position = Vector2D(0.0, 0.0)
        self._m_scale = 1.0
        self._m_rotation = 0.0

        self.m_game = game
