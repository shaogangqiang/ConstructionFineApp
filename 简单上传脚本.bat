@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ====================================
echo    GitHub 上传脚本（简化版）
echo ====================================
echo.

cd /d "%~dp0"

REM 检查 Token 文件
if not exist "github_token.txt" (
    echo.
    echo ❌ Token 文件不存在！
    echo.
    echo 请先创建一个名为 "github_token.txt" 的文本文件
    echo 把你的 GitHub Token 粘贴进去
    echo.
    echo 文件必须和脚本在同一个目录下！
    echo.
    pause
    exit /b
)

echo [1/3] 检查文件...
echo.

REM 检查 Token 文件
if not exist "github_token.txt" (
    echo ❌ Token 文件不存在！
    pause
    exit /b
)
echo ✅ Token 文件存在

REM 检查项目文件夹
if not exist "main.py" (
    echo ❌ 项目文件夹不对！
    echo.
    echo 脚本必须和项目文件在同一个目录下
    echo.
    pause
    exit /b
)
echo ✅ 项目文件存在

echo.
echo [2/3] 检查 GitHub 用户名...
echo.

set /p GITHUB_USERNAME=请输入你的 GitHub 用户名（不要带空格）:

if "%GITHUB_USERNAME%"=="" (
    echo ❌ 用户名不能为空！
    pause
    exit /b
)

echo ✅ 用户名: %GITHUB_USERNAME%

echo.
echo [3/3] 上传文件到 GitHub...
echo.

REM 使用 curl 上传文件
where curl >nul 2>&1
if errorlevel 1 (
    echo.
    echo ====================================
    echo ⚠️ curl 命令不可用！
    echo ====================================
    echo.
    echo 你的电脑可能没有安装 curl。
    echo.
    echo 解决方案：
    echo 1. 如果是 Windows 10/11，curl 应该已经安装
    echo 2. 如果是 Windows 7，需要手动安装
    echo 3. 或者使用 GitHub 网页手动上传
    echo.
    echo 手动上传步骤：
    echo ====================================
    echo 1. 打开浏览器，访问：https://github.com/%GITHUB_USERNAME%/new
    echo 2. 仓库名输入：ConstructionFineApp
    echo 3. 点击 "Create repository"
    echo 4. 点击 "uploading an existing file" 或 "Add file"
    echo 5. 把这个目录下的所有文件拖进去上传
    echo 6. 确保上传了 .github/workflows/build.yml 文件
    echo 7. 提交文件
    echo 8. 点击 "Actions" 等待编译
    echo ====================================
    echo.
    pause
    exit /b
)

echo ✅ curl 命令可用

echo.
echo 创建仓库...
curl -s -H "Authorization: token %GITHUB_TOKEN%" -H "Accept: application/vnd.github.v3+json" "https://api.github.com/user/repos" -d "{\"name\":\"ConstructionFineApp\",\"description\":\"施工现场罚款系统\",\"private\":false}" >nul 2>&1

echo.
echo 上传文件...
echo.

set /a count=0

REM 上传 main.py
if exist "main.py" (
    echo 上传 main.py...
    powershell -Command "[Convert]::ToBase64String([IO.File]::ReadAll('main.py'))" > temp64.txt
    set /p BASE64=<temp64.txt
    curl -s -X PUT -H "Authorization: token %GITHUB_TOKEN%" -H "Content-Type: application/json" -d "{\"message\":\"Upload main.py\",\"content\":\"%BASE64%\"}" "https://api.github.com/repos/%GITHUB_USERNAME%/ConstructionFineApp/contents/main.py" >nul 2>&1
    del temp64.txt
    set /a count+=1
)

REM 上传 buildozer.spec
if exist "buildozer.spec" (
    echo 上传 buildozer.spec...
    powershell -Command "[Convert]::ToBase64String([IO.File]::ReadAll('buildozer.spec'))" > temp64.txt
    set /p BASE64=<temp64.txt
    curl -s -X PUT -H "Authorization: token %GITHUB_TOKEN%" -H "Content-Type: application/json" -d "{\"message\":\"Upload buildozer.spec\",\"content\":\"%BASE64%\"}" "https://api.github.com/repos/%GITHUB_USERNAME%/ConstructionFineApp/contents/buildozer.spec" >nul 2>&1
    del temp64.txt
    set /a count+=1
)

