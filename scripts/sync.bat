@echo off

echo.
echo ==========================================
echo 博客文章同步和格式化工具
echo ==========================================
echo.
echo 选择操作:
echo 1. 格式化现有文件
echo 2. 从Obsidian同步新文件
echo 3. 执行完整流程
echo 4. 预览模式 - 格式化现有文件
echo 5. 预览模式 - 从Obsidian同步
echo 6. 预览模式 - 完整流程
echo 0. 退出
echo.
set /p choice=请输入选项 (0-6):

if "%choice%"=="1" goto format
if "%choice%"=="2" goto sync
if "%choice%"=="3" goto all
if "%choice%"=="4" goto format_dry
if "%choice%"=="5" goto sync_dry
if "%choice%"=="6" goto all_dry
if "%choice%"=="0" goto exit
goto invalid

:format
echo.
echo 正在格式化现有文件...
python scripts\blog_sync.py --format
goto end

:sync
echo.
echo 正在从Obsidian同步文件...
python scripts\blog_sync.py --sync
goto end

:all
echo.
echo 正在执行完整流程...
python scripts\blog_sync.py --all
goto end

:format_dry
echo.
echo 预览模式 - 格式化现有文件...
python scripts\blog_sync.py --format --dry-run
goto end

:sync_dry
echo.
echo 预览模式 - 从Obsidian同步...
python scripts\blog_sync.py --sync --dry-run
goto end

:all_dry
echo.
echo 预览模式 - 完整流程...
python scripts\blog_sync.py --all --dry-run
goto end

:invalid
echo.
echo 无效选项，请重新选择
echo.
goto start

:end
echo.
echo  操作完成！
echo  如果文件已更新，记得运行以下命令提交更改:
echo    git add .
echo    git commit -m "同步文章更新"
echo    git push origin main
echo.
pause
:exit