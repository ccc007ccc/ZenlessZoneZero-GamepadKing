import time
from EmulationGamepad import EmulationGamepad
from Xbox_Controller import XboxController
import winsound

class XboxEmulator:
    def __init__(self):
        self.gamepad = EmulationGamepad('ds4')
        self.is_running = True
        self.dualsense = XboxController()
        self.left_trigger_is_pressed = False
        self.open_emulation = False
        
    def on_left_trigger(self):
        # print(f'left trigger changed: {value}')
        if self.open_emulation:
            self.open_emulation = False
            print('模拟手柄已关闭')
        else:
            self.open_emulation = True
            print('模拟手柄已启用')
            winsound.Beep(500, 50)
        # else:
            # print('左扳机力度小于0.5，不执行操作')
    
    def on_circle(self):
        if self.open_emulation:
            self.gamepad.DoubleDodge()
    def run(self):
        self.dualsense.add_lt_callback("press", self.on_left_trigger)
        self.dualsense.add_b_callback("press", self.on_circle)
        
        self.dualsense.start()
        while self.is_running:
            time.sleep(0.001)