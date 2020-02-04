"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages, setuptools
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
# from io import open

# here = path.abspath(path.dirname(__file__))

# # Get the long description from the README file
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='dicom_anonymizer',  # Required
    version='1.0.1',  # Required
    description='Program to anonymize dicom files with default and custom rules', # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)ls
    url='https://gitlab.kitware.io/kitware/DicomAnonymizer.git',  # Optional
    author='Guillaume Lemaitre, Edern Haumont, Laurenn Lam',  # Optional
    author_email='laurenn.lam@kitware.com',  # Optional

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python'
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords='dicom anonymizer medical',  # Optional

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=setuptools.find_packages(),  # Required

    # Define an executable calls dicom-anonymizer from a specific file
    entry_points={
        'console_scripts': [
            'dicom-anonymizer = dicomanonymizer.anonymizer:main'
        ]
    },

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['pydicom', 'tqdm'],  # Optional
)