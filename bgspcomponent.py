from spcomponent import SpriteComponent
import sdl2
from vector2d import Vector2D


# Encapsulate background image and its offset
class BGTexture:
    m_texture: sdl2.SDL_Texture = None
    m_offset: Vector2D = Vector2D(0.0, 0.0)


class BGSpriteComponent(SpriteComponent):
    def __init__(self, owner: "Actor", draw_order: int = 10) -> None:
        super().__init__(owner, draw_order)
        self._m_scroll_speed: float = 0.0
        self._m_screen_size: Vector2D = Vector2D(0.0, 0.0)
        self._m_bg_textures: list = []

    # Implements
    def update(self, dt: float) -> None:
        super().update(dt)  # TODO Why???
        for bgt in self._m_bg_textures:
            # Update offset
            bgt.m_offset.x += self._m_scroll_speed * dt
            # If offset is offscreen
            if bgt.m_offset.x < -(self._m_screen_size.x):
                # Reset offset to right of last background texture
                bgt.m_offset.x = (len(self._m_bg_textures) -
                                  1) * self._m_screen_size.x - 1

    # Overrides
    def draw(self, renderer: sdl2.SDL_Renderer) -> None:
        # Draw background textures
        for bgt in self._m_bg_textures:
            print(bgt.m_texture)
            print(bgt.m_offset.x)
            # Create a rectangle based on screen size
            rect = sdl2.SDL_Rect()
            rect.w = int(self._m_screen_size.x)
            rect.h = int(self._m_screen_size.y)
            # Center around owner's position
            rect.x = int(self._m_owner.get_position().x -
                         rect.w / 2 + bgt.m_offset.x)
            rect.y = int(self._m_owner.get_position().y -
                         rect.h / 2 + bgt.m_offset.y)

            # Draw this bg
            sdl2.SDL_RenderCopy(renderer, bgt.m_texture, None, rect)

    def set_bg_textures(self, textures: list) -> None:
        count = 0
        for texture in textures:
            temp = BGTexture()
            temp.m_texture = texture
            # Texture is screen width
            temp.m_offset.x = count * self._m_screen_size.x
            temp.m_offset.y = 0
            self._m_bg_textures.append(temp)
            count += 1

    def set_screen_size(self, size: Vector2D) -> None:
        self._m_screen_size = size

    def set_scroll_speed(self, speed: float) -> None:
        self._m_scroll_speed = speed

    def get_scroll_speed(self) -> float:
        return self._m_scroll_speed
