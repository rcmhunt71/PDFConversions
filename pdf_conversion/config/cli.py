import argparse

from pdf_conversion.documents.file_extensions import SupportedDocTypes


class CommandLine:

    DEFAULT_DPI = 100
    DEFAULT_QUALITY = 90
    TARGET_FORMAT = SupportedDocTypes.WEBP

    CONV_TYPES = dict([(doc_type.value, doc_type.name) for doc_type in SupportedDocTypes if
                       not doc_type.name.lower().startswith("not")])

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-d", "--dpi",
                                 help=f"Set conversion DPI (Default: {self.DEFAULT_DPI})",
                                 default=self.DEFAULT_DPI,
                                 type=int)
        self.parser.add_argument("-q", "--quality",
                                 help=f"Quality Factor [0, 100] (Default: {self.DEFAULT_QUALITY})",
                                 default=self.DEFAULT_QUALITY,
                                 type=int)
        self.parser.add_argument("-f", "--format",
                                 help=f"Conversion Format. Supported Formats: "
                                      f"{', '.join(sorted(list(self.CONV_TYPES.keys())))}  "
                                      f"(Default: {self.TARGET_FORMAT.value})",
                                 default=self.TARGET_FORMAT.value,
                                 type=str)
        self.args = self.parser.parse_args()
        self.args.doc_format = self._validate_doc_format_type()

    def _validate_doc_format_type(self):
        enum_name = (self.CONV_TYPES[self.args.format.lower()] if self.args.format.lower() in self.CONV_TYPES.keys()
                     else self.TARGET_FORMAT.name)
        return getattr(SupportedDocTypes, enum_name)