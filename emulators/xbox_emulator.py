from .base_emulator import BaseEmulator
from controllers.xbox_controller import XboxController
import winsound

class XboxEmulator(BaseEmulator):
    def _create_controller(self):
        return XboxController()

    def _setup_callbacks(self):
        self.controller.add_callback('lt', 'change', self.on_left_trigger)
        self.controller.add_callback('b', 'press', self.on_circle)
        self.controller.add_callback('dpad_up', 'press', self.on_pad_up_down)
        self.controller.add_callback('dpad_up', 'release', self.on_pad_up_up)
        
    def on_left_trigger(self, value):
        if value > 0.5 and not self.left_trigger:
            self.left_trigger = True
        elif value <= 0.01 and self.left_trigger:
            self.left_trigger = False
            
    def change_mode(self):
        super().change_mode()
        if self.open_emulation:
            winsound.Beep(900, 30)
        else:
            winsound.Beep(400, 50)