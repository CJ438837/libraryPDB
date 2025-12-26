# download_safe.py
import os
import requests
from typing import List, Optional

def advanced_search_and_download_pdb(
    save_dir: str,
    organisms: Optional[List[str]] = None,
    methods: Optional[List[str]] = None,
    keywords: Optional[List[str]] = None,
    max_results: int = 50,
    batch_size: int = 100
) -> List[str]:
    """
    Recherche avancée PDB via RCSB Search v2 et télécharge les structures trouvées.
    Les PDB manquants ou supprimés sont ignorés.
    """
    os.makedirs(save_dir, exist_ok=True)
    nodes = []

    if organisms:
        nodes.append({
            "type": "group",
            "logical_operator": "or",
            "nodes": [{
                "type": "terminal",
                "service": "text",
                "parameters": {
                    "attribute": "rcsb_entity_source_organism.taxonomy_lineage.name",
                    "operator": "contains_words",
                    "value": org
                }
            } for org in organisms]
        })

    if methods:
        nodes.append({
            "type": "group",
            "logical_operator": "or",
            "nodes": [{
                "type": "terminal",
                "service": "text",
                "parameters": {
                    "attribute": "exptl.method",
                    "operator": "exact_match",
                    "value": method
                }
            } for method in methods]
        })

    if keywords:
        nodes.append({
            "type": "group",
            "logical_operator": "or",
            "nodes": [{
                "type": "terminal",
                "service": "text",
                "parameters": {
                    "attribute": "struct.title",
                    "operator": "contains_words",
                    "value": kw
                }
            } for kw in keywords]
        })

    if not nodes:
        raise ValueError("Aucun critère de recherche fourni")

    query = {"type": "group", "logical_operator": "and", "nodes": nodes}
    downloaded = []
    start = 0

    while len(downloaded) < max_results:
        payload = {
            "query": query,
            "return_type": "entry",
            "request_options": {"paginate": {"start": start, "rows": batch_size}}
        }

        r = requests.post("https://search.rcsb.org/rcsbsearch/v2/query", json=payload)
        r.raise_for_status()
        results = r.json().get("result_set", [])
        if not results:
            break

        for item in results:
            if len(downloaded) >= max_results:
                break

            pdb_id = item["identifier"]
            path = os.path.join(save_dir, f"{pdb_id}.pdb")
            if os.path.exists(path):
                downloaded.append(path)
                continue

            try:
                pdb = requests.get(f"https://files.rcsb.org/download/{pdb_id}.pdb")
                pdb.raise_for_status()
                with open(path, "wb") as f:
                    f.write(pdb.content)
                downloaded.append(path)
            except requests.HTTPError:
                print(f"⚠️ PDB file not found: {pdb_id}, skipping...")

        start += batch_size

    return downloaded


def search_by_sequence_and_download_pdb(
    sequence: str,
    save_dir: str,
    max_results: int = 50,
    batch_size: int = 100
) -> List[str]:
    """
    Recherche PDB par similarité de séquence et télécharge les structures correspondantes.
    Ignore les fichiers PDB manquants.
    """
    os.makedirs(save_dir, exist_ok=True)
    query = {"type": "terminal", "service": "sequence",
             "parameters": {"value": sequence, "target": "pdb_protein_sequence"}}

    downloaded = []
    start = 0

    while len(downloaded) < max_results:
        payload = {
            "query": query,
            "return_type": "entry",
            "request_options": {"paginate": {"start": start, "rows": batch_size}}
        }

        r = requests.post("https://search.rcsb.org/rcsbsearch/v2/query", json=payload)
        r.raise_for_status()
        results = r.json().get("result_set", [])
        if not results:
            break

        for item in results:
            if len(downloaded) >= max_results:
                break

            pdb_id = item["identifier"]
            path = os.path.join(save_dir, f"{pdb_id}.pdb")
            if os.path.exists(path):
                downloaded.append(path)
                continue

            try:
                pdb = requests.get(f"https://files.rcsb.org/download/{pdb_id}.pdb")
                pdb.raise_for_status()
                with open(path, "wb") as f:
                    f.write(pdb.content)
                downloaded.append(path)
            except requests.HTTPError:
                print(f"⚠️ PDB file not found: {pdb_id}, skipping...")

        start += batch_size

    return downloaded
