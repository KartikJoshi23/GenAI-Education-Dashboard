"""
GenAI in Higher Education - Dashboard
Clean and simple version that works reliably
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="GenAI Education Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# THEME SETUP
# =============================================================================

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

THEMES = {
    "dark": {
        "bg": "#0a0a0a",
        "card": "#1a1a1a",
        "text": "#ffffff",
        "text2": "#a0a0a0",
        "accent": "#6366f1",
        "grid": "#2a2a2a",
        "success": "#22c55e",
        "danger": "#ef4444"
    },
    "light": {
        "bg": "#ffffff",
        "card": "#f8f9fa",
        "text": "#1a1a1a",
        "text2": "#6b7280",
        "accent": "#4f46e5",
        "grid": "#e5e7eb",
        "success": "#16a34a",
        "danger": "#dc2626"
    }
}

def get_theme():
    return THEMES[st.session_state.theme]

# Color maps
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

INST_COLORS = {
    "Research University": "#6366f1",
    "Teaching University": "#8b5cf6",
    "Liberal Arts College": "#ec4899",
    "Technical Institute": "#22c55e",
    "Community College": "#f59e0b"
}

# =============================================================================
# CSS
# =============================================================================

def apply_css():
    t = get_theme()
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {t["bg"]};
        }}
        
        .main .block-container {{
            padding: 2rem 3rem;
            max-width: 1400px;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: {t["card"]};
        }}
        
        [data-testid="stSidebar"] * {{
            color: {t["text"]} !important;
        }}
        
        h1, h2, h3, h4, h5, h6, p, span, label {{
            color: {t["text"]} !important;
        }}
        
        .main-title {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {t["text"]} !important;
            margin-bottom: 0.5rem;
        }}
        
        .subtitle {{
            font-size: 1.1rem;
            color: {t["text2"]} !important;
            margin-bottom: 2rem;
        }}
        
        .section-header {{
            font-size: 1.3rem;
            font-weight: 600;
            color: {t["text"]} !important;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {t["accent"]};
        }}
        
        [data-testid="stMetricValue"] {{
            color: {t["accent"]} !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {t["text2"]} !important;
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            background-color: {t["card"]};
            border-radius: 10px;
            padding: 0.25rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: {t["text2"]} !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {t["accent"]} !important;
            color: white !important;
            border-radius: 8px;
        }}
        
        .info-box {{
            background: {t["card"]};
            border-left: 4px solid {t["accent"]};
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }}
        
        .stButton > button {{
            background-color: {t["accent"]};
            color: white;
            border: none;
            border-radius: 8px;
        }}
        
        .stDownloadButton > button {{
            background-color: {t["success"]};
            color: white;
        }}
        
        .footer {{
            text-align: center;
            color: {t["text2"]};
            padding: 2rem;
            margin-top: 2rem;
            border-top: 1px solid {t["grid"]};
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# DATA LOADING
# =============================================================================

@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/dataset.csv")
    except:
        return None

# =============================================================================
# CHART 1: LINE CHART
# =============================================================================

def chart_line(df):
    t = get_theme()
    
    trend = df.groupby(["survey_quarter", "region"])["ai_adoption_rate"].mean().reset_index()
    
    fig = px.line(
        trend,
        x="survey_quarter",
        y="ai_adoption_rate",
        color="region",
        markers=True,
        color_discrete_map=REGION_COLORS,
        title="📈 AI Adoption Trends by Region"
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=t["text"],
        height=420,
        xaxis=dict(gridcolor=t["grid"], title="Quarter"),
        yaxis=dict(gridcolor=t["grid"], title="Adoption Rate (%)"),
        legend=dict(orientation="h", y=-0.2)
    )
    
    return fig

# =============================================================================
# CHART 2: HORIZONTAL BAR
# =============================================================================

def chart_hbar(df):
    t = get_theme()
    
    regional = df.groupby("region")["ai_adoption_rate"].mean().sort_values().reset_index()
    
    fig = px.bar(
        regional,
        x="ai_adoption_rate",
        y="region",
        orientation="h",
        color="region",
        color_discrete_map=REGION_COLORS,
        title="🌍 Average Adoption by Region",
        text=regional["ai_adoption_rate"].round(1)
    )
    
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=t["text"],
        height=380,
        showlegend=False,
        xaxis=dict(gridcolor=t["grid"], title="Adoption Rate (%)"),
        yaxis=dict(gridcolor=t["grid"], title="")
    )
    
    return fig

# =============================================================================
# CHART 3: PIE/DONUT CHART
# =============================================================================

def chart_donut(df):
    t = get_theme()
    
    policy_counts = df["policy_stance"].value_counts().reset_index()
    policy_counts.columns = ["Policy", "Count"]
    
    fig = px.pie(
        policy_counts,
        values="Count",
        names="Policy",
        hole=0.5,
        color="Policy",
        color_discrete_map=POLICY_COLORS,
        title="📋 Policy Stance Distribution"
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color=t["text"],
        height=400
    )
    
    return fig

# =============================================================================
# CHART 4: VERTICAL BAR
# =============================================================================

def chart_vbar(df):
    t = get_theme()
    
    inst = df.groupby("institution_type")["ai_adoption_rate"].mean().sort_values(ascending=False).reset_index()
    
    fig = px.bar(
        inst,
        x="institution_type",
        y="ai_adoption_rate",
        color="institution_type",
        color_discrete_map=INST_COLORS,
        title="🏛️ Adoption by Institution Type",
        text=inst["ai_adoption_rate"].round(1)
    )
    
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=t["text"],
        height=400,
        showlegend=False,
        xaxis=dict(gridcolor=t["grid"], title="", tickangle=-20),
        yaxis=dict(gridcolor=t["grid"], title="Adoption Rate (%)")
    )
    
    return fig

# =============================================================================
# CHART 5: HISTOGRAM
# =============================================================================

def chart_histogram(df, column):
    t = get_theme()
    
    title_text = column.replace("_", " ").title()
    
    fig = px.histogram(
        df,
        x=column,
        nbins=25,
        title=f"📊 Distribution: {title_text}",
        color_discrete_sequence=[t["accent"]]
    )
    
    # Add mean line
    mean_val = df[column].mean()
    fig.add_vline(x=mean_val, line_dash="dash", line_color=t["danger"],
                  annotation_text=f"Mean: {mean_val:.1f}")
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=t["text"],
        height=380,
        xaxis=dict(gridcolor=t["grid"], title=title_text),
        yaxis=dict(gridcolor=t["grid"], title="Frequency")
    )
    
    return fig

# =============================================================================
# CHART 6: HEATMAP
# =============================================================================

def chart_heatmap(df):
    t = get_theme()
    
    cols = [
        "ai_adoption_rate",
        "student_ai_literacy_index",
        "faculty_training_hours",
        "learning_outcome_delta",
        "integrity_incident_rate",
        "student_satisfaction_score"
    ]
    
    corr = df[cols].corr()
    
    labels = ["Adoption", "Literacy", "Training", "Outcome", "Incidents", "Satisfaction"]
    
    fig = px.imshow(
        corr,
        x=labels,
        y=labels,
        color_continuous_scale="RdBu",
        aspect="auto",
        title="🔗 Metric Correlations",
        text_auto=".2f"
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color=t["text"],
        height=450
    )
    
    return fig

# =============================================================================
# CHART 7: GROUPED BAR - Policy Impact
# =============================================================================

def chart_policy_impact(df):
    t = get_theme()
    
    policy_data = df.groupby("policy_stance").agg({
        "ai_adoption_rate": "mean",
        "student_ai_literacy_index": "mean",
        "learning_outcome_delta": "mean"
    }).reset_index()
    
    # Melt for grouped bar
    melted = policy_data.melt(
        id_vars="policy_stance",
        var_name="Metric",
        value_name="Value"
    )
    
    # Clean metric names
    melted["Metric"] = melted["Metric"].replace({
        "ai_adoption_rate": "Adoption Rate",
        "student_ai_literacy_index": "AI Literacy",
        "learning_outcome_delta": "Learning Δ"
    })
    
    fig = px.bar(
        melted,
        x="policy_stance",
        y="Value",
        color="Metric",
        barmode="group",
        title="📊 Key Metrics by Policy Stance",
        color_discrete_sequence=[t["accent"], "#8b5cf6", "#22c55e"]
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=t["text"],
        height=400,
        xaxis=dict(gridcolor=t["grid"], title="Policy Stance"),
        yaxis=dict(gridcolor=t["grid"], title="Value"),
        legend=dict(orientation="h", y=-0.2)
    )
    
    return fig

# =============================================================================
# CHART 8: SCATTER BUBBLE
# =============================================================================

def chart_bubble(df):
    t = get_theme()
    
    # Aggregate
    bubble = df.groupby("region").agg({
        "ai_adoption_rate": "mean",
        "student_satisfaction_score": "mean",
        "institution_id": "count"
    }).reset_index()
    bubble.columns = ["Region", "Adoption", "Satisfaction", "Count"]
    
    fig = px.scatter(
        bubble,
        x="Adoption",
        y="Satisfaction",
        size="Count",
        color="Region",
        color_discrete_map=REGION_COLORS,
        title="🔵 Adoption vs Satisfaction by Region",
        size_max=60,
        hover_data=["Count"]
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=t["text"],
        height=450,
        xaxis=dict(gridcolor=t["grid"], title="Adoption Rate (%)"),
        yaxis=dict(gridcolor=t["grid"], title="Satisfaction Score")
    )
    
    return fig

# =============================================================================
# MAIN APP
# =============================================================================

def main():
    apply_css()
    t = get_theme()
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("❌ Dataset not found. Please ensure 'data/dataset.csv' exists.")
        st.stop()
    
    # ===== SIDEBAR =====
    with st.sidebar:
        st.markdown("## 🎓 GenAI Dashboard")
        st.caption("Higher Education AI Adoption")
        st.markdown("---")
        
        # Theme Toggle
        st.markdown("### ⚙️ Appearance")
        current_theme = "🌙 Dark" if st.session_state.theme == "dark" else "☀️ Light"
        st.write(f"Current: **{current_theme}**")
        
        if st.button("🔄 Toggle Theme", use_container_width=True):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()
        
        st.markdown("---")
        
        # Filters
        st.markdown("### 🔍 Filters")
        
        regions = st.multiselect(
            "🌍 Region",
            options=sorted(df["region"].unique()),
            default=[]
        )
        
        inst_types = st.multiselect(
            "🏛️ Institution Type",
            options=sorted(df["institution_type"].unique()),
            default=[]
        )
        
        policies = st.multiselect(
            "📋 Policy Stance",
            options=["Restrictive", "Cautious", "Permissive", "Integrated"],
            default=[]
        )
        
        quarters = st.multiselect(
            "📅 Quarter",
            options=sorted(df["survey_quarter"].unique()),
            default=[]
        )
        
        st.markdown("---")
        st.markdown("### 📊 Dataset")
        st.caption(f"Records: {len(df):,}")
        st.caption(f"Countries: {df['country'].nunique()}")
    
    # Apply filters
    filtered = df.copy()
    if regions:
        filtered = filtered[filtered["region"].isin(regions)]
    if inst_types:
        filtered = filtered[filtered["institution_type"].isin(inst_types)]
    if policies:
        filtered = filtered[filtered["policy_stance"].isin(policies)]
    if quarters:
        filtered = filtered[filtered["survey_quarter"].isin(quarters)]
    
    if len(filtered) == 0:
        st.warning("⚠️ No data matches filters. Please adjust.")
        st.stop()
    
    # ===== HEADER =====
    st.markdown('<h1 class="main-title">🎓 Generative AI in Higher Education</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Global Adoption & Policy Dashboard — Exploring how universities adopt and govern AI tools</p>', unsafe_allow_html=True)
    
    # Info box
    st.markdown(f"""
    <div class="info-box">
        📊 Showing <strong>{len(filtered):,}</strong> institutions from 
        <strong>{filtered['country'].nunique()}</strong> countries
    </div>
    """, unsafe_allow_html=True)
    
    # ===== KPIs =====
    st.markdown('<p class="section-header">📈 Key Metrics</p>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Institutions", f"{len(filtered):,}")
    c2.metric("Avg Adoption", f"{filtered['ai_adoption_rate'].mean():.1f}%")
    c3.metric("Avg AI Literacy", f"{filtered['student_ai_literacy_index'].mean():.1f}")
    c4.metric("Avg Satisfaction", f"{filtered['student_satisfaction_score'].mean():.2f}")
    
    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Countries", f"{filtered['country'].nunique()}")
    c6.metric("Learning Delta", f"{filtered['learning_outcome_delta'].mean():+.1f}%")
    c7.metric("Incident Rate", f"{filtered['integrity_incident_rate'].mean():.1f}")
    c8.metric("Training Hours", f"{filtered['faculty_training_hours'].mean():.1f}")
    
    st.markdown("---")
    
    # ===== TABS =====
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Analysis", "📈 Insights"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(chart_line(filtered), use_container_width=True)
        with col2:
            st.plotly_chart(chart_hbar(filtered), use_container_width=True)
        
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(chart_donut(filtered), use_container_width=True)
        with col4:
            st.plotly_chart(chart_vbar(filtered), use_container_width=True)
    
    with tab2:
        st.markdown("#### Select a metric to analyze its distribution:")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            metric = st.selectbox(
                "Metric",
                ["ai_adoption_rate", "student_ai_literacy_index", "faculty_training_hours",
                 "learning_outcome_delta", "integrity_incident_rate", "student_satisfaction_score"],
                format_func=lambda x: x.replace("_", " ").title()
            )
        with col2:
            st.plotly_chart(chart_histogram(filtered, metric), use_container_width=True)
        
        st.markdown("---")
        st.plotly_chart(chart_heatmap(filtered), use_container_width=True)
    
    with tab3:
        st.markdown("#### How different policies affect outcomes:")
        st.plotly_chart(chart_policy_impact(filtered), use_container_width=True)
        
        st.markdown("---")
        st.markdown("#### Regional comparison (bubble size = institution count):")
        st.plotly_chart(chart_bubble(filtered), use_container_width=True)
    
    st.markdown("---")
    
    # ===== DATA EXPLORER =====
    st.markdown('<p class="section-header">📋 Data Explorer</p>', unsafe_allow_html=True)
    
    with st.expander("🔍 View Data (Top 100)"):
        cols = ["institution_name", "country", "region", "institution_type",
                "ai_adoption_rate", "policy_stance", "student_ai_literacy_index",
                "learning_outcome_delta", "student_satisfaction_score"]
        st.dataframe(filtered[cols].head(100), use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns(2)
    with col1:
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Data (CSV)", csv, "genai_data.csv", "text/csv", use_container_width=True)
    with col2:
        summary = filtered.describe().round(2).to_csv().encode('utf-8')
        st.download_button("📊 Download Summary", summary, "summary.csv", "text/csv", use_container_width=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        🎓 GenAI in Higher Education Dashboard<br>
        Synthetic data for research • 5,000 institutions • 45+ countries
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
