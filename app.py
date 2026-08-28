import streamlit as st
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# ==============================================================================
# 1. PREMIUM CINEMATIC UI STYLING & STRUCTURE (Blending Images 1 & 3)
# ==============================================================================
st.set_page_config(
    page_title="CRETAX // QUANTUM ENZYME AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom injection to force high-end sci-fi cards, spacing, and glows
st.markdown("""
    <style>
    /* Dark Matte Canvas Base */
    .stApp {
        background-color: #08090C;
        color: #E2E8F0;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    header, footer {visibility: hidden;}
    
    /* Styled Sidebar to match premium layout */
    section[data-testid="stSidebar"] {
        background-color: #0C0D14 !important;
        border-right: 1px solid rgba(0, 229, 255, 0.1);
    }
    
    /* Deep Glassmorphic Interactive Lab Containers */
    .sci-card {
        background: linear-gradient(135deg, rgba(18, 20, 28, 0.85) 0%, rgba(10, 11, 16, 0.95) 100%);
        border: 1px solid rgba(0, 229, 255, 0.12);
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6);
    }
    
    .panel-tag {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #00E5FF;
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    .panel-title {
        font-size: 22px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 20px;
        letter-spacing: -0.5px;
    }
    
    /* Premium Data Metrics Layout */
    .metrics-grid {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    .metric-row {
        padding: 12px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    .metric-val {
        font-size: 36px;
        font-weight: 800;
        color: #00FFCC;
        font-family: monospace;
        line-height: 1;
    }
    .metric-lbl {
        font-size: 11px;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# Top Premium Brand Navigation Header
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid rgba(0, 229, 255, 0.15); margin-bottom: 30px;">
        <div style="font-weight: 800; letter-spacing: 2px; color: #FFFFFF; font-size: 16px;">✕ CRETAX <span style='color:#718096; font-weight:300; font-size:13px;'> | ENZYME QUANTUM TUNNELING ENGINE</span></div>
        <div style='color: #00FFCC; font-size: 12px; font-family: monospace; background: rgba(0,255,204,0.08); padding: 4px 14px; border-radius: 20px; border: 1px solid rgba(0,255,204,0.2);'>CORE SYNC: ACTIVE</div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. RUNNABLE DATA INTERACTION CONTROLS
# ==============================================================================
with st.sidebar:
    st.markdown("<h3 style='color:#FFFFFF; margin-bottom:15px;'>🧬 Molecular Engine Config</h3>", unsafe_allow_html=True)
    
    # Real-world scientific properties inputs
    pdb_code = st.text_input("Target PDB Code Identifier", value="1AIL", max_chars=4, help="Examples: 1AIL (Enzyme Domain), 1UBQ (Protein Cluster), 4INS (Insulin)").upper()
    style_type = st.selectbox("3D Structural View Model", ["cartoon", "sphere", "stick", "line"])
    color_scheme = st.selectbox("Color Mapping Scheme", ["spectrum", "chain", "ss"])
    
    st.write("---")
    tunneling_factor = st.slider("Quantum Tunneling Bias Coefficient", 0.1, 2.0, 0.85)

# ==============================================================================
# 3. DYNAMIC DATA CALCULATOR LAYER
# ==============================================================================
# Calculations dynamically compute variables so it functions like a real platform
calculated_stability = round(0.98 - (tunneling_factor * 0.05), 3)
calculated_viability = int(78 * tunneling_factor) if (78 * tunneling_factor) <= 100 else 100

# ==============================================================================
# 4. TWO-COLUMN INTERACTIVE PREMIUM GRID
# ==============================================================================
col_left, col_right = st.columns([1, 1.4], gap="large")

# --- LEFT PANEL: COMPUTATIONAL ANALYSIS WINDOW ---
with col_left:
    # Top Data Readout Block
    st.markdown(f"""
    <div class="sci-card">
        <div class="panel-tag">QUANTUM SPECTRAL READOUTS</div>
        <div class="panel-title">Active Matrix Sequence: {pdb_code}</div>
        <div class="metrics-grid">
            <div class="metric-row">
                <div class="metric-val">{calculated_viability}%</div>
                <div class="metric-lbl">Tunneling Transition Probability</div>
            </div>
            <div class="metric-row">
                <div class="metric-val">{calculated_stability}</div>
                <div class="metric-lbl">Quantum Stability Metric (QSM)</div>
            </div>
            <div class="metric-row">
                <div class="metric-val">{(14 * tunneling_factor):.1f} fs</div>
                <div class="metric-lbl">Wavefunction Collapse Velocity</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bottom Historical Metric Graphing Block
    st.markdown("<div class='sci-card'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-tag'>TIMELINE MONITORING LOG</div>", unsafe_allow_html=True)
    
    chart_options = {
        "backgroundColor": "transparent",
        "xAxis": {"type": "category", "data": ["Step A", "Step B", "Step C", "Step D", "Current"], "axisLine": {"show": False}},
        "yAxis": {"type": "value", "splitLine": {"lineStyle": {"color": "rgba(255,255,255,0.03)"}}, "axisLine": {"show": False}},
        "series": [{
            "data": [0.4 * tunneling_factor, 0.6 * tunneling_factor, 0.5 * tunneling_factor, 0.8 * tunneling_factor, calculated_stability],
            "type": "line",
            "smooth": True,
            "itemStyle": {"color": "#00FFCC"},
            "lineStyle": {"width": 3, "shadowBlur": 10, "shadowColor": "#00FFCC"},
            "areaStyle": {"color": "rgba(0, 255, 204, 0.03)"}
        }],
        "grid": {"top": "10%", "bottom": "15%", "left": "10%", "right": "5%"}
    }
    st_echarts(options=chart_options, height="175px")
    st.markdown("</div>", unsafe_allow_html=True)


# --- RIGHT PANEL: SECURE INTERACTIVE 3D ENZYME ENGINE ---
with col_right:
    st.markdown(f"""
    <div class="sci-card" style="border-color: rgba(0, 255, 204, 0.25);">
        <div class="panel-tag">HOLOGRAPHIC ENZYME RENDERING ENGINE</div>
        <div class="panel-title">Active Secure Stream // Target: {pdb_code}</div>
    """, unsafe_allow_html=True)
    
    # Secure web rendering canvas with cross-browser fallback scripts
    secure_html_canvas = f"""
    <div id="canvas-3dmol" style="width: 100%; height: 440px; background-color: #0E0F16; border-radius: 8px; border: 1px solid rgba(255,255,255,0.03);"></div>
    
    <!-- Load stable secure dependencies directly via CDN -->
    <script src="https://jsdelivr.net"></script>
    <script src="https://jsdelivr.net"></script>
    
    <script>
        $(function() {{
            let container = $('#canvas-3dmol');
            let viewer = $3Dmol.createViewer(container, {{ backgroundColor: '#0E0F16' }});
            
            // Pull files using secure structural URLs over HTTPS to bypass mixed-content blocks
            let secureUrl = 'https://rcsb.org{pdb_code}.pdb';
            
            $.get(secureUrl, function(data) {{
                viewer.addModel(data, "pdb");
                viewer.setStyle({{}}, {{{style_type}: {{color: '{color_scheme}'}}}});
                viewer.zoomTo();
                viewer.render();
            }}).fail(function() {{
                container.html("<div style='color:#FF4B4B; font-family:monospace; padding:40px; text-align:center;'>❌ FAILED TO PARSE COORDINATE VECTOR FOR '{pdb_code}'</div>");
            }});
        }});
    </script>
    """
    
    # Display the secure 3D canvas object
    components.html(secure_html_canvas, height=450)
    
    st.markdown("""
        <div style='color: #718096; font-size:11px; margin-top:12px; display:flex; justify-content:space-between;'>
            <span>⚙️ <b>Interactive Track:</b> Drag to Rotate // Right-Click to Pan // Scroll to Zoom</span>
            <span style='color: #00FFCC;'>MODEL: LIVE STRUCTURE DATA</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
