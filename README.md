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

🔍 PDBsearch_utils — Advanced structure retrieval from the PDB

This module provides high-level utilities to query the RCSB Protein Data Bank (PDB) and automatically download structure files (.pdb) in a robust, reproducible, and scriptable manner.
It is designed for large-scale bioinformatics pipelines, dataset construction, and method benchmarking.

All searches rely on the official RCSB Search API v2 and gracefully handle missing or deprecated entries.

🔎 advanced_search_and_download_pdb

Perform an advanced multi-criteria search on the PDB and download matching structures.

This function allows combining organism, experimental method, and text-based keywords into a single query.
It is particularly useful for building curated structural datasets (e.g. human kinases solved by X-ray crystallography).

Key features

Logical combination of multiple biological and experimental criteria

Automatic pagination and batch downloading

Skips missing or obsolete PDB entries without interrupting execution

Fully reproducible dataset construction

Typical use cases

Building a structural benchmark dataset

Downloading all structures for a protein family

Reproducing datasets used in publications

Automated updates of local PDB libraries

Example

```python 
from libraryPDB import advanced_search_and_download_pdb

pdb_files = advanced_search_and_download_pdb(
    save_dir="data/pdb/kinases",
    organisms=["Homo sapiens"],
    methods=["X-RAY DIFFRACTION"],
    keywords=["kinase"],
    max_results=200
)
```

Notes

At least one search criterion must be provided.

Searches are performed using logical AND between groups and OR within each group.

The function returns a list of downloaded PDB file paths.

🧬 search_by_sequence_and_download_pdb

Search the PDB by protein sequence similarity and download corresponding structures.

This function leverages the RCSB sequence search service to retrieve structures that match a given amino acid sequence.
It is ideal when no PDB identifier is known a priori.

Key features

Sequence-based structural discovery

Automatic handling of pagination

Safe downloading with error handling

Suitable for homolog search and structure coverage analysis

Typical use cases

Finding all structures related to a protein of interest

Exploring structural diversity of homologous proteins

Building datasets from novel or uncharacterized sequences

Structural annotation pipelines

Example
```python 
from libraryPDB import search_by_sequence_and_download_pdb

sequence = "MGSSHHHHHHSSGLVPRGSHM..."  # protein sequence
pdb_files = search_by_sequence_and_download_pdb(
    sequence=sequence,
    save_dir="data/pdb/sequence_hits",
    max_results=100
)

```

Notes

The input sequence must be provided as a raw amino acid string.

Returned structures may correspond to different organisms or constructs.

The function ignores unavailable or withdrawn PDB entries.

📌 Methodological considerations

These functions are designed to support:

Reproducible bioinformatics workflows

Large-scale structural analyses

Dataset generation for statistical or comparative studies

They intentionally avoid GUI interaction and manual curation steps, favoring automation, traceability, and scalability.


🧪 PDBio_utils — Low-level PDB file manipulation utilities

This module provides lightweight, dependency-free utilities for cleaning, standardizing, and preprocessing PDB files at the text level.

Unlike full structural parsers, these functions operate directly on PDB records (ATOM / HETATM) and are designed to be:

Fast

Deterministic

Easily composable in pipelines

Safe for large-scale dataset processing

They are especially useful before descriptor computation, statistical analysis, or machine-learning–free workflows.

🔄 normalize_chain_ids

Normalize chain identifiers to a continuous alphabetical range (A, B, C, ...).

This function ensures that:

Chain IDs are consistent across structures

Non-standard or missing chain identifiers are mapped deterministically

Downstream tools expecting standard chain labels behave correctly

Typical use cases

Dataset harmonization

Preparing structures for batch analysis

Removing inconsistencies introduced by experimental constructs

Example
```python 
from libraryPDB import normalize_chain_ids

normalize_chain_ids("input.pdb", "normalized_chains.pdb")

```

🔢 reindex_residues

Reindex residues to a continuous numbering starting at 1.

This function removes:

Gaps

Insertions

Non-standard residue numbering

while preserving residue order within each chain.

Why this matters

Simplifies residue-wise comparisons

Avoids indexing conflicts in statistical analyses

Facilitates descriptor computation and alignment-free analyses

Typical use cases

Structural dataset standardization

Preparing inputs for custom bioinformatics tools

Ensuring reproducibility across PDB versions

Example
```python 
from libraryPDB import reindex_residues

reindex_residues("input.pdb", "reindexed.pdb")

```

📐 center_structure

Translate the structure so that its Cα centroid lies at the origin (0, 0, 0).

