import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from pipeline import PremiumEnzymePipeline

# ==========================================
# PAGE VIEWS & DARK SAPPHIRE CUSTOM ENGINE THEME
# ==========================================
st.set_page_config(
    layout="wide", 
    page_title="Quantum Enzyme AI Hub",
    initial_sidebar_state="collapsed"
)

# Premium Custom CSS Injection for a sleek, enterprise SaaS interface
st.markdown("""
<style>
    /* Global Background Override */
    .stApp { background-color: #0d0e12; color: #f1f3f9; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 90%; }
    
    /* Elegant Dark Sapphire Glassmorphism Containers */
    .glass-card {
        background: rgba(20, 24, 33, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.75rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        margin-bottom: 1.5rem;
    }
    
    /* Premium Minimal Metrics */
    .premium-metric-box {
        background: linear-gradient(135deg, rgba(29, 36, 51, 0.5) 0%, rgba(17, 22, 31, 0.5) 100%);
        border: 1px solid rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: left;
    }
    
    /* Typography Overrides */
    h1 { font-family: 'Inter', sans-serif; font-weight: 800; color: #ffffff; letter-spacing: -1px; margin-bottom: 0.5rem; }
    h2 { font-family: 'Inter', sans-serif; font-weight: 700; color: #ffffff; margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 0.5rem; }
    h3 { font-family: 'Inter', sans-serif; font-weight: 600; color: #a0aec0; margin-bottom: 0.75rem; }
    
    /* Modern Form Elements Overrides */
    div[data-testid="stMetricLabel"] p { font-size: 11px !important; text-transform: uppercase; letter-spacing: 1px; color: #718096 !important; font-weight: 600; }
    div[data-testid="stMetricValue"] div { font-size: 26px !important; font-weight: 700 !important; color: #00f2fe !important; }
    
    /* Hide Default UI Artifacts */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# ENTERPRISE MASTER APP HEADER
# ==========================================
st.markdown("""
<div style="margin-bottom: 2.5rem;">
    <h1>Quantum Enzyme Tunneling Engine & AI Mutation Platform</h1>
    <p style="color:#718096; margin:0; font-size:14px; font-weight: 500; letter-spacing: 0.5px;">
        PRODUCTION-GRADE QUANTITATIVE BIOLOGY & IN-SILICO MOLECULAR DESIGN MATRIX
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# INTEGRATED APP PANEL CONTROLS (UNIFIED UI)
# ==========================================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("<h3 style='margin-top:0; color:#ffffff;'>🎛️ Simulation Parameters Control Console</h3>", unsafe_allow_html=True)

ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3, gap="medium")

with ctrl_col1:
    pdb_input = st.text_input("Target RCSB PDB Accession ID", value="1yge", max_chars=4).lower().strip()
    active_site_radius = st.slider("Active Site Extraction Shell (Å)", 3.0, 10.0, 6.0, step=0.5)

with ctrl_col2:
    barrier_height = st.slider("Potential Barrier V_0 (eV)", 0.1, 2.5, 0.6, step=0.05)
    substrate_energy = st.slider("Kinetic State Energy E (eV)", 0.0, 2.0, 0.15, step=0.05)

with ctrl_col3:
    tunnel_width = st.slider("Tunneling Gap Distance Vector (Å)", 0.5, 4.0, 1.2, step=0.05)

st.markdown('</div>', unsafe_allow_html=True)

# Background pipeline module orchestration initialization
runner = PremiumEnzymePipeline(pdb_input)

if not os.path.exists(runner.pdb_filename):
    with st.spinner("📡 Syncing biological parameters from global database mirrors..."):
        runner.download_data()

active_seq = runner.extract_active_site_sequence(radius_angstroms=active_site_radius)

try:
    tunneling_prob = runner.run_quantum_engine(
        width_angstroms=tunnel_width, 
        barrier_ev=barrier_height, 
        substrate_energy_ev=substrate_energy
    )
except ValueError as e:
    st.error(f"❌ Physical Boundary Condition Violation: {e}")
    tunneling_prob = 0.0

# ==========================================
# MAIN RESPONSE GRID ARCHITECTURE
# ==========================================
grid_col1, grid_col2 = st.columns(2, gap="large")

