from .base_emulator import BaseEmulator
from controllers.dualsense_controller import DualSenseController
import time,threading

class DualSenseEmulator(BaseEmulator):
    def _create_controller(self):
        super()._create_controller()
        return DualSenseController()
    
    def emulation_gamepad_callback(self, client, target, large_motor, small_motor, led_number, user_data):
        super().emulation_gamepad_callback(client, target, large_motor, small_motor, led_number, user_data)
        threading.Thread(target=self.controller.set_rumble, args=('left', large_motor, 0.05)).start()
        threading.Thread(target=self.controller.set_rumble, args=('right', small_motor, 0.05)).start()

    def change_lightbar_color(self, mode : str):
        if mode == 'normal':
            self.controller.set_lightbar_color(0, 0, 255)
        elif mode == 'king':
            self.controller.set_lightbar_color(255, 0, 0)
            
    def change_rumble(self, mode : str):
        if mode == 'normal':
            self.controller.set_rumble('left', 0, 0.05)
            self.controller.set_rumble('right', 80, 0.05)
        elif mode == 'king':
            self.controller.set_rumble('left', 60, 0.05)
            self.controller.set_rumble('right', 0, 0.05)
    
    def skills_num_change(self):
        super().skills_num_change()
        if self.king_mode == True:
            self.controller.set_player_light(self.skills_num)
        else:
            self.controller.set_player_light(0)
    
    def change_mode(self):
        super().change_mode()
        self.change_lightbar_color('king') if self.king_mode else self.change_lightbar_color('normal')
        self.change_rumble('king') if self.king_mode else self.change_rumble('normal')
        