import argparse
import os
import typing

from pdf_conversion.documents.file_extensions import SupportedDocTypes


class CommandLine:

    DEFAULT_IMAGE_DIR = '.'
    DEFAULT_DPI = 200
    DEFAULT_QUALITY = 90
    DEFAULT_FORMAT = SupportedDocTypes.WEBP
    DEFAULT_LOSSLESS = True
    DEFAULT_THREADS = 4

    CONV_TYPES = dict([(doc_type.value, doc_type.name) for doc_type in SupportedDocTypes if
                       not doc_type.name.lower().startswith("not")])

    def __init__(self, defaults_dict: typing.Optional[dict] = None):
        """
        Sets up the CLI arguments.
        NOTE: If an option is added or removed, be sure to update CommandLine.print_args() to reflect the change.

        :param defaults_dict: Defaults to use. Overrides class level defaults. Class-level defaults are set in case
             no defaults are specified or can be found.

        """

        # Override class level defaults, if specified.
        if defaults_dict is not None:
            self._set_defaults(defaults_dict)

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-f", "--format",
                                 help=f"Conversion Format. Supported Formats: "
                                      f"{', '.join(sorted(list(self.CONV_TYPES.keys())))}  "
                                      f"(Default: {self.DEFAULT_FORMAT.value})",
                                 default=self.DEFAULT_FORMAT.value,
                                 type=str)
        self.parser.add_argument("-d", "--dpi",
                                 help=f"Set conversion DPI (Default: {self.DEFAULT_DPI})",
                                 default=-1,
                                 type=int)
        self.parser.add_argument("-t", "--threads",
                                 help=f"Set number of processing threads (tiff). Default: {self.DEFAULT_THREADS}",
                                 default=-1,
                                 type=int)
        self.parser.add_argument('-l', '--not_lossless',
                                 help=f"Do not create a lossless representation, if applicable.",
                                 action='store_true',
                                 default=self.DEFAULT_LOSSLESS)
        self.parser.add_argument("-q", "--quality",
                                 help=f"Quality Factor [0, 100], Compression value [0, 100] if lossless "
                                      f"(Default: {self.DEFAULT_QUALITY})",
                                 default=-1,
                                 type=int)
        self.parser.add_argument("-i", "--image_dir",
                                 help=f"Set the image storage directory. (Default: {self.DEFAULT_IMAGE_DIR})",
                                 default=self.DEFAULT_IMAGE_DIR,
                                 type=str)

        self.args = self.parser.parse_args()
        self.args.lossless = not self.args.not_lossless
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
                  f"\t Using the default format: '{self.DEFAULT_FORMAT.name.lower()}'\n")
            enum_name = self.DEFAULT_FORMAT.name
        return getattr(SupportedDocTypes, enum_name)

    def print_args(self) -> typing.NoReturn:
        """
        Print the arg values provided by the CLI.

        :return: None
        """
        border = '-' * 80
        print(border)
        print(f"FORMAT: {self.args.doc_format.value}")
        print(f"TIFF --> DPI: {self.args.dpi}  Threads: {self.args.threads}")
        print(f"WEBP --> Quality: {self.args.quality}  Lossless? {str(not self.args.not_lossless)}")
        print(f"Image Directory: {os.path.abspath(self.args.image_dir)} (Provided [raw]: '{self.args.image_dir}')")
        print(border)

    def _set_defaults(self, config: typing.Dict[any, any]) -> typing.NoReturn:
        """
        Read the defaults config file and overwrite hardcoded defaults with desired defaults.

        :return: None
        """
        for def_key, default_val in config.items():
            # Convert the format to the corresponding tuple.
            if def_key.lower() == 'format':
                tuple_name = self.CONV_TYPES.get(default_val.lower(), None)
                if tuple_name is None:
                    print(f"\n\tWARNING: Target_format ('{default_val}') is not supported. "
                          f"Using the default format: '{self.DEFAULT_FORMAT.value}' for the CLI option default.\n")
                    continue
                default_val = getattr(SupportedDocTypes, tuple_name)

            setattr(self, f"DEFAULT_{def_key.upper()}", default_val)
