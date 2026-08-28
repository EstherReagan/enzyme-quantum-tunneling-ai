import streamlit as st
from streamlit_echarts import st_echarts
from stmol import make_with_py3dmol
import py3Dmol

# ==============================================================================
# 1. ARCHITECTURAL LAYOUT & CSS HARD-RESET
# ==============================================================================
st.set_page_config(
    page_title="CRETAX // QUANTUM ENZYME AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom injection to keep spacing structured, clean, and perfectly aligned
st.markdown("""
    <style>
    /* Dark Matte Canvas Minimalist Base */
    .stApp {
        background-color: #0B0C10;
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    
    header, footer {visibility: hidden;}
    
    /* Spacious Modular Box Blocks */
    .premium-panel {
        background-color: #12131C;
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    /* Clean Typography Grid */
    .panel-tag {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #64748B;
        margin-bottom: 8px;
    }
    
    .panel-title {
        font-size: 20px;
        font-weight: 600;
        letter-spacing: -0.5px;
        color: #FFFFFF;
        margin-bottom: 20px;
    }
    
    /* Micro-Analytics Metrics */
    .stat-container {
        padding: 12px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }
    .stat-num {
        font-size: 32px;
        font-weight: 700;
        color: #00E5FF;
        font-family: monospace;
    }
    .stat-lbl {
        font-size: 11px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)

# Top Premium Brand Bar
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 30px;">
        <div style="font-weight: 800; letter-spacing: 2px; color: #FFFFFF;">✕ CRETAX <span style='color:#64748B; font-weight:300; font-size:13px;'> | QUANTUM TUNNELING ENGINE</span></div>
        <div style='color: #00FFCC; font-size: 12px; font-family: monospace; background: rgba(0,255,204,0.08); padding: 4px 12px; border-radius: 20px;'>CORE SYNC ACTIVE</div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. DATA LAYER (Real Enzyme Configuration Input)
# ==============================================================================
# Letting users input real PDB database identifiers to make it functional
with st.sidebar:
    st.markdown("### Molecular Dataset Config")
    pdb_code = st.text_input("Protein Data Bank (PDB) Code", value="1AIL", max_chars=4, help="Enter any valid 4-character PDB code (e.g., 1AIL, 4INS, 7DHL)").upper()
    style_type = st.selectbox("Render Model Style", ["cartoon", "sphere", "stick", "line"])
    color_scheme = st.selectbox("Color Theme Strategy", ["spectrum", "chain", "ss"])
    st.write("---")
    tunneling_factor = st.slider("Quantum Tunneling Bias Coefficient", 0.1, 2.0, 0.85)

# ==============================================================================
# 3. GRAPHICAL GRID SYSTEM
# ==============================================================================
col_data, col_viewer = st.columns([1, 2], gap="large")

# --- LEFT COLUMN: SYSTEM DATA READOUTS ---
with col_data:
    st.markdown("<div class='premium-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-tag'>AI SPECTRAL ANALYTICS</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='panel-title'>Specimen Matrix: {pdb_code}</div>", unsafe_allow_html=True)
    
    # Grid calculation mapping based on the active slider input to make it feel responsive
    calculated_stability = round(0.98 - (tunneling_factor * 0.05), 3)
    calculated_viability = int(78 * tunneling_factor) if (78 * tunneling_factor) <= 100 else 100

    st.markdown(f"""
        <div class="stat-container">
            <div class="stat-num">{calculated_viability}%</div>
            <div class="stat-lbl">Tunneling Probability Rate</div>
        </div>
        <div class="stat-container">
            <div class="stat-num">{calculated_stability}</div>
            <div class="stat-lbl">Quantum Stability Metric (QSM)</div>
        </div>
        <div class="stat-container">
            <div class="stat-num">{(14 * tunneling_factor):.1f} fs</div>
            <div class="stat-lbl">Wavefunction Collapse Velocity</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Real-Time Data Graphing
    st.markdown("<div class='premium-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-tag'>HISTORICAL MONITORING</div>", unsafe_allow_html=True)
    
    chart_options = {
        "backgroundColor": "transparent",
        "xAxis": {"type": "category", "data": ["T-1", "T-2", "T-3", "T-4", "T-5"], "axisLine": {"show": False}},
        "yAxis": {"type": "value", "splitLine": {"lineStyle": {"color": "rgba(255,255,255,0.03)"}}},
        "series": [{
            "data": [0.4 * tunneling_factor, 0.6 * tunneling_factor, 0.5 * tunneling_factor, 0.8 * tunneling_factor, calculated_stability],
            "type": "line",
            "smooth": True,
            "itemStyle": {"color": "#00FFCC"},
            "lineStyle": {"width": 3}
        }],
        "grid": {"top": "15%", "bottom": "15%", "left": "12%", "right": "5%"}
    }
    st_echarts(options=chart_options, height="180px")
    st.markdown("</div>", unsafe_allow_html=True)


# --- RIGHT COLUMN: THE LIVE 3D INTERACTIVE ENGINE ---
with col_viewer:
    st.markdown("<div class='premium-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-tag'>3D INTERACTIVE MOLECULAR CANVAS</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='panel-title'>Active Hologram Stream // PDB Target: {pdb_code}</div>", unsafe_allow_html=True)
    
    # Instantiating the real 3D atomic renderer block
    try:
        viewer = py3Dmol.view(query=f'pdb:{pdb_code}')
        viewer.setStyle({style_type: {'color': color_scheme}})
        viewer.setBackgroundColor('#12131C') # Blends seamlessly directly with our panel background box
        viewer.zoomTo()
        
        # Pass the interactive instance straight to the UI layout
        make_with_py3dmol(viewer, width=700, height=450)
        
        st.markdown(f"<span style='color: #64748B; font-size:11px;'>⚙️ Use your mouse left-click to <b>Rotate</b>, right-click to <b>Pan</b>, and scroll wheel to <b>Zoom</b> into structural pockets.</span>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to pull atomic coordinate layout mapping for sequence code '{pdb_code}'. Verify target index link context.")
        
    st.markdown("</div>", unsafe_allow_html=True)
