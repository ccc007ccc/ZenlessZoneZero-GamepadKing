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
                return DS(microphone_initially_muted=False, microphone_invert_led=False, mapping=Mapping.RAW)
            except InvalidDeviceIndexException:
                print(f"连接DualSense失败，重试 {retries + 1} 次...")
                retries += 1
                time.sleep(retry_interval)

    def start(self):
        self.controller.activate()
        self.controller.lightbar.set_color(0, 0, 255)

    def stop(self):
        self.controller.deactivate()

    def add_callback(self, button, event, callback):
        if button == 'lt':
            self.controller.left_trigger.on_change(callback)
            
            
        elif button == 'a':
            if event == 'press':
                self.controller.btn_cross.on_down(callback)
            elif event == 'release':
                self.controller.btn_cross.on_up(callback)
        elif button == 'b':
            if event == 'press':
                self.controller.btn_circle.on_down(callback)
            elif event == 'release':
                self.controller.btn_circle.on_up(callback)
        elif button == 'x':
            if event == 'press':
                self.controller.btn_square.on_down(callback)
            elif event == 'release':
                self.controller.btn_square.on_up(callback)
        elif button == 'y':
            if event == 'press':
                self.controller.btn_triangle.on_down(callback)
            elif event == 'release':
                self.controller.btn_triangle.on_up(callback)
            
        elif button == 'dpad_up':
            if event == 'press':
                self.controller.btn_up.on_down(callback)
            elif event == 'release':
                self.controller.btn_up.on_up(callback)
        elif button == 'dpad_down':
            if event == 'press':
                self.controller.btn_down.on_down(callback)
            elif event == 'release':
                self.controller.btn_down.on_up(callback)
        elif button == 'dpad_left':
            if event == 'press':
                self.controller.btn_left.on_down(callback)
            elif event == 'release':
                self.controller.btn_left.on_up(callback)
        elif button == 'dpad_right':
            if event == 'press':
                self.controller.btn_right.on_down(callback)
            elif event == 'release':
                self.controller.btn_right.on_up(callback)
                
        elif button == 'back':
            if event == 'press':
                self.controller.btn_create.on_down(callback)  # 这方法不按真实名称起,找了半天
            elif event == 'release':
                self.controller.btn_create.on_up(callback)

    def set_lightbar_color(self, red : int, green : int, blue : int):
        self.controller.lightbar.set_color(red, green, blue)
    
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