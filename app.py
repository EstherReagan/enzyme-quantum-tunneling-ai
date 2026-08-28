import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from pipeline import PremiumEnzymePipeline

# ==========================================
# PAGE VIEWS & DEEP TECH CYBER LAYOUT
# ==========================================
st.set_page_config(
    layout="wide", 
    page_title="QUANTUM ENZYME MATRIX v1.0",
    initial_sidebar_state="collapsed"
)

# Enterprise Sci-Fi Cyber UI Theme Stylesheet
st.markdown("""
<style>
    /* Base Global Dark Space Styles */
    @import url('https://googleapis.com');
    
    .stApp { background-color: #06070d; color: #a5b4fc; }
    .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; max-width: 95%; }
    
    /* Neon Cyber HUD Container Cards */
    .hud-card {
        background: linear-gradient(180deg, rgba(10, 15, 30, 0.85) 0%, rgba(5, 7, 15, 0.95) 100%);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.05), inset 0 0 15px rgba(0, 242, 254, 0.02);
        margin-bottom: 1.25rem;
    }
    
    .hud-card-accent {
        border-top: 3px solid #00f2fe !important;
    }
    
    .hud-card-green {
        border: 1px solid rgba(0, 255, 157, 0.15);
        box-shadow: 0 0 20px rgba(0, 255, 157, 0.05);
    }
    
    /* Deep Tech Minimal Numerical Matrices */
    .tech-metric-panel {
        background: rgba(0, 0, 0, 0.4);
        border-left: 3px solid #00f2fe;
        padding: 0.75rem 1rem;
        border-radius: 0 6px 6px 0;
        margin-bottom: 0.75rem;
    }
    
    /* Specialized Typography Overrides */
    .tech-title { font-family: 'Orbitron', sans-serif; font-weight: 700; color: #ffffff; letter-spacing: 2px; text-transform: uppercase; text-shadow: 0 0 10px rgba(0,242,254,0.3); margin: 0; }
    .tech-subtitle { font-family: 'Share Tech Mono', monospace; color: #00f2fe; font-size: 13px; letter-spacing: 1px; margin-bottom: 1.5rem; }
    .section-header { font-family: 'Orbitron', sans-serif; font-size: 14px; font-weight: 700; color: #ffffff; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 1rem; padding-bottom: 0.25rem; border-bottom: 1px solid rgba(255,255,255,0.08); }
    
    /* Clean System Parameter Sliders */
    .stSlider label, .stTextInput label { font-family: 'Share Tech Mono', monospace !important; color: #8492a6 !important; text-transform: uppercase; font-size: 11px !important; letter-spacing: 0.5px; }
    
    /* Data Grid Adjustments */
    div[data-testid="stDataFrame"] { border: 1px solid rgba(0, 242, 254, 0.1) !important; border-radius: 6px; }
    
    /* Interactive Status Indicators */
    .status-badge { font-family: 'Share Tech Mono', monospace; font-size: 10px; background: rgba(0, 255, 157, 0.1); color: #00ff9d; padding: 2px 6px; border-radius: 3px; border: 1px solid rgba(0, 255, 157, 0.2); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SYSTEM HEADER STATUS HEADER
# ==========================================
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(0,242,254,0.1); padding-bottom: 0.75rem;">
    <div>
        <h1 class="tech-title">🧬 Quantum Enzyme Analytics Workspace</h1>
        <p class="tech-subtitle">SYSTEM STATUS: ACTIVE // ENGINE MATRIX VER v1.0.3 // REAGAN CO-PILOT PIPELINE</p>
    </div>
    <div>
        <span class="status-badge">🟢 CORE MODULE ONLINE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# INTEGRATED APP PANEL CONTROLS (UNIFIED CONSOLE)
# ==========================================
st.markdown('<div class="hud-card hud-card-accent">', unsafe_allow_html=True)
st.markdown("<p style='font-family:\"Orbitron\", sans-serif; font-size:12px; font-weight:700; color:#ffffff; margin-top:0; margin-bottom:1rem; letter-spacing:1px;'>🎛️ HUD INTERFACE RUNTIME CONTROLS</p>", unsafe_allow_html=True)

ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3, gap="medium")

with ctrl_col1:
    pdb_input = st.text_input("🧬 Target Accession PDB ID", value="1yge", max_chars=4).lower().strip()
    active_site_radius = st.slider("📐 Shell Extraction Radius (Å)", 3.0, 10.0, 6.0, step=0.5)

with ctrl_col2:
    barrier_height = st.slider("🔋 Potential Barrier Max V_0 (eV)", 0.1, 2.5, 0.6, step=0.05)
    substrate_energy = st.slider("⚡ Particle Kinetic State E (eV)", 0.0, 2.0, 0.15, step=0.05)

with ctrl_col3:
    tunnel_width = st.slider("⚛️ Quantum Tunneling Width (Å)", 0.5, 4.0, 1.2, step=0.05)

st.markdown('</div>', unsafe_allow_html=True)

# Pipeline computational backend loading orchestration
runner = PremiumEnzymePipeline(pdb_input)

if not os.path.exists(runner.pdb_filename):
    with st.spinner("📡 Fetching coordinate parameters from PDB data bank..."):
        runner.download_data()

active_seq = runner.extract_active_site_sequence(radius_angstroms=active_site_radius)

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
# MAIN HUD DATA VIEW GRID ARCHITECTURE
# ==========================================
grid_col1, grid_col2 = st.columns(2, gap="large")

with grid_col1:
    st.markdown('<div class="hud-card" style="height: 520px;">', unsafe_allow_html=True)
    st.markdown("<div class='section-header'>🔬 Active Structural Core Geometry</div>", unsafe_allow_html=True)
    
    # Grid parameter arrays
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.markdown(f"""
        <div class="tech-metric-panel">
            <span style="font-family:'Share Tech Mono', monospace; font-size:10px; color:#718096; display:block;">TARGET COFACTOR</span>
            <span style="font-family:'Orbitron', sans-serif; font-size:14px; font-weight:700; color:#ffffff;">Iron Center (FE)</span>
        </div>
        """, unsafe_allow_html=True)
    with sub_col2:
        st.markdown(f"""
        <div class="tech-metric-panel" style="border-left-color: #00ff9d;">
            <span style="font-family:'Share Tech Mono', monospace; font-size:10px; color:#718096; display:block;">SEQUENCE MOTIF</span>
            <span style="font-family:'Share Tech Mono', monospace; font-size:14px; font-weight:700; color:#00ff9d;">{active_seq}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # 3D hardware WebGL coordinate matrix layout viewer
    viewer_html = f"""
    <script src='https://pitt.edu'></script>
    <div id='viewer' style='width:100%; height:320px; background-color: #08090d; border-radius: 6px; border: 1px solid rgba(0,242,254,0.1);'></div>
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
    st.components.v1.html(viewer_html, height=330)
    st.markdown('</div>', unsafe_allow_html=True)

with grid_col2:
    st.markdown('<div class="hud-card" style="height: 520px;">', unsafe_allow_html=True)
    st.markdown("<div class='section-header'>🌌 Real-Time Quantum Wave Attenuation Spectrum</div>", unsafe_allow_html=True)
    
    # Modernized science layout panels
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown(f"""
        <div class="tech-metric-panel">
            <span style="font-family:'Share Tech Mono', monospace; font-size:10px; color:#718096; display:block;">TRANSMISSION COEFFICIENT (T)</span>
            <span style="font-family:'Orbitron', sans-serif; font-size:16px; font-weight:700; color:#00f2fe;">{tunneling_prob:.5e}</span>
        </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""
        <div class="tech-metric-panel" style="border-left-color: #ff4b4b;">
            <span style="font-family:'Share Tech Mono', monospace; font-size:10px; color:#718096; display:block;">PROBABILITY SCALE RATIO</span>
            <span style="font-family:'Orbitron', sans-serif; font-size:15px; font-weight:700; color:#ff4b4b;">1 in {int(1/max(1e-40, tunneling_prob)):,}</span>
        </div>
        """, unsafe_allow_html=True)
        
    # Plotly analytical curve generation trace
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
        name='Schrödinger Solution Matrix', 
        line=dict(color='#00f2fe', width=3)
    ))
    
    fig.add_shape(
        type="line", 
        x0=tunnel_width, x1=tunnel_width, 
        y0=min(rates) if rates else 1e-40, y1=max(rates) if rates else 1.0, 
        line=dict(color="#ff4b4b", width=1.5, dash="dot")
    )
    
    fig.update_layout(
        xaxis=dict(
            title=dict(text="TRANSFER SHELL DISTANCE (Å)", font=dict(family='Share Tech Mono', size=11, color='#8492a6')),
            gridcolor='rgba(0,242,254,0.05)', 
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text="ATTENUATION VECTOR LOG(T)", font=dict(family='Share Tech Mono', size=11, color='#8492a6')),
