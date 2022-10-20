import sdl2
import sdl2.sdlimage as sdlimage
import builtins
from vector2d import *


class Game:
    def __init__(self):
        # TODO add type hinting after it works
        self._m_window = None
        self._m_renderer = None
        self._m_running = True
        self._m_time_then = 0.0

        # TODO Textures here
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

        if sdlimage.IMG_Init() == 0:
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

        # TODO Draw sprite components below
        # [old code] Draw scene to color-buffer:
        sdl2.SDL_SetRenderDrawColor(
            self._m_renderer, 192, 192, 192, 255)              # Color
        top_wall = sdl2.SDL_Rect(0, 0, 1024, self._m_thick)    # Shapes
        bot_wall = sdl2.SDL_Rect(0, 768-self._m_thick, 1024, self._m_thick)
        right_wall = sdl2.SDL_Rect(1024-self._m_thick, 0, self._m_thick, 1024)
        paddle = sdl2.SDL_Rect(int(self._m_paddle_pos.x),
                               int(self._m_paddle_pos.y-self._m_paddle_h/2),
                               int(self._m_thick),
                               int(self._m_paddle_h))
        ball = sdl2.SDL_Rect(int(self._m_ball_pos.x-self._m_thick/2),
                             int(self._m_ball_pos.y-self._m_thick/2),
                             int(self._m_thick),
                             int(self._m_thick))
        sdl2.SDL_RenderFillRect(self._m_renderer, top_wall)    # Draws
        sdl2.SDL_RenderFillRect(self._m_renderer, bot_wall)
        sdl2.SDL_RenderFillRect(self._m_renderer, right_wall)
        sdl2.SDL_RenderFillRect(self._m_renderer, paddle)
        sdl2.SDL_RenderFillRect(self._m_renderer, ball)

        # Swap color-buffer to update screen
        sdl2.SDL_RenderPresent(self._m_renderer)
