import yaml
import os

def load_config(config_path: str = "config/config.yaml") -> dict:
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        # print(config)
    return config

class ConfigLoader:
    """Configuration loader class for the application"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        
    def load_config(self) -> dict:
        """Load configuration from YAML file"""
        return load_config(self.config_path)