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
        self.open_emulation = False

    @abstractmethod
    def _create_controller(self):
        pass

    def change_mode(self):
        self.open_emulation = not self.open_emulation
        print(f'模拟手柄已{"启用" if self.open_emulation else "关闭"}')
        

    def on_circle(self):
        if self.open_emulation:
            self.gamepad.DoubleDodge()

    def on_left_trigger_down(self):
        self.left_trigger = True

    def on_left_trigger_up(self):
        self.left_trigger = False

    def on_pad_up_down(self):
        self.pad_up = True

    def on_pad_up_up(self):
        self.pad_up = False

    def run(self):
        self._setup_callbacks()
        self.controller.start()
        while self.is_running:
            if self.left_trigger and self.pad_up:
                time.sleep(0.5)
                self.change_mode()
            time.sleep(0.001)
        self.controller.stop()

    @abstractmethod
    def _setup_callbacks(self):
        pass