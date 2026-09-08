import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objects as go
import requests
import numpy as np
import os

# ===== CONFIG =====

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# ===== CREATE APP =====

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

app.title = "Enzyme Quantum Tunneling AI"

# ===== DARK THEME CSS =====

THEME = {
    "dark_bg": "#0a0e27",
    "card_bg": "#1a1f3a",
    "primary": "#00D9FF",
    "accent": "#39FF14",
    "secondary": "#FF006E",
    "text": "#ffffff",
    "text_dim": "#b0b8d8"
}

styles = f"""
<style>
body {{
    background: linear-gradient(135deg, {THEME['dark_bg']} 0%, {THEME['card_bg']} 100%);
    color: {THEME['text']};
    font-family: 'Inter', 'Segoe UI', sans-serif;
    margin: 0;
    padding: 0;
}}

.container {{
    max-width: 1600px;
    margin: 0 auto;
    padding: 2rem;
}}

.premium-card {{
    background: linear-gradient(135deg, {THEME['card_bg']} 0%, #16192b 100%);
    border: 1px solid rgba(0, 217, 255, 0.2);
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 8px 32px rgba(0, 217, 255, 0.08);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.premium-card:hover {{
    border-color: rgba(0, 217, 255, 0.4);
    box-shadow: 0 12px 48px rgba(0, 217, 255, 0.15);
    transform: translateY(-4px);
}}

.metric-card {{
    background: linear-gradient(135deg, {THEME['card_bg']} 0%, #16192b 100%);
    border: 1px solid rgba(57, 255, 20, 0.15);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    margin: 0.75rem;
}}

.metric-value {{
    font-size: 2rem;
    font-weight: 800;
    color: {THEME['accent']};
    font-family: 'Monaco', monospace;
    margin: 0.8rem 0;
}}

.metric-label {{
    font-size: 0.8rem;
    color: {THEME['text_dim']};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}}

.glow-title {{
    background: linear-gradient(135deg, {THEME['primary']} 0%, {THEME['accent']} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}}

.slider-container {{
    background: linear-gradient(135deg, {THEME['card_bg']} 0%, #16192b 100%);
    border: 1px solid rgba(0, 217, 255, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}}

.slider-label {{
    color: {THEME['primary']};
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

button {{
    background: linear-gradient(135deg, {THEME['primary']} 0%, #0099CC 100%);
    color: #000;
    border: none;
    border-radius: 8px;
    padding: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 217, 255, 0.4);
}}

.info-box {{
    background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(57, 255, 20, 0.05) 100%);
    border-left: 4px solid {THEME['primary']};
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
    color: {THEME['text_dim']};
}}

.footer {{
    text-align: center;
    color: {THEME['text_dim']};
    padding: 2rem;
    border-top: 1px solid rgba(0, 217, 255, 0.1);
    margin-top: 3rem;
    font-size: 0.9rem;
}}
</style>
"""

