import vgamepad
import time
 
class EmulationGamepad:   
    stop_time = 0.05
    def __init__(self, gamepad_type='ds4'):
        # 根据传入的手柄类型创建一个虚拟手柄
        if gamepad_type.lower() == 'xbox':
            # 创建一个虚拟XBOX 360手柄
            self.gamepad = vgamepad.VX360Gamepad()

            # 定义所有的XBox360游戏手柄按键
            self.UP    = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
            self.DOWN  = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
            self.LEFT  = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
            self.RIGHT = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT

            self.START = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_START
            self.BACK  = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK
            self.GUIDE = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE

            self.LEFT_THUMB     = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
            self.RIGHT_THUMB    = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
            self.LEFT_SHOULDER  = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
            self.RIGHT_SHOULDER = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER

            self.A = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A
            self.B = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B
            self.X = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_X
            self.Y = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y
        else:
            # 创建一个虚拟DS4手柄
            self.gamepad = vgamepad.VDS4Gamepad()
        
            # 定义DS4游戏手柄所有的按键
            self.NONE      = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NONE
            self.NORTHWEST = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHWEST
            self.LEFT      = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_WEST
            self.SOUTHWEST = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHWEST
            self.DOWN     = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTH
            self.SOUTHEAST = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHEAST
            self.RIGHT      = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_EAST
            self.NORTHEAST = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHEAST
            self.UP     = vgamepad.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTH
            
            self.LEFT_THUMB     = vgamepad.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT 
            self.RIGHT_THUMB    = vgamepad.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT
            self.LEFT_SHOULDER  = vgamepad.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT
            self.RIGHT_SHOULDER = vgamepad.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT
            
            self.Y = vgamepad.DS4_BUTTONS.DS4_BUTTON_TRIANGLE
            self.B   = vgamepad.DS4_BUTTONS.DS4_BUTTON_CIRCLE
            self.A    = vgamepad.DS4_BUTTONS.DS4_BUTTON_CROSS
            self.X   = vgamepad.DS4_BUTTONS.DS4_BUTTON_SQUARE
            
            self.PS       = vgamepad.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS
            self.TOUCHPAD = vgamepad.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD
    def Dodge(self):
        # 闪避
        self.gamepad.press_button(self.A)
        self.gamepad.update()
        time.sleep(self.stop_time * 1.2)
        self.gamepad.release_button(self.A)
        self.gamepad.update()
    
    def Attack(self):
        #攻击
        self.gamepad.press_button(self.X)
        self.gamepad.update()
        time.sleep(self.stop_time)
        self.gamepad.release_button(self.X)
        self.gamepad.update()
        
    def ChangeAvatar(self, direction):
        if direction == 'left':
            self.direction = self.LEFT_SHOULDER
        elif direction == 'right':
            self.direction = self.RIGHT_SHOULDER
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
        