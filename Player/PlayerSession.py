import json
from pathlib import Path


class PlayerSession:
    def __init__(self, player_config: dict, playtime: str):
        self.gender = player_config.get("gender")
        self.name = player_config.get("name")
        self.age = player_config.get("age")
        self.contingency = player_config.get("contingency")
        self.treatment = player_config.get("treatment")
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

    def create_player_conf(self, location, file_name):
        # create a conf file for the player
        conf = {
            "name": self.name,
            "contingency": self.contingency,
            "date": self.playtime,
            "age": self.age,
            "gender": self.gender,
            "treatment": self.treatment
        }
        with open(Path(location / file_name), "w+") as c:
            res = json.dumps(conf)
            c.write(res)
