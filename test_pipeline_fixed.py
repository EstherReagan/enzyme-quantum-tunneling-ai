import pytest
import numpy as np
import os
import pandas as pd
from pipeline import PremiumEnzymePipeline

@pytest.fixture
def runner():
    """Initializes the baseline evaluation test platform class."""
    return PremiumEnzymePipeline("1yge")

class TestEnzymeQuantumEngine:
    """Rigorous scientific matrix check validating wave calculation functions."""
    
    def test_zero_barrier_saturation(self, runner):
        """Zero barrier potential configurations must evaluate to a transmission coefficient of 1.0."""
        assert runner.run_quantum_engine(width_angstroms=1.2, barrier_ev=0.0, substrate_energy_ev=0.0) == 1.0

    def test_kinetic_energy_saturation(self, runner):
        """Particle kinetic energy matching or exceeding the barrier energy must evaluate to 1.0."""
        assert runner.run_quantum_engine(width_angstroms=1.2, barrier_ev=0.4, substrate_energy_ev=0.5) == 1.0
        
    def test_distance_decay_monotonicity(self, runner):
        """Increasing spatial tunnel gap widths must enforce a smaller transmission coefficient."""
        narrow = runner.run_quantum_engine(width_angstroms=1.0, barrier_ev=0.6, substrate_energy_ev=0.1)
        wide = runner.run_quantum_engine(width_angstroms=2.0, barrier_ev=0.6, substrate_energy_ev=0.1)
        assert narrow > wide
        
    @pytest.mark.parametrize("w,b,e", [
        (-1.2, 0.6, 0.1),  # Invalid negative width distance
        (1.2, -0.6, 0.1),  # Invalid negative barrier vector energy
        (0.0, 0.6, 0.1),   # Invalid zero distance limit
        (1.2, 0.6, -0.1)   # Invalid negative substrate energy
    ])
    def test_unphysical_input_aborts(self, runner, w, b, e):
        """Ensures input anomalies are cleanly identified via ValueError exceptions."""
        with pytest.raises(ValueError):
            runner.run_quantum_engine(width_angstroms=w, barrier_ev=b, substrate_energy_ev=e)

def test_ai_matrix_dataframe_dimensions(runner):
    """Verifies that the analytical array mapping returns correctly structured columns."""
    df = runner.run_ai_engine("WHVLI")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ['Candidate', 'Score']
    assert len(df) == 20
    assert df['Score'].is_monotonic_decreasing
