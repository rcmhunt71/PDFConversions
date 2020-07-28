#!/usr/bin/python

import typing

from pdf_conversion.documents.document import Document
from pdf_conversion.documents.file_extensions import SupportedDocTypes
from pdf_conversion.converters.pdf2tiff import PdfToTiff
from pdf_conversion.converters.tiff2webp import TiffToWebp


class NoTargetConversionType(Exception):
    def __str__(self):
        return "No target conversion format specified."


class PDFConversion:
    """
    Primary class for converting PDF to specified images. Contained basic logic for determining which conversion
    routines are needed, based on the extension provided.
    """

    def __init__(self, document: Document, image_format: SupportedDocTypes.NOT_DEFINED) -> None:
        """
        :param document: Instantiated Document object (contains filespec, used for tracking conversion process)
        :param image_format: Convert image from PDF to specified format.

        """
        self.document = document
        self.image_format = image_format

    def set_image_format(self, image_format: SupportedDocTypes):
        """
        Set or update the target image format to convert PDF
        :param image_format: Target image format (SupportedDocTypes enumeration)
        :return: Self (allows method chaining)

        """
        self.image_format = image_format
        return self

    def convert(self, doc_format: SupportedDocTypes = SupportedDocTypes.NOT_DEFINED, **kwargs) -> typing.NoReturn:
        """
        Convert the pdf to the desired format (either specified at method invocation or stored at the object level)
        :param doc_format: [OPTIONAL] - SupportedDocType enumeration, DEFAULT = NOT_DEFINED
        :param kwargs: Any additional argument (image format specific; see image format class specifications for
                  lists of specific parameters)

        :return: None

        """

        # Get the desired target format (specified at method call or or at object level)
        doc_format = doc_format or self.image_format
        if doc_format is None or doc_format.value is None:
            raise NoTargetConversionType

        # If target format matches current format; no op. (At this point, it must be defined doc type)
        if self.document.doc_type.lower() == doc_format.value:
            print(f"Target Format ('{doc_format.value}') matches the current document type. Nothing to do.")
            return self

        # For PDF to TIFF or PDF to WEBP, both need to be in the TIFF format first.
        if doc_format in [SupportedDocTypes.WEBP, SupportedDocTypes.TIFF]:
            self._convert_pdf_to_tiff(**kwargs)

        # Conversion to webp format (from intermediate TIFF format)
        if doc_format == SupportedDocTypes.WEBP:
            self._convert_tiff_to_webp(**kwargs)

    def _convert_pdf_to_tiff(self, **kwargs) -> typing.NoReturn:
        """
        Call PDF to TIFF libraries.

        :param kwargs: Additional args available to conversion process (beyond standard BaseClass args)
            * Currently no additional args defined.

        :return: None

        """
        converter = PdfToTiff(src_file_spec=self.document.filespec, output_folder=self.document.file_dir, **kwargs)
        converter.convert()
        self.document.files.extend(converter.images)
        self.document.conversion_duration = converter.conversion_duration

    def _convert_tiff_to_webp(self, **kwargs) -> typing.NoReturn:
        """
        Call TIFF to webp libraries.

        :param kwargs: Additional dictionary of args available to conversion process (beyond standard BaseClass args)
            * lossless: (bool) - Enable lossless conversion process
            * quality: (int) 0 - 100 - See pdf_conversion.converters.tiff2web.py:TiffToWeb class for details.

        :return: None

        """
        # Conversion of PDF to TIFF generates 1 TIFF per page. This information is stored in the Document class.
        # Iterate through Document.images metadata list to get the list of TIFF image file specs.
        tiffs = [image for image in self.document.files if image.lower().endswith(SupportedDocTypes.TIFF.value)]

        # Convert each image, and store the information in the Document metadata.
        for image in tiffs:
            converter = TiffToWebp(src_file_spec=image, output_folder=self.document.file_dir, **kwargs)
            converter.convert()
            self.document.files.extend(converter.images)
            self.document.conversion_duration += converter.conversion_duration


