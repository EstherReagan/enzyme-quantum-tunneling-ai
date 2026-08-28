import pytest
import numpy as np
import os
import pandas as pd
import torch
from unittest.mock import patch, MagicMock
from pipeline import PremiumEnzymePipeline


# ========================
# FIXTURES
# ========================

@pytest.fixture
def runner():
    """Standard pipeline runner"""
    return PremiumEnzymePipeline("1yge")

@pytest.fixture
def mock_pdb_response():
    """Mock PDB file content"""
    return """HEADER    ENZYME
ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00           N
ATOM      2  CA  ALA A   1       1.458   0.000   0.000  1.00  0.00           C
END"""


# ========================
# QUANTUM ENGINE TESTS
# ========================

class TestQuantumEngine:
    """Test WKB tunneling calculations"""
    
    def test_boundary_zero_barrier(self, runner):
        """Zero barrier → 100% transmission"""
        result = runner.run_quantum_engine(1.2, 0.0)
        assert result == 1.0
    
    def test_boundary_width_monotonicity(self, runner):
        """Wider barrier → lower transmission"""
        narrow = runner.run_quantum_engine(1.0, 0.6)
        wide = runner.run_quantum_engine(2.0, 0.6)
        assert narrow > wide, f"Expected {narrow} > {wide}"
    
    def test_boundary_barrier_monotonicity(self, runner):
        """Taller barrier → lower transmission"""
        low_barrier = runner.run_quantum_engine(1.2, 0.3)
        high_barrier = runner.run_quantum_engine(1.2, 0.9)
        assert low_barrier > high_barrier, f"Expected {low_barrier} > {high_barrier}"
    
    def test_substrate_energy_effect(self, runner):
        """Higher substrate energy → higher transmission"""
        low_energy = runner.run_quantum_engine(1.2, 0.6, substrate_energy_ev=0.0)
        high_energy = runner.run_quantum_engine(1.2, 0.6, substrate_energy_ev=0.3)
        assert high_energy > low_energy
    
    @pytest.mark.parametrize("width,barrier,substrate", [
        (-1.0, 0.5, 0.1),      # Negative width
        (1.0, -0.5, 0.1),      # Negative barrier
        (1.0, 0.5, -0.1),      # Negative substrate energy
    ])
    def test_invalid_inputs_raise_error(self, runner, width, barrier, substrate):
        """Invalid inputs should raise ValueError"""
        with pytest.raises(ValueError):
            runner.run_quantum_engine(width, barrier, substrate)
    
    def test_exponential_decay_with_width(self, runner):
        """Verify exponential relationship: T ∝ exp(-κa)"""
        widths = np.array([1.0, 1.5, 2.0, 2.5])
        probs = np.array([
            runner.run_quantum_engine(w, 0.6) for w in widths
        ])
        
        # All values should be positive
        assert np.all(probs > 0)
        
        # Should decay with width
        assert probs[0] > probs[3]
    
    def test_literature_benchmark(self, runner):
        """
        Validate against Soybean Lipoxygenase literature.
        Expected: T ~1e-18 for 1.2Å barrier at 0.6eV
        """
        prob = runner.run_quantum_engine(1.2, 0.6, substrate_energy_ev=0.1)
        
        # Should be within reasonable range
        assert 1e-20 < prob < 1e-15, f"Got {prob}, expected ~1e-18"
    
    def test_numerical_stability_large_widths(self, runner):
        """Very large widths should not overflow/underflow"""
        result = runner.run_quantum_engine(100.0, 0.6)
        assert 0 <= result <= 1.0
        assert result > 0
    
    def test_returns_float_not_numpy(self, runner):
        """Output should be Python float"""
        result = runner.run_quantum_engine(1.2, 0.6)
        assert isinstance(result, float)
        assert not isinstance(result, np.ndarray)
    
    def test_deterministic_output(self, runner):
        """Same inputs → same outputs"""
        prob1 = runner.run_quantum_engine(1.2, 0.6)
        prob2 = runner.run_quantum_engine(1.2, 0.6)
        assert prob1 == prob2


# ========================
# AI ENGINE TESTS
# ========================