The centering is computed using only Cα atoms, ensuring robustness to:

Ligands

Solvent

Missing side chains

If no Cα atoms are found, the structure is written unchanged.

Typical use cases

Structural comparison

Shape-based descriptors

Visualization normalization

Coordinate-invariant statistical analyses

Example
```python 
from libraryPDB import center_structure

center_structure("input.pdb", "centered.pdb")
```

🧩 Internal helper functions

These internal functions are not intended for direct user interaction but form the backbone of the module:

_parse_atom_lines
Extracts all ATOM and HETATM records from a PDB file.

_write_pdb_lines
Writes PDB-formatted lines to disk while preserving formatting.

They ensure consistent parsing and output formatting across all I/O utilities.

📌 Design philosophy

PDBio_utils follows a minimalist design:

No external dependencies

No structural assumptions beyond the PDB format

Full compatibility with large-scale automated workflows

This makes it ideal for:

High-throughput bioinformatics pipelines

Reproducible research

Dataset curation prior to statistical analysis


🧬 PDBparser — Lightweight PDB parsing and structural filtering

This module provides a minimal, transparent, and dependency-free PDB parser, designed for controlled bioinformatics workflows.

Instead of relying on complex object hierarchies, PDBparser exposes plain Python data structures (lists and dictionaries), making it:

Easy to understand

Easy to debug

Easy to integrate into custom pipelines

Ideal for educational and research-oriented use

📖 parse_atoms

Parse a PDB file and return a list of atom dictionaries.

Each atom is represented as a simple Python dictionary containing:

Atom name

Residue name

Chain ID

Residue index

Cartesian coordinates

Chemical element

Record type (ATOM or HETATM)

Returned structure

```python 
{
  "line_type": "ATOM",
  "atom_name": "CA",
  "res_name": "ALA",
  "chain": "A",
  "res_id": 42,
  "coords": (x, y, z),
  "element": "C"
}

##Example

from libraryPDB import parse_atoms

atoms = parse_atoms("protein.pdb")
```

🔗 get_chains

Return the sorted list of chain identifiers present in the structure.

Typical use cases

Detect multi-chain assemblies

Filter monomeric structures

Select the principal biological chain

Example
```python 
from libraryPDB import get_chains

chains = get_chains("protein.pdb")

```
🧱 get_residues

Return the list of residues as (residue_name, residue_id) tuples.

Optionally, restrict extraction to a single chain.

Example
```python 
from libraryPDB import get_residues

residues = get_residues("protein.pdb", chain="A")

```
📍 get_ca_coords

Extract the Cartesian coordinates of Cα atoms only, optionally restricted to a single chain.

This function is optimized for:

Structural descriptors

Distance-based analyses

Shape and topology metrics

Example
```python 
from libraryPDB import get_ca_coords

ca_coords = get_ca_coords("protein.pdb", chain="A")

```

🔧 Structural transformation utilities

These functions modify the structure by filtering atoms while preserving valid PDB formatting.

🧹 remove_ligands

Remove all HETATM records and keep protein atoms only.

Use cases

Ligand-free structural comparison

Protein-centric descriptor computation

Dataset standardization

```python 
from libraryPDB import remove_ligands

remove_ligands("input.pdb", "protein_only.pdb")
```

🔒 keep_only_chain

Extract a single chain from a multi-chain PDB file.

Use cases

Biological monomer isolation

Removing crystallographic artifacts

Consistent dataset generation

```python 
from libraryPDB import keep_only_chain

keep_only_chain("input.pdb", chain="A", out_file="chain_A.pdb")
```

🎯 keep_only_ca

Keep only Cα atoms in the structure.

This dramatically reduces structural complexity while preserving the protein backbone geometry.

Use cases

Coarse-grained analyses

Radius of gyration and compactness

Fast large-scale statistics

```python 
from libraryPDB import keep_only_ca

keep_only_ca("input.pdb", "ca_only.pdb")
```

📝 write_pdb

Write a list of atom dictionaries back to a valid PDB file.

This function ensures:

Proper column alignment

Continuous atom numbering

Compatibility with common visualization tools

It is used internally by all transformation functions.

📌 Design philosophy

PDBparser intentionally avoids:

Heavy abstractions

Hidden heuristics

External dependencies

In favor of:

Explicit control

Predictable behavior

Reproducibility

This makes it especially suitable for:

Dataset curation

Statistical structural biology

Method development and benchmarking

📊 PDBdescriptors — Structure-level protein descriptors

This module computes lightweight, interpretable structural descriptors directly from PDB files.

