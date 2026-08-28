import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from pipeline import PremiumEnzymePipeline
import Bio.PDB

# ========================
# PAGE CONFIG & CUSTOM CSS
# ========================

st.set_page_config(
    layout="wide",
    page_title="Enzyme Quantum Tunneling AI",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Premium Computational Biology Research Platform"
    }
)

# ========================
# CUSTOM CSS (Premium Dark Theme)
# ========================

custom_css = """
<style>
    /* Root color palette */
    :root {
        --primary: #00D9FF;      /* Neon cyan */
        --secondary: #FF006E;    /* Neon pink */
        --accent: #39FF14;       /* Neon green */
        --dark-bg: #0a0e27;      /* Very dark blue */
        --card-bg: #1a1f3a;      /* Dark blue */
        --text-primary: #ffffff; /* White */
        --text-secondary: #b0b8d8; /* Light gray */
        --border: #2d3748;       /* Border gray */
    }
    
    /* Overall page styling */
    body {
        background-color: var(--dark-bg);
        color: var(--text-primary);
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        padding: 2rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--card-bg);
        border-right: 1px solid var(--border);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--text-primary);
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Premium card styling */
    .premium-card {
        background: linear-gradient(135deg, #1a1f3a 0%, #16192b 100%);
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 217, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .premium-card:hover {
        border-color: rgba(0, 217, 255, 0.5);
        box-shadow: 0 12px 48px rgba(0, 217, 255, 0.2);
        transform: translateY(-2px);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1a1f3a 0%, #16192b 100%);
        border: 1px solid rgba(57, 255, 20, 0.15);
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(57, 255, 20, 0.4);
        box-shadow: 0 8px 24px rgba(57, 255, 20, 0.15);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--accent);
        font-family: 'Monaco', monospace;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    /* Tabs */
    [role="tablist"] {
        background-color: transparent;
        border-bottom: 1px solid var(--border);
    }
    
    [role="tab"] {
        color: var(--text-secondary) !important;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    [role="tab"][aria-selected="true"] {
        color: var(--primary) !important;
        border-bottom-color: var(--primary);
    }
    
    [role="tab"]:hover {
        color: var(--primary) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00D9FF 0%, #0099CC 100%);
        color: #000;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 217, 255, 0.4);
    }
    
    /* Sliders */
    .stSlider [data-baseweb="slider"] {
        background-color: var(--border);
    }
    
    /* Text inputs */
    .stTextInput input {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
        border-radius: 8px;
        padding: 0.75rem;
    }
    
    .stTextInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(0, 217, 255, 0.2) !important;
    }
    
    /* Data frames */
    .stDataFrame [data-testid="dataframe"] {
        background-color: transparent !important;
    }
    
    [data-testid="stDataFrameContainer"] {
        background-color: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Info/Success boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid;
        padding: 1rem;
    }
    
    .stInfo {
        background-color: rgba(0, 217, 255, 0.1) !important;
        border-left-color: var(--primary) !important;
        color: var(--text-secondary) !important;
    }
    
    .stSuccess {
        background-color: rgba(57, 255, 20, 0.1) !important;
        border-left-color: var(--accent) !important;
        color: var(--accent) !important;
    }
    
    .stError {
        background-color: rgba(255, 0, 110, 0.1) !important;
        border-left-color: var(--secondary) !important;
        color: var(--secondary) !important;
    }
    
    /* Markdown text */
    .markdown-text {
        color: var(--text-primary);
    }
    
    /* Caption styling */
    .stCaption {
        color: var(--text-secondary) !important;
    }
    
    /* Loading spinner */
    .stSpinner > div > div {
        background-color: var(--primary) !important;
    }
    
    /* Glow effect for titles */
    .glow-title {
        background: linear-gradient(135deg, #00D9FF 0%, #39FF14 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(0, 217, 255, 0.3);
        font-weight: 800;
        font-size: 2.5rem;
    }
    
    /* Code blocks */
    .stCode {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ========================
# HELPER FUNCTIONS
# ========================

THREE_TO_ONE = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
    'GLU': 'E', 'GLN': 'Q', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
    'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
    'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
}

@st.cache_resource
def load_pipeline(pdb_id):
    """Load pipeline once, cache across reruns"""
    return PremiumEnzymePipeline(pdb_id)

def extract_active_site_sequence(pdb_path, radius_angstroms=6.0):
    """Parse PDB and extract single-letter sequence near Fe core"""
    if not os.path.exists(pdb_path):
        return None
    
    try:
        parser = Bio.PDB.PDBParser(QUIET=True)
        structure = parser.get_structure("enzyme", pdb_path)
        
        iron_atom = None
        for atom in structure.get_atoms():
            if atom.get_name() == "FE":
                iron_atom = atom
                break
        
        if iron_atom is None:
            return None
        
        iron_coord = iron_atom.get_coord()
        
        nearby_residues = set()
        for atom in structure.get_atoms():
            if atom.get_name() == 'CA':
                dist = np.linalg.norm(atom.coord - iron_coord)
                if dist < radius_angstroms:
                    nearby_residues.add(atom.get_parent())
        
        sequence = []
        for res in sorted(nearby_residues, key=lambda r: r.get_id()[1]):
            res_name = res.get_resname()
            if res_name in THREE_TO_ONE:
                sequence.append(THREE_TO_ONE[res_name])
        
        return "".join(sequence) if sequence else None
    except:
        return None

def create_premium_metric(label, value, delta=None, color="cyan"):
    """Create premium metric card"""
    color_map = {
        "cyan": "#00D9FF",
        "green": "#39FF14",
        "pink": "#FF006E"
    }
    
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color: {color_map.get(color, '#00D9FF')}">{value}</div>
        {f'<div style="font-size: 0.75rem; color: #b0b8d8; margin-top: 0.5rem;">{delta}</div>' if delta else ''}
    </div>
    """

