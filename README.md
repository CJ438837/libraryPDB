# libraryPDB

**libraryPDB** is a lightweight Python library for searching, downloading, parsing, cleaning and analyzing protein structures from the Protein Data Bank (PDB).

The library is designed for **large-scale bioinformatics analyses**, with a strong focus on:
- transparency
- reproducibility
- dependency-free workflows
- coarse-grained, interpretable structural descriptors

Unlike full-featured molecular modeling toolkits, `libraryPDB` deliberately avoids heavy object models and external dependencies, making it suitable for **high-throughput structural screening** and **exploratory data analysis**.

---

## Key features

- 🔍 Programmatic search and download of PDB structures (RCSB PDB Search v2 API)
- 🧹 Lightweight PDB cleaning and normalization
- 🧬 Simple PDB parsing without external parsers
- 📐 Cα-based structural descriptors
- ✅ Structural integrity and quality checks
- 📊 Single-call structure summary for large datasets
- 🚀 Designed for batch processing and big data analysis

---

## Installation

### From GitHub (current version)

```bash
pip install git+https://github.com/CJ438837/libraryPDB.git
```

After installation:

```python
import libraryPDB
```

---

## Design philosophy

- No heavy object-oriented models
- No external bioinformatics dependencies
- Direct manipulation of standard PDB text files
- Explicit and reproducible heuristics
- Functional, script-friendly API
- Suitable for thousands of structures

This library is **not** intended to replace tools such as PyMOL, MDTraj, or Biopython, but to provide a **fast and transparent first-pass structural analysis toolkit**.

---

## PDB search and download

`libraryPDB` provides simple wrappers around the official **RCSB PDB Search v2 REST API**.

### Metadata-based search

```python
from libraryPDB import advanced_search_and_download_pdb

pdb_files = advanced_search_and_download_pdb(
    save_dir="pdb_kinases",
    keywords=["kinase"],
    organisms=["Homo sapiens"],
    methods=["X-RAY DIFFRACTION"],
    max_results=100
)

print(len(pdb_files))
```

---

## PDB parsing and basic handling

All parsing functions operate **directly on PDB files** and return simple Python data structures.

### Parse atoms

```python
from libraryPDB import parse_atoms

atoms = parse_atoms("protein.pdb")
print(atoms[0])
```

---

## High-level structure summary

```python
from libraryPDB import pdb_summary

summary = pdb_summary("protein.pdb")
```

---

## Typical applications

- Large-scale PDB dataset screening
- Structural diversity analysis
- Dataset curation and quality control
- Feature extraction for statistics or machine learning
- Rapid characterization of predicted structures (e.g. AlphaFold)

---

## License

MIT License
