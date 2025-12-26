from typing import Set


def _iter_pdb_lines(pdb_file: str):
    with open(pdb_file) as f:
        for line in f:
            yield line.rstrip("\n")


def has_ca_only(pdb_file: str) -> bool:
    """
    Retourne True si tous les ATOM sont des CA.
    Ignore HETATM.
    """
    for line in _iter_pdb_lines(pdb_file):
        if not line.startswith("ATOM"):
            continue
        atom_name = line[12:16].strip()
        if atom_name != "CA":
            return False
    return True

def has_multiple_models(pdb_file: str) -> bool:
    """
    Retourne True si le fichier contient plusieurs modèles (NMR).
    """
    model_count = 0
    for line in _iter_pdb_lines(pdb_file):
        if line.startswith("MODEL"):
            model_count += 1
            if model_count > 1:
                return True
    return False

def has_altlocs(pdb_file: str) -> bool:
    """
    Retourne True si des positions alternatives sont présentes.
    """
    for line in _iter_pdb_lines(pdb_file):
        if not line.startswith("ATOM"):
            continue
        altloc = line[16]
        if altloc.strip():
            return True
    return False

def num_chains(pdb_file: str) -> int:
    """
    Retourne le nombre de chaînes ATOM distinctes.
    """
    chains: Set[str] = set()
    for line in _iter_pdb_lines(pdb_file):
        if line.startswith("ATOM"):
            chain_id = line[21]
            chains.add(chain_id)
    return len(chains)



