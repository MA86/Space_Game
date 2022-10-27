from component import Component
import sdl2
import math
import ctypes


class SpriteComponent(Component):
    def __init__(self, owner: "Actor", draw_order: int = 100) -> None:
        super().__init__(owner)
        self.m_texture: sdl2.SDL_Texture = None
        self.m_draw_order: int = draw_order
        self.m_text_width = ctypes.c_int(0)
        self.m_text_height = ctypes.c_int(0)

        self._m_owner.get_game().add_sprite(self)

    def delete(self) -> None:
        # Remove from owner's list
        super().delete()
        # Remove from game's list
        self._m_owner.get_game().remove_sprite(self)

    def draw(self, renderer: sdl2.SDL_Renderer) -> None:
        if self.m_texture != None:
            # Create a rectangle based on owner's transform
            rect = sdl2.SDL_Rect()
            rect.w = int(self.m_text_width.value *
                         self._m_owner.get_scale())
            rect.h = int(self.m_text_height.value * self._m_owner.get_scale())
            rect.x = int(self._m_owner.get_position().x - rect.w / 2)
            rect.y = int(self._m_owner.get_position().y - rect.h / 2)

            # Draw (convert rad to deg, and clockwise to counter)
            sdl2.SDL_RenderCopyEx(renderer,
                                  self.m_texture,
                                  None,
                                  rect,
                                  math.degrees(self._m_owner.get_rotation()),
                                  None,
                                  sdl2.SDL_FLIP_NONE)

    def set_texture(self, texture: sdl2.SDL_Texture) -> None:
        self.m_texture = texture

        # Specify height/width for texture
        sdl2.SDL_QueryTexture(texture, None, None,
                              ctypes.byref(self.m_text_width), ctypes.byref(self.m_text_height))

    def get_draw_order(self) -> int:
        return self.m_draw_order

    def get_text_height(self) -> int:
        return self.m_text_height

    def get_text_width(self) -> int:
        return self.m_text_width
