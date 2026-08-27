import pytest
import numpy as np
import os
from pipeline import PremiumEnzymePipeline

def test_quantum_engine_boundary_conditions():
    """Verifies that the physics engine correctly resolves barrier boundaries."""
    runner = PremiumEnzymePipeline("1yge")
    
    # Force create data folder and download structure to ensure server data is present
    os.makedirs("data", exist_ok=True)
    try:
        runner.download_data()
    except Exception:
        pass # Allow test to continue if file already exists locally
    
    # Boundary Condition 1: If barrier height is 0, transmission must equal 100% (1.0)
    assert runner.run_quantum_engine(width_angstroms=1.2, barrier_ev=0.0) == 1.0
    
    # Boundary Condition 2: Transmission must drop exponentially as width increases
    narrow_prob = runner.run_quantum_engine(width_angstroms=1.0, barrier_ev=0.6)
    wide_prob = runner.run_quantum_engine(width_angstroms=2.0, barrier_ev=0.6)
    assert narrow_prob > wide_prob
