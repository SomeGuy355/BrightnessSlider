import os
from time import sleep
from pathlib import Path
import threading
import vlc
import pystray # https://www.geeksforgeeks.org/create-a-responsive-system-tray-icon-using-python-pystray/
from PIL import Image
import sys
import subprocess
DIRNAME = os.path.dirname(__file__)

# httpsgithub.comchrismahClickMonitorDDC7.2

# https://stackoverflow.com/questions/59014318/filenotfounderror-could-not-find-module-libvlc-dll
added_directory = os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

# change cwd to this folder
# os.chdir(Path(__file__).resolve().parent)

# play 1 sec silence to have a volume to be controled
player = vlc.MediaPlayer(  os.path.join(DIRNAME,r'resources\1-second-of-silence.mp3')  )
player.play()

image = Image.open(  os.path.join(DIRNAME,r"resources\brightness_icon.png")  )

print("Opening Click Monitor DDC...")
CM_EXE = os.path.join(DIRNAME,r"click_monitor\ClickMonitorDDC_7_2.exe")
subprocess.Popen([CM_EXE])
print("Opened successfully")

def after_click(icon, query):
    if str(query) == "Exit":
        icon.stop()

def main():
    # initalize values
    old_value = player.audio_get_volume()
    sleeping = True
    sleep_count = 0
    sleep_max = 20 # how long should program count to till it goes back to sleeping
    
    while True:
        value = player.audio_get_volume()
        norm_value = (value**3.003003)/(21.6**3.003003) # normalized from log to linear
        rtt_value = int(round(norm_value/10)*10)        # norm_value Rounded To Ten (rtt)

        if old_value != rtt_value:                                      # if volume is changed
            sleeping = False                                            # stop sleeping and
            # https://docs.google.com/spreadsheets/d/1tfnxCc0wor5Oqkimz7PoH9ChBVjHqm-sdeiliasdmQY/edit?gid=0#gid=0
            # equation is given by solving for y in above document
            print('Changing brightness to {}...'.format( rtt_value ))
            subprocess.Popen([CM_EXE,'b',str(rtt_value)])    # change brightness
            print('Changed brightness.')
        else:                                                       # if value has not changed then either
            if sleeping:                                                # sleep for a lot
                sleep(1)
            else:                                                       # or count towards sleep
                sleep(0.1)                                              # and take short break
                sleep_count += 1

        if sleep_count >= sleep_max:                                # if volume hasn't been changed in 'sleep_max' amount of iterations then go back to sleep
            sleeping = True
            sleep_count = 0

        old_value = rtt_value

brightness_icon = pystray.Icon("VolumeBrightness", image, "VolumeBrightness", menu=pystray.Menu(
    pystray.MenuItem("Exit", after_click)))

brightness_thread = threading.Thread(target=main, daemon=True)
print('starting thread...')
brightness_thread.start() # do not need to worry about brightness.join() because it is a daemeon?

print('thread started.\nstarting icon...\n')
brightness_icon.run() # blocking till icon.stop() is called

print("exiting...")
player.release()
added_directory.close()
image.close()
# os.system( 'taskkill /f /im {}'.format(os.path.join(DIRNAME,r"click_monitor\ClickMonitorDDC_7_2.exe")) ) # https://stackoverflow.com/questions/2940858/kill-process-by-name
os.system( 'taskkill /f /im ClickMonitorDDC_7_2.exe' ) # https://stackoverflow.com/questions/2940858/kill-process-by-name
sys.exit(0)
