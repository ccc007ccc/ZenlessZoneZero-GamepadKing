import sys
import tkinter as tk
from tkinter import ttk, messagebox
import yaml
from PIL import Image, ImageTk
from threading import Thread
from queue import Queue, Empty
from emulators.dualsense_emulator import DualSenseEmulator
from emulators.xbox_emulator import XboxEmulator
from utils.hid_hide import HidHide

class EmulatorThread(Thread):
    def __init__(self, emulator, output_queue):
        super().__init__()
        self.emulator = emulator
        self.output_queue = output_queue
        self.running = True

    def run(self):
        try:
            self.emulator.run()
        except Exception as e:
            self.output_queue.put(f"错误: {str(e)}")
        finally:
            self.running = False

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GamepadKing Emulator")        # 锁定窗口大小
        self.resizable(False, False)
        self.geometry("600x400")

        # Configuration
        self.config_file = 'config.yml'
        self.auto_start = tk.BooleanVar()
        self.macro = tk.BooleanVar()
        self.physical_controller = tk.StringVar(value='dualsense')
        self.emulated_controller = tk.StringVar(value='ds4')
        self.emulator = None
        self.emulator_thread = None
        self.output_queue = Queue()
        # 设置窗口图标
        self.set_window_icon('gui\\img\\favicon.png')  # 更换为你的图标路径
        self.setup_ui()
        self.load_config()

        if self.auto_start.get():
            self.start_emulation()
            
    def set_window_icon(self, icon_path):
        try:
            # 使用 Pillow 处理图标（支持更多格式）
            image = Image.open(icon_path)
            self.iconphoto(True, ImageTk.PhotoImage(image))
        except Exception as e:
            messagebox.showerror("图标设置错误", f"无法加载图标: {e}")
    def setup_ui(self):
        # Setup UI elements
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Physical Controller
        ttk.Label(frame, text="物理手柄:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        physical_controller_combo = ttk.Combobox(frame, textvariable=self.physical_controller, values=["dualsense", "xbox"])
        physical_controller_combo.grid(row=0, column=1, padx=5, pady=5)

        # Emulated Controller
        ttk.Label(frame, text="模拟手柄:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        emulated_controller_combo = ttk.Combobox(frame, textvariable=self.emulated_controller, values=["ds4", "xbox"])
        emulated_controller_combo.grid(row=1, column=1, padx=5, pady=5)

        # Macro Checkbox
        ttk.Checkbutton(frame, text="启用宏", variable=self.macro).grid(row=2, column=0,  padx=5, pady=5)

        # Auto Start Checkbox
        ttk.Checkbutton(frame, text="下次启动程序是否自动启动模拟", variable=self.auto_start).grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        ttk.Button(frame, text="开始模拟", command=self.start_emulation).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(frame, text="停止模拟", command=self.stop_emulation).grid(row=4, column=1, padx=5, pady=5)

        # Output Text Area
        self.output_text = tk.Text(frame, height=15, state=tk.DISABLED)
        self.output_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

        # Load and Save Config Buttons
        ttk.Button(frame, text="保存配置", command=self.save_config).grid(row=6, column=0, padx=5, pady=5)
        ttk.Button(frame, text="读取配置", command=self.load_config).grid(row=6, column=1, padx=5, pady=5)

        # Start the output update loop
        self.update_output_loop()

    def load_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.physical_controller.set(config.get('physical_controller', 'dualsense'))
                self.emulated_controller.set(config.get('emulated_controller', 'ds4'))
                self.macro.set(config.get('macro', True))
                self.auto_start.set(config.get('auto_start', False))
            self.append_output("配置已加载。")
        except FileNotFoundError:
            self.append_output("找不到配置文件，使用默认设置。")
        except Exception as e:
            self.append_output(f"加载配置时出错: {str(e)}")

    def save_config(self):
        config = {
            'auto_start': self.auto_start.get(),
            'physical_controller': self.physical_controller.get(),
            'emulated_controller': self.emulated_controller.get(),
            'macro': self.macro.get(),
        }

        config_template = f"""
# GamepadKing Emulator 配置文件

# 物理手柄类型 可选择 dualSense, xbox
physical_controller: {config['physical_controller']}

# 模拟手柄类型 可选择 ds4, xbox
emulated_controller: {config['emulated_controller']}

# 是否在启动程序时自动开始模拟
auto_start: {config['auto_start']}

# 是否启用宏
macro: {config['macro']}
        """

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                f.write(config_template)
            self.append_output("配置已保存。")
        except Exception as e:
            self.append_output(f"保存配置时出错: {str(e)}")

    def start_emulation(self):
        if self.emulator is not None:
            self.append_output("模拟已在运行中。")
            return

        physical_controller = self.physical_controller.get().lower()
        emulated_controller = self.emulated_controller.get()
        macro = self.macro.get()

        if physical_controller == "dualsense":
            self.emulator = DualSenseEmulator(emulated_controller, "ds4", macro)
        elif physical_controller == "xbox":
            self.emulator = XboxEmulator(emulated_controller, "xbox", macro)

        self.emulator_thread = EmulatorThread(self.emulator, self.output_queue)
        self.emulator_thread.start()

        self.append_output("模拟已开始。")

    def stop_emulation(self):
        if self.emulator is not None:
            self.emulator.stop()
            self.emulator_thread.join()
            self.emulator = None
            self.emulator_thread = None
            self.append_output("模拟已停止。")
            HidHide().hide_panel(True, True)

    def append_output(self, text):
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.insert(tk.END, text + '\n')
        self.output_text.configure(state=tk.DISABLED)

    def update_output_loop(self):
        while self.emulator_thread and self.emulator_thread.is_alive():
            try:
                text = self.output_queue.get_nowait()
                self.append_output(text)
            except Empty:
                pass
            self.after(100, self.update_output_loop)

    def on_closing(self):
        if self.emulator is not None:
            self.stop_emulation()
        self.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
