import os
import eel
from engine.command import*
eel.init("www")
os.system('start chrome --new-window --app=http://localhost:8000/index.html')
eel.start('index.html', mode=None, host='localhost', port=8000, block=True)