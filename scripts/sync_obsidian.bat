@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ====================================
echo Obsidian 到 Hugo 同步工具
echo ====================================
echo.

:: 设置默认路径 - 请根据实际情况修改
set "OBSIDIAN_VAULT=D:\iCloud\DATA\iCloudDrive\iCloud~md~obsidian\下水道\阅读笔记\扩展阅读"
set "HUGO_CONTENT=D:\Projects\blog\content"
set "AUTHOR=clef233"

:: 检查 Python 是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python
    pause
    exit /b 1
)

:: 检查脚本文件是否存在
if not exist "%~dp0obsidian_sync.py" (
    echo 错误: 未找到 obsidian_sync.py 脚本文件
    echo 请确保脚本文件在当前目录
    pause
    exit /b 1
)

:: 显示当前配置
echo 当前配置:
echo   Obsidian 路径: %OBSIDIAN_VAULT%
echo   Hugo 内容路径: %HUGO_CONTENT%
echo   作者: %AUTHOR%
echo.

:: 询问用户确认
set /p confirm="配置是否正确? (Y/N): "
if /i not "!confirm!"=="Y" (
    echo.
    echo 请修改脚本中的路径配置
    echo 脚本位置: %~dp0sync_obsidian.bat
    pause
    exit /b 0
)

echo.
echo 开始同步...
echo.

:: 运行同步脚本
python "%~dp0obsidian_sync.py" ^
    --obsidian-vault "%OBSIDIAN_VAULT%" ^
    --hugo-content "%HUGO_CONTENT%" ^
    --author "%AUTHOR%" ^
    --log-level INFO

if errorlevel 1 (
    echo.
    echo 同步过程中出现错误，请检查日志文件 obsidian_sync.log
    pause
    exit /b 1
)

echo.
echo 同步完成!
echo.
echo 接下来你可以:
echo 1. 检查生成的文章文件
echo 2. 运行 Hugo 本地服务器: hugo server -D
echo 3. 提交更改到 Git
echo.

pause