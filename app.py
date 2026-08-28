import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# ==============================================================================
# 1. LUXURY GLASSMORPHIC CORE THEME (Refined spacing inspired by Image 3)
# ==============================================================================
st.set_page_config(
    page_title="CRETAX // QUANTUM ENZYME AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom absolute tracking overrides to guarantee structured box alignments
st.markdown("""
    <style>
    .stApp {
        background-color: #08090C;
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    header, footer {visibility: hidden;}
    
    /* Control Panel Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0C0D14 !important;
        border-right: 1px solid rgba(0, 229, 255, 0.1);
    }
    
    /* Premium Box Panel Containers */
    .sci-card {
        background: linear-gradient(135deg, rgba(18, 20, 28, 0.9) 0%, rgba(10, 11, 16, 0.98) 100%);
        border: 1px solid rgba(0, 229, 255, 0.12);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 22px;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.6);
    }
    
    .panel-tag {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        color: #00E5FF;
        font-weight: 600;
        margin-bottom: 6px;
    }
    
    .panel-title {
        font-size: 20px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 24px;
    }
    
    /* Interactive Numeric Grid */
    .metrics-container {
        display: flex;
        flex-direction: column;
        gap: 18px;
    }
    .metric-block {
        padding-bottom: 14px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }
    .metric-value-text {
        font-size: 34px;
        font-weight: 800;
        color: #00FFCC;
        font-family: monospace;
        line-height: 1;
    }
    .metric-label-text {
        font-size: 11px;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# Top Premium Navigation Brand Header Bar
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid rgba(0, 229, 255, 0.15); margin-bottom: 35px;">
        <div style="font-weight: 800; letter-spacing: 2px; color: #FFFFFF; font-size: 16px;">✕ CRETAX <span style='color:#64748B; font-weight:300; font-size:13px;'> | ENZYME QUANTUM TUNNELING AI</span></div>
        <div style='color: #00FFCC; font-size: 11px; font-family: monospace; background: rgba(0,255,204,0.06); padding: 4px 14px; border-radius: 20px; border: 1px solid rgba(0,255,204,0.15);'>CORE INTEGRATION STATUS: OPERATIONAL</div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. RUNNABLE SIDEBAR CALCULATION PARAMETERS
# ==============================================================================
with st.sidebar:
    st.markdown("<h3 style='color:#FFFFFF; margin-bottom:15px;'>🔬 Computation Settings</h3>", unsafe_allow_html=True)
    
    # Inputs feeding into your backend array properties
    pdb_id = st.text_input("Target Protein Data Bank (PDB) Code", value="1AIL", max_chars=4).upper()
    render_style = st.selectbox("3D Visualization View Model", ["cartoon", "sphere", "stick", "line"])
    color_map = st.selectbox("Color Mapping Matrix", ["spectrum", "chain", "ss"])
    
    st.write("---")
    quantum_slider = st.slider("Sub-atomic Displacement Index Factor", 0.1, 2.0, 0.85)

# Reactive simulation calculation loops running live off the sidebar states
calc_stability = round(0.995 - (quantum_slider * 0.04), 3)
calc_viability = int(82 * quantum_slider) if (82 * quantum_slider) <= 100 else 100

# ==============================================================================
# 3. SPLIT COLUMN SCI-FI VIEWPORT INTERFACE
# ==============================================================================
col_analytics, col_render_canvas = st.columns([1, 1.4], gap="large")

# --- LEFT BLOCK: ANALYTICS AND SIGNAL WAVE PACKETS ---
with col_analytics:
    st.markdown(f"""
    <div class="sci-card">
        <div class="panel-tag">QUANTUM MATRIX READOUTS</div>
        <div class="panel-title">Active Target Domain: {pdb_id}</div>
        <div class="metrics-container">
            <div class="metric-block">
                <div class="metric-value-text">{calc_viability}%</div>
                <div class="metric-label-text">Tunneling Probability Distribution</div>
            </div>
            <div class="metric-block">
                <div class="metric-value-text">{calc_stability}</div>
                <div class="metric-label-text">Quantum Stability Metric (QSM)</div>
            </div>
            <div class="metric-block">
                <div class="metric-value-text">{(12.4 * quantum_slider):.1f} fs</div>
                <div class="metric-label-text">Wavefunction De-coherence Velocity</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Neon line graph timeline logger
    st.markdown("<div class='sci-card'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-tag'>STABILITY HISTORICAL TIMELINE STREAM</div>", unsafe_allow_html=True)
    
    timeline_chart = {
        "backgroundColor": "transparent",
        "xAxis": {"type": "category", "data": ["Node A", "Node B", "Node C", "Node D", "Live"], "axisLine": {"show": False}},
        "yAxis": {"type": "value", "splitLine": {"lineStyle": {"color": "rgba(255,255,255,0.03)"}}, "axisLine": {"show": False}},
        "series": [{
            "data": [0.35 * quantum_slider, 0.58 * quantum_slider, 0.49 * quantum_slider, 0.72 * quantum_slider, calc_stability],
            "type": "line",
            "smooth": True,
            "itemStyle": {"color": "#00FFCC"},
            "lineStyle": {"width": 3, "shadowBlur": 12, "shadowColor": "#00FFCC"},
            "areaStyle": {"color": "rgba(0, 255, 204, 0.02)"}
        }],
        "grid": {"top": "10%", "bottom": "15%", "left": "10%", "right": "5%"}
    }
    st_echarts(options=timeline_chart, height="175px")
    st.markdown("</div>", unsafe_allow_html=True)


# --- RIGHT BLOCK: LIVE 3D ATOMIC RENDERING CANVAS ---
with col_render_canvas:
    st.markdown(f"""
    <div class="sci-card" style="border-color: rgba(0, 229, 255, 0.25);">
        <div class="panel-tag">HOLOGRAPHIC GEOMETRY MODEL CANVAS</div>
        <div class="panel-title">Active Biological Vector Stream // ID: {pdb_id}</div>
    """, unsafe_allow_html=True)
    
    # Encrypted secure browser iframe component bypassing missing package bindings
    secure_viewport_js = f"""
    <div id="mol-canvas-container" style="width: 100%; height: 435px; background-color: #0E0F16; border-radius: 8px;"></div>
    
    <script src="https://jsdelivr.net"></script>
    <script src="https://jsdelivr.net"></script>
    
    <script>
        $(function() {{
            let surface_element = $('#mol-canvas-container');
            let renderer = $3Dmol.createViewer(surface_element, {{ backgroundColor: '#0E0F16' }});
            let target_url = 'https://rcsb.org{pdb_id}.pdb';
            
            $.get(target_url, function(data) {{
                renderer.addModel(data, "pdb");
                renderer.setStyle({{}}, {{{render_style}: {{color: '{color_map}'}}}});
                renderer.zoomTo();
                renderer.render();
            }}).fail(function() {{
                surface_element.html("<div style='color:#FF4B4B; font-family:monospace; padding:50px; text-align:center;'>❌ FAILED TO FETCH CRYSTALLOGRAPHIC DATA FOR VECTOR: {pdb_id}</div>");
            }});
        }});
    </script>
    """
    
    components.html(secure_viewport_js, height=445)
    
    st.markdown("""
        <div style='color: #64748B; font-size:11px; margin-top:14px; display:flex; justify-content:space-between; width:100%;'>
            <span>⚙️ <b>Navigation Tracking:</b> Left-Click to Rotate // Right-Click to Pan // Scroll Wheel to Zoom</span>
            <span style='color: #00FFCC;'>STREAM STATUS: SECURE L3</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
