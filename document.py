#!/usr/bin/python

import os
import typing

from file_extensions import SupportedDocTypes

class Document:
    def __init__(self, file_spec: str, conversion_dir: str = None):
        self.filespec = os.path.abspath(file_spec)
        self.image_dir = os.path.abspath(conversion_dir) or os.path.split(self.filespec)[0]
        self.filename = self.filespec.split(os.path.sep)[-1]
        self.doc_type = self.filename.split('.')[-1].lower()
        self.images = []
        self.conversion_duration = 0

    def get_image_types(self) -> typing.List[str]:
        types = list(set([filename.split('.')[-1] for filename in self.images]))
        types.extend([self.filename.split('.')[-1]])
        return types

    def _return_list_of_images_of_type(self, image_type: str) -> typing.List[str]:
        return [image for image in self.images if image.lower().endswith(image_type.lower())]

    @property
    def tiffs(self):
        return self._return_list_of_images_of_type(SupportedDocTypes.TIFF.value)

    @property
    def webps(self):
        return self._return_list_of_images_of_type(SupportedDocTypes.WEBP.value)