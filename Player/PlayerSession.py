import json
from pathlib import Path


class PlayerSession:
    def __init__(self, player_config: dict, playtime: str):
        self.gender = player_config.get("gender")
        self.name = player_config.get("name")
        self.id = player_config.get("id")
        self.age = player_config.get("age")
        self.contingency = player_config.get("contingency")
        self.treatment = player_config.get("treatment")
        self.height = player_config.get("height")
        self.playtime = playtime
        self.gsr_dir = None
        self.websocket_dir = None
        self.eog_dir = None
        self.eeg_dir = None
        self.trial_block = player_config.get("trial_block")

    def set_folders(self, eeg, eog, websocket, gsr):
        self.eeg_dir = eeg
        self.eog_dir = eog
        self.websocket_dir = websocket
        self.gsr_dir = gsr

    def create_player_conf(self, location, file_name):
        # create a conf file for the player
        # **important** we don't record the players name! This is solemnly used to show the name in VR
        conf = {
            "id": self.id,
            "contingency": self.contingency,
            "date": self.playtime,
            "age": self.age,
            "gender": self.gender,
            "treatment": self.treatment,
            "height": self.height,
            "trial_block": self.trial_block
        }
        with open(Path(location / file_name), "w+") as c:
            res = json.dumps(conf)
            c.write(res)
