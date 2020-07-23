#!/usr/bin/env python
import locale
import os
import pprint
from time import perf_counter

import ghostscript
import pdf2image
import pdf2image.exceptions as pdf_exc


class BasePDFConversion:
    image_format = None

    def __init__(self, pdf_file_spec, output_file=None, dpi=200, threads=5, output_folder='.', paths_only=True):
        self.pdf_file_spec = pdf_file_spec
        self.output_file = output_file
        self.output_folder = output_folder
        self.dpi = dpi
        self.fmt = self.image_format
        self.threads = threads
        self.paths_only = paths_only
        self.timing = 0
        self.name = __class__.__name__
        if self.image_format is None:
            raise Exception("BasePDFConversion: Image format is not set.")

    def convert_to_file(self):
        raise NotImplementedError


class PDFtoTiff(BasePDFConversion):
    image_format = 'tiff'

    def __init__(self, pdf_file_spec, output_file=None, dpi=200, threads=5, output_folder='.', paths_only=True):
        super().__init__(
            pdf_file_spec, output_file=output_file, dpi=dpi, threads=threads, output_folder=output_folder,
            paths_only=paths_only)
        self.name = __class__.__name__

    def convert_to_file(self):
        if os.path.exists(self.pdf_file_spec):
            start = perf_counter()
            try:
                pdf2image.convert_from_path(
                    self.pdf_file_spec,
                    dpi=self.dpi,
                    fmt=self.fmt,
                    thread_count=self.threads,
                    output_file=f'{self.output_file}.{self.image_format}',
                    output_folder=self.output_folder,
                    paths_only=self.paths_only,
                )
            except (pdf_exc.PDFInfoNotInstalledError, pdf_exc.PDFPageCountError, pdf_exc.PDFSyntaxError) as exc:
                return f"ERROR: ({exc.__class__.__name__}): {exc}"
            except pdf_exc.PopplerNotInstalledError as exc:
                return f"ERROR: {exc}"
            self.timing = perf_counter() - start
            print(f"{self.name}: Conversion took: {self.timing:0.6f} seconds.")
        else:
            print(f"Unable to find '{self.pdf_file_spec}'")
        return self


class PDFtoJpg(PDFtoTiff):
    image_format = 'jpg'


class PDFtoPng(PDFtoTiff):
    image_format = 'png'


class GhostscriptPDF2Tiff(BasePDFConversion):
    image_format = 'tiff24nc'

    def __init__(self, pdf_file_spec, output_file=None, dpi=200, threads=5, output_folder='.', paths_only=True):
        super().__init__(
            pdf_file_spec, output_file=output_file, dpi=dpi, threads=threads, output_folder=output_folder,
            paths_only=paths_only)
        self.name = __class__.__name__

    def convert_to_file(self):
        if os.path.exists(self.pdf_file_spec):
            start = perf_counter()
            args = [
                "pdf2tiff",
                "-dNOPAUSE",
                "-dSAFER",
                "-dBATCH",
                f"-dNumRenderingThreads={self.threads}",
                f"-q",
                f"-sDEVICE={self.image_format}",
                f"-r{self.dpi}",
                f"-sOutputFile={os.path.abspath(f'{self.output_file}-%00d.tif')}",
                f"{self.pdf_file_spec}",
            ]
            encoding = locale.getpreferredencoding()

            try:
                args = [a.encode(encoding) for a in args]
                gs_apis = ghostscript.Ghostscript(*args)
                gs_apis.exit()
                ghostscript.cleanup()

            except Exception as exc:
                print(f"\tERROR ({self.name}): Exception: {exc}")

            self.timing = perf_counter() - start
            print(f"{self.name}: Conversion took: {self.timing:0.4f} seconds.")

        else:
            print(f"{self.name}: Unable to find '{self.pdf_file_spec}'")

        return self


if __name__ == '__main__':
    output_dir = "tiffs"
    big_pdf = True
    num_threads = 5
    iterations = 1
    stats = {}
    pdf_file = "./pdfs/ddmdp.pdf" if big_pdf else "./pdfs/lflm.pdf"
    pdf_file_spec = os.path.abspath(pdf_file)
    sub_path_mapping = {"gs": GhostscriptPDF2Tiff, "pdf2tiff": PDFtoTiff}

    for sub_path, conversion_class in sub_path_mapping.items():
        outfile = os.path.abspath(os.path.sep.join(
            [output_dir, sub_path, f"{pdf_file.split(os.path.sep)[-1].split('.')[0]}"]))
        print(f"\nINPUT FILE:  {pdf_file}\nOUTPUT DIR: {outfile}.*\nLarge PDF? {big_pdf}\nThreads: {num_threads}")
        stats[sub_path] = []
        for _ in range(iterations):
            pdf_converter = conversion_class(pdf_file_spec, output_file=outfile, threads=num_threads)
            stats[sub_path].append(pdf_converter.convert_to_file().timing)

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
