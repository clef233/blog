@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 启动博客管理后台...
echo 访问 http://localhost:5000
python app.py