from pycaw.pycaw import AudioUtilities
from pycaw.pycaw import AudioSession

sessions = AudioUtilities.GetAllSessions()

print(sessions)
