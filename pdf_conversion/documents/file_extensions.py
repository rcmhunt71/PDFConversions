from enum import Enum


class SupportedDocTypes(Enum):
    PDF = 'pdf'
    WEBP = 'webp'
    TIFF = 'tif'
    NOT_DEFINED = None
