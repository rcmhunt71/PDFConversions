import os

import yaml


class DefaultValues:
    DEFAULTS_CFG_FILE = 'defaults.cfg'

    APP_DEFAULTS = 'defaults'
    TIFF_DEFAULTS = 'tif'
    WEBP_DEFAULTS = 'webp'

    def __init__(self, filename: str = DEFAULTS_CFG_FILE):
        self.cfg_file = filename
        for domain, data in self._read_cfg_file().items():
            setattr(self, domain, data)

    def _read_cfg_file(self):
        if not os.path.exists(self.cfg_file):
            return

        # Read the defaults config file
        with open(self.DEFAULTS_CFG_FILE, "r") as CFG:
            defaults = yaml.safe_load(CFG)

        return defaults
