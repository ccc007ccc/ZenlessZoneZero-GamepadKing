from .base_emulator import BaseEmulator
from controllers.dualsense_controller import DualSenseController

class DualSenseEmulator(BaseEmulator):
    def _create_controller(self):
        return DualSenseController()

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
    def change_mode(self):
        super().change_mode()
        self.change_lightbar_color('king') if self.king_mode else self.change_lightbar_color('normal')
        self.change_rumble('king') if self.king_mode else self.change_rumble('normal')