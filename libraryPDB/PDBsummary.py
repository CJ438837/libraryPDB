from typing import Dict
from .PDBdescriptors import (
    num_residues, num_atoms,
    aa_composition, glycine_ratio, hydrophobic_ratio,
    radius_of_gyration, max_ca_distance, missing_residue_ratio, secondary_structure_ratio, compactness_index, ca_density
)

from .PDBquality import (
    has_ca_only, has_multiple_models, has_altlocs, num_chains
)

def pdb_summary(pdb_file: str) -> Dict[str, float]:
    """
    Retourne un dictionnaire combinant :
    - descripteurs quantitatifs simples
    - métriques de qualité structurelle
    - des métriques heuristiques utiles
    """
    summary = {}

    # --- Quality checks ---
    summary["has_ca_only"] = has_ca_only(pdb_file)
    summary["multiple_models"] = has_multiple_models(pdb_file)
    summary["has_altlocs"] = has_altlocs(pdb_file)
    summary["num_chains"] = num_chains(pdb_file)

    # --- Basic descriptors ---
    summary["num_residues"] = num_residues(pdb_file)
    summary["num_atoms"] = num_atoms(pdb_file)
    summary["missing_residue_ratio"] = missing_residue_ratio(pdb_file)

    # --- Amino acid composition ---
    summary["glycine_ratio"] = glycine_ratio(pdb_file)
    summary["hydrophobic_ratio"] = hydrophobic_ratio(pdb_file)
    summary["aa_composition"] = aa_composition(pdb_file)  # dictionnaire AA -> fraction

    # --- Geometrical descriptors ---
    summary["radius_of_gyration"] = radius_of_gyration(pdb_file)
    summary["max_ca_distance"] = max_ca_distance(pdb_file)
    summary["secondary_structure_ratio"] = secondary_structure_ratio(pdb_file)
    summary["compactness_index"] = compactness_index(pdb_file)
    summary["ca_density"] = ca_density(pdb_file)

    return summary

