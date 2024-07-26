from .base_emulator import BaseEmulator
from controllers.xbox_controller import XboxController
import winsound, threading

class XboxEmulator(BaseEmulator):
    def _setup_callbacks(self):
        super()._setup_callbacks()
        self.controller.add_callback('r_x', 'change', self.r_x_change)
        self.controller.add_callback('r_y', 'change', self.r_y_change)
        self.controller.add_callback('l_x', 'change', self.l_x_change)
        self.controller.add_callback('l_y', 'change', self.l_y_change)
    def _create_controller(self):
        super()._create_controller()
        return XboxController()

    def run_loop(self):
        super().run_loop()
        self.right_joystick_change_xy(self.r_x, self.r_y)
        self.left_joystick_change_xy(self.l_x, self.l_y)
    
    def emulation_gamepad_callback(self, client, target, large_motor, small_motor, led_number, user_data):
        super().emulation_gamepad_callback(client, target, large_motor, small_motor, led_number, user_data)
        threading.Thread(target=self.controller.set_rumble, args=('left', large_motor)).start()
        threading.Thread(target=self.controller.set_rumble, args=('right', small_motor)).start()
        
    def change_rumble(self, mode : str):
        if mode == 'normal':
            self.controller.set_rumble('left', 0, 0.2)
            self.controller.set_rumble('right', 127, 0.2)
        elif mode == 'king':
            self.controller.set_rumble('left', 127, 0.15)
            self.controller.set_rumble('right', 0, 0.15)
            
    def change_mode(self):
        super().change_mode()
        self.change_rumble('king') if self.king_mode else self.change_rumble('normal')
