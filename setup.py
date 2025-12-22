from setuptools import setup, find_packages

setup(
    name="libraryPDB",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "typing",
        "collections",
        "os",
        "math"
    ],
    python_requires='>=3.8',
    author="Cédric Jadot",
    description="Python library for manipulating and analyzing PDB files",
    url="https://github.com/cj438837/libraryPDB",  # si tu mets sur GitHub
)
