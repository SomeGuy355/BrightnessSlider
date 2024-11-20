import os
from time import sleep
from pathlib import Path
import vlc
# httpsgithub.comchrismahClickMonitorDDC7.2

# https://stackoverflow.com/questions/59014318/filenotfounderror-could-not-find-module-libvlc-dll
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

# change cwd to this folder to play 1 sec silence to have a volume to be controled
os.chdir(Path(__file__).resolve().parent)
player = vlc.MediaPlayer('1-second-of-silence.mp3')
player.play()

while True:
    player.audio_set_volume(int(input()))
    sleep(0.5)
    print(player.audio_get_volume())
