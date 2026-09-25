@echo off
chcp 65001 >nul
title Kemer Yat Turu - Yerel Onizleme (localhost:8000)
cd /d "%~dp0"

echo ==========================================================
echo    KEMER YAT TURU - Yerel onizleme sunucusu
echo.
echo    Adres    : http://localhost:8000
echo    Klasor   : %cd%
echo    Durdurma : Bu pencerede Ctrl + C , sonra E
echo               (veya pencereyi kapatin)
echo ==========================================================
echo.

rem 2 saniye sonra varsayilan tarayiciyi otomatik acar
start "" /b cmd /c "timeout /t 2 >nul & start http://localhost:8000/"

py -m http.server 8000
if errorlevel 1 python -m http.server 8000

echo.
echo Sunucu durduruldu.
pause
