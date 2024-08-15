import sys, time
import ctypes
import yaml
import io
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from emulators.dualsense_emulator import DualSenseEmulator
from emulators.xbox_emulator import XboxEmulator
from utils.hid_hide import HidHide

# 重定向标准输出到自定义的StringIO对象
class StringIORedirect(io.StringIO):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)

    def flush(self):
        pass

class EmulatorThread(threading.Thread):
    def __init__(self, emulator, output_text_widget):
        super().__init__()
        self.emulator = emulator
        self.output_text_widget = output_text_widget
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self._stop_event = threading.Event()

    def run(self):
        try:
            sys.stdout = StringIORedirect(self.output_text_widget)
            sys.stderr = StringIORedirect(self.output_text_widget)
            while not self._stop_event.is_set():
                self.emulator.run()  # 假设 emulator.run() 是一个可以被多次调用的方法
        except Exception as e:
            print(f"错误: {str(e)}")
        finally:
            sys.stdout = self.stdout
            sys.stderr = self.stderr

    def stop(self):
        self._stop_event.set()
        self.emulator.stop()

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GamepadKing Emulator")
        self.geometry("600x400")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # 设置窗口图标和任务栏图标
        self.iconbitmap("gui/img/favicon.ico")  # 请确保图标路径和文件存在

        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("starter")
        except AttributeError:
            pass

        self.setup_ui()
        self.load_config()

        self.emulator = None
        self.emulator_thread = None

        if self.auto_start_var.get():
            self.start_emulation()

    def setup_ui(self):
        controller_frame = ttk.Frame(self)
        controller_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(controller_frame, text="物理手柄:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.physical_controller_combo = ttk.Combobox(controller_frame, values=["dualsense", "xbox"])
        self.physical_controller_combo.grid(row=0, column=1, padx=5, pady=5)
        self.physical_controller_combo.current(0)

        ttk.Label(controller_frame, text="模拟手柄:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.emulated_controller_combo = ttk.Combobox(controller_frame, values=["ds4", "xbox"])
        self.emulated_controller_combo.grid(row=0, column=3, padx=5, pady=5)
        self.emulated_controller_combo.current(0)

        config_frame = ttk.Frame(self)
        config_frame.pack(fill=tk.X, padx=10, pady=5)

        self.macro_var = tk.BooleanVar(value=True)
        self.macro_checkbox = ttk.Checkbutton(config_frame, text="启用宏", variable=self.macro_var)
        self.macro_checkbox.grid(row=0, column=0, padx=5, pady=5)

        self.auto_start_var = tk.BooleanVar(value=False)
        self.auto_start_checkbox = ttk.Checkbutton(config_frame, text="下次启动程序是否自动启动模拟", variable=self.auto_start_var)
        self.auto_start_checkbox.grid(row=0, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        self.start_button = ttk.Button(button_frame, text="开始模拟", command=self.start_emulation)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = ttk.Button(button_frame, text="停止模拟", command=self.stop_emulation, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)

        self.save_config_button = ttk.Button(button_frame, text="保存配置", command=self.save_config)
        self.save_config_button.grid(row=0, column=2, padx=5, pady=5)

        self.load_config_button = ttk.Button(button_frame, text="读取配置", command=self.load_config)
        self.load_config_button.grid(row=0, column=3, padx=5, pady=5)

        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def load_config(self):
        try:
            with open('config.yml', 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.physical_controller_combo.set(config.get('physical_controller', 'dualsense'))
                self.emulated_controller_combo.set(config.get('emulated_controller', 'ds4'))
                self.macro_var.set(config.get('macro', True))
                self.auto_start_var.set(config.get('auto_start', False))

            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "配置已加载。\n")
            self.output_text.config(state=tk.DISABLED)
        except FileNotFoundError:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "找不到配置文件，使用默认设置。\n")
            self.output_text.config(state=tk.DISABLED)
        except Exception as e:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"加载配置时出错: {str(e)}\n")
            self.output_text.config(state=tk.DISABLED)

    def save_config(self):
        config = {
            'auto_start': self.auto_start_var.get(),
            'physical_controller': self.physical_controller_combo.get(),
            'emulated_controller': self.emulated_controller_combo.get(),
            'macro': self.macro_var.get(),
        }

        config_template = """
# GamepadKing Emulator 配置文件

# 物理手柄类型 可选择 dualSense, xbox
physical_controller: {physical_controller}

# 模拟手柄类型 可选择 ds4, xbox
emulated_controller: {emulated_controller}

# 是否在启动程序时自动开始模拟
auto_start: {auto_start}

# 是否启用宏
macro: {macro}
        """

        try:
            with open('config.yml', 'w', encoding='utf-8') as f:
                f.write(config_template.format(**config))

            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "配置已保存。\n")
            self.output_text.config(state=tk.DISABLED)
        except Exception as e:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"保存配置时出错: {str(e)}\n")
            self.output_text.config(state=tk.DISABLED)

    def start_emulation(self):
        if self.emulator is not None:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "模拟已在运行中。\n")
            self.output_text.config(state=tk.DISABLED)
            return

        physical_controller = self.physical_controller_combo.get().lower()
        emulated_controller = self.emulated_controller_combo.get()
        macro = self.macro_var.get()

        if physical_controller == "dualsense":
            self.emulator = DualSenseEmulator(emulated_controller, "ds4", macro)
        elif physical_controller == "xbox":
            self.emulator = XboxEmulator(emulated_controller, "xbox", macro)

        self.emulator_thread = EmulatorThread(self.emulator, self.output_text)
        self.emulator_thread.start()

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "模拟已开始。\n")
        self.output_text.config(state=tk.DISABLED)
        

    def stop_emulation(self, close_window=False):
        if self.emulator is not None:
            self.stop_button.config(state=tk.DISABLED)  # 禁用停止模拟按钮
            self.output_text.config(state=tk.NORMAL)
            print("正在停止模拟...")
            self.output_text.insert(tk.END, "正在停止模拟...\n")
            self.output_text.config(state=tk.DISABLED)

            def stop_emulator_thread():
                self.emulator_thread.stop()
                self.emulator_thread.join()  # 等待线程结束

                self.emulator = None
                self.emulator_thread = None
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)

                self.output_text.config(state=tk.NORMAL)
                print("模拟已停止。")
                self.output_text.insert(tk.END, "模拟已停止。\n")
                self.output_text.config(state=tk.DISABLED)

                HidHide().hide_panel(True, True)
                
                if close_window:
                    self.close_window()

            threading.Thread(target=stop_emulator_thread,daemon=True).start()  # 在单独的线程中执行停止操作

    def close_window(self):
        self.destroy()
    def on_closing(self):
        if self.emulator is not None:
            self.stop_emulation(True)
        else:
            self.close_window()

if __name__ == "__main__":
    window = MainWindow()
    window.mainloop()
