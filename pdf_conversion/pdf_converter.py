#!/usr/bin/env python

import sys

from pdf_conversion.config.cli import CommandLine
from pdf_conversion.converters.pdf_conversion import PDFConversion
from pdf_conversion.documents.document_info import DocumentInfo

source_pdf = "../../data/pdfs/ddmdp.pdf"
image_dir = "../../data/tiffs/pdf2tiff"

args = CommandLine().args

print(f"DPI: {args.dpi}  Quality: {args.quality}  Convert To: {args.doc_type.value}")
pdf = DocumentInfo(file_spec=source_pdf, conversion_dir=image_dir)
PDFConversion(pdf).convert(doc_format=args.doc_type, lossless=True, dpi=args.dpi, quality=args.quality)

print(f"LIST OF TIFFs:\n{pdf.tiff}")
print(f"LIST OF WEBPs:\n{pdf.webp}")
print(f"DURATION: {pdf.conversion_duration:0.4f} seconds")

print(f"EXISTING DOC FORMATS: {pdf.get_format_types()}")
