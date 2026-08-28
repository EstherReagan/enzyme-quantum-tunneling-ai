import os
import requests
import numpy as np
import pandas as pd
import Bio.PDB
import torch
from transformers import AutoTokenizer, EsmForMaskedLM
from scipy.constants import hbar, m_p, eV


class PremiumEnzymePipeline:
    def __init__(self, pdb_id: str):
        self.pdb_id = pdb_id.lower().strip()
        self.pdb_filename = f"data/{self.pdb_id}.pdb"
        
    def download_data(self):
        """Downloads PDB structure file from RCSB."""
        os.makedirs("data", exist_ok=True)
        url = f"https://files.rcsb.org/download/{self.pdb_id}.pdb"
        
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                with open(self.pdb_filename, "w") as file:
                    file.write(response.text)
                print(f"✅ Downloaded structure: {self.pdb_id.upper()}")
                return True
            else:
                print(f"⚠️ PDB {self.pdb_id} not found (HTTP {response.status_code})")
                return False
        except Exception as e:
            print(f"⚠️ Download failed: {e}")
            return False

    def run_quantum_engine(self, width_angstroms, barrier_ev, substrate_energy_ev=0.1):
        """
        Calculates quantum tunneling probability using WKB approximation.
        
        T = exp(-2κa) where κ = sqrt(2m(V0-E))/ℏ
        
        Args:
            width_angstroms: Distance to tunnel through (Å)
            barrier_ev: Barrier height (eV)
            substrate_energy_ev: Substrate vibrational state (eV)
            
        Returns:
            Tunneling probability [0, 1]
        """
        # ✅ FIX #1: Add input validation
        if width_angstroms <= 0:
            raise ValueError(f"Width must be positive, got {width_angstroms}")
        if barrier_ev <= 0:
            raise ValueError(f"Barrier height must be positive, got {barrier_ev}")
        if substrate_energy_ev < 0:
            raise ValueError(f"Substrate energy must be non-negative, got {substrate_energy_ev}")
        
        # ✅ FIX #2: Include substrate energy term
        a = width_angstroms * 1e-10  # Convert Å to meters
        V0 = barrier_ev * eV  # Convert eV to joules
        E = substrate_energy_ev * eV  # Substrate vibrational energy
        
        # Check if substrate clears barrier
        if E >= V0:
            return 1.0
        
        # WKB transmission coefficient
        kappa = np.sqrt(2 * m_p * (V0 - E)) / hbar
        T = np.exp(-2 * kappa * a)
        
        # ✅ FIX #3: Apply prefactor (empirical from literature)
        # Typical H-tunneling prefactor: 0.001-0.01
        prefactor = 0.01
        T_corrected = float(min(1.0, prefactor * T))
        
        return T_corrected

    def run_ai_engine(self):
        """
        Runs ESM-2 masked language model to predict beneficial mutations.
        Returns ranked amino acid candidates.
        """
        sequence_window = "WHVLI"
        print(f"🧬 AI Processing Target Sequence: {sequence_window}")
        
        model_name = "facebook/esm2_t6_8M_UR50D"
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = EsmForMaskedLM.from_pretrained(model_name).to(device)
        model.eval()
        
        try:
            # ✅ FIX #2: Use masking for proper prediction
            target_pos = 2  # Mask position 2 (V)
            masked_sequence = sequence_window[:target_pos] + "[MASK]" + sequence_window[target_pos+1:]
            
            inputs = tokenizer(masked_sequence, return_tensors="pt").to(device)
            
            with torch.no_grad():
                outputs = model(**inputs)
            
            # Get logits at masked position
            masked_idx = (inputs['input_ids'] == tokenizer.mask_token_id).nonzero(as_tuple=True)[1][0].item()
            logits = outputs.logits[0, masked_idx, :]
            
            # Convert to probabilities
            probs = torch.softmax(logits, dim=0)
            
            # Get scores for standard amino acids
            amino_acids = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 
                          'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
            
            mutation_scores = {}
            for aa in amino_acids:
                aa_token = tokenizer.convert_tokens_to_ids(aa)
                if aa_token != tokenizer.unk_token_id:
                    mutation_scores[aa] = float(probs[aa_token])
            
            df = pd.DataFrame(
                list(mutation_scores.items()), 
                columns=['Candidate', 'Score']
            ).sort_values(by='Score', ascending=False).reset_index(drop=True)
            
            return df
        
        finally:
            # ✅ FIX #3: Cleanup GPU memory
            del model
            torch.cuda.empty_cache()


if __name__ == "__main__":
    print("🚀 Premium Enzyme Pipeline v2.0")
    runner = PremiumEnzymePipeline("1yge")
    runner.download_data()
    
    prob = runner.run_quantum_engine(width_angstroms=1.2, barrier_ev=0.6)
    print(f"✅ Tunneling Probability: {prob:.5e}")
    
    df = runner.run_ai_engine()
    print("\n🔬 Top 3 AI-Designed Mutations:")
    print(df.head(3).to_string(index=False))
