import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdf_conversion",
    version="0.0.1",
    author="rhunt",
    author_email="robert.hunt1@fiserv.com",
    description="Utility for converting PDFs to various image formats (TIFF, webp)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    install_requires=['pdf2image', 'Pillow', 'PyYaml'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
