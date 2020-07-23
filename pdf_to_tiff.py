#!/usr/bin/env python
import locale
import os
from time import perf_counter

import ghostscript
import pdf2image
import pdf2image.exceptions as pdf_exc


class BasePDFConversion:
    """
    This is a simple base class, designed with the purpose of being able to compare different pdf-to-<image>
    implementation - by creating a common process for invocation. This would not be needed in a production
    implementation.
    """

    IMAGE_FORMAT = None     # Specify the expected/default format.
    IMAGE_EXTENSION = None  # Specify the expected/default file extension.

    def __init__(self, pdf_file_spec, output_file=None, dpi=200, threads=5, output_folder='.', extension=None):
        """
        Instantiate the class.

        :param pdf_file_spec: File path and file name of the source PDF file.
        :param output_file: Base filename for output image file names.
        :param dpi: Dots-per-inch - Translates into clarity/resolution of the generated image.
        :param threads: Number of processes processing the PDF (more threads = can be faster overall, but adds overhead)
        :param output_folder: File path for output image file names.
        :param extension: Output file extension

        """
        self.pdf_file_spec = pdf_file_spec
        self.output_file = output_file
        self.output_folder = output_folder
        self.dpi = dpi
        self.fmt = self.IMAGE_FORMAT
        self.extension = extension or self.IMAGE_EXTENSION
        self.threads = threads

        # If the format or extension is not provide, do not continue.
        if self.fmt is None or self.extension is None:
            raise Exception("BasePDFConversion: Image format or extension is not set.")

        # Used for tracking the time required to convert the pdf to image.
        self.timing = 0

        # Used for providing which class through an exception.
        self.name = __class__.__name__

    def convert_to_image(self):
        """
        Virtual definition for creating an image. Each child class should have a tool-specific implementation.
        :return:
        """
        raise NotImplementedError


class PDFtoTiff(BasePDFConversion):
    """
    PDF to TIFF conversion, using the 'pdf2image' python implementation.
    """
    IMAGE_FORMAT = 'tiff'
    IMAGE_EXTENSION = "tif"

    def __init__(self, pdf_file_spec, output_file=None, dpi=200, threads=5, output_folder='.', extension=None):
        """
        Init - Super() does most work, but needed to add class name, which is used when throwing exceptions.

        :param pdf_file_spec: File path and file name of the source PDF file.
        :param output_file: Base filename for output image file names.
        :param dpi: Dots-per-inch - Translates into clarity/resolution of the generated image.
        :param threads: Number of processes processing the PDF (more threads = can be faster overall, but adds overhead)
        :param output_folder: File path for output image file names.
        :param extension: Output file extension

        """
        super().__init__(
            pdf_file_spec, output_file=output_file, dpi=dpi, threads=threads, output_folder=output_folder,
            extension=extension)
        self.name = __class__.__name__

    def convert_to_image(self):
        """
        Convert the PDF to tiff image.

        :return: self (allows chaining of methods, since the methods do not return any additional info).

        """

        # If the PDF file is found...
        if os.path.exists(self.pdf_file_spec):

            start = perf_counter()

            # Actual pdf2image call
            try:
                pdf2image.convert_from_path(
                    self.pdf_file_spec,
                    dpi=self.dpi,
                    fmt=self.fmt,
                    thread_count=self.threads,
                    output_file=f'{self.output_file}.{self.extension}',
                    output_folder=self.output_folder,
                )

            except (pdf_exc.PDFInfoNotInstalledError, pdf_exc.PDFPageCountError, pdf_exc.PDFSyntaxError) as exc:
                return f"ERROR: ({exc.__class__.__name__}): {exc}"

            except pdf_exc.PopplerNotInstalledError as exc:
                return f"ERROR: {exc}"

            # Measure time to convert the PDF to image files.
            self.timing = perf_counter() - start
            print(f"{self.name}: Conversion took: {self.timing:0.6f} seconds.")

        # Specified PDF was not found.
        else:
            print(f"Unable to find '{self.pdf_file_spec}'")

        return self


class PDFtoJpg(PDFtoTiff):
    """
    PDF to Jpg conversion, using the 'pdf2image' python implementation.
    """
    IMAGE_FORMAT = 'jpg'
    IMAGE_EXTENSION = 'jpg'


class PDFtoPng(PDFtoTiff):
    """
    PDF to png conversion, using the 'pdf2image' python implementation.
    """
    IMAGE_FORMAT = 'png'
    IMAGE_EXTENSION = 'png'


