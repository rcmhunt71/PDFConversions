from abc import ABC, abstractmethod
import typing


class IImageFormatConverter(ABC):

    IMAGE_FORMAT = None
    IMAGE_EXTENSION = None

    def __init__(
            self, src_file_spec: str, output_file: typing.Optional[str] = None,
            output_folder: typing.Optional[str] = '.', extension: typing.Optional[int] = None, **kwargs) -> None:
        """
        :param src_file_spec: File path and file name of the source file.
        :param output_file: Base filename for output image file names.
        :param output_folder: File path for output image file names.
        :param extension: Output file extension
        :param kwargs: Any additional args for overloading child __init__()

        """
        self.src_file_spec = src_file_spec
        self.output_file = output_file
        self.output_folder = output_folder

        self.fmt = self.IMAGE_FORMAT
        self.extension = extension or self.IMAGE_EXTENSION

        # If the format or extension is not provided, do not continue.
        if self.fmt is None or self.extension is None:
            raise Exception(f"{self.__class__.__name__}: Image format or extension is not set.")

        # Used for tracking the time required to convert the pdf to image.
        self.conversion_duration = 0

        # Used for providing which class through an exception.
        self.images = []

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
