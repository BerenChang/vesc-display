import os
import sys

from PyQt5.QtWidgets import QApplication
import data_updater
from gui import GUIApp as GUIApp
from gui_lite import GUIApp as GUIAppLite
from utils import GUIAppComm, get_script_dir
from config import Config

log = None
if len(sys.argv) > 1:
    if not os.path.isfile(sys.argv[1]):
        print("argv[1] not file, launching in normal mode")
        input()
        exit(1)
    else:
        log = sys.argv[1]

if not os.path.isdir(get_script_dir(False) + "/configs"):
    os.mkdir(get_script_dir(False) + "/configs")
if not os.path.isdir(get_script_dir(False) + "/logs"):
    os.mkdir(get_script_dir(False) + "/logs")
print("loading config ... ", end='')
try:
    Config.load()
    print("ok, launching ui")
except:
    print("fault!")
    input()
    exit(1)

app = QApplication([])
ui = GUIAppLite()

comm = GUIAppComm()
comm.setCallback(ui.callback_update_gui)
thread = data_updater.WorkerThread(comm.push_data)
thread.name = "data_updater"
thread.play_log_path = log
thread.start()
ui.data_updater_thread = thread
ui.show()
thread.stopped_flag = True

app.exit(0)
exit(0)

