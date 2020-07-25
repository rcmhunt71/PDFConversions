#!/usr/bin/env python

from document import Document
from pdf_conversion import PDFConversion
from file_extensions import SupportedDocTypes

source_pdf = './pdfs/ddmdp.pdf'
image_dir = "./tiffs/pdf2tiff"

pdf = Document(source_pdf, conversion_dir=image_dir)
PDFConversion(pdf).convert(SupportedDocTypes.WEBP, lossless=False)

print(f"LIST OF TIFFs:\n{pdf.tiffs}")
print(f"LIST OF WEBPs:\n{pdf.webps}")
print(f"DURATION: {pdf.conversion_duration:0.4f} seconds")

print(f"EXISTING DOC TYPES: {pdf.get_image_types()}")
