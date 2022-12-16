import argparse
import atexit
import csv
import logging
import threading
import time
from datetime import datetime
from pathlib import Path
from pprint import pprint

import brainflow.exit_codes
import yaml
from brainflow import BrainFlowError, DataFilter
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
import sys

from Player.PlayerSession import PlayerSession

sys.path.append("../")
from utils import get_com_port
from utils.utils import load_config


class GSR:
    def __init__(self, config: yaml, root_data_path: Path, ip: str = "192.168.50.110",
                 board_id: BoardIds = BoardIds.EMOTIBIT_BOARD):
        print("GSR init")
        self.board = None
        self.board_id = board_id
        self.config = config
        self.ip = ip
        self.file = Path(root_data_path / 'gsr' / config["DATA_CAPTURE"]["GSR"])
        BoardShim.enable_dev_board_logger()

        params = BrainFlowInputParams()
        params.ip_address = self.ip
        self.board = BoardShim(self.board_id, params)
        self.board.prepare_session()

    def prep_stream_file(self):
        header_list = ["package_number", "acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z", "mag_x", "mag_y",
                       "mag_z", "timestamp", "marker_ch",
                       "num_rows"]
        try:
            with open(self.file, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter="\t")
                csvwriter.writerow(header_list)
        except Exception as e:
            print(e)
            return False
        return True

    def stream_to_file(self):
        print(self.file)
        self.board.add_streamer(streamer_params="file://{}:a".format(self.file))

    def insert_marker(self, i: float):
        print("inserting {}".format(i))

        self.board.insert_marker(i)


if __name__ == '__main__':
    # first we need to enter the device's IP in the config file
    # then we open the Emotibit Oscilloscope to see if data is flowing correctly
    #   if LSL is connected
    print("Is the LSL stream connected in Emotibit Oscilloscope?")
    config = load_config(Path(Path.cwd().parent / "conf.yaml"))

    gsr = GSR(config, Path(Path.cwd()))
    print(gsr.board.get_board_descr(gsr.board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET))
    # we establish communication to the emotibit: [CMD: HE]
    # then: we send the command to start record (to SD): [CMD: RB]
    gsr.stream_to_file()
    gsr.board.start_stream()

    # finally: stop command [CMD: RE]
    while True:
        time.sleep(1.0)
    # todo: necessary to write custom software?? No, if we use the LSL marker stream!
