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


class EEG:
    def __init__(self, config: yaml, root_data_path: Path, board_id: BoardIds = BoardIds.CYTON_BOARD):
        print("EEG init")
        self.board = None
        self.board_id = board_id
        self.config = config
        self.file = Path(root_data_path / 'eeg' / config["DATA_CAPTURE"]["EEG"])
        BoardShim.enable_dev_board_logger()

        params = BrainFlowInputParams()
        # params.ip_port = args.ip_port
        params.serial_port = get_com_port.return_com_port("FTDI")
        # params.mac_address = args.mac_address
        # params.other_info = args.other_info
        # params.serial_number = args.serial_number
        # params.ip_address = args.ip_address
        # params.ip_protocol = args.ip_protocol
        # params.timeout = args.timeout
        # params.file = args.file
        # params.master_board = args.master_board
        # params.preset = args.preset

        self.board = BoardShim(self.board_id, params)
        self.board.prepare_session()

    def common_capture(self):
        eeg_names = self.board.get_eeg_names(board_id=self.board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
        print("eeg names, according to Default 10-20 locations: {}".format(eeg_names))
        eeg_channels = self.board.get_eeg_channels(board_id=self.board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
        print("eeg channels: {}".format(eeg_channels))
        board_descr = self.board.get_board_descr(self.board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)

        print("board description: ")
        pprint(board_descr)
        try:
            emg_ch = self.board.get_emg_channels(board_id=self.board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
            ecg_ch = self.board.get_ecg_channels(board_id=self.board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
            eog_ch = self.board.get_eog_channels(board_id=self.board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)

            acc_ch = self.board.get_accel_channels(board_id=self.board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
            anal_ch = self.board.get_analog_channels(board_id=self.board.board_id,
                                                     preset=BrainFlowPresets.DEFAULT_PRESET)
            other_ch = self.board.get_other_channels(board_id=self.board.board_id,
                                                     preset=BrainFlowPresets.DEFAULT_PRESET)
            if self.board.board_id != BoardIds.CYTON_BOARD | self.board.board_id != BoardIds.CYTON_DAISY_BOARD:
                exg_ch = self.board.get_exg_channels(board_id=self.board.board_id,
                                                     preset=BrainFlowPresets.DEFAULT_PRESET)
                gyro_ch = self.board.get_gyro_channels(board_id=self.board.board_id,
                                                       preset=BrainFlowPresets.DEFAULT_PRESET)
                eda_ch = self.board.get_eda_channels(board_id=self.board.board_id,
                                                     preset=BrainFlowPresets.DEFAULT_PRESET)
                ppg_ch = self.board.get_ppg_channels(board_id=self.board.board_id,
                                                     preset=BrainFlowPresets.DEFAULT_PRESET)
                temp_ch = self.board.get_temperature_channels(board_id=self.board.board_id,
                                                              preset=BrainFlowPresets.DEFAULT_PRESET)
                res_ch = self.board.get_resistance_channels(board_id=self.board.board_id,
                                                            preset=BrainFlowPresets.DEFAULT_PRESET)
        except BrainFlowError as e:
            print(e)
            pass
        try:
            data = self.board.get_board_data()  # get all data and remove it from internal buffer
            print(self.board.get_sampling_rate(board_id=self.board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET))
        except BrainFlowError as e:
            print(e)
            pass

    def prep_stream_file(self):
        header_list = ["package_number", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8", "ch9", "ch10", "ch11",
                       "ch12", "ch13", "ch14", "ch15", "ch16", "acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z",
                       "eda",
                       "ppg1", "ppg2", "temp", "res_1", "res_2", "battery", "timestamp", "marker_ch", "num_rows"]
        try:
            with open(self.file, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter="\t")
                csvwriter.writerow(header_list)
        except Exception as e:
            print(e)
            return False
        return True

    def stream_to_ip(self):
        ip = self.config["DATA_CAPTURE"]["STREAM"]["IP"]
        port = self.config["DATA_CAPTURE"]["STREAM"]["PORT"]
        self.board.add_streamer(streamer_params="streaming_board://{}:{}".format(ip, port))

    def stream_to_file(self):
        self.board.add_streamer(streamer_params="file://{}:a".format(self.file))

    def save_to_file(self):
        data = self.board.get_board_data()
        DataFilter.write_file(data, str(self.file.resolve()), 'a')  # use 'a' for append mode

    def insert_marker(self, i: float):
        print("inserting {}".format(i))

        self.board.insert_marker(i)

    def config_board(self):
        """
        config board is a function to set the OpenBCI in a mode to record directly to the SD Card
        This function needs to be called AFTER prepare_session and BEFORE start_stream!
        :param board:
        """
        if not self.board.is_prepared():
            print("first prepare the board!")
            return

        res = self.board.config_board("V")
        print("Board version: {}".format(res))

        logging_time = {
            "A": "5m",
            "S": "15m",
            "F": "30m",
            "G": "1h",
            "H": "2h",
            "J": "4h",
            "K": "12h",
            "L": "24h",
            "a": "14s"
        }

        SD_CMD = list(logging_time.keys())[
            list(logging_time.values()).index(self.config["DATA_CAPTURE"]["SD_CARD_TIME"])]
        if SD_CMD:
            print("setting the SD card to {}, with cmd {}".format(self.config["DATA_CAPTURE"]["SD_CARD_TIME"], SD_CMD))
            self.board.config_board(SD_CMD)
        else:
            print("didn't find correct SD Card command?")

    def stop_sd_recording(self):
        self.board.config_board("j")
        print("stopping SD card recording")

    def launch_eeg(self):
        self.prep_stream_file()
        # self.stream_to_ip()
        self.stream_to_file()
        self.config_board()
        self.board.start_stream()
        # self.common_capture()
        print("EEG started")

    def start_test_markers_thread(self):
        x = threading.Thread(target=self.test_markers())
        logging.info("Main    : before running thread")
        x.start()
        logging.info("Main    : wait for the thread to finish")
        x.join()
        logging.info("Main    : all done")

    def test_markers(self):
        i = 1.0
        try:
            while True:
                print("sending {}".format(i))
                self.insert_marker(i)
                i += 0.1
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        self.stop_eeg()

    @atexit.register
    def stop_eeg(self):
        # make sure we clean the connection if the application is stopped
        print("finishing up EEG")
        self.stop_sd_recording()
        self.board.stop_stream()
        self.board.release_session()
