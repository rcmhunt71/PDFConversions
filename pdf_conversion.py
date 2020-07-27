#1/usr/bin/python

import typing

from document import Document
from pdf2tiff import PdfToTiff
from tiff2webp import TiffToWebp
from file_extensions import SupportedDocTypes


class NoTargetConversionType(Exception):
    def __str__(self):
        return "No target conversion format specified."


class PDFConversion:

    def __init__(self, document: Document, target_type: str = None) -> None:
        self.document = document
        self.target_type = target_type

    def set_type(self, target_type: SupportedDocTypes):
        self.target_type = target_type
        return self

    def convert(self, doc_format: SupportedDocTypes = None, **kwargs):
        doc_format = doc_format or self.target_type
        if doc_format is None:
            raise NoTargetConversionType

        if self.document.doc_type.lower() == doc_format.value:
            print(f"Target Format ('{doc_format.value}') matches the current document type. Nothing to do.")
            return self

        if doc_format in [SupportedDocTypes.WEBP, SupportedDocTypes.TIFF]:
            self._convert_pdf_to_tiff(**kwargs)

        if doc_format == SupportedDocTypes.WEBP:
            self._convert_tiff_to_webp(**kwargs)

    def _convert_pdf_to_tiff(self, **kwargs) -> typing.NoReturn:
        converter = PdfToTiff(src_file_spec=self.document.filespec, output_folder=self.document.image_dir, **kwargs)
        converter.convert()
        self.document.images.extend(converter.images)
        self.document.conversion_duration = converter.conversion_duration

    def _convert_tiff_to_webp(self, **kwargs) -> typing.NoReturn:
        tiffs = [image for image in self.document.images if image.lower().endswith(SupportedDocTypes.TIFF.value)]
        for image in tiffs:
            converter = TiffToWebp(src_file_spec=image, output_folder=self.document.image_dir, **kwargs)
            converter.convert()
            self.document.images.extend(converter.images)
            self.document.conversion_duration += converter.conversion_duration


