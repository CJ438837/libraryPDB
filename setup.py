from setuptools import setup, find_packages

setup(
    name="libraryPDB",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    license="MIT",
    author="Cédric Jadot",
    author_email="cedricjadot@msn.com",
    description="Lightweight Python library for large-scale PDB structural analysis",
    url="https://github.com/CJ438837/libraryPDB",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
