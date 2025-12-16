"""
=============================================================================
GenAI in Higher Education - Professional Dashboard
=============================================================================
Clean, intuitive, and visually appealing dashboard with working theme toggle.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="GenAI Education Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# THEME SYSTEM
# =============================================================================

def init_session_state():
    """Initialize session state variables."""
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

init_session_state()

# Theme color palettes
THEMES = {
    "dark": {
        "bg_primary": "#0a0a0a",
        "bg_secondary": "#141414",
        "bg_card": "#1a1a1a",
        "text_primary": "#ffffff",
        "text_secondary": "#a0a0a0",
        "border": "#2a2a2a",
        "accent": "#6366f1",
        "accent_light": "#818cf8",
        "success": "#22c55e",
        "warning": "#eab308",
        "danger": "#ef4444",
        "chart_bg": "rgba(0,0,0,0)",
        "grid": "#2a2a2a"
    },
    "light": {
        "bg_primary": "#ffffff",
        "bg_secondary": "#f8f9fa",
        "bg_card": "#ffffff",
        "text_primary": "#1a1a1a",
        "text_secondary": "#6b7280",
        "border": "#e5e7eb",
        "accent": "#4f46e5",
        "accent_light": "#6366f1",
        "success": "#16a34a",
        "warning": "#ca8a04",
        "danger": "#dc2626",
        "chart_bg": "rgba(0,0,0,0)",
        "grid": "#e5e7eb"
    }
}

def get_theme():
    """Get current theme colors."""
    return THEMES[st.session_state.theme]

# Chart color palettes (consistent across themes)
REGION_COLORS = {
    "North America": "#6366f1",
    "Europe": "#8b5cf6", 
    "Asia Pacific": "#ec4899",
    "Latin America": "#22c55e",
    "Middle East": "#f59e0b",
    "Africa": "#06b6d4"
}

POLICY_COLORS = {
    "Restrictive": "#ef4444",
    "Cautious": "#f59e0b",
    "Permissive": "#3b82f6",
    "Integrated": "#22c55e"
}

INSTITUTION_COLORS = {
    "Research University": "#6366f1",
    "Teaching University": "#8b5cf6",
    "Liberal Arts College": "#ec4899",
    "Technical Institute": "#22c55e",
    "Community College": "#f59e0b"
}

# =============================================================================
# CSS STYLING
# =============================================================================

def apply_theme_css():
    """Apply comprehensive CSS styling based on current theme."""
    t = get_theme()
    
    css = f"""
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Global Styles */
        .stApp {{
            background-color: {t["bg_primary"]};
            font-family: 'Inter', sans-serif;
        }}
        
        /* Main Container */
        .main .block-container {{
            padding: 2rem 3rem;
            max-width: 1400px;
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {t["bg_secondary"]};
            border-right: 1px solid {t["border"]};
        }}
        
        [data-testid="stSidebar"] * {{
            color: {t["text_primary"]} !important;
        }}
        
        /* Headers */
        .main-title {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {t["text_primary"]};
            margin-bottom: 0.25rem;
            letter-spacing: -0.02em;
        }}
        
        .main-subtitle {{
            font-size: 1.1rem;
            color: {t["text_secondary"]};
            margin-bottom: 2rem;
            font-weight: 400;
        }}
        
        .section-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: {t["text_primary"]};
            margin: 2rem 0 1.25rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        /* KPI Cards */
        .kpi-container {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        
        .kpi-card {{
            background: {t["bg_card"]};
            border: 1px solid {t["border"]};
            border-radius: 12px;
            padding: 1.25rem;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .kpi-value {{
            font-size: 2rem;
            font-weight: 700;
            color: {t["accent"]};
            line-height: 1.2;
        }}
        
        .kpi-label {{
            font-size: 0.85rem;
            color: {t["text_secondary"]};
            margin-top: 0.5rem;
            font-weight: 500;
        }}
        
        .kpi-delta {{
            font-size: 0.75rem;
            margin-top: 0.25rem;
            font-weight: 500;
        }}
        
        .kpi-delta.positive {{
            color: {t["success"]};
        }}
        
        .kpi-delta.negative {{
            color: {t["danger"]};
        }}
        
        /* Chart Container */
        .chart-container {{
            background: {t["bg_card"]};
            border: 1px solid {t["border"]};
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }}
        
        .chart-title {{
            font-size: 1rem;
            font-weight: 600;
            color: {t["text_primary"]};
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid {t["border"]};
        }}
        
        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: {t["bg_secondary"]};
            border-radius: 10px;
            padding: 0.25rem;
            gap: 0.25rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: transparent;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            color: {t["text_secondary"]};
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {t["accent"]} !important;
            color: white !important;
        }}
        
        /* Metrics Override */
        [data-testid="stMetricValue"] {{
            color: {t["accent"]} !important;
            font-size: 1.75rem !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {t["text_secondary"]} !important;
        }}
        
        /* Selectbox Styling */
        .stSelectbox label, .stMultiSelect label {{
            color: {t["text_primary"]} !important;
            font-weight: 500;
        }}
        
        /* Button Styling */
        .stButton > button {{
            background-color: {t["accent"]};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            font-weight: 500;
            transition: all 0.2s;
        }}
        
        .stButton > button:hover {{
            background-color: {t["accent_light"]};
            transform: translateY(-1px);
        }}
        
        /* Theme Toggle Button */
        .theme-btn {{
            background: {t["bg_card"]};
            border: 1px solid {t["border"]};
            border-radius: 8px;
            padding: 0.5rem 1rem;
            cursor: pointer;
            color: {t["text_primary"]};
            font-weight: 500;
            transition: all 0.2s;
        }}
        
        .theme-btn:hover {{
            background: {t["accent"]};
            color: white;
        }}
        
        /* Data Table */
        .stDataFrame {{
            border: 1px solid {t["border"]};
            border-radius: 8px;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background: {t["bg_card"]};
            border-radius: 8px;
            color: {t["text_primary"]} !important;
        }}
        
        /* Download Button */
        .stDownloadButton > button {{
            background-color: {t["success"]};
            color: white;
        }}
        
        .stDownloadButton > button:hover {{
            background-color: #16a34a;
        }}
        
        /* Info Box */
        .info-box {{
            background: {t["bg_card"]};
            border: 1px solid {t["border"]};
            border-left: 4px solid {t["accent"]};
            border-radius: 8px;
            padding: 1rem 1.25rem;
            margin: 1rem 0;
            color: {t["text_primary"]};
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 2rem;
            color: {t["text_secondary"]};
            font-size: 0.85rem;
            margin-top: 3rem;
            border-top: 1px solid {t["border"]};
        }}
        
        /* Hide Streamlit Elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {t["bg_secondary"]};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {t["border"]};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {t["text_secondary"]};
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# =============================================================================
# DATA LOADING
# =============================================================================

@st.cache_data
def load_data():
    """Load and cache the dataset."""
    try:
        df = pd.read_csv("data/dataset.csv")
        return df
    except FileNotFoundError:
        return None

# =============================================================================
# KPI COMPONENT
# =============================================================================

def render_kpi_card(value, label, delta=None, delta_type="positive"):
    """Render a single KPI card."""
    t = get_theme()
    
    delta_html = ""
    if delta:
        delta_class = "positive" if delta_type == "positive" else "negative"
        delta_icon = "↑" if delta_type == "positive" else "↓"
        delta_html = f'<div class="kpi-delta {delta_class}">{delta_icon} {delta}</div>'
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>
    """

# =============================================================================
# CHART 1: LINE CHART - Adoption Trends Over Time
# =============================================================================

def create_line_chart(df):
    """Create clean line chart showing adoption trends."""
    t = get_theme()
    
    # Aggregate by quarter and region
    trend = df.groupby(["survey_quarter", "region"])["ai_adoption_rate"].mean().reset_index()
    trend = trend.sort_values("survey_quarter")
    
    fig = go.Figure()
    
    for region in trend["region"].unique():
        region_data = trend[trend["region"] == region]
        fig.add_trace(go.Scatter(
            x=region_data["survey_quarter"],
            y=region_data["ai_adoption_rate"],
            mode='lines+markers',
            name=region,
            line=dict(width=3, color=REGION_COLORS.get(region, "#6366f1")),
            marker=dict(size=8),
            hovertemplate=f"<b>{region}</b><br>" +
                          "Quarter: %{x}<br>" +
                          "Adoption: %{y:.1f}%<extra></extra>"
        ))
    
    fig.update_layout(
        title=dict(
            text="📈 AI Adoption Rate Trends by Region",
            font=dict(size=16, color=t["text_primary"])
        ),
        xaxis=dict(
            title="Quarter",
            gridcolor=t["grid"],
            linecolor=t["border"],
            tickfont=dict(color=t["text_secondary"]),
            titlefont=dict(color=t["text_secondary"])
        ),
        yaxis=dict(
            title="Adoption Rate (%)",
            gridcolor=t["grid"],
            linecolor=t["border"],
            tickfont=dict(color=t["text_secondary"]),
            titlefont=dict(color=t["text_secondary"])
        ),
        paper_bgcolor=t["chart_bg"],
        plot_bgcolor=t["chart_bg"],
        font=dict(color=t["text_primary"]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(color=t["text_primary"])
        ),
        height=420,
        margin=dict(l=60, r=30, t=60, b=80),
        hovermode="x unified"
    )
    
    return fig

# =============================================================================
# CHART 2: HORIZONTAL BAR - Regional Comparison
# =============================================================================

def create_horizontal_bar(df, metric="ai_adoption_rate"):
    """Create horizontal bar chart for regional comparison."""
    t = get_theme()
    
    # Aggregate by region
    regional = df.groupby("region")[metric].mean().sort_values(ascending=True).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=regional["region"],
        x=regional[metric],
        orientation='h',
        marker=dict(
            color=[REGION_COLORS.get(r, t["accent"]) for r in regional["region"]],
            line=dict(width=0)
        ),
        text=[f"{v:.1f}%" for v in regional[metric]],
        textposition='outside',
        textfont=dict(color=t["text_primary"], size=12),
        hovertemplate="<b>%{y}</b><br>Adoption Rate: %{x:.1f}%<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(
            text="🌍 Average Adoption Rate by Region",
            font=dict(size=16, color=t["text_primary"])
        ),
        xaxis=dict(
            title="Adoption Rate (%)",
            gridcolor=t["grid"],
            linecolor=t["border"],
            tickfont=dict(color=t["text_secondary"]),
            titlefont=dict(color=t["text_secondary"]),
            range=[0, regional[metric].max() * 1.2]
        ),
        yaxis=dict(
            title="",
            linecolor=t["border"],
            tickfont=dict(color=t["text_primary"])
        ),
        paper_bgcolor=t["chart_bg"],
        plot_bgcolor=t["chart_bg"],
        height=380,
        margin=dict(l=120, r=60, t=60, b=40)
    )
    
    return fig

# =============================================================================
# CHART 3: DONUT CHART - Policy Distribution
# =============================================================================

def create_donut_chart(df):
    """Create donut chart showing policy stance distribution."""
    t = get_theme()
    
    policy_counts = df["policy_stance"].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=policy_counts.index,
        values=policy_counts.values,
        hole=0.6,
        marker=dict(
            colors=[POLICY_COLORS.get(p, t["accent"]) for p in policy_counts.index],
            line=dict(color=t["bg_primary"], width=3)
        ),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(color=t["text_primary"], size=12),
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>",
        pull=[0.02] * len(policy_counts)
    )])
    
    fig.update_layout(
        title=dict(
            text="📋 Policy Stance Distribution",
            font=dict(size=16, color=t["text_primary"])
        ),
        paper_bgcolor=t["chart_bg"],
        font=dict(color=t["text_primary"]),
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=False,
        annotations=[
            dict(
                text=f"<b>{len(df):,}</b><br>Total",
                x=0.5, y=0.5,
                font=dict(size=16, color=t["text_primary"]),
                showarrow=False
            )
        ]
    )
    
    return fig

# =============================================================================
# CHART 4: VERTICAL BAR - Institution Type Comparison
# =============================================================================

def create_vertical_bar(df):
    """Create vertical bar chart for institution type comparison."""
    t = get_theme()
    
    inst_data = df.groupby("institution_type").agg({
        "ai_adoption_rate": "mean",
        "institution_id": "count"
    }).reset_index()
    inst_data.columns = ["Institution Type", "Adoption Rate", "Count"]
    inst_data = inst_data.sort_values("Adoption Rate", ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=inst_data["Institution Type"],
        y=inst_data["Adoption Rate"],
        marker=dict(
            color=[INSTITUTION_COLORS.get(i, t["accent"]) for i in inst_data["Institution Type"]],
            line=dict(width=0)
        ),
        text=[f"{v:.1f}%" for v in inst_data["Adoption Rate"]],
        textposition='outside',
        textfont=dict(color=t["text_primary"], size=11),
        hovertemplate="<b>%{x}</b><br>Adoption Rate: %{y:.1f}%<br>Count: %{customdata:,}<extra></extra>",
        customdata=inst_data["Count"]
    ))
    
    fig.update_layout(
        title=dict(
            text="🏛️ Adoption Rate by Institution Type",
            font=dict(size=16, color=t["text_primary"])
        ),
        xaxis=dict(
            title="",
            tickangle=-20,
            gridcolor=t["grid"],
            linecolor=t["border"],
            tickfont=dict(color=t["text_primary"], size=10)
        ),
        yaxis=dict(
            title="Adoption Rate (%)",
            gridcolor=t["grid"],
            linecolor=t["border"],
            tickfont=dict(color=t["text_secondary"]),
            titlefont=dict(color=t["text_secondary"])
        ),
        paper_bgcolor=t["chart_bg"],
        plot_bgcolor=t["chart_bg"],
        height=400,
        margin=dict(l=60, r=30, t=60, b=100)
    )
    
    return fig

# =============================================================================
# CHART 5: HISTOGRAM - Distribution Analysis
# =============================================================================

def create_histogram(df, column):
    """Create clean histogram for distribution analysis."""
    t = get_theme()
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=df[column],
        nbinsx=25,
        marker=dict(
            color=t["accent"],
            line=dict(color=t["bg_primary"], width=1)
        ),
        hovertemplate="Range: %{x}<br>Count: %{y}<extra></extra>"
    ))
    
    # Add mean line
    mean_val = df[column].mean()
    fig.add_vline(
        x=mean_val,
        line_dash="dash",
        line_color=t["danger"],
        line_width=2,
        annotation_text=f"Mean: {mean_val:.1f}",
        annotation_position="top",
        annotation_font_color=t["text_primary"]
    )
    
    title_text = column.replace('_', ' ').title()
    
    fig.update_layout(
        title=dict(
            text=f"📊 Distribution of {title_text}",
            font=dict(size=16, color=t["text_primary"])
        ),
        xaxis=dict(
            title=title_text,
            gridcolor=t["grid"],
            linecolor=t["border"],
            tickfont=dict(color=t["text_secondary"]),
            titlefont=dict(color=t["text_secondary"])
        ),
        yaxis=dict(
            title="Frequency",
            gridcolor=t["grid"],
            linecolor=t["border"],
            tickfont=dict(color=t["text_secondary"]),
            titlefont=dict(color=t["text_secondary"])
        ),
        paper_bgcolor=t["chart_bg"],
        plot_bgcolor=t["chart_bg"],
        height=380,
        margin=dict(l=60, r=30, t=60, b=60),
        bargap=0.05
    )
    
    return fig

# =============================================================================
# CHART 6: HEATMAP - Correlation Matrix
# =============================================================================

def create_heatmap(df):
    """Create clean correlation heatmap."""
    t = get_theme()
    
    columns = [
        "ai_adoption_rate",
        "student_ai_literacy_index",
        "faculty_training_hours",
        "learning_outcome_delta",
        "integrity_incident_rate",
        "student_satisfaction_score"
    ]
    
    corr = df[columns].corr()
    
    # Clean labels
    labels = [
        "Adoption Rate",
        "AI Literacy",
        "Training Hours",
        "Learning Outcome",
        "Incident Rate",
        "Satisfaction"
    ]
    
    # Custom colorscale
    colorscale = [
        [0, "#ef4444"],
        [0.5, t["bg_card"]],
        [1, "#22c55e"]
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=labels,
        y=labels,
        colorscale=colorscale,
        zmid=0,
        zmin=-1,
        zmax=1,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        textfont=dict(size=11, color=t["text_primary"]),
        hoverongaps=False,
        hovertemplate="<b>%{x}</b> vs <b>%{y}</b><br>Correlation: %{z:.2f}<extra></extra>",
        colorbar=dict(
            title="Correlation",
            tickfont=dict(color=t["text_secondary"]),
            titlefont=dict(color=t["text_secondary"])
        )
    ))
    
    fig.update_layout(
        title=dict(
            text="🔗 Metric Correlations",
            font=dict(size=16, color=t["text_primary"])
        ),
        xaxis=dict(
            tickfont=dict(color=t["text_primary"], size=10),
            tickangle=-30
        ),
        yaxis=dict(
            tickfont=dict(color=t["text_primary"], size=10),
            autorange="reversed"
        ),
        paper_bgcolor=t["chart_bg"],
        plot_bgcolor=t["chart_bg"],
        height=450,
        margin=dict(l=100, r=30, t=60, b=100)
    )
    
    return fig

# =============================================================================
# CHART 7: GROUPED BAR - Policy vs Outcomes
# =============================================================================

def create_grouped_bar(df):
    """Create grouped bar chart comparing metrics by policy stance."""
    t = get_theme()
    
    # Aggregate by policy stance
    policy_data = df.groupby("policy_stance").agg({
        "ai_adoption_rate": "mean",
        "student_ai_literacy_index": "mean",
        "learning_outcome_delta": "mean"
    }).reset_index()
    
    # Order by policy progression
    order = ["Restrictive", "Cautious", "Permissive", "Integrated"]
    policy_data["policy_stance"] = pd.Categorical(
        policy_data["policy_stance"], 
        categories=order, 
        ordered=True
    )
    policy_data = policy_data.sort_values("policy_stance")
    
    fig = go.Figure()
    
    metrics = [
        ("ai_adoption_rate", "Adoption Rate (%)", t["accent"]),
        ("student_ai_literacy_index", "AI Literacy", "#8b5cf6"),
        ("learning_outcome_delta", "Learning Δ (%)", "#22c55e")
    ]
    
    for col, name, color in metrics:
        fig.add_trace(go.Bar(
            x=policy_data["policy_stance"],
            y=policy_data[col],
            name=name,
            marker_color=color,
            hovertemplate=f"<b>{name}</b><br>" + "%{x}: %{y:.1f}<extra></extra>"
        ))
    
    fig.update_layout(
        title=dict(
            text="📊 Key Metrics by Policy Stance",
            font=dict(size=16, color=t["text_primary"])
        ),
        xaxis=dict(
            title="Policy Stance",
            gridcolor=t["grid"],
            linecolor=t["border"],
            tickfont=dict(color=t["text_primary"]),
            titlefont=dict(color=t["text_secondary"])
        ),
        yaxis=dict(
            title="Value",
            gridcolor=t["grid"],
            linecolor=t["border"],
            tickfont=dict(color=t["text_secondary"]),
            titlefont=dict(color=t["text_secondary"])
        ),
        paper_bgcolor=t["chart_bg"],
        plot_bgcolor=t["chart_bg"],
        barmode='group',
        height=400,
        margin=dict(l=60, r=30, t=60, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(color=t["text_primary"])
        )
    )
    
    return fig

# =============================================================================
# CHART 8: BUBBLE CHART - Multi-dimensional Analysis
# =============================================================================

def create_bubble_chart(df):
    """Create bubble chart for multi-dimensional analysis."""
    t = get_theme()
    
    # Aggregate by region and institution type
    bubble_data = df.groupby(["region", "institution_type"]).agg({
        "ai_adoption_rate": "mean",
        "student_satisfaction_score": "mean",
        "institution_id": "count"
    }).reset_index()
    bubble_data.columns = ["Region", "Institution Type", "Adoption Rate", "Satisfaction", "Count"]
    
    # Sample for cleaner visualization
    bubble_data = bubble_data.nlargest(20, "Count")
    
    fig = go.Figure()
    
    for region in bubble_data["Region"].unique():
        region_data = bubble_data[bubble_data["Region"] == region]
        
        fig.add_trace(go.Scatter(
            x=region_data["Adoption Rate"],
            y=region_data["Satisfaction"],
            mode='markers',
            name=region,
            marker=dict(
                size=region_data["Count"] / region_data["Count"].max() * 50 + 10,
                color=REGION_COLORS.get(region, t["accent"]),
                opacity=0.7,
                line=dict(color='white', width=1)
            ),
            text=region_data["Institution Type"],
            hovertemplate="<b>%{text}</b><br>" +
                          "Region: " + region + "<br>" +
                          "Adoption: %{x:.1f}%<br>" +
                          "Satisfaction: %{y:.2f}<br>" +
                          "Count: %{marker.size:.0f}<extra></extra>"
        ))
    
    fig.update_layout(
        title=dict(
            text="🔵 Adoption vs Satisfaction (Bubble Size = Count)",
            font=dict(size=16, color=t["text_primary"])
        ),
        xaxis=dict(
            title="AI Adoption Rate (%)",
            gridcolor=t["grid"],
            linecolor=t["border"],
            tickfont=dict(color=t["text_secondary"]),
            titlefont=dict(color=t["text_secondary"])
        ),
        yaxis=dict(
            title="Student Satisfaction Score",
            gridcolor=t["grid"],
            linecolor=t["border"],
            tickfont=dict(color=t["text_secondary"]),
            titlefont=dict(color=t["text_secondary"])
        ),
        paper_bgcolor=t["chart_bg"],
        plot_bgcolor=t["chart_bg"],
        height=450,
        margin=dict(l=60, r=30, t=60, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(color=t["text_primary"])
        )
    )
    
    return fig

# =============================================================================
# SIDEBAR
# =============================================================================

def render_sidebar(df):
    """Render sidebar with theme toggle and filters."""
    t = get_theme()
    
    with st.sidebar:
        # Logo/Title
        st.markdown("## 🎓 GenAI Dashboard")
        st.caption("Higher Education AI Adoption")
        
        st.markdown("---")
        
        # Theme Toggle
        st.markdown("### ⚙️ Theme")
        
        current = st.session_state.theme
        new_theme = "light" if current == "dark" else "dark"
        icon = "☀️ Light Mode" if current == "dark" else "🌙 Dark Mode"
        
        if st.button(f"Switch to {icon}", use_container_width=True):
            st.session_state.theme = new_theme
            st.rerun()
        
        st.markdown("---")
        
        # Filters
        st.markdown("### 🔍 Filters")
        
        # Region
        regions = st.multiselect(
            "🌍 Region",
            options=sorted(df["region"].unique()),
            default=[],
            help="Select regions (empty = all)"
        )
        
        # Institution Type
        inst_types = st.multiselect(
            "🏛️ Institution Type",
            options=sorted(df["institution_type"].unique()),
            default=[],
            help="Select institution types"
        )
        
        # Policy Stance
        policies = st.multiselect(
            "📋 Policy Stance",
            options=["Restrictive", "Cautious", "Permissive", "Integrated"],
            default=[],
            help="Select policy stances"
        )
        
        # Quarter
        quarters = st.multiselect(
            "📅 Quarter",
            options=sorted(df["survey_quarter"].unique()),
            default=[],
            help="Select time periods"
        )
        
        st.markdown("---")
        
        # Dataset Info
        st.markdown("### 📊 Dataset Info")
        st.caption(f"**Records:** {len(df):,}")
        st.caption(f"**Countries:** {df['country'].nunique()}")
        st.caption(f"**Period:** 2023-Q1 to 2024-Q4")
        
        return {
            "regions": regions,
            "inst_types": inst_types,
            "policies": policies,
            "quarters": quarters
        }

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    
    # Apply CSS
    apply_theme_css()
    t = get_theme()
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("❌ Dataset not found. Please ensure 'data/dataset.csv' exists.")
        st.stop()
    
    # Render sidebar and get filters
    filters = render_sidebar(df)
    
    # Apply filters
    filtered_df = df.copy()
    
    if filters["regions"]:
        filtered_df = filtered_df[filtered_df["region"].isin(filters["regions"])]
    if filters["inst_types"]:
        filtered_df = filtered_df[filtered_df["institution_type"].isin(filters["inst_types"])]
    if filters["policies"]:
        filtered_df = filtered_df[filtered_df["policy_stance"].isin(filters["policies"])]
    if filters["quarters"]:
        filtered_df = filtered_df[filtered_df["survey_quarter"].isin(filters["quarters"])]
    
    # Check filtered data
    if len(filtered_df) == 0:
        st.warning("⚠️ No data matches your filters. Please adjust your selection.")
        st.stop()
    
    # ===== HEADER =====
    st.markdown('<h1 class="main-title">🎓 Generative AI in Higher Education</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">Exploring global adoption patterns, policies, and outcomes across institutions worldwide</p>', unsafe_allow_html=True)
    
    # Filter summary
    st.markdown(f"""
    <div class="info-box">
        📊 Displaying <strong>{len(filtered_df):,}</strong> institutions from 
        <strong>{filtered_df['country'].nunique()}</strong> countries across 
        <strong>{filtered_df['region'].nunique()}</strong> regions
    </div>
    """, unsafe_allow_html=True)
    
    # ===== KPI SECTION =====
    st.markdown('<div class="section-title">📈 Key Performance Indicators</div>', unsafe_allow_html=True)
    
    # Calculate KPIs
    avg_adoption = filtered_df["ai_adoption_rate"].mean()
    avg_literacy = filtered_df["student_ai_literacy_index"].mean()
    avg_satisfaction = filtered_df["student_satisfaction_score"].mean()
    avg_outcome = filtered_df["learning_outcome_delta"].mean()
    avg_incident = filtered_df["integrity_incident_rate"].mean()
    avg_training = filtered_df["faculty_training_hours"].mean()
    integrated_pct = (filtered_df["policy_stance"] == "Integrated").mean() * 100
    high_adoption_pct = (filtered_df["ai_adoption_rate"] >= 45).mean() * 100
    
    # KPI Row 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Institutions", f"{len(filtered_df):,}")
    with col2:
        st.metric("📈 Avg Adoption", f"{avg_adoption:.1f}%")
    with col3:
        st.metric("🎓 Avg AI Literacy", f"{avg_literacy:.1f}")
    with col4:
        st.metric("⭐ Avg Satisfaction", f"{avg_satisfaction:.2f}")
    
    # KPI Row 2
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("🌍 Countries", f"{filtered_df['country'].nunique()}")
    with col6:
        delta_color = "normal" if avg_outcome >= 0 else "inverse"
        st.metric("📚 Learning Delta", f"{avg_outcome:+.1f}%")
    with col7:
        st.metric("⚠️ Incident Rate", f"{avg_incident:.1f}")
    with col8:
        st.metric("✅ Integrated Policy", f"{integrated_pct:.1f}%")
    
    st.markdown("---")
    
    # ===== CHART TABS =====
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Deep Analysis", "📈 Insights"])
    
    # ----- TAB 1: OVERVIEW -----
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_line_chart(filtered_df), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_horizontal_bar(filtered_df), use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.plotly_chart(create_donut_chart(filtered_df), use_container_width=True)
        
        with col4:
            st.plotly_chart(create_vertical_bar(filtered_df), use_container_width=True)
    
    # ----- TAB 2: DEEP ANALYSIS -----
    with tab2:
        # Histogram with selector
        st.markdown("#### 📊 Distribution Analysis")
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            hist_metric = st.selectbox(
                "Select Metric",
                options=[
                    "ai_adoption_rate",
                    "student_ai_literacy_index",
                    "faculty_training_hours",
                    "learning_outcome_delta",
                    "integrity_incident_rate",
                    "student_satisfaction_score"
                ],
                format_func=lambda x: x.replace("_", " ").title()
            )
        
        with col2:
            st.plotly_chart(create_histogram(filtered_df, hist_metric), use_container_width=True)
        
        st.markdown("---")
        
        # Correlation Heatmap
        st.plotly_chart(create_heatmap(filtered_df), use_container_width=True)
    
    # ----- TAB 3: INSIGHTS -----
    with tab3:
        st.markdown("#### 📊 Policy Impact Analysis")
        st.markdown("*How do different policy stances affect key outcomes?*")
        
        st.plotly_chart(create_grouped_bar(filtered_df), use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("#### 🔵 Multi-dimensional View")
        st.markdown("*Relationship between adoption, satisfaction, and institution count*")
        
        st.plotly_chart(create_bubble_chart(filtered_df), use_container_width=True)
    
    st.markdown("---")
    
    # ===== DATA EXPLORER =====
    st.markdown('<div class="section-title">📋 Data Explorer</div>', unsafe_allow_html=True)
    
    with st.expander("🔍 View Data Sample (Top 100 Records)", expanded=False):
        display_cols = [
            "institution_name", "country", "region", "institution_type",
            "ai_adoption_rate", "policy_stance", "student_ai_literacy_index",
            "learning_outcome_delta", "student_satisfaction_score"
        ]
        st.dataframe(
            filtered_df[display_cols].head(100),
            use_container_width=True,
            hide_index=True
        )
    
    # Download buttons
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Full Data (CSV)",
            data=csv,
            file_name="genai_education_data.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        summary = filtered_df.describe().round(2).to_csv().encode('utf-8')
        st.download_button(
            label="📊 Download Summary Stats",
            data=summary,
            file_name="genai_education_summary.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # ===== FOOTER =====
    st.markdown("""
    <div class="footer">
        <strong>🎓 GenAI in Higher Education Dashboard</strong><br>
        Synthetic data for research demonstration • Built with Streamlit & Plotly<br>
        5,000 simulated institutions across 45+ countries
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    main()