with grid_col1:
    st.markdown('<div class="glass-card" style="height: 520px;">', unsafe_allow_html=True)
    st.markdown("<h2 style='margin-top:0;'>🔬 Active Site Environment</h2>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
        <span style="font-size:11px; font-weight:600; color:#4a5568; text-transform:uppercase; display:block; letter-spacing:0.5px;">Catalytic Center Vector</span>
        <span style="font-size:16px; font-weight:700; color:#3182ce; display:block; margin-bottom:0.75rem;">Iron Coordination Complex (FE)</span>
        <span style="font-size:11px; font-weight:600; color:#4a5568; text-transform:uppercase; display:block; letter-spacing:0.5px;">Extracted Biological Motif Sequence</span>
        <code style="font-size:14px; font-weight:800; color:#00f2fe; background:rgba(0,242,254,0.04); padding:4px 8px; border-radius:6px; border:1px solid rgba(0,242,254,0.12); display:inline-block;">{active_seq}</code>
    </div>
    """, unsafe_allow_html=True)
    
    # Live WebGL Viewport Canvas Wrapper Mesh Injection
    viewer_html = f"""
    <script src='https://pitt.edu'></script>
    <div id='viewer' style='width:100%; height:300px; background-color: #0b0c10; border-radius: 10px; border: 1px solid rgba(255,255,255,0.03);'></div>
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
    st.components.v1.html(viewer_html, height=310)
    st.markdown('</div>', unsafe_allow_html=True)

with grid_col2:
    st.markdown('<div class="glass-card" style="height: 520px;">', unsafe_allow_html=True)
    st.markdown("<h2 style='margin-top:0;'>🌌 Wave Function Attenuation</h2>", unsafe_allow_html=True)
    
    # Modern display metrics grids
    m_col1, m_col2 = st.columns(2, gap="small")
    with m_col1:
        st.markdown('<div class="premium-metric-box">', unsafe_allow_html=True)
        st.metric(label="Transmission Coefficient (T)", value=f"{tunneling_prob:.5e}")
        st.markdown('</div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown('<div class="premium-metric-box">', unsafe_allow_html=True)
        st.metric(label="Statistical Tunnel Frequency", value=f"1 in {int(1/max(1e-40, tunneling_prob)):,}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Generating Plotly spectra trace arrays cleanly
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
        name='WKB Wave Mechanics', 
        line=dict(color='#00f2fe', width=3.5)
    ))
    
    fig.add_shape(
        type="line", 
        x0=tunnel_width, x1=tunnel_width, 
        y0=min(rates) if rates else 1e-40, y1=max(rates) if rates else 1.0, 
        line=dict(color="#ff4b4b", width=1.5, dash="dash")
    )
    
    fig.update_layout(
        xaxis=dict(
            title="Transfer Space Vector Coordinate (Å)", 
            gridcolor='rgba(255,255,255,0.05)', 
            zeroline=False
        ),
        yaxis=dict(
            title="Probability Coefficient Log(T)", 
            type="log", 
            gridcolor='rgba(255,255,255,0.05)', 
            zeroline=False
        ),
        height=280,
        margin=dict(l=10, r=10, t=10, b=10),
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# IN-SILICO GENERATIVE MACHINE LEARNING GRID
# ==========================================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("<h2 style='margin-top:0;'>🤖 Deep Learning Evolutionary Mutation Engine Workspace</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#718096; font-size:13px; margin-top:-0.5rem; margin-bottom:1.5rem;'>Perform zero-shot mutation screening loops using the structural parameter grids of Meta AI's pre-trained ESM-2 Transformer network layers.</p>", unsafe_allow_html=True)

btn_col, dl_col = st.columns(2, gap="medium")
with btn_col:
    trigger_ai = st.button("🚀 Run In-Silico Directed Evolution Analysis", use_container_width=True)

if trigger_ai:
    with st.spinner("🧠 Computation active... Evaluating structural matrix probability states..."):
        df_ranked = runner.run_ai_engine(active_seq)
        
        # Display data arrays inside an organized layout matrix frame
        st.dataframe(
            df_ranked.style.background_gradient(cmap="Blues", subset=["Score"]).format({"Score": "{:.4f}"}),
            use_container_width=True
        )
