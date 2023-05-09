"""Antibody folding via IgFold"""
import os
from typing import Optional
from pymol.cmd import get_names, read_pdbstr

from designer.common import AMINO_ACIDS

def fold_antibody(igfold, heavy_chain: str, light_chain: Optional[str], use_refine: bool) -> dict[str, str]:
    """Fold antibody sequence and output PDB"""
    sequences = {
        "H": heavy_chain
    }
    if light_chain:
        sequences["L"] = light_chain

    for chain, sequence in sequences.items():
        if not all(c in AMINO_ACIDS for c in sequence):
            return {"status": "error",
                    "content": f"Chain '{chain}' contains non-aminoacid characters"}

    result_pdb = ""
    try:
        igfold.fold("temp_file.pdb",
                    sequences=sequences, do_refine=use_refine,
                    use_openmm=True, do_renum=False)
        with open("temp_file.pdb", "rt", encoding="utf8") as file:
            result_pdb = file.read()
        os.remove("temp_file.pdb")
        os.remove("temp_file.fasta")
    except Exception:
        return {"status": "error", "content": "Folding failed"}
    return {"status": "ok", "content": result_pdb}

def append_model(model_pdbstr: str, prefix: str = "antibody_"):
    """Gets model pdb string and appends it to the session"""
    structures = get_names('objects')
    print(structures)
    structures = [structure for structure in structures if structure.startswith(prefix)]
    idx = 0
    if structures:
        last_idx = max(int(suffix) for structure in structures
                       if (suffix := structure[len(prefix):]).isnumeric())
        idx = last_idx + 1
    read_pdbstr(model_pdbstr, f"{prefix}{idx}")
