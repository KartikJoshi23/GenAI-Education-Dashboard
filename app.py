"""
=============================================================================
GenAI in Higher Education - Interactive Dashboard
=============================================================================
A Streamlit dashboard exploring Generative AI adoption and policy
in higher education institutions worldwide.

Features:
- Dark/Light theme toggle
- Interactive filters
- 8 diverse chart types
- Data export functionality

Run: streamlit run app.py
=============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Import custom modules
from src.utils import (
    load_data, apply_filters, calculate_kpis, get_filter_options,
    format_number, get_download_filename, get_theme_colors,
    REGION_COLORS, POLICY_COLORS, INST_TYPE_COLORS
)
from src.charts import (
    create_adoption_trend_chart,
    create_regional_bar_chart,
    create_policy_donut_chart,
    create_histogram,
    create_correlation_heatmap,
    create_scatter_plot,
    create_grouped_bar_chart,
    create_box_plot
)

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="GenAI in Education Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# THEME MANAGEMENT
# =============================================================================

def init_theme():
    """Initialize theme in session state."""
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"


def toggle_theme():
    """Toggle between dark and light theme."""
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"


def get_current_theme():
    """Get current theme from session state."""
    return st.session_state.get("theme", "dark")


# =============================================================================
# DYNAMIC CSS STYLES
# =============================================================================

def apply_custom_css(theme: str):
    """Apply custom CSS based on current theme."""
    
    colors = get_theme_colors(theme)
    
    css = f"""
    <style>
        /* ===== ROOT VARIABLES ===== */
        :root {{
            --bg-primary: {colors["background"]};
            --bg-secondary: {colors["card_bg"]};
            --border-color: {colors["card_border"]};
            --text-primary: {colors["text_primary"]};
            --text-secondary: {colors["text_secondary"]};
            --accent-primary: {colors["primary"]};
            --accent-success: {colors["success"]};
            --accent-warning: {colors["warning"]};
            --accent-danger: {colors["danger"]};
        }}
        
        /* ===== MAIN CONTAINER ===== */
        .main .block-container {{
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }}
        
        /* ===== SIDEBAR ===== */
        [data-testid="stSidebar"] {{
            background-color: {colors["card_bg"]};
        }}
        
        [data-testid="stSidebar"] .stMarkdown {{
            color: {colors["text_primary"]};
        }}
        
        /* ===== HEADERS ===== */
        h1, h2, h3, h4, h5, h6 {{
            color: {colors["text_primary"]} !important;
        }}
        
        .main-header {{
            font-size: 2.2rem;
            font-weight: 700;
            color: {colors["text_primary"]};
            margin-bottom: 0.3rem;
        }}
        
        .sub-header {{
            font-size: 1.1rem;
            color: {colors["text_secondary"]};
            margin-bottom: 1.5rem;
        }}
        
        .section-header {{
            font-size: 1.25rem;
            font-weight: 600;
            color: {colors["text_primary"]};
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {colors["primary"]};
        }}
        
        /* ===== METRIC CARDS ===== */
        [data-testid="metric-container"] {{
            background: linear-gradient(135deg, {colors["card_bg"]} 0%, {colors["background"]} 100%);
            border: 1px solid {colors["card_border"]};
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        
        [data-testid="metric-container"] label {{
            color: {colors["text_secondary"]} !important;
        }}
        
        [data-testid="metric-container"] [data-testid="stMetricValue"] {{
            color: {colors["primary"]} !important;
            font-weight: 600;
        }}
        
        [data-testid="metric-container"] [data-testid="stMetricDelta"] {{
            font-size: 0.85rem;
        }}
        
        /* ===== TABS ===== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
            background-color: {colors["card_bg"]};
            border-radius: 10px;
            padding: 4px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: transparent;
            border-radius: 8px;
            padding: 10px 20px;
            color: {colors["text_secondary"]};
            font-weight: 500;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {colors["primary"]} !important;
            color: white !important;
        }}
        
        /* ===== EXPANDERS ===== */
        .streamlit-expanderHeader {{
            background-color: {colors["card_bg"]};
            border: 1px solid {colors["card_border"]};
            border-radius: 8px;
            color: {colors["text_primary"]};
        }}
        
        .streamlit-expanderContent {{
            background-color: {colors["card_bg"]};
            border: 1px solid {colors["card_border"]};
            border-top: none;
            border-radius: 0 0 8px 8px;
        }}
        
        /* ===== SELECTBOX & MULTISELECT ===== */
        .stSelectbox, .stMultiSelect {{
            color: {colors["text_primary"]};
        }}
        
        /* ===== DATAFRAME ===== */
        .stDataFrame {{
            border: 1px solid {colors["card_border"]};
            border-radius: 8px;
        }}
        
        /* ===== BUTTONS ===== */
        .stButton > button {{
            background-color: {colors["primary"]};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .stButton > button:hover {{
            background-color: {colors["secondary"]};
            transform: translateY(-1px);
        }}
        
        .stDownloadButton > button {{
            background-color: {colors["success"]};
            color: white;
            border: none;
            border-radius: 8px;
        }}
        
        .stDownloadButton > button:hover {{
            background-color: #059669;
        }}
        
        /* ===== INFO/WARNING BOXES ===== */
        .stAlert {{
            border-radius: 8px;
        }}
        
        /* ===== THEME TOGGLE BUTTON ===== */
        .theme-toggle {{
            position: fixed;
            top: 0.8rem;
            right: 1rem;
            z-index: 999;
        }}
        
        /* ===== FOOTER ===== */
        .footer {{
            text-align: center;
            color: {colors["text_muted"]};
            font-size: 0.85rem;
            margin-top: 2rem;
            padding: 1rem;
            border-top: 1px solid {colors["card_border"]};
        }}
        
        /* ===== HIDE STREAMLIT ELEMENTS ===== */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* ===== PLOTLY CHART CONTAINER ===== */
        .js-plotly-plot {{
            border-radius: 12px;
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


# =============================================================================
# SIDEBAR
# =============================================================================

def render_sidebar(df: pd.DataFrame) -> dict:
    """Render sidebar with theme toggle and filters."""
    
    theme = get_current_theme()
    colors = get_theme_colors(theme)
    
    # Theme toggle at top of sidebar
    st.sidebar.markdown("### ⚙️ Settings")
    
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        st.write(f"Theme: **{'🌙 Dark' if theme == 'dark' else '☀️ Light'}**")
    with col2:
        if st.button("🔄", help="Toggle theme"):
            toggle_theme()
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Dashboard title
    st.sidebar.markdown("## 🎓 GenAI in Education")
    st.sidebar.markdown("*Global Adoption Dashboard*")
    
    st.sidebar.markdown("---")
    
    # Filters
    st.sidebar.markdown("### 🔍 Filters")
    
    filter_options = get_filter_options(df)
    
    # Time Period
    st.sidebar.markdown("##### 📅 Time Period")
    selected_quarters = st.sidebar.multiselect(
        "Quarters",
        options=filter_options["survey_quarter"],
        default=filter_options["survey_quarter"],
        help="Select survey quarters"
    )
    
    # Geographic
    st.sidebar.markdown("##### 🌍 Geography")
    selected_regions = st.sidebar.multiselect(
        "Regions",
        options=filter_options["region"],
        default=[],
        help="Leave empty for all regions"
    )
    
    # Filter countries based on selected regions
    if selected_regions:
        available_countries = df[df["region"].isin(selected_regions)]["country"].unique().tolist()
    else:
        available_countries = filter_options["country"]
    
    selected_countries = st.sidebar.multiselect(
        "Countries",
        options=sorted(available_countries),
        default=[],
        help="Leave empty for all countries"
    )
    
    # Institution Characteristics
    st.sidebar.markdown("##### 🏛️ Institution")
    selected_inst_types = st.sidebar.multiselect(
        "Institution Type",
        options=filter_options["institution_type"],
        default=[],
        help="Filter by institution type"
    )
    
    selected_sizes = st.sidebar.multiselect(
        "Size",
        options=filter_options["institution_size"],
        default=[],
        help="Filter by enrollment size"
    )
    
    selected_funding = st.sidebar.multiselect(
        "Funding Type",
        options=filter_options["funding_type"],
        default=[]
    )
    
    # Policy & Academic
    st.sidebar.markdown("##### 📋 Policy")
    selected_policies = st.sidebar.multiselect(
        "Policy Stance",
        options=filter_options["policy_stance"],
        default=[],
        help="Filter by AI policy approach"
    )
    
    selected_disciplines = st.sidebar.multiselect(
        "Discipline Focus",
        options=filter_options["primary_discipline_focus"],
        default=[]
    )
    
    st.sidebar.markdown("---")
    
    # Dataset info
    st.sidebar.markdown("### 📊 Dataset")
    st.sidebar.caption(f"**Records**: {len(df):,}")
    st.sidebar.caption(f"**Countries**: {df['country'].nunique()}")
    st.sidebar.caption(f"**Period**: 2023-Q1 to 2024-Q4")
    st.sidebar.caption("**Type**: Synthetic")
    
    return {
        "quarters": selected_quarters,
        "regions": selected_regions,
        "countries": selected_countries,
        "institution_types": selected_inst_types,
        "sizes": selected_sizes,
        "funding_types": selected_funding,
        "policy_stances": selected_policies,
        "disciplines": selected_disciplines
    }


# =============================================================================
# KPI SECTION
# =============================================================================

def render_kpi_section(df: pd.DataFrame):
    """Render KPI metrics cards."""
    
    kpis = calculate_kpis(df)
    
    st.markdown('<p class="section-header">📈 Key Performance Indicators</p>', unsafe_allow_html=True)
    
    # Row 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Institutions",
            value=format_number(kpis["total_institutions"]["value"], "int"),
            help="Unique institutions in filtered data"
        )
    
    with col2:
        delta = kpis["avg_adoption_rate"]["delta"]
        st.metric(
            label="Avg Adoption Rate",
            value=f"{kpis['avg_adoption_rate']['value']:.1f}%",
            delta=f"{delta:+.1f}% YoY" if delta else None,
            help="Average % of courses with AI integration"
        )
    
    with col3:
        delta = kpis["avg_literacy_index"]["delta"]
        st.metric(
            label="Avg AI Literacy",
            value=f"{kpis['avg_literacy_index']['value']:.1f}",
            delta=f"{delta:+.1f} YoY" if delta else None,
            help="Student AI literacy index (0-100)"
        )
    
    with col4:
        delta = kpis["avg_incident_rate"]["delta"]
        st.metric(
            label="Avg Integrity Incidents",
            value=f"{kpis['avg_incident_rate']['value']:.1f}",
            delta=f"{delta:+.1f} YoY" if delta else None,
            delta_color="inverse",
            help="AI-related incidents per 1K students"
        )
    
    # Row 2
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            label="Countries",
            value=format_number(kpis["total_countries"]["value"], "int"),
            help="Countries represented"
        )
    
    with col6:
        st.metric(
            label="Avg Learning Δ",
            value=f"{kpis['avg_outcome_delta']['value']:+.1f}%",
            help="Average assessment score change"
        )
    
    with col7:
        st.metric(
            label="Avg Satisfaction",
            value=f"{kpis['avg_satisfaction']['value']:.2f}/5",
            help="Student satisfaction (Likert 1-5)"
        )
    
    with col8:
        st.metric(
            label="Integrated Policy %",
            value=f"{kpis['integrated_policy_pct']['value']:.1f}%",
            help="% with 'Integrated' policy stance"
        )


# =============================================================================
# CHART TABS
# =============================================================================

def render_overview_tab(df: pd.DataFrame, theme: str):
    """Render Overview tab with 4 charts."""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Chart 1: Line Chart - Adoption Trends
        fig = create_adoption_trend_chart(df, group_by="region", theme=theme)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Chart 2: Horizontal Bar - Regional Comparison
        fig = create_regional_bar_chart(df, metric="ai_adoption_rate", theme=theme)
        st.plotly_chart(fig, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Chart 3: Donut - Policy Distribution
        fig = create_policy_donut_chart(df, theme=theme)
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        # Chart 4: Grouped Bar - Institution Type
        fig = create_grouped_bar_chart(df, metric="ai_adoption_rate", 
                                       group_by="institution_type", theme=theme)
        st.plotly_chart(fig, use_container_width=True)


def render_analysis_tab(df: pd.DataFrame, theme: str):
    """Render Analysis tab with 4 charts."""
    
    # Chart 5: Histogram
    st.markdown("#### 📊 Distribution Analysis")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        hist_metric = st.selectbox(
            "Select Metric",
            options=["ai_adoption_rate", "student_ai_literacy_index", 
                     "integrity_incident_rate", "learning_outcome_delta",
                     "faculty_training_hours", "student_satisfaction_score"],
            format_func=lambda x: x.replace("_", " ").title(),
            key="hist_metric"
        )
        hist_color = st.selectbox(
            "Color By",
            options=["None", "region", "policy_stance", "institution_type"],
            format_func=lambda x: x.replace("_", " ").title(),
            key="hist_color"
        )
    
    with col2:
        color_by = hist_color if hist_color != "None" else None
        fig = create_histogram(df, hist_metric, color_by=color_by, theme=theme)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Chart 6: Correlation Heatmap
    st.markdown("#### 🔗 Correlation Analysis")
    
    corr_cols = [
        "ai_adoption_rate", "student_ai_literacy_index", "integrity_incident_rate",
        "learning_outcome_delta", "faculty_training_hours", "infrastructure_readiness",
        "policy_maturity_score", "student_satisfaction_score"
    ]
    
    fig = create_correlation_heatmap(df, corr_cols, theme=theme)
    st.plotly_chart(fig, use_container_width=True)


def render_relationships_tab(df: pd.DataFrame, theme: str):
    """Render Relationships tab with scatter and box plots."""
    
    # Chart 7: Scatter Plot
    st.markdown("#### 📈 Relationship Explorer")
    
    col1, col2, col3 = st.columns(3)
    
    scatter_options = [
        "ai_adoption_rate", "student_ai_literacy_index", "integrity_incident_rate",
        "learning_outcome_delta", "faculty_training_hours", "infrastructure_readiness",
        "policy_maturity_score", "student_satisfaction_score", "research_output_ai_pct"
    ]
    
    with col1:
        x_var = st.selectbox(
            "X-Axis",
            options=scatter_options,
            format_func=lambda x: x.replace("_", " ").title(),
            index=0,
            key="scatter_x"
        )
    
    with col2:
        y_var = st.selectbox(
            "Y-Axis",
            options=scatter_options,
            format_func=lambda x: x.replace("_", " ").title(),
            index=3,
            key="scatter_y"
        )
    
    with col3:
        color_var = st.selectbox(
            "Color By",
            options=["None", "region", "policy_stance", "institution_type"],
            format_func=lambda x: x.replace("_", " ").title() if x != "None" else "None",
            key="scatter_color"
        )
    
    color_col = color_var if color_var != "None" else None
    show_trendline = color_col is None
    
    fig = create_scatter_plot(df, x_var, y_var, color_col=color_col, 
                              theme=theme, trendline=show_trendline)
    st.plotly_chart(fig, use_container_width=True)
    
    # Display correlation coefficient
    if color_col is None:
        corr_val = df[[x_var, y_var]].corr().iloc[0, 1]
        st.info(f"📊 **Pearson Correlation**: r = {corr_val:.3f}")
    
    st.markdown("---")
    
    # Chart 8: Box Plot
    st.markdown("#### 📦 Distribution by Category")
    
    col4, col5 = st.columns(2)
    
    with col4:
        box_y = st.selectbox(
            "Metric",
            options=scatter_options,
            format_func=lambda x: x.replace("_", " ").title(),
            index=0,
            key="box_y"
        )
    
    with col5:
        box_x = st.selectbox(
            "Group By",
            options=["policy_stance", "region", "institution_type", "funding_type"],
            format_func=lambda x: x.replace("_", " ").title(),
            key="box_x"
        )
    
    fig = create_box_plot(df, box_y, box_x, theme=theme)
    st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# METHODOLOGY SECTION
# =============================================================================

def render_methodology_section(theme: str):
    """Render methodology and assumptions."""
    
    st.markdown('<p class="section-header">📖 Methodology & Assumptions</p>', unsafe_allow_html=True)
    
    with st.expander("🔬 Data Generation Methodology", expanded=False):
        st.markdown("""
        ### Synthetic Dataset Overview
        
        This dashboard uses a **synthetic dataset** generated for research demonstration.
        The data simulates a global survey of higher education institutions regarding
        their Generative AI adoption and policies.
        
        #### Generation Parameters
        - **Random Seed**: 42 (fixed for reproducibility)
        - **Total Records**: 5,000 institutions
        - **Time Period**: 8 quarters (2023-Q1 to 2024-Q4)
        - **Geographic Coverage**: 45+ countries across 6 regions
        - **Exclusions**: Pakistan (per project requirements)
        
        #### Key Assumptions
        1. **Regional Variation**: North America and Europe have higher baseline adoption
        2. **Temporal Trends**: All metrics show quarterly improvement
        3. **Policy Effects**: "Integrated" policies correlate with better outcomes
        4. **Institution Type**: Research universities lead in adoption
        """)
    
    with st.expander("📊 Metric Definitions", expanded=False):
        st.markdown("""
        | Metric | Range | Description |
        |--------|-------|-------------|
        | AI Adoption Rate | 0-82% | % of courses with AI integration |
        | Student AI Literacy | 0-100 | Composite assessment score |
        | Integrity Incident Rate | 0-48 | Cases per 1,000 students |
        | Learning Outcome Delta | -18% to +38% | Assessment score change |
        | Policy Maturity Score | 1-5 | Governance completeness |
        | Infrastructure Readiness | 1-10 | Technical capability |
        | Faculty Training Hours | 0-115 | Avg PD hours per faculty |
        | Student Satisfaction | 1-5 | Likert satisfaction rating |
        """)
    
    with st.expander("⚠️ Limitations", expanded=False):
        st.markdown("""
        ### Important Caveats
        
        1. **Synthetic Data**: All data is artificially generated
        2. **No Real-World Conclusions**: Do not use for actual policy decisions
        3. **Simplified Assumptions**: Real relationships are more complex
        4. **Cross-Sectional Limits**: Cannot establish causation
        
        ### Appropriate Uses
        ✅ Dashboard design demonstration  
        ✅ Statistical method exploration  
        ✅ Academic project submission  
        ❌ Policy recommendations  
        ❌ Investment decisions  
        """)


# =============================================================================
# DATA TABLE & DOWNLOAD
# =============================================================================

def render_data_section(df: pd.DataFrame, theme: str):
    """Render data explorer and download section."""
    
    st.markdown('<p class="section-header">📋 Data Explorer</p>', unsafe_allow_html=True)
    
    # Column selector
    all_cols = df.columns.tolist()
    default_cols = [
        "institution_name", "country", "region", "institution_type",
        "ai_adoption_rate", "policy_stance", "student_ai_literacy_index",
        "learning_outcome_delta", "student_satisfaction_score"
    ]
    
    selected_cols = st.multiselect(
        "Select columns to display:",
        options=all_cols,
        default=[c for c in default_cols if c in all_cols]
    )
    
    if selected_cols:
        st.dataframe(
            df[selected_cols].head(100),
            use_container_width=True,
            hide_index=True
        )
    
    # Download buttons
    st.markdown("#### 💾 Download Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv_full = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Full Dataset (CSV)",
            data=csv_full,
            file_name=get_download_filename("genai_education_full"),
            mime="text/csv"
        )
    
    with col2:
        if selected_cols:
            csv_selected = df[selected_cols].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Selected Columns",
                data=csv_selected,
                file_name=get_download_filename("genai_education_selected"),
                mime="text/csv"
            )
    
    with col3:
        summary = df.describe().round(2)
        csv_summary = summary.to_csv().encode('utf-8')
        st.download_button(
            label="📥 Summary Stats",
            data=csv_summary,
            file_name=get_download_filename("genai_education_summary"),
            mime="text/csv"
        )


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    
    # Initialize theme
    init_theme()
    theme = get_current_theme()
    
    # Apply custom CSS
    apply_custom_css(theme)
    
    # Header
    st.markdown(f"""
        <h1 class="main-header">🎓 Generative AI in Higher Education</h1>
        <p class="sub-header">Global Adoption & Policy Dashboard | 
        Exploring how universities worldwide are adopting and governing AI tools</p>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_data("data/dataset.csv")
    
    if df.empty:
        st.error("❌ Could not load dataset. Please ensure 'data/dataset.csv' exists.")
        st.info("💡 Run the data generator script first to create the dataset.")
        st.stop()
    
    # Sidebar filters
    filters = render_sidebar(df)
    
    # Apply filters
    filtered_df = apply_filters(
        df,
        regions=filters["regions"],
        countries=filters["countries"],
        institution_types=filters["institution_types"],
        funding_types=filters["funding_types"],
        policy_stances=filters["policy_stances"],
        quarters=filters["quarters"],
        disciplines=filters["disciplines"],
        sizes=filters["sizes"]
    )
    
    # Check if data remains after filtering
    if filtered_df.empty:
        st.warning("⚠️ No data matches current filters. Please adjust your selection.")
        st.stop()
    
    # Show filter summary
    st.info(f"📊 Displaying **{len(filtered_df):,}** records from **{filtered_df['country'].nunique()}** countries")
    
    # KPI Section
    render_kpi_section(filtered_df)
    
    st.markdown("---")
    
    # Chart Tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 Overview",
        "🔍 Analysis", 
        "📈 Relationships"
    ])
    
    with tab1:
        render_overview_tab(filtered_df, theme)
    
    with tab2:
        render_analysis_tab(filtered_df, theme)
    
    with tab3:
        render_relationships_tab(filtered_df, theme)
    
    st.markdown("---")
    
    # Methodology
    render_methodology_section(theme)
    
    st.markdown("---")
    
    # Data Explorer
    render_data_section(filtered_df, theme)
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p>📊 GenAI in Higher Education Dashboard | 🔬 Synthetic Data for Research Demonstration</p>
            <p>Built with Streamlit & Plotly | Data: 5,000 simulated institutions across 45+ countries</p>
        </div>
    """, unsafe_allow_html=True)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
