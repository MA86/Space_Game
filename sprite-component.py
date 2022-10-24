from component import *
import sdl2
import math


class SpriteComponent(Component):
    def __init__(self, owner: "Actor", draw_order: int = 100) -> None:
        super().__init__(owner)
        self.m_texture: sdl2.SDL_Texture = None
        self.m_draw_order: int = draw_order
        self.m_text_width: int = 0
        self.m_text_height: int = 0

        self._m_owner._m_game.add_sprite(self)  # TODO use GetGame() instead

    # Redefine compare for bisect.insort
    def __lt__(self, other: "Component") -> bool:
        return self._m_draw_order < other._m_draw_order

    def delete(self) -> None:
        # Remove from owner's list
        super().delete()
        # Remove from game's list
        self._m_owner._m_game.remove_sprite(self)  # TODO same as above

    def draw(self, renderer: sdl2.SDL_Renderer) -> None:
        if self.m_texture != None:
            # Create a rectangle based on owner's transform
            rect = sdl2.SDL_Rect()
            rect.w = int(self.m_text_width *
                         self._m_owner._m_scale)                    # TODO as above
            rect.h = int(self.m_text_height * self._m_owner._m_scale)
            rect.x = int(self._m_owner._m_position.x - rect.w / 2)
            rect.y = int(self._m_owner._m_position.y - rect.h / 2)

            # Draw (convert rad to deg, and clockwise to counter)
            sdl2.SDL_RenderCopyEx(renderer,
                                  self.m_texture,
                                  None,
                                  rect,
                                  # TODO above
                                  math.degrees(self._m_owner._m_rotation),
                                  None,
                                  sdl2.SDL_FLIP_NONE)

    def set_texture(self, texture: sdl2.SDL_Texture) -> None:
        self.m_texture = texture

        # Specify height/width for texture
        sdl2.SDL_QueryTexture(texture, None, None,
                              self.m_text_width, self.m_text_height)
