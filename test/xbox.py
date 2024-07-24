from ..controllers.xbox_controller import XboxController
import time

class XboxControllerTester:
    def __init__(self):
        self.controller = XboxController()

    def setup_callbacks(self):
        buttons = ['a', 'b', 'x', 'y', 'lb', 'rb', 'back', 'start', 'ls', 'rs', 
                   'dpad_up', 'dpad_down', 'dpad_left', 'dpad_right']
        
        for button in buttons:
            self.controller.add_callback(button, 'press', lambda b=button: self.on_button_press(b))
            self.controller.add_callback(button, 'release', lambda b=button: self.on_button_release(b))

        analog_inputs = ['ls_x', 'ls_y', 'rs_x', 'rs_y', 'lt', 'rt']
        for input in analog_inputs:
            self.controller.add_callback(input, 'change', lambda v, i=input: self.on_analog_change(i, v))

    def on_button_press(self, button):
        print(f"{button.upper()} 按下")

    def on_button_release(self, button):
        print(f"{button.upper()} 释放")

    def on_analog_change(self, input, value):
        print(f"{input.upper()}: {value}")

    def run(self):
        self.setup_callbacks()
        self.controller.start()
        print("Xbox控制器测试程序启动。按 Ctrl+C 退出。")
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n程序退出")
        finally:
            self.controller.stop()

if __name__ == "__main__":
    tester = XboxControllerTester()
    tester.run()