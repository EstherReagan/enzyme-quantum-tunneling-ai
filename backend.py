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

app = FastAPI(title="Enzyme Quantum Tunneling API")

# Enable CORS for Dash frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================
# DATA MODELS
# ========================

class QuantumParams(BaseModel):
    width_angstroms: float
    barrier_ev: float
    substrate_energy_ev: float = 0.1

class QuantumResult(BaseModel):
    tunneling_probability: float
    log_scale: float
    enhancement_fold: float

class MutationResult(BaseModel):
    amino_acid: str
    score: float
    rank: int

class EnzymeInfo(BaseModel):
    pdb_id: str
    name: str
    sequence: str
    barrier_height: float
    tunneling_width: float

# ========================
# QUANTUM ENGINE
# ========================

def calculate_quantum_tunneling(
    width_angstroms: float,
    barrier_ev: float,
    substrate_energy_ev: float = 0.1
) -> dict:
    """WKB quantum tunneling calculation"""
    
    if width_angstroms <= 0:
        raise ValueError("Width must be positive")
    if barrier_ev <= 0:
        raise ValueError("Barrier height must be positive")
    if substrate_energy_ev < 0:
        raise ValueError("Substrate energy must be non-negative")
    
    a = width_angstroms * 1e-10
    V0 = barrier_ev * eV
    E = substrate_energy_ev * eV
    
    if E >= V0:
        return {
            "tunneling_probability": 1.0,
            "log_scale": 0.0,
            "enhancement_fold": 1e20
        }
    
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

# ========================
# AI ENGINE (FIXED)
# ========================

MODEL_NAME = "facebook/esm2_t6_8M_UR50D"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Cache models
@app.on_event("startup")
async def load_models():
    """Load ESM-2 model on startup"""
    global tokenizer, model
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = EsmForMaskedLM.from_pretrained(MODEL_NAME).to(device)
        model.eval()
        print("✅ ESM-2 model loaded successfully")
    except Exception as e:
        print(f"⚠️ Model loading failed: {e}")

def predict_mutations(sequence: str) -> list:
    """
    Predict beneficial mutations using ESM-2.
    Returns ranked amino acid candidates.
    """
    if not sequence or len(sequence) == 0:
        return []
    
    try:
        # Use first residue as target
        target_pos = 0
        masked_seq = "[MASK]" + sequence[1:]
        
        inputs = tokenizer(masked_seq, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Get logits at masked position
        logits = outputs.logits[0, 1, :]
        probs = torch.softmax(logits, dim=0)
        
        # Standard amino acids
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
        
        # Sort by score
        mutations.sort(key=lambda x: x["score"], reverse=True)
        
        # Add rank
        for i, mut in enumerate(mutations):
            mut["rank"] = i + 1
        
        return mutations[:20]
    
    except Exception as e:
        print(f"❌ Mutation prediction failed: {e}")
        return []

@app.post("/mutations")
def mutations_endpoint(sequence: str):
    """Predict mutations for given sequence"""
    mutations = predict_mutations(sequence)
    return {"mutations": mutations}

# ========================
# PDB HANDLING (UNIVERSAL)
# ========================

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

def parse_pdb_structure(pdb_data: str) -> dict:
    """Parse PDB structure and extract info"""
    try:
        # Write to temp file
        temp_path = "/tmp/temp.pdb"
        with open(temp_path, "w") as f:
            f.write(pdb_data)
        
        parser = Bio.PDB.PDBParser(QUIET=True)
        structure = parser.get_structure("enzyme", temp_path)
        
        # Extract sequence
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
        
        # Get active site (first 6-12 residues)
        active_site = full_seq[:min(12, len(full_seq))] if full_seq else "ALVGHP"
        
        return {
            "pdb_id": "PDB",
            "sequence_length": len(full_seq),
            "full_sequence": full_seq[:100],  # First 100 residues
            "active_site": active_site,
            "num_chains": len(list(structure[0]))
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parse error: {str(e)}")

@app.get("/pdb/{pdb_id}")
def get_pdb(pdb_id: str):
    """Get PDB structure and info"""
    pdb_data = fetch_pdb(pdb_id)
    info = parse_pdb_structure(pdb_data)
    
    return {
        "pdb_id": pdb_id.upper(),
        "pdb_data": pdb_data,
        "info": info
    }

# ========================
# SEARCH & DISCOVERY
# ========================

@app.get("/search/{enzyme_name}")
def search_enzymes(enzyme_name: str):
    """Search PDB for enzymes by name (mock - returns common enzymes)"""
    common_enzymes = {
        "lipoxygenase": {"pdb_id": "1YGE", "name": "Soybean Lipoxygenase"},
        "dhfr": {"pdb_id": "1DRF", "name": "Dihydrofolate Reductase"},
        "p450": {"pdb_id": "1OXO", "name": "Cytochrome P450 3A4"},
        "aldolase": {"pdb_id": "1ZAH", "name": "Aldolase"},
        "protease": {"pdb_id": "1HTM", "name": "HIV Protease"},
        "kinase": {"pdb_id": "1ATP", "name": "ATP-dependent Kinase"},
    }
    
    results = []
    query = enzyme_name.lower().strip()
    
    for key, value in common_enzymes.items():
        if query in key or query in value["name"].lower():
            results.append(value)
    
    return {"results": results, "total": len(results)}

@app.get("/featured-enzymes")
def featured_enzymes():
    """Get featured enzymes for quick access"""
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

# ========================
# HEALTH CHECK
# ========================

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "active", "version": "2.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
