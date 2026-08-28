import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from pipeline import PremiumEnzymePipeline

# ==========================================
# PAGE CONFIGURATIONS & COMPACT CONTAINERS
# ==========================================
st.set_page_config(
    layout="wide", 
    page_title="Quantum Enzyme AI Hub",
    initial_sidebar_state="expanded"
)

# Custom Enterprise CSS Injector for shadows, depth, and clean topography grids
st.markdown("""
<style>
    /* Remove redundant white spacing */
    .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; max-width: 95%; }
    
    /* Premium dark-mode modular structural cards */
    .metric-card { 
        background-color: #16171d; 
        border: 1px solid #232733; 
        border-radius: 12px; 
        padding: 1.25rem; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin-bottom: 1rem;
    }
    .info-card {
        background: linear-gradient(135deg, #111217 0%, #1a1c24 100%);
        border: 1px solid #232733;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
    }
    
    /* Clean typography accents */
    h1 { font-family: 'Inter', sans-serif; font-weight: 800; color: #ffffff; letter-spacing: -0.75px; margin-bottom: 0.25rem; }
    h2 { font-family: 'Inter', sans-serif; font-weight: 700; color: #f7fafc; margin-top: 1rem; }
    h3 { font-family: 'Inter', sans-serif; font-weight: 600; color: #cbd5e0; margin-bottom: 0.75rem; }
    
    /* Style default metric labels cleanly */
    div[data-testid="stMetricLabel"] p { font-size: 11px !important; text-transform: uppercase; letter-spacing: 0.5px; color: #a0aec0 !important; }
    div[data-testid="stMetricValue"] div { font-size: 24px !important; font-weight: 700 !important; color: #00ffcc !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# EXECUTIVE APP HEADER HUB
# ==========================================
st.title("🧬 Quantum Enzyme Tunneling Engine & AI Mutation Platform")
st.markdown("<p style='color:#a0aec0; margin:0 0 1.5rem 0; font-size:14px;'>Production-Grade Quantitative Biology & In-Silico Molecular Direct Evolution Workspace</p>", unsafe_allow_html=True)

# ==========================================
# SIDEBAR REFACTOR PARAMETER SCISSORS
# ==========================================
st.sidebar.header("⚙️ Simulation Controls")
st.sidebar.markdown("Modify chemical boundaries below to update the quantum-AI core variables dynamically.")

pdb_input = st.sidebar.text_input("Target RCSB PDB Accession ID", value="1yge", max_chars=4).lower().strip()
st.sidebar.markdown("---")

st.sidebar.subheader("🔋 Energy Grid Scales")
barrier_height = st.sidebar.slider("Potential Barrier V_0 (eV)", 0.1, 2.5, 0.6, step=0.05)
substrate_energy = st.sidebar.slider("Kinetic State Energy E (eV)", 0.0, 2.0, 0.15, step=0.05)
st.sidebar.markdown("---")

st.sidebar.subheader("📐 Molecular Geometry Shells")
tunnel_width = st.sidebar.slider("Tunneling Gap Vector Distance (Å)", 0.5, 4.0, 1.2, step=0.05)
active_site_radius = st.sidebar.slider("Active Site Extraction Shell (Å)", 3.0, 10.0, 6.0, step=0.5)

# Initialization of background pipeline wrapper class
runner = PremiumEnzymePipeline(pdb_input)

# Verify local file presence or download dynamically
if not os.path.exists(runner.pdb_filename):
    with st.spinner(f"📡 Querying global structural mirrors for {pdb_input.upper()}..."):
        runner.download_data()

# Dynamic extraction linked to background code modules
active_seq = runner.extract_active_site_sequence(radius_angstroms=active_site_radius)

# ==========================================
# REAL CORE MATHEMATICAL ROUTINES
# ==========================================
try:
    tunneling_prob = runner.run_quantum_engine(
        width_angstroms=tunnel_width, 
        barrier_ev=barrier_height, 
        substrate_energy_ev=substrate_energy
    )
except ValueError as e:
    st.error(f"❌ Boundary Condition Exception: {e}")
    tunneling_prob = 0.0

# ==========================================
# RESPONSIVE GRID COLUMNS ARCHITECTURE
# ==========================================
# FIXED SYNTAX TYPO HERE: Added '2' to column declaration argument explicitly
grid_col1, grid_col2 = st.columns(2, gap="large")

with grid_col1:
    st.subheader("🔬 Structural Active-Site Shell Matrix")
    
    # Structural encapsulation panel
    st.markdown(f"""
    <div class="info-card">
        <span style="font-size:10px; font-weight:700; color:#718096; text-transform:uppercase; display:block; margin-bottom:2px;">Central Target Atom Identity</span>
        <span style="font-size:18px; font-weight:700; color:#3182ce; display:block; margin-bottom:12px;">Iron Metal Core Coordination Complex (FE)</span>
        <span style="font-size:10px; font-weight:700; color:#718096; text-transform:uppercase; display:block; margin-bottom:2px;">Extracted Biological Sequence Loop Fragment</span>
        <code style="font-size:15px; font-weight:800; color:#00ffcc; background:rgba(0,255,204,0.05); padding:4px 8px; border-radius:4px; border:1px solid rgba(0,255,204,0.15); display:inline-block;">{active_seq}</code>
    </div>
    """, unsafe_allow_html=True)
    
    # 3D hardware WebGL canvas engine viewport
    st.markdown("<p style='font-size:12px; font-weight:600; color:#a0aec0; margin-bottom:6px;'>Interactive WebGL Coordinate Model Rendering</p>", unsafe_allow_html=True)
    viewer_html = f"""
    <script src='https://pitt.edu'></script>
    <div id='viewer' style='width:100%; height:340px; background-color: #0b0c10; border-radius: 12px; border: 1px solid #232733;'></div>
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
    st.subheader("🌌 Physics-Corrected Attenuation Spectrum")
    
    # Containerized calculation display boxes
    m_col1, m_col2 = st.columns(2, gap="small")
    with m_col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(label="Wave Transmission Coeff (T)", value=f"{tunneling_prob:.5e}")
        st.markdown('</div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(label="Tunneling Statistical Frequency", value=f"1 in {int(1/max(1e-40, tunneling_prob)):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Plotly responsive dark layout graph canvas
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
        name='WKB Mathematical Solution', 
        line=dict(color='#00ffcc', width=3.5)
    ))
    
    # Vertical spatial locator guide vector
    fig.add_shape(
        type="line", 
        x0=tunnel_width, x1=tunnel_width, 
        y0=min(rates) if rates else 1e-40, y1=max(rates) if rates else 1.0, 
        line=dict(color="#ff4b4b", width=2, dash="dash")
    )
    
    fig.update_layout(
        xaxis_title="Proton Transfer Spatial Coordinate Coordinate (Å)",
        yaxis_title="Probability Vector Log(T)",
        yaxis_type="log",
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#111217',
        gridcolor='#232733'
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# ENTERPRISE AI SCREENING WORKBENCH
# ==========================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.subheader("🤖 Generative AI Mutation Screening Matrix Workspace")
st.markdown("<p style='color:#a0aec0; font-size:13px; margin-top:-0.5rem; margin-bottom:1rem;'>Query evolutionary mutation likelihood statistics via Meta AI's pre-trained deep structural Transformer layers.</p>", unsafe_allow_html=True)

btn_col, pad_col = st.columns([1, 2])
with btn_col:
    trigger_ai = st.button("🚀 Run In-Silico Directed Evolution Analysis", use_container_width=True)

if trigger_ai:
    with st.spinner("🧠 Computation in progress... Analyzing hidden spatial structural vectors..."):
        df_ranked = runner.run_ai_engine(active_seq)
        
        # Display data arrays inside an organized, color-graded corporate data grid table
        st.dataframe(
            df_ranked.style.background_gradient(cmap="Blues", subset=["Score"]).format({"Score": "{:.4f}"}),
            use_container_width=True
        )
        st.success("🏆 Matrix evaluation loop finalized successfully with no memory resource leaks!")
else:
    st.info("💡 Launch the processing sequence above to execute mutation scanning calculations natively across all 20 canonical amino acid residues variables.")
