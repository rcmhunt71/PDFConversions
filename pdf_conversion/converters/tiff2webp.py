import os
from time import perf_counter
import typing

from PIL import Image

from pdf_conversion.converters.image_converter import IImageFormatConverter
from pdf_conversion.documents.file_extensions import SupportedDocTypes


class TiffToWebp(IImageFormatConverter):
    IMAGE_FORMAT = SupportedDocTypes.WEBP.value
    IMAGE_EXTENSION = SupportedDocTypes.WEBP.value

    # DEFAULT QUALITY range: [0, 100]
    # If LOSSLESS, DEFAULT_QUALITY = 0 (quickest compression) to 100 (best compression)
    # If not LOSSLESS, DEFAULT_QUALITY = 0 (smallest size) to 100 = (largest size)
    # REFERENCE: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html?highlight=webp#webp
    LOSSLESS = True
    DEFAULT_QUALITY = 90
    QUALITY_KW = 'quality'

    def __init__(
            self, src_file_spec: str, output_file: typing.Optional[str] = None, dpi: typing.Optional[int] = 0,
            threads: typing.Optional[int] = 0, output_folder: typing.Optional[str] = '.',
            extension: typing.Optional[str] = None, lossless: typing.Optional[bool] = None,
            quality: typing.Optional[int] = -1, defaults: typing.Optional[dict] = None, **kwargs) -> None:

        """
        Init - Super() does most of the work; this class's __init__() stores conversion specific options.

        :param src_file_spec: File path and file name of the source file.
        :param output_file: Base filename for output image file names.
        :param dpi: Dots-per-inch - Translates into clarity/resolution of the generated image.
        :param threads: Number of processes processing the source image
        :param output_folder: File path for output image file names.
        :param extension: Output file extension
        :param lossless: (bool) - Do lossless conversion (more expensive, more accurate)
        :param quality: (int: 0 - 100) - Quality for non-lossless, compression for lossless.
              see class description for more detail.
        :param kwargs: Any extra args (needed to support the ability to overload the base class __init___ in
               other subclasses)

        """
        super().__init__(src_file_spec=src_file_spec, output_file=output_file, output_folder=output_folder,
                         extension=extension, dpi=dpi, threads=threads)
        self.lossless = lossless if lossless is not None else self.LOSSLESS
        defaults = defaults or {}
        self.quality = kwargs.get(self.QUALITY_KW, -1)
        if quality < 0:
            self.quality = defaults.get(self.QUALITY_KW, self.DEFAULT_QUALITY)

    def convert(self) -> "TiffToWebp":
        """
        Convert the TIFF to webp image.

        :return: self (allows chaining of methods, since the methods do not return any additional info).

        """
        webp_filename = f"{os.path.split(self.src_file_spec)[-1].split('.')[0]}.{self.IMAGE_EXTENSION}"
        webp_filespec = os.path.sep.join([self.output_folder, webp_filename])

        try:
            start_time = perf_counter()
            with Image.open(self.src_file_spec) as IMAGE:
                IMAGE.save(webp_filespec, lossless=self.lossless, quality=self.quality)
            self.conversion_duration = perf_counter() - start_time
            print(f"\t{self.__class__.__name__}: "
                  f"Conversion to {self.IMAGE_FORMAT}: {self.conversion_duration:0.3f} seconds")
            print(f"\t{self.__class__.__name__}: "
                  f"LOSSLESS? {str(self.lossless)}    QUALITY: {self.quality}%")

        except OSError as exc:
            print(f"{self.__class__.__name__}: ERROR: Unable to convert '{self.src_file_spec}': {exc}")

        else:
            self.images.append(webp_filespec)

        return self
