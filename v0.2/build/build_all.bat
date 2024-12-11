:: thank you chatGPT for like... all of this .bat file btw
echo off

:: Change directory to the main folder
cd /d "%~dp0\.."

:: Run PyInstaller to create an EXE (using relative path to the Python script)
pyinstaller --onefile --noconfirm --clean --windowed --distpath "dist" "src\main.py"
pyinstaller --onefile --noconfirm --clean --windowed --distpath "dist" "src\gui.py"
pyinstaller --onefile --noconfirm --clean --windowed --distpath "dist" --name "Monitor 1 - Brightness" "src\general_audio_daemon.py"
pyinstaller --onefile --noconfirm --clean --windowed --distpath "dist" --name "Monitor 1 - Contrast"   "src\general_audio_daemon.py"
pyinstaller --onefile --noconfirm --clean --windowed --distpath "dist" --name "Monitor 2 - Brightness" "src\general_audio_daemon.py"
pyinstaller --onefile --noconfirm --clean --windowed --distpath "dist" --name "Monitor 2 - Contrast"   "src\general_audio_daemon.py"

:: Remove .spec files after build
del /q "main.spec"
del /q "gui.spec"
del /q "Monitor 1 - Brightness.spec"
del /q "Monitor 1 - Contrast.spec"
del /q "Monitor 2 - Brightness.spec"
del /q "Monitor 2 - Contrast.spec"

@REM :: Remove the folders in build folder after build
rd /s /q "build\main"        
rd /s /q "build\gui"
rd /s /q "build\Monitor 1 - Brightness"
rd /s /q "build\Monitor 1 - Contrast"
rd /s /q "build\Monitor 2 - Brightness"
rd /s /q "build\Monitor 2 - Contrast"

:: Inform the user that the files are ready
echo Done...
pause
