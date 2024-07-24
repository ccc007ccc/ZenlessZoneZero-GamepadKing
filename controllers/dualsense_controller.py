from dualsense_controller import DualSenseController as DS , Mapping
from dualsense_controller.core.exception import InvalidDeviceIndexException
from .base_controller import BaseController
import time

class DualSenseController(BaseController):
    def __init__(self):
        self.controller = self.connect_dualsense(1)

    def connect_dualsense(self, retry_interval):
        retries = 0
        while True:
            try:
                return DS(microphone_invert_led=False, mapping=Mapping.RAW)
            except InvalidDeviceIndexException:
                print(f"连接DualSense失败，重试 {retries + 1} 次...")
                retries += 1
                time.sleep(retry_interval)

    def start(self):
        self.controller.activate()

    def stop(self):
        self.controller.deactivate()

    def add_callback(self, button, event, callback):
        if button == 'left_trigger':
            self.controller.left_trigger.on_change(callback)
        elif button == 'circle':
            self.controller.btn_circle.on_down(callback)
        elif button == 'up':
            if event == 'press':
                self.controller.btn_up.on_down(callback)
            elif event == 'release':
                self.controller.btn_up.on_up(callback)

    def set_lightbar_color(self, color):
        if color == 'blue':
            self.controller.lightbar.set_color_blue()
        elif color == 'red':
            self.controller.lightbar.set_color_red()
    
    def set_rumble(self, direction : str, strength : int, duration ):
        if direction == 'left':
            self.controller.left_rumble.set(strength)
        elif direction == 'right':
            self.controller.right_rumble.set(strength)
        else:
            raise ValueError('Invalid direction')
        time.sleep(duration)
        self.controller.left_rumble.set(0)
        self.controller.right_rumble.set(0)