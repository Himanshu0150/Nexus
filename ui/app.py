import streamlit as st
import urllib.request
import urllib.parse
import json
import os

# --- 1. Page Configuration & Nexus Precision Design Tokens ---
st.set_page_config(
    page_title="NEXUS ELECTRONICS — High-Performance Precision Hardware",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://localhost:8000"

# Inject Global Nexus Precision CSS (Pure CSS Variables, Typography & High-Contrast Overrides)
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">

<style>
:root {
    --nexus-bg: #FAFAF9;
    --nexus-card: #FFFFFF;
    --nexus-surface-secondary: #F3F4F6;
    --nexus-text-primary: #171717;
    --nexus-text-secondary: #52525B;
    --nexus-border: #E4E4E7;
    --nexus-border-hover: #D4D4D8;
    --nexus-brand-blue: #2563EB;
    --nexus-blue-hover: #1D4ED8;
    --nexus-blue-light: #EFF6FF;
    --nexus-blue-border: #BFDBFE;
    --nexus-success: #15803D;
    --nexus-success-bg: #F0FDF4;
    --nexus-warning: #B45309;
    --nexus-warning-bg: #FFFBEB;
    --nexus-warning-border: #FDE68A;
    --nexus-error: #B91C1C;
    --nexus-error-bg: #FEF2F2;
    --nexus-error-border: #FECACA;

    /* Semantic Aliases & Compatibility Tokens */
    --nexus-canvas: var(--nexus-card);
    --nexus-surface-low: var(--nexus-surface-secondary);
    --nexus-surface-high: var(--nexus-border);
    --nexus-ink: var(--nexus-text-primary);
    --nexus-secondary: var(--nexus-text-secondary);
    --nexus-cobalt: var(--nexus-brand-blue);
    --nexus-cobalt-hover: var(--nexus-blue-hover);
    --nexus-cobalt-light: var(--nexus-blue-light);
    --nexus-charcoal: var(--nexus-text-primary);
    --nexus-charcoal-hover: #000000;
}

/* Universal Typography & Surfaces */
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    color: var(--nexus-text-primary) !important;
    background-color: var(--nexus-bg) !important;
}

/* Headings */
h1, h2, h3, h4, h5, h6, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: var(--nexus-text-primary) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}

/* Markdown paragraphs & text (scoped to non-button containers) */
div[data-testid="stMarkdownContainer"] > p,
div[data-testid="stMarkdownContainer"] > span {
    color: var(--nexus-text-primary);
}

/* Top Announcement Bar */
.nexus-announcement {
    background: var(--nexus-surface-secondary);
    border: 1px solid var(--nexus-border);
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 11px;
    font-weight: 500;
    color: var(--nexus-text-secondary) !important;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
    letter-spacing: 0.02em;
}
.nexus-announcement strong {
    color: var(--nexus-text-primary) !important;
    font-weight: 700;
}
.nexus-announcement .badge-dot {
    width: 6px;
    height: 6px;
    background: var(--nexus-brand-blue);
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
}

/* Architectural Hero Section */
.nexus-hero {
    background: var(--nexus-surface-secondary);
    border: 1px solid var(--nexus-border);
    border-radius: 8px;
    padding: 32px 36px;
    margin-bottom: 24px;
    position: relative;
}
.nexus-hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #ffffff;
    border: 1px solid var(--nexus-border);
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--nexus-text-primary) !important;
    margin-bottom: 12px;
}
.nexus-hero h1 {
    font-size: 36px !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
    margin: 0 0 10px 0;
    color: var(--nexus-text-primary) !important;
    line-height: 1.15;
}
.nexus-hero p {
    font-size: 14px !important;
    color: var(--nexus-text-secondary) !important;
    max-width: 680px;
    line-height: 1.6;
    margin: 0 0 20px 0;
}
.nexus-spec-ticker {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    border-top: 1px solid var(--nexus-border);
    padding-top: 16px;
    margin-top: 16px;
}
.nexus-spec-item {
    font-size: 12px;
    color: var(--nexus-text-secondary);
}
.nexus-spec-item strong {
    color: var(--nexus-text-primary);
    font-weight: 700;
    display: block;
    font-size: 14px;
}

/* Category Discipline Cards */
.discipline-card {
    background: #ffffff;
    border: 1px solid var(--nexus-border);
    border-radius: 6px;
    padding: 16px;
    text-align: center;
    transition: all 0.15s ease;
    cursor: pointer;
    margin-bottom: 8px;
}
.discipline-card:hover {
    border-color: var(--nexus-brand-blue);
    transform: translateY(-1px);
    box-shadow: 0 2px 6px rgba(37, 99, 235, 0.08);
}
.discipline-icon {
    font-size: 26px;
    margin-bottom: 6px;
    display: block;
}
.discipline-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--nexus-text-primary);
    line-height: 1.2;
}
.discipline-sub {
    font-size: 11px;
    color: var(--nexus-text-secondary);
    margin-top: 2px;
}

/* Product Cards */
.nexus-card {
    background: #ffffff;
    border: 1px solid var(--nexus-border);
    border-radius: 6px;
    padding: 14px;
    margin-bottom: 16px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.nexus-card:hover {
    border-color: var(--nexus-border-hover);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}
.card-img-wrap {
    background: var(--nexus-surface-secondary);
    border-radius: 4px;
    padding: 8px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Badges */
.badge-tag {
    background: var(--nexus-surface-secondary);
    color: var(--nexus-text-primary);
    border: 1px solid var(--nexus-border);
    font-size: 10px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    display: inline-block;
}
.badge-stock-in {
    background: var(--nexus-success-bg);
    color: var(--nexus-success);
    border: 1px solid #BBF7D0;
    font-size: 10px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
.badge-stock-low {
    background: var(--nexus-warning-bg);
    color: var(--nexus-warning);
    border: 1px solid var(--nexus-warning-border);
    font-size: 10px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
.badge-stock-out {
    background: var(--nexus-error-bg);
    color: var(--nexus-error);
    border: 1px solid var(--nexus-error-border);
    font-size: 10px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

/* ==============================================================================
   BUTTON DESIGN SYSTEM (Primary, Secondary, Active Sidebar, Disabled)
   ============================================================================== */
.stButton > button,
button[kind="primary"],
button[kind="secondary"],
button[data-testid="baseButton-primary"],
button[data-testid="baseButton-secondary"],
.stFormSubmitButton > button {
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    min-height: 40px !important;
    padding: 8px 16px !important;
    letter-spacing: 0.01em !important;
    transition: all 0.15s ease-in-out !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    line-height: 1.4 !important;
    cursor: pointer !important;
}

/* Primary actions: Brand Blue Background with Crisp White Text */
button[kind="primary"],
button[data-testid="baseButton-primary"],
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"],
.stFormSubmitButton > button[kind="primary"],
.stFormSubmitButton > button[data-testid="baseButton-primary"] {
    background-color: var(--nexus-brand-blue) !important;
    color: #ffffff !important;
    border: 1px solid var(--nexus-brand-blue) !important;
    box-shadow: 0 1px 2px rgba(37, 99, 235, 0.12) !important;
}

button[kind="primary"] *,
button[data-testid="baseButton-primary"] *,
.stButton > button[kind="primary"] *,
.stButton > button[data-testid="baseButton-primary"] *,
.stFormSubmitButton > button[kind="primary"] *,
.stFormSubmitButton > button[data-testid="baseButton-primary"] * {
    color: #ffffff !important;
    font-weight: 600 !important;
}

button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover,
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[data-testid="baseButton-primary"]:hover {
    background-color: var(--nexus-blue-hover) !important;
    border-color: var(--nexus-blue-hover) !important;
    color: #ffffff !important;
    box-shadow: 0 2px 4px rgba(29, 78, 216, 0.2) !important;
}

button[kind="primary"]:hover *,
button[data-testid="baseButton-primary"]:hover *,
.stButton > button[kind="primary"]:hover *,
.stButton > button[data-testid="baseButton-primary"]:hover *,
.stFormSubmitButton > button[kind="primary"]:hover *,
.stFormSubmitButton > button[data-testid="baseButton-primary"]:hover * {
    color: #ffffff !important;
}

button[kind="primary"]:active,
button[data-testid="baseButton-primary"]:active {
    background-color: #1E40AF !important;
    border-color: #1E40AF !important;
}

/* Secondary actions: White background, dark text, subtle border */
button[kind="secondary"],
button[data-testid="baseButton-secondary"],
.stButton > button[kind="secondary"],
.stButton > button[data-testid="baseButton-secondary"],
.stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]),
.stFormSubmitButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]) {
    background-color: #ffffff !important;
    color: var(--nexus-text-primary) !important;
    border: 1px solid var(--nexus-border) !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
}

button[kind="secondary"] *,
button[data-testid="baseButton-secondary"] *,
.stButton > button[kind="secondary"] *,
.stButton > button[data-testid="baseButton-secondary"] *,
.stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]) *,
.stFormSubmitButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]) * {
    color: var(--nexus-text-primary) !important;
    font-weight: 600 !important;
}

button[kind="secondary"]:hover,
button[data-testid="baseButton-secondary"]:hover,
.stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]):hover,
.stFormSubmitButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]):hover {
    background-color: var(--nexus-surface-secondary) !important;
    border-color: var(--nexus-border-hover) !important;
    color: var(--nexus-text-primary) !important;
}

button[kind="secondary"]:hover *,
button[data-testid="baseButton-secondary"]:hover *,
.stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]):hover *,
.stFormSubmitButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]):hover * {
    color: var(--nexus-text-primary) !important;
}

/* Disabled controls */
button:disabled,
button[disabled],
.stButton > button:disabled,
.stButton > button[disabled] {
    background-color: var(--nexus-surface-secondary) !important;
    border: 1px solid var(--nexus-border) !important;
    color: var(--nexus-text-secondary) !important;
    opacity: 0.65 !important;
    cursor: not-allowed !important;
    box-shadow: none !important;
}

button:disabled *,
button[disabled] *,
.stButton > button:disabled *,
.stButton > button[disabled] * {
    color: var(--nexus-text-secondary) !important;
}

/* ==============================================================================
   SIDEBAR STYLING & ACTIVE NAVIGATION HIGHLIGHTS
   ============================================================================== */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid var(--nexus-border) !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
    background-color: #ffffff !important;
}

/* Sidebar navigation buttons (Inactive) */
section[data-testid="stSidebar"] .stButton > button[kind="secondary"],
section[data-testid="stSidebar"] .stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]) {
    background-color: #ffffff !important;
    color: var(--nexus-text-primary) !important;
    border: 1px solid var(--nexus-border) !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-weight: 500 !important;
    padding-left: 12px !important;
}

