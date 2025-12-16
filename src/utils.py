"""
Utility Functions
=================
Helper functions for data loading, filtering, and calculations.
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Optional, Any


# =============================================================================
# COLOR SCHEMES FOR THEMES
# =============================================================================

THEME_COLORS = {
    "dark": {
        "background": "#0f172a",
        "card_bg": "#1e293b",
        "card_border": "#334155",
        "text_primary": "#e2e8f0",
        "text_secondary": "#94a3b8",
        "text_muted": "#64748b",
        "primary": "#6366f1",
        "secondary": "#8b5cf6",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "info": "#3b82f6",
        "grid": "#334155",
        "plot_bg": "rgba(0,0,0,0)",
        "paper_bg": "rgba(0,0,0,0)",
    },
    "light": {
        "background": "#ffffff",
        "card_bg": "#f8fafc",
        "card_border": "#e2e8f0",
        "text_primary": "#1e293b",
        "text_secondary": "#475569",
        "text_muted": "#94a3b8",
        "primary": "#4f46e5",
        "secondary": "#7c3aed",
        "success": "#059669",
        "warning": "#d97706",
        "danger": "#dc2626",
        "info": "#2563eb",
        "grid": "#e2e8f0",
        "plot_bg": "rgba(0,0,0,0)",
        "paper_bg": "rgba(0,0,0,0)",
    }
}

# Region colors (consistent across themes)
REGION_COLORS = {
    "North America": "#6366f1",
    "Europe": "#8b5cf6",
    "Asia Pacific": "#ec4899",
    "Latin America": "#10b981",
    "Middle East": "#f59e0b",
    "Africa": "#3b82f6"
}

# Policy stance colors
POLICY_COLORS = {
    "Restrictive": "#ef4444",
    "Cautious": "#f59e0b",
    "Permissive": "#3b82f6",
    "Integrated": "#10b981"
}

# Institution type colors
INST_TYPE_COLORS = {
    "Research University": "#6366f1",
    "Teaching University": "#8b5cf6",
    "Liberal Arts College": "#ec4899",
    "Technical Institute": "#10b981",
    "Community College": "#f59e0b"
}


def get_theme_colors(theme: str = "dark") -> Dict[str, str]:
    """Get color scheme for the specified theme."""
    return THEME_COLORS.get(theme, THEME_COLORS["dark"])


# =============================================================================
# DATA LOADING
# =============================================================================

@st.cache_data(ttl=3600)
def load_data(filepath: str = "data/dataset.csv") -> pd.DataFrame:
    """
    Load and cache the dataset.
    
    Parameters
    ----------
    filepath : str
        Path to the CSV file
        
    Returns
    -------
    pd.DataFrame
        Loaded dataset with proper dtypes
    """
    try:
        df = pd.read_csv(filepath)
        
        # Ensure proper dtypes for categorical columns
        categorical_cols = [
            "region", "country", "institution_type", "institution_size",
            "funding_type", "policy_stance", "primary_discipline_focus",
            "adoption_tier", "readiness_category"
        ]
        
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype("category")
        
        return df
    
    except FileNotFoundError:
        st.error(f"Dataset not found at {filepath}. Please ensure the data file exists.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()


# =============================================================================
# FILTERING
# =============================================================================

def get_filter_options(df: pd.DataFrame) -> Dict[str, List]:
    """Extract unique values for filter dropdowns."""
    
    return {
        "region": sorted(df["region"].dropna().unique().tolist()),
        "country": sorted(df["country"].dropna().unique().tolist()),
        "institution_type": sorted(df["institution_type"].dropna().unique().tolist()),
        "institution_size": ["Small (<5K)", "Medium (5K-15K)", "Large (15K-30K)", "Very Large (>30K)"],
        "funding_type": ["Public", "Private", "Mixed"],
        "policy_stance": ["Restrictive", "Cautious", "Permissive", "Integrated"],
        "primary_discipline_focus": sorted(df["primary_discipline_focus"].dropna().unique().tolist()),
        "survey_quarter": sorted(df["survey_quarter"].dropna().unique().tolist()),
        "year": sorted(df["year"].dropna().unique().tolist())
    }


def apply_filters(
    df: pd.DataFrame,
    regions: Optional[List[str]] = None,
    countries: Optional[List[str]] = None,
    institution_types: Optional[List[str]] = None,
    funding_types: Optional[List[str]] = None,
    policy_stances: Optional[List[str]] = None,
    quarters: Optional[List[str]] = None,
    disciplines: Optional[List[str]] = None,
    sizes: Optional[List[str]] = None
) -> pd.DataFrame:
    """Apply multiple filters to the dataset."""
    
    filtered = df.copy()
    
    if regions and len(regions) > 0:
        filtered = filtered[filtered["region"].isin(regions)]
    
    if countries and len(countries) > 0:
        filtered = filtered[filtered["country"].isin(countries)]
    
    if institution_types and len(institution_types) > 0:
        filtered = filtered[filtered["institution_type"].isin(institution_types)]
    
    if funding_types and len(funding_types) > 0:
        filtered = filtered[filtered["funding_type"].isin(funding_types)]
    
    if policy_stances and len(policy_stances) > 0:
        filtered = filtered[filtered["policy_stance"].isin(policy_stances)]
    
    if quarters and len(quarters) > 0:
        filtered = filtered[filtered["survey_quarter"].isin(quarters)]
    
    if disciplines and len(disciplines) > 0:
        filtered = filtered[filtered["primary_discipline_focus"].isin(disciplines)]
    
    if sizes and len(sizes) > 0:
        filtered = filtered[filtered["institution_size"].isin(sizes)]
    
    return filtered


# =============================================================================
# KPI CALCULATIONS
# =============================================================================

def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate key performance indicators from the dataset."""
    
    if df.empty:
        return {key: {"value": 0, "delta": None} for key in [
            "total_institutions", "avg_adoption_rate", "avg_literacy_index",
            "avg_incident_rate", "avg_outcome_delta", "avg_satisfaction",
            "integrated_policy_pct", "high_adoption_pct"
        ]}
    
    # Calculate year-over-year changes
    has_2023 = 2023 in df["year"].values
    has_2024 = 2024 in df["year"].values
    
    adoption_delta = literacy_delta = incident_delta = None
    
    if has_2023 and has_2024:
        df_2023 = df[df["year"] == 2023]
        df_2024 = df[df["year"] == 2024]
        
        if len(df_2023) > 0 and len(df_2024) > 0:
            adoption_delta = df_2024["ai_adoption_rate"].mean() - df_2023["ai_adoption_rate"].mean()
            literacy_delta = df_2024["student_ai_literacy_index"].mean() - df_2023["student_ai_literacy_index"].mean()
            incident_delta = df_2024["integrity_incident_rate"].mean() - df_2023["integrity_incident_rate"].mean()
    
    return {
        "total_institutions": {
            "value": df["institution_id"].nunique(),
            "delta": None
        },
        "total_countries": {
            "value": df["country"].nunique(),
            "delta": None
        },
        "avg_adoption_rate": {
            "value": df["ai_adoption_rate"].mean(),
            "delta": adoption_delta
        },
        "avg_literacy_index": {
            "value": df["student_ai_literacy_index"].mean(),
            "delta": literacy_delta
        },
        "avg_incident_rate": {
            "value": df["integrity_incident_rate"].mean(),
            "delta": incident_delta
        },
        "avg_outcome_delta": {
            "value": df["learning_outcome_delta"].mean(),
            "delta": None
        },
        "avg_satisfaction": {
            "value": df["student_satisfaction_score"].mean(),
            "delta": None
        },
        "avg_training_hours": {
            "value": df["faculty_training_hours"].mean(),
            "delta": None
        },
        "integrated_policy_pct": {
            "value": (df["policy_stance"] == "Integrated").mean() * 100,
            "delta": None
        },
        "high_adoption_pct": {
            "value": (df["ai_adoption_rate"] >= 45).mean() * 100,
            "delta": None
        },
        "avg_policy_maturity": {
            "value": df["policy_maturity_score"].mean(),
            "delta": None
        },
        "avg_infrastructure": {
            "value": df["infrastructure_readiness"].mean(),
            "delta": None
        }
    }


# =============================================================================
# FORMATTING HELPERS
# =============================================================================

def format_number(value: float, format_type: str = "float", precision: int = 1) -> str:
    """Format a number for display."""
    
    if pd.isna(value):
        return "N/A"
    
    if format_type == "int":
        return f"{int(value):,}"
    elif format_type == "pct":
        return f"{value:.{precision}f}%"
    elif format_type == "currency":
        if value >= 1_000_000:
            return f"${value/1_000_000:.1f}M"
        elif value >= 1_000:
            return f"${value/1_000:.1f}K"
        return f"${value:.0f}"
    return f"{value:.{precision}f}"


def get_download_filename(prefix: str = "genai_education_data") -> str:
    """Generate a timestamped filename for downloads."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.csv"
