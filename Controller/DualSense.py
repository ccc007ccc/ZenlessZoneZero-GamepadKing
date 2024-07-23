import time
from EmulationGamepad import EmulationGamepad
from dualsense_controller import DualSenseController
from dualsense_controller.core.exception import InvalidDeviceIndexException
import winsound

class DualSenseEmulator:
    def __init__(self):
        self.gamepad = EmulationGamepad('ds4')
        self.is_running = True
        self.dualsense = self.connect_dualsense(1)
        self.dualsense.lightbar.set_color_blue()
        self.left_trigger_is_pressed = False
        self.open_emulation = False

    def connect_dualsense(self, retry_interval):
        retries = 0
        while True :
            try:
                return DualSenseController()
            except InvalidDeviceIndexException as e:
                print(f"连接DualSense失败，重试 {retries + 1} 次...")
                retries += 1
                time.sleep(retry_interval)
    def on_left_trigger(self, value):
        if value > 0.5 and not self.left_trigger_is_pressed:
            self.left_trigger_is_pressed = True
            if self.open_emulation:
                self.open_emulation = False
                print('模拟手柄已关闭')
                self.dualsense.lightbar.set_color_blue()
            else:
                self.open_emulation = True
                print('模拟手柄已启用')
                self.dualsense.lightbar.set_color_red()
        elif value <= 0.01 and self.left_trigger_is_pressed:
            self.left_trigger_is_pressed = False

    def on_circle(self):
        if self.open_emulation:
            self.gamepad.DoubleDodge()

    def run(self):
        self.dualsense.left_trigger.on_change(self.on_left_trigger)
        self.dualsense.btn_circle.on_down(self.on_circle)
        
        self.dualsense.activate()
        while self.is_running:
            time.sleep(0.001)
        self.dualsense.deactivate()
