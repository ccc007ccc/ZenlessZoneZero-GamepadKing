from emulators.dualsense_emulator import DualSenseEmulator
from emulators.xbox_emulator import XboxEmulator
from utils.hid_hide import HidHide

def main():
    while True:
        choice = input("请选择你的手柄:\n0. DualSense\n1. Xbox\n7. HidHide管理\n请输入数字: ")
        #第一个选择
        if choice == '0':
            # DualSenseEmulator("模拟成的手柄类型", "物理手柄类型")
            emulator = DualSenseEmulator("ds4", "ds4")
            break
        elif choice == '1':
            # XboxEmulator("模拟成的手柄类型", "物理手柄类型")
            emulator = XboxEmulator("xbox", "xbox")
            break
        elif choice == '7':
            print("HidHide管理")
            HidHide().hide_panel(True)
            return
        else:
            print("无效选项，请重新选择。")
    try:
        emulator.run()
    except KeyboardInterrupt:
        emulator.stop()
        HidHide().hide_panel(True,True)
        print("程序已退出。")
        return
if __name__ == "__main__":
    main()