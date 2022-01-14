import yaml
import os
from enum import Enum
from .bunchify import Bunchify


class ConfigType(Enum):
    YAML = 'yml'


class Config:
    @staticmethod
    def read_conf(name: str, config_type: ConfigType = ConfigType.YAML) -> Bunchify:
        root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        path = os.path.join(root_path, f"config/{name}.{config_type.value}")
        with open(path) as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)
            f.close()

        return Bunchify(conf)
