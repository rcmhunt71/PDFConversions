#!/usr/bin/python

import os
import typing

from pdf_conversion.documents.file_extensions import SupportedDocTypes


class DocumentInfo:
    """
    Stores basic information about source PDF file, and all conversion info (type, time elapsed during the
    conversion process, resulting intermediary and final image locations)
    """
    def __init__(self, file_spec: str, conversion_dir: str = None):
        self.filespec = os.path.abspath(file_spec)
        self.file_dir = os.path.abspath(conversion_dir) or os.path.split(self.filespec)[0]
        self.filename = self.filespec.split(os.path.sep)[-1]
        self.doc_type = self.filename.split('.')[-1].lower()
        self.files = []
        self.conversion_duration = 0

    def get_format_types(self) -> typing.List[str]:
        """
        Get the list of formats the source exists: pdf, tif, webp, etc.

        :return: List of unique file format types

        """
        formats = list(set([filename.split('.')[-1] for filename in self.files]))
        formats.extend([self.filename.split('.')[-1]])
        return formats

    def _return_list_of_filespecs_of_file_format(self, file_format: SupportedDocTypes) -> typing.List[str]:
        """
        Return a list of all file specs matching the desired file format.

        :param file_format: The file format to list

        :return: List of files matching the file format (extension)

        """
        return [file_ for file_ in self.files if file_.lower().endswith(file_format.value.lower())]

    @property
    def tiff(self):
        """
        Return all file specs that are in the TIFF format.

        :return: List of file specs for TIFF images.

        """
        return self._return_list_of_filespecs_of_file_format(SupportedDocTypes.TIFF)

    @property
    def webp(self):
        """
        Return all file specs that are in the webp format.

        :return: List of file specs for webp images.

        """
        return self._return_list_of_filespecs_of_file_format(SupportedDocTypes.WEBP)
