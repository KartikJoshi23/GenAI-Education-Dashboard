"""
GenAI in Higher Education - Interactive Dashboard
Simplified version for reliable deployment
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
# THEME CONFIGURATION
# =============================================================================

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def get_colors():
    """Get colors based on current theme."""
    if st.session_state.theme == "dark":
        return {
            "bg": "#0f172a",
            "card": "#1e293b",
            "text": "#e2e8f0",
            "text2": "#94a3b8",
            "primary": "#6366f1",
            "success": "#10b981",
            "warning": "#f59e0b",
            "danger": "#ef4444",
            "grid": "#334155"
        }
    else:
        return {
            "bg": "#ffffff",
            "card": "#f8fafc",
            "text": "#1e293b",
            "text2": "#475569",
            "primary": "#4f46e5",
            "success": "#059669",
            "warning": "#d97706",
            "danger": "#dc2626",
            "grid": "#e2e8f0"
        }

REGION_COLORS = {
    "North America": "#6366f1",
    "Europe": "#8b5cf6",
    "Asia Pacific": "#ec4899",
    "Latin America": "#10b981",
    "Middle East": "#f59e0b",
    "Africa": "#3b82f6"
}

POLICY_COLORS = {
    "Restrictive": "#ef4444",
    "Cautious": "#f59e0b",
    "Permissive": "#3b82f6",
    "Integrated": "#10b981"
}

INST_COLORS = {
    "Research University": "#6366f1",
    "Teaching University": "#8b5cf6",
    "Liberal Arts College": "#ec4899",
    "Technical Institute": "#10b981",
    "Community College": "#f59e0b"
}

# =============================================================================
# CUSTOM CSS
# =============================================================================

def apply_css():
    colors = get_colors()
    st.markdown(f"""
    <style>
        .main .block-container {{
            padding-top: 1rem;
            max-width: 1400px;
        }}
        
        .metric-card {{
            background: {colors["card"]};
            border-radius: 10px;
            padding: 1rem;
            border: 1px solid {colors["grid"]};
        }}
        
        .metric-value {{
            font-size: 1.8rem;
            font-weight: 700;
            color: {colors["primary"]};
        }}
        
        .metric-label {{
            font-size: 0.9rem;
            color: {colors["text2"]};
        }}
        
        .section-header {{
            font-size: 1.3rem;
            font-weight: 600;
            color: {colors["text"]};
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {colors["primary"]};
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
    """Load the dataset."""
    try:
        df = pd.read_csv("data/dataset.csv")
        return df
    except FileNotFoundError:
        st.error("Dataset not found! Please ensure 'data/dataset.csv' exists.")
        return None

# =============================================================================
# CHART FUNCTIONS
# =============================================================================

def chart_line_trend(df):
    """Line chart: Adoption trends over time."""
    colors = get_colors()
    
    trend = df.groupby(["survey_quarter", "region"])["ai_adoption_rate"].mean().reset_index()
    
    fig = px.line(
        trend,
        x="survey_quarter",
        y="ai_adoption_rate",
        color="region",
        markers=True,
        color_discrete_map=REGION_COLORS
    )
    
    fig.update_layout(
        title="AI Adoption Trends by Region",
        xaxis_title="Quarter",
        yaxis_title="Adoption Rate (%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=colors["text"],
        height=400,
        xaxis=dict(gridcolor=colors["grid"]),
        yaxis=dict(gridcolor=colors["grid"])
    )
    
    return fig


def chart_bar_regional(df):
    """Horizontal bar: Regional comparison."""
    colors = get_colors()
    
    regional = df.groupby("region")["ai_adoption_rate"].mean().sort_values()
    
    fig = go.Figure(go.Bar(
        x=regional.values,
        y=regional.index,
        orientation='h',
        marker_color=[REGION_COLORS.get(r, colors["primary"]) for r in regional.index],
        text=[f"{v:.1f}%" for v in regional.values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Average Adoption Rate by Region",
        xaxis_title="Adoption Rate (%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=colors["text"],
        height=380,
        xaxis=dict(gridcolor=colors["grid"]),
        yaxis=dict(gridcolor=colors["grid"])
    )
    
    return fig


def chart_donut_policy(df):
    """Donut chart: Policy distribution."""
    colors = get_colors()
    
    policy_counts = df["policy_stance"].value_counts()
    
    fig = go.Figure(go.Pie(
        labels=policy_counts.index,
        values=policy_counts.values,
        hole=0.5,
        marker_colors=[POLICY_COLORS.get(p, colors["primary"]) for p in policy_counts.index]
    ))
    
    fig.update_layout(
        title="Policy Stance Distribution",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color=colors["text"],
        height=400
    )
    
    return fig


def chart_bar_institution(df):
    """Grouped bar: By institution type."""
    colors = get_colors()
    
    inst = df.groupby("institution_type")["ai_adoption_rate"].mean().sort_values(ascending=False)
    
    fig = go.Figure(go.Bar(
        x=inst.index,
        y=inst.values,
        marker_color=[INST_COLORS.get(i, colors["primary"]) for i in inst.index],
        text=[f"{v:.1f}%" for v in inst.values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Adoption Rate by Institution Type",
        yaxis_title="Adoption Rate (%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=colors["text"],
        height=400,
        xaxis=dict(gridcolor=colors["grid"], tickangle=-30),
        yaxis=dict(gridcolor=colors["grid"])
    )
    
    return fig


def chart_histogram(df, column):
    """Histogram: Distribution analysis."""
    colors = get_colors()
    
    fig = px.histogram(
        df,
        x=column,
        nbins=30,
        color_discrete_sequence=[colors["primary"]]
    )
    
    fig.update_layout(
        title=f"Distribution: {column.replace('_', ' ').title()}",
        xaxis_title=column.replace('_', ' ').title(),
        yaxis_title="Frequency",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=colors["text"],
        height=380,
        xaxis=dict(gridcolor=colors["grid"]),
        yaxis=dict(gridcolor=colors["grid"])
    )
    
    return fig


def chart_heatmap(df):
    """Heatmap: Correlation matrix."""
    colors = get_colors()
    
    cols = ["ai_adoption_rate", "student_ai_literacy_index", "integrity_incident_rate",
            "learning_outcome_delta", "faculty_training_hours", "student_satisfaction_score"]
    
    corr = df[cols].corr()
    
    labels = [c.replace('_', ' ').title()[:15] for c in cols]
    
    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=labels,
        y=labels,
        colorscale="RdBu",
        zmid=0,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        textfont={"size": 10}
    ))
    
    fig.update_layout(
        title="Metric Correlations",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color=colors["text"],
        height=450
    )
    
    return fig


def chart_scatter(df, x_col, y_col):
    """Scatter plot: Relationship analysis."""
    colors = get_colors()
    
    sample = df.sample(n=min(1000, len(df)), random_state=42)
    
    fig = px.scatter(
        sample,
        x=x_col,
        y=y_col,
        color="region",
        color_discrete_map=REGION_COLORS,
        opacity=0.6,
        trendline="ols"
    )
    
    fig.update_layout(
        title=f"{x_col.replace('_', ' ').title()} vs {y_col.replace('_', ' ').title()}",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=colors["text"],
        height=420,
        xaxis=dict(gridcolor=colors["grid"]),
        yaxis=dict(gridcolor=colors["grid"])
    )
    
    return fig


def chart_box(df, y_col, x_col):
    """Box plot: Distribution by category."""
    colors = get_colors()
    
    if x_col == "region":
        color_map = REGION_COLORS
    elif x_col == "policy_stance":
        color_map = POLICY_COLORS
    else:
        color_map = INST_COLORS
    
    fig = px.box(
        df,
        x=x_col,
        y=y_col,
        color=x_col,
        color_discrete_map=color_map
    )
    
    fig.update_layout(
        title=f"{y_col.replace('_', ' ').title()} by {x_col.replace('_', ' ').title()}",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=colors["text"],
        height=420,
        showlegend=False,
        xaxis=dict(gridcolor=colors["grid"], tickangle=-30),
        yaxis=dict(gridcolor=colors["grid"])
    )
    
    return fig

# =============================================================================
# MAIN APP
# =============================================================================

def main():
    # Apply CSS
    apply_css()
    colors = get_colors()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎓 GenAI Dashboard")
        st.markdown("---")
        
        # Theme Toggle
        st.markdown("### ⚙️ Settings")
        theme_label = "🌙 Dark Mode" if st.session_state.theme == "dark" else "☀️ Light Mode"
        if st.button(f"Switch to {'Light' if st.session_state.theme == 'dark' else 'Dark'} Mode"):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()
        
        st.markdown("---")
    
    # Load data
    df = load_data()
    
    if df is None:
        st.stop()
    
    # Sidebar Filters
    with st.sidebar:
        st.markdown("### 🔍 Filters")
        
        # Region filter
        all_regions = df["region"].unique().tolist()
        selected_regions = st.multiselect(
            "Regions",
            options=all_regions,
            default=[]
        )
        
        # Institution type filter
        all_inst = df["institution_type"].unique().tolist()
        selected_inst = st.multiselect(
            "Institution Type",
            options=all_inst,
            default=[]
        )
        
        # Policy filter
        all_policy = df["policy_stance"].unique().tolist()
        selected_policy = st.multiselect(
            "Policy Stance",
            options=all_policy,
            default=[]
        )
        
        # Quarter filter
        all_quarters = sorted(df["survey_quarter"].unique().tolist())
        selected_quarters = st.multiselect(
            "Quarters",
            options=all_quarters,
            default=all_quarters
        )
        
        st.markdown("---")
        st.caption(f"📊 Total Records: {len(df):,}")
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_regions:
        filtered_df = filtered_df[filtered_df["region"].isin(selected_regions)]
    if selected_inst:
        filtered_df = filtered_df[filtered_df["institution_type"].isin(selected_inst)]
    if selected_policy:
        filtered_df = filtered_df[filtered_df["policy_stance"].isin(selected_policy)]
    if selected_quarters:
        filtered_df = filtered_df[filtered_df["survey_quarter"].isin(selected_quarters)]
    
    # Header
    st.markdown("# 🎓 Generative AI in Higher Education")
    st.markdown("*Global Adoption & Policy Dashboard*")
    
    st.info(f"📊 Showing **{len(filtered_df):,}** institutions from **{filtered_df['country'].nunique()}** countries")
    
    # KPI Section
    st.markdown('<p class="section-header">📈 Key Metrics</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Institutions", f"{len(filtered_df):,}")
    
    with col2:
        st.metric("Avg Adoption Rate", f"{filtered_df['ai_adoption_rate'].mean():.1f}%")
    
    with col3:
        st.metric("Avg AI Literacy", f"{filtered_df['student_ai_literacy_index'].mean():.1f}")
    
    with col4:
        st.metric("Avg Satisfaction", f"{filtered_df['student_satisfaction_score'].mean():.2f}/5")
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("Countries", f"{filtered_df['country'].nunique()}")
    
    with col6:
        st.metric("Avg Incident Rate", f"{filtered_df['integrity_incident_rate'].mean():.1f}")
    
    with col7:
        st.metric("Avg Learning Δ", f"{filtered_df['learning_outcome_delta'].mean():+.1f}%")
    
    with col8:
        integrated_pct = (filtered_df["policy_stance"] == "Integrated").mean() * 100
        st.metric("Integrated Policy %", f"{integrated_pct:.1f}%")
    
    st.markdown("---")
    
    # Charts - Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Analysis", "📈 Relationships"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(chart_line_trend(filtered_df), use_container_width=True)
        with col2:
            st.plotly_chart(chart_bar_regional(filtered_df), use_container_width=True)
        
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(chart_donut_policy(filtered_df), use_container_width=True)
        with col4:
            st.plotly_chart(chart_bar_institution(filtered_df), use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns([1, 3])
        with col1:
            hist_col = st.selectbox(
                "Select Metric",
                ["ai_adoption_rate", "student_ai_literacy_index", 
                 "integrity_incident_rate", "learning_outcome_delta",
                 "faculty_training_hours", "student_satisfaction_score"],
                format_func=lambda x: x.replace('_', ' ').title()
            )
        with col2:
            st.plotly_chart(chart_histogram(filtered_df, hist_col), use_container_width=True)
        
        st.plotly_chart(chart_heatmap(filtered_df), use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            x_var = st.selectbox("X-Axis", 
                ["ai_adoption_rate", "faculty_training_hours", "infrastructure_readiness"],
                format_func=lambda x: x.replace('_', ' ').title())
        with col2:
            y_var = st.selectbox("Y-Axis",
                ["learning_outcome_delta", "student_ai_literacy_index", "student_satisfaction_score"],
                format_func=lambda x: x.replace('_', ' ').title())
        
        st.plotly_chart(chart_scatter(filtered_df, x_var, y_var), use_container_width=True)
        
        col3, col4 = st.columns(2)
        with col3:
            box_y = st.selectbox("Metric for Box Plot",
                ["ai_adoption_rate", "student_ai_literacy_index", "integrity_incident_rate"],
                format_func=lambda x: x.replace('_', ' ').title(),
                key="box_y")
        with col4:
            box_x = st.selectbox("Group By",
                ["policy_stance", "region", "institution_type"],
                format_func=lambda x: x.replace('_', ' ').title(),
                key="box_x")
        
        st.plotly_chart(chart_box(filtered_df, box_y, box_x), use_container_width=True)
    
    st.markdown("---")
    
    # Data Explorer
    st.markdown('<p class="section-header">📋 Data Explorer</p>', unsafe_allow_html=True)
    
    with st.expander("View Data Sample"):
        st.dataframe(filtered_df.head(100), use_container_width=True)
    
    # Download
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Filtered Data (CSV)",
        csv,
        "genai_education_data.csv",
        "text/csv"
    )
    
    # Footer
    st.markdown("---")
    st.caption("🎓 GenAI in Higher Education Dashboard | Synthetic Data for Research")


if __name__ == "__main__":
    main()
