from enum import Enum


class SupportedDocTypes(Enum):
    PDF: str = 'pdf'
    WEBP: str = 'webp'
    TIFF: str = 'tif'