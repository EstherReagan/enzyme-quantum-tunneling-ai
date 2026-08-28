import pytest
import numpy as np
import os
import pandas as pd
import torch
from pipeline import PremiumEnzymePipeline

# ========================
# HIGH-FIDELITY FIXTURES
# ========================

@pytest.fixture
def runner():
    """Standard automated pipeline wrapper initializer."""
    return PremiumEnzymePipeline("1yge")

# ========================
# QUANTUM MACHINE MODULE TESTS
# ========================

class TestQuantumEngineModule:
    """Rigorous scientific check bounds checking physical wave constraints."""
    
    def test_boundary_zero_barrier_saturation(self, runner):
        """Zero barrier potential must force immediate 100% vector transmission saturation."""
        result = runner.run_quantum_engine(width_angstroms=1.2, barrier_ev=0.0, substrate_energy_ev=0.0)
        assert result == 1.0

    def test_kinetic_substrate_energy_saturation(self, runner):
        """When particle kinetic energy matches or exceeds the barrier, transmission saturates to 1.0."""
        result = runner.run_quantum_engine(width_angstroms=1.2, barrier_ev=0.5, substrate_energy_ev=0.6)
        assert result == 1.0
        
    def test_distance_monotonicity_decay(self, runner):
        """An expanding distance barrier width must force a strict monotonic decay calculation value."""
        narrow_channel = runner.run_quantum_engine(width_angstroms=1.0, barrier_ev=0.6, substrate_energy_ev=0.1)
        wide_channel = runner.run_quantum_engine(width_angstroms=2.0, barrier_ev=0.6, substrate_energy_ev=0.1)
        assert narrow_channel > wide_channel
        
    @pytest.mark.parametrize("width,barrier,energy", [
        (-1.2, 0.6, 0.1),  # Physically impossible negative width distance
        (1.2, -0.6, 0.1),  # Physically impossible negative potential energy barrier
        (0.0, 0.6, 0.1),   # Physically impossible zero-width boundary
        (1.2, 0.6, -0.1)   # Physically impossible negative substrate energy
    ])
    def test_invalid_physics_input_protection(self, runner, width, barrier, energy):
        """Pipeline must catch negative parameters and cleanly abort via a ValueError."""
        with pytest.raises(ValueError):
            runner.run_quantum_engine(width_angstroms=width, barrier_ev=barrier, substrate_energy_ev=energy)
            
    def test_literature_order_calibration(self, runner):
        """Validates that values align correctly with Klinman textbook biological controls (~1e-18)."""
        prob = runner.run_quantum_engine(width_angstroms=1.2, barrier_ev=0.6, substrate_energy_ev=0.1)
        # Verify the calculation falls within realistic quantum proton kinetic scales
        assert 1e-21 < prob < 1e-15, f"Physics alignment drift anomaly detected: {prob}"

# ========================
# DEEP ML ARTIFICIAL INTELLIGENCE TESTS
# ========================

class TestAIInferenceModule:
    """Verifies matrix dimensions, language model formatting, and memory state checks."""
    
    def test_ai_matrix_output_compliance(self, runner):
        """Ensures the transformer pipeline returns cleanly organized and sorted data arrays."""
        sample_fragment = "WHVLI"
        df = runner.run_ai_engine(sample_fragment)
        
        # Verify strict professional data types and columns
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ['Candidate', 'Score']
        assert len(df) == 20  # Must represent all 20 canonical amino acids
        assert df['Candidate'].is_unique
        
        # Ensure scores are correctly ordered from best (highest) to worst
        assert df['Score'].is_monotonic_decreasing

# ========================
# INTEGRATION STEP PIPELINE TESTS
# ========================

def test_full_pipeline_cohesion(runner):
    """Integration test verifying end-to-end data passing between engines."""
    # 1. Structural extraction verification
    active_seq = runner.extract_active_site_sequence()
    assert isinstance(active_seq, str)
    assert len(active_seq) >= 5
    
    # 2. Sequential calculation integration execution checks
    quantum_coefficient = runner.run_quantum_engine(width_angstroms=1.2, barrier_ev=0.6, substrate_energy_ev=0.1)
    ai_variant_matrix = runner.run_ai_engine(active_seq)
    
    assert quantum_coefficient <= 1.0
    assert not ai_variant_matrix.empty
