from abc import ABC, abstractmethod
import typing

from pdf_conversion.config.defaults import DefaultValues


class IImageFormatConverter(ABC):

    IMAGE_FORMAT = None
    IMAGE_EXTENSION = None

    def __init__(
            self, src_file_spec: str, output_file: typing.Optional[str] = None, dpi: typing.Optional[int] = 0,
            threads: typing.Optional[int] = 0, output_folder: typing.Optional[str] = '.',
            extension: typing.Optional[int] = None, **kwargs) -> None:
        """
        :param src_file_spec: File path and file name of the source file.
        :param output_file: Base filename for output image file names.
        :param dpi: Dots-per-inch - Translates into clarity/resolution of the generated image.
        :param threads: Number of processes processing the source image
        :param output_folder: File path for output image file names.
        :param extension: Output file extension
        :param kwargs: Any additional args for overloading child __init__()

        """
        self.src_file_spec = src_file_spec
        self.output_file = output_file
        self.output_folder = output_folder

        self.dpi = dpi
        self.threads = threads
        self.fmt = self.IMAGE_FORMAT
        self.extension = extension or self.IMAGE_EXTENSION

        # If the format or extension is not provided, do not continue.
        if self.fmt is None or self.extension is None:
            raise Exception(f"{self.__class__.__name__}: Image format or extension is not set.")

        # Used for tracking the time required to convert the pdf to image.
        self.conversion_duration = 0

        # Used for providing which class through an exception.
        self.images = []

    # def _set_default(self, defaults: DefaultValues, attribute: str) -> typing.NoReturn:
    #     if defaults is None:
    #         return
    #
    #     image_default = getattr(defaults, defaults.TIFF_DEFAULTS).get(attribute, -1)
    #     app_default = getattr(defaults, defaults.APP_DEFAULTS).get(attribute, -1)
    #
    #     setattr(self, attribute, getattr(self, f"DEFAULT_{attribute.upper()}"))
    #     if image_default > 0:
    #         setattr(self, attribute, image_default)
    #     elif app_default > 0:
    #         setattr(self, attribute, app_default)

    @abstractmethod
    def convert(self) -> "IImageFormatConverter":
        """
        Implemented instance of this function should return the instance of the obj
        e.g. -

        def convert():
          <code>
          return self

        :return:
            self
        """
        pass
