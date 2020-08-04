import argparse

from pdf_conversion.documents.file_extensions import SupportedDocTypes


class CommandLine:

    DEFAULT_DPI = 100
    DEFAULT_QUALITY = 90
    TARGET_TYPE = 'webp'

    CONV_TYPES = dict([(doc_type.name, doc_type.value) for doc_type in SupportedDocTypes if
                       not doc_type.name.lower().startswith("not")])

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-d", "--dpi", help=f"Set conversion DPI (Default: {self.DEFAULT_DPI})",
                                 default=self.DEFAULT_DPI, type=int)
        self.parser.add_argument("-q", "--quality", help=f"Quality Factor [0, 100] (Default: {self.DEFAULT_QUALITY})",
                                 default=self.DEFAULT_QUALITY, type=int)
        self.parser.add_argument("-t", "--type",
                                 help=f"Conversion Format. Supported Formats: "
                                      f"{', '.join(sorted(list(self.CONV_TYPES.values())))}"
                                      f"  (Default: {self.TARGET_TYPE})",
                                 default=self.TARGET_TYPE)
        self.args = self.parser.parse_args()
        self.args.doc_type = self._validate_doc_type()

    def _validate_doc_type(self):
        return (self.CONV_TYPES[self.args.type.lower()] if self.args.type.lower() in self.CONV_TYPES else
                self.CONV_TYPES[CommandLine.TARGET_TYPE])
