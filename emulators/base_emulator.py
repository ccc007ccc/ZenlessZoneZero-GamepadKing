from abc import ABC, abstractmethod
from utils.emulation_gamepad import EmulationGamepad
import time

class BaseEmulator(ABC):
    def __init__(self, controller_type : str):
        self.is_running = True
        self.controller = self._create_controller()
        self.gamepad = EmulationGamepad(controller_type)
        self.left_trigger = False
        self.pad_up = False
        self.pad_down = False
        self.pad_left = False
        self.pad_right = False
        self.back = False
        
        self.skills_num = 1
        self.double_dodge_is_open = True
        self.breath_of_Fire_is_open = False
        self.king_mode = False
        

    @abstractmethod
    def _create_controller(self):
        pass

    def change_mode(self):
        self.king_mode = not self.king_mode 
        self.skills_num_change()
        print(f'模拟手柄已{"启用" if self.king_mode else "关闭"}')
        
    def double_dodge(self):
        if self.double_dodge_is_open and self.king_mode:
            self.gamepad.DoubleDodge()
    def breath_of_Fire(self):
        if self.breath_of_Fire_is_open and self.king_mode:
            self.gamepad.BreathOfFire()
            
    def on_left_trigger(self, value):
        # print(f'left trigger value: {value}')
        if value > 255/2 and not self.left_trigger:
            # print('left trigger pressed')
            self.on_left_trigger_down()
        elif value <= 0.1 and self.left_trigger:
            self.on_left_trigger_up()
            
    def on_left_trigger_down(self):
        self.left_trigger = True
    def on_left_trigger_up(self):
        self.left_trigger = False

    def on_pad_up_down(self):
        # print('pad up pressed')
        self.pad_up = True
    def on_pad_up_up(self):
        self.pad_up = False
    def on_pad_down_down(self):
        self.pad_down = True
    def on_pad_down_up(self):
        self.pad_down = False
    def on_pad_left_down(self):
        self.pad_left = True
    def on_pad_left_up(self):
        self.pad_left = False
    def on_pad_right_down(self):
        self.pad_right = True
    def on_pad_right_up(self):
        self.pad_right = False
        
    
    def skills_num_add(self):
        self.skills_num += 1
        self.skills_num_change()
        print(f'已启用技能数量: {self.skills_num}')
    def skills_num_sub(self):
        self.skills_num -= 1 if self.skills_num > 0 else 0
        self.skills_num_change()
        print(f'已启用技能数量: {self.skills_num}')
    def skills_num_change(self):
        ...
    
    def on_left_tighter_and_pad_up(self):
        if self.left_trigger and self.pad_up:
            self.change_mode()
            time.sleep(0.3)
    def on_left_tighter_and_pad_down(self):
        ...
        
    def on_left_tighter_and_pad_left(self):
        if self.left_trigger and self.pad_left:
            self.double_dodge_is_open = not self.double_dodge_is_open
            self.skills_num_add() if self.double_dodge_is_open else self.skills_num_sub()
            print(f'双闪{"已启用" if self.double_dodge_is_open else "关闭"}')
            time.sleep(0.3)
    def on_left_tighter_and_pad_right(self):
        if self.left_trigger and self.pad_right:
            self.breath_of_Fire_is_open = not self.breath_of_Fire_is_open
            self.skills_num_add() if self.breath_of_Fire_is_open else self.skills_num_sub()
            print(f'刀刀烈火{"已启用" if self.breath_of_Fire_is_open else "关闭"}')
            time.sleep(0.3)
            
    def on_back(self):
        print('back pressed')
        self.back = True

    def run(self):
        self._setup_callbacks()
        self.controller.start()
        while self.is_running:
            self.on_left_tighter_and_pad_up()
            self.on_left_tighter_and_pad_down()
            self.on_left_tighter_and_pad_left()
            self.on_left_tighter_and_pad_right()
            time.sleep(0.001)
        self.controller.stop()

    def _setup_callbacks(self):
        self.controller.add_callback('lt', 'change', self.on_left_trigger)
        
        self.controller.add_callback('b', 'press', self.double_dodge)
        self.controller.add_callback('x', 'press', self.breath_of_Fire)
        
        self.controller.add_callback('dpad_up', 'press', self.on_pad_up_down)
        self.controller.add_callback('dpad_up', 'release', self.on_pad_up_up)
        self.controller.add_callback('dpad_down', 'press', self.on_pad_down_down)
        self.controller.add_callback('dpad_down', 'release', self.on_pad_down_up)
        self.controller.add_callback('dpad_left', 'press', self.on_pad_left_down)
        self.controller.add_callback('dpad_left', 'release', self.on_pad_left_up)
        self.controller.add_callback('dpad_right', 'press', self.on_pad_right_down)
        self.controller.add_callback('dpad_right', 'release', self.on_pad_right_up)
        
        self.controller.add_callback('back', 'press', self.on_back)