# ===== LAYOUT =====

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="selected-enzyme", data={"pdb_id": "1YGE", "name": "Soybean Lipoxygenase"}),
    
    html.Div([
        # HEADER
        html.Div([
            html.Span("🧬 COMPUTATIONAL BIOLOGY", style={"color": THEME["primary"], "fontSize": "0.9rem", "fontWeight": "700", "letterSpacing": "2px", "textTransform": "uppercase"}),
            html.H1("Enzyme Quantum Tunneling", className="glow-title", style={"margin": "0"}),
            html.P("AI-Powered Mutation Design & Quantum Analysis", style={"color": THEME["text_dim"], "fontSize": "1.2rem", "marginBottom": "2rem"}),
        ], className="container", style={"paddingTop": "3rem"}),
        
        # FEATURED ENZYMES
        html.Div([
            html.H3("Featured Enzymes", style={"color": THEME["primary"], "marginBottom": "1.5rem"}),
            html.Div(id="enzyme-buttons", style={"display": "flex", "gap": "1rem", "flexWrap": "wrap", "marginBottom": "2rem"}),
        ], className="container"),
        
        # MAIN INTERFACE
        html.Div([
            html.Div([
                # LEFT: CONTROLS
                html.Div([
                    html.Div([
                        html.H3("Parameters", style={"color": THEME["primary"], "marginBottom": "1.5rem"}),
                        
                        html.Div([
                            html.Label("Barrier Height (eV)", className="slider-label"),
                            dcc.Slider(id="barrier-slider", min=0.1, max=2.0, step=0.1, value=0.6,
                                      marks={0.1: "0.1", 0.5: "0.5", 1.0: "1.0", 1.5: "1.5", 2.0: "2.0"},
                                      tooltip={"placement": "bottom", "always_visible": True}),
                        ], className="slider-container"),
                        
                        html.Div([
                            html.Label("Tunnel Width (Å)", className="slider-label"),
                            dcc.Slider(id="width-slider", min=0.5, max=5.0, step=0.1, value=1.2,
                                      marks={0.5: "0.5", 1.5: "1.5", 2.5: "2.5", 3.5: "3.5", 5.0: "5.0"},
                                      tooltip={"placement": "bottom", "always_visible": True}),
                        ], className="slider-container"),
                        
                        html.Div([
                            html.Label("Substrate Energy (eV)", className="slider-label"),
                            dcc.Slider(id="energy-slider", min=0.0, max=0.5, step=0.05, value=0.1,
                                      marks={0: "0", 0.25: "0.25", 0.5: "0.5"},
                                      tooltip={"placement": "bottom", "always_visible": True}),
                        ], className="slider-container"),
                        
                        html.Button("📊 CALCULATE", id="calculate-btn", n_clicks=0, style={"width": "100%", "marginTop": "1.5rem"}),
                        
                    ], className="premium-card"),
                    
                    html.Div(id="results-metrics"),
                    
                ], style={"flex": "1", "minWidth": "300px"}),
                
                # RIGHT: VISUALIZATIONS
                html.Div([
                    dcc.Tabs(id="viz-tabs", value="tab-quantum", children=[
                        dcc.Tab(label="🌌 Quantum Landscape", value="tab-quantum", children=[
                            dcc.Graph(id="quantum-plot", style={"height": "500px"})
                        ]),
                        
                        dcc.Tab(label="🤖 AI Mutations", value="tab-mutations", children=[
                            dcc.Graph(id="mutations-plot", style={"height": "500px"})
                        ]),
                        
                        dcc.Tab(label="📊 Analytics", value="tab-analytics", children=[
                            dcc.Graph(id="analytics-plot", style={"height": "500px"})
                        ]),
                    ]),
                    
                ], style={"flex": "1", "minWidth": "400px"}),
                
            ], style={"display": "flex", "gap": "2rem", "flexWrap": "wrap"}),
            
        ], className="container"),
        
        # FOOTER
        html.Div([
            html.P(f"🧬 Enzyme Quantum Tunneling AI v3.0 | GitHub | 🟢 ACTIVE", style={"color": THEME["text_dim"]}),
        ], className="footer"),
        
    ], style={"background": f"linear-gradient(135deg, {THEME['dark_bg']} 0%, {THEME['card_bg']} 100%)", "minHeight": "100vh"}),
    
], style={"margin": "0", "padding": "0"})

# Inject CSS
app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        {styles}
    </head>
    <body>
        {{%app_entry%}}
        <footer>{{%config%}}{{%scripts%}}{{%renderer%}}</footer>
    </body>