class GhostscriptPDF2Tiff(BasePDFConversion):
    """
    PDF to TIFF conversion, using the 'GhostScript' shared object implementation.
    """
    IMAGE_FORMAT = 'tiff24nc'
    IMAGE_EXTENSION = 'tif'

    def __init__(self, pdf_file_spec, output_file=None, dpi=200, threads=5, output_folder='.', extension=None):
        """
        Init - Super() does most work, but needed to add class name, which is used when throwing exceptions.

        :param pdf_file_spec: File path and file name of the source PDF file.
        :param output_file: Base filename for output image file names.
        :param dpi: Dots-per-inch - Translates into clarity/resolution of the generated image.
        :param threads: Number of processes processing the PDF (more threads = can be faster overall, but adds overhead)
        :param output_folder: File path for output image file names.
        :param extension: Output file extension

        """
        super().__init__(
            pdf_file_spec, output_file=output_file, dpi=dpi, threads=threads, output_folder=output_folder,
            extension=extension)
        self.name = __class__.__name__

    def convert_to_image(self):
        """
        Convert the PDF to tiff image.

        :return: self (allows chaining of methods, since the methods do not return any additional info).

        """

        # If the PDF file is found...
        if os.path.exists(self.pdf_file_spec):
            start = perf_counter()
            args = [
                "pdf2tiff",
                "-dNOPAUSE",
                "-dSAFER",
                "-dBATCH",
                f"-dNumRenderingThreads={self.threads}",
                f"-q",
                f"-sDEVICE={self.IMAGE_FORMAT}",
                f"-r{self.dpi}",
                f"-sOutputFile={os.path.abspath(f'{self.output_file}-%00d.{self.extension}')}",
                f"{self.pdf_file_spec}",
            ]
            encoding = locale.getpreferredencoding()
            args = [a.encode(encoding) for a in args]

            # Convert the PDF to the TIFF (Need to clean up instance after execution,
            # to allow conversion of additional documents)
            try:
                gs_apis = ghostscript.Ghostscript(*args)
                gs_apis.exit()
                ghostscript.cleanup()

            except Exception as exc:
                print(f"\tERROR ({self.name}): Exception: {exc}")

            # Measure time to convert the PDF to image files.
            self.timing = perf_counter() - start
            print(f"{self.name}: Conversion took: {self.timing:0.4f} seconds.")

        # Specified PDF was not found.
        else:
            print(f"{self.name}: Unable to find '{self.pdf_file_spec}'")

        return self


if __name__ == '__main__':
    " TESTING ROUTINE - executed as this script"

    output_dir = "tiffs"  # Base Relative Directory for storing resulting images
    big_pdf = True        # Which PDF should be tested (6 pages vs 25 pages)
    num_threads = 5       # Number of threads to use in conversion process
    iterations = 1        # Number of test iterations to build sample

    stats = {}            # Store timing results (k: conversion_process, v: timings)

    # Determine which PDF (absolute path) to use, based on big_pdf boolean
    pdf_file = "./pdfs/ddmdp.pdf" if big_pdf else "./pdfs/lflm.pdf"
    pdf_file_spec = os.path.abspath(pdf_file)

    # Mapping algorithm type to concrete class
    sub_path_mapping = {"gs": GhostscriptPDF2Tiff, "pdf2tiff": PDFtoTiff}

    # For each algorithm, convert the PDF 'iteration' times and record the conversions times.
    for sub_path, conversion_class in sub_path_mapping.items():

        # Determine the output file spec
        outfile = os.path.abspath(os.path.sep.join(
            [output_dir, sub_path, f"{pdf_file.split(os.path.sep)[-1].split('.')[0]}"]))
        print(f"\nINPUT FILE:  {pdf_file}\nOUTPUT DIR: {outfile}.*\nLarge PDF? {big_pdf}\nThreads: {num_threads}")

        # Initialize the algorithm conversion time list.
        stats[sub_path] = []

        # Execute the conversion and record the time
        for _ in range(iterations):
            pdf_converter = conversion_class(pdf_file_spec, output_file=outfile, threads=num_threads)
            stats[sub_path].append(pdf_converter.convert_to_image().timing)

    # Determine and print the stats (Min, Max, Avg, Multiplier change)
    avgs = []
    for key, data in stats.items():
        avg = sum(data) / len(data)
        print(f"{key}:\n"
              f"\tIterations: {len(data)}\n"
              f"\tAvg: {avg:0.4f} sec\n"
              f"\tMin: {min(data):0.4f} sec\n"
              f"\tMax: {max(data):0.4f} sec\n")
        avgs.append(avg)
    print(f"There is a factor of {avgs[0]/avgs[1]:0.2f} difference based on the average.")
