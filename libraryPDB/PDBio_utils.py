from typing import List, Tuple


def _parse_atom_lines(pdb_file: str) -> List[str]:
    """Retourne toutes les lignes ATOM et HETATM."""
    with open(pdb_file) as f:
        lines = [line.rstrip("\n") for line in f if line.startswith(("ATOM","HETATM"))]
    return lines

def _write_pdb_lines(lines: List[str], out_file: str):
    """Écrit les lignes dans un fichier PDB."""
    with open(out_file, "w") as f:
        for line in lines:
            f.write(line + "\n")

def normalize_chain_ids(pdb_file: str, out_file: str):
    lines = _parse_atom_lines(pdb_file)
    chain_map = {}
    next_chain = ord('A')

    new_lines = []
    for line in lines:
        chain_id = line[21]
        if chain_id not in chain_map:
            chain_map[chain_id] = chr(next_chain)
            next_chain += 1
            if next_chain > ord('Z'):
                next_chain = ord('A')  # wrap-around
        new_line = line[:21] + chain_map[chain_id] + line[22:]
        new_lines.append(new_line)

    _write_pdb_lines(new_lines, out_file)

def reindex_residues(pdb_file: str, out_file: str):
    lines = _parse_atom_lines(pdb_file)
    resid_map = {}
    next_resid = 1
    last_resname_chain = None

    new_lines = []
    for line in lines:
        resname = line[17:20]
        chain_id = line[21]
        key = (chain_id, resname)
        if key not in resid_map:
            resid_map[key] = next_resid
            next_resid += 1
        new_resid = resid_map[key]
        new_line = line[:22] + f"{new_resid:>4}" + line[26:]
        new_lines.append(new_line)

    _write_pdb_lines(new_lines, out_file)

def center_structure(pdb_file: str, out_file: str):
    ca_coords = []
    lines = _parse_atom_lines(pdb_file)
    for line in lines:
        if line[12:16].strip() == "CA":
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            ca_coords.append((x, y, z))

    if not ca_coords:
        _write_pdb_lines(lines, out_file)
        return

    # calcul centre de masse
    n = len(ca_coords)
    cx = sum(x for x,_,_ in ca_coords)/n
    cy = sum(y for _,y,_ in ca_coords)/n
    cz = sum(z for _,_,z in ca_coords)/n

    new_lines = []
    for line in lines:
        x = float(line[30:38])
        y = float(line[38:46])
        z = float(line[46:54])

        x_new = x - cx
        y_new = y - cy
        z_new = z - cz

        new_line = line[:30] + f"{x_new:8.3f}{y_new:8.3f}{z_new:8.3f}" + line[54:]
        new_lines.append(new_line)

    _write_pdb_lines(new_lines, out_file)




