import os
from pycaw.pycaw import AudioUtilities #, IAudioEndpointVolume
# from comtypes import CLSCTX_ALL
import subprocess
from time import sleep
import sys

if getattr(sys, 'frozen', False):  # Running as an executable
    BASE_PATH = os.path.dirname(sys.executable)
else:  # Running as a script
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

print('trying to set cmddc')
print(__file__)
CM_EXE = os.path.join(BASE_PATH,r"click_monitor\ClickMonitorDDC_7_2.exe")
print(CM_EXE)

print('opening cdexe')
subprocess.run([CM_EXE])
print('opening\nopening brightness')
subprocess.Popen(  os.path.join(BASE_PATH,r"resources\brightness.exe")  )
print('opened\nopeningcontrast')
subprocess.Popen(  os.path.join(BASE_PATH,r"resources\contrast.exe")  )
print(os.path.dirname(__file__))

sleep(3)

# Get all active audio sessions
sessions = AudioUtilities.GetAllSessions()
brightness = 0
contrast = 0
old_brightness = 0
old_contrast = 0
sleeping = True
sheep = 0 # counting sheep
SHEEP_MAX = 30 # how long should program count to till it goes back to sleeping

def watcher_thread():
    while True:
        # retrive and set brightness and contrast values
        for session in sessions:
            if session.Process:
                volume = session.SimpleAudioVolume  # Use SimpleAudioVolume for session volume control
                if 'brightness' in session.Process.name().lower():  # check process name
                    brightness = volume.GetMasterVolume() * 100     # Volume in percentage
                    brightness = int(round(brightness/10)*10)       # round it to 10
                elif 'contrast' in session.Process.name().lower():
                    contrast = volume.GetMasterVolume() * 100
                    contrast = int(round(contrast/10)*10)

        # set brightness/contrast with CM_DDC or sleep
        if brightness != old_brightness and contrast != old_contrast:                                      # if volume is changed
            sleeping = False
            # subprocess.Popen([CM_EXE,'b',str(brightness), 'c', str(contrast)])

        elif brightness != old_brightness:
            sleeping = False
            # subprocess.Popen([CM_EXE,'b',str(brightness)])

        elif contrast != old_contrast:
            sleeping = False
            # subprocess.Popen([CM_EXE,'c',str(contrast)])

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


print("exiting...")
player.release()
added_directory.close()
image.close()
# os.system( 'taskkill /f /im {}'.format(os.path.join(DIRNAME,r"click_monitor\ClickMonitorDDC_7_2.exe")) ) # https://stackoverflow.com/questions/2940858/kill-process-by-name
os.system( 'taskkill /f /im ClickMonitorDDC_7_2.exe' ) # https://stackoverflow.com/questions/2940858/kill-process-by-name
sys.exit(0)