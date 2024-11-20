import os
import sys
import pystray # https://www.geeksforgeeks.org/create-a-responsive-system-tray-icon-using-python-pystray/
import comtypes
import threading
import subprocess
from PIL import Image
from time import sleep
from pycaw.pycaw import AudioUtilities


if getattr(sys, 'frozen', False):  # Running as an executable
    BASE_PATH = os.path.dirname(sys.executable)
else:  # Running as a script
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def after_click(icon, query):
    if str(query) == "Exit":
        icon.stop()

def watcher_thread():
    CM_EXE = os.path.join(BASE_PATH,r"click_monitor\ClickMonitorDDC_7_2.exe")
    # Get all active audio sessionsimport comtypes
    try:
        comtypes.CoInitializeEx(comtypes.COINIT_MULTITHREADED)
        sessions = AudioUtilities.GetAllSessions()
        

        for session in sessions:
            if session.Process:
                volume = session.SimpleAudioVolume  # Use SimpleAudioVolume for session volume control
                if 'brightness' in session.Process.name().lower():  # check process name
                    brightness_session = session
                    brightness_mute = volume.GetMute()

                elif 'contrast' in session.Process.name().lower():
                    brightness_session = session


        old_brightness = 0
        old_contrast = 0
        brightness_mute = False

        sleeping = True

        sheep = 0 # counting sheep
        SHEEP_MAX = 30 # how long should program count to till it goes back to sleeping

        while True:
            # retrive and set brightness and contrast values
            for session in sessions:
                if session.Process:
                    volume = session.SimpleAudioVolume  # Use SimpleAudioVolume for session volume control
                    if 'brightness' in session.Process.name().lower():  # check process name
                        brightness = volume.GetMasterVolume() * 100     # Volume in percentage
                        brightness = int(round(brightness/10)*10)       # round it to 10
                        
                        if volume.GetMute() != brightness_mute:
                            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                            brightness_mute = brightness_mute
                    elif 'contrast' in session.Process.name().lower():
                        contrast = volume.GetMasterVolume() * 100
                        contrast = int(round(contrast/10)*10)

            # set brightness/contrast with CM_DDC or sleep
            if brightness != old_brightness and contrast != old_contrast:                                      # if volume is changed
                sleeping = False
                subprocess.Popen([CM_EXE,'b',str(brightness), 'c', str(contrast)])

            elif brightness != old_brightness:
                sleeping = False
                subprocess.Popen([CM_EXE,'b',str(brightness)])

            elif contrast != old_contrast:
                sleeping = False
                subprocess.Popen([CM_EXE,'c',str(contrast)])

            else:                                                       # if value has not changed then either
                if sleeping:                                                # if sleeping, then sleep
                    sleep(1)
                else:
                    sleep(0.1)                                              # else, take short break
                    sheep += 1                                              # count sheep

            # go to sleep if sheep reached SHEEP_MAX
            if sheep >= SHEEP_MAX:                                # if volume hasn't been changed in 'SHEEP_MAX' amount of iterations then go back to sleep
                sleeping = True
                sheep = 0

            old_brightness = brightness
            old_contrast = contrast
    except KeyboardInterrupt:
        print("KeyboardInterrupt caught, cleaning up...")
    finally:
        comtypes.CoUninitialize()

try:
    CM_EXE = os.path.join(BASE_PATH,r"click_monitor\ClickMonitorDDC_7_2.exe")

    print('opening cdexe')
    subprocess.Popen([CM_EXE])
    print('opening\nopening brightness')
    subprocess.Popen(  os.path.join(BASE_PATH,r"brightness.exe")  )
    print('opened\nopeningcontrast')
    subprocess.Popen(  os.path.join(BASE_PATH,r"contrast.exe")  )

    # Wait for processes to appear on windows mixer
    sleep(3)

    ICON_FILE = Image.open(  os.path.join(BASE_PATH,r"brightness_icon.png")  )

    brightness_icon = pystray.Icon("PCMixer", ICON_FILE, "PCMixer", menu=pystray.Menu(
        pystray.MenuItem("Exit", after_click)))

    Watcher_Thread = threading.Thread(target=watcher_thread, daemon=False)
    print('starting thread...')
    Watcher_Thread.start() # do not need to worry about brightness.join() because it is a daemeon?
    # pretty sure it will leave comtypes open tho, so like, minor memory leak ig?

    print('thread started.\nstarting icon...\n')
    brightness_icon.run() # blocking till icon.stop() is called

finally:
    print("exiting...")
    ICON_FILE.close()
    os.system( 'taskkill /f /im ClickMonitorDDC_7_2.exe' ) # https://stackoverflow.com/questions/2940858/kill-process-by-name
    os.system( 'taskkill /f /im brightness.exe' ) # https://stackoverflow.com/questions/2940858/kill-process-by-name
    os.system( 'taskkill /f /im contrast.exe' ) # https://stackoverflow.com/questions/2940858/kill-process-by-name
    sys.exit(0)