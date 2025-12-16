"""
Visualization Components
========================
Plotly-based chart functions with theme support.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional

from src.utils import (
    get_theme_colors, REGION_COLORS, POLICY_COLORS, INST_TYPE_COLORS
)


def get_layout_defaults(theme: str = "dark") -> Dict:
    """Get common layout settings for the specified theme."""
    colors = get_theme_colors(theme)
    
    return {
        "paper_bgcolor": colors["paper_bg"],
        "plot_bgcolor": colors["plot_bg"],
        "font": {
            "color": colors["text_primary"],
            "family": "system-ui, -apple-system, sans-serif",
            "size": 12
        },
        "margin": {"l": 50, "r": 30, "t": 50, "b": 50},
        "hoverlabel": {
            "bgcolor": colors["card_bg"],
            "font_size": 12,
            "font_color": colors["text_primary"],
            "bordercolor": colors["card_border"]
        },
        "legend": {
            "bgcolor": "rgba(0,0,0,0)",
            "font": {"color": colors["text_primary"]}
        }
    }


# =============================================================================
# CHART 1: LINE CHART - Adoption Trends Over Time
# =============================================================================

def create_adoption_trend_chart(
    df: pd.DataFrame,
    group_by: str = "region",
    theme: str = "dark"
) -> go.Figure:
    """
    Create a multi-line trend chart showing adoption rates over quarters.
    """
    colors = get_theme_colors(theme)
    
    # Aggregate data
    trend_data = df.groupby(["survey_quarter", group_by]).agg({
        "ai_adoption_rate": "mean"
    }).reset_index()
    
    # Sort quarters chronologically
    quarter_order = sorted(trend_data["survey_quarter"].unique())
    
    # Select color map
    if group_by == "region":
        color_map = REGION_COLORS
    elif group_by == "policy_stance":
        color_map = POLICY_COLORS
    elif group_by == "institution_type":
        color_map = INST_TYPE_COLORS
    else:
        color_map = None
    
    fig = px.line(
        trend_data,
        x="survey_quarter",
        y="ai_adoption_rate",
        color=group_by,
        markers=True,
        color_discrete_map=color_map,
        category_orders={"survey_quarter": quarter_order}
    )
    
    fig.update_traces(
        line={"width": 2.5},
        marker={"size": 8}
    )
    
    fig.update_layout(
        **get_layout_defaults(theme),
        title={
            "text": f"AI Adoption Trends by {group_by.replace('_', ' ').title()}",
            "font": {"size": 16, "color": colors["text_primary"]}
        },
        height=400,
        xaxis={
            "title": "Quarter",
            "gridcolor": colors["grid"],
            "tickangle": -45,
            "linecolor": colors["grid"]
        },
        yaxis={
            "title": "Average Adoption Rate (%)",
            "gridcolor": colors["grid"],
            "zeroline": False,
            "linecolor": colors["grid"]
        },
        legend_title=group_by.replace("_", " ").title()
    )
    
    return fig


# =============================================================================
# CHART 2: HORIZONTAL BAR CHART - Regional Comparison
# =============================================================================

def create_regional_bar_chart(
    df: pd.DataFrame,
    metric: str = "ai_adoption_rate",
    theme: str = "dark"
) -> go.Figure:
    """
    Create a horizontal bar chart comparing regions on a selected metric.
    """
    colors = get_theme_colors(theme)
    
    # Aggregate by region
    regional = df.groupby("region").agg({
        metric: ["mean", "std", "count"]
    }).reset_index()
    regional.columns = ["Region", "Mean", "Std", "Count"]
    regional = regional.sort_values("Mean", ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=regional["Region"],
        x=regional["Mean"],
        orientation="h",
        marker={
            "color": [REGION_COLORS.get(r, colors["primary"]) for r in regional["Region"]],
            "line": {"width": 0}
        },
        error_x={
            "type": "data",
            "array": regional["Std"] / np.sqrt(regional["Count"]),
            "color": colors["text_muted"],
            "thickness": 1.5
        },
        text=regional["Mean"].round(1),
        textposition="outside",
        textfont={"color": colors["text_primary"], "size": 11},
        hovertemplate="<b>%{y}</b><br>" +
                      f"{metric.replace('_', ' ').title()}: " + "%{x:.1f}<br>" +
                      "Institutions: %{customdata}<extra></extra>",
        customdata=regional["Count"]
    ))
    
    fig.update_layout(
        **get_layout_defaults(theme),
        title={
            "text": f"Regional Comparison: {metric.replace('_', ' ').title()}",
            "font": {"size": 16, "color": colors["text_primary"]}
        },
        height=380,
        xaxis={
            "title": metric.replace("_", " ").title(),
            "gridcolor": colors["grid"],
            "linecolor": colors["grid"]
        },
        yaxis={
            "title": "",
            "gridcolor": colors["grid"],
            "linecolor": colors["grid"]
        }
    )
    
    return fig


# =============================================================================
# CHART 3: DONUT/PIE CHART - Policy Distribution
# =============================================================================

def create_policy_donut_chart(
    df: pd.DataFrame,
    theme: str = "dark"
) -> go.Figure:
    """
    Create a donut chart showing policy stance distribution.
    """
    colors = get_theme_colors(theme)
    
    policy_counts = df["policy_stance"].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=policy_counts.index,
        values=policy_counts.values,
        hole=0.55,
        marker={
            "colors": [POLICY_COLORS.get(p, colors["primary"]) for p in policy_counts.index],
            "line": {"color": colors["background"], "width": 2}
        },
        textinfo="percent+label",
        textposition="outside",
        textfont={"color": colors["text_primary"], "size": 11},
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>%{percent}<extra></extra>",
        pull=[0.02, 0.02, 0.02, 0.02]
    )])
    
    fig.update_layout(
        **get_layout_defaults(theme),
        title={
            "text": "Policy Stance Distribution",
            "font": {"size": 16, "color": colors["text_primary"]}
        },
        height=400,
        showlegend=True,
        legend={
            "orientation": "h",
            "y": -0.1,
            "x": 0.5,
            "xanchor": "center",
            "font": {"color": colors["text_primary"]}
        },
        annotations=[{
            "text": f"<b>{len(df):,}</b><br>Institutions",
            "x": 0.5, "y": 0.5,
            "font": {"size": 14, "color": colors["text_primary"]},
            "showarrow": False
        }]
    )
    
    return fig


# =============================================================================
# CHART 4: HISTOGRAM - Distribution Analysis
# =============================================================================

def create_histogram(
    df: pd.DataFrame,
    column: str,
    color_by: Optional[str] = None,
    theme: str = "dark",
    nbins: int = 30
) -> go.Figure:
    """
    Create a histogram with optional grouping.
    """
    colors = get_theme_colors(theme)
    
    if color_by:
        if color_by == "region":
            color_map = REGION_COLORS
        elif color_by == "policy_stance":
            color_map = POLICY_COLORS
        elif color_by == "institution_type":
            color_map = INST_TYPE_COLORS
        else:
            color_map = None
        
        fig = px.histogram(
            df,
            x=column,
            color=color_by,
            nbins=nbins,
            color_discrete_map=color_map,
            opacity=0.75,
            barmode="overlay"
        )
    else:
        fig = px.histogram(
            df,
            x=column,
            nbins=nbins,
            color_discrete_sequence=[colors["primary"]]
        )
    
    fig.update_layout(
        **get_layout_defaults(theme),
        title={
            "text": f"Distribution: {column.replace('_', ' ').title()}",
            "font": {"size": 16, "color": colors["text_primary"]}
        },
        height=380,
        xaxis={
            "title": column.replace("_", " ").title(),
            "gridcolor": colors["grid"],
            "linecolor": colors["grid"]
        },
        yaxis={
            "title": "Frequency",
            "gridcolor": colors["grid"],
            "linecolor": colors["grid"]
        },
        bargap=0.05
    )
    
    return fig


# =============================================================================
# CHART 5: HEATMAP - Correlation Matrix
# =============================================================================

def create_correlation_heatmap(
    df: pd.DataFrame,
    columns: List[str],
    theme: str = "dark"
) -> go.Figure:
    """
    Create a correlation matrix heatmap.
    """
    colors = get_theme_colors(theme)
    
    # Calculate correlation matrix
    corr = df[columns].corr()
    
    # Create labels
    labels = [c.replace("_", " ").title()[:18] + "..." if len(c) > 18 
              else c.replace("_", " ").title() for c in columns]
    
    # Define colorscale based on theme
    if theme == "dark":
        colorscale = [
            [0, "#ef4444"],
            [0.5, "#1e293b"],
            [1, "#10b981"]
        ]
    else:
        colorscale = [
            [0, "#dc2626"],
            [0.5, "#f8fafc"],
            [1, "#059669"]
        ]
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=labels,
        y=labels,
        colorscale=colorscale,
        zmid=0,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        textfont={"size": 10, "color": colors["text_primary"]},
        hoverongaps=False,
        hovertemplate="<b>%{x}</b> vs <b>%{y}</b><br>Correlation: %{z:.3f}<extra></extra>",
        colorbar={
            "title": "r",
            "tickfont": {"color": colors["text_primary"]},
            "titlefont": {"color": colors["text_primary"]}
        }
    ))
    
    fig.update_layout(
        **get_layout_defaults(theme),
        title={
            "text": "Metric Correlations",
            "font": {"size": 16, "color": colors["text_primary"]}
        },
        height=480,
        xaxis={
            "tickangle": -45,
            "side": "bottom",
            "tickfont": {"size": 10}
        },
        yaxis={
            "autorange": "reversed",
            "tickfont": {"size": 10}
        }
    )
    
    return fig


# =============================================================================
# CHART 6: SCATTER PLOT - Relationship Analysis
# =============================================================================

def create_scatter_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: Optional[str] = None,
    theme: str = "dark",
    trendline: bool = True
) -> go.Figure:
    """
    Create a scatter plot showing relationship between two variables.
    """
    colors = get_theme_colors(theme)
    
    # Sample if dataset is large
    plot_df = df.sample(n=min(1500, len(df)), random_state=42) if len(df) > 1500 else df.copy()
    
    # Determine color mapping
    if color_col:
        if color_col == "region":
            color_map = REGION_COLORS
        elif color_col == "policy_stance":
            color_map = POLICY_COLORS
        elif color_col == "institution_type":
            color_map = INST_TYPE_COLORS
        else:
            color_map = None
    else:
        color_map = None
    
    fig = px.scatter(
        plot_df,
        x=x_col,
        y=y_col,
        color=color_col,
        color_discrete_map=color_map,
        trendline="ols" if trendline and color_col is None else None,
        opacity=0.6,
        hover_data=["institution_name", "country"]
    )
    
    fig.update_traces(marker={"size": 7, "line": {"width": 0}})
    
    # Style trendline
    if trendline and color_col is None:
        fig.update_traces(
            line={"color": colors["danger"], "width": 2},
            selector=dict(mode="lines")
        )
    
    fig.update_layout(
        **get_layout_defaults(theme),
        title={
            "text": f"{x_col.replace('_', ' ').title()} vs {y_col.replace('_', ' ').title()}",
            "font": {"size": 16, "color": colors["text_primary"]}
        },
        height=420,
        xaxis={
            "title": x_col.replace("_", " ").title(),
            "gridcolor": colors["grid"],
            "linecolor": colors["grid"]
        },
        yaxis={
            "title": y_col.replace("_", " ").title(),
            "gridcolor": colors["grid"],
            "linecolor": colors["grid"]
        }
    )
    
    return fig


# =============================================================================
# CHART 7: GROUPED BAR CHART - Institution Type Breakdown
# =============================================================================

def create_grouped_bar_chart(
    df: pd.DataFrame,
    metric: str = "ai_adoption_rate",
    group_by: str = "institution_type",
    theme: str = "dark"
) -> go.Figure:
    """
    Create a vertical bar chart with metric breakdown by category.
    """
    colors = get_theme_colors(theme)
    
    # Aggregate
    breakdown = df.groupby(group_by).agg({
        metric: "mean",
        "institution_id": "count"
    }).reset_index()
    breakdown.columns = [group_by, "Value", "Count"]
    breakdown = breakdown.sort_values("Value", ascending=False)
    
    # Select color scheme
    if group_by == "institution_type":
        bar_colors = [INST_TYPE_COLORS.get(t, colors["primary"]) for t in breakdown[group_by]]
    elif group_by == "policy_stance":
        bar_colors = [POLICY_COLORS.get(t, colors["primary"]) for t in breakdown[group_by]]
    elif group_by == "region":
        bar_colors = [REGION_COLORS.get(t, colors["primary"]) for t in breakdown[group_by]]
    else:
        bar_colors = colors["primary"]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=breakdown[group_by],
        y=breakdown["Value"],
        marker={"color": bar_colors, "line": {"width": 0}},
        text=breakdown["Value"].round(1),
        textposition="outside",
        textfont={"color": colors["text_primary"], "size": 11},
        hovertemplate="<b>%{x}</b><br>" +
                      f"{metric.replace('_', ' ').title()}: " + "%{y:.1f}<br>" +
                      "n = %{customdata:,}<extra></extra>",
        customdata=breakdown["Count"]
    ))
    
    fig.update_layout(
        **get_layout_defaults(theme),
        title={
            "text": f"{metric.replace('_', ' ').title()} by {group_by.replace('_', ' ').title()}",
            "font": {"size": 16, "color": colors["text_primary"]}
        },
        height=400,
        xaxis={
            "title": "",
            "tickangle": -30,
            "gridcolor": colors["grid"],
            "linecolor": colors["grid"]
        },
        yaxis={
            "title": metric.replace("_", " ").title(),
            "gridcolor": colors["grid"],
            "linecolor": colors["grid"]
        }
    )
    
    return fig


# =============================================================================
# CHART 8: BOX PLOT - Distribution by Category
# =============================================================================

def create_box_plot(
    df: pd.DataFrame,
    y_col: str,
    x_col: str,
    theme: str = "dark"
) -> go.Figure:
    """
    Create a box plot showing distribution across categories.
    """
    colors = get_theme_colors(theme)
    
    # Select color scheme
    if x_col == "region":
        color_map = REGION_COLORS
    elif x_col == "policy_stance":
        color_map = POLICY_COLORS
    elif x_col == "institution_type":
        color_map = INST_TYPE_COLORS
    else:
        color_map = None
    
    fig = px.box(
        df,
        x=x_col,
        y=y_col,
        color=x_col,
        color_discrete_map=color_map,
        notched=True
    )
    
    fig.update_traces(
        marker={"outliercolor": colors["text_muted"], "size": 4},
        line={"width": 1.5}
    )
    
    fig.update_layout(
        **get_layout_defaults(theme),
        title={
            "text": f"{y_col.replace('_', ' ').title()} by {x_col.replace('_', ' ').title()}",
            "font": {"size": 16, "color": colors["text_primary"]}
        },
        height=420,
        showlegend=False,
        xaxis={
            "title": "",
            "tickangle": -30,
            "gridcolor": colors["grid"],
            "linecolor": colors["grid"]
        },
        yaxis={
            "title": y_col.replace("_", " ").title(),
            "gridcolor": colors["grid"],
            "linecolor": colors["grid"]
        }
    )
    
    return fig
