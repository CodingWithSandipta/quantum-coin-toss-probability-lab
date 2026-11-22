"""
components/ui_components.py - Reusable Streamlit UI Widgets & Layout Components
Provides custom cards, banners, metric widgets, and callouts following
the modern Dark Navy / Deep Purple scientific laboratory theme.
"""

import streamlit as st
from typing import Optional


def render_header(title: str, subtitle: str, badge: Optional[str] = None):
    """Renders a modern glowing laboratory header."""
    badge_html = f'<span class="lab-badge">{badge}</span>' if badge else ""
    st.markdown(
        f"""
        <div class="lab-header-container">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h1 class="lab-title">{title}</h1>
                    <p class="lab-subtitle">{subtitle}</p>
                </div>
                {badge_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label: str, value: str, subvalue: str = "", delta_color: str = "#06b6d4"):
    """Renders a stylish quantum metric card."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subvalue" style="color: {delta_color};">{subvalue}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_concept_card(title: str, description: str, icon: str = "⚛️", link: Optional[str] = None):
    """Renders a clickable educational concept card."""
    link_html = f'<div style="margin-top: 10px;"><a href="{link}" class="card-link">Explore Module →</a></div>' if link else ""
    st.markdown(
        f"""
        <div class="concept-card">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">{icon}</div>
            <h3 style="color: #f8fafc; margin-top: 0; font-size: 1.25rem;">{title}</h3>
            <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.5;">{description}</p>
            {link_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dirac_formula(equation: str, label: str = "Quantum State"):
    """Displays a formatted Dirac notation formula in a styled container."""
    st.markdown(
        f"""
        <div class="formula-container">
            <span class="formula-label">{label}:</span>
            <span class="formula-text">{equation}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_banner(text: str, alert_type: str = "info"):
    """Displays a styled alert banner (info, tip, warning, success)."""
    icons = {
        "info": "ℹ️",
        "tip": "💡",
        "warning": "⚠️",
        "success": "✅",
    }
    icon = icons.get(alert_type, "ℹ️")
    st.markdown(
        f"""
        <div class="alert-box alert-{alert_type}">
            <span style="font-size: 1.2rem; margin-right: 10px;">{icon}</span>
            <div>{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