section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover,
section[data-testid="stSidebar"] .stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]):hover {
    background-color: var(--nexus-surface-secondary) !important;
    border-color: var(--nexus-border-hover) !important;
    color: var(--nexus-text-primary) !important;
}

/* Sidebar active navigation item: light-blue surface with blue accent border */
section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] {
    background-color: var(--nexus-blue-light) !important;
    color: var(--nexus-brand-blue) !important;
    border: 1px solid var(--nexus-blue-border) !important;
    border-left: 3px solid var(--nexus-brand-blue) !important;
    font-weight: 700 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding-left: 11px !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] .stButton > button[kind="primary"] *,
section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] * {
    color: var(--nexus-brand-blue) !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover,
section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"]:hover {
    background-color: #DBEAFE !important;
    border-color: var(--nexus-brand-blue) !important;
    border-left: 3px solid var(--nexus-blue-hover) !important;
    color: var(--nexus-blue-hover) !important;
}

section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover *,
section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"]:hover * {
    color: var(--nexus-blue-hover) !important;
}

/* Sidebar 1-Click Demo Login button override (should remain bold brand-blue) */
div:has(.sidebar-login-marker) + div .stButton > button,
div:has(.sidebar-login-marker) + div button[kind="primary"] {
    background-color: var(--nexus-brand-blue) !important;
    color: #ffffff !important;
    border: 1px solid var(--nexus-brand-blue) !important;
    text-align: center !important;
    justify-content: center !important;
    box-shadow: 0 1px 2px rgba(37, 99, 235, 0.15) !important;
}
div:has(.sidebar-login-marker) + div .stButton > button *,
div:has(.sidebar-login-marker) + div button[kind="primary"] * {
    color: #ffffff !important;
    font-weight: 600 !important;
}
div:has(.sidebar-login-marker) + div .stButton > button:hover,
div:has(.sidebar-login-marker) + div button[kind="primary"]:hover {
    background-color: var(--nexus-blue-hover) !important;
    border-color: var(--nexus-blue-hover) !important;
}
div:has(.sidebar-login-marker) + div .stButton > button:hover *,
div:has(.sidebar-login-marker) + div button[kind="primary"]:hover * {
    color: #ffffff !important;
}

/* ==============================================================================
   FORM CONTROLS, SELECTBOXES & INPUTS
   ============================================================================== */
div[data-baseweb="select"] {
    border-radius: 6px !important;
}
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1px solid var(--nexus-border) !important;
    border-radius: 6px !important;
    color: var(--nexus-text-primary) !important;
    min-height: 40px !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: var(--nexus-border-hover) !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--nexus-brand-blue) !important;
    box-shadow: 0 0 0 1px var(--nexus-brand-blue) !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: var(--nexus-text-primary) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
div[data-baseweb="select"] svg {
    fill: var(--nexus-text-secondary) !important;
    color: var(--nexus-text-secondary) !important;
    opacity: 0.9 !important;
}

/* Dropdown popover options */
ul[data-baseweb="menu"] {
    background-color: #ffffff !important;
    border: 1px solid var(--nexus-border) !important;
    border-radius: 6px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
    padding: 4px !important;
}
li[data-baseweb="menu-item"] {
    color: var(--nexus-text-primary) !important;
    font-size: 13px !important;
    border-radius: 4px !important;
    padding: 8px 12px !important;
}
li[data-baseweb="menu-item"]:hover,
li[data-baseweb="menu-item"][aria-selected="true"] {
    background-color: var(--nexus-blue-light) !important;
    color: var(--nexus-brand-blue) !important;
}
li[data-baseweb="menu-item"] * {
    color: inherit !important;
}

/* BaseWeb Text & Number Inputs */
div[data-baseweb="input"] {
    background-color: #ffffff !important;
    border: 1px solid var(--nexus-border) !important;
    border-radius: 6px !important;
    min-height: 40px !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}
div[data-baseweb="input"]:hover {
    border-color: var(--nexus-border-hover) !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: var(--nexus-brand-blue) !important;
    box-shadow: 0 0 0 1px var(--nexus-brand-blue) !important;
}
div[data-baseweb="input"] input {
    color: var(--nexus-text-primary) !important;
    font-size: 13px !important;
    background-color: transparent !important;
    font-family: inherit !important;
    padding: 8px 12px !important;
}
div[data-baseweb="input"] input::placeholder {
    color: #9CA3AF !important;
}

/* Number input step buttons */
div[data-testid="stNumberInput"] button {
    border-color: var(--nexus-border) !important;
    background-color: #ffffff !important;
    color: var(--nexus-text-primary) !important;
}
div[data-testid="stNumberInput"] button:hover {
    background-color: var(--nexus-surface-secondary) !important;
    border-color: var(--nexus-border-hover) !important;
}

/* Radio buttons & Checkboxes */
div[data-testid="stRadio"] label,
div[data-testid="stCheckbox"] label {
    color: var(--nexus-text-primary) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* Expanders */
div[data-testid="stExpander"] {
    background-color: #ffffff !important;
    border: 1px solid var(--nexus-border) !important;
    border-radius: 6px !important;
}
div[data-testid="stExpander"] summary {
    color: var(--nexus-text-primary) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}
div[data-testid="stExpander"] summary:hover {
    color: var(--nexus-brand-blue) !important;
}

/* Progress bar banner */
.shipping-progress-banner {
    background: var(--nexus-surface-secondary);
    border: 1px solid var(--nexus-border);
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}
.progress-bar-track {
    width: 100%;
    height: 6px;
    background: var(--nexus-border);
    border-radius: 9999px;
    overflow: hidden;
    margin-top: 6px;
}
.progress-bar-thumb {
    height: 100%;
    background: var(--nexus-brand-blue);
    border-radius: 9999px;
    transition: width 0.4s ease;
}

/* Trust cards */
.trust-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
    margin: 28px 0;
}
.trust-card {
    background: #ffffff;
    border: 1px solid var(--nexus-border);
    border-radius: 6px;
    padding: 20px;
}
.trust-card strong {
    font-size: 14px;
    color: var(--nexus-text-primary);
    display: block;
    margin-bottom: 6px;
}
.trust-card p {
    font-size: 12px;
    color: var(--nexus-text-secondary);
    line-height: 1.5;
    margin: 0;
}

/* Manifesto Dark Callout */
.manifesto-banner {
    background: #18181B;
    border: 1px solid #27272A;
    border-radius: 6px;
    padding: 32px 36px;
    color: #ffffff !important;
    margin: 36px 0 20px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 20px;
}
.manifesto-banner h3 {
    color: #ffffff !important;
    font-size: 22px !important;
    margin: 0 0 6px 0;
}
.manifesto-banner p {
    color: #A1A1AA !important;
    font-size: 13px !important;
    max-width: 650px;
    line-height: 1.5;
    margin: 0;
}

/* Badges & Tags */
.badge-tag {
    background: var(--nexus-surface-secondary);
    color: var(--nexus-text-secondary);
    border: 1px solid var(--nexus-border);
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 2px 8px;
    border-radius: 4px;
}
.badge-stock-in {
    background: #F0FDF4;
    color: var(--nexus-success);
    border: 1px solid #DCFCE7;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 4px;
}
.badge-stock-low {
    background: #FFFBEB;
    color: var(--nexus-warning);
    border: 1px solid #FEF3C7;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 4px;
}
.badge-rating {
    background: #FFFBEB;
    color: var(--nexus-warning);
    border: 1px solid #FEF3C7;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    gap: 3px;
}
.badge-rating-zero {
    background: var(--nexus-surface-secondary);
    color: var(--nexus-text-secondary);
    border: 1px solid var(--nexus-border);
    font-size: 11px;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)


# --- 2. API Helper Functions ---
def fetch_json(endpoint):
    try:
        with urllib.request.urlopen(f"{API_URL}{endpoint}", timeout=8) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None

def post_json(endpoint, data):
    req = urllib.request.Request(
        f"{API_URL}{endpoint}",
        data=json.dumps(data).encode(),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode()), None
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode())
            return None, err.get('detail', str(e))
        except Exception:
            return None, str(e)
    except Exception as e:
        return None, str(e)

def delete_req(endpoint):
    req = urllib.request.Request(f"{API_URL}{endpoint}", method='DELETE')
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            return json.loads(response.read().decode()), None
    except Exception as e:
        return None, str(e)

