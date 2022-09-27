import argparse
import csv
import time
from pprint import pprint

import brainflow.exit_codes
from brainflow import BrainFlowError, DataFilter
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets

import get_com_port


def eeg_board_setup() -> BoardShim:
    BoardShim.enable_dev_board_logger()

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False,
                        default=get_com_port.return_com_port("FTDI"))
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=False, default=BoardIds.CYTON_BOARD)  # CYTON_DAISY_BOARD)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    parser.add_argument('--master-board', type=int, help='master board id for streaming and playback boards',
                        required=False, default=BoardIds.NO_BOARD)
    parser.add_argument('--preset', type=int, help='preset for streaming and playback boards',
                        required=False, default=BrainFlowPresets.DEFAULT_PRESET)
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file
    params.master_board = args.master_board
    params.preset = args.preset

    board = BoardShim(args.board_id, params)
    board.prepare_session()
    return board


def common_capture(board: BoardShim):
    eeg_names = board.get_eeg_names(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
    print("eeg names, according to Default 10-20 locations: {}".format(eeg_names))
    eeg_channels = board.get_eeg_channels(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
    print("eeg channels: {}".format(eeg_channels))
    board_descr = board.get_board_descr(board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)

    print("board description: ")
    pprint(board_descr)
    try:
        emg_ch = board.get_emg_channels(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
        ecg_ch = board.get_ecg_channels(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
        eog_ch = board.get_eog_channels(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)

        acc_ch = board.get_accel_channels(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
        anal_ch = board.get_analog_channels(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
        other_ch = board.get_other_channels(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
        if board.board_id != BoardIds.CYTON_BOARD | board.board_id != BoardIds.CYTON_DAISY_BOARD:
            exg_ch = board.get_exg_channels(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
            gyro_ch = board.get_gyro_channels(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
            eda_ch = board.get_eda_channels(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
            ppg_ch = board.get_ppg_channels(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
            temp_ch = board.get_temperature_channels(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
            res_ch = board.get_resistance_channels(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET)
    except BrainFlowError as e:
        print(e)
        pass
    try:
        data = board.get_board_data()  # get all data and remove it from internal buffer
        print(board.get_sampling_rate(board_id=board.board_id, preset=BrainFlowPresets.DEFAULT_PRESET))
    except BrainFlowError as e:
        print(e)
        pass


def prep_stream_file(filename):
    header_list = ["package_number", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8", "ch9", "ch10", "ch11",
                   "ch12", "ch13", "ch14", "ch15", "ch16", "acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z",
                   "eda",
                   "ppg1", "ppg2", "temp", "res_1", "res_2", "battery", "timestamp", "marker_ch", "num_rows"]
    try:
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter="\t")
            csvwriter.writerow(header_list)
    except Exception as e:
        print(e)
        return False
    return True


def stream_to_ip(board: BoardShim, ip: str = "224.0.0.1", port: str = "5050"):
    board.add_streamer(streamer_params="streaming_board://{}:{}".format(ip, port))


def stream_to_file(board: BoardShim, filename: str):
    board.add_streamer(streamer_params="file://{}:a".format(filename))


def save_to_file(board: BoardShim, filename: str):
    data = board.get_board_data()
    DataFilter.write_file(data, filename, 'a')  # use 'a' for append mode


def insert_marker_test(board: BoardShim, i: float):
    board.insert_marker(i)
    print("inserted {}".format(i))


def main():
    board = eeg_board_setup()
    csv_file = "test.csv"
    prep_stream_file(csv_file)
    # stream_to_ip(board)
    stream_to_file(board, csv_file)
    board.start_stream()
    # # time.sleep(10)
    # common_capture(board)
    #
    i = 1.0
    try:
        while True:
            insert_marker_test(board, i)
            i += 0.1
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    print("finishing up")
    board.stop_stream()
    board.release_session()


if __name__ == "__main__":
    main()
