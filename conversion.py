import os

import pdf2image
import pdf2image.exceptions as pdf_exc


class PDF2Tiff:
    image_format = 'tiff'

    def __init__(self, pdf_file_spec, output_file=None, dpi=200, threads=3, output_folder='.', paths_only=True):
        self.pdf_file_spec = pdf_file_spec
        self.output_file = output_file
        self.output_folder = output_folder
        self.dpi = dpi
        self.fmt = self.image_format
        self.threads = threads
        self.paths_only = paths_only

    def convert_to_file(self):
        if os.path.exists(self.pdf_file_spec):
            try:
                return pdf2image.convert_from_path(
                    self.pdf_file_spec,
                    dpi=self.dpi,
                    fmt=self.fmt,
                    thread_count=self.threads,
                    output_file=self.output_file,
                    output_folder=self.output_folder,
                    paths_only=self.paths_only,
                )
            except (pdf_exc.PDFInfoNotInstalledError, pdf_exc.PDFPageCountError, pdf_exc.PDFSyntaxError) as exc:
                return f"RUT-ROH: ({exc.__class__.__name__}): {exc}"
            except pdf_exc.PopplerNotInstalledError as exc:
                return f"RUT-ROH: {exc}"
        else:
            return f"Unable to find '{self.pdf_file_spec}'"


class PDFtoJpg(PDF2Tiff):
    image_format = 'jpg'


class PDFtoPng(PDF2Tiff):
    image_format = 'png'


if __name__ == '__main__':
    big_pdf = False

    pdf = "DD_Mortgage Director_proposal.pdf" if big_pdf else "LeadingForward Leadership Model.pdf"
    outfile = f"{pdf.split('.')[0]}.{PDF2Tiff.image_format}"

    print(f"INPUT FILE:  {pdf}\nOUTPUT FILE: {outfile}\n")

    pdf_converter = PDF2Tiff(pdf, output_file=outfile)
    print(pdf_converter.convert_to_file())
