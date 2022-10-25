from spcomponent import SpriteComponent
import sdl2
from vector2d import Vector2D


# Encapsulate background image and its offset
class BGTexture:
    m_Texture: sdl2.SDL_Texture = None
    m_offset: Vector2D = Vector2D(0.0, 0.0)


class BGSpriteComponent(SpriteComponent):
    def __init__(self, owner: "Actor", draw_order: int) -> None:
        super().__init__(owner, draw_order)
        self._m_scroll_speed: float = 0.0
        self._m_screen_size: "Vector2D"
        self._m_bg_textures: list = []

    # Implements
    def update(self, dt: float) -> None:
        super().update(dt)  # TODO Why???
        for bg in self._m_bg_textures:
            # Update offset
            bg.
