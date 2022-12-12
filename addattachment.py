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
import asyncio
import logging
from datetime import datetime

from brainflow import BoardIds

from EEG.brainflow_get_data import EEG
from LSL.LSL_ReceiveData import LSLReceptor
from Player.PlayerSession import PlayerSession
from utils.GUI import GUI
from utils.utils import *
from websocket.WebSocketServer import start_ws_server
import atexit


def stop_all(websocket, eeg, gsr):
    eeg.stop_eeg()


if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()
    # load the config file
    config = load_config(Path(Path.cwd() / "conf.yaml"))
    # make a player object to keep track of variables
    player = PlayerSession(gui.get_results(), datetime.now().strftime("%Y_%m_%d__%H_%M"))
    # create the folder structure to capture the different datastreams
    root_data_path = create_folder_structure(player.playtime, config)
    # create a config file keeping track of all settings for that child
    player.create_player_conf(location=root_data_path, file_name="player_config.json")
    # check if an LSL stream is running
    """IMPORTANT
    Make sure emotibit oscilloscope is looking for a stream 'DataSyncMarker_emotibit, source_id = LSL1'
    next, the python file should be the first one to connect, ONLY then you may open emotibit oscilloscope!
    """

    # open EEG stream and stream towards EEG folder
    eeg = EEG(
        config=config,
        root_data_path=root_data_path,
        board_id=BoardIds.CYTON_BOARD
    )

    lsl = LSLReceptor(eeg=eeg, prop="name", value="DataSyncMarker_eeg")
    while not lsl.is_running():
        continue

    eeg.launch_eeg()
    x = lsl.start_receive_thread()

    # eeg.start_test_markers_thread()
    # open websocket and stream data to folder websocket (separate files for EOG data?)
    websocket_data = [
        {"name": player.name},
        {"contingency": player.contingency}
    ]
    x.join()
    logging.info("Main    : all done")
    try:
        asyncio.run(start_ws_server(params=websocket_data, output_file="test.csv", ip='192.168.50.188', port=8081))
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        print("stopped by keyboard")
        stop_all(eeg=eeg)
        pass
