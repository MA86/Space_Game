from sprite_component import SpriteComponent


class AnimSpriteComponent(SpriteComponent):
    def __init__(self, owner: "Actor", draw_order: int = 100) -> None:
        super().__init__(owner, draw_order)
        self._m_anim_textures = []
        self._m_current_frame = 0.0
        self._m_anim_fps = 24.0

    # Implements
    def update(self, dt: float) -> None:
        super().update(dt)  # TODO Why???

        if len(self._m_anim_textures) > 0:
            # Update current frame
            self._m_current_frame += self._m_anim_fps * dt
            while self._m_current_frame >= len(self._m_anim_textures):
                self._m_current_frame -= len(self._m_anim_textures)

            # Set current texture
            self.set_texture(self._m_anim_textures[int(self._m_current_frame)])

    def set_anim_textures(self, textures: list) -> None:
        self._m_anim_textures = textures
        if len(self._m_anim_textures) > 0:
            # Set first frame as current frame
            self._m_current_frame = 0.0
            self.set_texture(self._m_anim_textures[0])
