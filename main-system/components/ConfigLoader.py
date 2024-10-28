import json

class ConfigLoader:
    def __init__(self, config_filepath: str):
        self.config_filepath = config_filepath
        self.loaded_configs = json.load(open(config_filepath))
    
    def fetch_imaging_configs(self):
        """
        returns all imaging configs
        """
        return self.loaded_configs["imaging"]

    def fetch_exstate_configs(self):
        """
        returns all exteral configs
        """
        return self.loaded_configs["exstate"]

    def fetch_all_configs(self):
        """
        returns all configs
        """
        return self.loaded_configs

config = ConfigLoader("main-system\components\config.json")
print(config.fetch_all_configs())
print(config.fetch_exstate_configs())
print(config.fetch_imaging_configs())