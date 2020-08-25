import os
import typing

import yaml


class DefaultValues:
    DEFAULTS_CFG_FILE = 'defaults.cfg'

    APP_DEFAULTS = 'defaults'
    TIFF_DEFAULTS = 'tif'
    WEBP_DEFAULTS = 'webp'

    def __init__(self, filespec: str = DEFAULTS_CFG_FILE) -> typing.NoReturn:
        """
        Default Values Constructor
        :param filespec: Filespec to read.
        """
        self.cfg_file = filespec

        # For each key, create an attribute and store the value dict in the attribute.
        for domain, data in self._read_cfg_file().items():
            setattr(self, domain, data)

    def _read_cfg_file(self) -> typing.Dict[str, dict]:
        """
        Read YAML config file into a complex data structure (defaults)
        
        :return: JSON data structure 
        """
        if not os.path.exists(self.cfg_file):
            return {}

        # Read the defaults config file
        with open(self.DEFAULTS_CFG_FILE, "r") as CFG:
            defaults = yaml.safe_load(CFG)

        return defaults
