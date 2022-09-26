import yaml as yaml
"""
utils functions
"""

def load_config(config_path):
    try:
        with open(config_path, "r") as config_file:
            return yaml.safe_load(config_file)
    except yaml.YAMLError as e:
        print(e)
