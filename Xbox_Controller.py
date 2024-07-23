import threading
import time
from inputs import get_gamepad, UnpluggedError
from typing import Callable

class XboxController:
    def __init__(self):
        self.lt_pressed = False
        self.b_pressed = False
        self.lt_callbacks = {"press": [], "release": []}
        self.b_callbacks = {"press": [], "release": []}
        self.running = False

    def add_lt_callback(self, event: str, callback: Callable):
        if event in ["press", "release"]:
            self.lt_callbacks[event].append(callback)

    def add_b_callback(self, event: str, callback: Callable):
        if event in ["press", "release"]:
            self.b_callbacks[event].append(callback)

    def _read_gamepad(self):
        while self.running:
            try:
                events = get_gamepad()
                for event in events:
                    if event.code == "ABS_Z":  # LT
                        if event.state > 0 and not self.lt_pressed:
                            self.lt_pressed = True
                            for callback in self.lt_callbacks["press"]:
                                callback()
                        elif event.state == 0 and self.lt_pressed:
                            self.lt_pressed = False
                            for callback in self.lt_callbacks["release"]:
                                callback()
                    elif event.code == "BTN_EAST":  # B
                        if event.state == 1 and not self.b_pressed:
                            self.b_pressed = True
                            for callback in self.b_callbacks["press"]:
                                callback()
                        elif event.state == 0 and self.b_pressed:
                            self.b_pressed = False
                            for callback in self.b_callbacks["release"]:
                                callback()
                time.sleep(0.001)  # Adjust sleep time if necessary
            except UnpluggedError:
                print("手柄断开,一秒后重连")
                time.sleep(1)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._read_gamepad, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

# # 使用示例
# if __name__ == "__main__":
#     def lt_pressed():
#         print("LT pressed")

#     def lt_released():
#         print("LT released")

#     def b_pressed():
#         print("B pressed")

#     def b_released():
#         print("B released")

#     controller = XboxController()
#     controller.add_lt_callback("press", lt_pressed)
#     controller.add_lt_callback("release", lt_released)
#     controller.add_b_callback("press", b_pressed)
#     controller.add_b_callback("release", b_released)

#     controller.start()

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         controller.stop()
