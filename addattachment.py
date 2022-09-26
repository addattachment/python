"""
entry file for the addattachment project
In this file, we'll:
1. have a GUI for entering player name?
2. setup of directory structure
3. three different processes for capturing data:
    - open the websocket towards unity
    - start capturing the EEG datastream + insert markers based on LSL markers
    - capture OSC messages of Emotibit Oscilloscope

We'll try to make an executable of this project using PyInstaller
"""
from datetime import datetime

from pathlib import Path

from utils.GUI import GUI
from utils.utils import *


class PlayerSession:
    def __init__(self, name, playtime):
        self.name = name
        self.playtime = playtime
        self.gsr_dir = None
        self.websocket_dir = None
        self.eog_dir = None
        self.eeg_dir = None

    def set_folders(self, eeg, eog, websocket, gsr):
        self.eeg_dir = eeg
        self.eog_dir = eog
        self.websocket_dir = websocket
        self.gsr_dir = gsr


def create_folder_structure(player_name: str, date: str, config: yaml):
    root_data_path = Path(config['DATA_CAPTURE']['ROOT_DATA_PATH'])
    print("creating the folder structure in {}".format(root_data_path))
    dir_list = config['DATA_CAPTURE']['DIRECTORIES']
    for i in dir_list:
        _dir = root_data_path / date / player_name / i
        # we'll create the directory if it doesn't exist yet, otherwise we'll have to check first
        try:
            Path.mkdir(Path(_dir), parents=True, exist_ok=False)
        except FileExistsError as e:
            res = input("Folder exists already, do you really want to overwrite it? Y/N")
            if res == "Y":
                Path.mkdir(Path(_dir), parents=True, exist_ok=True)
            else:
                continue


def create_player_conf():
    # create a conf file for the player
    print("todo")


if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()
    # load the config file
    config = load_config(Path(Path.cwd() / "conf.yaml"))
    # make a player object to keep track of variables
    player = PlayerSession(gui.get_results(), datetime.now().strftime("%Y_%m_%d__%H_%M"))
    # create the folder structure to capture the different datastreams
    create_folder_structure(player.name, player.playtime, config)
    # open websocket and stream data to folder websocket (separate files for EOG data?)

    # open EEG stream and stream towards EEG folder

    # open GSR and stream towards GSR folder
