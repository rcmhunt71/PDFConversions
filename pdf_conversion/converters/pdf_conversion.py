import typing

from pdf_conversion.documents.document_info import DocumentInfo
from pdf_conversion.documents.file_extensions import SupportedDocTypes
from pdf_conversion.config.defaults import DefaultValues
from pdf_conversion.converters.pdf2tiff import PdfToTiff
from pdf_conversion.converters.tiff2webp import TiffToWebp


class NoTargetConversionType(Exception):
    def __str__(self):
        return "No target conversion format specified."


class PDFConversion:
    """
    Primary class for converting PDF to specified images. Contains basic logic for determining which conversion
    routines are needed, based on the extension provided.
    """

    def __init__(self, document: DocumentInfo, image_format: SupportedDocTypes = SupportedDocTypes.NOT_DEFINED,
                 defaults: typing.Optional[DefaultValues] = None) -> None:
        """
        :param document: Instantiated Document object (contains filespec, used for tracking conversion process)
        :param image_format: Convert image from PDF to specified format.
        :param defaults: A dictionary of defaults for each image type (optional)

        """
        self.document = document
        self.image_format = image_format
        self.defaults = defaults

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
        if doc_format is None or not isinstance(doc_format, SupportedDocTypes) or doc_format.value is None:
            raise NoTargetConversionType

        # If target format matches the current format; no op. (At this point, it must be defined doc type)
        if self.document.doc_type.lower() == doc_format.value:
            print(f"Target Format ('{doc_format.value}') matches the current document type. Nothing to do.")
            return self

        # For PDF to TIFF.
        if doc_format == SupportedDocTypes.TIFF:
            defaults_dict = getattr(self.defaults, DefaultValues.TIFF_DEFAULTS) if self.defaults is not None else {}
            self._convert_pdf_to_tiff(defaults_dict, **kwargs)

        # For PDF to webp format (with intermediate TIFF format)
        elif doc_format == SupportedDocTypes.WEBP:
            defaults_dict = getattr(self.defaults, DefaultValues.TIFF_DEFAULTS) if self.defaults is not None else {}
            self._convert_pdf_to_tiff(defaults_dict, **kwargs)

            defaults_dict = getattr(self.defaults, DefaultValues.WEBP_DEFAULTS) if self.defaults is not None else {}
            self._convert_tiff_to_webp(defaults_dict, **kwargs)

    def _convert_pdf_to_tiff(self, defaults: typing.Optional[dict] = None, **kwargs) -> typing.NoReturn:
        """
        Call PDF to TIFF libraries.

        :param defaults: a Dictionary of tiff specific defaults (See PdfToTiff class for DEFAULT_* parameters)
        :param kwargs: Additional args available to conversion process (beyond standard BaseClass args)
            * Currently no additional args defined.

        :return: None

        """
        converter = PdfToTiff(src_file_spec=self.document.filespec, output_folder=self.document.file_dir,
                              defaults=defaults, **kwargs)

        converter.convert()
        self._print_attribute_settings(converter)

        self.document.files.extend(converter.images)
        self.document.conversion_duration = converter.conversion_duration

    def _convert_tiff_to_webp(self, defaults: typing.Optional[dict] = None, **kwargs) -> typing.NoReturn:
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
            converter = TiffToWebp(
                src_file_spec=image, defaults=defaults, output_folder=self.document.file_dir, **kwargs)

            converter.convert()
            self._print_attribute_settings(converter)

            self.document.files.extend(converter.images)
            self.document.conversion_duration += converter.conversion_duration

    @staticmethod
    def _print_attribute_settings(target_obj: typing.Any) -> typing.NoReturn:
        """
        Prints all non-callable, non-capitalized, non-reserved attributes within the specified obj
        :param target_obj: Instantiated obj
        :return: None
        """
        for attribute in dir(target_obj):
            if (not attribute.startswith('_') and not callable(getattr(target_obj, attribute)) and
                    not attribute == attribute.upper()):
                print(f"{target_obj.IMAGE_FORMAT} attribute: {attribute} = {getattr(target_obj, attribute)}")
