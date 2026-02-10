from datetime import datetime
from threading import Lock
from pynput import keyboard, mouse


class ActivityTracker:
    def __init__(self):
        # Last time any keyboard/mouse input was detected
        self.last_input_time = datetime.now()
        self._lock = Lock()

        self._keyboard_listener = None
        self._mouse_listener = None
        self._started = False

    # --------------------------------------------
    # Keyboard input handler
    # --------------------------------------------
    def _on_keyboard(self, key):
        with self._lock:
            self.last_input_time = datetime.now()

    # --------------------------------------------
    # Mouse input handler
    # --------------------------------------------
    def _on_mouse(self, *args):
        with self._lock:
            self.last_input_time = datetime.now()

    # --------------------------------------------
    # Reset input time (day change / restart safe)
    # --------------------------------------------
    def reset(self):
        with self._lock:
            self.last_input_time = datetime.now()

    # --------------------------------------------
    # Start listeners (SAFE: only once)
    # --------------------------------------------
    def start(self):
        if self._started:
            return

        # Keyboard listener
        self._keyboard_listener = keyboard.Listener(
            on_press=self._on_keyboard
        )
        self._keyboard_listener.daemon = True
        self._keyboard_listener.start()

        # Mouse listener
        self._mouse_listener = mouse.Listener(
            on_move=self._on_mouse,
            on_click=self._on_mouse,
            on_scroll=self._on_mouse
        )
        self._mouse_listener.daemon = True
        self._mouse_listener.start()

        self._started = True
        print("🎧 ActivityTracker started (keyboard + mouse)")
