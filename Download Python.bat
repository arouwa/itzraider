@echo off
color 4F >nul

:: Python'ın kurulu olup olmadığını kontrol et
python --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo Python is already installed. Skipping installation...
) else (
    :: Python'ı indir
    echo Please wait, we are downloading Python...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe

    :: Python'ı yükle (Sessiz Kurulum)
    echo Please wait, we are installing Python...
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    :: Geçici dosyaları sil
    del python-installer.exe
)

:: Pip'in doğru çalıştığını kontrol et
echo Please wait, checking Pip installation...
pip --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    :: Pip kurulu, paketleri yükle
    echo Please wait, we are downloading Packages.
    timeout /t 5 /nobreak >nul
    cls
    echo [-----------] /0/
    echo Please Wait...
    pip install requests >nul
    cls
    echo [***--------] /25/
    echo Please Wait...
    pip install time >nul
    cls
    echo [******-----] /50/
    echo Please Wait...
    pip install random >nul
    cls
    echo [**********] /100/
    echo Please Wait...
    pip install colorama >nul
    Echo wait for start... 
    timeout /t 5 /nobreak >nul
    start Main.py
pause

