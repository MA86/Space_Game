import ctypes
import sdl2
from actor import Actor
from anim_sprite_component import AnimSpriteComponent


class Ship(Actor):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)
        self._m_right_speed = 0.0
        self._m_down_speed = 0.0

        # Create a component for Ship
        asc = AnimSpriteComponent(self)
        anim_textures = [game.get_texture(b"assets/ship01.png"),
                         game.get_texture(b"assets/ship02.png"),
                         game.get_texture(b"assets/ship03.png"),
                         game.get_texture(b"assets/ship04.png")]
        asc.set_anim_textures(anim_textures)

    def update_actor(self, dt: float) -> None:
        # Update position
        position = self._m_position     # TODO
        position.x += self._m_right_speed * dt
        position.y += self._m_down_speed * dt

        # Restrict position to left of screen
        if position.x < 25.0:
            position.x = 25.0
        elif position.x > 500.0:
            position.x = 500.0
        if position.y < 25.0:
            position.y = 25.0
        elif position.y > 743.0:
            position.y = 743.0
        # Set position
        self._m_position = position  # TODO

    def process_keyboard(self, keyb_state: ctypes.Array) -> None:
        self._m_right_speed = 0.0
        self._m_down_speed = 0.0

        if keyb_state[sdl2.SDL_SCANCODE_D]:
            self._m_right_speed += 250.0
        if keyb_state[sdl2.SDL_SCANCODE_A]:
            self._m_right_speed -= 250.0
        if keyb_state[sdl2.SDL_SCANCODE_S]:
            self._m_down_speed += 300.0
        if keyb_state[sdl2.SDL_SCANCODE_W]:
            self._m_down_speed -= 300.0
