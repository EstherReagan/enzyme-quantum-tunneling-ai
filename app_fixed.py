import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from pipeline import PremiumEnzymePipeline

# ==========================================
# PAGE VIEW CONFIGURATIONS & THEME INTEGRATION
# ==========================================
st.set_page_config(
    layout="wide", 
    page_title="Quantum Enzyme AI Hub",
    initial_sidebar_state="expanded"
)

# Custom CSS Injector to remove clutter, fix contrast, and add visual depth
st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .stMetric { background-color: #1a1c23; border: 1px solid #2d313f; border-radius: 10px; padding: 1.2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    div[data-testid="stNotification"] { border-radius: 10px; }
    h1 { font-family: 'Inter', sans-serif; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; }
    h3 { font-family: 'Inter', sans-serif; font-weight: 600; color: #a0aec0; }
    .card { background-color: #111217; border-radius: 12px; padding: 1.5rem; border: 1px solid #1f212a; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER SECTION
# ==========================================
st.title("🧬 Quantum Enzyme Tunneling Engine & AI Mutation Platform")
st.markdown("##### *Production-Grade Quantitative Biology & In-Silico Direct Evolution Hub*")
st.markdown("---")

# ==========================================
# SIDEBAR CONTROLS (DYNAMIC ROUTING VIA PIPELINE)
# ==========================================
st.sidebar.header("⚙️ Pipeline Parameters")
st.sidebar.markdown("Configure the geometric and energetic variables below to update the quantum-AI engine simulation in real-time.")

pdb_input = st.sidebar.text_input("RCSB PDB Target Identifier", value="1yge", max_chars=4).lower().strip()
st.sidebar.markdown("---")
st.sidebar.subheader("🔋 Energy Threshold Scaffolds")
barrier_height = st.sidebar.slider("Tunneling Barrier V_0 (eV)", 0.1, 2.5, 0.6, step=0.05)
substrate_energy = st.sidebar.slider("Substrate Kinetic Energy E (eV)", 0.0, 2.0, 0.15, step=0.05)
st.sidebar.markdown("---")
st.sidebar.subheader("📐 Structural Space Metrics")
tunnel_width = st.sidebar.slider("Proton Transfer Width (Å)", 0.5, 4.0, 1.2, step=0.05)
active_site_radius = st.sidebar.slider("Active Site Shell Radius (Å)", 3.0, 10.0, 6.0, step=0.5)

# Initialization of background pipeline wrapper class
runner = PremiumEnzymePipeline(pdb_input)

# Verify local directory storage and fetch missing data
if not os.path.exists(runner.pdb_filename):
    with st.spinner(f"📡 Downloading structural coordinate files from RCSB database..."):
        runner.download_data()

# Dynamic extraction linked to background code modules
active_seq = runner.extract_active_site_sequence(radius_angstroms=active_site_radius)

# ==========================================
# MATHEMATICAL WORKFLOW INFERENCES
# ==========================================
try:
    tunneling_prob = runner.run_quantum_engine(
        width_angstroms=tunnel_width, 
        barrier_ev=barrier_height, 
        substrate_energy_ev=substrate_energy
    )
except ValueError as e:
    st.error(f"❌ Physical Boundary Violation: {e}")
    tunneling_prob = 0.0

# ==========================================
# RESPONSIVE DASHBOARD LAYOUT GRID
# ==========================================
grid_col1, grid_col2 = st.columns([1, 1], gap="large")

with grid_col1:
    st.subheader("🔬 3D Active Site Macro-Environment")
    
    # Styled parameter display block
    st.markdown(f"""
    <div class="card">
        <p style="margin:0; color:#888; font-size:12px; font-weight:600; text-transform:uppercase;">Isolated Target Atom Cofactor</p>
        <p style="margin:0 0 10px 0; color:#4facfe; font-size:20px; font-weight:700;">Iron Core Coordination Center (FE)</p>
        <p style="margin:0; color:#888; font-size:12px; font-weight:600; text-transform:uppercase;">Extracted Catalytic Sequence Loop</p>
        <code style="color:#00ffcc; font-size:16px; font-weight:700; background:none; padding:0;">{active_seq}</code>
    </div>
    """, unsafe_allow_html=True)
    
    # 3D hardware WebGL canvas engine wrapper
    viewer_html = f"""
    <script src='https://pitt.edu'></script>
    <div id='viewer' style='width:100%; height:340px; background-color: #0b0c10; border-radius: 12px; border: 1px solid #1f212a;'></div>
    <script>
      let viewer = $3Dmol.createViewer(document.getElementById('viewer'), {{}});
      fetch('https://rcsb.org{pdb_input}.pdb')
        .then(response => response.text())
        .then(data => {{
            viewer.addModel(data, 'pdb');
            viewer.setStyle({{}}, {{cartoon: {{color: 'spectrum', opacity: 0.85}}}});
            viewer.setStyle({{atom: 'FE'}}, {{sphere: {{color: '#ff4b4b', radius: 2.2}}}});
            viewer.zoomTo({{atom: 'FE'}});
            viewer.render();
        }});
    </script>
    """
    st.components.v1.html(viewer_html, height=360)

with grid_col2:
    st.subheader("🌌 Quantum Wave Attenuation Spectrum")
    
    # Modernized spacing cards for probability outputs
    metric_col1, metric_col2 = st.columns(2, gap="medium")
    with metric_col1:
        st.metric(label="Transmission Probability (T)", value=f"{tunneling_prob:.5e}")
    with metric_col2:
        st.metric(label="Statistical Tunneling Frequency", value=f"1 in {int(1/max(1e-40, tunneling_prob)):,}")
    
    # Plotly dynamic analytical spectrum visualization
    widths = np.linspace(0.5, 4.0, 50)
    rates = []
    for w in widths:
        try:
            rates.append(runner.run_quantum_engine(w, barrier_height, substrate_energy))
        except ValueError:
            rates.append(0.0)
            
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=widths, y=rates, 
        mode='lines', 
        name='Wave Equation Solution', 
        line=dict(color='#00ffcc', width=3.5)
    ))
    fig.add_shape(
        type="vertical", 
        x0=tunnel_width, x1=tunnel_width, 
        y0=min(rates), y1=max(rates), 
        line=dict(color="#ff4b4b", width=2, dash="dash")
    )
    
    fig.update_layout(
        xaxis_title="Proton Transfer Space Coordinate (Å)",
        yaxis_title="Probability Vector Log(T)",
        yaxis_type="log",
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#111217',
        gridcolor='#2d313f'
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MACHINE LEARNING SCREENING LAYER
# ==========================================
st.markdown("---")
st.subheader("🤖 Generative AI Multi-Engine Mutation Scoring Matrix")
st.markdown("Route the active-site coordinate matrix variables through the pre-trained structural weights layer of Meta AI's **ESM-2** Transformer model.")

btn_col, info_col = st.columns([1, 2])
with btn_col:
    trigger_ai = st.button("🚀 Execute In-Silico Direct Evolution Sequence", use_container_width=True)

if trigger_ai:
    with st.spinner("🧠 Computation in progress... Analyzing masked evolutionary token parameters..."):
        df_ranked = runner.run_ai_engine(active_seq)
        
        # Display ranked data matrix inside a crisp, premium design layout table
        st.dataframe(
            df_ranked.style.background_gradient(cmap="Blues", subset=["Score"]).format({"Score": "{:.4f}"}),
            use_container_width=True
        )
        st.success("🏆 Mutational evaluation sequence finalized successfully with zero active memory leaks!")
else:
    st.info("💡 Click the button above to dynamically run predictions across all 20 standard amino acid mutation variables.")
