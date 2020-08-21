import os
from time import perf_counter
import typing

import pdf2image
import pdf2image.exceptions as pdf_exc

from pdf_conversion.converters.image_converter import IImageFormatConverter
from pdf_conversion.documents.file_extensions import SupportedDocTypes


class PdfToTiff(IImageFormatConverter):
    """
    PDF to TIFF conversion, using the 'pdf2image' python implementation.
    """
    IMAGE_FORMAT = 'tiff'
    IMAGE_EXTENSION = SupportedDocTypes.TIFF.value
    DEFAULT_DPI = 200
    DEFAULT_THREADS = 4

    def __init__(self, src_file_spec: str, output_file: typing.Optional[str] = None, dpi: typing.Optional[int] = 0,
                 threads: typing.Optional[int] = 0, output_folder: typing.Optional[str] = '.',
                 extension: typing.Optional[int] = None, defaults: typing.Optional[dict] = None, **kwargs):

        super().__init__(
            src_file_spec=src_file_spec, output_file=output_file, output_folder=output_folder,
            threads=threads, extension=extension, dpi=dpi)

        defaults = defaults or {}
        if self.dpi < 1:
            self.dpi = defaults.get('dpi', self.DEFAULT_DPI)
        if self.threads < 1:
            self.threads = defaults.get('threads', self.DEFAULT_THREADS)

    def convert(self) -> "PdfToTiff":
        """
        Convert the PDF to tiff image.

        :return: self (allows chaining of methods, since the methods do not return any additional info).

        """
        if os.path.exists(self.src_file_spec):

            # filename = self.src_file_spec.split(os.path.sep)[-1].split('.')[0]
            # outfile_generator = (filename for _ in range(1000))
            start_conversion = perf_counter()

            # Actual pdf2image call
            try:
                self.images = pdf2image.convert_from_path(
                    self.src_file_spec,
                    dpi=self.dpi,
                    fmt=self.fmt,
                    thread_count=self.threads,
                    # output_file=outfile_generator,
                    output_folder=self.output_folder,
                    paths_only=True,
                )

            except (pdf_exc.PDFInfoNotInstalledError, pdf_exc.PDFPageCountError, pdf_exc.PDFSyntaxError) as exc:
                print(f"ERROR: ({exc.__class__.__name__}): {exc}")

            except pdf_exc.PopplerNotInstalledError as exc:
                print(f"ERROR: ({exc.__class__.__name__}): {exc}")

            else:
                # Measure time to convert the PDF to image files.
                self.conversion_duration = perf_counter() - start_conversion
                print(f"{__class__.__name__}: Conversion took: {self.conversion_duration:0.6f} seconds.")
                print(f"{__class__.__name__}: Num images: {len(self.images)}")

        # Specified PDF was not found.
        else:
            print(f"Unable to find '{self.src_file_spec}'")

        return self
