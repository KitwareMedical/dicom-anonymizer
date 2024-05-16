"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name='dicom_anonymizer',  # Required
    version='1.0.12',  # Required
    author='Laurenn Lam',
    author_email='laurenn.lam@kitware.com',
    description="Program to anonymize dicom files with default and custom rules",
    url="https://github.com/KitwareMedical/dicom-anonymizer",
    project_urls={
        "Bug Tracker": "https://github.com/KitwareMedical/dicom-anonymizer/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python"
    ],
    keywords=["dicom", "anonymizer", "medical"],
    python_requires='>=3.6',

    packages=find_packages(),  # Required

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
    # https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
    install_requires=['pydicom', 'tqdm'],  # Optional

    extras_require={
        'dev': [
            "pytest",
            "bs4",
            "fire",
            "requests",
            "pre-commit",
            "ruff"
        ]
    }
)
