import os
from typing import List, Tuple, Dict



def parse_atoms(pdb_file: str) -> List[Dict]:
    """Parse le fichier PDB et retourne une liste de dictionnaires pour chaque atome"""
    atoms = []
    with open(pdb_file, "r") as f:
        for line in f:
            if line.startswith(("ATOM", "HETATM")):
                line_type = line[:6].strip()
                atom_name = line[12:16].strip()
                res_name = line[17:20].strip()
                chain = line[21].strip()
                res_id = int(line[22:26].strip())
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                element = line[76:78].strip() if len(line) >= 78 else ""

                atoms.append({
                    "line_type": line_type,
                    "atom_name": atom_name,
                    "res_name": res_name,
                    "chain": chain,
                    "res_id": res_id,
                    "coords": (x, y, z),
                    "element": element
                })
    return atoms


def get_chains(pdb_file: str) -> List[str]:
    """Retourne la liste triée des chaînes présentes dans le PDB"""
    atoms = parse_atoms(pdb_file)
    chains = set(a["chain"] for a in atoms)
    return sorted(chains)


def get_residues(pdb_file: str, chain: str = None) -> List[Tuple[str, int]]:
    """Retourne la liste des résidus sous forme (res_name, res_id), optionnellement filtrée par chaîne"""
    atoms = parse_atoms(pdb_file)
    residues = []
    seen = set()
    for a in atoms:
        if chain is None or a["chain"] == chain:
            key = (a["res_name"], a["res_id"])
            if key not in seen:
                residues.append(key)
                seen.add(key)
    return residues


def get_ca_coords(pdb_file: str, chain: str = None) -> List[Tuple[float, float, float]]:
    """Retourne les coordonnées des atomes CA uniquement"""
    atoms = parse_atoms(pdb_file)
    return [a["coords"] for a in atoms if a["atom_name"] == "CA" and (chain is None or a["chain"] == chain)]


# ------------------------------
# Fonctions de transformation
# ------------------------------

def remove_ligands(pdb_file: str, out_file: str):
    """Supprime les HETATM et écrit un nouveau fichier PDB"""
    atoms = parse_atoms(pdb_file)
    atoms = [a for a in atoms if a["line_type"] == "ATOM"]
    write_pdb(atoms, out_file)


def keep_only_chain(pdb_file: str, chain: str, out_file: str):
    """Garde uniquement les atomes de la chaîne spécifiée"""
    atoms = parse_atoms(pdb_file)
    atoms = [a for a in atoms if a["chain"] == chain]
    write_pdb(atoms, out_file)


def keep_only_ca(pdb_file: str, out_file: str):
    """Garde uniquement les atomes CA"""
    atoms = parse_atoms(pdb_file)
    atoms = [a for a in atoms if a["atom_name"] == "CA"]
    write_pdb(atoms, out_file)


# ------------------------------
# Écriture PDB
# ------------------------------

def write_pdb(atoms: List[Dict], out_file: str):
    """Écrit la liste d’atomes dans un fichier PDB"""
    with open(out_file, "w") as f:
        for i, a in enumerate(atoms, start=1):
            line = "{:<6}{:>5} {:<4} {:>3} {:>1}{:>4}    {:>8.3f}{:>8.3f}{:>8.3f} {:>6} {:>6}          {:>2}\n".format(
                "ATOM",
                i,
                a["atom_name"],
                a["res_name"],
                a["chain"],
                a["res_id"],
                a["coords"][0],
                a["coords"][1],
                a["coords"][2],
                1.0,
                0.0,
                a["element"]
            )
            f.write(line)
        f.write("END\n")
