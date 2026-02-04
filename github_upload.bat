@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ====================================
echo    GitHub 自动化上传脚本
echo ====================================
echo.

REM 检查 Token 文件
if not exist "github_token.txt" (
    echo ❌ Token 文件不存在！
    echo.
    echo 请先创建一个名为 "github_token.txt" 的文本文件
    echo 把你的 GitHub Token 粘贴进去
    echo.
    pause
    exit /b
)

REM 读取 Token
set /p GITHUB_TOKEN=<github_token.txt
set "GITHUB_TOKEN=%GITHUB_TOKEN: =%"

echo ✅ Token 已读取
echo.

REM 输入你的 GitHub 用户名
set /p GITHUB_USERNAME=请输入你的 GitHub 用户名:

if "%GITHUB_USERNAME%"=="" (
    echo ❌ 用户名不能为空！
    pause
    exit /b
)

echo ✅ 用户名: %GITHUB_USERNAME%
echo.

REM 输入仓库名称（默认 ConstructionFineApp）
set /p REPO_NAME=请输入仓库名称（直接回车使用默认:）:
if "%REPO_NAME%"=="" set REPO_NAME=ConstructionFineApp

echo ✅ 仓库名: %REPO_NAME%
echo.

REM 项目文件路径
set "PROJECT_PATH=%~dp0"

echo ✅ 项目路径: %PROJECT_PATH%
echo.

REM 检查 curl 是否可用
where curl >nul 2>&1
if errorlevel 1 (
    echo ❌ curl 命令不可用！
    echo.
    echo 这个脚本需要 curl 命令。
    echo 如果是 Windows 10/11，curl 应该已经安装。
    echo 如果是 Windows 7，需要手动安装 curl。
    echo.
    pause
    exit /b
)

echo ✅ curl 命令可用
echo.

echo ====================================
echo    开始上传到 GitHub
echo ====================================
echo.

REM 第1步：创建仓库
echo [1/4] 创建仓库...
curl -X POST "https://api.github.com/user/repos" ^
  -H "Authorization: token %GITHUB_TOKEN%" ^
  -H "Accept: application/vnd.github.v3+json" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"%REPO_NAME%\",\"description\":\"施工现场罚款系统 - 安卓APP\",\"private\":false,\"auto_init\":false}" ^
  >nul 2>&1

if errorlevel 1 (
    echo ❌ 创建仓库失败，但可能已存在，继续...
) else (
    echo ✅ 仓库创建成功（或已存在）
)

echo.

REM 第2步：上传文件
echo [2/4] 上传文件...
echo.

set count=0

REM 遍历项目文件夹并上传所有文件
for /r "%PROJECT_PATH%" %%F in (*) do (
    set "filepath=%%F"
    
    REM 跳过 Token 文件和脚本本身
    if "%%~nxF"=="github_token.txt" goto :skip
    if "%%~nxF"=="github_upload.bat" goto :skip
    if "%%~nxF"=="自动化上传脚本.py" goto :skip
    if "%%~nxF"=="快速开始.md" goto :skip
    if "%%~nxF"=="上传文件到GitHub-超详细步骤.md" goto :skip
    if "%%~nxF"=="创建build.yml文件-超详细步骤.md" goto :skip
    if "%%~nxF"=="最简单的APK获取方式.md" goto :skip
    if "%%~nxF"=="内网穿透使用指南.md" goto :skip
    if "%%~nxF"=="手机APP安装指南.md" goto :skip
    if "%%~nxF"=="README-Web版本.md" goto :skip
    
    REM 计算相对路径
    set "relpath=!filepath:%PROJECT_PATH%=!"
    
    REM 转换为 Unix 路径（GitHub API 需要）
    set "ghpath=!relpath:\=\/!"
    
    REM Base64 编码文件内容
    echo 上传: !ghpath!
    
    REM 使用临时脚本进行 Base64 编码
    powershell -Command "[Convert]::ToBase64String([IO.File]::ReadAll('!filepath!'))" >temp64.txt
    set /p BASE64=<temp64.txt
    del temp64.txt
    
    REM 构造 JSON
    set JSON={\"message\":\"Upload !ghpath!\",\"content\":\"!BASE64!\"}
    
    REM 上传文件
    curl -X PUT "https://api.github.com/repos/%GITHUB_USERNAME%/%REPO_NAME%/contents/!ghpath!" ^
      -H "Authorization: token %GITHUB_TOKEN%" ^
      -H "Accept: application/vnd.github.v3+json" ^
      -H "Content-Type: application/json" ^
      -d "!JSON!" ^
      >nul 2>&1
    
    if errorlevel 1 (
        echo   ❌ 上传失败: !ghpath!
    ) else (
        echo   ✅ 上传成功: !ghpath!
        set /a count+=1
    )
    
    :skip
)

echo.
echo ====================================
echo    上传完成
echo ====================================
echo.
echo 📊 上传了 %count% 个文件
echo.

REM 第3步：检查关键文件
echo [3/4] 检查关键文件...
echo.

REM 检查 .github/workflows/build.yml 文件是否存在
curl -s -H "Authorization: token %GITHUB_TOKEN%" ^
  "https://api.github.com/repos/%GITHUB_USERNAME%/%REPO_NAME%/contents/.github/workflows/build.yml" ^
  >nul 2>&1

if errorlevel 0 (
    echo ✅ .github/workflows/build.yml 文件已上传（重要！）
) else (
    echo ⚠️  .github/workflows/build.yml 文件未找到！
    echo.
    echo 这个文件非常重要，没有它 GitHub Actions 不会自动编译。
    echo.
    echo 请手动在 GitHub 网页上创建这个文件：
    echo 1. 访问: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%/new/.github/workflows
    echo 2. 文件名输入: .github/workflows/build.yml
    echo 3. 粘贴我之前发送的 build.yml 代码
    echo 4. 点击提交
)

echo.

REM 第4步：等待编译
echo [4/4] 后续步骤...
echo.
echo ✅ 文件已上传！接下来的步骤：
echo.
echo 1. 访问你的仓库: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo 2. 点击顶部的 "Actions" 标签
echo 3. 等待 3-5 分钟自动编译
echo 4. 编译完成后下载 APK
echo.
echo ====================================
echo    完成！
echo ====================================
echo.

pause
