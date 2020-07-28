#!/usr/bin/env python

from pdf_conversion.documents.document import Document
from pdf_conversion.converters.pdf_conversion import PDFConversion
from pdf_conversion.documents.file_extensions import SupportedDocTypes

source_pdf = "../../data/pdfs/ddmdp.pdf"
image_dir = "../../data/tiffs/pdf2tiff"

pdf = Document(file_spec=source_pdf, conversion_dir=image_dir)
PDFConversion(pdf).convert(doc_format=SupportedDocTypes.WEBP, lossless=False, dpi=100)

print(f"LIST OF TIFFs:\n{pdf.tiff}")
print(f"LIST OF WEBPs:\n{pdf.webp}")
print(f"DURATION: {pdf.conversion_duration:0.4f} seconds")

print(f"EXISTING DOC FORMATS: {pdf.get_format_types()}")
