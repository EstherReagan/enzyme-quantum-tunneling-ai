from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import pandas as pd
import requests
import torch
from transformers import AutoTokenizer, EsmForMaskedLM
from scipy.constants import hbar, m_p, eV
import Bio.PDB
import os
import json

app = FastAPI(title="Enzyme Quantum Tunneling API", version="3.0")

# CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== MODELS =====

class QuantumParams(BaseModel):
    width_angstroms: float
    barrier_ev: float
    substrate_energy_ev: float = 0.1

class QuantumResult(BaseModel):
    tunneling_probability: float
    log_scale: float
    enhancement_fold: float

# ===== QUANTUM ENGINE =====

def calculate_quantum_tunneling(width_angstroms: float, barrier_ev: float, substrate_energy_ev: float = 0.1) -> dict:
    """WKB semi-classical quantum tunneling calculation"""
    
    if width_angstroms <= 0:
        raise ValueError("Width must be positive")
    if barrier_ev <= 0:
        raise ValueError("Barrier must be positive")
    
    a = width_angstroms * 1e-10
    V0 = barrier_ev * eV
    E = substrate_energy_ev * eV
    
    if E >= V0:
        return {"tunneling_probability": 1.0, "log_scale": 0.0, "enhancement_fold": 1e20}
    
    kappa = np.sqrt(2 * m_p * (V0 - E)) / hbar
    T = np.exp(-2 * kappa * a)
    prefactor = 0.01
    T_corrected = float(min(1.0, prefactor * T))
    
    T_water = 1e-20
    fold = T_corrected / T_water if T_corrected > 0 else 0
    
    return {
        "tunneling_probability": T_corrected,
        "log_scale": float(np.log10(T_corrected)) if T_corrected > 0 else -40,
        "enhancement_fold": float(fold)
    }

@app.post("/quantum", response_model=QuantumResult)
def quantum_endpoint(params: QuantumParams):
    """Calculate quantum tunneling"""
    result = calculate_quantum_tunneling(
        params.width_angstroms,
        params.barrier_ev,
        params.substrate_energy_ev
    )
    return result

# ===== AI ENGINE =====

MODEL_NAME = "facebook/esm2_t6_8M_UR50D"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = None
model = None

@app.on_event("startup")
async def load_models():
    """Load ESM-2 on startup"""
    global tokenizer, model
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = EsmForMaskedLM.from_pretrained(MODEL_NAME).to(device)
        model.eval()
        print("✅ ESM-2 loaded")
    except Exception as e:
        print(f"⚠️ Model error: {e}")

def predict_mutations(sequence: str) -> list:
    """Predict mutations using ESM-2"""
    if not sequence or len(sequence) == 0:
        return []
    
    try:
        target_pos = 0
        masked_seq = "[MASK]" + sequence[1:]
        
        inputs = tokenizer(masked_seq, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        logits = outputs.logits[0, 1, :]
        probs = torch.softmax(logits, dim=0)
        
        amino_acids = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I',
                      'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
        
        mutations = []
        for aa in amino_acids:
            try:
                aa_token = tokenizer.convert_tokens_to_ids(aa)
                if aa_token != tokenizer.unk_token_id:
                    score = float(probs[aa_token])
                    mutations.append({
                        "amino_acid": aa,
                        "score": score,
                        "rank": 0
                    })
            except:
                pass
        
        mutations.sort(key=lambda x: x["score"], reverse=True)
        
        for i, mut in enumerate(mutations):
            mut["rank"] = i + 1
        
        return mutations[:20]
    except Exception as e:
        print(f"❌ Mutation error: {e}")
        return []

@app.post("/mutations")
def mutations_endpoint(sequence: str):
    """Predict mutations"""
    mutations = predict_mutations(sequence)
    return {"mutations": mutations}

# ===== PDB HANDLING =====

def fetch_pdb(pdb_id: str) -> str:
    """Download PDB file"""
    pdb_id = pdb_id.lower().strip()
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.text
        else:
            raise HTTPException(status_code=404, detail=f"PDB {pdb_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def parse_pdb(pdb_data: str) -> dict:
    """Parse PDB structure"""
    try:
        temp_path = "/tmp/temp.pdb"
        with open(temp_path, "w") as f:
            f.write(pdb_data)
        
        parser = Bio.PDB.PDBParser(QUIET=True)
        structure = parser.get_structure("enzyme", temp_path)
        
        THREE_TO_ONE = {
            'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
            'GLU': 'E', 'GLN': 'Q', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
            'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
            'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
        }
        
        sequence = []
        for chain in structure[0]:
            for residue in chain:
                res_name = residue.get_resname()
                if res_name in THREE_TO_ONE:
                    sequence.append(THREE_TO_ONE[res_name])
        
        full_seq = "".join(sequence)
        active_site = full_seq[:min(12, len(full_seq))] if full_seq else "ALVGHP"
        
        return {
            "sequence_length": len(full_seq),
            "full_sequence": full_seq[:100],
            "active_site": active_site,
            "num_chains": len(list(structure[0]))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parse error: {str(e)}")

@app.get("/pdb/{pdb_id}")
def get_pdb(pdb_id: str):
    """Get PDB structure"""
    pdb_data = fetch_pdb(pdb_id)
    info = parse_pdb(pdb_data)
    
    return {
        "pdb_id": pdb_id.upper(),
        "info": info
    }

# ===== FEATURED ENZYMES =====

@app.get("/featured-enzymes")
def featured_enzymes():
    """Get featured enzymes"""
    return {
        "enzymes": [
            {
                "name": "Soybean Lipoxygenase",
                "pdb_id": "1YGE",
                "description": "Proton tunneling in lipid oxidation",
                "barrier_height": 0.6,
                "tunneling_width": 1.2
            },
            {
                "name": "Dihydrofolate Reductase",
                "pdb_id": "1DRF",
                "description": "Hydride transfer enzyme",
                "barrier_height": 0.5,
                "tunneling_width": 1.0
            },
            {
                "name": "Cytochrome P450 3A4",
                "pdb_id": "1OXO",
                "description": "Drug metabolism enzyme",
                "barrier_height": 0.7,
                "tunneling_width": 1.3
            },
            {
                "name": "Formate Oxidase",
                "pdb_id": "1FOX",
                "description": "Electron tunneling enzyme",
                "barrier_height": 0.65,
                "tunneling_width": 1.15
            }
        ]
    }

@app.get("/health")
def health():
    """Health check"""
    return {"status": "active", "version": "3.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