</html>
'''

# ===== CALLBACKS =====

@callback(
    Output("enzyme-buttons", "children"),
    Input("url", "pathname")
)
def update_enzyme_buttons(_):
    """Load featured enzymes"""
    try:
        response = requests.get(f"{BACKEND_URL}/featured-enzymes", timeout=5)
        enzymes = response.json()["enzymes"]
        
        buttons = [
            html.Button(
                f"🧪 {enzyme['name']}",
                id={"type": "enzyme-btn", "index": enzyme["pdb_id"]},
                n_clicks=0,
                style={"background": f"linear-gradient(135deg, {THEME['primary']} 0%, #0099CC 100%)", "color": "#000"} if enzyme["pdb_id"] == "1YGE" else {"border": f"2px solid {THEME['primary']}", "background": THEME['card_bg'], "color": THEME['primary']},
            )
            for enzyme in enzymes
        ]
        
        return buttons
    except:
        return html.Div("Loading enzymes...", style={"color": THEME["text_dim"]})

@callback(
    Output("selected-enzyme", "data"),
    Input({"type": "enzyme-btn", "index": dash.ALL}, "n_clicks"),
    State({"type": "enzyme-btn", "index": dash.ALL}, "id"),
    prevent_initial_call=True
)
def select_enzyme(n_clicks, ids):
    """Select enzyme"""
    if not ids or not any(n_clicks):
        return dash.no_update
    
    clicked_id = ids[np.argmax(n_clicks)]["index"]
    
    enzyme_map = {
        "1YGE": "Soybean Lipoxygenase",
        "1DRF": "Dihydrofolate Reductase",
        "1OXO": "Cytochrome P450 3A4",
        "1FOX": "Formate Oxidase",
    }
    
    return {"pdb_id": clicked_id, "name": enzyme_map.get(clicked_id, "Unknown")}

@callback(
    [Output("quantum-plot", "figure"),
     Output("mutations-plot", "figure"),
     Output("results-metrics", "children")],
    Input("calculate-btn", "n_clicks"),
    [State("barrier-slider", "value"),
     State("width-slider", "value"),
     State("energy-slider", "value"),
     State("selected-enzyme", "data")],
    prevent_initial_call=True
)
def calculate_results(n_clicks, barrier, width, energy, enzyme):
    """Calculate results"""
    
    try:
        # Quantum calculation
        params = {"width_angstroms": width, "barrier_ev": barrier, "substrate_energy_ev": energy}
        response = requests.post(f"{BACKEND_URL}/quantum", json=params, timeout=5)
        result = response.json()
        
        # Quantum landscape
        widths = np.linspace(max(0.5, width-1), width+1, 20)
        barriers = np.linspace(max(0.1, barrier-0.5), barrier+0.5, 20)
        
        Z = np.zeros((len(barriers), len(widths)))
        for i, b in enumerate(barriers):
            for j, w in enumerate(widths):
                try:
                    resp = requests.post(f"{BACKEND_URL}/quantum", json={"width_angstroms": w, "barrier_ev": b, "substrate_energy_ev": energy}, timeout=2)
                    Z[i, j] = resp.json()["log_scale"]
                except:
                    Z[i, j] = -40
        
        quantum_fig = go.Figure(data=go.Heatmap(
            z=Z, x=widths, y=barriers,
            colorscale=[[0, '#0a0e27'], [0.5, '#00D9FF'], [1, '#39FF14']],
            colorbar=dict(title="Log₁₀(T)")
        ))
        
        quantum_fig.update_layout(
            title="<b>Quantum Tunneling Probability</b>",
            xaxis_title="<b>Width (Å)</b>",
            yaxis_title="<b>Barrier (eV)</b>",
            plot_bgcolor="#0a0e27",
            paper_bgcolor="#1a1f3a",
            font=dict(color="#ffffff"),
            height=500
        )
        
        # Mutations (mock)
        amino_acids = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
        scores = np.random.dirichlet(np.ones(20)) * 10
        
        mutations_fig = go.Figure(data=go.Bar(
            y=amino_acids, x=scores, orientation='h',
            marker=dict(color=scores, colorscale=[[0, '#FF006E'], [0.5, '#00D9FF'], [1, '#39FF14']])
        ))
        
        mutations_fig.update_layout(
            title="<b>AI Mutation Scores</b>",
            xaxis_title="<b>Score</b>",
            plot_bgcolor="#0a0e27",
            paper_bgcolor="#1a1f3a",
            font=dict(color="#ffffff"),
            height=500, showlegend=False
        )
        
        # Metrics
        metrics = html.Div([
            html.Div([
                html.Div([html.Div("TUNNELING", className="metric-label"), html.Div(f"{result['tunneling_probability']:.3e}", className="metric-value")], className="metric-card"),
                html.Div([html.Div("LOG SCALE", className="metric-label"), html.Div(f"{result['log_scale']:.2f}", className="metric-value")], className="metric-card"),
                html.Div([html.Div("ENHANCEMENT", className="metric-label"), html.Div(f"{result['enhancement_fold']:.1f}x", className="metric-value")], className="metric-card"),
                html.Div([html.Div("ENZYME", className="metric-label"), html.Div(enzyme["name"][:20].upper(), className="metric-value", style={"fontSize": "1.2rem"})], className="metric-card"),
            ], style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(150px, 1fr))", "gap": "1rem", "marginTop": "2rem"}),
            
            html.Div("✅ Calculation complete!", className="info-box"),
        ])
        
        return quantum_fig, mutations_fig, metrics
    
    except Exception as e:
        error = html.Div(f"❌ Error: {str(e)}", className="info-box", style={"borderLeftColor": "#FF006E", "color": "#FF006E"})
        return {}, {}, error

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
