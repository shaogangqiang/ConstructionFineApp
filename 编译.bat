@echo off
chcp 65001 >nul
echo ====================================
echo    施工现场罚款系统 - 编译脚本
echo ====================================
echo.

echo 检查 Python 环境...
python --version
if errorlevel 1 (
    echo ❌ Python 未安装或未添加到 PATH
    echo 请访问 https://www.python.org/downloads/ 安装 Python 3.8+
    pause
    exit /b
)

echo ✅ Python 环境正常
echo.

echo 检查 buildozer 是否安装...
python -c "import buildozer" 2>nul
if errorlevel 1 (
    echo ⚠️ buildozer 未安装，正在安装...
    pip install buildozer
    if errorlevel 1 (
        echo ❌ buildozer 安装失败
        pause
        exit /b
    )
)

echo ✅ buildozer 已安装
echo.

echo ====================================
echo    开始编译 APK
echo ====================================
echo.
echo 首次编译会自动下载 Android SDK 和 NDK
echo 可能需要 30-60 分钟，请耐心等待...
echo.

buildozer android debug

if errorlevel 1 (
    echo.
    echo ❌ 编译失败！
    echo.
    echo 可能的原因：
    echo 1. JDK 或 Android SDK 未正确配置
    echo 2. 网络连接问题
    echo 3. 权限不足
    echo.
    echo 请查看上面的错误信息进行排查
    echo.
    echo 详细文档请查看：README.md
    pause
    exit /b
)

echo.
echo ====================================
echo    ✅ 编译成功！
echo ====================================
echo.
echo APK 文件位于：bin\ 文件夹中
echo.
echo 通过以下方式安装到手机：
echo 1. 连接手机并开启 USB 调试
echo 2. 运行：buildozer android deploy run
echo 3. 或手动复制 APK 文件到手机安装
echo.
pause
