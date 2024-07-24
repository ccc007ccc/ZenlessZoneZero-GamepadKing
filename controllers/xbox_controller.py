import threading
import time
from inputs import get_gamepad
from .base_controller import BaseController

class XboxController(BaseController):
    def __init__(self):
        self.callbacks = {
            'a': {'press': [], 'release': []},
            'b': {'press': [], 'release': []},
            'x': {'press': [], 'release': []},
            'y': {'press': [], 'release': []},
            'lb': {'press': [], 'release': []},
            'rb': {'press': [], 'release': []},
            'lt': {'change': []},
            'rt': {'change': []},
            'back': {'press': [], 'release': []},
            'start': {'press': [], 'release': []},
            'ls': {'press': [], 'release': []},
            'rs': {'press': [], 'release': []},
            'dpad_up': {'press': [], 'release': []},
            'dpad_down': {'press': [], 'release': []},
            'dpad_left': {'press': [], 'release': []},
            'dpad_right': {'press': [], 'release': []},
            'ls_x': {'change': []},
            'ls_y': {'change': []},
            'rs_x': {'change': []},
            'rs_y': {'change': []}
        }
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._read_gamepad, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        

    def add_callback(self, button, event, callback):
        self.callbacks[button][event].append(callback)

    def _read_gamepad(self):
        while self.running:
            try:
                events = get_gamepad()
                for event in events:
                    self._handle_event(event)
                time.sleep(0.001)
            except Exception as e:
                print(f"Error reading gamepad: {e}")
                time.sleep(1)  # Wait before trying again

    def _handle_event(self, event):
        if event.code == "BTN_SOUTH":  # A
            self._callbacks('a', event.state == 1)
        elif event.code == "BTN_EAST":  # B
            self._callbacks('b', event.state == 1)
        elif event.code == "BTN_NORTH":  # Y
            self._callbacks('y', event.state == 1)
        elif event.code == "BTN_WEST":  # X
            self._callbacks('x', event.state == 1)
        elif event.code == "BTN_TL":  # LB
            self._callbacks('lb', event.state == 1)
        elif event.code == "BTN_TR":  # RB
            self._callbacks('rb', event.state == 1)
            
        elif event.code == "ABS_Z":  # LT
            self._analog_callbacks('lt', event.state)
        elif event.code == "ABS_RZ":  # RT
            self._analog_callbacks('rt', event.state)
            
        elif event.code == "BTN_SELECT":  # Back
            self._callbacks('back', event.state == 1)
        elif event.code == "BTN_START":  # Start
            self._callbacks('start', event.state == 1)
        elif event.code == "BTN_THUMBL":  # LS
            self._callbacks('ls', event.state == 1)
        elif event.code == "BTN_THUMBR":  # RS
            self._callbacks('rs', event.state == 1)
        elif event.code == "ABS_HAT0Y":  # D-pad Up/Down
            if event.state == -1:
                self._callbacks('dpad_up', True)
            elif event.state == 1:
                self._callbacks('dpad_down', True)
            else:
                self._callbacks('dpad_up', False)
                self._callbacks('dpad_down', False)
        elif event.code == "ABS_HAT0X":  # D-pad Left/Right
            if event.state == -1:
                self._callbacks('dpad_left', True)
            elif event.state == 1:
                self._callbacks('dpad_right', True)
            else:
                self._callbacks('dpad_left', False)
                self._callbacks('dpad_right', False)
        elif event.code == "ABS_X":  # Left Stick X
            self._analog_callbacks('ls_x', event.state)
        elif event.code == "ABS_Y":  # Left Stick Y
            self._analog_callbacks('ls_y', event.state)
        elif event.code == "ABS_RX":  # Right Stick X
            self._analog_callbacks('rs_x', event.state)
        elif event.code == "ABS_RY":  # Right Stick Y
            self._analog_callbacks('rs_y', event.state)

    def _callbacks(self, button, is_pressed):
        event = 'press' if is_pressed else 'release'
        for callback in self.callbacks[button][event]:
            callback()

    def _analog_callbacks(self, button, value):
        for callback in self.callbacks[button]['change']:
            callback(value)