from emulators.dualsense_emulator import DualSenseEmulator
from emulators.xbox_emulator import XboxEmulator
from utils.hid_hide import HidHide

def main():
    while True:
        choice = input("请选择要使用的控制器:\n0. DualSense\n1. Xbox\n7. HidHide管理\n请输入数字: ")
        if choice == '0':
            emulator = DualSenseEmulator("ds4")
            break
        elif choice == '1':
            emulator = XboxEmulator("xbox")
            break
        elif choice == '7':
            print("HidHide管理")
            HidHide().hide_panel(True)
            return
        else:
            print("无效选项，请重新选择。")
    
    emulator.run()

if __name__ == "__main__":
    main()