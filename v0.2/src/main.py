import os
import sys
import pystray # https://www.geeksforgeeks.org/create-a-responsive-system-tray-icon-using-python-pystray/
import comtypes
import threading
import subprocess
from PIL import Image
from time import sleep
from pycaw.pycaw import AudioUtilities
import json


def left_click(icon, query):
    subprocess.Popen([os.path.join('..','dist','gui.exe'),'--reopen-when-closed'])
    icon.stop()
def right_click(icon, query):
    if str(query) == "Exit":
        icon.stop()

def watcher_thread():
    get_vol = lambda sesh: int(round(sesh.GetMasterVolume() * 100/10)*10)

    # Get all active audio sessionsimport comtypes. what the FUCK does this mean
    try:
        comtypes.CoInitializeEx(comtypes.COINIT_MULTITHREADED)
        all_sessions = AudioUtilities.GetAllSessions()

        sessions = [None] * 4
        value = [None] * 4
        # old_value = [None] * 4

        for session in all_sessions:
            if session.Process:
                if '1' in session.Process.name().lower(): # check for first monitor
                    if 'brightness' in session.Process.name().lower():  # check process name
                        sessions[0] = session.SimpleAudioVolume
                        value[0] = get_vol(sessions[0])
                        # old_value[0] = get_vol(sessions[0])

                    elif 'contrast' in session.Process.name().lower():
                        sessions[1] = session.SimpleAudioVolume
                        value[1] = get_vol(sessions[1])
                        # old_value[1] = get_vol(sessions[1])

                elif '2' in session.Process.name().lower():
                    if 'brightness' in session.Process.name().lower():  # check process name
                        sessions[2] = session.SimpleAudioVolume
                        value[2] = get_vol(sessions[2])
                        # old_value[2] = get_vol(sessions[2])

                    elif 'contrast' in session.Process.name().lower():
                        sessions[3] = session.SimpleAudioVolume
                        value[3] = get_vol(sessions[3])
                        # old_value[3] = get_vol(sessions[3])
        # brightness_mute = brightness_session.GetMute()

        sleeping = True

        sheep = 0 # counting sheep
        SHEEP_MAX = 30 # how long should program count to till it goes back to sleeping

        while True:

            for i, enabled in enumerate(ENABLED_AUDIO_DAEMONS):
                if enabled:                                     # only check enabled daemons
                    temp = get_vol(sessions[i])
                    if temp != value[i]:                            # only update values if temp isnt
                        value[i] = temp
                        sleeping = False                                # value changed so wake up
                        if i == 0  or i == 1:
                            monitor_number = '1'
                        else:
                            monitor_number = '2'
                        if i % 2 == 0:                                  # if is even, then change brightness, else then contrast
                            subprocess.Popen([CMDDC_FILE_REL,monitor_number,'b',str(value[i])])
                        else:
                            subprocess.Popen([CMDDC_FILE_REL,monitor_number,'c',str(value[i])])

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

    except KeyboardInterrupt:
        print("KeyboardInterrupt caught, cleaning up...") #  this will literally never get called so idfk
    finally:
        print('FUCKKKKKKKKKKKKKKKKKKKKK')
        comtypes.CoUninitialize() # i think this is also never getting called everr

try:
    AUDIO_DAEMON_NAMES = ["Monitor 1 - Brightness", "Monitor 1 - Contrast", "Monitor 2 - Brightness", "Monitor 2 - Contrast"]
    CMDDC_FILE_REL = os.path.join('..','click_monitor','ClickMonitorDDC_7_2.exe')

    if getattr(sys, 'frozen', False):  # Running as an executable
        print('Running as EXE')
        # BASE_PATH = os.path.dirname(sys.executable)
        os.chdir(os.path.dirname(sys.executable)) # and idfk
    else:  # Running as a script
        print('Running as script')
        # BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        os.chdir(os.path.dirname(os.path.realpath(__file__))) # because apparently fucking VS Code changes the CWD???? fuck me
    
    try: # load settings
        _ = os.path.join('..', 'assets', 'settings.json')
        with open(_, 'r') as file:
            data = json.load(file)
        
        _m1e = data.get("monitor1", False)
        _m2e = data.get("monitor2", False)

        ENABLED_AUDIO_DAEMONS = [data.get("brightness1", False), data.get("contrast1", False), data.get("brightness2", False), data.get("contrast2", False)]
        
        if _m1e == False: # overwrite bools if that monitor isnt enabled
            ENABLED_AUDIO_DAEMONS[0] = False
            ENABLED_AUDIO_DAEMONS[1] = False
        if _m2e == False:
            ENABLED_AUDIO_DAEMONS[2] = False
            ENABLED_AUDIO_DAEMONS[3] = False

        data.get("sleep_polling_freq", "1")
        data.get("awake_polling_freq", "1")
        data.get("awake_timeout", "1")  
    except FileNotFoundError:
        print(f"No file found at {_}")
    except Exception as e:
        # Handle the error and print the error message
        print(f"An error occurred: {e}")

    print('opening CMDDC')
    subprocess.Popen([CMDDC_FILE_REL])
    
    print("Enabled Daemons List: ", ENABLED_AUDIO_DAEMONS)
    for i, enabled in enumerate(ENABLED_AUDIO_DAEMONS):
        if enabled:
            subprocess.Popen(  os.path.join('..', 'dist',r"{}.exe".format(AUDIO_DAEMON_NAMES[i]))  )
            print('Opened:',r"{}.exe".format(AUDIO_DAEMON_NAMES[i]))

    # Wait for processes to appear on windows sound mixer
    sleep(3)


    Watcher_Thread = threading.Thread(target=watcher_thread, daemon=False)
    Watcher_Thread.start() # do not need to worry about Watcher_Thread.join() because it is a daemeon?
    # pretty sure it will leave comtypes open tho, so like, minor memory leak ig?
    # just don't open and close this alot??? ;)

    # sleep(30)
    with Image.open(os.path.join('..', 'assets', r"brightness_icon.png")) as icon_image:
        brightness_icon = pystray.Icon("PCMixer", icon_image, "PCMixer", menu=pystray.Menu(
            pystray.MenuItem('left click woo',action=left_click,default=True,visible=False),
            pystray.MenuItem("Exit", right_click)))
        brightness_icon.run()

except Exception as e:
    # Handle the error and print the error message
    print(f"An error occurred: {e}")
finally:
    print("exiting...")
    
    os.system( 'taskkill /f /im ClickMonitorDDC_7_2.exe' ) # https://stackoverflow.com/questions/2940858/kill-process-by-name
    
    for name in AUDIO_DAEMON_NAMES:
        os.system( 'taskkill /f /im "{}.exe"'.format(name) )
    
    sys.exit(0)