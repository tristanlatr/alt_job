#! /usr/bin/env python3

from setuptools import setup
import sys
if sys.version_info[0] < 3: 
    raise Exception("Sorry, you must use Python 3")
import pathlib


# The directory containing this file
HERE = pathlib.Path(__file__).parent

#Version of the project
version = {}
exec((HERE / "alt_job" / "__version__.py").read_text(encoding='utf-8'), version)

# The text of the README file
README = (HERE / "README.md").read_text(encoding='utf-8')

setup(
    name='alt_job',
    description="Atl Job scrapes a bunch of green/social/alternative websites to send digest of new job posting by email. Also generates an Excel file with job postings informations.",
    url='https://github.com/tristanlatr/alt_job',
    maintainer='tristanlatr',
    version=version['__version__'],
    packages=['alt_job','alt_job.scrapers'],
    install_requires=[
          'pyasn1', 'scrapy-user-agents', 'pdfplumber', 'requests', 'tqdm', 'scrapy', 'bs4', 'XlsxWriter'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    license='The MIT License',
    long_description=README,
    long_description_content_type="text/markdown"
)