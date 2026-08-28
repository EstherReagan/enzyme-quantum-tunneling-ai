import pytest
import numpy as np
import os
import pandas as pd
from pipeline import PremiumEnzymePipeline

@pytest.fixture
def runner():
    """Initializes standard computational model class configurations."""
    return PremiumEnzymePipeline("1yge")

class TestEnzymeQuantumEngineModule:
    """Scientific bounding check checking boundary wave constraints."""
    
    def test_zero_barrier_saturation(self, runner):
        """Zero barrier fields must force transmission coefficients exactly matching 1.0."""
        assert runner.run_quantum_engine(width_angstroms=1.2, barrier_ev=0.0, substrate_energy_ev=0.0) == 1.0

    def test_kinetic_substrate_energy_saturation(self, runner):
        """Particle kinetic energy values exceeding barrier heights must force transmission coefficients to 1.0."""
        assert runner.run_quantum_engine(width_angstroms=1.2, barrier_ev=0.4, substrate_energy_ev=0.5) == 1.0
        
    def test_distance_decay_monotonicity(self, runner):
        """Widening transfer space vectors must compute a lower quantum tunneling transmission score."""
        narrow = runner.run_quantum_engine(width_angstroms=1.0, barrier_ev=0.6, substrate_energy_ev=0.1)
        wide = runner.run_quantum_engine(width_angstroms=2.0, barrier_ev=0.6, substrate_energy_ev=0.1)
        assert narrow > wide
        
    @pytest.mark.parametrize("w,b,e", [
        (-1.2, 0.6, 0.1),  # Invalid negative width distance parameter
        (1.2, -0.6, 0.1),  # Invalid negative barrier energy parameter
        (0.0, 0.6, 0.1),   # Invalid zero space limit threshold
        (1.2, 0.6, -0.1)   # Invalid negative substrate energy threshold
    ])
    def test_unphysical_input_exceptions(self, runner, w, b, e):
        """Ensures math edge-case boundary errors correctly raise a ValueError."""
        with pytest.raises(ValueError):
            runner.run_quantum_engine(width_angstroms=w, barrier_ev=b, substrate_energy_ev=e)

class TestAIInferenceEngineModule:
    """Verifies output analytical metrics returning from transformer workflows."""
    
    def test_ai_matrix_dimensions_and_sorting(self, runner):
        """Validates that matrix scoring evaluations generate correctly sized tables."""
        df = runner.run_ai_engine("WHVLI")
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ['Candidate', 'Score']
        assert len(df) == 20
        assert df['Score'].is_monotonic_decreasing

def test_integration_pipeline_cohesion(runner):
    """End-to-end multi-engine coordination data connectivity check."""
    active_seq = runner.extract_active_site_sequence()
    assert isinstance(active_seq, str)
    assert len(active_seq) >= 5
    
    quantum_coefficient = runner.run_quantum_engine(width_angstroms=1.2, barrier_ev=0.6, substrate_energy_ev=0.1)
    ai_matrix = runner.run_ai_engine(active_seq)
    
    assert quantum_coefficient <= 1.0
    assert not ai_matrix.empty
