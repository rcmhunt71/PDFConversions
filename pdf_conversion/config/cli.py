import argparse
import os
import typing

from pdf_conversion.documents.file_extensions import SupportedDocTypes

import yaml


class CommandLine:

    DEFAULTS_CFG_FILE = "defaults.cfg"
    DEFAULT_CFG_DIR = "."
    DEFAULT_DPI = 100
    DEFAULT_QUALITY = 90
    TARGET_FORMAT = SupportedDocTypes.WEBP
    LOSSLESS = False

    CONV_TYPES = dict([(doc_type.value, doc_type.name) for doc_type in SupportedDocTypes if
                       not doc_type.name.lower().startswith("not")])

    def __init__(self):
        self._get_defaults()
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-d", "--dpi",
                                 help=f"Set conversion DPI (Default: {self.DEFAULT_DPI})",
                                 default=self.DEFAULT_DPI,
                                 type=int)
        self.parser.add_argument("-f", "--format",
                                 help=f"Conversion Format. Supported Formats: "
                                      f"{', '.join(sorted(list(self.CONV_TYPES.keys())))}  "
                                      f"(Default: {self.TARGET_FORMAT.value})",
                                 default=self.TARGET_FORMAT.value,
                                 type=str)
        self.parser.add_argument('-l', '--lossless',
                                 help=f"Create a lossless representation. Default={self.LOSSLESS}",
                                 action='store_true',
                                 default=self.LOSSLESS)
        self.parser.add_argument("-q", "--quality",
                                 help=f"Quality Factor [0, 100], Compression value [0, 100] if lossless "
                                      f"(Default: {self.DEFAULT_QUALITY})",
                                 default=self.DEFAULT_QUALITY,
                                 type=int)
        self.parser.add_argument("-c", "--cfg",
                                 help=f"Path to config files for defaults. "
                                      f"Default: '{os.path.abspath(self.DEFAULT_CFG_DIR)}'",
                                 default=self.DEFAULT_CFG_DIR,
                                 type=str)

        self.args = self.parser.parse_args()
        self.args.doc_format = self._validate_doc_format_type()

    def _validate_doc_format_type(self) -> SupportedDocTypes:
        """
        Verify specified conversion format matches supported types.

        :return:  if supported, the corresponding SupportedDocTypes enum,
                  if not supported, the default SupportedDocTypes enum format type

        """
        if self.args.format.lower() in self.CONV_TYPES.keys():
            enum_name = self.CONV_TYPES[self.args.format.lower()]
        else:
            print(f"WARNING: Unrecognized conversion format: '{self.args.format.lower()}' -- "
                  f"Supported formats: {', '.join(sorted(list(self.CONV_TYPES.keys())))}\n"
                  f"\t Using the default format: '{self.TARGET_FORMAT.name.lower()}'\n")
            enum_name = self.TARGET_FORMAT.name
        return getattr(SupportedDocTypes, enum_name)

    def print_args(self) -> typing.NoReturn:
        """
        Print the arg values provided by the CLI.
        :return: None
        """
        print(f"DPI: {self.args.dpi}  Quality: {self.args.quality}  Lossless? {str(self.args.lossless)}")
        print(f"Conversion Format: {self.args.doc_format.value}")

    def _get_defaults(self) -> typing.NoReturn:
        """
        Read the defaults config file and overwrite hardcoded defaults with desired defaults.

        :return: None.

        """
        if not os.path.exists(self.DEFAULTS_CFG_FILE):
            return

        # Read the defaults config file
        with open(self.DEFAULTS_CFG_FILE, "r") as CFG:
            defaults = yaml.safe_load(CFG)

        # Iterate through the file and update any attributes that are already defined.
        for def_key, default_val in defaults.items():
            if hasattr(self, def_key.upper()):

                # Convert the format to the corresponding tuple.
                if def_key.upper() == 'TARGET_FORMAT':
                    tuple_name = self.CONV_TYPES.get(default_val.lower(), None)
                    if tuple_name is None:
                        print(f"\n\tWARNING: Target_format ('{default_val}') is not supported. "
                              f"Using the default format: '{self.TARGET_FORMAT.value}' for the CLI option default.\n")
                        continue
                    default_val = getattr(SupportedDocTypes, tuple_name)

                setattr(self, def_key.upper(), default_val)
