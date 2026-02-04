@echo off
chcp 65001 >nul
echo ====================================
echo    最简单的获取 APK 方式
echo ====================================
echo.
echo 由于编译APK需要复杂的环境配置，
echo 我推荐以下几种方式：
echo.
echo 方式一：使用在线编译服务（最简单）
echo  1. 访问：https://ci.kivy.org/
echo  2. 上传你的代码文件
echo  3. 自动编译并下载 APK
echo.
echo 方式二：使用 GitHub Actions（推荐）
echo  1. 注册 GitHub 账号（免费）
echo  2. 创建新仓库
echo  3. 上传文件
echo  4. 自动编译下载 APK
echo  5. 详见：https://docs.kivy.org/en/stable/guide/packaging-android.html
echo.
echo 方式三：本地编译（复杂）
echo  需要安装：Python、JDK、Android SDK、Android NDK
echo  首次编译需要 30-60 分钟
echo.
echo ====================================
echo   推荐方式：GitHub Actions
echo ====================================
echo.
echo 我可以帮你准备 GitHub Actions 配置文件，
echo 你只需要：
echo 1. 注册 GitHub 账号
echo 2. 创建仓库
echo 3. 上传文件
echo 4. 自动获取 APK
echo.
echo 需要我帮你准备吗？(输入 Y/N)
set /p choice=

if /i "%choice%"=="Y" (
    echo.
    echo 好的，正在准备 GitHub Actions 配置...
    echo.
    timeout /t 2 >nul
    call setup_github_actions.bat
) else if /i "%choice%"=="N" (
    echo.
    echo 好的，你可以使用其他方式获取 APK。
    echo.
) else (
    echo.
    echo 无效的选择，请重新运行。
    echo.
)

pause
