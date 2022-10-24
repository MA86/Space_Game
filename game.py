import sdl2dll
import sdl2
import sdl2.sdlimage as sdlimage
import bisect
from vector2d import *


class Game:
    def __init__(self):
        # TODO add type hinting after it works
        self._m_window = None
        self._m_renderer = None
        self._m_running = True
        self._m_time_then = 0.0

        self._m_textures = {}
        self._m_actors = []
        self._m_pending_actors = []
        self._m_sprites = []

        self._m_updating_actors = False

        # Game objects
        self._m_ship: "Ship"

    # These are public methods:

    def initialize(self) -> bool:
        # Initialize graphics subsystem
        result = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_AUDIO)
        if result != 0:
            sdl2.SDL_Log("SDL initialization failed: ",
                         sdl2.SDL_GetError())
            return False

        # Create window
        self._m_window = sdl2.SDL_CreateWindow(b"Spaceship Shooter",
                                               sdl2.SDL_WINDOWPOS_CENTERED,
                                               sdl2.SDL_WINDOWPOS_CENTERED, 1024, 768, 0)
        if self._m_window == None:
            sdl2.SDL_Log("Window failed: ", sdl2.SDL_GetError())
            return False

        # Create renderer
        self._m_renderer = sdl2.SDL_CreateRenderer(self._m_window,
                                                   -1,
                                                   sdl2.SDL_RENDERER_ACCELERATED |
                                                   sdl2.SDL_RENDERER_PRESENTVSYNC)
        if self._m_renderer == None:
            sdl2.SDL_Log("Renderer failed: ", sdl2.SDL_GetError())
            return False

        if sdlimage.IMG_Init(sdlimage.IMG_INIT_PNG) == 0:
            sdl2.SDL_Log("Image failed: ", sdl2.SDL_GetError())
            return False

        # TODO Load data here

        # Initial time
        self._m_time_then = sdl2.SDL_GetTicks()

        return True

    def run_loop(self) -> None:
        while self._m_running:
            self._process_input()
            self._process_update()
            self._process_output()

    def shutdown(self) -> None:
        # Shutdown in reverse
        # TODO Unloaddata here
        sdlimage.IMG_Quit()
        sdl2.SDL_DestroyRenderer(self._m_renderer)
        sdl2.SDL_DestroyWindow(self._m_window)
        sdl2.SDL_Quit()

    # These are helper methods:

    def _process_input(self) -> None:
        event = sdl2.SDL_Event()
        # Process events-queue
        while sdl2.SDL_PollEvent(event):
            if event.type == sdl2.SDL_QUIT:
                self._m_running = False

        # Process keyboard state
        keyb_state = sdl2.SDL_GetKeyboardState(None)
        if keyb_state[sdl2.SDL_SCANCODE_ESCAPE]:
            self._m_running = False

        self._m_ship._process_keyboard(keyb_state)

    def _process_update(self) -> None:
        # Wait 16ms (for frame limiting)
        sdl2.SDL_Delay(16)

        time_now = sdl2.SDL_GetTicks()
        delta_time = (time_now - self._m_time_then) / 1000.0

        # Clamp max delta time (for debugging)
        if delta_time > 0.05:
            delta_time = 0.05

        # Time now is time then
        self._m_time_then = sdl2.SDL_GetTicks()

        # Update actors
        self._m_updating_actors = True
        for actor in self._m_actors:
            actor.update(delta_time)
        self._m_updating_actors = False

        # Add pending actors
        for pending_actor in self._m_pending_actors:
            self._m_actors.append(pending_actor)
        self._m_pending_actors.clear()

        # Collect dead actors
        temp = []
        for dead_actor in self._m_actors:
            temp.append(dead_actor)

        # Remove dead actors from self._m_actors
        for da in temp:
            da.delete()

    def _process_output(self) -> None:
        # Clear color-buffer to blue
        sdl2.SDL_SetRenderDrawColor(self._m_renderer, 0, 0, 0, 255)
        sdl2.SDL_RenderClear(self._m_renderer)

        # TODO Draw sprites
        for sprite in self._m_sprites:
            sprite.draw(self._m_renderer)

        # Swap color-buffer to display on screen
        sdl2.SDL_RenderPresent(self._m_renderer)

    def _load_data(self) -> None:
        # Ship actor plus components
        self._m_ship = Ship(self)
        self._m_ship.set_position(Vector2D(100.0, 384.0))
        self._m_ship.set_scale(1.5)

        # Background actor plus components
        bg_actor = Actor(self)
        bg_actor.set_position(Vector2D(512.0, 384.0))
        bg_sprite_far = BGSpriteComponent(bg_actor)
        bg_sprite_far.set_screen_size(Vector2D(1024.0, 768.0))
        bg_texture = [self.get_texture("assets/farback01.png"),
                      self.get_texture("assets/farback02.png")]
        bg_sprite_far.set_bgtextures(bg_texture)
        bg_sprite_far.set_scroll_speed(-100.0)

        bg_sprite_near = BGSpriteComponent(bg_actor, 50)
        bg_sprite_near.set_screen_size(Vector2D(1024.0, 768.0))
        bg_texture = [self.get_texture("assets/stars.png"),
                      self.get_texture("assets/stars.png")]
        bg_sprite_near.set_bgtexture(bg_texture)
        bg_sprite_near.set_scroll_speed(-200.0)

    def _unload_data(self) -> None:
        # TODO
        pass

    def get_texture(self, filename: str) -> sdl2.SDL_Texture:
        # Search for texture in dictionary
        texture = self._m_textures.get(filename)
        if texture != None:
            return texture
        else:
            # Load image
            surface = sdlimage.IMG_Load(filename)
            if surface == None:
                sdl2.SDL_Log("Failed to load image file: ", filename)
                return None
            # Create texture
            texture = sdl2.SDL_CreateTextureFromSurface(
                self._m_renderer, surface)
            sdl2.SDL_FreeSurface(surface)
            if texture == None:
                sdl2.SDL_Log("Failed to create texture: ", filename)
                return None

            # Add to dic
            self._m_textures[filename] = texture
        return texture

    def add_actor(self, actor: "Actor") -> None:
        if self._m_updating_actors:
            self._m_pending_actors.append(actor)
        else:
            self._m_actors.append(actor)

    def remove_actor(self, actor: "Actor") -> None:
        # Check in pending-actors list
        if actor in self._m_pending_actors:
            self._m_pending_actors.remove(actor)
        # Check in actors list
        if actor in self._m_actors:
            self._m_actors.remove(actor)

    def add_sprite(self, sprite: "SpriteComponent") -> None:
        # Add based on update order
        bisect.insort_left(self._m_sprites, sprite)

    def remove_sprite(self, sprite: "SpriteComponent") -> None:
        self._m_sprites.remove(sprite)
