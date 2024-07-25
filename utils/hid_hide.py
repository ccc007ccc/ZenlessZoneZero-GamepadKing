import subprocess, sys, winreg, json, re

class HidHide:
    def __init__(self):
        # 初始化时获取 HidHide 的路径和 CLI 的路径
        self.hid_hide_path = self.get_hid_hide_path()
        self.hid_hide_cli_path = self.get_hid_hide_cli_path()
        
    def read_registry_value(self, key, subkey, value_name):
        # 读取注册表值
        try:
            registry_key = winreg.OpenKey(key, subkey, 0, winreg.KEY_READ)
            value, regtype = winreg.QueryValueEx(registry_key, value_name)
            winreg.CloseKey(registry_key)
            return value
        except WindowsError as e:
            print(f"错误的键或值: {e}")
            return None
        
    def get_hid_hide_path(self):
        # 获取 HidHide 的安装路径
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Nefarius Software Solutions e.U.\HidHide"
        value_name = "Path"

        value = self.read_registry_value(key, subkey, value_name)
        if value:
            print(f"HidHide路径为: {value}")
            return value
        else:
            print("未找到HidHide路径，请检查是否安装HidHide")
            return None
        
    def get_hid_hide_cli_path(self):
        # 获取 HidHideCLI.exe 的路径
        if self.hid_hide_path:
            path = self.hid_hide_path + "x64\\HidHideCLI.exe"
            print(f"HidHideCLI路径为: {path}")
            return path
        return None

    def run_command(self, command):
        # 运行命令并返回输出
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            if result.stderr == "":
                return result.stdout
            else:
                return result.stdout, result.stderr
        except Exception as e:
            return "", f"运行命令时出错: {e}"

    def app_clean(self):
        # 移除不存在的注册应用程序
        return self.run_command(f'"{self.hid_hide_cli_path}" --app-clean')
        
    def app_list(self):
        # 列出注册的应用程序
        return self.run_command(f'"{self.hid_hide_cli_path}" --app-list')
        
    def app_reg(self, path):
        # 注册应用程序使其可以看到隐藏设备
        return self.run_command(f'"{self.hid_hide_cli_path}" --app-reg "{path}"')
        
    def app_unreg(self, path):
        # 撤销应用程序查看隐藏设备的权限
        return self.run_command(f'"{self.hid_hide_cli_path}" --app-unreg "{path}"')
        
    def cancel(self):
        # 退出而不保存配置更改
        return self.run_command(f'"{self.hid_hide_cli_path}" --cancel')
        
    def cloak_off(self):
        # 停用 HID 设备隐藏
        return self.run_command(f'"{self.hid_hide_cli_path}" --cloak-off')
        
    def cloak_on(self):
        # 启用 HID 设备隐藏
        return self.run_command(f'"{self.hid_hide_cli_path}" --cloak-on')
        
    def cloak_state(self):
        # 报告当前的隐藏状态
        return self.run_command(f'"{self.hid_hide_cli_path}" --cloak-state')
        
    def cloak_toggle(self):
        # 切换隐藏状态
        return self.run_command(f'"{self.hid_hide_cli_path}" --cloak-toggle')
        
    def dev_all(self):
        # 列出所有 HID 设备
        return self.run_command(f'"{self.hid_hide_cli_path}" --dev-all')
        
    def dev_gaming(self):
        # 列出所有用于游戏的 HID 设备
        return self.run_command(f'"{self.hid_hide_cli_path}" --dev-gaming')
        
    def dev_hide(self, device_instance_path, auto = False):
        # 隐藏指定的设备
        if self.is_hidden(device_instance_path) and auto == True:
            print(f'设备{self.parse_dev_gaming_name(device_instance_path)}已解除隐藏')
            return self.dev_unhide(device_instance_path)
        else:
            print(f'设备{self.parse_dev_gaming_name(device_instance_path)}已隐藏')
            return self.run_command(f'"{self.hid_hide_cli_path}" --dev-hide "{device_instance_path}"')
        
    def dev_list(self):
        # 运行 `--dev-list` 命令并获取输出
        stdout = self.run_command(f'"{self.hid_hide_cli_path}" --dev-list')
        
        # 使用正则表达式提取所有 deviceInstancePath
        device_instance_paths = re.findall(r'--dev-hide\s+"([^"]+)"', stdout)
        
        if device_instance_paths:
            return device_instance_paths
        else:
            print("未找到任何设备实例路径")
            return []
        
        
    def dev_unhide(self, device_instance_path):
        # 取消隐藏指定的设备
        return self.run_command(f'"{self.hid_hide_cli_path}" --dev-unhide "{device_instance_path}"')
        
    def inv_off(self):
        # 关闭逆应用程序列表
        return self.run_command(f'"{self.hid_hide_cli_path}" --inv-off')
        
    def inv_on(self):
        # 打开逆应用程序列表
        return self.run_command(f'"{self.hid_hide_cli_path}" --inv-on')
        
    def inv_state(self):
        # 显示逆应用程序列表状态
        return self.run_command(f'"{self.hid_hide_cli_path}" --inv-state')
        
    def version(self):
        # 显示配置客户端版本
        return self.run_command(f'"{self.hid_hide_cli_path}" --version')

    def app_reg_python(self):
        try:
            # 获取当前运行的 Python 程序的路径并注册它
            python_path = sys.executable
            self.app_reg(python_path)
            print(f'当前运行的 Python 程序路径为: {python_path}, 已注册到 HidHide 中')
        except Exception as e:
            print(f"HidHide 注册 Python 程序时出错: {e}")
            
    def parse_dev_gaming(self):
        # 运行 `--dev-gaming` 命令并获取输出
        stdout = self.run_command(f'"{self.hid_hide_cli_path}" --dev-gaming')
        
        try:
            # 解析 JSON 输出
            devices = json.loads(stdout)
            return devices
        except TypeError as e:
            print("请不要在使用脚本时开启HidHideClient!!!")
            return None
    def parse_dev_gaming_name(self, index=None):
        # 解析 `--dev-gaming` 输出并获取 friendlyName
        devices = self.parse_dev_gaming()
        
        if devices is None:
            return None
        elif index is None:
        # 如果 index 为空，返回所有 friendlyName
            return [device["friendlyName"] for device in devices]
        
        elif isinstance(index, int):
            # 如果 index 是整数，返回指定索引的 friendlyName
            if 0 <= index < len(devices):
                return devices[index]["friendlyName"]
            else:
                print("索引超出范围")
                return None
        elif isinstance(index, str):
            # 如果 index 是字符串，假设它是 deviceInstancePath，查找对应的 friendlyName
            for device in devices:
                for dev in device.get("devices", []):
                    if dev.get("deviceInstancePath") == index:
                        return device["friendlyName"]
            print(f"设备实例路径 '{index}' 未找到")
            return None
    
    def parse_dev_gaming_path(self, index=None):
        # 解析 `--dev-gaming` 输出并获取 deviceInstancePath
        devices = self.parse_dev_gaming()
        
        if devices is None:
            return None
        
        # 获取所有设备的 deviceInstancePath
        device_instance_paths = []
        for device in devices:
            for dev in device.get("devices", []):
                if "deviceInstancePath" in dev:
                    device_instance_paths.append(dev["deviceInstancePath"])
        
        # 如果 index 为空，返回所有 deviceInstancePath
        if index is None:
            return device_instance_paths
        
        # 否则返回指定 index 的 deviceInstancePath
        if 0 <= index < len(device_instance_paths):
            return device_instance_paths[index]
        else:
            print("索引超出范围")
            return None

    def is_hidden(self, device_instance_path : str):
        """
        判断指定设备是否被隐藏
        :param device_instance_path: 设备实例路径
        :return: True/False
        """
        hidden_devices = self.dev_list()
        
        if hidden_devices is None:
            print("获取隐藏设备列表失败")
            return False
        
        # 比较指定设备实例路径是否在隐藏设备列表中
        return device_instance_path in hidden_devices
    
    # 隐藏面板
    def hide_panel(self, auto = False):
        """
        隐藏面板
        :param device_instance_path: 设备实例路径
        :return: True/False
        """
        while True:
            device_list = self.parse_dev_gaming_name()
            # 如果列表中实例数量大于1
            if len(device_list) > 1 or auto:
                for index, device in enumerate(device_list):
                    if self.is_hidden(self.parse_dev_gaming_path(index)):
                        print(f"{index} : {device} 已隐藏")
                    else:
                        print(f"{index} : {device}")
                if auto:
                    index = int(input("请输入要隐藏或解除隐藏的设备序号："))
                else:
                    index = int(input("请输入要隐藏的设备序号："))
                if index < len(device_list):
                    if auto:
                        self.dev_hide(self.parse_dev_gaming_path(index),True)
                    else:
                        self.dev_hide(self.parse_dev_gaming_path(index))
                    break
                else:
                    print("输入错误")
            else:
                self.dev_hide(self.parse_dev_gaming_path(0))
                break
                


if __name__ == "__main__":
    hid_hide = HidHide()
    if hid_hide.hid_hide_cli_path:
        while True:
            device_list = hid_hide.parse_dev_gaming_name()
            for index, device in enumerate(device_list):
                if hid_hide.is_hidden(hid_hide.parse_dev_gaming_path(index)):
                    print(f"{index} : {device} 已隐藏")
                else:
                    print(f"{index} : {device}")
            index = int(input("请输入要隐藏的设备序号："))
            if index < len(device_list):
                hid_hide.dev_hide(hid_hide.parse_dev_gaming_path(index), True)
            else:
                print("输入错误")
        
            
        