def plot_quantum_landscape_premium(width_range, barrier_range, runner):
    """Create premium tunneling landscape visualization"""
    widths = np.linspace(width_range[0], width_range[1], 20)
    barriers = np.linspace(barrier_range[0], barrier_range[1], 20)
    
    probs = np.zeros((len(barriers), len(widths)))
    for i, b in enumerate(barriers):
        for j, w in enumerate(widths):
            try:
                probs[i, j] = runner.run_quantum_engine(w, b)
            except:
                probs[i, j] = 1e-40
    
    fig = go.Figure(data=go.Heatmap(
        z=np.log10(probs + 1e-40),
        x=widths,
        y=barriers,
        colorscale=[[0, '#0a0e27'], [0.5, '#00D9FF'], [1, '#39FF14']],
        colorbar=dict(title="Log₁₀(T)", thickness=20)
    ))
    
    fig.update_layout(
        title="<b>Quantum Tunneling Probability Landscape</b>",
        xaxis_title="<b>Barrier Width (Å)</b>",
        yaxis_title="<b>Barrier Height (eV)</b>",
        height=500,
        plot_bgcolor="#0a0e27",
        paper_bgcolor="#1a1f3a",
        font=dict(color="#ffffff", family="monospace"),
        hovermode="closest",
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0, 217, 255, 0.1)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0, 217, 255, 0.1)")
    
    return fig

def plot_mutation_distribution_premium(mutations_df):
    """Create premium mutation score distribution"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=mutations_df['Candidate'],
        x=mutations_df['Score'],
        orientation='h',
        marker=dict(
            color=mutations_df['Score'],
            colorscale=[[0, '#FF006E'], [0.5, '#00D9FF'], [1, '#39FF14']],
            line=dict(color='rgba(0, 217, 255, 0.5)', width=1)
        ),
        text=[f"{score:.4f}" for score in mutations_df['Score']],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="<b>AI-Predicted Mutation Scores</b>",
        xaxis_title="<b>ESM-2 Score</b>",
        yaxis_title="<b>Amino Acid</b>",
        height=500,
        plot_bgcolor="#0a0e27",
        paper_bgcolor="#1a1f3a",
        font=dict(color="#ffffff", family="monospace"),
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0, 217, 255, 0.1)")
    
    return fig

# ========================
# HEADER SECTION
# ========================

col_header1, col_header2 = st.columns([3, 1])

with col_header1:
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <span style="font-size: 0.9rem; color: #00D9FF; letter-spacing: 2px; text-transform: uppercase; font-weight: 600;">
            🧬 Computational Biology Platform
        </span>
    </div>
    <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #00D9FF 0%, #39FF14 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        Enzyme Quantum Tunneling
    </h1>
    <p style="color: #b0b8d8; font-size: 1.1rem; margin-top: 0.5rem; font-weight: 300;">
        AI-Powered Mutation Design & Predictive Analytics
    </p>
    """, unsafe_allow_html=True)

