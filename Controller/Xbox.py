import time
from EmulationGamepad import EmulationGamepad
from Xbox_Controller import XboxController
import winsound

class XboxEmulator:
    def __init__(self):
        self.is_running = True
        self.dualsense = XboxController()
        self.gamepad = EmulationGamepad('ds4')
        self.left_trigger = False
        self.pad_up = False
        self.open_emulation = False
        
        
    def change_mode(self):
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
    
    def on_left_trigger_down(self):
        self.left_trigger = True
        
    def on_left_trigger_up(self):
        self.left_trigger = False
    
    def on_pad_up_down(self):
        self.pad_up = True
    
    def on_pad_up_up(self):
        self.pad_up = False
    def run(self):
        self.dualsense.add_lt_callback("press", self.on_left_trigger_down)
        self.dualsense.add_lt_callback("release", self.on_left_trigger_up)
        self.dualsense.add_dpad_up_callback("press", self.on_pad_up_down)
        self.dualsense.add_dpad_up_callback("release", self.on_pad_up_up)
        
        self.dualsense.add_b_callback("press", self.on_circle)
        
        
        self.dualsense.start()
        while self.is_running:
            if self.left_trigger and self.pad_up:
                time.sleep(0.5)
                self.change_mode()
            time.sleep(0.001)
        self.dualsense.stop()