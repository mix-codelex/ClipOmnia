@echo off
echo ================================================
echo   Building PySide6 App + Creating Installer
echo ================================================
echo.

echo.
echo ================================================
echo   Running PyInstaller
echo ================================================
echo.
REM --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32"
pyinstaller --onefile --windowed ^
    --icon=src\assets\icon.ico ^
    --add-data "src\assets;src\assets" ^
    main.py

IF %ERRORLEVEL% NEQ 0 (
    echo PyInstaller build failed!
    pause
    exit /b 1
)

echo.
echo PyInstaller build completed!
echo EXE created at: dist\main.exe
echo.

REM ------------------------------------------------
REM 2. Run Inno Setup Compiler
REM ------------------------------------------------
echo ================================================
echo   Building Windows Installer (Inno Setup)
echo ================================================
echo.

REM 💡 CHANGE THIS to your InnoSetup installation path
SET ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

%ISCC% setup.iss

IF %ERRORLEVEL% NEQ 0 (
    echo Inno Setup build failed!
    pause
    exit /b 1
)

echo.
echo ================================================
echo   Installer successfully created!
echo   Check folder: dist_installer\
echo ================================================
pause
