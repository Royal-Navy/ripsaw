import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ripsaw",
    version="0.0.1",
    author="975523J",
    author_email="NAVYMWC-FOASUWBDATSCI@mod.gov.uk",
    description="An optimisation tool for external programs that use text based input and output.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/maritime-warfare-centre/ripsaw",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)