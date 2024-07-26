import threading, time, ctypes
from inputs import get_gamepad
from .base_controller import BaseController

# 定义 XInput 结构和常量
class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]
class XboxController(BaseController):
    def __init__(self):
        self.controller_type = 'xbox'
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
            'l_x': {'change': []},
            'l_y': {'change': []},
            'r_x': {'change': []},
            'r_y': {'change': []},
            'home': {'press': [], 'release': []}
        }
        self.running = False
        self.thread = None
        self.left_rumble = 0
        self.right_rumble = 0
        
        # 加载 XInput DLL
        self.xinput = ctypes.windll.xinput1_4 if hasattr(ctypes.windll, 'xinput1_4') else ctypes.windll.xinput9_1_0
        
        # 初始化震动结构
        self.vibration = XINPUT_VIBRATION(0, 0)

    def start(self):
        super().start()
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
            self._callbacks('start', event.state == 1)
        elif event.code == "BTN_START":  # Start
            self._callbacks('back', event.state == 1)
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
            self._analog_callbacks('l_x', event.state)
        elif event.code == "ABS_Y":  # Left Stick Y
            self._analog_callbacks('l_y', event.state)
        elif event.code == "ABS_RX":  # Right Stick X
            self._analog_callbacks('r_x', event.state)
        elif event.code == "ABS_RY":  # Right Stick Y
            self._analog_callbacks('r_y', event.state)
            


    def _callbacks(self, button, is_pressed):
        event = 'press' if is_pressed else 'release'
        for callback in self.callbacks[button][event]:
            callback()

    def _analog_callbacks(self, button, value):
        for callback in self.callbacks[button]['change']:
            callback(value)
    
    def set_rumble(self, direction: str, strength: int, duration=None):
        """
        设置控制器的震动
        :param direction: 震动的方向，'left' 或 'right'
        :param strength: 震动强度 (0-255)
        :param duration: 震动持续时间（秒），None 表示持续震动直到被停止
        """
        if strength < 0 or strength > 255:
            raise ValueError('Strength must be between 0 and 255')

        # 将 0-255 的值映射到 0-65535
        mapped_strength = int((strength / 255) * 65535)

        if direction == 'left':
            self.left_rumble = mapped_strength
            self.vibration.wLeftMotorSpeed = mapped_strength
        elif direction == 'right':
            self.right_rumble = mapped_strength
            self.vibration.wRightMotorSpeed = mapped_strength
        else:
            raise ValueError('Invalid direction')

        # 发送震动命令到控制器
        self.xinput.XInputSetState(0, ctypes.byref(self.vibration))

        if duration is not None:
            # 如果指定了持续时间，创建一个线程来停止震动
            threading.Timer(duration, self._stop_rumble, args=[direction]).start()

    def _stop_rumble(self, direction):
        """
        停止指定方向的震动
        """
        self.set_rumble(direction, 0)

    def stop_all_rumble(self):
        """
        停止所有震动
        """
        self.vibration.wLeftMotorSpeed = 0
        self.vibration.wRightMotorSpeed = 0
        self.xinput.XInputSetState(0, ctypes.byref(self.vibration))
        self.left_rumble = 0
        self.right_rumble = 0