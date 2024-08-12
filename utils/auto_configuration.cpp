#include <iostream>
#include <windows.h>
#include <filesystem>
#include <cstdlib>
#include <conio.h>
#include <string>
#include <shellapi.h>
#include <fstream>

// 设置控制台为UTF-8编码
void setConsoleEncoding() {
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
}

// 使用 curl 下载文件
bool downloadFile(const std::wstring& url, const std::wstring& output) {
    std::wstring command = L"curl -L -o \"" + output + L"\" \"" + url + L"\"";
    return system(std::string(command.begin(), command.end()).c_str()) == 0;
}

// 安装HidHide
bool installHidHide() {
    std::wstring hidhideInstaller = L"HidHide_1.5.230_x64.exe";
    std::wstring hidhideUrl = L"https://github.com/nefarius/HidHide/releases/download/v1.5.230.0/HidHide_1.5.230_x64.exe";

    std::cout << "下载HidHide安装程序..." << std::endl;
    if (!downloadFile(hidhideUrl, hidhideInstaller)) {
        std::cerr << "下载HidHide失败。" << std::endl;
        return false;
    }

    std::cout << "安装HidHide..." << std::endl;
    if (system("HidHide_1.5.230_x64.exe /quiet /norestart") != 0) {
        std::cerr << "HidHide安装失败。" << std::endl;
        return false;
    }

    std::filesystem::remove(hidhideInstaller); // 删除安装文件
    return true;
}

// 检查HidHide是否安装
bool isHidHideInstalled() {
    HKEY hKey;
    LPCWSTR subKey = L"SOFTWARE\\Nefarius Software Solutions e.U.\\HidHide";
    LPCWSTR valueName = L"Path";
    wchar_t value[260] = L""; // 初始化为一个空字符串
    DWORD value_length = sizeof(value);

    if (RegOpenKeyExW(HKEY_LOCAL_MACHINE, subKey, 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        if (RegQueryValueExW(hKey, valueName, NULL, NULL, (LPBYTE)value, &value_length) == ERROR_SUCCESS) {
            if (wcslen(value) > 0) {
                std::cout << "HidHide路径为: ";
                std::wcout << value << std::endl;
                RegCloseKey(hKey);
                return true;
            }
        }
        RegCloseKey(hKey);
    }
    return false;
}

// 下载并解压Python
bool setupPython() {
    std::wstring pythonZip = L"python.zip";
    std::wstring pythonUrl = L"https://github.com/ccc007ccc/ZenlessZoneZero-GamepadKing/archive/refs/heads/venv.zip";
    std::wstring pythonDir = L"python_env";

    std::cout << "下载Python..." << std::endl;
    if (!downloadFile(pythonUrl, pythonZip)) {
        std::cerr << "下载Python失败。" << std::endl;
        return false;
    }

    std::cout << "解压Python..." << std::endl;
    std::wstring unzipCommand = L"powershell -Command \"Expand-Archive -Path '" + pythonZip + L"' -DestinationPath '" + pythonDir + L"'\"";
    if (system(std::string(unzipCommand.begin(), unzipCommand.end()).c_str()) != 0) {
        std::cerr << "解压Python失败。" << std::endl;
        return false;
    }

    std::filesystem::remove(pythonZip); // 删除压缩包
    // 移动Python到当前目录
    std::wstring moveCommand = L"move /Y '" + pythonDir + L"\\ZenlessZoneZero-GamepadKing-venv' python_env";

    return true;
}

// 检测pip是否安装
bool isPipInstalled() {
    std::wstring pipPath = L"python_env\\Scripts\\pip.exe";
    return std::filesystem::exists(pipPath);
}

// 安装pip
bool installPip() {
    std::wstring pipInstaller = L"get-pip.py";
    std::wstring pipUrl = L"https://bootstrap.pypa.io/get-pip.py";

    std::cout << "下载Pip安装程序..." << std::endl;
    if (!downloadFile(pipUrl, pipInstaller)) {
        std::cerr << "下载Pip安装程序失败。" << std::endl;
        return false;
    }
    if (system("python_env\\python.exe get-pip.py") != 0) {
        std::cerr << "Pip安装失败。" << std::endl;
        return false;
    }
    std::filesystem::remove(pipInstaller);
    return true;
}

// 检查Python环境是否已设置
bool isPythonSetup() {
    return std::filesystem::exists("python_env\\python.exe");
}

// 检查是否存在main.py
bool isMainPyExists() {
    if (std::filesystem::exists("main.py")) {
        std::cout << "main.py 文件存在" << std::endl;
        return true;
    } else {
        std::cerr << "main.py 文件不存在，请检查文件夹内容。" << std::endl;
        return false;
    }
}


// 安装依赖项
bool installDependencies() {
    std::cout << "安装Python依赖项..." << std::endl;
    std::wstring pipCommand = L"python_env\\Scripts\\pip.exe install -r requirements.txt";
    if (system(std::string(pipCommand.begin(), pipCommand.end()).c_str()) != 0) {
        std::cerr << "依赖安装失败。" << std::endl;
        return false;
    }
    return true;
}

// 运行Python脚本
bool runPythonScript() {
    std::cout << "启动Python脚本..." << std::endl;
    if (system("python_env\\python.exe main.py") != 0) {
        std::cerr << "Python脚本运行失败。" << std::endl;
        return false;
    }
    return true;
}

// 等待用户按任意键关闭程序
void waitForKeyPress() {
    std::cout << "按任意键关闭程序..." << std::endl;
    _getch();  // 等待用户按任意键
}

int main() {
    setConsoleEncoding(); // 设置控制台编码为UTF-8

    if (!isHidHideInstalled()) {
        if (!installHidHide()) {
            waitForKeyPress();
            std::exit(EXIT_FAILURE);
        }
    }

    if (!isPythonSetup()) {
        if (!setupPython()) {
            waitForKeyPress();
            std::exit(EXIT_FAILURE);
        }
    }

    if (!isPipInstalled()) {
        if (!installPip()) {
            waitForKeyPress();
            std::exit(EXIT_FAILURE);
        }
    }

    if (!isMainPyExists()) {
        waitForKeyPress();
        std::exit(EXIT_FAILURE);
    }


    // 安装依赖项
    if (!installDependencies()) {
        waitForKeyPress();
        std::exit(EXIT_FAILURE);
    }

    if (!runPythonScript()) {
        waitForKeyPress();
        std::exit(EXIT_FAILURE);
    }

    waitForKeyPress();  // 正常运行后也等待用户按键
    return 0;
}