All descriptors are:

Cα-based (coarse-grained, robust, fast)

Dependency-free

Designed for large-scale structural statistics

Resistant to malformed or partially corrupted PDB files

The goal is not atomic precision, but comparability and robustness across hundreds to thousands of structures.

🧱 Core design

Descriptors are computed using only:

ATOM records

Cα atoms

Spatial geometry

This makes the module ideal for:

Structural diversity analysis

Family-wide comparison (e.g. kinases, GPCRs, enzymes)

Dataset quality control

Bioinformatics benchmarking

🔢 Basic size descriptors
num_residues

Return the number of residues based on Cα atoms.
```python 
from libraryPDB import num_residues

n_res = num_residues("protein.pdb")
```

num_atoms

Return the total number of ATOM records.
```python 
from libraryPDB import num_atoms

n_atoms = num_atoms("protein.pdb")
```

🧬 Amino acid composition
aa_composition

Return the amino acid composition as fractions, based on Cα atoms.
```python 
from libraryPDB import aa_composition

composition = aa_composition("protein.pdb")
```

glycine_ratio

Return the fraction of glycine residues.
```python 
from libraryPDB import glycine_ratio
```

hydrophobic_ratio

Return the fraction of hydrophobic residues
(ALA, VAL, ILE, LEU, MET, PHE, TRP, PRO).
```python 
from libraryPDB import hydrophobic_ratio
```

📐 Global shape descriptors
radius_of_gyration

Compute the radius of gyration (Rg) based on Cα atoms.

This descriptor captures the global size and spread of the structure.

```python 
from libraryPDB import radius_of_gyration
```

max_ca_distance

Return the maximum pairwise Cα–Cα distance.

This approximates the largest spatial extent of the protein.

```python 
from libraryPDB import max_ca_distance
```

🧩 Structural completeness
missing_residue_ratio

Estimate the fraction of missing residues based on residue index gaps.

This helps distinguish:

Full-length structures

Partially crystallized domains

Truncated constructs

```python 
from libraryPDB import missing_residue_ratio
```

🧠 Coarse secondary structure proxy
secondary_structure_ratio

Estimate local structural regularity using Cα–Cα distances.

A short distance between consecutive Cα atoms is interpreted as
a proxy for ordered secondary structure.

⚠️ This is a heuristic, not a DSSP replacement.

```python 
from libraryPDB import secondary_structure_ratio
```

🧊 Compactness and packing
compactness_index

Measure how compact the structure is relative to its size.

Lower values correspond to:

Tighter folding

More globular proteins

Higher values indicate:

Elongated or flexible structures

```python 
from libraryPDB import compactness_index
```

ca_density

Estimate the spatial density of Cα atoms inside the bounding box.

Useful for:

Fold comparison

Structural family clustering

Detecting unusual architectures

```python 
from libraryPDB import ca_density
```

🛡️ Robust parsing philosophy

All internal parsers are:

Tolerant to misaligned columns

Resistant to invalid residue numbers

Safe against corrupted coordinate fields

Malformed atoms are silently ignored, ensuring:

Pipeline continuity

Large-scale dataset processing without crashes

🧪 Scientific intent

PDBdescriptors is designed for:

Comparative structural bioinformatics

Exploratory data analysis

Statistical characterization of protein families

It is not intended to replace high-resolution structural tools,
but to enable fast, reproducible structural insights at scale.

🧪 PDBquality — Structural quality control utilities

This module provides lightweight quality checks for PDB files.

Rather than enforcing strict filtering rules, it exposes simple boolean and numeric indicators that allow users to:

Inspect dataset heterogeneity

Filter structures according to their needs

Document structural quality in large-scale studies

All checks operate directly on the PDB file and require no external dependencies.

🧬 Cα-only structures
has_ca_only

Return True if all ATOM records correspond to Cα atoms.

This is useful to:

Detect coarse-grained structures

Verify preprocessing pipelines

Ensure compatibility with Cα-based descriptors

```python 
from libraryPDB import has_ca_only

is_ca_only = has_ca_only("protein.pdb")
```

🧫 Multiple models detection
has_multiple_models

Return True if the PDB contains more than one MODEL record.

This typically indicates:

NMR ensembles

Multi-model structures

Such structures may require special handling before analysis.

```python 
from libraryPDB import has_multiple_models
```

🔀 Alternate conformations
has_altlocs

Return True if alternate atom locations (altLoc identifiers) are present.

Alternate conformations can:

Bias geometric descriptors

Indicate local disorder or ambiguity