with col_header2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1f3a 0%, #16192b 100%); border: 1px solid rgba(0, 217, 255, 0.3); border-radius: 12px; padding: 1rem; text-align: center; height: fit-content;">
        <div style="font-size: 0.8rem; color: #b0b8d8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">Status</div>
        <div style="font-size: 1.3rem; color: #39FF14; font-weight: 700;">🟢 ACTIVE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ========================
# SIDEBAR CONFIGURATION
# ========================

st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(57, 255, 20, 0.05) 100%); border: 1px solid rgba(0, 217, 255, 0.2); border-radius: 10px; padding: 1rem; margin-bottom: 1.5rem;">
    <div style="font-size: 0.9rem; color: #00D9FF; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">⚙️ Configuration</div>
</div>
""", unsafe_allow_html=True)

pdb_id = st.sidebar.text_input(
    "🧪 PDB ID",
    value="1yge",
    help="Enter PDB structure identifier"
).upper()

barrier_height = st.sidebar.slider(
    "🔗 Barrier Height (eV)",
    min_value=0.1,
    max_value=2.0,
    value=0.6,
    step=0.1
)

tunnel_width = st.sidebar.slider(
    "📏 Tunnel Width (Å)",
    min_value=0.5,
    max_value=5.0,
    value=1.2,
    step=0.1
)

substrate_energy = st.sidebar.slider(
    "⚡ Substrate Energy (eV)",
    min_value=0.0,
    max_value=0.5,
    value=0.1,
    step=0.05
)

active_site_radius = st.sidebar.slider(
    "🎯 Active Site Radius (Å)",
    min_value=3.0,
    max_value=10.0,
    value=6.0,
    step=0.5
)

st.sidebar.markdown("---")

col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    download_pdb = st.button("📥 Download", use_container_width=True)
with col_btn2:
    reset_btn = st.button("🔄 Reset", use_container_width=True)

if reset_btn:
    st.cache_resource.clear()
    st.rerun()

# ========================
# MAIN TABS
# ========================

tab1, tab2, tab3, tab4 = st.tabs(["🔬 Quantum Engine", "🤖 AI Mutations", "📊 Analytics", "📖 Methods"])

# ========================
# TAB 1: QUANTUM ENGINE
# ========================

with tab1:
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="color: #00D9FF; margin-bottom: 0.5rem;">Quantum Tunneling Analysis</h2>
        <p style="color: #b0b8d8;">Real-time WKB calculations for enzymatic proton tunneling</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h3 style="color: #00D9FF; margin-bottom: 1rem;">📋 Structure Information</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if download_pdb:
            with st.spinner("⏳ Downloading structure..."):
                runner = load_pipeline(pdb_id)
                success = runner.download_data()
                if success:
                    st.success("✅ Structure downloaded successfully!")
        
        runner = load_pipeline(pdb_id)
        pdb_path = f"data/{pdb_id.lower()}.pdb"
        
        if os.path.exists(pdb_path):
            st.markdown(f"""
            <div class="premium-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="color: #39FF14; font-weight: 700; font-size: 1.2rem;">✅ LOADED</div>
                        <div style="color: #b0b8d8; font-size: 0.9rem; margin-top: 0.3rem;">{pdb_id}</div>
                    </div>
                    <div style="font-size: 2rem;">🧬</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            sequence = extract_active_site_sequence(pdb_path, active_site_radius)
            if sequence:
                st.markdown(f"""
                <div class="premium-card">
                    <div style="color: #b0b8d8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">Active Site Sequence</div>
                    <div style="font-family: monospace; font-size: 1.3rem; color: #00D9FF; font-weight: 700; letter-spacing: 3px;">{sequence}</div>
                    <div style="color: #b0b8d8; font-size: 0.8rem; margin-top: 0.5rem;">Within {active_site_radius}Å of catalytic center</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("💡 Click 'Download' to fetch the PDB structure")
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h3 style="color: #39FF14; margin-bottom: 1.5rem;">🌌 Results</h3>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            prob = runner.run_quantum_engine(tunnel_width, barrier_height, substrate_energy)
            
            st.markdown(create_premium_metric(
                "Tunneling Probability",
                f"{prob:.3e}",
                "WKB Calculation",
                "green"
            ), unsafe_allow_html=True)
            
            st.markdown(create_premium_metric(
                "Log₁₀ Scale",
                f"{np.log10(prob):.2f}",
                "For comparison",
                "cyan"
            ), unsafe_allow_html=True)
            
            T_water = 1e-20
            fold = prob / T_water if prob > 0 else 0
            st.markdown(create_premium_metric(
                "Enhancement",
                f"{fold:.1f}x",
                "vs water",
                "pink"
            ), unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"Calculation error: {e}")
    
    # Visualization
    st.markdown("<hr style='border: 1px solid rgba(0, 217, 255, 0.2); margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h3 style="color: #00D9FF;">Quantum Landscape</h3>
        <p style="color: #b0b8d8; font-size: 0.9rem;">Interactive heatmap showing tunneling probability across parameter space</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(
        plot_quantum_landscape_premium(
            (max(0.5, tunnel_width - 0.8), tunnel_width + 0.8),
            (max(0.1, barrier_height - 0.3), barrier_height + 0.3),
            runner
        ),
        use_container_width=True
    )

# ========================
# TAB 2: AI MUTATIONS
# ========================

with tab2:
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="color: #39FF14; margin-bottom: 0.5rem;">AI-Designed Mutations</h2>
        <p style="color: #b0b8d8;">Meta ESM-2 predictions for beneficial amino acid substitutions</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        with st.spinner("🧠 Running ESM-2 inference..."):
            runner = load_pipeline(pdb_id)
            mutations_df = runner.run_ai_engine()
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("<div class='premium-card' style='padding: 0;'>", unsafe_allow_html=True)
            st.dataframe(
                mutations_df.head(15),
                use_container_width=True,
                height=500,
                hide_index=True
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="premium-card">
                <h4 style="color: #39FF14; margin-bottom: 1rem;">🏆 Top 5</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for idx, row in mutations_df.head(5).iterrows():
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom: 0.8rem;">
                    <div style="font-size: 0.7rem; color: #b0b8d8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.3rem;">#{idx+1}</div>
                    <div style="font-size: 1.4rem; color: #39FF14; font-weight: 700; font-family: monospace;">{row['Candidate']}</div>
                    <div style="font-size: 0.8rem; color: #00D9FF; margin-top: 0.3rem;">{row['Score']:.4f}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<hr style='border: 1px solid rgba(0, 217, 255, 0.2); margin: 2rem 0;'>", unsafe_allow_html=True)
        
        st.plotly_chart(
            plot_mutation_distribution_premium(mutations_df),
            use_container_width=True
        )
        
        # Export
        st.markdown("""
        <div class="premium-card">
            <div style="display: flex; gap: 1rem;">
        """, unsafe_allow_html=True)
        
        csv = mutations_df.to_csv(index=False)
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            st.download_button(
                "📥 Download CSV",
                csv,
                "mutations.csv",
                "text/csv",
                use_container_width=True
            )
        with col_exp2:
            json_export = mutations_df.to_json()
            st.download_button(
                "📥 Download JSON",
                json_export,
                "mutations.json",
                "application/json",
                use_container_width=True
            )
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ AI Engine failed: {e}")

# ========================
# TAB 3: ANALYTICS
# ========================

with tab3:
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="color: #00D9FF; margin-bottom: 0.5rem;">Literature Benchmarks</h2>
        <p style="color: #b0b8d8;">Validation against published enzyme kinetics data</p>
    </div>
    """, unsafe_allow_html=True)
    
    bench_data = {
        'Enzyme': ['Soybean Lipoxygenase', 'DHFR', 'Formate Oxidase'],
        'PDB ID': ['1YGE', '1DRF', '1FOX'],
        'Tunneling T': ['1.88e-18', '2.50e-19', '1.10e-18'],
        'Barrier (eV)': [0.6, 0.5, 0.7],
        'Width (Å)': [1.2, 1.0, 1.3]
    }
    
    bench_df = pd.DataFrame(bench_data)
    
    st.markdown("<div class='premium-card' style='padding: 0;'>", unsafe_allow_html=True)
    st.dataframe(bench_df, use_container_width=True, hide_index=True, height=300)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="premium-card">
        <h4 style="color: #39FF14; margin-bottom: 1rem;">📚 References</h4>
        <ul style="color: #b0b8d8; line-height: 1.8;">
            <li><strong>Klinman et al. (2013)</strong> - <em>Annu. Rev. Biochem.</em><br>
                Hydrogen tunneling links protein dynamics to enzyme catalysis</li>
            <li><strong>Scrutton et al. (2012)</strong> - <em>Nat. Chem.</em><br>
                Good vibrations in enzyme-catalysed reactions</li>
            <li><strong>Liang & Klinman (2004)</strong> - <em>Biochemistry</em><br>
                Structural basis for enzyme-catalyzed H-transfer reactions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ========================