def put_json(endpoint, data=None):
    data_bytes = json.dumps(data).encode() if data else b""
    req = urllib.request.Request(
        f"{API_URL}{endpoint}",
        data=data_bytes,
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            return json.loads(response.read().decode()), None
    except Exception as e:
        return None, str(e)


# --- 3. Session State Management ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}  # {product_id: qty}
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = "All"
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None
if 'checkout_step' not in st.session_state:
    st.session_state.checkout_step = 1
if 'selected_address_id' not in st.session_state:
    st.session_state.selected_address_id = None
if 'selected_payment_method' not in st.session_state:
    st.session_state.selected_payment_method = "Credit Card (Nexus Pay)"

# Current logged-in user state (defaults to Demo User ID 1)
if 'user' not in st.session_state:
    demo = fetch_json("/users/1")
    if demo:
        st.session_state.user = demo
    else:
        st.session_state.user = {"id": 1, "name": "Demo User", "email": "demo@nexus.com"}

def set_page(page_name):
    st.session_state.page = page_name
    if page_name != "Cart":
        st.session_state.checkout_step = 1

LOW_STOCK_THRESHOLD = 5

def get_product_stock(prod):
    """Safely extracts the stock quantity from a product object supporting standard aliases."""
    if not isinstance(prod, dict):
        return 0
    for key in ('stock', 'stockQuantity', 'quantity', 'inventory', 'stock_quantity'):
        if key in prod and prod[key] is not None:
            try:
                return int(prod[key])
            except (ValueError, TypeError):
                pass
    return 0

def render_stock_badge(stock, detailed=False):
    """Renders consistent stock availability badges matching the NEXUS design system."""
    if stock <= 0:
        label = "❌ Sold Out (0 units)" if detailed else "❌ Sold Out"
        return f"<span class='badge-stock-out'>{label}</span>"
    elif stock <= LOW_STOCK_THRESHOLD:
        label = f"⚠️ Low Stock ({stock} units left)" if detailed else f"⚠️ Low Stock ({stock})"
        return f"<span class='badge-stock-low'>{label}</span>"
    else:
        label = f"● In Stock ({stock} units ready for dispatch)" if detailed else f"● In Stock ({stock})"
        return f"<span class='badge-stock-in'>{label}</span>"

def add_to_cart_action(pid, qty=1):
    prod = fetch_json(f"/products/{pid}")
    if not prod:
        st.error("Product not found.")
        return
    max_stock = get_product_stock(prod)
    if max_stock <= 0:
        st.error(f"Cannot add to cart. '{prod['name']}' is currently sold out!")
        return
    current_qty = st.session_state.cart.get(pid, 0)
    if current_qty + qty > max_stock:
        st.error(f"Cannot add {qty} more. Only {max_stock} units in stock ({current_qty} already in bag)!")
    else:
        st.session_state.cart[pid] = current_qty + qty
        st.toast(f"🛒 Added {prod['name']} (Qty: {qty}) to cart!", icon="✅")


# --- 4. Sidebar Controls (Customer Profile & Navigation) ---
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 14px;">
        <span style="font-size: 18px; font-weight: 800; letter-spacing: -0.02em; color: #171717;">NEXUS</span>
        <span style="font-size: 10px; font-weight: 700; color: #2563EB; letter-spacing: 0.12em;">PRECISION</span>
    </div>
    """, unsafe_allow_html=True)

    # Active User Profile Box
    user = st.session_state.user
    if user:
        st.markdown(f"""
        <div style="background: #F3F4F6; border: 1px solid #E4E4E7; border-left: 3px solid #2563EB; border-radius: 6px; padding: 12px; margin-bottom: 10px;">
            <div style="font-size: 10px; font-weight: 700; color: #52525B; text-transform: uppercase; letter-spacing: 0.05em;">Authorized Profile</div>
            <div style="font-size: 13px; font-weight: 700; color: #171717; margin-top: 2px;">👤 {user['name']}</div>
            <div style="font-size: 11px; color: #52525B; margin-top: 2px;">{user['email']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 Sign Out", key="sidebar_signout", use_container_width=True):
            st.session_state.user = None
            st.session_state.cart = {}
            st.session_state.selected_address_id = None
            st.toast("Signed out successfully.")
            st.rerun()
    else:
        st.markdown("""
        <div style="background: #F3F4F6; border: 1px solid #E4E4E7; border-left: 3px solid #B45309; border-radius: 6px; padding: 12px; margin-bottom: 10px;">
            <div style="font-size: 10px; font-weight: 700; color: #B45309; text-transform: uppercase; letter-spacing: 0.05em;">Guest Session</div>
            <div style="font-size: 13px; font-weight: 600; color: #171717; margin-top: 2px;">Guest Customer</div>
            <div style="font-size: 11px; color: #52525B; margin-top: 2px;">Sign in for ACID checkout & saved addresses.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<span class="sidebar-login-marker" style="display:none;"></span>', unsafe_allow_html=True)
        if st.button("⚡ 1-Click Demo Login", key="sidebar_demo_login", use_container_width=True, type="primary"):
            res, err = post_json("/auth/login", {"email": "demo@nexus.com", "password": "demo123"})
            if res and "user" in res:
                st.session_state.user = res["user"]
                st.session_state.selected_address_id = None
                st.toast("⚡ Signed in as Demo User!", icon="✅")
                st.rerun()

    # Primary Navigation
    nav_items = [
        ("Home", "🏛️ Brand Storefront"),
        ("Catalog", "💻 Hardware Catalog"),
        ("Cart", f"🛒 Cart & Checkout ({sum(st.session_state.cart.values())})"),
        ("Profile", "👤 Saved Addresses"),
        ("Orders", "📦 Order History"),
        ("Auth", "🔑 Customer Sign In"),
        ("Databases", "📊 Database Telemetry")
    ]
    
    for p_id, label in nav_items:
        is_active = (st.session_state.page == p_id)
        btn_type = "primary" if is_active else "secondary"
        if st.button(label, key=f"nav_{p_id}", use_container_width=True, type=btn_type):
            set_page(p_id)
            st.rerun()

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E4E4E7;'/>", unsafe_allow_html=True)

    # Live Catalog Facets ($facet Aggregation)
    facets = fetch_json("/products/facets") or {}
    cat_facet_map = {item['_id']: item['count'] for item in facets.get('categories', [])}
    price_buckets = facets.get('price_buckets', [])
    total_facet_items = sum(cat_facet_map.values()) or 100

    st.markdown("""
    <div style="font-size: 10px; font-weight: 700; text-transform: uppercase; color: #52525B; letter-spacing: 0.05em; margin-bottom: 8px;">
        Disciplines ($facet)
    </div>
    """, unsafe_allow_html=True)

    # All Disciplines filter
    is_all_cat = (st.session_state.selected_category == "All")
    btn_all_type = "primary" if is_all_cat and st.session_state.page == "Catalog" else "secondary"
    if st.button(f"🌐 All Disciplines ({total_facet_items})", key="side_cat_all", use_container_width=True, type=btn_all_type):
        st.session_state.selected_category = "All"
        set_page("Catalog")
        st.rerun()

    # Category quick filters
    cat_defs = [
        ("laptops", "💻 Laptops"),
        ("phones", "📱 Smartphones"),
        ("shoes", "👟 Audio & Gear"),
        ("books", "📚 Tech Literature")
    ]
    for c_slug, c_title in cat_defs:
        c_count = cat_facet_map.get(c_slug, 0)
        is_c_sel = (st.session_state.selected_category == c_slug)
        b_type = "primary" if is_c_sel and st.session_state.page == "Catalog" else "secondary"
        if st.button(f"{c_title} ({c_count})", key=f"side_cat_{c_slug}", use_container_width=True, type=b_type):
            st.session_state.selected_category = c_slug
            set_page("Catalog")
            st.rerun()

    if price_buckets:
        st.markdown("""
        <div style="font-size: 10px; font-weight: 700; text-transform: uppercase; color: #52525B; letter-spacing: 0.05em; margin: 12px 0 8px 0;">
            Price Distribution ($bucket)
        </div>
        """, unsafe_allow_html=True)
        for pb in price_buckets:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 4px 10px; background: #FFFFFF; border: 1px solid #E4E4E7; border-radius: 4px; margin-bottom: 4px; font-size: 11px;">
                <span style="color: #171717; font-weight: 500;">🏷️ {pb['label']}</span>
                <span style="font-weight: 700; color: #15803D; background: #F0FDF4; border: 1px solid #DCFCE7; padding: 1px 6px; border-radius: 9999px;">{pb['count']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E4E4E7;'/>", unsafe_allow_html=True)
    
    # Live Telemetry Monitor
    st.markdown("""
    <div style="font-size: 10px; font-weight: 700; text-transform: uppercase; color: #52525B; letter-spacing: 0.04em; margin-bottom: 8px;">
        Database Architecture
    </div>
    <div style="display: flex; flex-direction: column; gap: 6px; font-size: 11px; color: #171717;">
        <div>🐘 <strong>PostgreSQL</strong>: <span style="color: #15803D; font-weight: 600;">ACID Locks Active</span></div>
        <div>🍃 <strong>MongoDB</strong>: <span style="color: #15803D; font-weight: 600;">100 Products & SVGs</span></div>
        <div>🔮 <strong>ChromaDB</strong>: <span style="color: #15803D; font-weight: 600;">384-dim MiniLM Vectors</span></div>
    </div>
    """, unsafe_allow_html=True)


# --- 5. Global Top Bar & Announcement ---
st.markdown("""
<div class="nexus-announcement">
    <div style="display: flex; align-items: center;">
        <span class="badge-dot"></span>
        <strong>SPRING HARDWARE RELEASE 2025</strong>
        <span style="color: #D4D4D8; margin: 0 8px;">/</span>
        <span>Complimentary expedited courier dispatch on all orders over $150</span>
    </div>
    <div style="display: none; font-size: 11px; color: #52525B;">
        Direct Technical Support • Enterprise Procurement
    </div>
</div>
""", unsafe_allow_html=True)

# Top Header Bar
col_logo, col_action = st.columns([3, 1])
with col_logo:
    st.markdown("""
    <div style="display: flex; align-items: baseline; gap: 8px;">
        <span style="font-size: 20px; font-weight: 800; letter-spacing: -0.03em; color: #171717;">NEXUS</span>
        <span style="font-size: 11px; font-weight: 700; color: #2563EB; letter-spacing: 0.12em; text-transform: uppercase;">ELECTRONICS</span>
    </div>
    """, unsafe_allow_html=True)

with col_action:
    cart_count = sum(st.session_state.cart.values())
    if st.button(f"🛒 Shopping Bag ({cart_count})", key="top_quick_cart", use_container_width=True):
        set_page("Cart")
        st.rerun()


# ==============================================================================
# VIEW 1: BRAND HOMEPAGE (Art-Directed Storefront)
# ==============================================================================
if st.session_state.page == "Home":
    # Hero Section with Ticker and Showcase
    hero_col_text, hero_col_visual = st.columns([6, 6], gap="large")
    with hero_col_text:
        st.markdown("""
        <div class="nexus-hero" style="height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div class="nexus-hero-pill">
                <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #2563EB;"></span>
                Nexus Hardware Release 2025
            </div>
            <h1>Technology for everyday life.</h1>
            <p>
                Engineered for seamless productivity, immersive sound, and all-day endurance.
                Discover precision computing instruments, high-performance electronics, and curated tech.
            </p>
            <div class="nexus-spec-ticker">
                <div class="nexus-spec-item"><strong>0.8 mm</strong> Anodized Tolerance</div>
                <div class="nexus-spec-item"><strong>100% CNC</strong> Aerospace Aluminum</div>
                <div class="nexus-spec-item"><strong>Zero Bloat</strong> Hardware BIOS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with hero_col_visual:
        # Use locally cached hero image with fallback
        local_hero = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "images", "hero_trinity.webp")
        if os.path.exists(local_hero):
            st.image(local_hero, use_column_width=True)
        else:
            st.image(f"{API_URL}/products/P0001/image", use_column_width=True)
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 4px; padding: 6px 12px; margin-top: 6px; display: inline-flex; align-items: center; gap: 6px; font-size: 11px; font-weight: 600; color: #171717;">
            <span style="color: #2563EB;">✓</span> TRINITY FLAGSHIP SUITE — CALIBRATED 2025
        </div>
        """, unsafe_allow_html=True)

    # 1-Click Action Buttons
    c_btn1, c_btn2, _ = st.columns([2, 2, 4])
    with c_btn1:
        if st.button("Explore Products →", type="primary", use_container_width=True, key="hp_explore_btn"):
            set_page("Catalog")
            st.rerun()
    with c_btn2:
        if st.button("Browse Laptops", use_container_width=True, key="hp_laptops_btn"):
            st.session_state.selected_category = "laptops"
            set_page("Catalog")
            st.rerun()

    # Product Classification Grid (6 Hardware Disciplines)
    st.markdown("<h3 style='margin: 32px 0 12px 0; font-size: 18px;'>Product Classification</h3>", unsafe_allow_html=True)
    d_cols = st.columns(6)
    disciplines = [
        ("laptops", "💻", "Laptops", "Aerolite Series"),
        ("phones", "📱", "Smartphones", "Horizon Pro"),
        ("shoes", "🎧", "Audio & Gear", "Aura Studio"),
        ("books", "📚", "Technical", "Clean Systems"),
        ("All", "🖥️", "Displays", "5K Reference"),
        ("All", "⚡", "Power & Docks", "Thunderbolt 5")
    ]
    for idx, (cat_key, icon, title, sub) in enumerate(disciplines):
        with d_cols[idx]:
            st.markdown(f"""
            <div class="discipline-card">
                <span class="discipline-icon">{icon}</span>
                <div class="discipline-title">{title}</div>
                <div class="discipline-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"View {title}", key=f"disc_btn_{idx}", use_container_width=True):
                st.session_state.selected_category = cat_key
                set_page("Catalog")
                st.rerun()

    # Featured Products Section
    st.markdown("<h3 style='margin: 32px 0 4px 0; font-size: 18px;'>Featured Hardware</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 12px; color: #52525B; margin-bottom: 16px;'>Certified benchmarks of Nexus industrial engineering.</p>", unsafe_allow_html=True)
    
    featured = fetch_json("/products?limit=4") or []
    if featured:
        f_cols = st.columns(4)
        for idx, prod in enumerate(featured[:4]):
            with f_cols[idx]:
                avg_r = prod.get('avg_rating', 0.0)
                rev_count = prod.get('review_count', 0)
                if rev_count > 0 and avg_r > 0:
                    hp_rating = f"<span class='badge-rating'>★ {avg_r:.1f} <span style='font-weight:400; color:#52525B;'>({rev_count})</span></span>"
                else:
                    hp_rating = "<span class='badge-rating-zero'>★ Unrated</span>"
                hp_stock = get_product_stock(prod)
                hp_stock_badge = render_stock_badge(hp_stock)
                st.markdown(f"""
                <div class="nexus-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span class="badge-tag">{prod['category']}</span>
                        {hp_rating}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.image(f"{API_URL}/products/{prod['product_id']}/image", use_column_width=True)
                st.markdown(f"""
                <div style="margin: 6px 0 10px 0;">
                    <div style="font-size: 14px; font-weight: 700; color: #171717; line-height: 1.3; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{prod['name']}</div>
                    <div style="margin: 4px 0 6px 0;">{hp_stock_badge}</div>
                    <div style="font-size: 16px; font-weight: 800; color: #171717;">${prod['price']:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                
                b1, b2 = st.columns([1, 1])
                with b1:
                    if st.button("Details", key=f"hp_det_{prod['product_id']}", use_container_width=True):
                        st.session_state.selected_product = prod['product_id']
                        set_page("Product")
                        st.rerun()
                with b2:
                    if hp_stock > 0:
                        if st.button("+ Add", key=f"hp_add_{prod['product_id']}", use_container_width=True, type="primary"):
                            add_to_cart_action(prod['product_id'], 1)
                            st.rerun()
                    else:
                        st.button("Sold Out", key=f"hp_sold_{prod['product_id']}", disabled=True, use_container_width=True)

    # Engineering Trust Cards
    st.markdown("""
    <div class="trust-grid">
        <div class="trust-card">
            <strong>🚚 Free Express Dispatch</strong>
            <p>Guaranteed next-business-day shipping with carbon-neutral secure transit on all continental orders over $150.</p>
        </div>
        <div class="trust-card">
            <strong>⏱️ 30-Day Evaluation Period</strong>
            <p>Test Nexus instruments in your actual daily workflow. Complete, hassle-free returns with prepaid return shipping labels.</p>
        </div>
        <div class="trust-card">
            <strong>🛡️ 2-Year Official Nexus Warranty</strong>
            <p>Full comprehensive structural, battery, and electronic component coverage with rapid replacement guarantee.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Industrial Manifesto Banner
    st.markdown("""
    <div class="manifesto-banner">
        <div>
            <div style="font-size: 10px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #2563EB; margin-bottom: 4px;">BESPOKE DESIGN ETHOS</div>
            <h3>Built without compromise. Down to the single micron.</h3>
            <p>
                Every Nexus chassis is carved from a solid unibody ingot of aerospace-grade alloy.
                No unnecessary seams, zero rattling components, and purely silent thermal dissipation.
            </p>
        </div>
        <div>
            <span style="background: #ffffff; color: #171717; font-size: 12px; font-weight: 700; padding: 10px 18px; border-radius: 4px; display: inline-block;">
                Read The Manifesto →
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# VIEW 2: HARDWARE CATALOG & PRODUCT LISTING
# ==============================================================================
elif st.session_state.page == "Catalog":
    # Breadcrumbs & Technical Category Header
    st.markdown("""
    <nav style="font-size: 12px; color: #52525B; margin-bottom: 8px;">
        <span style="color: #52525B;">Catalog</span> / <span style="color: #52525B;">Hardware Architecture</span> / <strong style="color: #171717;">Systems & Instruments</strong>
    </nav>
    <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 6px; padding: 20px 24px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
        <div>
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                <span style="background: #F3F4F6; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; color: #171717; text-transform: uppercase;">SYS-SERIES: ARCH-04</span>
                <span style="font-size: 11px; color: #52525B;">100 Calibrated SKU Configurations</span>
            </div>
            <h2 style="font-size: 24px; margin: 0 0 4px 0;">Hardware Catalog & Workstations</h2>
            <p style="font-size: 13px; color: #52525B; margin: 0; max-width: 650px;">
                Engineered with uniform CNC unibody enclosures, micro-etched low-reflectance displays, and custom cooling for sustained compile, 3D rendering, and local LLM deployment.
            </p>
        </div>
        <div style="display: flex; gap: 18px; font-size: 11px; background: #F3F4F6; border: 1px solid #E4E4E7; padding: 10px 16px; border-radius: 4px;">
            <div><span style="color: #52525B; display: block; font-size: 10px; text-transform: uppercase;">TDP Envelope</span><strong style="color: #171717;">115W Sustained</strong></div>
            <div style="width: 1px; background: #E4E4E7;"></div>
            <div><span style="color: #52525B; display: block; font-size: 10px; text-transform: uppercase;">Acoustic Floor</span><strong style="color: #171717;">&lt; 38 dBA</strong></div>
            <div style="width: 1px; background: #E4E4E7;"></div>
            <div><span style="color: #52525B; display: block; font-size: 10px; text-transform: uppercase;">Color Accuracy</span><strong style="color: #171717;">ΔE &lt; 0.8</strong></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Search & Filter Controls Toolbar
    cat_col, search_col, rating_col, mode_col, sort_col = st.columns([1.2, 1.8, 1.1, 1.1, 1.0])
    
    with cat_col:
        # Dynamic category counts from MongoDB $facet aggregation
        cat_facets = fetch_json("/products/facets") or {}
        cat_counts = {item['_id']: item['count'] for item in cat_facets.get('categories', [])}
        total_facet_count = sum(cat_counts.values()) or 100
        cat_options = ["All", "laptops", "phones", "shoes", "books"]
        cat_labels = {
            "All": f"🌐 All Disciplines ({total_facet_count})",
            "laptops": f"💻 Laptops ({cat_counts.get('laptops', 0)})",
            "phones": f"📱 Smartphones ({cat_counts.get('phones', 0)})",
            "shoes": f"👟 Audio & Apparel ({cat_counts.get('shoes', 0)})",
            "books": f"📚 Technical Books ({cat_counts.get('books', 0)})"
        }
        current_cat_idx = cat_options.index(st.session_state.selected_category) if st.session_state.selected_category in cat_options else 0
        selected_category = st.selectbox(
            "Discipline",
            cat_options,
            index=current_cat_idx,
            format_func=lambda x: cat_labels.get(x, x),
            label_visibility="collapsed"
        )
        st.session_state.selected_category = selected_category

    with search_col:
        search_q = st.text_input(
            "Search Query",
            placeholder="Search specs, hardware parameters, or keywords...",
            label_visibility="collapsed"
        )

    with rating_col:
        rating_filter = st.selectbox(
            "Min Rating",
            ["All", "4★ & above", "3★ & above"],
            label_visibility="collapsed"
        )

    with mode_col:
        search_mode = st.selectbox(
            "Search Engine",
            ["vector", "keyword"],
            format_func=lambda x: "🔮 AI Vector Search" if x == "vector" else "🔍 Exact Keyword",
            label_visibility="collapsed"
        )

    with sort_col:
        sort_mode = st.selectbox(
            "Sort Order",
            ["Default", "Price: Low to High", "Price: High to Low", "In-Stock First"],
            label_visibility="collapsed"
        )

    # Price Range Filter (ESR Rule Range Predicate) & Polyglot In-Stock Availability
    p_slider_col, p_stock_col, p_info_col = st.columns([2.5, 1.2, 1.0])
    with p_slider_col:
        price_range = st.slider(
            "Price Range Filter ($)",
            min_value=0,
            max_value=2000,
            value=(0, 2000),
            step=50,
            format="$%d"
        )
    with p_stock_col:
        st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)
        in_stock_only = st.checkbox("⚡ In Stock Only", value=False, key="cat_in_stock_only")
    with p_info_col:
        st.markdown(f"""
        <div style="padding-top: 24px; font-size: 12px; color: #52525B;">
            Active Bracket: <strong style="color: #171717;">${price_range[0]} – ${price_range[1]}</strong>
        </div>
        """, unsafe_allow_html=True)

    # Fetch products from API
    query_parts = []
    if selected_category != "All":
        query_parts.append(f"category={urllib.parse.quote(selected_category)}")
    if search_q:
        query_parts.append(f"q={urllib.parse.quote(search_q)}")
        query_parts.append(f"mode={search_mode}")
    if rating_filter == "4★ & above":
        query_parts.append("min_rating=4.0")
    elif rating_filter == "3★ & above":
        query_parts.append("min_rating=3.0")
    if price_range[0] > 0:
        query_parts.append(f"min_price={price_range[0]}")
    if price_range[1] < 2000:
        query_parts.append(f"max_price={price_range[1]}")
    if sort_mode == "Price: Low to High":
        query_parts.append("sort=price_asc")
    elif sort_mode == "Price: High to Low":
        query_parts.append("sort=price_desc")
    if in_stock_only:
        query_parts.append("in_stock=true")
    
    qs = "&".join(query_parts)
    products = fetch_json(f"/products?{qs}" if qs else "/products") or []

    # Client-side sort options (fallback for in-stock ordering)
    if sort_mode == "Price: Low to High":
        products = sorted(products, key=lambda x: float(x.get('price', 0)))
    elif sort_mode == "Price: High to Low":
        products = sorted(products, key=lambda x: float(x.get('price', 0)), reverse=True)
    elif sort_mode == "In-Stock First":
        products = sorted(products, key=lambda x: get_product_stock(x), reverse=True)

    st.markdown(f"<div style='font-size: 12px; color: #52525B; margin: 12px 0 16px 0;'>Displaying <strong>{len(products)}</strong> calibrated hardware instruments</div>", unsafe_allow_html=True)

    if not products:
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 6px; padding: 40px; text-align: center;">
            <div style="font-size: 32px; margin-bottom: 8px;">🔍</div>
            <h4 style="margin: 0 0 6px 0; color: #171717;">No matching hardware configurations found</h4>
            <p style="font-size: 13px; color: #52525B;">Try adjusting your keyword filter or switch to AI Vector Search for conceptual discovery.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # 3-Column Responsive Hardware Grid
        grid_cols = st.columns(3)
        for idx, prod in enumerate(products):
            with grid_cols[idx % 3]:
                stock = get_product_stock(prod)
                stock_label = render_stock_badge(stock)
                
                # Dynamic rating badge from MongoDB Aggregation
                avg_r = prod.get('avg_rating', 0.0)
                rev_count = prod.get('review_count', 0)
                if rev_count > 0 and avg_r > 0:
                    rating_badge = f"<span class='badge-rating'>★ {avg_r:.1f} <span style='font-weight:400; color:#52525B;'>({rev_count})</span></span>"
                else:
                    rating_badge = "<span class='badge-rating-zero'>★ Unrated</span>"

                # Attribute summary tag
                attrs = prod.get('attributes', {})
                attr_summary = " • ".join([f"{v}" for k, v in list(attrs.items())[:2]]) if attrs else prod.get('category', '').capitalize()
                
                st.markdown(f"""
                <div class="nexus-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div style="display: flex; gap: 6px; align-items: center;">
                            <span class="badge-tag">{prod['category']}</span>
                            {rating_badge}
                        </div>
                        {stock_label}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.image(f"{API_URL}/products/{prod['product_id']}/image", use_column_width=True)
                
                st.markdown(f"""
                <div style="margin: 6px 0 12px 0;">
                    <div style="font-size: 11px; color: #52525B; font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em;">{attr_summary}</div>
                    <div style="font-size: 15px; font-weight: 700; color: #171717; margin: 2px 0 4px 0; line-height: 1.3;">{prod['name']}</div>
                    <div style="font-size: 12px; color: #52525B; line-height: 1.4; height: 34px; overflow: hidden; margin-bottom: 8px;">{prod['description']}</div>
                    <div style="font-size: 18px; font-weight: 800; color: #171717;">${prod['price']:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                
                b_det, b_add = st.columns([1, 1])
                with b_det:
                    if st.button("Details", key=f"cat_det_{prod['product_id']}", use_container_width=True):
                        st.session_state.selected_product = prod['product_id']
                        set_page("Product")
                        st.rerun()
                with b_add:
                    if stock > 0:
                        if st.button("Add 🛒", key=f"cat_add_{prod['product_id']}", use_container_width=True, type="primary"):
                            add_to_cart_action(prod['product_id'], 1)
                            st.rerun()
                    else:
                        st.button("Sold Out", key=f"cat_sold_{prod['product_id']}", disabled=True, use_container_width=True)
                
                st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# VIEW 3: PRODUCT DETAILS & HARDWARE SCHEMATICS
# ==============================================================================
elif st.session_state.page == "Product":
    pid = st.session_state.selected_product
    if not pid:
        set_page("Catalog")
        st.rerun()
    prod = fetch_json(f"/products/{pid}")
    if not prod:
        st.error("Failed to load product specifications.")
        if st.button("← Back to Catalog"):
            set_page("Catalog")
            st.rerun()
    else:
        # Breadcrumbs
        st.markdown(f"""
        <nav style="font-size: 12px; color: #52525B; margin-bottom: 14px;">
            <span>Home</span> / <span>Catalog</span> / <span style="text-transform: capitalize;">{prod['category']}</span> / <strong style="color: #171717;">{prod['name']}</strong>
        </nav>
        """, unsafe_allow_html=True)
        
        if st.button("← Return to Hardware Catalog", key="det_back_btn"):
            set_page("Catalog")
            st.rerun()

        # Dual Column Overview
        c_gallery, c_spec = st.columns([6, 6], gap="large")
        
        with c_gallery:
            st.markdown("""
            <div style="background: #F3F4F6; border: 1px solid #E4E4E7; border-radius: 6px; padding: 20px; text-align: center; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 10px; font-weight: 700; color: #52525B; text-transform: uppercase; margin-bottom: 8px;">
                    <span>AEROLITE UNIBODY SPECIFICATION</span>
                    <span>FACTORY CALIBRATED</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.image(f"{API_URL}/products/{pid}/image", use_column_width=True)
            
            st.markdown("""
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 14px;">
                <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 4px; padding: 12px; font-size: 11px;">
                    <strong style="color: #171717; display: block; margin-bottom: 2px;">⚡ Thunderbolt 5</strong>
                    <span style="color: #52525B;">120Gbps bi-directional external bandwidth.</span>
                </div>
                <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 4px; padding: 12px; font-size: 11px;">
                    <strong style="color: #171717; display: block; margin-bottom: 2px;">🛡️ Aerospace CNC</strong>
                    <span style="color: #52525B;">Monolithic 6000-series alloy unibody.</span>
                </div>
                <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 4px; padding: 12px; font-size: 11px;">
                    <strong style="color: #171717; display: block; margin-bottom: 2px;">🌱 Zero Net Carbon</strong>
                    <span style="color: #52525B;">100% renewable energy assembly.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c_spec:
            stock = get_product_stock(prod)
            stock_badge = render_stock_badge(stock, detailed=True)
            
            avg_r = prod.get('avg_rating', 0.0)
            rev_count = prod.get('review_count', 0)
            if rev_count > 0 and avg_r > 0:
                review_sub = f"★ {avg_r:.1f} &nbsp;•&nbsp; {rev_count} verified benchmark reviews &nbsp;•&nbsp; SKU: {prod['product_id']}"
            else:
                review_sub = f"★ Unrated &nbsp;•&nbsp; 0 verified benchmark reviews &nbsp;•&nbsp; SKU: {prod['product_id']}"
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span class="badge-tag">{prod['category']}</span>
                {stock_badge}
            </div>
            <h1 style="font-size: 30px; font-weight: 700; color: #171717; margin: 0 0 8px 0; line-height: 1.2;">{prod['name']}</h1>
            <div style="font-size: 12px; color: #52525B; margin-bottom: 12px;">{review_sub}</div>
            <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 6px; padding: 16px; margin-bottom: 16px;">
                <div style="font-size: 28px; font-weight: 800; color: #171717;">${prod['price']:,.2f}</div>
                <div style="font-size: 11px; color: #52525B; margin-top: 2px;">Excludes applicable local taxes. Expedited shipping included.</div>
            </div>
            <p style="font-size: 14px; color: #52525B; line-height: 1.6; margin-bottom: 16px;">{prod['description']}</p>
            """, unsafe_allow_html=True)

            # Hardware Attributes Chips
            attrs = prod.get('attributes', {})
            if attrs:
                st.markdown("<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #52525B; margin-bottom: 6px;'>Calibrated Parameters</div>", unsafe_allow_html=True)
                chips = "".join([
                    f"<div style='background: #F3F4F6; border: 1px solid #E4E4E7; border-radius: 4px; padding: 6px 12px; margin-right: 8px; margin-bottom: 8px; display: inline-block;'>"
                    f"<div style='font-size: 10px; color: #52525B; text-transform: uppercase; font-weight: 700;'>{k}</div>"
                    f"<div style='font-size: 13px; font-weight: 700; color: #171717;'>{v}</div></div>"
                    for k, v in attrs.items()
                ])
                st.markdown(f"<div style='display: flex; flex-wrap: wrap; margin-bottom: 16px;'>{chips}</div>", unsafe_allow_html=True)

            # Purchase Action Block
            q_col, btn_add_col, btn_buy_col = st.columns([1.5, 2.5, 2.5])
            with q_col:
                det_qty = st.number_input("Qty", min_value=1, max_value=max(1, stock), value=1, key="det_qty_input", disabled=(stock <= 0))
            with btn_add_col:
                if stock > 0:
                    if st.button("🛒 Add to Bag", key="det_add_bag_btn", use_container_width=True, type="primary"):
                        add_to_cart_action(pid, det_qty)
                        st.rerun()
                else:
                    st.button("Sold Out", key="det_sold_out_btn", disabled=True, use_container_width=True)
            with btn_buy_col:
                if stock > 0:
                    if st.button("⚡ Buy Now", key="det_buy_now_btn", use_container_width=True):
                        add_to_cart_action(pid, det_qty)
                        set_page("Cart")
                        st.session_state.checkout_step = 1
                        st.rerun()
                else:
                    st.button("Unavailable", key="det_unavail_btn", disabled=True, use_container_width=True)

        # Mastery in Precision Hardware (Technical Specification Table & Thermal Dock)
        st.markdown("<h3 style='margin: 40px 0 12px 0; font-size: 20px;'>Mastery in Precision Hardware</h3>", unsafe_allow_html=True)
        tab_spec_col, tab_dock_col = st.columns([7, 5], gap="large")
        
        with tab_spec_col:
            st.markdown("""
            <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 6px; overflow: hidden;">
                <div style="background: #F3F4F6; padding: 12px 18px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: #52525B;">
                    Core Architectural Parameters
                </div>
                <div style="padding: 12px 18px; border-bottom: 1px solid #E4E4E7; display: flex; justify-content: space-between; font-size: 13px;">
                    <span style="color: #52525B;">Processor Unit</span>
                    <strong style="color: #171717;">Unified Silicon Compute Block</strong>
                </div>
                <div style="padding: 12px 18px; border-bottom: 1px solid #E4E4E7; display: flex; justify-content: space-between; font-size: 13px;">
                    <span style="color: #52525B;">Display Architecture</span>
                    <strong style="color: #171717;">Low-Reflectance Mini-LED Liquid XDR</strong>
                </div>
                <div style="padding: 12px 18px; border-bottom: 1px solid #E4E4E7; display: flex; justify-content: space-between; font-size: 13px;">
                    <span style="color: #52525B;">Acoustic Floor</span>
                    <strong style="color: #171717;">0 dB Whispering Vapor Chamber Cooling</strong>
                </div>
                <div style="padding: 12px 18px; display: flex; justify-content: space-between; font-size: 13px;">
                    <span style="color: #52525B;">Database Record</span>
                    <strong style="color: #171717;">MongoDB Document &amp; PostgreSQL Inventory Lock</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with tab_dock_col:
            st.markdown("""
            <div style="background: #F3F4F6; border: 1px solid #E4E4E7; border-radius: 6px; padding: 20px;">
                <div style="font-size: 10px; font-weight: 700; text-transform: uppercase; color: #2563EB; letter-spacing: 0.08em; margin-bottom: 4px;">THERMAL DYNAMICS</div>
                <h4 style="font-size: 16px; margin: 0 0 8px 0; color: #171717;">Vapor Chamber Heat Channeling</h4>
                <p style="font-size: 12px; color: #52525B; line-height: 1.5; margin-bottom: 14px;">
                    Dual high-density centrifugal impeller fans engineered with 0.15mm laser-thinned blades evacuate sustained workloads silently. Zero thermal throttling during continuous local compilation.
                </p>
                <div style="display: flex; justify-content: space-between; border-top: 1px solid #E4E4E7; padding-top: 10px; font-size: 11px;">
                    <span style="color: #52525B;">Thermal Dissipation Efficiency</span>
                    <strong style="color: #15803D;">+38% vs Industry Standard</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ChromaDB Semantic Vector Search Recommendations
        st.markdown("<h3 style='margin: 40px 0 12px 0; font-size: 18px;'>Similar Hardware Instruments (AI Semantic Search)</h3>", unsafe_allow_html=True)
        similar_prods = fetch_json(f"/products/{pid}/similar") or []
        if similar_prods:
            sim_cols = st.columns(len(similar_prods))
            for i, sim in enumerate(similar_prods):
                with sim_cols[i]:
                    st.image(f"{API_URL}/products/{sim['product_id']}/image", use_column_width=True)
                    st.markdown(f"""
                    <div style="font-size: 13px; font-weight: 700; color: #171717; margin-top: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{sim['name']}</div>
                    <div style="font-size: 15px; font-weight: 800; color: #171717; margin: 2px 0 8px 0;">${sim['price']:,.2f}</div>
                    """, unsafe_allow_html=True)
                    if st.button("Inspect", key=f"sim_view_{sim['product_id']}", use_container_width=True):
                        st.session_state.selected_product = sim['product_id']
                        st.rerun()


# ==============================================================================
# VIEW 4: SHOPPING CART & MULTI-STEP CHECKOUT
# ==============================================================================
elif st.session_state.page == "Cart":
    # Order Confirmation Screen (Step 4)
    if st.session_state.get('checkout_step') == 4:
        last_id = st.session_state.get('last_order_id', 'N/A')
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #15803D; border-radius: 6px; padding: 44px; text-align: center; margin-bottom: 24px;">
            <div style="font-size: 48px; margin-bottom: 12px;">✅</div>
            <div style="display: inline-block; background: #F0FDF4; color: #15803D; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 4px; text-transform: uppercase; margin-bottom: 12px; letter-spacing: 0.04em;">
                Transaction Approved • ACID Lock Executed
            </div>
            <h2 style="font-size: 24px; font-weight: 800; color: #171717; margin: 0 0 8px 0;">Order #{last_id} Confirmed!</h2>
            <p style="font-size: 13px; color: #52525B; max-width: 540px; margin: 0 auto 20px auto; line-height: 1.6;">
                Thank you for your order. Inventory was deducted atomically via PostgreSQL row-level locks to guarantee zero overselling.
            </p>
            <div style="background: #F3F4F6; border: 1px solid #E4E4E7; border-radius: 4px; padding: 14px; display: inline-block; text-align: left; font-size: 12px; color: #171717; margin-bottom: 20px;">
                <div>📍 <strong>Shipping Destination:</strong> {st.session_state.get('selected_address_text', 'Standard Registered Address')}</div>
                <div style="margin-top: 4px;">💳 <strong>Payment Instrument:</strong> {st.session_state.get('selected_payment_method', 'Credit Card')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c_h, c_c = st.columns(2)
        with c_h:
            if st.button("📦 View in Order History", type="primary", use_container_width=True):
                st.session_state.checkout_step = 1
                set_page("Orders")
                st.rerun()
        with c_c:
            if st.button("🛍️ Continue Shopping", use_container_width=True):
                st.session_state.checkout_step = 1
                set_page("Catalog")
                st.rerun()

    # Empty Cart State
    elif not st.session_state.cart:
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 6px; padding: 48px; text-align: center; margin-bottom: 24px;">
            <div style="font-size: 40px; margin-bottom: 8px;">🛒</div>
            <h3 style="font-size: 20px; font-weight: 700; color: #171717; margin-bottom: 6px;">Your Shopping Bag is Empty</h3>
            <p style="font-size: 13px; color: #52525B; margin-bottom: 20px;">Browse our precision hardware disciplines to configure your equipment.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🛍️ Open Hardware Catalog", type="primary", use_container_width=True):
            set_page("Catalog")
            st.rerun()

    # Active Cart & Checkout Steps
    else:
        # Calculate subtotal & load line items
        subtotal = 0.0
        items_payload = []
        cart_items_data = []
        for pid, qty in list(st.session_state.cart.items()):
            prod = fetch_json(f"/products/{pid}")
            if prod:
                total_line = prod['price'] * qty
                subtotal += total_line
                prod_stock = get_product_stock(prod)
                items_payload.append({"product_id": pid, "qty": qty})
                cart_items_data.append({
                    "product_id": pid, "name": prod['name'], "price": prod['price'],
                    "qty": qty, "total": total_line, "stock": prod_stock
                })

        free_shipping_threshold = 150.0
        shipping = 0.0 if subtotal >= free_shipping_threshold else 15.0
        tax = round(subtotal * 0.08, 2)
        grand_total = round(subtotal + shipping + tax, 2)
        pct_free = min(100, int((subtotal / free_shipping_threshold) * 100))

        # Free Shipping Threshold Progress Banner
        st.markdown(f"""
        <div class="shipping-progress-banner">
            <div>
                <strong style="color: #171717; font-size: 13px;">
                    {'✓ You qualify for Free Next-Day Courier Delivery!' if shipping == 0 else f'Add ${(free_shipping_threshold - subtotal):,.2f} more to unlock Free Next-Day Delivery!'}
                </strong>
                <div style="font-size: 11px; color: #52525B; margin-top: 2px;">Orders over $150.00 qualify for priority expedited transit.</div>
            </div>
            <div style="width: 200px;">
                <div style="display: flex; justify-content: space-between; font-size: 10px; font-weight: 700; color: #52525B;">
                    <span>COURIER PROGRESS</span>
                    <span style="color: #2563EB;">{pct_free}%</span>
                </div>
                <div class="progress-bar-track">
                    <div class="progress-bar-thumb" style="width: {pct_free}%;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Checkout Step Indicator Tabs
        s_c1, s_c2, s_c3 = st.columns(3)
        with s_c1:
            s1_type = "primary" if st.session_state.checkout_step == 1 else "secondary"
            if st.button(f"1️⃣ Review Items ({sum(st.session_state.cart.values())})", key="cart_tab_1", use_container_width=True, type=s1_type):
                st.session_state.checkout_step = 1
                st.rerun()
        with s_c2:
            s2_type = "primary" if st.session_state.checkout_step == 2 else "secondary"
            if st.button("2️⃣ Shipping Destination", key="cart_tab_2", use_container_width=True, type=s2_type):
                st.session_state.checkout_step = 2
                st.rerun()
        with s_c3:
            s3_type = "primary" if st.session_state.checkout_step == 3 else "secondary"
            if st.button("3️⃣ Payment & Confirm", key="cart_tab_3", use_container_width=True, type=s3_type):
                st.session_state.checkout_step = 3
                st.rerun()

        st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

        # --- STEP 1: REVIEW ITEMS ---
        if st.session_state.checkout_step == 1:
            col_items, col_sum = st.columns([7, 5], gap="large")
            with col_items:
                st.markdown("<h4 style='font-size: 16px; margin-bottom: 12px;'>Bag Items</h4>", unsafe_allow_html=True)
                for item in cart_items_data:
                    pid = item['product_id']
                    item_stock = item['stock']
                    stock_pill = render_stock_badge(item_stock)
                    sold_out_warn = "<div style='color: #B91C1C; font-size: 11px; font-weight: 600; margin-top: 4px;'>⚠️ Currently sold out. Please remove this item to proceed.</div>" if item_stock <= 0 else ""
                    st.markdown(f"""
                    <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 4px; padding: 12px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: baseline;">
                            <strong style="font-size: 14px; color: #171717;">{item['name']}</strong>
                            <span style="font-size: 16px; font-weight: 800; color: #171717;">${item['total']:,.2f}</span>
                        </div>
                        <div style="font-size: 11px; color: #52525B; display: flex; align-items: center; gap: 8px; margin-top: 4px;">
                            <span>Unit: ${item['price']:,.2f}</span>
                            <span>•</span>
                            {stock_pill}
                        </div>
                        {sold_out_warn}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    ci_img, ci_qty, ci_del = st.columns([1.5, 3.5, 2])
                    with ci_img:
                        st.image(f"{API_URL}/products/{pid}/image", width=80)
                    with ci_qty:
                        new_q = st.number_input("Qty", min_value=1, max_value=max(1, item_stock), value=min(item['qty'], max(1, item_stock)), key=f"cart_q_{pid}", disabled=(item_stock <= 0))
                        if new_q != item['qty']:
                            st.session_state.cart[pid] = new_q
                            st.rerun()
                    with ci_del:
                        st.markdown("<div style='padding-top: 24px;'></div>", unsafe_allow_html=True)
                        if st.button("Remove", key=f"cart_del_{pid}", use_container_width=True):
                            del st.session_state.cart[pid]
                            st.rerun()
                    st.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid #E4E4E7;'/>", unsafe_allow_html=True)

                c_cont, c_clr = st.columns([2, 1])
                with c_cont:
                    if st.button("← Add More Hardware", use_container_width=True):
                        set_page("Catalog")
                        st.rerun()
                with c_clr:
                    if st.button("Clear Bag", use_container_width=True):
                        st.session_state.cart = {}
                        st.rerun()

            with col_sum:
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 6px; padding: 20px;">
                    <h4 style="font-size: 16px; margin: 0 0 12px 0; color: #171717;">Order Summary</h4>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px;">
                        <span style="color: #52525B;">Subtotal ({sum(st.session_state.cart.values())} items)</span>
                        <strong style="color: #171717;">${subtotal:,.2f}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px;">
                        <span style="color: #52525B;">Courier Shipping</span>
                        <strong style="color: #171717;">{'FREE' if shipping == 0 else f'${shipping:,.2f}'}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 12px;">
                        <span style="color: #52525B;">Estimated Tax (8%)</span>
                        <strong style="color: #171717;">${tax:,.2f}</strong>
                    </div>
                    <div style="border-top: 1px solid #E4E4E7; padding-top: 10px; display: flex; justify-content: space-between; font-size: 18px; font-weight: 800;">
                        <span style="color: #171717;">Total</span>
                        <span style="color: #171717;">${grand_total:,.2f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
                has_out_of_stock = any(item['stock'] <= 0 for item in cart_items_data)
                has_over_stock = any(item['qty'] > item['stock'] for item in cart_items_data)
                if has_out_of_stock or has_over_stock:
                    st.warning("⚠️ Some items in your bag exceed available inventory stock. Please adjust quantities before proceeding.")
                if st.button("Proceed to Delivery Address →", type="primary", use_container_width=True, key="cart_to_s2", disabled=(has_out_of_stock or has_over_stock)):
                    st.session_state.checkout_step = 2
                    st.rerun()

        # --- STEP 2: SHIPPING DESTINATION ---
        elif st.session_state.checkout_step == 2:
            st.markdown("<h4 style='font-size: 16px; margin-bottom: 12px;'>Step 2: Shipping Destination</h4>", unsafe_allow_html=True)
            col_addr_list, col_addr_snap = st.columns([7, 5], gap="large")
            
            with col_addr_list:
                if not st.session_state.user:
                    st.markdown("""
                    <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 4px; padding: 16px; margin-bottom: 16px;">
                        <strong style="color: #B45309; font-size: 13px;">🔒 Authentication Required</strong>
                        <p style="font-size: 12px; color: #B45309; margin: 4px 0 0 0;">Please sign in to select or save shipping destinations.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("⚡ 1-Click Sign In as Demo User", type="primary", use_container_width=True, key="cart_demo_s2"):
                        res, err = post_json("/auth/login", {"email": "demo@nexus.com", "password": "demo123"})
                        if res and "user" in res:
                            st.session_state.user = res["user"]
                            st.rerun()
                else:
                    user_id = st.session_state.user['id']
                    addresses = fetch_json(f"/users/{user_id}/addresses") or []
                    if addresses:
                        addr_options = [a['id'] for a in addresses]
                        addr_map = {
                            a['id']: f"{a['label']}: {a['recipient_name']} — {a['street']}, {a['city']}, {a['state']} {a['postal_code']}"
                            for a in addresses
                        }
                        default_id = next((a['id'] for a in addresses if a.get('is_default')), addresses[0]['id'])
                        selected_id = st.radio(
                            "Choose a saved shipping destination:",
                            options=addr_options,
                            format_func=lambda x: addr_map[x],
                            index=addr_options.index(default_id) if default_id in addr_options else 0,
                            key="cart_addr_radio"
                        )
                        st.session_state.selected_address_id = selected_id
                        st.session_state.selected_address_text = addr_map[selected_id]
                    else:
                        st.info("No saved addresses. Please add an address below.")
                        st.session_state.selected_address_text = ""

                    # Inline Add Address
                    with st.expander("+ Add New Destination", expanded=(not addresses)):
                        with st.form("inline_addr_form"):
                            lbl = st.text_input("Label", value="Home")
                            rec = st.text_input("Recipient Full Name", value=st.session_state.user.get('name', ''))
                            st_addr = st.text_input("Street Address", placeholder="742 Evergreen Terrace")
                            ct = st.text_input("City", placeholder="Springfield")
                            stt = st.text_input("State", placeholder="OR")
                            zp = st.text_input("Postal Code", placeholder="97477")
                            def_chk = st.checkbox("Set as default shipping address", value=(not addresses))
                            if st.form_submit_button("Save & Use Address", type="primary"):
                                if st_addr and ct:
                                    payload = {
                                        "label": lbl, "recipient_name": rec, "street": st_addr,
                                        "city": ct, "state": stt, "postal_code": zp, "is_default": def_chk
                                    }
                                    res, err = post_json(f"/users/{user_id}/addresses", payload)
                                    if res:
                                        st.success("Address saved!")
                                        st.rerun()
                                    else:
                                        st.error(f"Error: {err}")
                                shower = True
                                if not (st_addr and ct):
                                    st.warning("Please provide street and city.")

                    b_s1, b_s3 = st.columns(2)
                    with b_s1:
                        if st.button("← Back to Review Items", use_container_width=True):
                            st.session_state.checkout_step = 1
                            st.rerun()
                    with b_s3:
                        if st.button("Continue to Payment →", key="to_s3_from_s2", type="primary", use_container_width=True):
                            if not addresses and not st.session_state.get('selected_address_text'):
                                st.error("Please add a delivery destination first.")
                            else:
                                st.session_state.checkout_step = 3
                                st.rerun()

            with col_addr_snap:
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 6px; padding: 20px;">
                    <h4 style="font-size: 15px; margin: 0 0 10px 0; color: #171717;">Order Snapshot</h4>
                    <div style="font-size: 13px; color: #52525B; margin-bottom: 4px;">Items: <strong style="color: #171717;">{sum(st.session_state.cart.values())}</strong></div>
                    <div style="font-size: 13px; color: #52525B; margin-bottom: 4px;">Subtotal: <strong style="color: #171717;">${subtotal:,.2f}</strong></div>
                    <div style="font-size: 13px; color: #52525B; margin-bottom: 4px;">Shipping: <strong style="color: #171717;">{'FREE' if shipping == 0 else f'${shipping:,.2f}'}</strong></div>
                    <div style="font-size: 13px; color: #52525B; margin-bottom: 8px;">Tax: <strong style="color: #171717;">${tax:,.2f}</strong></div>
                    <div style="border-top: 1px solid #E4E4E7; padding-top: 8px; font-size: 18px; font-weight: 800; color: #171717;">
                        Total: ${grand_total:,.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # --- STEP 3: PAYMENT & CONFIRMATION ---
        elif st.session_state.checkout_step == 3:
            st.markdown("<h4 style='font-size: 16px; margin-bottom: 12px;'>Step 3: Payment Method & Final Review</h4>", unsafe_allow_html=True)
            col_p_meth, col_p_conf = st.columns([7, 5], gap="large")
            
            with col_p_meth:
                payment_methods = [
                    "💳 Credit Card (Nexus Pay)",
                    "🍎 Apple Pay / Google Pay One-Touch",
                    "📦 Cash on Courier Delivery (COD)",
                    "🏦 Direct Bank Transfer / ACH"
                ]
                chosen_pay = st.radio("Select Payment Instrument:", payment_methods, index=0, key="cart_pay_radio")
                st.session_state.selected_payment_method = chosen_pay

                selected_addr = st.session_state.get('selected_address_text', 'Default Registered Address')
                st.markdown(f"""
                <div style="background: #F3F4F6; border: 1px solid #E4E4E7; border-radius: 4px; padding: 12px; margin: 16px 0;">
                    <div style="font-size: 10px; font-weight: 700; color: #52525B; text-transform: uppercase;">Destination Confirmed</div>
                    <div style="font-size: 13px; font-weight: 600; color: #171717; margin-top: 4px;">📍 {selected_addr}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("← Change Destination", use_container_width=True):
                    st.session_state.checkout_step = 2
                    st.rerun()

            with col_p_conf:
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 6px; padding: 22px;">
                    <h4 style="font-size: 16px; margin: 0 0 12px 0; color: #171717;">Final Order Summary</h4>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px;">
                        <span style="color: #52525B;">Subtotal</span><strong style="color: #171717;">${subtotal:,.2f}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px;">
                        <span style="color: #52525B;">Expedited Dispatch</span><strong style="color: #171717;">{'FREE' if shipping == 0 else f'${shipping:,.2f}'}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 12px;">
                        <span style="color: #52525B;">Estimated Tax</span><strong style="color: #171717;">${tax:,.2f}</strong>
                    </div>
                    <div style="border-top: 1px solid #E4E4E7; padding-top: 10px; display: flex; justify-content: space-between; align-items: baseline;">
                        <span style="font-size: 15px; font-weight: 700; color: #171717;">Total Charged</span>
                        <span style="font-size: 22px; font-weight: 800; color: #171717;">${grand_total:,.2f}</span>
                    </div>
                    <div style="font-size: 11px; color: #52525B; margin-top: 8px;">
                        🔒 PostgreSQL ACID row lock guarantees inventory reservation with zero overselling.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
                if st.button(f"⚡ Confirm & Execute Order (${grand_total:,.2f})", type="primary", use_container_width=True, key="cart_place_btn"):
                    if not st.session_state.user:
                        st.error("Please sign in before completing your order.")
                    else:
                        # Re-validate live inventory stock right before order execution
                        stock_errors = []
                        for pid, qty in list(st.session_state.cart.items()):
                            live_prod = fetch_json(f"/products/{pid}")
                            live_stock = get_product_stock(live_prod) if live_prod else 0
                            if live_stock < qty:
                                p_name = live_prod.get('name', pid) if live_prod else pid
                                stock_errors.append(f"'{p_name}' only has {live_stock} units left in stock (requested {qty})")
                        if stock_errors:
                            for s_err in stock_errors:
                                st.error(f"⚠️ Inventory check: {s_err}. Please review your bag.")
                        else:
                            order_payload = {
                                "user_id": st.session_state.user['id'],
                                "items": items_payload,
                                "shipping_address": st.session_state.get('selected_address_text', 'Standard Delivery Address'),
                                "payment_method": st.session_state.selected_payment_method
                            }
                            res, err = post_json("/orders", order_payload)
                            if err:
                                st.error(f"Transaction failed: {err}")
                            else:
                                st.balloons()
                                st.session_state.cart = {}
                                st.session_state.last_order_id = res['order_id']
                                st.session_state.checkout_step = 4
                                st.rerun()


# ==============================================================================
# VIEW 5: USER PROFILE & ADDRESS BOOK
# ==============================================================================
elif st.session_state.page == "Profile":
    user = st.session_state.user
    if not user:
        st.warning("Please sign in to manage account details and saved destinations.")
        if st.button("🔑 Sign In / Register", type="primary"):
            set_page("Auth")
            st.rerun()
    else:
        st.markdown(f"<h2 style='margin-bottom: 4px;'>Customer Profile & Addresses</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 12px; color: #52525B; margin-bottom: 20px;'>Manage account credentials, saved delivery destinations, and preferences.</p>", unsafe_allow_html=True)
        
        prof_c, addr_c = st.columns([5, 7], gap="large")
        
        with prof_c:
            st.markdown("<h4 style='font-size: 15px; margin-bottom: 10px;'>Account Credentials</h4>", unsafe_allow_html=True)
            with st.form("prof_edit_form"):
                pn = st.text_input("Full Name", value=user.get('name', ''))
                pe = st.text_input("Email Address", value=user.get('email', ''))
                st.markdown(f"<div style='font-size: 11px; color: #52525B; margin-bottom: 10px;'>Account Reference ID: #{user.get('id')}</div>", unsafe_allow_html=True)
                if st.form_submit_button("Save Profile Changes", type="primary"):
                    res, err = put_json(f"/users/{user['id']}", {"name": pn.strip(), "email": pe.strip().lower()})
                    if res:
                        st.session_state.user['name'] = pn.strip()
                        st.session_state.user['email'] = pe.strip().lower()
                        st.success("Profile saved!")
                        st.rerun()
                    else:
                        st.error(f"Failed: {err}")
            
            if st.button("🚪 Sign Out of Account", use_container_width=True):
                st.session_state.user = None
                st.session_state.cart = {}
                st.session_state.selected_address_id = None
                set_page("Auth")
                st.rerun()

        with addr_c:
            st.markdown("<h4 style='font-size: 15px; margin-bottom: 10px;'>Saved Delivery Destinations</h4>", unsafe_allow_html=True)
            addresses = fetch_json(f"/users/{user['id']}/addresses") or []
            if addresses:
                for a in addresses:
                    aid = a['id']
                    is_def = a.get('is_default', False)
                    def_tag = "<span style='background: #F0FDF4; color: #15803D; font-size: 9px; font-weight: 700; padding: 2px 6px; border-radius: 4px; margin-left: 6px;'>DEFAULT</span>" if is_def else ""
                    st.markdown(f"""
                    <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 4px; padding: 12px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: baseline;">
                            <strong style="font-size: 13px; color: #171717;">📍 {a['label']} {def_tag}</strong>
                            <span style="font-size: 11px; color: #52525B;">{a.get('country', 'USA')}</span>
                        </div>
                        <div style="font-size: 12px; color: #52525B; margin-top: 2px;">{a['recipient_name']} — {a['street']}, {a['city']}, {a['state']} {a['postal_code']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    ca_def, ca_del = st.columns([2, 1])
                    with ca_def:
                        if not is_def:
                            if st.button("Set Default", key=f"p_sdef_{aid}", use_container_width=True):
                                put_json(f"/users/{user['id']}/addresses/{aid}/default")
                                st.rerun()
                    with ca_del:
                        if st.button("Delete", key=f"p_del_{aid}", use_container_width=True):
                            delete_req(f"/users/{user['id']}/addresses/{aid}")
                            st.rerun()
            else:
                st.info("No saved addresses.")

            with st.expander("+ Add New Address"):
                with st.form("prof_add_addr_form"):
                    lbl = st.text_input("Label (e.g. Home, Work)", value="Home")
                    rc = st.text_input("Recipient Name", value=user.get('name', ''))
                    stt = st.text_input("Street Address", placeholder="742 Evergreen Terrace")
                    cy = st.text_input("City", placeholder="Springfield")
                    se = st.text_input("State", placeholder="OR")
                    zc = st.text_input("Postal Code", placeholder="97477")
                    is_d = st.checkbox("Make this my default shipping destination")
                    if st.form_submit_button("Save Destination", type="primary"):
                        if stt and cy:
                            payload = {
                                "label": lbl, "recipient_name": rc, "street": stt,
                                "city": cy, "state": se, "postal_code": zc, "is_default": is_d
                            }
                            res, err = post_json(f"/users/{user['id']}/addresses", payload)
                            if res:
                                st.success("Destination saved!")
                                st.rerun()
                            else:
                                st.error(f"Error: {err}")
                        else:
                            st.warning("Please enter street and city.")


# ==============================================================================
# VIEW 6: ORDER HISTORY
# ==============================================================================
elif st.session_state.page == "Orders":
    user = st.session_state.user
    if not user:
        st.markdown("<h2 style='margin-bottom: 6px;'>Your Order History</h2>", unsafe_allow_html=True)
        st.warning("Please sign in to view past order receipts.")
        if st.button("🔑 Sign In / Register", type="primary"):
            set_page("Auth")
            st.rerun()
    else:
        user_id = user['id']
        st.markdown("<h2 style='margin-bottom: 4px;'>Your Order History</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 12px; color: #52525B; margin-bottom: 20px;'>Displaying confirmed hardware orders for <strong>{user['name']}</strong> (Customer #{user_id})</p>", unsafe_allow_html=True)
        
        orders = fetch_json(f"/orders?user_id={user_id}") or []
        if not orders:
            st.markdown("""
            <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 6px; padding: 36px; text-align: center;">
                <div style="font-size: 32px; margin-bottom: 6px;">📦</div>
                <h4 style="margin: 0 0 4px 0; color: #171717;">No historical orders found</h4>
                <p style="font-size: 12px; color: #52525B;">Complete a checkout to record your hardware order here.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for o in orders:
                order_id = o['id']
                created = o.get('created_at', 'Recently')
                total = float(o.get('total', 0.0))
                status = o.get('status', 'completed').capitalize()
                addr = o.get('shipping_address') or 'Standard Registered Address'
                pay_method = o.get('payment_method') or 'Credit Card'
                
                with st.expander(f"📦 Order #{order_id} — ${total:,.2f} — {status} ({created})", expanded=True):
                    st.markdown(f"""
                    <div style="background: #F3F4F6; border: 1px solid #E4E4E7; border-radius: 4px; padding: 10px 14px; margin-bottom: 10px; font-size: 12px; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                        <div><strong>📍 Destination:</strong> {addr}</div>
                        <div><strong>💳 Payment:</strong> {pay_method}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    items = fetch_json(f"/orders/{order_id}/items") or []
                    for it in items:
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid #E4E4E7; font-size: 12px;">
                            <div>
                                <strong style="color: #171717;">{it['product_name']}</strong>
                                <span style="color: #52525B; font-size: 10px; margin-left: 6px;">(SKU: {it['product_id']})</span>
                            </div>
                            <div>
                                <span style="color: #52525B;">{it['qty']} × ${float(it['price']):,.2f} = </span>
                                <strong style="color: #171717;">${float(it['price']) * it['qty']:,.2f}</strong>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)


# ==============================================================================
# VIEW 7: AUTHENTICATION (SIGN IN / REGISTER)
# ==============================================================================
elif st.session_state.page == "Auth":
    st.markdown("<h2 style='margin-bottom: 4px;'>Customer Authentication</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 12px; color: #52525B; margin-bottom: 20px;'>Sign in with your Nexus credentials to manage saved addresses and track orders.</p>", unsafe_allow_html=True)
    
    if st.session_state.user:
        u = st.session_state.user
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #E4E4E7; border-radius: 6px; padding: 24px; margin-bottom: 20px;">
            <h4 style="margin: 0 0 4px 0; color: #171717;">Currently Authenticated as {u.get('name', 'Customer')}</h4>
            <div style="font-size: 12px; color: #52525B; margin-bottom: 12px;">{u.get('email', '')} &nbsp;•&nbsp; Account #{u.get('id', '')}</div>
            <p style="font-size: 13px; color: #52525B; margin: 0;">Your session is active. You can browse the catalog, configure hardware, or view past order receipts.</p>
        </div>
        """, unsafe_allow_html=True)
        
        ca1, ca2, ca3 = st.columns(3)
        with ca1:
            if st.button("🛍️ Hardware Catalog", use_container_width=True, type="primary"):
                set_page("Catalog")
                st.rerun()
        with ca2:
            if st.button("📦 Order History", use_container_width=True):
                set_page("Orders")
                st.rerun()
        with ca3:
            if st.button("🚪 Sign Out", use_container_width=True):
                st.session_state.user = None
                st.session_state.cart = {}
                st.session_state.selected_address_id = None
                st.rerun()
    else:
        auth_t1, auth_t2 = st.tabs(["🔑 Sign In", "📝 Create New Account"])
        with auth_t1:
            st.markdown("""
            <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 4px; padding: 12px; margin-bottom: 16px; font-size: 12px; color: #1E40AF;">
                💡 <strong>Demo Account Credentials</strong>: <code>demo@nexus.com</code> / <code>demo123</code>
            </div>
            """, unsafe_allow_html=True)
            if st.button("⚡ 1-Click Quick Login as Demo User", type="primary", use_container_width=True, key="auth_quick_demo"):
                res, err = post_json("/auth/login", {"email": "demo@nexus.com", "password": "demo123"})
                if res and "user" in res:
                    st.session_state.user = res["user"]
                    st.toast("⚡ Welcome back, Demo User!", icon="✅")
                    set_page("Catalog")
                    st.rerun()
                else:
                    st.error(f"Login failed: {err}")
            
            st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E4E4E7;'/>", unsafe_allow_html=True)
            with st.form("auth_manual_login"):
                in_e = st.text_input("Email Address", placeholder="name@example.com")
                in_p = st.text_input("Password", type="password")
                if st.form_submit_button("Sign In", use_container_width=True):
                    if in_e and in_p:
                        res, err = post_json("/auth/login", {"email": in_e.strip(), "password": in_p.strip()})
                        if res and "user" in res:
                            st.session_state.user = res["user"]
                            st.toast(f"Welcome back, {res['user']['name']}!", icon="✅")
                            set_page("Catalog")
                            st.rerun()
                        else:
                            st.error(f"Login failed: {err}")
                    else:
                        st.warning("Please provide email and password.")

        with auth_t2:
            with st.form("auth_reg_form"):
                rn = st.text_input("Full Name", placeholder="Alex Mercer")
                re_em = st.text_input("Email Address", placeholder="alex@example.com")
                rp = st.text_input("Password", type="password")
                if st.form_submit_button("Create Account", use_container_width=True):
                    if rn and re_em and rp:
                        res, err = post_json("/auth/register", {"name": rn.strip(), "email": re_em.strip(), "password": rp.strip()})
                        if res and "user" in res:
                            st.session_state.user = res["user"]
                            st.toast(f"🎉 Account created! Welcome, {res['user']['name']}!", icon="✅")
                            set_page("Catalog")
                            st.rerun()
                        else:
                            st.error(f"Registration failed: {err}")
                    else:
                        st.warning("Please fill in all fields.")


# ==============================================================================
# VIEW 8: DATABASE TELEMETRY
# ==============================================================================
elif st.session_state.page == "Databases":
    st.markdown("<h2 style='margin-bottom: 4px;'>System & Database Telemetry</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 12px; color: #52525B; margin-bottom: 20px;'>Live query routing across PostgreSQL (ACID & Auth), MongoDB (Catalog), and ChromaDB (Vector Similarity).</p>", unsafe_allow_html=True)
    
    debug_info = fetch_json("/debug/requests")
    if debug_info and 'requests' in debug_info and debug_info['requests']:
        st.table(debug_info['requests'])
    else:
        st.info("No queries recorded yet.")
