from actor import *


class Ship(Actor):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)
        self._m_right_speed = 0.0
        self._m_down_speed = 0.0

        # Create AnimSpriteComponent for it
        asc = AnimSpriteComponent(self)
        anim_textures = {game.get_texture("assets/ship01.png"),
                         game.get_texture("assets/ship02.png"),
                         game.get_texture("assets/ship03.png"),
                         game.get_texture("assets/ship04.png")}
        asc.set_anim_textures(anim_textures)

    def update_actor(dt: float) -> None:
