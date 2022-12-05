"""Example program to demonstrate how to send string-valued markers into LSL."""

import random
import time

from pylsl import StreamInfo, StreamOutlet


def main(streamName: str = 'MyMarkerStream', contentType: str = "Markers", sourceId: str = "myuidw43536"):
    # first create a new stream info (here we set the name to MyMarkerStream,
    # the content-type to Markers, 1 channel, irregular sampling rate,
    # and string-valued data) The last value would be the locally unique
    # identifier for the stream as far as available, e.g.
    # program-scriptname-subjectnumber (you could also omit it but interrupted
    # connections wouldn't auto-recover). The important part is that the
    # content-type is set to 'Markers', because then other programs will know how
    #  to interpret the content
    info = StreamInfo(streamName, contentType, 1, 0, 'string', sourceId)

    # next make an outlet
    outlet = StreamOutlet(info)

    print("now sending markers...")
    markernames = ['Test', 'Blah', 'Marker', 'XXX', 'Testtest', 'Test-1-2-3']
    while True:
        # pick a sample to send and wait for a bit
        outlet.push_sample([random.choice(markernames)])
        time.sleep(random.random() * 3)


if __name__ == '__main__':
    main(streamName="DataSyncMarker", contentType="Markers", sourceId="123456")
