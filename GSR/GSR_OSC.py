from pythonosc import dispatcher
from pythonosc import osc_server
import pandas as pd


class GSR:
    def __init__(self, ip, port):
        self.GSR_Values = {
            "/EmotiBit/0/PPG:RED": "PPG_RED",
            "/EmotiBit/0/PPG:IR": "PPG_IR",
            "/EmotiBit/0/PPG:GRN": "PPG_GRN",
            "/EmotiBit/0/EDA": "EDA",
            "/EmotiBit/0/HUMIDITY": "HUM",
            "/EmotiBit/0/ACC:X": "ACC_X",
            "/EmotiBit/0/ACC:Y": "ACC_Y",
            "/EmotiBit/0/ACC:Z": "ACC_Z",
            "/EmotiBit/0/GYRO:X": "GYR_X",
            "/EmotiBit/0/GYRO:Y": "GYR_Y",
            "/EmotiBit/0/GYRO:Z": "GYR_Z",
            "/EmotiBit/0/MAG:X": "MAG_X",
            "/EmotiBit/0/MAG:Y": "MAG_Y",
            "/EmotiBit/0/MAG:Z": "MAG_Z",
            "/EmotiBit/0/THERM": "THERM",
            "/EmotiBit/0/TEMP": "TEMP"
        }
        self.df = pd.DataFrame()
        self.ip = ip
        self.port = port

    @staticmethod
    def print_volume_handler(unused_addr, args, volume):
        """
        function to check what we're receiving
        :param unused_addr:
        :param args:
        :param volume:
        """
        print("[{0}] ~ {1}".format(args[0], volume))

    def create_dispatchers(self):
        dispatch = dispatcher.Dispatcher()
        for osc_cmd, df_col in self.GSR_Values.items():
            dispatch.map(osc_cmd, self.print_volume_handler, df_col)
        server = osc_server.ThreadingOSCUDPServer(
            (self.ip, self.port), dispatch)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()


if __name__ == '__main__':
    print("make sure to adapt the ipAddress and port specified in oscOutputSettings.xml file. (available in the "
          "C:\Program Files\EmotiBit\EmotiBit Oscilloscope\data folder for Windows). ")
    print("also, make sure the LSL marker stream is correct [link]("
          "https://github.com/EmotiBit/EmotiBit_Docs/blob/master/Working_with_emotibit_data.md#using-lsl-with"
          "-emotibit-oscilloscope)")
    default_ip = "127.0.0.1"
    default_port = 12345
    gsr = GSR(default_ip, default_port)
    gsr.create_dispatchers()
