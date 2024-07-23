from Controller.DualSense import DualSenseEmulator
from Controller.Xbox import XboxEmulator 
def main():
    while True:
        choice = input("请选择要使用的控制器:\n1. DualSense\n2. Xbox\n")
        if choice == '1':
            dualsense_emulator = DualSenseEmulator()
            dualsense_emulator.run()
            break
        elif choice == '2':
            xbox_emulator = XboxEmulator() 
            xbox_emulator.run()
            break
        else:
            print("无效选项，请重新选择。")
if __name__ == "__main__":
    main()