```python 
from libraryPDB import has_altlocs
```

🧵 Chain count
num_chains

Return the number of distinct chains present in ATOM records.

This is particularly useful to:

Filter single-chain proteins

Detect complexes

Enforce monomer-only datasets
```python 
from libraryPDB import num_chains
```

📌 Typical use cases

PDBquality is commonly used to:

Exclude NMR ensembles

Remove multi-chain complexes

Detect structures with alternate conformations

Document dataset quality in publications

Example:
```python 
if (
    not has_multiple_models(pdb)
    and not has_altlocs(pdb)
    and num_chains(pdb) == 1
):
    keep_structure(pdb)
```

🧠 Design philosophy

Fast: single-pass file scans

Non-destructive: no file modification

Composable: quality metrics can be combined arbitrarily

Transparent: no hidden heuristics

The goal is to let the user decide what “high quality” means for their study.

📊 PDBsummary — Unified structural summary

The PDBsummary module provides a high-level, unified interface to extract meaningful information from a PDB structure in a single call.

It combines:

Structural quality indicators

Basic size descriptors

Amino acid composition

Geometrical and compactness metrics

This module is designed for large-scale bioinformatics pipelines, where thousands of structures must be characterized consistently and reproducibly.

🔍 pdb_summary
Purpose

Generate a comprehensive structural fingerprint for a single PDB file.

The output is a Python dictionary that can be:

Easily converted to a CSV or DataFrame

Used for clustering, statistics, or visualization

Integrated into downstream machine-learning or comparative analyses

Function signature
```python 
from libraryPDB import pdb_summary

summary = pdb_summary("protein.pdb")
```
🧪 Included metrics
🧬 Structural quality indicators

Derived from PDBquality:

has_ca_only
Structure contains only Cα atoms.

multiple_models
Multiple MODEL records are present (e.g. NMR structures).

has_altlocs
Alternate atom locations are present.

num_chains
Number of distinct protein chains in the structure.

These indicators allow users to filter or stratify datasets based on structural quality.

📏 Basic size descriptors

num_residues
Number of residues, estimated from Cα atoms.

num_atoms
Total number of ATOM records.

missing_residue_ratio
Fraction of missing residues inferred from discontinuities in residue numbering.

🧬 Amino acid composition

glycine_ratio
Fraction of glycine residues.

hydrophobic_ratio
Fraction of hydrophobic residues
(ALA, VAL, ILE, LEU, MET, PHE, TRP, PRO).

aa_composition
Dictionary mapping amino acid three-letter codes to their relative frequencies.

Amino acid composition is computed exclusively from Cα atoms, ensuring robustness to side-chain truncation and partial atom records.

📐 Geometrical and structural descriptors

radius_of_gyration
Global measure of protein size and compactness.

max_ca_distance
Maximum internal distance between any two Cα atoms.

secondary_structure_ratio
Heuristic indicator of local compactness based on consecutive Cα distances.

compactness_index
Size-normalized compaction metric derived from the radius of gyration.

ca_density
Spatial density of Cα atoms within the bounding volume of the structure.

These descriptors enable quantitative comparison of global protein folds across large structural datasets.

📦 Example output
```python 
{
  'has_ca_only': False,
  'multiple_models': False,
  'has_altlocs': False,
  'num_chains': 1,
  'num_residues': 285,
  'num_atoms': 2280,
  'missing_residue_ratio': 0.04,
  'glycine_ratio': 0.07,
  'hydrophobic_ratio': 0.38,
  'aa_composition': {...},
  'radius_of_gyration': 21.6,
  'max_ca_distance': 64.2,
  'secondary_structure_ratio': 0.71,
  'compactness_index': 1.92,
  'ca_density': 0.0041
}
```

🔁 Typical workflow

```python 
import pandas as pd
from libraryPDB import pdb_summary

summaries = []
for pdb in pdb_files:
    s = pdb_summary(pdb)
    s["file"] = pdb
    summaries.append(s)

df = pd.DataFrame(summaries)
```

This table can then be:

Analyzed statistically (R, Python)

Visualized (PCA, clustering)

Used to demonstrate structural diversity within a protein family

🧠 Design philosophy

One function → one structure

No external dependencies

Fully deterministic

Robust to incomplete or imperfect PDB files

PDBsummary intentionally favors interpretability and reproducibility over black-box metrics.

📌 Why this matters

For a bioinformatics-focused paper, PDBsummary:

Demonstrates the added value of libraryPDB

Enables reproducible large-scale structural analysis

Bridges raw PDB data and statistical interpretation
