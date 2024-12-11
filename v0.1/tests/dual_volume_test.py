import os
# import threading
# import vlc
import pystray # https://www.geeksforgeeks.org/create-a-responsive-system-tray-icon-using-python-pystray/
from sys import exit
import subprocess

from time import sleep
# from pathlib import Path
from multiprocessing import Process
from PIL import Image

# import setproctitle



def sound_thread(target=None):
    CM_EXE = os.path.join(os.path.dirname(__file__),r"click_monitor\ClickMonitorDDC_7_2.exe")
    if target == 'brightness':
        CM_ARG = 'b'
    elif target == 'contrast':
        CM_ARG = 'c'
    else: print('how')

    # initalize values
    old_value = 0
    sleeping = True
    sheep = 0 # counting sheep
    SHEEP_MAX = 30 # how long should program count to till it goes back to sleeping
    
    while True:
        volume = (player.audio_get_volume()**3.003003)/(21.6**3.003003) # normalized from log (dB?) to linear
        rounded_volume = int(round(volume/10)*10)        # norm_value Rounded To Ten (rtt)

        if old_value != rounded_volume:                                      # if volume is changed
            sleeping = False                                            # stop sleeping and
            # https://docs.google.com/spreadsheets/d/1tfnxCc0wor5Oqkimz7PoH9ChBVjHqm-sdeiliasdmQY/edit?gid=0#gid=0
            # equation is given by solving for y in above document
            print('Changing {} to {}...'.format(target,rounded_volume))
            subprocess.Popen([CM_EXE,CM_ARG,str(rounded_volume)])    # change brightness
            print('Changed {}.'.format(target))
        else:                                                       # if value has not changed then either
            if sleeping:                                                # if sleeping, then sleep
                sleep(1)
            else:
                sleep(0.1)                                              # else, take short break
                sheep += 1                                              # count sheep

        if sheep >= SHEEP_MAX:                                # if volume hasn't been changed in 'SHEEP_MAX' amount of iterations then go back to sleep
            sleeping = True
            sheep = 0

        old_value = rounded_volume

def after_click(icon, query):
    if str(query) == "Exit":
        icon.stop()

if __name__ == '__main__':
    DIRNAME = os.path.dirname(__file__)
    BRIGHTNESS_IMAGE = Image.open(  os.path.join(DIRNAME,r"resources\brightness_icon.png")  )
    added_directory = os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC') # https://stackoverflow.com/questions/59014318/filenotfounderror-could-not-find-module-libvlc-dll

    print("Opening Click Monitor DDC...")
    CM_EXE = os.path.join(DIRNAME,r"click_monitor\ClickMonitorDDC_7_2.exe")
    subprocess.Popen([CM_EXE])
    print("Opened successfully")

    brightness = Process(target=sound_thread, args=('brightness',))
    brightness.start()
    print(brightness.name)

    contrast = Process(target=sound_thread, args=('contrast',))
    contrast.start()

    # brightness_icon = pystray.Icon("VolumeBrightness", image, "VolumeBrightness", menu=pystray.Menu(
    #     pystray.MenuItem("Exit", after_click)))

    # print('thread started.\nstarting icon...\n')
    # brightness_icon.run() # blocking till icon.stop() is called

    # print("exiting...")
    # player.release()
    # added_directory.close()
    # image.close()
    # # os.system( 'taskkill /f /im {}'.format(os.path.join(DIRNAME,r"click_monitor\ClickMonitorDDC_7_2.exe")) ) # https://stackoverflow.com/questions/2940858/kill-process-by-name
    # os.system( 'taskkill /f /im ClickMonitorDDC_7_2.exe' ) # https://stackoverflow.com/questions/2940858/kill-process-by-name
    # sys.exit(0)