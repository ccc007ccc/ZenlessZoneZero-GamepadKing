import sys, ctypes, yaml, io
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTextEdit, QLabel, QCheckBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QThread, Signal
from emulators.dualsense_emulator import DualSenseEmulator
from emulators.xbox_emulator import XboxEmulator
from utils.hid_hide import HidHide

# 重定向标准输出到自定义的StringIO对象
class StringIORedirect(io.StringIO):
    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    def write(self, string):
        self.signal.emit(string)

class EmulatorThread(QThread):
    output_signal = Signal(str)

    def __init__(self, emulator):
        super().__init__()
        self.emulator = emulator
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def run(self):
        try:
            # 重定向标准输出和标准错误
            sys.stdout = StringIORedirect(self.output_signal)
            sys.stderr = StringIORedirect(self.output_signal)
            self.emulator.run()
        except Exception as e:
            self.output_signal.emit(f"错误: {str(e)}")
        finally:
            # 恢复标准输出和标准错误
            sys.stdout = self.stdout
            sys.stderr = self.stderr

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("starter")
        self.setWindowTitle("GamepadKing Emulator")
        self.setWindowIcon(QIcon("gui/img/favicon.png"))
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.setup_ui()
        self.load_config()

        self.emulator = None
        self.emulator_thread = None

        if self.auto_start_checkbox.isChecked():
            self.start_emulation()
    def setup_ui(self):
        # 下拉框用于选择控制器
        self.physical_controller_combo = QComboBox()
        self.physical_controller_combo.addItems(["dualsense", "xbox"])
        self.emulated_controller_combo = QComboBox()
        self.emulated_controller_combo.addItems(["ds4", "xbox"])

        combo_layout = QHBoxLayout()
        combo_layout.addWidget(QLabel("物理手柄:"))
        combo_layout.addWidget(self.physical_controller_combo)
        combo_layout.addWidget(QLabel("模拟手柄:"))
        combo_layout.addWidget(self.emulated_controller_combo)
        self.layout.addLayout(combo_layout)
        
        # 多选框配置布局
        self.conifg_layout = QHBoxLayout()
        self.macro_checkbox = QCheckBox("启用宏")
        self.macro_checkbox.setChecked(True)
        self.auto_start_checkbox = QCheckBox("下次启动程序是否自动启动模拟")
        self.auto_start_checkbox.setChecked(False)
        self.conifg_layout.addWidget(self.macro_checkbox)
        self.conifg_layout.addWidget(self.auto_start_checkbox)
        self.layout.addLayout(self.conifg_layout)
        

        # 按钮
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("开始模拟")
        self.start_button.clicked.connect(self.start_emulation)
        self.stop_button = QPushButton("停止模拟")
        self.stop_button.clicked.connect(self.stop_emulation)
        self.stop_button.setEnabled(False)
        self.save_config_button = QPushButton("保存配置")
        self.save_config_button.clicked.connect(self.save_config)
        self.load_config_button = QPushButton("读取配置")
        self.load_config_button.clicked.connect(self.load_config)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.save_config_button)
        button_layout.addWidget(self.load_config_button)
        self.layout.addLayout(button_layout)

        # 输出文本区域
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

    def load_config(self):
        try:
            with open('config.yml', 'r', encoding='utf-8') as f:
                config_str = f.read()
                config = yaml.safe_load(config_str)
                self.physical_controller_combo.setCurrentText(config.get('physical_controller', 'dualsense'))
                self.emulated_controller_combo.setCurrentText(config.get('emulated_controller', 'ds4'))
                self.macro_checkbox.setChecked(config.get('macro', True))
                self.auto_start_checkbox.setChecked(config.get('auto_start', False))
                
            self.output_text.append("配置已加载。")
        except FileNotFoundError:
            self.output_text.append("找不到配置文件，使用默认设置。")
        except Exception as e:
            self.output_text.append(f"加载配置时出错: {str(e)}")

    def save_config(self):
        config = {
            'auto_start': self.auto_start_checkbox.isChecked(),
            'physical_controller': self.physical_controller_combo.currentText(),
            'emulated_controller': self.emulated_controller_combo.currentText(),
            'macro': self.macro_checkbox.isChecked(),
        }
        
        # 定义配置文件的模板，包括注释和顺序
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
            self.output_text.append("配置已保存。")
        except Exception as e:
            self.output_text.append(f"保存配置时出错: {str(e)}")

    def start_emulation(self):
        if self.emulator is not None:
            self.output_text.append("模拟已在运行中。")
            return

        physical_controller = self.physical_controller_combo.currentText().lower()
        emulated_controller = self.emulated_controller_combo.currentText()
        macro = self.macro_checkbox.isChecked()

        if physical_controller == "dualsense":
            self.emulator = DualSenseEmulator(emulated_controller, "ds4", macro)
        elif physical_controller == "xbox":
            self.emulator = XboxEmulator(emulated_controller, "xbox", macro)

        self.emulator_thread = EmulatorThread(self.emulator)
        self.emulator_thread.output_signal.connect(self.update_output)
        self.emulator_thread.start()

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.output_text.append("模拟已开始。")

    def stop_emulation(self):
        if self.emulator is not None:
            self.emulator.stop()
            self.emulator_thread.wait()
            self.emulator = None
            self.emulator_thread = None
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.output_text.append("模拟已停止。")
            HidHide().hide_panel(True, True)

    def update_output(self, text):
        self.output_text.append(text.strip())
    
    def closeEvent(self, event):
        if self.emulator is not None:
            self.stop_emulation()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())