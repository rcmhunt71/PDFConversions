import typing


class BaseImageFormatConverter:

    IMAGE_FORMAT = None
    IMAGE_EXTENSION = None
    DEFAULT_DPI = 200
    DEFAULT_THREADS = 1

    def __init__(self, src_file_spec: str, output_file: str = None, dpi: int = 0, threads: int = 0,
                 output_folder: int = '.', extension: int = None) -> None:
        """
        Init - Super() does most work, but needed to add class name, which is used when throwing exceptions.

        :param src_file_spec: File path and file name of the source file.
        :param output_file: Base filename for output image file names.
        :param dpi: Dots-per-inch - Translates into clarity/resolution of the generated image.
        :param threads: Number of processes processing the source image
        :param output_folder: File path for output image file names.
        :param extension: Output file extension

        """
        self.src_file_spec = src_file_spec
        self.output_file = output_file
        self.output_folder = output_folder
        self.dpi = dpi if dpi > 0 else self.DEFAULT_DPI
        self.threads = threads if threads > 0 else self.DEFAULT_THREADS
        self.fmt = self.IMAGE_FORMAT
        self.extension = extension or self.IMAGE_EXTENSION

        # If the format or extension is not provide, do not continue.
        if self.fmt is None or self.extension is None:
            raise Exception(f"{self.__class__.__name__}: Image format or extension is not set.")

        # Used for tracking the time required to convert the pdf to image.
        self.conversion_duration = 0

        # Used for providing which class through an exception.
        self.images = []

    def convert(self) -> typing.NoReturn:
        raise NotImplementedError
