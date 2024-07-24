from emulators.dualsense_emulator import DualSenseEmulator
from emulators.xbox_emulator import XboxEmulator

def main():
    while True:
        choice = input("请选择要使用的控制器:\n1. DualSense\n2. Xbox\n输入数字: ")
        if choice == '1':
            emulator = DualSenseEmulator("xbox")
            break
        elif choice == '2':
            emulator = XboxEmulator("ds4")
            break
        else:
            print("无效选项，请重新选择。")
    
    emulator.run()

if __name__ == "__main__":
    main()