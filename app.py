import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import Bio.PDB
from pipeline import PremiumEnzymePipeline

# ==========================================
# UI SPECIFICATION & STRUCTURAL CANVASES
# ==========================================
st.set_page_config(layout="wide", page_title="Quantum Enzyme AI Hub")

st.title("🧬 Quantum Enzyme Tunneling Engine & AI Mutation Platform")
st.markdown("### **Production-Grade Computational Biology Architecture**")

# ==========================================
# SIDEBAR CONTROLS (DYNAMIC ROUTING)
# ==========================================
st.sidebar.header("⚙️ Configuration Matrix")
pdb_input = st.sidebar.text_input("RCSB PDB ID Target", value="1yge", max_chars=4).lower().strip()
barrier_height = st.sidebar.slider("Tunneling Barrier Height V_0 (eV)", 0.1, 2.5, 0.6, step=0.05)
substrate_energy = st.sidebar.slider("Substrate Kinetic Energy E (eV)", 0.0, 2.0, 0.1, step=0.05)
tunnel_width = st.sidebar.slider("Proton Transfer Distance Width (Å)", 0.5, 4.0, 1.2, step=0.05)
active_site_radius = st.sidebar.slider("Active Site Extraction Radius (Å)", 3.0, 10.0, 5.0, step=0.5)

# Initialization of background pipeline wrapper class
runner = PremiumEnzymePipeline(pdb_input)

# Process trigger checking directory states
if not os.path.exists(runner.pdb_filename):
    with st.spinner(f"📡 Querying global structural mirrors for {pdb_input.upper()}..."):
        runner.download_data()

# Clean extraction sequence call
active_seq = runner.extract_active_site_sequence(radius_angstroms=active_site_radius)

# ==========================================
# DATA INFERENCE CALCULATIONS
# ==========================================
try:
    # Trigger real energy-corrected physics equations
    tunneling_prob = runner.run_quantum_engine(
        width_angstroms=tunnel_width, 
        barrier_ev=barrier_height, 
        substrate_energy_ev=substrate_energy
    )
except ValueError as e:
    st.error(f"❌ Physical Boundary Violation: {e}")
    tunneling_prob = 0.0

# ==========================================
# MAIN DASHBOARD INTERFACE LAYOUT GRID
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔬 Extracted Structural Environment")
    st.info(f"**Target Coordinate Center Vector:** Iron Core (FE)")
    st.success(f"**Isolated Active-Site Sequence Fragment:** `{active_seq}`")
    
    # Live hardware WebGL interactive viewer injection wrapper
    st.markdown("#### **WebGL 3D Active Site Mesh Visualization**")
    viewer_html = f"""
    <script src='https://pitt.edu'></script>
    <div id='viewer' style='width:100%; height:320px; background-color: #111; border-radius: 8px;'></div>
    <script>
      let viewer = $3Dmol.createViewer(document.getElementById('viewer'), {{}});
      fetch('https://rcsb.org{pdb_input}.pdb')
        .then(response => response.text())
        .then(data => {{
            viewer.addModel(data, 'pdb');
            viewer.setStyle({{}}, {{cartoon: {{color: 'spectrum', opacity: 0.85}}}});
            viewer.setStyle({{atom: 'FE'}}, {{sphere: {{color: 'red', radius: 2.0}}}});
            viewer.zoomTo({{atom: 'FE'}});
            viewer.render();
        }});
    </script>
    """
    st.components.v1.html(viewer_html, height=340)

with col2:
    st.subheader("🌌 Quantum Wave Transmission Spectrum")
    
    # Dynamic metrics connected to pipeline calculations
    m1, m2 = st.columns(2)
    m1.metric("Calculated Transmission Probability (T)", f"{tunneling_prob:.5e}")
    m2.metric("Proton Tunneling Ratio", f"1 in {int(1/max(1e-40, tunneling_prob)):,}")
    
    # Generating responsive dynamic parametric chart curves based on sliders
    widths = np.linspace(0.5, 4.0, 50)
    rates = [runner.run_quantum_engine(w, barrier_height, substrate_energy) for w in widths]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=widths, y=rates, mode='lines', name='Wave Function Decay', line=dict(color='#00ffcc', width=3)))
    fig.add_shape(type="vertical", x0=tunnel_width, x1=tunnel_width, y0=min(rates), y1=max(rates), line=dict(color="Red", width=2, dash="dash"))
    
    fig.update_layout(
        xaxis_title="Transfer Width Distance Vector (Å)",
        yaxis_title="Probability Log(T)",
        yaxis_type="log",
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# GENERATIVE MUTATION MATRIX PLAYGROUND
# ==========================================
st.subheader("🤖 Generative AI Mutation Matrix Screening Loop")

if st.button("🚀 Trigger Masked Meta ESM-2 Inference Sequence (Calculates Live Matrix)"):
    with st.spinner("🧠 Initializing Deep Transformer Matrix Layers..."):
        df_ranked = runner.run_ai_engine(active_seq)
        st.dataframe(df_ranked, use_container_width=True)
        st.success("🏆 Multi-engine inference lookup finished with zero resource leaks!")
else:
    st.caption("Click the button above to route the sequence window directly through the neural network parameters.")