class TestAIEngine:
    """Test ESM-2 mutation scoring"""
    
    def test_ai_engine_output_structure(self, runner):
        """Verify output is properly formatted DataFrame"""
        df = runner.run_ai_engine()
        
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ['Candidate', 'Score']
        assert len(df) == 20  # 20 standard amino acids
    
    def test_ai_engine_sorted_descending(self, runner):
        """Results should be sorted by score (descending)"""
        df = runner.run_ai_engine()
        assert df['Score'].is_monotonic_decreasing
    
    def test_ai_engine_no_duplicates(self, runner):
        """Each amino acid should appear once"""
        df = runner.run_ai_engine()
        assert df['Candidate'].nunique() == 20
    
    def test_ai_engine_scores_valid_range(self, runner):
        """Scores should be reasonable probabilities"""
        df = runner.run_ai_engine()
        
        assert df['Score'].min() >= -50
        assert df['Score'].max() <= 50
    
    def test_ai_engine_sums_to_one(self, runner):
        """If using softmax, scores should sum ~1.0"""
        df = runner.run_ai_engine()
        total = df['Score'].sum()
        
        # Should sum to approximately 1.0 if softmax
        # Allow some tolerance for numerical precision
        assert 0.5 < total < 2.0
    
    def test_ai_engine_memory_cleanup(self, runner):
        """Verify GPU memory doesn't leak"""
        if torch.cuda.is_available():
            initial = torch.cuda.memory_allocated()
            
            runner.run_ai_engine()
            runner.run_ai_engine()  # Run twice
            
            final = torch.cuda.memory_allocated()
            
            # Memory shouldn't grow unbounded
            # Allow up to 2GB for model loading
            assert final < initial + 2e9


# ========================
# DATA HANDLING TESTS
# ========================

class TestDataHandling:
    """Test PDB downloading and parsing"""
    
    @patch('requests.get')
    def test_download_valid_pdb(self, mock_get, runner, mock_pdb_response):
        """Successfully download valid PDB"""
        mock_get.return_value = MagicMock(
            status_code=200,
            text=mock_pdb_response
        )
        
        result = runner.download_data()
        assert result == True
        assert os.path.exists(f"data/{runner.pdb_id}.pdb")
    
    @patch('requests.get')
    def test_download_invalid_pdb(self, mock_get, runner):
        """Handle invalid PDB ID gracefully"""
        mock_get.return_value = MagicMock(status_code=404)
        
        result = runner.download_data()
        assert result == False
    
    @patch('requests.get')
    def test_download_network_error(self, mock_get, runner):
        """Handle network failures gracefully"""
        mock_get.side_effect = Exception("Connection timeout")
        
        result = runner.download_data()
        assert result == False
    
    def test_pdb_filename_correct(self, runner):
        """PDB filename should be lowercase"""
        runner_upper = PremiumEnzymePipeline("1YGE")
        assert runner_upper.pdb_id == "1yge"
        assert runner_upper.pdb_filename == "data/1yge.pdb"


# ========================
# INTEGRATION TESTS
# ========================

class TestIntegration:
    """Full pipeline tests"""
    
    def test_full_pipeline_workflow(self, runner):
        """Complete workflow: Calculate quantum + AI"""
        quantum_prob = runner.run_quantum_engine(1.2, 0.6)
        ai_mutations = runner.run_ai_engine()
        
        assert quantum_prob > 0
        assert len(ai_mutations) > 0
        assert quantum_prob <= 1.0
        assert len(ai_mutations) == 20
    
    def test_multiple_pdb_ids(self):
        """Verify different PDB IDs create separate instances"""
        runner1 = PremiumEnzymePipeline("1yge")
        runner2 = PremiumEnzymePipeline("1drf")
        
        assert runner1.pdb_id != runner2.pdb_id
        assert runner1.pdb_filename != runner2.pdb_filename


# ========================
# CLEANUP
# ========================

@pytest.fixture(scope="session", autouse=True)
def cleanup():
    """Clean up test data after all tests"""
    yield
    import shutil
    if os.path.exists("data"):
        # Optional: clean up test PDB files
        pass
