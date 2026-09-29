@echo off
chcp 65001 >nul
cd /d "%~dp0"
set NAME=PDZ-Download-Remove-Metadata

echo [1/3] Cai thu vien build...
python -m pip install -r requirements-build.txt || goto :err

echo [2/3] Build exe...
python -m PyInstaller --noconfirm --clean --onefile --windowed ^
  --icon assets\pdz.ico --version-file version.txt ^
  --exclude-module numpy --name "%NAME%" image_tool.py || goto :err

echo [3/3] Dong goi zip...
if exist release rmdir /s /q release
mkdir "release\%NAME%"
copy /y "dist\%NAME%.exe" "release\%NAME%\" >nul
copy /y HUONG-DAN-SU-DUNG.txt "release\%NAME%\" >nul
powershell -NoProfile -Command "Compress-Archive -Path 'release\%NAME%' -DestinationPath 'release\%NAME%.zip' -Force" || goto :err

echo.
echo Xong! File zip: %~dp0release\%NAME%.zip
pause
exit /b 0

:err
echo.
echo *** Build loi, xem thong bao phia tren ***
pause
exit /b 1
