from .base_emulator import BaseEmulator
from controllers.dualsense_controller import DualSenseController

class DualSenseEmulator(BaseEmulator):
    def _create_controller(self):
        return DualSenseController()

    def _setup_callbacks(self):
        self.controller.add_callback('left_trigger', 'change', self.on_left_trigger)
        self.controller.add_callback('circle', 'press', self.on_circle)
        self.controller.add_callback('up', 'press', self.on_pad_up_down)
        self.controller.add_callback('up', 'release', self.on_pad_up_up)

    def on_left_trigger(self, value):
        if value > 0.5 and not self.left_trigger:
            self.left_trigger = True
        elif value <= 0.01 and self.left_trigger:
            self.left_trigger = False

    def change_mode(self):
        super().change_mode()
        self.controller.set_lightbar_color('red' if self.open_emulation else 'blue')
        self.controller.set_rumble('left', 60 if self.open_emulation else 0, 0.05)
        self.controller.set_rumble('right', 0 if self.open_emulation else 80, 0.05)