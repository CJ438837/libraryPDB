"""
libraryPDB
==========

Lightweight Python library for large-scale analysis of PDB structures.
"""

# ---------------------------
# Core I/O utilities
# ---------------------------
from .PDBio_utils import (
    reindex_residues,
)

# ---------------------------
# Structural descriptors
# ---------------------------
from .PDBdescriptors import (
    num_residues,
    num_atoms,
    aa_composition,
    glycine_ratio,
    hydrophobic_ratio,
    radius_of_gyration,
    max_ca_distance,
    missing_residue_ratio,
    secondary_structure_ratio,
    compactness_index,
    ca_density,
)

# ---------------------------
# Quality checks
# ---------------------------
from .PDBquality import (
    has_ca_only,
    has_multiple_models,
    has_altlocs,
    num_chains,
)

# ---------------------------
# Summary
# ---------------------------
from .PDBsummary import (
    pdb_summary,
)

# ---------------------------
# Search & download
# ---------------------------
from .PDBsearch_utils import (
    advanced_search_and_download_pdb,
)

# ---------------------------
# Parsing & filtering
# ---------------------------
from .PDBparser import (
    parse_atoms,
    get_chains,
    get_residues,
    get_ca_coords,
    remove_ligands,
    keep_only_chain,
    keep_only_ca,
)

# ---------------------------
# Public API
# ---------------------------
__all__ = [
    # I/O
    "reindex_residues",

    # Descriptors
    "num_residues",
    "num_atoms",
    "aa_composition",
    "glycine_ratio",
    "hydrophobic_ratio",
    "radius_of_gyration",
    "max_ca_distance",
    "missing_residue_ratio",
    "secondary_structure_ratio",
    "compactness_index",
    "ca_density",

    # Quality
    "has_ca_only",
    "has_multiple_models",
    "has_altlocs",
    "num_chains",

    # Summary
    "pdb_summary",

    # Search
    "advanced_search_and_download_pdb",

    # Parsing
    "parse_atoms",
    "get_chains",
    "get_residues",
    "get_ca_coords",
    "remove_ligands",
    "keep_only_chain",
    "keep_only_ca",
]
