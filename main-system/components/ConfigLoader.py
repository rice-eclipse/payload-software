import json

class ConfigLoader:
    def __init__(self, config_filepath: str):
        self.config_filepath = config_filepath
        self.loaded_configs = json.load(open(config_filepath))
    
    def fetch_imaging_configs(self):
        """
        Returns all configs related to the camera imaging
        """
        return self.loaded_configs["imaging_configs"]

    def fetch_exstate_configs(self):
        """
        Returns all exteral state configs
        """
        return self.loaded_configs["exstate_configs"]

    def fetch_all_configs(self):
        """
        Returns all configs in a single dictionary
        """
        imaging = self.loaded_configs["imaging_configs"]
        exstate = self.loaded_configs["exstate_configs"]

        return imaging | exstate

# config = ConfigLoader("main-system\components\config.json")
# print(config.fetch_all_configs())
# print(config.fetch_exstate_configs())
# print(config.fetch_imaging_configs())