REM 上传 requirements.txt
if exist "requirements.txt" (
    echo 上传 requirements.txt...
    powershell -Command "[Convert]::ToBase64String([IO.File]::ReadAll('requirements.txt'))" > temp64.txt
    set /p BASE64=<temp64.txt
    curl -s -X PUT -H "Authorization: token %GITHUB_TOKEN%" -H "Content-Type: application/json" -d "{\"message\":\"Upload requirements.txt\",\"content\":\"%BASE64%\"}" "https://api.github.com/repos/%GITHUB_USERNAME%/ConstructionFineApp/contents/requirements.txt" >nul 2>&1
    del temp64.txt
    set /a count+=1
)

REM 上传 README.md
if exist "README.md" (
    echo 上传 README.md...
    powershell -Command "[Convert]::ToBase64String([IO.File]::ReadAll('README.md'))" > temp64.txt
    set /p BASE64=<temp64.txt
    curl -s -X PUT -H "Authorization: token %GITHUB_TOKEN%" -H "Content-Type: application/json" -d "{\"message\":\"Upload README.md\",\"content\":\"%BASE64%\"}" "https://api.github.com/repos/%GITHUB_USERNAME%/ConstructionFineApp/contents/README.md" >nul 2>&1
    del temp64.txt
    set /a count+=1
)

REM 检查并上传 .github/workflows/build.yml
if exist ".github\workflows\build.yml" (
    echo.
    echo ====================================
    echo ⚠️ 重要！上传 GitHub Actions 配置文件
    echo ====================================
    echo.
    echo 正在上传 .github/workflows/build.yml...
    powershell -Command "[Convert]::ToBase64String([IO.File]::ReadAll('.github\workflows\build.yml'))" > temp64.txt
    set /p BASE64=<temp64.txt
    curl -s -X PUT -H "Authorization: token %GITHUB_TOKEN%" -H "Content-Type: application/json" -d "{\"message\":\"Upload build.yml\",\"content\":\"%BASE64%\"}" "https://api.github.com/repos/%GITHUB_USERNAME%/ConstructionFineApp/contents/.github/workflows/build.yml" >nul 2>&1
    del temp64.txt
    set /a count+=1
    echo ✅ GitHub Actions 配置文件已上传！
    echo.
) else (
    echo.
    echo ====================================
    echo ⚠️ 警告：.github\workflows\build.yml 文件不存在！
    echo ====================================
    echo.
    echo 这个文件非常重要！没有它 GitHub Actions 不会自动编译。
    echo.
    echo 你需要手动在 GitHub 网页上创建这个文件：
    echo 1. 访问：https://github.com/%GITHUB_USERNAME%/ConstructionFineApp/new/.github/workflows
    echo 2. 文件名输入：.github/workflows/build.yml
    echo 3. 粘贴 build.yml 代码并提交
    echo.
)

echo.
echo ====================================
echo    上传完成
echo ====================================
echo.
echo 📊 上传了 %count% 个文件
echo.
echo ====================================
echo    接下来的步骤
echo ====================================
echo.
echo 1. 访问你的仓库：
echo    https://github.com/%GITHUB_USERNAME%/ConstructionFineApp
echo.
echo 2. 点击顶部的 "Actions" 标签
echo.
echo 3. 等待 3-5 分钟，你会看到一个名为 "Build Android APK" 的 workflow
echo.
echo 4. 等待状态从黄色变成绿色
echo.
echo 5. 点击进入这个 workflow
echo.
echo 6. 滚动到页面底部，找到 "Artifacts" 部分
echo.
echo 7. 展开 "fineapp-apk"
echo.
echo 8. 下载 APK 文件
echo.
echo 9. 把 APK 传输到手机并安装
echo.
echo ====================================
echo.

pause
