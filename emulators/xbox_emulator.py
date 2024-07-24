from .base_emulator import BaseEmulator
from controllers.xbox_controller import XboxController
import winsound

class XboxEmulator(BaseEmulator):
    def _create_controller(self):
        return XboxController()
    
    def change_mode(self):
        super().change_mode()
        if self.king_mode:
            winsound.Beep(900, 30)
        else:
            winsound.Beep(400, 50)