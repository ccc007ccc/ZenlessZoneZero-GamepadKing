import vgamepad
import time

import vgamepad.win
import vgamepad.win.virtual_gamepad

class EmulationGamepad:

    def __init__(self, emulation_gamepad_type, gamepad_type):
        self.stop_time = 0.03
        self.emulation_gamepad_type = emulation_gamepad_type
        self.gamepad_type = gamepad_type
        
        self.gamepad = vgamepad.VDS4Gamepad() if emulation_gamepad_type.lower() == 'ds4' else vgamepad.VX360Gamepad()
        self._setup_buttons()
        
        
        
        self.rs = False
        self.ls = False
        
        self.rb = False
        self.lb = False
        
        self.rt = False
        self.rt_value = 0
        
        self.lt = False
        self.lt_value = 0
        
        self.a = False
        self.b = False
        self.x = False
        self.y = False
        
        self.pad_up = False
        self.pad_down = False
        self.pad_left = False
        self.pad_right = False
        self.pad_left_up = False
        self.pad_left_down = False
        self.pad_right_up = False
        self.pad_right_down = False
        
        self.back = False
        self.start = False
        
        self.home = False

    def _setup_buttons(self):
        if self.emulation_gamepad_type == 'ds4':
            self._setup_ds4_buttons()
        else:
            self._setup_xbox_buttons()

    def stop(self):
        del self.gamepad
    def _setup_ds4_buttons(self):
        # 定义DS4游戏手柄所有的按键
        self.NONE      = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NONE
        self.LEFT_UP = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHWEST
        self.LEFT      = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_WEST
        self.LEFT_DOWN = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHWEST
        self.DOWN     = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTH
        self.RIGHT_DOWN = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHEAST
        self.RIGHT      = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_EAST
        self.RIGHT_UP = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHEAST
        self.UP     = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTH
        
        self.LS     = vgamepad.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT
        self.RS    = vgamepad.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT
        self.LB  = vgamepad.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT
        self.RB = vgamepad.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT
        
        self.A    = vgamepad.DS4_BUTTONS.DS4_BUTTON_CROSS
        self.B   = vgamepad.DS4_BUTTONS.DS4_BUTTON_CIRCLE
        self.X   = vgamepad.DS4_BUTTONS.DS4_BUTTON_SQUARE
        self.Y = vgamepad.DS4_BUTTONS.DS4_BUTTON_TRIANGLE
        
        self.START  = vgamepad.DS4_BUTTONS.DS4_BUTTON_OPTIONS
        self.BACK       = vgamepad.DS4_BUTTONS.DS4_BUTTON_SHARE
        self.HOME       = vgamepad.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS
        self.TOUCHPAD = vgamepad.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD

    def _setup_xbox_buttons(self):
        # 定义所有的XBox360游戏手柄按键
        
        self.UP    = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
        self.DOWN  = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
        self.LEFT  = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
        self.RIGHT = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT

        self.START = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_START
        self.BACK  = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK
        self.HOME = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE

        self.LS     = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
        self.RS    = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
        self.LB  = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
        self.RB = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER

        self.A = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A
        self.B = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B
        self.X = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_X
        self.Y = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y
        
        
    def up_press(self):
        self.pad_up = True
        self.update_dpad()
        self.gamepad.update()
    def up_release(self):
        self.pad_up = False
        self.update_dpad()
        self.gamepad.update()

    def down_press(self):
        self.pad_down = True
        self.update_dpad()
        self.gamepad.update()
    def down_release(self):
        self.pad_down = False
        self.update_dpad()
        self.gamepad.update()

    def left_press(self):
        self.pad_left = True
        self.update_dpad()
        self.gamepad.update()
    def left_release(self):
        self.pad_left = False
        self.update_dpad()
        self.gamepad.update()

    def right_press(self):
        self.pad_right = True
        self.update_dpad()
        self.gamepad.update()
    def right_release(self):
        self.pad_right = False
        self.update_dpad()
        self.gamepad.update()
    def update_dpad(self):
        if self.emulation_gamepad_type == "xbox":
        #     # 首先释放所有方向键
        #     if self.pad_up == False:
        #         self.gamepad.release_button(self.UP)
        #     elif self.pad_down == False:
        #         self.gamepad.release_button(self.DOWN)
        #     elif self.pad_left == False:
        #         self.gamepad.release_button(self.LEFT)
        #     elif self.pad_right == False:
        #         self.gamepad.release_button(self.RIGHT)
            
            # 然后根据当前状态按下相应的方向键
            if self.pad_up and self.pad_left:
                self.gamepad.press_button(self.UP)
                self.gamepad.press_button(self.LEFT)
                
                self.gamepad.release_button(self.DOWN)
                self.gamepad.release_button(self.RIGHT)
            elif self.pad_up and self.pad_right:
                self.gamepad.press_button(self.UP)
                self.gamepad.press_button(self.RIGHT)
                
                self.gamepad.release_button(self.DOWN)
                self.gamepad.release_button(self.LEFT)
            elif self.pad_down and self.pad_left:
                self.gamepad.press_button(self.DOWN)
                self.gamepad.press_button(self.LEFT)
                
                self.gamepad.release_button(self.UP)
                self.gamepad.release_button(self.RIGHT)
            elif self.pad_down and self.pad_right:
                self.gamepad.press_button(self.DOWN)
                self.gamepad.press_button(self.RIGHT)
                
                self.gamepad.release_button(self.UP)
                self.gamepad.release_button(self.LEFT)
            else:
                if self.pad_up:
                    self.gamepad.press_button(self.UP)
                    
                    self.gamepad.release_button(self.DOWN)
                    self.gamepad.release_button(self.LEFT)
                    self.gamepad.release_button(self.RIGHT)
                elif self.pad_down:
                    self.gamepad.press_button(self.DOWN)
                    
                    self.gamepad.release_button(self.UP)
                    self.gamepad.release_button(self.LEFT)
                    self.gamepad.release_button(self.RIGHT)
                elif self.pad_left:
                    self.gamepad.press_button(self.LEFT)
                    
                    self.gamepad.release_button(self.UP)
                    self.gamepad.release_button(self.DOWN)
                    self.gamepad.release_button(self.RIGHT)
                elif self.pad_right:
                    self.gamepad.press_button(self.RIGHT)
                    
                    self.gamepad.release_button(self.UP)
                    self.gamepad.release_button(self.DOWN)
                    self.gamepad.release_button(self.LEFT)
                else:
                    self.gamepad.release_button(self.UP)
                    self.gamepad.release_button(self.DOWN)
                    self.gamepad.release_button(self.LEFT)
                    self.gamepad.release_button(self.RIGHT)
        elif self.emulation_gamepad_type == "ds4":
            if self.pad_up and self.pad_left:
                self.gamepad.directional_pad(self.LEFT_UP)
            elif self.pad_up and self.pad_right:
                self.gamepad.directional_pad(self.RIGHT_UP)
            elif self.pad_down and self.pad_left:
                self.gamepad.directional_pad(self.LEFT_DOWN)
            elif self.pad_down and self.pad_right:
                self.gamepad.directional_pad(self.RIGHT_DOWN)
            elif self.pad_up:
                self.gamepad.directional_pad(self.UP)
            elif self.pad_down:
                self.gamepad.directional_pad(self.DOWN)
            elif self.pad_left:
                self.gamepad.directional_pad(self.LEFT)
            elif self.pad_right:
                self.gamepad.directional_pad(self.RIGHT)
            else:
                self.gamepad.directional_pad(self.NONE)

    def start_press(self):
        self.gamepad.press_button(self.START)
        self.start = True
        self.gamepad.update()

    def start_release(self):
        self.gamepad.release_button(self.START)
        self.start = False
        self.gamepad.update()

    def back_press(self):
        self.gamepad.press_button(self.BACK)
        self.back = True
        self.gamepad.update()

    def back_release(self):
        self.gamepad.release_button(self.BACK)
        self.back = False
        self.gamepad.update()

    def home_press(self):
        self.gamepad.press_button(self.HOME)
        self.home = True
        self.gamepad.update()

    def home_release(self):
        self.gamepad.release_button(self.HOME)
        self.home = False
        self.gamepad.update()

    def ls_press(self):
        self.gamepad.press_button(self.LS)
        self.ls = True
        self.gamepad.update()

    def ls_release(self):
        self.gamepad.release_button(self.LS)
        self.ls = False
        self.gamepad.update()

    def rs_press(self):
        self.gamepad.press_button(self.RS)
        self.rs = True
        self.gamepad.update()

    def rs_release(self):
        self.gamepad.release_button(self.RS)
        self.rs = False
        self.gamepad.update()

    def lb_press(self):
        self.gamepad.press_button(self.LB)
        self.lb = True
        self.gamepad.update()

    def lb_release(self):
        self.gamepad.release_button(self.LB)
        self.lb = False
        self.gamepad.update()

    def rb_press(self):
        self.gamepad.press_button(self.RB)
        self.rb = True
        self.gamepad.update()

    def rb_release(self):
        self.gamepad.release_button(self.RB)
        self.rb = False
        self.gamepad.update()

    def a_press(self):
        self.gamepad.press_button(self.A)
        self.a = True
        self.gamepad.update()

    def a_release(self):
        self.gamepad.release_button(self.A)
        self.a = False
        self.gamepad.update()

    def b_press(self):
        self.gamepad.press_button(self.B)
        self.b = True
        self.gamepad.update()

    def b_release(self):
        self.gamepad.release_button(self.B)
        self.b = False
        self.gamepad.update()

    def x_press(self):
        self.gamepad.press_button(self.X)
        self.x = True
        self.gamepad.update()

    def x_release(self):
        self.gamepad.release_button(self.X)
        self.x = False
        self.gamepad.update()

    def y_press(self):
        self.gamepad.press_button(self.Y)
        self.y = True
        self.gamepad.update()

    def y_release(self):
        self.gamepad.release_button(self.Y)
        self.y = False
        self.gamepad.update()
        
        
        
        
    def convert(self,value, xbox=False):
        """
        将0到255的数值转换为-1到1的范围
        :param value: 输入值，范围0到255
        :return: 转换后的值，范围-1到1
        """
        if xbox:
            return value / 32767 if value >= 0 else value / 32768
        else:
            if 0 <= value <= 255:
                return 2 * (value / 255.0) - 1
            else:
                raise ValueError("输入值必须在0到255之间")
        
    def right_joystick(self, x, y):
        if self.gamepad_type == "xbox":
            self.gamepad.right_joystick_float(self.convert(x,True), self.convert(y,True))
        elif self.gamepad_type == "ds4":
            if self.emulation_gamepad_type == "xbox":
                self.gamepad.right_joystick_float(self.convert(x), 0 - self.convert(y))
            else:
                self.gamepad.right_joystick_float(self.convert(x), self.convert(y))
                
        self.gamepad.update()
    def left_joystick(self, x, y):
        if self.gamepad_type == "xbox":
            self.gamepad.left_joystick_float(self.convert(x, True), self.convert(y, True))
        elif self.gamepad_type == "ds4":
            if self.emulation_gamepad_type == "xbox":
                self.gamepad.left_joystick_float(self.convert(x), 0 - self.convert(y))
            else:
                self.gamepad.left_joystick_float(self.convert(x), self.convert(y))
        
        self.gamepad.update()
        
    def right_trigger(self, value):
        self.gamepad.right_trigger(value)
        # print(f'left trigger value: {value}')
        if value > 255/2 and not self.rt:
            # print('left trigger pressed')
            self.rt = True
        elif value <= 0.1 and self.rt:
            self.rt = False
        self.gamepad.update()
        
    def left_trigger(self, value):
        self.gamepad.left_trigger(value)
        if value > 255/2 and not self.lt:
            self.lt = True
        elif value <= 0.1 and self.lt:
            self.lt = False
        self.gamepad.update()
    

    def Dodge(self):
        self.gamepad.press_button(self.A)
        self.gamepad.update()
        time.sleep(self.stop_time * 1.2)
        self.gamepad.release_button(self.A)
        self.gamepad.update()

    def Attack(self, intervals = 0.02):
        self.gamepad.press_button(self.X)
        self.gamepad.update()
        time.sleep(intervals)
        self.gamepad.release_button(self.X)
        self.gamepad.update()

    def ChangeAvatar(self, direction):
        self.direction = self.LB if direction == 'left' else self.RB
        self.gamepad.press_button(self.direction)
        self.gamepad.update()
        time.sleep(self.stop_time)
        self.gamepad.release_button(self.direction)
        self.gamepad.update()

    def DodgeAndAttack(self):
        self.Dodge()
        self.Attack()

    def DoubleDodge(self):
        self.DodgeAndAttack()
        self.ChangeAvatar("right")
        self.DodgeAndAttack()
        self.DodgeAndAttack()
        
    
    def BreathOfFire(self):
        if self.gamepad_type == "xbox":
            if self.x:
                self.Attack()
                time.sleep(0.285)
                if self.x == True:
                    self.Attack()
                    time.sleep(0.350)
                    if self.x == True:
                        self.Attack()
                        time.sleep(0.685)
                        if self.x == True:
                            self.Attack()
                            self.Attack()
        else:
            if self.x:
                self.Attack()
                time.sleep(0.285)
                if self.x == True:
                    self.Attack()
                    time.sleep(0.350)
                    if self.x == True:
                        self.Attack()
                        time.sleep(0.685)
                        if self.x == True:
                            self.Attack()
                            self.Attack()
                        
        # if self.x == True:
        #     self.Attack()
        #     time.sleep(0.285)