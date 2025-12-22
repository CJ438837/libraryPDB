# download.py
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

    query = {
        "type": "group",
        "logical_operator": "and",
        "nodes": nodes
    }

    downloaded = []
    start = 0

    while len(downloaded) < max_results:
        payload = {
            "query": query,
            "return_type": "entry",
            "request_options": {
                "paginate": {
                    "start": start,
                    "rows": batch_size
                }
            }
        }

        r = requests.post(
            "https://search.rcsb.org/rcsbsearch/v2/query",
            json=payload
        )
        r.raise_for_status()

        results = r.json().get("result_set", [])
        if not results:
            break

        for item in results:
            if len(downloaded) >= max_results:
                break

            pdb_id = item["identifier"]
            path = os.path.join(save_dir, f"{pdb_id}.pdb")

            if not os.path.exists(path):
                pdb = requests.get(f"https://files.rcsb.org/download/{pdb_id}.pdb")
                pdb.raise_for_status()
                with open(path, "wb") as f:
                    f.write(pdb.content)

            downloaded.append(path)

        start += batch_size

    return downloaded



import os
import requests
from typing import List


def search_by_sequence_and_download_pdb(
    sequence: str,
    save_dir: str,
    max_results: int = 50,
    batch_size: int = 100
) -> List[str]:
    """
    Recherche PDB par similarité de séquence (RCSB Search v2)
    et télécharge les structures correspondantes.
    """

    os.makedirs(save_dir, exist_ok=True)

    query = {
        "type": "terminal",
        "service": "sequence",
        "parameters": {
            "value": sequence,
            "target": "pdb_protein_sequence"
        }
    }

    downloaded = []
    start = 0

    while len(downloaded) < max_results:
        payload = {
            "query": query,
            "return_type": "entry",
            "request_options": {
                "paginate": {
                    "start": start,
                    "rows": batch_size
                }
            }
        }

        r = requests.post(
            "https://search.rcsb.org/rcsbsearch/v2/query",
            json=payload
        )

        # DEBUG utile si ça recasse
        if r.status_code != 200:
            print("Payload envoyé :", payload)
            print("Réponse :", r.text)

        r.raise_for_status()

        results = r.json().get("result_set", [])
        if not results:
            break

        for item in results:
            if len(downloaded) >= max_results:
                break

            pdb_id = item["identifier"]
            path = os.path.join(save_dir, f"{pdb_id}.pdb")

            if not os.path.exists(path):
                pdb = requests.get(
                    f"https://files.rcsb.org/download/{pdb_id}.pdb"
                )
                pdb.raise_for_status()
                with open(path, "wb") as f:
                    f.write(pdb.content)

            downloaded.append(path)

        start += batch_size

    return downloaded


