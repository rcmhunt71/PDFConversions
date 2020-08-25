#!/usr/bin/env python

from pdf_conversion.config.cli import CommandLine
from pdf_conversion.config.defaults import DefaultValues
from pdf_conversion.converters.pdf_conversion import PDFConversion
from pdf_conversion.documents.document_info import DocumentInfo

source_pdf = "../../data/pdfs/ddmdp.pdf"
default_cfg = './defaults.cfg'

defaults = DefaultValues(filespec=default_cfg)
app_defaults = getattr(defaults, DefaultValues.APP_DEFAULTS)

cli = CommandLine(app_defaults)
cli.print_args()

pdf = DocumentInfo(file_spec=source_pdf, conversion_dir=cli.args.image_dir)

PDFConversion(document=pdf, defaults=defaults).convert(
    doc_format=cli.args.doc_format, lossless=cli.args.lossless, dpi=cli.args.dpi, quality=cli.args.quality,
    threads=cli.args.threads)

print(pdf.document_status())
