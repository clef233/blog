@echo off

echo.
echo ==========================================
echo ��������ͬ���͸�ʽ������
echo ==========================================
echo.
echo ѡ�����:
echo 1. ��ʽ�������ļ�
echo 2. ��Obsidianͬ�����ļ�
echo 3. ִ����������
echo 4. Ԥ��ģʽ - ��ʽ�������ļ�
echo 5. Ԥ��ģʽ - ��Obsidianͬ��
echo 6. Ԥ��ģʽ - ��������
echo 0. �˳�
echo.
set /p choice=������ѡ�� (0-6):

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
echo ���ڸ�ʽ�������ļ�...
python scripts\blog_sync.py --format
goto end

:sync
echo.
echo ���ڴ�Obsidianͬ���ļ�...
python scripts\blog_sync.py --sync
goto end

:all
echo.
echo ����ִ����������...
python scripts\blog_sync.py --all
goto end

:format_dry
echo.
echo Ԥ��ģʽ - ��ʽ�������ļ�...
python scripts\blog_sync.py --format --dry-run
goto end

:sync_dry
echo.
echo Ԥ��ģʽ - ��Obsidianͬ��...
python scripts\blog_sync.py --sync --dry-run
goto end

:all_dry
echo.
echo Ԥ��ģʽ - ��������...
python scripts\blog_sync.py --all --dry-run
goto end

:invalid
echo.
echo ��Чѡ�������ѡ��
echo.
goto start

:end
echo.
echo  ������ɣ�
echo  ����ļ��Ѹ��£��ǵ��������������ύ����:
echo    git add .
echo    git commit -m "ͬ�����¸���"
echo    git push origin main
echo.
pause
:exit