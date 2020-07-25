#!/usr/bin/env python

import os
from time import perf_counter
import typing

from PIL import Image

from base_image_converter import BaseImageFormatConverter
from file_extensions import SupportedDocTypes

class TiffToWebp(BaseImageFormatConverter):
    IMAGE_FORMAT = SupportedDocTypes.WEBP.value
    IMAGE_EXTENSION = SupportedDocTypes.WEBP.value

    # DEFAULT QUALITY range: [0, 100]
    # If LOSSLESS, DEFAULT_QUALITY = 0 (quickest compression) to 100 (best compression)
    # If not LOSSLESS, DEFAULT_QUALITY = 0 (smallest size) to 100 = (largest size)
    # REFERENCE: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html?highlight=webp#webp
    LOSSLESS = True
    DEFAULT_QUALITY = 90

    def __init__(self, src_file_spec: str, output_file: str = None, dpi: int = 0, threads: int = 0,
                 output_folder: str = '.', extension: str = None, lossless: bool = None, quality: int = -1) -> None:
        """
        Init - Super() does most work, but needed to add class name, which is used when throwing exceptions.

        :param src_file_spec: File path and file name of the source file.
        :param output_file: Base filename for output image file names.
        :param dpi: Dots-per-inch - Translates into clarity/resolution of the generated image.
        :param threads: Number of processes processing the source image
        :param output_folder: File path for output image file names.
        :param extension: Output file extension
        :param lossless: (bool) - Do lossless conversion (more expensive, more accurate)
        :param quality: (int: 0 - 100) - Quality for non-lossless, compression for lossless.
              see class description for more detail.

        """
        super().__init__(src_file_spec=src_file_spec, output_file=output_file, output_folder=output_folder,
                         extension=extension, dpi=dpi, threads=threads)
        self.lossless = lossless if lossless is not None else self.LOSSLESS
        self.quality = quality if quality > -1 else self.DEFAULT_QUALITY

    def convert(self) -> "TiffToWebp":
        webp_filename = f"{os.path.split(self.src_file_spec)[-1].split('.')[0]}.{self.IMAGE_EXTENSION}"
        webp_filespec = os.path.sep.join([self.output_folder, webp_filename])
        try:
            start_time = perf_counter()
            with Image.open(self.src_file_spec) as IMAGE:
                IMAGE.save(webp_filespec, lossless=self.lossless, quality=self.quality)
            self.conversion_duration = perf_counter() - start_time
            print(f"{self.__class__.__name__}: "
                  f"Conversion to {self.IMAGE_FORMAT}: {self.conversion_duration:0.3f} seconds")
            print(f"{self.__class__.__name__}: "
                  f"LOSSLESS? {str(self.lossless)}    QUALITY: {self.quality}%")
        except OSError as exc:
            print(f"{self.__class__.__name__}: ERROR: Unable to convert '{self.src_file_spec}: {exc}")
        else:
            self.images.append(webp_filespec)
        return self


if __name__ == '__main__':
    file = '/home/rhunt/PycharmProjects/Pdf2Tiff/src/tiffs/pdf2tiff/d1be3efc-8974-4019-a7cc-132ff4d0d1c8-23.tif'

    converter = TiffToWebp(src_file_spec=file).convert()

    print(f"IMAGE: {converter.images}")
    print(f"DURATION: {converter.conversion_duration:0.4f} seconds")
    print(f"LOSSLESS? {str(converter.lossless)}")
    print(f"QUALITY: {str(converter.quality)}")
