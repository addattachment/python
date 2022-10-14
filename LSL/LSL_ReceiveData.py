"""Example program to demonstrate how to read string-valued markers from LSL."""

from pylsl import StreamInlet, resolve_stream


class LSLReceptor:
    def __init__(self, prop: str = 'type', value: str = 'Markers'):
        """
        function to capture LSL markers, we can convert these to float markers as described in data document
        :param prop: usually you don't touch this
        :param value: can be adjusted, we'll only be looking for data of this 'type'
        """
        self.streams = resolve_stream(prop, value)
        # create a new inlet to read from the stream
        self.inlet = StreamInlet(self.streams[0])

    def is_running(self):
        # print(self.inlet.info())
        if self.inlet.channel_count >= 1:
            return True
        else:
            return False
        # todo return boolean value to check if running!

    def receive_test(self):
        while True:
            # get a new sample (you can also omit the timestamp part if you're not
            # interested in it)
            sample, timestamp = self.inlet.pull_sample()
            print("got %s at time %s" % (sample[0], timestamp))

    def receive_when_sample_available(self):
        # we set timeout to 0.0 so it doesn't block
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
    lsl = LSLReceptor(value="Markers")
    lsl.receive_test()


if __name__ == '__main__':
    main()