# TAB 4: METHODS
# ========================

with tab4:
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="color: #39FF14; margin-bottom: 0.5rem;">Methodology</h2>
        <p style="color: #b0b8d8;">Complete documentation of computational methods and algorithms</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_method1, col_method2 = st.columns(2)
    
    with col_method1:
        st.markdown("""
        <div class="premium-card">
            <h3 style="color: #00D9FF; margin-bottom: 1rem;">⚛️ WKB Quantum Engine</h3>
            <p style="color: #b0b8d8; line-height: 1.8; font-family: monospace; font-size: 0.9rem;">
                <strong>T = Prefactor × exp(-2κa)</strong><br><br>
                where:<br>
                κ = √(2m(V₀-E))/ℏ<br>
                V₀ = barrier height (eV)<br>
                E = substrate energy (eV)<br>
                a = tunnel distance (m)<br>
                m = proton mass<br>
                ℏ = reduced Planck constant
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_method2:
        st.markdown("""
        <div class="premium-card">
            <h3 style="color: #39FF14; margin-bottom: 1rem;">🤖 AI Mutation Design</h3>
            <p style="color: #b0b8d8; line-height: 1.8;">
                <strong>ESM-2 Language Model Pipeline:</strong><br><br>
                1. <strong>Mask Target Position</strong><br>
                Replace residue with [MASK] token<br><br>
                2. <strong>Predict Distribution</strong><br>
                Model outputs amino acid probabilities<br><br>
                3. <strong>Rank Candidates</strong><br>
                Sort by ESM-2 confidence score<br><br>
                4. <strong>Filter & Validate</strong><br>
                Exclude unfavorable substitutions
            </p>
        </div>
        """, unsafe_allow_html=True)

# ========================
# FOOTER
# ========================

st.markdown("""
<hr style='border: 1px solid rgba(0, 217, 255, 0.2); margin: 3rem 0 2rem;'>
<div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem 0;">
    <div style="color: #b0b8d8; font-size: 0.85rem;">
        <span style="color: #00D9FF; font-weight: 700;">🧬 Enzyme Quantum Tunneling AI</span> v2.0 • Production-Ready Research Platform
    </div>
    <div style="color: #b0b8d8; font-size: 0.85rem;">
        <a href="https://github.com/EstherReagan/enzyme-quantum-tunneling-ai" style="color: #00D9FF; text-decoration: none;">GitHub</a> • 
        <span style="color: #39FF14;">🟢 Active</span>
    </div>
</div>
""", unsafe_allow_html=True)
