import math
from collections import Counter
from typing import Dict, List, Tuple

def _parse_ca_atoms(pdb_file: str) -> List[Tuple[str, int, float, float, float]]:
    """
    Extrait les atomes CA :
    retourne [(resname, resid, x, y, z), ...]
    """
    ca_atoms = []

    with open(pdb_file) as f:
        for line in f:
            if not line.startswith("ATOM"):
                continue
            if line[12:16].strip() != "CA":
                continue

            resname = line[17:20].strip()
            resid = int(line[22:26])
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])

            ca_atoms.append((resname, resid, x, y, z))

    return ca_atoms

def num_residues(pdb_file: str) -> int:
    """Nombre de résidus (basé sur les CA)."""
    return len(_parse_ca_atoms(pdb_file))

def num_atoms(pdb_file: str) -> int:
    """Nombre total d'atomes ATOM."""
    count = 0
    with open(pdb_file) as f:
        for line in f:
            if line.startswith("ATOM"):
                count += 1
    return count

def aa_composition(pdb_file: str) -> Dict[str, float]:
    """
    Retourne la composition en AA (%),
    basée sur les CA.
    """
    ca_atoms = _parse_ca_atoms(pdb_file)
    total = len(ca_atoms)

    counts = Counter(res for res, *_ in ca_atoms)

    return {aa: count / total for aa, count in counts.items()}

def glycine_ratio(pdb_file: str) -> float:
    comp = aa_composition(pdb_file)
    return comp.get("GLY", 0.0)

HYDROPHOBIC = {"ALA", "VAL", "ILE", "LEU", "MET", "PHE", "TRP", "PRO"}

def hydrophobic_ratio(pdb_file: str) -> float:
    comp = aa_composition(pdb_file)
    return sum(comp.get(aa, 0.0) for aa in HYDROPHOBIC)

def radius_of_gyration(pdb_file: str) -> float:
    ca_atoms = _parse_ca_atoms(pdb_file)
    n = len(ca_atoms)

    if n == 0:
        return 0.0

    cx = sum(x for _, _, x, _, _ in ca_atoms) / n
    cy = sum(y for _, _, _, y, _ in ca_atoms) / n
    cz = sum(z for _, _, _, _, z in ca_atoms) / n

    rg = math.sqrt(
        sum((x - cx)**2 + (y - cy)**2 + (z - cz)**2
            for _, _, x, y, z in ca_atoms) / n
    )

    return rg

def max_ca_distance(pdb_file: str) -> float:
    ca_atoms = _parse_ca_atoms(pdb_file)
    max_dist = 0.0

    for i in range(len(ca_atoms)):
        _, _, x1, y1, z1 = ca_atoms[i]
        for j in range(i + 1, len(ca_atoms)):
            _, _, x2, y2, z2 = ca_atoms[j]
            d = math.sqrt(
                (x1 - x2)**2 +
                (y1 - y2)**2 +
                (z1 - z2)**2
            )
            max_dist = max(max_dist, d)

    return max_dist

def missing_residue_ratio(pdb_file: str) -> float:
    ca_atoms = _parse_ca_atoms(pdb_file)

    if len(ca_atoms) < 2:
        return 0.0

    resids = sorted(resid for _, resid, *_ in ca_atoms)
    expected = resids[-1] - resids[0] + 1
    missing = expected - len(resids)

    return missing / expected



import math
from typing import List, Tuple

def _parse_ca_coords(pdb_file: str) -> List[Tuple[float, float, float]]:
    """
    Retourne les coordonnées (x,y,z) des atomes CA
    """
    ca_coords = []
    with open(pdb_file) as f:
        for line in f:
            if not line.startswith("ATOM"):
                continue
            if line[12:16].strip() != "CA":
                continue
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            ca_coords.append((x, y, z))
    return ca_coords

def secondary_structure_ratio(pdb_file: str) -> float:
    ca_coords = _parse_ca_coords(pdb_file)
    if len(ca_coords) < 2:
        return 0.0

    count_ss = 0
    for i in range(len(ca_coords) - 1):
        x1, y1, z1 = ca_coords[i]
        x2, y2, z2 = ca_coords[i+1]
        d = math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
        if d < 4.0:  # heuristique
            count_ss += 1

    return count_ss / (len(ca_coords) - 1)

def compactness_index(pdb_file: str) -> float:
    ca_coords = _parse_ca_coords(pdb_file)
    n = len(ca_coords)
    if n < 2:
        return 0.0

    # centre
    cx = sum(x for x, _, _ in ca_coords)/n
    cy = sum(y for _, y, _ in ca_coords)/n
    cz = sum(z for _, _, z in ca_coords)/n

    # rayon de giration
    rg = math.sqrt(sum((x-cx)**2 + (y-cy)**2 + (z-cz)**2 for x,y,z in ca_coords)/n)

    # index de compacité heuristique
    return rg / (n ** (1/3))

def ca_density(pdb_file: str) -> float:
    ca_coords = _parse_ca_coords(pdb_file)
    if not ca_coords:
        return 0.0

    xs = [x for x,_,_ in ca_coords]
    ys = [y for _,y,_ in ca_coords]
    zs = [z for _,_,z in ca_coords]

    vol = (max(xs)-min(xs)) * (max(ys)-min(ys)) * (max(zs)-min(zs))
    if vol == 0:
        return 0.0

    return len(ca_coords)/vol
