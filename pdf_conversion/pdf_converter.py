#!/usr/bin/env python

from pdf_conversion.config.cli import CommandLine
from pdf_conversion.converters.pdf_conversion import PDFConversion
from pdf_conversion.documents.document_info import DocumentInfo

source_pdf = "../../data/pdfs/ddmdp.pdf"
image_dir = "../../data/tiffs/pdf2tiff"


cli = CommandLine()
cli.print_args()

pdf = DocumentInfo(file_spec=source_pdf, conversion_dir=image_dir)
PDFConversion(pdf).convert(doc_format=cli.args.doc_format, lossless=cli.args.lossless,
                           dpi=cli.args.dpi, quality=cli.args.quality)
print(pdf.document_status())
