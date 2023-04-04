"""Example program to demonstrate how to read string-valued markers from LSL."""
import logging
import threading

from pylsl import StreamInlet, resolve_stream

from EEG.brainflow_get_data import EEG


class LSLReceptor:
    def __init__(self, eeg: EEG = None, prop: str = 'type', value: str = 'Markers'):
        """.
        function to capture LSL markers, we can convert these to float markers as described in data document
        :param prop: usually you don't touch this
        :param value: can be adjusted, we'll only be looking for data of this 'type'
        """
        self.streams = resolve_stream(prop, value)
        # create a new inlet to read from the stream
        self.inlet = StreamInlet(self.streams[0])
        self.Marker = {'game_start': 0, 'ball_release': 1, 'ball_good_hit': 2, 'ball_bad_hit': 3, 'score': 4, 'test': 5,
                       'end_game': 6}
        self.eeg = eeg

    def is_running(self):
        # print(self.inlet.info())
        if self.inlet.channel_count >= 1:
            return True
        else:
            return False
        # todo return boolean value to check if running!

    def start_receive_thread(self):
        x = threading.Thread(target=self.receive_test)
        logging.info("Main    : before running thread")
        x.start()
        logging.info("Main    : wait for the thread to finish")
        return x

    def receive_test(self):
        while True:
            # get a new sample (you can also omit the timestamp part if you're not
            # interested in it)
            sample, timestamp = self.inlet.pull_sample()
            print("got %s at time %s from name %s and source id %s" % (
                sample[0], timestamp, self.streams[0].name(), self.streams[0].source_id()))
            if self.eeg is not None:
                self.eeg.insert_marker(round(sample[0], 1))
            try:
                print("converted: {}".format(list(self.Marker.keys())[list(self.Marker.values()).index(sample[0])]))
            except Exception as e:
                print(e)
                pass

    def receive_when_sample_available(self):
        # we set timeout to 0.0, so it doesn't block
        sample, timestamp = self.inlet.pull_sample(timeout=0.0)
        # print("got %s at time %s" % (sample[0], timestamp))
        if sample is not None:
            sample = self.convert_marker_to_Brainflow(sample)
        return sample, timestamp

    @staticmethod
    def convert_marker_to_Brainflow(stringsample: str):
        print('todo')
        float_sample = 1.0  # todo make the magic of conversion happen
        return float_sample


def main():
    # lsl = LSLReceptor(value="Markers")
    # lsl = LSLReceptor(prop="source_id", value="LSL2")
    lsl = LSLReceptor(prop="name", value="DataSyncMarker_eeg")
    print(lsl.inlet.value_type)
    lsl.start_receive_thread()


if __name__ == '__main__':
    main()
