from abc import ABC, abstractmethod
from utils.emulation_gamepad import EmulationGamepad
from utils.hid_hide import HidHide
import time, threading

class BaseEmulator(ABC):
    def __init__(self, emulation_gamepad_type : str, gamepad_type, macro = True):
        self.hid_hide = HidHide()
        self.is_running = True
        self.macro = macro
        self.controller = self._create_controller()
        self.emulation_gamepad_type = emulation_gamepad_type
        self.gamepad_type = gamepad_type
        
        self.gamepad = EmulationGamepad(self.emulation_gamepad_type,self.gamepad_type)
        self.gamepad.gamepad.register_notification(callback_function=self.emulation_gamepad_callback)
        
        self.r_x = 127
        self.r_y = 127
        self.l_x = 127
        self.l_y = 127
        
        self.skills_num = 1
        self.double_dodge_is_open = True
        self.breath_of_Fire_is_open = False
        self.king_mode = False
        
        
    def emulation_gamepad_callback(self,client, target, large_motor, small_motor, led_number, user_data):
        """
        Callback function triggered at each received state change

        :param client: vigem bus ID
        :param target: vigem device ID
        :param large_motor: integer in [0, 255] representing the state of the large motor
        :param small_motor: integer in [0, 255] representing the state of the small motor
        :param led_number: integer in [0, 255] representing the state of the LED ring
        :param user_data: placeholder, do not use
        """
        # Do your things here. For instance:
        # print(f"Received notification for client {client}, target {target}")
        # print(f"large motor: {large_motor}, small motor: {small_motor}")
        # print(f"led number: {led_number}")
        

    @abstractmethod
    def _create_controller(self):
        self.hid_hide.hide_panel()
        self.hid_hide.cloak_on()
        
    def change_mode(self):
        self.king_mode = not self.king_mode 
        self.skills_num_change()
        print(f'宏模式已{"启用" if self.king_mode else "关闭"}')
        time.sleep(0.3)
        
    def double_dodge(self):
        if self.king_mode and self.double_dodge_is_open and self.gamepad.b:
            self.gamepad.DoubleDodge()
    def breath_of_Fire(self):
        if self.king_mode and self.breath_of_Fire_is_open and self.gamepad.x:
            self.gamepad.BreathOfFire()
    
    def right_joystick_change_xy(self, x, y):
        # print(f'右摇杆坐标: {x}, {y}')
        self.gamepad.right_joystick(x, y)
    def right_joystick_change(self, joystick):
        x = joystick.x
        y = joystick.y
        # print(f'右摇杆: {x}, {y}')
        self.gamepad.right_joystick(x, y)
    def left_joystick_change_xy(self, x, y):
        # print(f'左摇杆坐标: {x}, {y}')
        self.gamepad.left_joystick(x, y)
    def left_joystick_change(self, joystick):
        x = joystick.x
        y = joystick.y
        # print(f'左摇杆: {x}, {y}')
        self.gamepad.left_joystick(x, y)
    
    def r_x_change(self, value):
        self.r_x = value
    def r_y_change(self, value):
        self.r_y = value
    def l_x_change(self, value):
        self.l_x = value
    def l_y_change(self, value):
        self.l_y = value
    
    def on_lt(self, value):
        self.gamepad.left_trigger(value)
    def on_rt(self, value):
        self.gamepad.right_trigger(value)
    
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
        if self.gamepad.lt and self.gamepad.pad_up:
            self.change_mode()
            time.sleep(0.1)
    def on_left_tighter_and_pad_down(self):
        ...
        
    def on_left_tighter_and_pad_left(self):
        if self.gamepad.lt and self.gamepad.pad_left:
            self.double_dodge_is_open = not self.double_dodge_is_open
            self.skills_num_add() if self.double_dodge_is_open else self.skills_num_sub()
            print(f'双闪{"已启用" if self.double_dodge_is_open else "关闭"}')
            time.sleep(0.3)
    def on_left_tighter_and_pad_right(self):
        if self.gamepad.lt and self.gamepad.pad_right:
            self.breath_of_Fire_is_open = not self.breath_of_Fire_is_open
            self.skills_num_add() if self.breath_of_Fire_is_open else self.skills_num_sub()
            print(f'刀刀烈火{"已启用" if self.breath_of_Fire_is_open else "关闭"}')
            time.sleep(0.3)


    def breath_of_Fire(self):
        while self.is_running:
            if self.king_mode and self.breath_of_Fire_is_open:
                self.gamepad.BreathOfFire()
            time.sleep(0.001)
            
    def run(self):
        self._setup_callbacks()
        self.controller.start()
        threading.Thread(target=self.breath_of_Fire, daemon=True).start()
        while self.is_running:        
            if self.macro:    
                self.run_loop()
            time.sleep(0.001)
        self.controller.stop()
    def stop(self):
        self.is_running = False
        self.gamepad.stop()
    def run_loop(self):
        self.on_left_tighter_and_pad_up()
        self.on_left_tighter_and_pad_down()
        self.on_left_tighter_and_pad_left()
        self.on_left_tighter_and_pad_right()
        self.double_dodge()

    @abstractmethod
    def _setup_callbacks(self):
        
        #摇杆xy回调在子类里定义
        
        self.controller.add_callback('rs', 'press', self.gamepad.rs_press)
        self.controller.add_callback('rs', 'release', self.gamepad.rs_release)
        self.controller.add_callback('ls', 'press', self.gamepad.ls_press)
        self.controller.add_callback('ls', 'release', self.gamepad.ls_release)
        
        self.controller.add_callback('rt', 'change', self.on_rt)
        self.controller.add_callback('lt', 'change', self.on_lt)
        self.controller.add_callback('rb', 'press', self.gamepad.rb_press)
        self.controller.add_callback('rb', 'release', self.gamepad.rb_release)
        self.controller.add_callback('lb', 'press', self.gamepad.lb_press)
        self.controller.add_callback('lb', 'release', self.gamepad.lb_release)
        
        self.controller.add_callback('a', 'press', self.gamepad.a_press)
        self.controller.add_callback('a', 'release', self.gamepad.a_release)
        self.controller.add_callback('b', 'press', self.gamepad.b_press)
        self.controller.add_callback('b', 'release', self.gamepad.b_release)
        self.controller.add_callback('x', 'press', self.gamepad.x_press)
        self.controller.add_callback('x', 'release', self.gamepad.x_release)
        self.controller.add_callback('y', 'press', self.gamepad.y_press)
        self.controller.add_callback('y', 'release', self.gamepad.y_release)
        
        
        self.controller.add_callback('dpad_up', 'press', self.gamepad.up_press)
        self.controller.add_callback('dpad_up', 'release', self.gamepad.up_release)
        self.controller.add_callback('dpad_down', 'press', self.gamepad.down_press)
        self.controller.add_callback('dpad_down', 'release', self.gamepad.down_release)
        self.controller.add_callback('dpad_left', 'press', self.gamepad.left_press)
        self.controller.add_callback('dpad_left', 'release', self.gamepad.left_release)
        self.controller.add_callback('dpad_right', 'press', self.gamepad.right_press)
        self.controller.add_callback('dpad_right', 'release', self.gamepad.right_release)
        
        self.controller.add_callback('back', 'press', self.gamepad.back_press)
        self.controller.add_callback('back', 'release', self.gamepad.back_release)
        self.controller.add_callback('start', 'press', self.gamepad.start_press)
        self.controller.add_callback('start', 'release', self.gamepad.start_release)
        
        self.controller.add_callback('home', 'press', self.gamepad.home_press)
        self.controller.add_callback('home', 'release', self.gamepad.home_release)
        