import streamlit as st
import urllib.request
import urllib.parse
import json
import os
import time

# ==============================================================================
# 1. PAGE CONFIGURATION & METADATA
# ==============================================================================
st.set_page_config(
    page_title="NEXUS — Premium Multipurpose Store",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "http://127.0.0.1:8000"

# ==============================================================================
# 2. DESIGN SYSTEM & HIGH-PERFORMANCE CSS
# ==============================================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
/* --------------------------------------------------------------------------
   Core Design Tokens: Flipkart / Amazon Premium White & Blue Palette
-------------------------------------------------------------------------- */
:root {
    --nexus-bg-primary: #FFFFFF;
    --nexus-bg-secondary: #F5F7FA;
    --nexus-bg-surface: #F8FAFC;
    --nexus-text-primary: #172033;
    --nexus-text-secondary: #687386;
    --nexus-text-muted: #94A3B8;
    --nexus-blue: #2874F0;
    --nexus-blue-hover: #1E5BC6;
    --nexus-blue-light: #EAF2FF;
    --nexus-blue-border: #C8DCFE;
    --nexus-border: #E5E9F0;
    --nexus-border-light: #F0F3F8;
    --nexus-success: #16865C;
    --nexus-success-bg: #EDFBF4;
    --nexus-warning: #D97706;
    --nexus-warning-bg: #FFFBEB;
    --nexus-error: #DC4545;
    --nexus-error-bg: #FEF2F2;
    --nexus-radius: 6px;
}

/* --------------------------------------------------------------------------
   Layout Overrides: Hide Streamlit Default Clutter & Establish Clean Canvas
-------------------------------------------------------------------------- */
header[data-testid="stHeader"],
footer,
section[data-testid="stSidebar"] {
    display: none !important;
}

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background-color: var(--nexus-bg-secondary) !important;
    color: var(--nexus-text-primary) !important;
}

.block-container {
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    max-width: 1440px !important;
}

/* Headings */
h1, h2, h3, h4, h5, h6, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    font-family: 'Inter', sans-serif !important;
    color: var(--nexus-text-primary) !important;
    font-weight: 700 !important;
    letter-spacing: -0.015em !important;
}

/* --------------------------------------------------------------------------
   Hide Empty Streamlit Elements & Style Blocks
-------------------------------------------------------------------------- */
div[data-testid="element-container"]:empty,
div[data-testid="element-container"]:has(> div[data-testid="stMarkdownContainer"] > style:only-child) {
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

#nexus-navbar-root {
    display: none !important;
}

div[data-testid="element-container"]:has(#nexus-navbar-root) {
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* --------------------------------------------------------------------------
   Unified Persistent Two-Row Top Navigation Container
-------------------------------------------------------------------------- */
.block-container > div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:has(#nexus-navbar-root),
.block-container > div > div > div > div[data-testid="stVerticalBlockBorderWrapper"]:has(#nexus-navbar-root),
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:has(#nexus-navbar-root) {
    position: sticky !important;
    top: 0 !important;
    z-index: 99999 !important;
    background-color: #FFFFFF !important;
    border-bottom: 1px solid var(--nexus-border) !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04) !important;
    padding: 10px 1.5rem 8px 1.5rem !important;
    margin-left: -1.5rem !important;
    margin-right: -1.5rem !important;
    margin-top: 0 !important;
    margin-bottom: 18px !important;
}

/* Tighten inner spacing inside unified navbar so both rows fit cleanly */
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:has(#nexus-navbar-root) div[data-testid="stVerticalBlock"] {
    gap: 0.35rem !important;
}

.nexus-navbar-divider {
    border-top: 1px solid var(--nexus-border-light);
    margin: 4px 0 6px 0;
    width: 100%;
}

/* Row 1 / Row 2 Top Header Elements */
.nexus-top-row1 {
    display: flex;
    align-items: center;
    gap: 16px;
    padding-bottom: 6px;
}

.nexus-top-row2 {
    display: flex;
    align-items: center;
    gap: 12px;
    border-top: 1px solid var(--nexus-border-light);
    padding-top: 6px;
}

/* Branding Logo */
.nexus-brand-text {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--nexus-text-primary);
    display: flex;
    align-items: center;
    gap: 4px;
}
.nexus-brand-accent {
    color: var(--nexus-blue);
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Location Pill */
.nexus-loc-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: var(--nexus-text-secondary);
    line-height: 1.2;
}
.nexus-loc-pill strong {
    color: var(--nexus-text-primary);
    display: block;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 170px;
}

/* Category Navigation Strip Buttons */
div.nexus-cat-strip button {
    border-radius: 9999px !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    padding: 6px 14px !important;
    min-height: 34px !important;
    height: 34px !important;
}

/* --------------------------------------------------------------------------
   Buttons & Inputs System (Flipkart/Amazon Modern Clean Style)
-------------------------------------------------------------------------- */
.stButton > button,
button[kind="primary"],
button[kind="secondary"],
.stFormSubmitButton > button {
    border-radius: var(--nexus-radius) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    min-height: 38px !important;
    padding: 7px 14px !important;
    letter-spacing: 0.01em !important;
    transition: all 0.12s ease !important;
}

/* Primary Button: Solid Brand Blue */
button[kind="primary"],
.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background-color: var(--nexus-blue) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--nexus-blue) !important;
    box-shadow: 0 1px 2px rgba(40, 116, 240, 0.15) !important;
}
button[kind="primary"]:hover,
.stButton > button[kind="primary"]:hover {
    background-color: var(--nexus-blue-hover) !important;
    border-color: var(--nexus-blue-hover) !important;
    color: #FFFFFF !important;
}
button[kind="primary"] *,
.stButton > button[kind="primary"] * {
    color: #FFFFFF !important;
}

/* Secondary Button: White Card with Clean Border */
button[kind="secondary"],
.stButton > button:not([kind="primary"]),
.stFormSubmitButton > button:not([kind="primary"]) {
    background-color: #FFFFFF !important;
    color: var(--nexus-text-primary) !important;
    border: 1px solid var(--nexus-border) !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
}
button[kind="secondary"]:hover,
.stButton > button:not([kind="primary"]):hover {
    background-color: var(--nexus-bg-surface) !important;
    border-color: var(--nexus-blue-border) !important;
    color: var(--nexus-blue) !important;
}
button[kind="secondary"]:hover * {
    color: var(--nexus-blue) !important;
}

/* Popover Buttons */
div[data-testid="stPopover"] > button {
    background-color: #FFFFFF !important;
    border: 1px solid var(--nexus-border) !important;
    color: var(--nexus-text-primary) !important;
    border-radius: var(--nexus-radius) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    min-height: 38px !important;
    padding: 6px 12px !important;
}
div[data-testid="stPopover"] > button:hover {
    border-color: var(--nexus-blue) !important;
    background-color: var(--nexus-bg-surface) !important;
}

/* Inputs & Form Controls */
div[data-baseweb="input"] {
    background-color: #FFFFFF !important;
    border: 1px solid var(--nexus-border) !important;
    border-radius: var(--nexus-radius) !important;
    min-height: 38px !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: var(--nexus-blue) !important;
    box-shadow: 0 0 0 2px var(--nexus-blue-light) !important;
}
div[data-baseweb="input"] input {
    font-size: 13px !important;
    color: var(--nexus-text-primary) !important;
    padding: 8px 12px !important;
}

div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid var(--nexus-border) !important;
    border-radius: var(--nexus-radius) !important;
    min-height: 36px !important;
    font-size: 13px !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--nexus-blue) !important;
}

/* --------------------------------------------------------------------------
   Product Cards & Grid System
-------------------------------------------------------------------------- */
.nexus-product-card {
    background: #FFFFFF;
    border: 1px solid var(--nexus-border);
    border-radius: 8px;
    padding: 14px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    margin-bottom: 14px;
}
.nexus-product-card:hover {
    border-color: var(--nexus-blue-border);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
}

.nexus-product-img-wrap {
    background: var(--nexus-bg-surface);
    border-radius: 6px;
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
    min-height: 160px;
}
.nexus-product-img-wrap img {
    max-height: 140px;
    width: auto;
    object-fit: contain;
}

.nexus-product-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--nexus-text-primary);
    line-height: 1.35;
    margin-bottom: 4px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    height: 38px;
}

.nexus-product-attr {
    font-size: 11px;
    font-weight: 500;
    color: var(--nexus-text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.nexus-product-price {
    font-size: 17px;
    font-weight: 800;
    color: var(--nexus-text-primary);
    margin: 4px 0 8px 0;
}

/* Badges */
.badge-cat {
    background: var(--nexus-bg-surface);
    color: var(--nexus-text-secondary);
    border: 1px solid var(--nexus-border);
    font-size: 10px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.badge-rating {
    background: #FFFBEB;
    color: #92400E;
    border: 1px solid #FDE68A;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    gap: 3px;
}
.badge-stock-in {
    background: var(--nexus-success-bg);
    color: var(--nexus-success);
    border: 1px solid #BBF7D0;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
}
.badge-stock-low {
    background: var(--nexus-warning-bg);
    color: var(--nexus-warning);
    border: 1px solid #FDE68A;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
}
.badge-stock-out {
    background: var(--nexus-error-bg);
    color: var(--nexus-error);
    border: 1px solid #FECACA;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
}

/* --------------------------------------------------------------------------
   Left Facet Sidebar (Desktop Flipkart / Amazon Style)
-------------------------------------------------------------------------- */
.nexus-facet-box {
    background: #FFFFFF;
    border: 1px solid var(--nexus-border);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
}
.nexus-facet-title {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--nexus-text-primary);
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* --------------------------------------------------------------------------
   Cart, Checkout & Progress Bar
-------------------------------------------------------------------------- */
.shipping-progress-banner {
    background: #FFFFFF;
    border: 1px solid var(--nexus-border);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 18px;
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
/* --------------------------------------------------------------------------
   Homepage Components: Hero, Categories, Sections, Footer
-------------------------------------------------------------------------- */
.nexus-home-hero {
    background: linear-gradient(135deg, #FFFFFF 0%, #F0F6FF 100%);
    border: 1px solid var(--nexus-border);
    border-radius: 12px;
    padding: 32px 36px;
    box-shadow: 0 2px 10px rgba(40, 116, 240, 0.04);
}
.nexus-hero-badge {
    display: inline-block;
    background: var(--nexus-blue-light);
    color: var(--nexus-blue);
    border: 1px solid var(--nexus-blue-border);
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 12px;
}
.nexus-hero-title {
    font-size: 28px;
    font-weight: 800;
    color: var(--nexus-text-primary);
    line-height: 1.25;
    margin-bottom: 10px;
    letter-spacing: -0.02em;
}
.nexus-hero-sub {
    font-size: 14px;
    color: var(--nexus-text-secondary);
    line-height: 1.55;
    margin-bottom: 6px;
    max-width: 580px;
}

.nexus-section-header {
    margin: 20px 0 14px 0;
}
.nexus-section-title {
    font-size: 20px;
    font-weight: 800;
    color: var(--nexus-text-primary);
    margin: 0;
    letter-spacing: -0.01em;
}
.nexus-section-sub {
    font-size: 13px;
    color: var(--nexus-text-secondary);
    margin: 4px 0 0 0;
}

.nexus-cat-card {
    background: #FFFFFF;
    border: 1px solid var(--nexus-border);
    border-radius: 10px;
    padding: 20px 16px 14px 16px;
    text-align: center;
    transition: all 0.15s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    margin-bottom: 10px;
}
.nexus-cat-card:hover {
    border-color: var(--nexus-blue);
    transform: translateY(-2px);
    box-shadow: 0 8px 18px rgba(40, 116, 240, 0.08);
}
.nexus-cat-icon {
    font-size: 36px;
    margin-bottom: 10px;
    display: block;
}
.nexus-cat-title {
    font-size: 16px;
    font-weight: 700;
    color: var(--nexus-text-primary);
    margin-bottom: 4px;
}
.nexus-cat-desc {
    font-size: 12px;
    color: var(--nexus-text-secondary);
    line-height: 1.4;
    margin-bottom: 10px;
    min-height: 34px;
}

.nexus-footer {
    background: #FFFFFF;
    border-top: 1px solid var(--nexus-border);
    border-radius: 10px;
    padding: 32px 36px 20px 36px;
    margin-top: 36px;
    box-shadow: 0 -1px 4px rgba(0, 0, 0, 0.02);
}
.nexus-footer-brand {
    font-size: 18px;
    font-weight: 800;
    color: var(--nexus-blue);
    margin-bottom: 8px;
}
.nexus-footer-sub {
    font-size: 12px;
    color: var(--nexus-text-secondary);
    line-height: 1.5;
}
.nexus-footer-heading {
    font-size: 13px;
    font-weight: 700;
    color: var(--nexus-text-primary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 10px;
}
.nexus-footer-links {
    list-style: none;
    padding: 0;
    margin: 0;
}
.nexus-footer-links li {
    font-size: 12px;
    color: var(--nexus-text-secondary);
    margin-bottom: 6px;
}
.nexus-footer-bottom {
    border-top: 1px solid var(--nexus-border-light);
    margin-top: 24px;
    padding-top: 14px;
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: var(--nexus-text-secondary);
}
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. CURRENCY FORMATTING HELPER (INDIAN RUPEES ₹)
# ==============================================================================
def format_rupee(amount):
    """
    Centralized Indian Rupee formatting function.
    Formats numbers into standard Indian Rupee notation with the ₹ symbol.
    """
    try:
        val = float(amount)
        return f"₹{val:,.2f}"
    except (ValueError, TypeError):
        return f"₹{amount}"


# ==============================================================================
# 4. HIGH-PERFORMANCE API CLIENT & STREAMLIT CACHE
# ==============================================================================
def fetch_json(endpoint):
    try:
        req = urllib.request.Request(
            f"{API_URL}{endpoint}",
            headers={'User-Agent': 'Nexus-Client'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None

def post_json(endpoint, data):
    req = urllib.request.Request(
        f"{API_URL}{endpoint}",
        data=json.dumps(data).encode(),
        headers={'Content-Type': 'application/json', 'User-Agent': 'Nexus-Client'}
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
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
    req = urllib.request.Request(f"{API_URL}{endpoint}", method='DELETE', headers={'User-Agent': 'Nexus-Client'})
    try:
        with urllib.request.urlopen(req, timeout=6) as response:
            return json.loads(response.read().decode()), None
    except Exception as e:
        return None, str(e)

def put_json(endpoint, data=None):
    data_bytes = json.dumps(data).encode() if data else b""
    req = urllib.request.Request(
        f"{API_URL}{endpoint}",
        data=data_bytes,
        headers={'Content-Type': 'application/json', 'User-Agent': 'Nexus-Client'},
        method='PUT'
    )
    try:
        with urllib.request.urlopen(req, timeout=6) as response:
            return json.loads(response.read().decode()), None
    except Exception as e:
        return None, str(e)

# Streamlit Caching for Read Queries (eliminates redundant DB & API latency)
@st.cache_data(ttl=120, show_spinner=False)
def get_cached_facets():
    return fetch_json("/products/facets") or {}

@st.cache_data(ttl=60, show_spinner=False)
def get_cached_products(category=None, q=None, min_rating=None, min_price=None, max_price=None, sort=None, in_stock=False):
    params = []
    if category and category != "All":
        params.append(f"category={urllib.parse.quote(category)}")
    if q:
        params.append(f"q={urllib.parse.quote(q)}")
    if min_rating and min_rating > 0:
        params.append(f"min_rating={min_rating}")
    if min_price is not None and min_price > 0:
        params.append(f"min_price={min_price}")
    if max_price is not None and max_price < 2000:
        params.append(f"max_price={max_price}")
    if sort:
        params.append(f"sort={sort}")
    if in_stock:
        params.append("in_stock=true")
    qs = "&".join(params)
    return fetch_json(f"/products?{qs}" if qs else "/products") or []

@st.cache_data(ttl=120, show_spinner=False)
def get_cached_product(pid):
    return fetch_json(f"/products/{pid}")

@st.cache_data(ttl=120, show_spinner=False)
def get_cached_similar(pid):
    return fetch_json(f"/products/{pid}/similar") or []


# ==============================================================================
# 5. SESSION STATE MANAGEMENT
# ==============================================================================
if 'cart' not in st.session_state:
    st.session_state.cart = {}  # {product_id: qty}
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = "All"
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'submitted_query' not in st.session_state:
    st.session_state.submitted_query = ""
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None
if 'checkout_step' not in st.session_state:
    st.session_state.checkout_step = 1
if 'selected_address_id' not in st.session_state:
    st.session_state.selected_address_id = None
if 'selected_address_text' not in st.session_state:
    st.session_state.selected_address_text = ""
if 'selected_payment_method' not in st.session_state:
    st.session_state.selected_payment_method = "Credit Card (Nexus Pay)"

# User state (defaults to Demo User ID 1)
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

def select_category_action(cat):
    st.session_state.selected_category = cat
    st.session_state.page = "Catalog"

def get_product_stock(prod):
    if not isinstance(prod, dict):
        return 0
    for key in ('stock', 'stockQuantity', 'quantity', 'inventory', 'stock_quantity'):
        if key in prod and prod[key] is not None:
            try:
                return int(prod[key])
            except (ValueError, TypeError):
                pass
    return 0

def render_stock_badge(stock):
    if stock <= 0:
        return "<span class='badge-stock-out'>❌ Sold Out</span>"
    elif stock <= 5:
        return f"<span class='badge-stock-low'>⚠️ Only {stock} left</span>"
    else:
        return f"<span class='badge-stock-in'>● In Stock ({stock})</span>"

def add_to_cart_action(pid, qty=1):
    prod = get_cached_product(pid)
    if not prod:
        st.error("Product not found.")
        return
    max_stock = get_product_stock(prod)
    if max_stock <= 0:
        st.error(f"'{prod['name']}' is currently sold out!")
        return
    current_qty = st.session_state.cart.get(pid, 0)
    if current_qty + qty > max_stock:
        st.error(f"Cannot add {qty} more. Only {max_stock} units available!")
    else:
        st.session_state.cart[pid] = current_qty + qty
        st.toast(f"🛒 Added {prod['name']} (Qty: {qty}) to cart!", icon="✅")

def render_product_card(prod, key_prefix="p"):
    stock_qty = get_product_stock(prod)
    stock_badge = render_stock_badge(stock_qty)
    
    avg_r = prod.get('avg_rating', 0.0)
    rev_count = prod.get('review_count', 0)
    rating_badge = f"<span class='badge-rating'>★ {avg_r:.1f} ({rev_count})</span>" if rev_count > 0 else "<span style='font-size: 10px; color: #94A3B8;'>Unrated</span>"

    attrs = prod.get('attributes', {})
    attr_summary = " • ".join([f"{v}" for k, v in list(attrs.items())[:2]]) if attrs else prod.get('category', '').capitalize()
    price_formatted = format_rupee(prod['price'])

    st.markdown(f"""
    <div class="nexus-product-card">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span class="badge-cat">{prod['category']}</span>
                {rating_badge}
            </div>
            <div class="nexus-product-img-wrap">
                <img src="{API_URL}/products/{prod['product_id']}/image" alt="{prod['name']}" loading="lazy"/>
            </div>
            <div class="nexus-product-attr">{attr_summary}</div>
            <div class="nexus-product-title" title="{prod['name']}">{prod['name']}</div>
            <div style="margin: 4px 0 6px 0;">{stock_badge}</div>
            <div class="nexus-product-price">{price_formatted}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if stock_qty > 0:
        if st.button("🛒 Add to Cart", key=f"{key_prefix}_add_{prod['product_id']}", use_container_width=True, type="primary"):
            add_to_cart_action(prod['product_id'], 1)
            st.rerun()
    else:
        st.button("Sold Out", key=f"{key_prefix}_sold_{prod['product_id']}", disabled=True, use_container_width=True)

    if st.button("View Details", key=f"{key_prefix}_det_{prod['product_id']}", use_container_width=True):
        st.session_state.selected_product = prod['product_id']
        set_page("Product")
        st.rerun()


# ==============================================================================
# 6. UNIFIED PERSISTENT TWO-ROW TOP NAVIGATION (FLIPKART STYLE)
# ==============================================================================
# Determine Current Delivery Address display
delivery_user = st.session_state.user
delivery_display_name = "Select Location"
delivery_address_line = "Add Address"
user_addresses = []

if delivery_user:
    user_addresses = fetch_json(f"/users/{delivery_user['id']}/addresses") or []
    if user_addresses:
        active_addr = None
        if st.session_state.selected_address_id:
            active_addr = next((a for a in user_addresses if a['id'] == st.session_state.selected_address_id), None)
        if not active_addr:
            active_addr = next((a for a in user_addresses if a.get('is_default')), user_addresses[0])
            st.session_state.selected_address_id = active_addr['id']
            st.session_state.selected_address_text = f"{active_addr['recipient_name']}, {active_addr['street']}, {active_addr['city']} {active_addr['postal_code']}"

        delivery_display_name = active_addr.get('recipient_name') or delivery_user['name']
        delivery_address_line = f"{active_addr.get('city', '')} {active_addr.get('postal_code', '')}".strip() or "Standard Address"
    else:
        delivery_display_name = delivery_user['name']
        delivery_address_line = "No address saved"

cart_item_count = sum(st.session_state.cart.values())

# Unified Single Navigation Container holding BOTH Row 1 and Row 2
navbar_container = st.container()
with navbar_container:
    st.markdown('<div id="nexus-navbar-root"></div>', unsafe_allow_html=True)

    # --- ROW 1: MAIN NAVIGATION ---
    r1_col_loc, r1_col_search, r1_col_btn, r1_col_act, r1_col_ord, r1_col_cart, r1_col_brand = st.columns(
        [2.2, 4.4, 0.6, 1.2, 1.1, 1.2, 1.3],
        gap="small"
    )

    # 1. Delivery Location Popover
    with r1_col_loc:
        if delivery_user and user_addresses:
            loc_btn_label = f"📍 {delivery_display_name[:10]} ({delivery_address_line[:12]})"
        elif delivery_user:
            loc_btn_label = f"📍 {delivery_user['name'][:10]} (No Address)"
        else:
            loc_btn_label = "📍 Select Delivery Location"

        with st.popover(loc_btn_label, use_container_width=True):
            st.markdown("<h4 style='margin: 0 0 6px 0; font-size: 15px;'>📍 Delivery Destination</h4>", unsafe_allow_html=True)
            if delivery_user:
                if user_addresses:
                    st.markdown("<p style='font-size: 12px; color: #687386; margin-bottom: 8px;'>Select saved address:</p>", unsafe_allow_html=True)
                    for addr in user_addresses:
                        is_current = (addr['id'] == st.session_state.selected_address_id)
                        btn_type = "primary" if is_current else "secondary"
                        tag = " (Default)" if addr.get('is_default') else ""
                        if st.button(
                            f"🏠 {addr['label']}{tag}: {addr['street']}, {addr['city']}",
                            key=f"nav_addr_pick_{addr['id']}",
                            type=btn_type,
                            use_container_width=True
                        ):
                            st.session_state.selected_address_id = addr['id']
                            st.session_state.selected_address_text = f"{addr['recipient_name']}, {addr['street']}, {addr['city']} {addr['postal_code']}"
                            st.rerun()
                else:
                    st.info("No addresses saved yet.")
                
                st.markdown("<hr style='margin: 8px 0;'/>", unsafe_allow_html=True)
                if st.button("Manage Address Book", key="nav_to_profile", use_container_width=True):
                    set_page("Profile")
                    st.rerun()
            else:
                st.warning("Please sign in to select saved delivery destinations.")
                if st.button("🔑 Sign In / Register", key="nav_loc_signin", type="primary", use_container_width=True):
                    set_page("Auth")
                    st.rerun()

    # 2. Main Product Search Input in the center, occupying largest available width
    with r1_col_search:
        search_val = st.text_input(
            "Search",
            value=st.session_state.submitted_query,
            placeholder="Search for products, brands and more (Press Enter)",
            label_visibility="collapsed",
            key="main_search_input"
        )
        if search_val != st.session_state.submitted_query:
            st.session_state.submitted_query = search_val.strip()
            set_page("Catalog")
            st.rerun()

    # 3. Search button adjacent to the search input
    with r1_col_btn:
        if st.session_state.submitted_query:
            if st.button("✕", key="btn_clear_search", use_container_width=True, help="Clear Search"):
                st.session_state.submitted_query = ""
                st.rerun()
        else:
            if st.button("🔍", key="btn_trigger_search", use_container_width=True, type="primary", help="Submit Search"):
                if search_val:
                    st.session_state.submitted_query = search_val.strip()
                set_page("Catalog")
                st.rerun()

    # 4. Account / Profile Dropdown
    with r1_col_act:
        act_label = f"👤 {delivery_user['name'].split()[0]}" if delivery_user else "👤 Account"
        with st.popover(act_label, use_container_width=True):
            if delivery_user:
                st.markdown(f"**👤 {delivery_user['name']}**")
                st.caption(f"{delivery_user['email']} • ID #{delivery_user['id']}")
                st.markdown("<hr style='margin: 6px 0;'/>", unsafe_allow_html=True)
                if st.button("📍 Saved Addresses", key="pop_prof", use_container_width=True):
                    set_page("Profile")
                    st.rerun()
                if st.button("📦 Order History", key="pop_ord", use_container_width=True):
                    set_page("Orders")
                    st.rerun()
                if st.button("📊 DB Telemetry", key="pop_db", use_container_width=True):
                    set_page("Databases")
                    st.rerun()
                if st.button("🚪 Sign Out", key="pop_signout", use_container_width=True):
                    st.session_state.user = None
                    st.session_state.cart = {}
                    st.session_state.selected_address_id = None
                    st.rerun()
            else:
                st.markdown("#### Customer Access")
                if st.button("⚡ 1-Click Demo Login", key="pop_demo_login", type="primary", use_container_width=True):
                    res, err = post_json("/auth/login", {"email": "demo@nexus.com", "password": "demo123"})
                    if res and "user" in res:
                        st.session_state.user = res["user"]
                        st.toast("⚡ Signed in as Demo User!", icon="✅")
                        st.rerun()
                if st.button("🔑 Sign In / Register", key="pop_auth_page", use_container_width=True):
                    set_page("Auth")
                    st.rerun()

    # 5. Order History Icon & Label
    with r1_col_ord:
        is_ord_active = (st.session_state.page == "Orders")
        ord_btn_type = "primary" if is_ord_active else "secondary"
        if st.button("📦 Orders", key="top_orders_btn", use_container_width=True, type=ord_btn_type):
            set_page("Orders")
            st.rerun()

    # 6. Shopping Cart Icon & Live Item Count
    with r1_col_cart:
        is_cart_active = (st.session_state.page == "Cart")
        cart_btn_type = "primary" if is_cart_active else "secondary"
        cart_label = f"🛒 Cart ({cart_item_count})"
        if st.button(cart_label, key="top_cart_btn", use_container_width=True, type=cart_btn_type):
            set_page("Cart")
            st.rerun()

    # 7. NEXUS Logo/Brand on Far Right
    with r1_col_brand:
        if st.button("⚡ NEXUS", key="nav_brand_home", use_container_width=True):
            st.session_state.selected_category = "All"
            st.session_state.submitted_query = ""
            set_page("Home")
            st.rerun()

    # Subtle horizontal divider between Row 1 and Row 2 inside the navbar container
    st.markdown('<div class="nexus-navbar-divider"></div>', unsafe_allow_html=True)

    # --- ROW 2: CATEGORY NAVIGATION STRIP ---
    cat_defs = [
        ("All", "🌐", "All Categories"),
        ("laptops", "💻", "Laptops"),
        ("shoes", "👟", "Shoes"),
        ("books", "📚", "Books"),
        ("phones", "📱", "Phones")
    ]

    st.markdown('<div class="nexus-cat-strip">', unsafe_allow_html=True)
    cat_cols = st.columns([1.3, 1.3, 1.3, 1.3, 1.3, 3.5], gap="small")

    for idx, (cat_slug, icon, label) in enumerate(cat_defs):
        with cat_cols[idx]:
            is_selected = (st.session_state.selected_category == cat_slug and st.session_state.page == "Catalog")
            c_type = "primary" if is_selected else "secondary"
            if st.button(f"{icon} {label}", key=f"cat_nav_{cat_slug}", use_container_width=True, type=c_type):
                select_category_action(cat_slug)
                st.rerun()

    with cat_cols[5]:
        if st.session_state.page == "Home":
            st.markdown(
                f"<div style='font-size: 11px; color: #687386; text-align: right; padding-top: 8px;'>"
                f"Welcome to <strong style='color: #2874F0;'>NEXUS Store</strong>"
                f"</div>",
                unsafe_allow_html=True
            )
        else:
            active_cat_label = next((l for s, i, l in cat_defs if s == st.session_state.selected_category), "All Categories")
            query_snippet = f" • Query: <em>'{st.session_state.submitted_query}'</em>" if st.session_state.submitted_query else ""
            st.markdown(
                f"<div style='font-size: 11px; color: #687386; text-align: right; padding-top: 8px;'>"
                f"Browsing: <strong style='color: #172033;'>{active_cat_label}</strong>"
                f"{query_snippet}"
                f"</div>",
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# VIEW 0: HOMEPAGE (LANDING PAGE)
# ==============================================================================
if st.session_state.page == "Home":
    all_cached_products = get_cached_products() or []

    # 1. HERO SECTION
    hero_col_text, hero_col_visual = st.columns([1.6, 1.0], gap="large")
    with hero_col_text:
        st.markdown("""
        <div class="nexus-home-hero">
            <span class="nexus-hero-badge">✦ Official Multipurpose Store</span>
            <h1 class="nexus-hero-title">Next-Gen Electronics & Essentials</h1>
            <p class="nexus-hero-sub">
                Explore curated computing workstations, flagship mobile smartphones, 
                performance athletic footwear, and timeless literature — all backed by 
                verified real-time stock and instant ACID checkout.
            </p>
        </div>
        """, unsafe_allow_html=True)

        btn_c1, btn_c2 = st.columns([1.2, 1.4], gap="small")
        with btn_c1:
            if st.button("🛍️ Shop Now", key="hero_shop_now", type="primary", use_container_width=True):
                select_category_action("All")
                st.rerun()
        with btn_c2:
            if st.button("⚡ Browse Laptops", key="hero_shop_laptops", use_container_width=True):
                select_category_action("laptops")
                st.rerun()

    with hero_col_visual:
        featured_lead = next((p for p in all_cached_products if p.get('product_id') == 'P0014'), all_cached_products[0] if all_cached_products else None)
        lead_img = f"{API_URL}/products/{featured_lead['product_id']}/image" if featured_lead else ""
        lead_name = featured_lead['name'] if featured_lead else "Featured Flagship"
        lead_price = format_rupee(featured_lead['price']) if featured_lead else ""
        lead_stock = get_product_stock(featured_lead) if featured_lead else 0
        lead_stock_badge = render_stock_badge(lead_stock)

        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid var(--nexus-border); border-radius: 12px; padding: 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.04); text-align: center;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span class="badge-cat">Featured Hardware</span>
                <span style="font-size: 11px; font-weight: 700; color: #16865C; background: #EDFBF4; padding: 2px 8px; border-radius: 4px;">Verified Quality</span>
            </div>
            <div style="background: var(--nexus-bg-surface); border-radius: 8px; padding: 16px; margin: 8px 0 12px 0; min-height: 160px; display: flex; align-items: center; justify-content: center;">
                <img src="{lead_img}" alt="{lead_name}" style="max-height: 140px; width: auto; object-fit: contain;"/>
            </div>
            <div style="font-size: 15px; font-weight: 700; color: #172033; margin-bottom: 4px;">{lead_name}</div>
            <div style="font-size: 12px; color: #687386; margin-bottom: 6px;">{lead_stock_badge}</div>
            <div style="font-size: 18px; font-weight: 800; color: #2874F0;">{lead_price}</div>
        </div>
        """, unsafe_allow_html=True)
        if featured_lead:
            if st.button("View Featured Specs", key="hero_view_featured_lead", use_container_width=True):
                st.session_state.selected_product = featured_lead['product_id']
                set_page("Product")
                st.rerun()

    st.markdown("<hr style='margin: 24px 0 20px 0; border: none; border-top: 1px solid #E5E9F0;'/>", unsafe_allow_html=True)

    # 2. SHOP BY CATEGORY SECTION
    st.markdown("""
    <div class="nexus-section-header">
        <div>
            <h2 class="nexus-section-title">Shop by Category</h2>
            <p class="nexus-section-sub">Browse authentic departments with targeted technical filtering and real-time stock</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cat_metadata = [
        {
            "slug": "laptops",
            "icon": "💻",
            "title": "Laptops",
            "desc": "High-performance ultrabooks, mobile workstations & gaming hardware",
            "count": len([p for p in all_cached_products if p.get('category') == 'laptops'])
        },
        {
            "slug": "phones",
            "icon": "📱",
            "title": "Phones",
            "desc": "Flagship 5G smartphones, OLED displays & advanced camera systems",
            "count": len([p for p in all_cached_products if p.get('category') == 'phones'])
        },
        {
            "slug": "shoes",
            "icon": "👟",
            "title": "Shoes",
            "desc": "Athletic running trainers, street sneakers & durable footwear",
            "count": len([p for p in all_cached_products if p.get('category') == 'shoes'])
        },
        {
            "slug": "books",
            "icon": "📚",
            "title": "Books",
            "desc": "Science fiction masterpieces, technical guides & bestselling titles",
            "count": len([p for p in all_cached_products if p.get('category') == 'books'])
        }
    ]

    cat_cols_ui = st.columns(4, gap="medium")
    for idx, cinfo in enumerate(cat_metadata):
        with cat_cols_ui[idx]:
            st.markdown(f"""
            <div class="nexus-cat-card">
                <div>
                    <span class="nexus-cat-icon">{cinfo['icon']}</span>
                    <div class="nexus-cat-title">{cinfo['title']}</div>
                    <div class="nexus-cat-desc">{cinfo['desc']}</div>
                    <div style="font-size: 11px; color: #2874F0; font-weight: 600; margin-bottom: 12px;">{cinfo['count']} Products Available</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Explore {cinfo['title']} →", key=f"home_cat_btn_{cinfo['slug']}", use_container_width=True):
                select_category_action(cinfo['slug'])
                st.rerun()

    st.markdown("<hr style='margin: 28px 0 20px 0; border: none; border-top: 1px solid #E5E9F0;'/>", unsafe_allow_html=True)

    # 3. FEATURED PRODUCTS (1 from each department with live stock)
    st.markdown("""
    <div class="nexus-section-header">
        <div>
            <h2 class="nexus-section-title">⭐ Featured Products</h2>
            <p class="nexus-section-sub">Hand-picked department highlights across verified in-stock inventory</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    featured_selection = []
    for cinfo in cat_metadata:
        cat_in_stock = [p for p in all_cached_products if p.get('category') == cinfo['slug'] and get_product_stock(p) > 0]
        if cat_in_stock:
            featured_selection.append(cat_in_stock[0])

    if len(featured_selection) < 4:
        for p in all_cached_products:
            if p not in featured_selection and get_product_stock(p) > 0:
                featured_selection.append(p)
            if len(featured_selection) == 4:
                break

    feat_cols = st.columns(4, gap="medium")
    for idx, prod in enumerate(featured_selection[:4]):
        with feat_cols[idx]:
            render_product_card(prod, key_prefix="home_feat")

    st.markdown("<hr style='margin: 28px 0 20px 0; border: none; border-top: 1px solid #E5E9F0;'/>", unsafe_allow_html=True)

    # 4. POPULAR / HIGHEST RATED PRODUCTS (Real ratings & reviews from Mongo database)
    st.markdown("""
    <div class="nexus-section-header">
        <div>
            <h2 class="nexus-section-title">🔥 Customer Top Favorites</h2>
            <p class="nexus-section-sub">Highest rated items based on verified customer feedback and real review scores</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    top_rated_selection = sorted(
        [p for p in all_cached_products if p.get('avg_rating', 0) >= 4.0 and get_product_stock(p) > 0],
        key=lambda x: (x.get('avg_rating', 0.0), x.get('review_count', 0)),
        reverse=True
    )[:4]

    pop_cols = st.columns(4, gap="medium")
    for idx, prod in enumerate(top_rated_selection):
        with pop_cols[idx]:
            render_product_card(prod, key_prefix="home_pop")

    # 5. FOOTER SECTION
    st.markdown("""
    <div class="nexus-footer">
        <div style="display: grid; grid-template-columns: 1.5fr 1fr 1fr 1.2fr; gap: 24px;">
            <div>
                <div class="nexus-footer-brand">⚡ NEXUS E-COMMERCE</div>
                <p class="nexus-footer-sub">
                    High-performance multipurpose e-commerce architecture powered by polyglot databases.
                    Real-time transactional inventory, rich MongoDB catalog queries, and ChromaDB vector search.
                </p>
            </div>
            <div>
                <div class="nexus-footer-heading">Departments</div>
                <ul class="nexus-footer-links">
                    <li>💻 Laptops & Workstations</li>
                    <li>📱 Smartphones & Mobiles</li>
                    <li>👟 Footwear & Athletic</li>
                    <li>📚 Bestselling Literature</li>
                </ul>
            </div>
            <div>
                <div class="nexus-footer-heading">Customer Center</div>
                <ul class="nexus-footer-links">
                    <li>📦 Order History & Invoices</li>
                    <li>📍 Saved Address Manager</li>
                    <li>🛒 Shopping Cart & Checkout</li>
                    <li>🔒 ACID Guarantee</li>
                </ul>
            </div>
            <div>
                <div class="nexus-footer-heading">Architecture</div>
                <ul class="nexus-footer-links">
                    <li>⚡ FastAPI Microservice API</li>
                    <li>🐘 PostgreSQL Connection Pool</li>
                    <li>🍃 MongoDB Catalog & Reviews</li>
                    <li>🔍 ChromaDB Vector Engine</li>
                </ul>
            </div>
        </div>
        <div class="nexus-footer-bottom">
            <span>© 2026 NEXUS Multipurpose Platform. All rights reserved. Prices displayed in Indian Rupees (₹).</span>
            <span>⚡ High Performance Desktop Edition</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# VIEW 1: CATEGORY LISTING PAGE (PRODUCT GRID & LEFT FACET SIDEBAR)
# ==============================================================================
elif st.session_state.page == "Catalog":
    # 2-Column Desktop Shopping Layout: Left Facet Sidebar & Right Product Grid
    col_filters, col_main_grid = st.columns([1, 3.4], gap="large")

    # --------------------------------------------------------------------------
    # LEFT FACET SIDEBAR (Visible only on product catalog/search)
    # --------------------------------------------------------------------------
    with col_filters:
        st.markdown("""
        <div class="nexus-facet-box">
            <div class="nexus-facet-title">
                <span>Filters</span>
                <span style="font-size: 10px; color: #2874F0; cursor: pointer;">ACID Catalog</span>
            </div>
        """, unsafe_allow_html=True)

        # 1. Price Range Filter (in Indian Rupees ₹)
        st.markdown("<div style='font-size: 12px; font-weight: 600; margin-bottom: 4px;'>Price Range (₹)</div>", unsafe_allow_html=True)
        price_range = st.slider(
            "Price Range",
            min_value=0,
            max_value=2000,
            value=(0, 2000),
            step=50,
            format="₹%d",
            label_visibility="collapsed",
            key="cat_filter_price_slider"
        )
        st.markdown(
            f"<div style='font-size: 11px; color: #687386; margin-bottom: 12px;'>"
            f"Range: <strong style='color: #172033;'>{format_rupee(price_range[0])} – {format_rupee(price_range[1])}</strong>"
            f"</div>",
            unsafe_allow_html=True
        )

        st.markdown("<hr style='margin: 8px 0 12px 0; border: none; border-top: 1px solid #E5E9F0;'/>", unsafe_allow_html=True)

        # 2. Availability Filter
        st.markdown("<div style='font-size: 12px; font-weight: 600; margin-bottom: 4px;'>Availability</div>", unsafe_allow_html=True)
        in_stock_only = st.checkbox("⚡ In Stock Only", value=False, key="cat_filter_in_stock")

        st.markdown("<hr style='margin: 8px 0 12px 0; border: none; border-top: 1px solid #E5E9F0;'/>", unsafe_allow_html=True)

        # 3. Minimum Rating Filter
        st.markdown("<div style='font-size: 12px; font-weight: 600; margin-bottom: 4px;'>Customer Rating</div>", unsafe_allow_html=True)
        rating_choice = st.selectbox(
            "Customer Rating",
            ["All Ratings", "4★ & above", "3★ & above"],
            label_visibility="collapsed",
            key="cat_filter_rating"
        )
        min_rating_val = 4.0 if rating_choice == "4★ & above" else (3.0 if rating_choice == "3★ & above" else None)

        st.markdown("<hr style='margin: 8px 0 12px 0; border: none; border-top: 1px solid #E5E9F0;'/>", unsafe_allow_html=True)

        # 4. Category-Specific Filters (Derived from actual underlying attributes)
        selected_cat = st.session_state.selected_category
        filter_attr_1 = None
        filter_attr_2 = None

        if selected_cat == "laptops":
            st.markdown("<div style='font-size: 12px; font-weight: 600; margin-bottom: 4px;'>Memory (RAM)</div>", unsafe_allow_html=True)
            filter_attr_1 = st.selectbox("RAM", ["All", "8GB", "16GB", "32GB"], key="filter_laptop_ram", label_visibility="collapsed")
            st.markdown("<div style='font-size: 12px; font-weight: 600; margin: 8px 0 4px 0;'>Processor (CPU)</div>", unsafe_allow_html=True)
            filter_attr_2 = st.selectbox("CPU", ["All", "i5", "i7", "M1", "M2"], key="filter_laptop_cpu", label_visibility="collapsed")

        elif selected_cat == "shoes":
            st.markdown("<div style='font-size: 12px; font-weight: 600; margin-bottom: 4px;'>Shoe Size</div>", unsafe_allow_html=True)
            filter_attr_1 = st.selectbox("Size", ["All", "6", "7", "8", "9", "10", "11", "12"], key="filter_shoe_size", label_visibility="collapsed")
            st.markdown("<div style='font-size: 12px; font-weight: 600; margin: 8px 0 4px 0;'>Color</div>", unsafe_allow_html=True)
            filter_attr_2 = st.selectbox("Color", ["All", "Black", "White", "Navy", "Red", "Grey", "Olive", "Brown", "Blue"], key="filter_shoe_color", label_visibility="collapsed")

        elif selected_cat == "phones":
            st.markdown("<div style='font-size: 12px; font-weight: 600; margin-bottom: 4px;'>Storage Capacity</div>", unsafe_allow_html=True)
            filter_attr_1 = st.selectbox("Storage", ["All", "128GB", "256GB", "512GB"], key="filter_phone_storage", label_visibility="collapsed")
            st.markdown("<div style='font-size: 12px; font-weight: 600; margin: 8px 0 4px 0;'>Camera</div>", unsafe_allow_html=True)
            filter_attr_2 = st.selectbox("Camera", ["All", "12MP", "48MP", "108MP"], key="filter_phone_camera", label_visibility="collapsed")

        elif selected_cat == "books":
            st.markdown("<div style='font-size: 12px; font-weight: 600; margin-bottom: 4px;'>Length</div>", unsafe_allow_html=True)
            filter_attr_1 = st.selectbox("Pages", ["All", "Under 300 pages", "300–600 pages", "600+ pages"], key="filter_book_pages", label_visibility="collapsed")

        # Clear Filters Action
        st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
        if st.button("Reset All Filters", key="btn_reset_filters", use_container_width=True):
            st.session_state.submitted_query = ""
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # MAIN PRODUCT CATALOG & TOOLBAR
    # --------------------------------------------------------------------------
    with col_main_grid:
        # Fetch matching products with cache
        raw_products = get_cached_products(
            category=selected_cat,
            q=st.session_state.submitted_query,
            min_rating=min_rating_val,
            min_price=price_range[0],
            max_price=price_range[1],
            in_stock=in_stock_only
        )

        # Apply category-specific attribute filtering on the loaded set
        products = []
        for p in raw_products:
            attrs = p.get('attributes', {})
            include = True
            if selected_cat == "laptops":
                if filter_attr_1 and filter_attr_1 != "All" and attrs.get('ram') != filter_attr_1:
                    include = False
                if filter_attr_2 and filter_attr_2 != "All" and attrs.get('cpu') != filter_attr_2:
                    include = False
            elif selected_cat == "shoes":
                if filter_attr_1 and filter_attr_1 != "All" and str(attrs.get('size')) != str(filter_attr_1):
                    include = False
                if filter_attr_2 and filter_attr_2 != "All" and attrs.get('color') != filter_attr_2:
                    include = False
            elif selected_cat == "phones":
                if filter_attr_1 and filter_attr_1 != "All" and attrs.get('storage') != filter_attr_1:
                    include = False
                if filter_attr_2 and filter_attr_2 != "All" and attrs.get('camera') != filter_attr_2:
                    include = False
            elif selected_cat == "books":
                pages = attrs.get('pages', 0)
                if filter_attr_1 == "Under 300 pages" and pages >= 300:
                    include = False
                elif filter_attr_1 == "300–600 pages" and not (300 <= pages <= 600):
                    include = False
                elif filter_attr_1 == "600+ pages" and pages <= 600:
                    include = False
            
            if include:
                products.append(p)

        # PRODUCT TOOLBAR (Clean Flipkart/Amazon Header)
        tb_col_left, tb_col_sort = st.columns([3, 1.2], gap="medium")
        
        with tb_col_left:
            display_title = "All Products" if selected_cat == "All" else selected_cat.capitalize()
            query_sub = f" for '{st.session_state.submitted_query}'" if st.session_state.submitted_query else ""
            st.markdown(
                f"<div style='margin-bottom: 12px;'>"
                f"<h2 style='font-size: 22px; font-weight: 700; margin: 0;'>{display_title}{query_sub}</h2>"
                f"<span style='font-size: 12px; color: #687386;'>Showing <strong>{len(products)}</strong> results</span>"
                f"</div>",
                unsafe_allow_html=True
            )

        with tb_col_sort:
            sort_selection = st.selectbox(
                "Sort by",
                ["Relevance", "Price: Low to High", "Price: High to Low", "Customer Rating", "In-Stock First"],
                label_visibility="collapsed",
                key="cat_sort_select"
            )

        # Apply sorting
        if sort_selection == "Price: Low to High":
            products = sorted(products, key=lambda x: float(x.get('price', 0)))
        elif sort_selection == "Price: High to Low":
            products = sorted(products, key=lambda x: float(x.get('price', 0)), reverse=True)
        elif sort_selection == "Customer Rating":
            products = sorted(products, key=lambda x: float(x.get('avg_rating', 0.0)), reverse=True)
        elif sort_selection == "In-Stock First":
            products = sorted(products, key=lambda x: get_product_stock(x), reverse=True)

        # EMPTY STATE
        if not products:
            st.markdown("""
            <div style="background: #FFFFFF; border: 1px solid #E5E9F0; border-radius: 8px; padding: 48px; text-align: center; margin-top: 12px;">
                <div style="font-size: 36px; margin-bottom: 8px;">🔍</div>
                <h3 style="font-size: 18px; font-weight: 700; color: #172033; margin: 0 0 6px 0;">No matching products found</h3>
                <p style="font-size: 13px; color: #687386; margin: 0 0 16px 0;">Try clearing your filters or search keywords.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Clear All Filters", key="empty_reset_btn", type="primary"):
                st.session_state.submitted_query = ""
                st.rerun()
        else:
            # 3-COLUMN DESKTOP PRODUCT GRID
            grid_cols = st.columns(3, gap="medium")
            for idx, prod in enumerate(products):
                col_idx = idx % 3
                with grid_cols[col_idx]:
                    render_product_card(prod, key_prefix="pgrid")
                    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# VIEW 2: PRODUCT DETAILS PAGE (FULL WIDTH — NO FACET SIDEBAR)
# ==============================================================================
elif st.session_state.page == "Product":
    pid = st.session_state.selected_product
    if not pid:
        set_page("Catalog")
        st.rerun()
    prod = get_cached_product(pid)
    if not prod:
        st.error("Product specifications could not be loaded.")
        if st.button("← Return to Products"):
            set_page("Catalog")
            st.rerun()
    else:
        # Breadcrumbs
        st.markdown(f"""
        <nav style="font-size: 12px; color: #687386; margin-bottom: 14px;">
            <span>Catalog</span> / <span style="text-transform: capitalize;">{prod['category']}</span> / <strong style="color: #172033;">{prod['name']}</strong>
        </nav>
        """, unsafe_allow_html=True)

        if st.button("← Return to Category Listing", key="det_back_catalog_btn"):
            set_page("Catalog")
            st.rerun()

        # Two-Column Product Overview
        det_img_col, det_info_col = st.columns([5, 6], gap="large")

        with det_img_col:
            st.markdown(f"""
            <div style="background: #FFFFFF; border: 1px solid #E5E9F0; border-radius: 8px; padding: 24px; text-align: center; margin-bottom: 16px;">
                <img src="{API_URL}/products/{pid}/image" style="max-height: 320px; width: 100%; object-fit: contain;" alt="{prod['name']}"/>
            </div>
            """, unsafe_allow_html=True)

            # Quality Trust Chips
            st.markdown("""
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                <div style="background: #FFFFFF; border: 1px solid #E5E9F0; border-radius: 6px; padding: 12px; font-size: 11px;">
                    <strong style="color: #172033; display: block; margin-bottom: 2px;">⚡ Verified Genuine</strong>
                    <span style="color: #687386;">100% authentic product warranty.</span>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E5E9F0; border-radius: 6px; padding: 12px; font-size: 11px;">
                    <strong style="color: #172033; display: block; margin-bottom: 2px;">🚚 Free Dispatch</strong>
                    <span style="color: #687386;">Complimentary priority courier.</span>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E5E9F0; border-radius: 6px; padding: 12px; font-size: 11px;">
                    <strong style="color: #172033; display: block; margin-bottom: 2px;">🛡️ 30-Day Return</strong>
                    <span style="color: #687386;">Hassle-free replacement policy.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with det_info_col:
            stock = get_product_stock(prod)
            stock_badge = render_stock_badge(stock)
            price_inr = format_rupee(prod['price'])

            avg_r = prod.get('avg_rating', 0.0)
            rev_count = prod.get('review_count', 0)
            rating_sub = f"★ {avg_r:.1f} • {rev_count} verified customer ratings" if rev_count > 0 else "★ Unrated"

            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span class="badge-cat">{prod['category']}</span>
                {stock_badge}
            </div>
            <h1 style="font-size: 26px; font-weight: 700; color: #172033; margin: 0 0 6px 0; line-height: 1.25;">{prod['name']}</h1>
            <div style="font-size: 12px; color: #687386; margin-bottom: 16px;">{rating_sub} &nbsp;•&nbsp; SKU: <strong style="color: #172033;">{prod['product_id']}</strong></div>
            
            <div style="background: #FFFFFF; border: 1px solid #E5E9F0; border-radius: 6px; padding: 16px; margin-bottom: 16px;">
                <div style="font-size: 28px; font-weight: 800; color: #172033;">{price_inr}</div>
                <div style="font-size: 11px; color: #687386; margin-top: 2px;">Inclusive of all applicable taxes. Free courier delivery.</div>
            </div>

            <p style="font-size: 14px; color: #475569; line-height: 1.6; margin-bottom: 20px;">{prod['description']}</p>
            """, unsafe_allow_html=True)

            # Dynamic Attributes Display
            attrs = prod.get('attributes', {})
            if attrs:
                st.markdown("<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #687386; margin-bottom: 8px;'>Specifications</div>", unsafe_allow_html=True)
                chips = "".join([
                    f"<div style='background: #F8FAFC; border: 1px solid #E5E9F0; border-radius: 6px; padding: 6px 12px; margin-right: 8px; margin-bottom: 8px; display: inline-block;'>"
                    f"<span style='font-size: 10px; color: #687386; text-transform: uppercase; font-weight: 700; display: block;'>{k}</span>"
                    f"<span style='font-size: 13px; font-weight: 700; color: #172033;'>{v}</span></div>"
                    for k, v in attrs.items()
                ])
                st.markdown(f"<div style='display: flex; flex-wrap: wrap; margin-bottom: 20px;'>{chips}</div>", unsafe_allow_html=True)

            # Purchase Quantity & Action Buttons
            q_col, btn_add_col, btn_buy_col = st.columns([1.5, 2.5, 2.5], gap="small")
            with q_col:
                det_qty = st.number_input("Qty", min_value=1, max_value=max(1, stock), value=1, key="det_qty_input", disabled=(stock <= 0))
            with btn_add_col:
                if stock > 0:
                    if st.button("🛒 Add to Cart", key="det_add_cart_btn", use_container_width=True, type="primary"):
                        add_to_cart_action(pid, det_qty)
                        st.rerun()
                else:
                    st.button("Sold Out", key="det_sold_btn", disabled=True, use_container_width=True)
            with btn_buy_col:
                if stock > 0:
                    if st.button("⚡ Buy Now", key="det_buy_now_btn", use_container_width=True):
                        add_to_cart_action(pid, det_qty)
                        set_page("Cart")
                        st.rerun()
                else:
                    st.button("Unavailable", key="det_unavail_btn", disabled=True, use_container_width=True)

        # ChromaDB AI Similar Products Recommendations
        st.markdown("<h3 style='margin: 40px 0 16px 0; font-size: 18px;'>Similar Products You May Like</h3>", unsafe_allow_html=True)
        similar_prods = get_cached_similar(pid)
        if similar_prods:
            sim_cols = st.columns(min(len(similar_prods), 5), gap="medium")
            for i, sim in enumerate(similar_prods[:5]):
                with sim_cols[i]:
                    st.markdown(f"""
                    <div class="nexus-product-card" style="padding: 10px;">
                        <div class="nexus-product-img-wrap" style="min-height: 110px;">
                            <img src="{API_URL}/products/{sim['product_id']}/image" style="max-height: 90px;"/>
                        </div>
                        <div style="font-size: 13px; font-weight: 700; color: #172033; margin: 4px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{sim['name']}</div>
                        <div style="font-size: 15px; font-weight: 800; color: #172033; margin-bottom: 8px;">{format_rupee(sim['price'])}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("View", key=f"sim_view_{sim['product_id']}", use_container_width=True):
                        st.session_state.selected_product = sim['product_id']
                        st.rerun()


# ==============================================================================
# VIEW 3: SHOPPING CART & 4-STEP CHECKOUT (NO FACET SIDEBAR)
# ==============================================================================
elif st.session_state.page == "Cart":
    # Step 4: Order Confirmed
    if st.session_state.get('checkout_step') == 4:
        last_id = st.session_state.get('last_order_id', 'N/A')
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #16865C; border-radius: 8px; padding: 48px; text-align: center; margin-bottom: 24px;">
            <div style="font-size: 48px; margin-bottom: 12px;">✅</div>
            <div style="display: inline-block; background: #EDFBF4; color: #16865C; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 4px; text-transform: uppercase; margin-bottom: 12px; letter-spacing: 0.04em;">
                Transaction Approved • ACID Lock Executed
            </div>
            <h2 style="font-size: 26px; font-weight: 800; color: #172033; margin: 0 0 8px 0;">Order #{last_id} Confirmed!</h2>
            <p style="font-size: 13px; color: #687386; max-width: 540px; margin: 0 auto 20px auto; line-height: 1.6;">
                Thank you for shopping with NEXUS. Inventory was reserved atomically via PostgreSQL row-level locks to guarantee zero overselling.
            </p>
            <div style="background: #F8FAFC; border: 1px solid #E5E9F0; border-radius: 6px; padding: 14px; display: inline-block; text-align: left; font-size: 12px; color: #172033; margin-bottom: 20px;">
                <div>📍 <strong>Shipping Destination:</strong> {st.session_state.get('selected_address_text', 'Default Registered Address')}</div>
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
        <div style="background: #FFFFFF; border: 1px solid #E5E9F0; border-radius: 8px; padding: 56px; text-align: center; margin-bottom: 24px;">
            <div style="font-size: 48px; margin-bottom: 12px;">🛒</div>
            <h3 style="font-size: 22px; font-weight: 700; color: #172033; margin-bottom: 6px;">Your Shopping Cart is Empty</h3>
            <p style="font-size: 13px; color: #687386; margin-bottom: 20px;">Explore our categories to add products to your cart.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🛍️ Browse Products Now", type="primary", use_container_width=True):
            set_page("Catalog")
            st.rerun()

    # Active Cart & Checkout Steps
    else:
        # Precompute Subtotal in Indian Rupees
        subtotal = 0.0
        items_payload = []
        cart_items_data = []

        for pid, qty in list(st.session_state.cart.items()):
            prod = get_cached_product(pid)
            if prod:
                line_total = float(prod['price']) * qty
                subtotal += line_total
                p_stock = get_product_stock(prod)
                items_payload.append({"product_id": pid, "qty": qty})
                cart_items_data.append({
                    "product_id": pid, "name": prod['name'], "price": prod['price'],
                    "qty": qty, "total": line_total, "stock": p_stock
                })

        free_shipping_threshold = 150.0
        shipping = 0.0 if subtotal >= free_shipping_threshold else 15.0
        tax = round(subtotal * 0.08, 2)
        grand_total = round(subtotal + shipping + tax, 2)
        pct_free = min(100, int((subtotal / free_shipping_threshold) * 100))

        # Free Shipping Threshold Banner in Indian Rupees
        st.markdown(f"""
        <div class="shipping-progress-banner">
            <div>
                <strong style="color: #172033; font-size: 13px;">
                    {'✓ You qualify for Free Next-Day Courier Delivery!' if shipping == 0 else f'Add {format_rupee(free_shipping_threshold - subtotal)} more to unlock Free Delivery!'}
                </strong>
                <div style="font-size: 11px; color: #687386; margin-top: 2px;">Orders over {format_rupee(free_shipping_threshold)} qualify for free priority dispatch.</div>
            </div>
            <div style="width: 220px;">
                <div style="display: flex; justify-content: space-between; font-size: 10px; font-weight: 700; color: #687386;">
                    <span>DELIVERY PROGRESS</span>
                    <span style="color: #2874F0;">{pct_free}%</span>
                </div>
                <div class="progress-bar-track">
                    <div class="progress-bar-thumb" style="width: {pct_free}%;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Checkout Step Tabs
        s_c1, s_c2, s_c3 = st.columns(3, gap="small")
        with s_c1:
            t1_type = "primary" if st.session_state.checkout_step == 1 else "secondary"
            if st.button(f"1️⃣ Review Cart ({sum(st.session_state.cart.values())})", key="chk_tab_1", use_container_width=True, type=t1_type):
                st.session_state.checkout_step = 1
                st.rerun()
        with s_c2:
            t2_type = "primary" if st.session_state.checkout_step == 2 else "secondary"
            if st.button("2️⃣ Delivery Address", key="chk_tab_2", use_container_width=True, type=t2_type):
                st.session_state.checkout_step = 2
                st.rerun()
        with s_c3:
            t3_type = "primary" if st.session_state.checkout_step == 3 else "secondary"
            if st.button("3️⃣ Payment & Place Order", key="chk_tab_3", use_container_width=True, type=t3_type):
                st.session_state.checkout_step = 3
                st.rerun()

        st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

        # STEP 1: REVIEW ITEMS
        if st.session_state.checkout_step == 1:
            col_items, col_sum = st.columns([7, 5], gap="large")
            with col_items:
                st.markdown("<h4 style='font-size: 16px; margin-bottom: 12px;'>Cart Items</h4>", unsafe_allow_html=True)
                for item in cart_items_data:
                    pid = item['product_id']
                    item_stock = item['stock']
                    stock_pill = render_stock_badge(item_stock)
                    sold_out_warn = "<div style='color: #DC4545; font-size: 11px; font-weight: 600; margin-top: 4px;'>⚠️ Currently sold out. Please remove this item to proceed.</div>" if item_stock <= 0 else ""
                    
                    st.markdown(f"""
                    <div style="background: #FFFFFF; border: 1px solid #E5E9F0; border-radius: 6px; padding: 12px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: baseline;">
                            <strong style="font-size: 14px; color: #172033;">{item['name']}</strong>
                            <span style="font-size: 16px; font-weight: 800; color: #172033;">{format_rupee(item['total'])}</span>
                        </div>
                        <div style="font-size: 11px; color: #687386; display: flex; align-items: center; gap: 8px; margin-top: 4px;">
                            <span>Unit: {format_rupee(item['price'])}</span>
                            <span>•</span>
                            {stock_pill}
                        </div>
                        {sold_out_warn}
                    </div>
                    """, unsafe_allow_html=True)

                    ci_img, ci_qty, ci_del = st.columns([1.5, 3.5, 2], gap="small")
                    with ci_img:
                        st.image(f"{API_URL}/products/{pid}/image", width=80)
                    with ci_qty:
                        new_q = st.number_input("Qty", min_value=1, max_value=max(1, item_stock), value=min(item['qty'], max(1, item_stock)), key=f"cart_qty_{pid}", disabled=(item_stock <= 0))
                        if new_q != item['qty']:
                            st.session_state.cart[pid] = new_q
                            st.rerun()
                    with ci_del:
                        st.markdown("<div style='padding-top: 24px;'></div>", unsafe_allow_html=True)
                        if st.button("Remove", key=f"cart_del_{pid}", use_container_width=True):
                            del st.session_state.cart[pid]
                            st.rerun()
                    st.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid #E5E9F0;'/>", unsafe_allow_html=True)

                c_cont, c_clr = st.columns([2, 1], gap="small")
                with c_cont:
                    if st.button("← Add More Products", use_container_width=True):
                        set_page("Catalog")
                        st.rerun()
                with c_clr:
                    if st.button("Clear Cart", use_container_width=True):
                        st.session_state.cart = {}
                        st.rerun()

            with col_sum:
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 1px solid #E5E9F0; border-radius: 8px; padding: 20px;">
                    <h4 style="font-size: 16px; margin: 0 0 14px 0; color: #172033;">Price Details</h4>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 8px;">
                        <span style="color: #687386;">Price ({sum(st.session_state.cart.values())} items)</span>
                        <strong style="color: #172033;">{format_rupee(subtotal)}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 8px;">
                        <span style="color: #687386;">Delivery Charges</span>
                        <strong style="color: {'#16865C' if shipping == 0 else '#172033'};">{'FREE' if shipping == 0 else format_rupee(shipping)}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 12px;">
                        <span style="color: #687386;">Estimated Taxes (8%)</span>
                        <strong style="color: #172033;">{format_rupee(tax)}</strong>
                    </div>
                    <div style="border-top: 1px solid #E5E9F0; padding-top: 12px; display: flex; justify-content: space-between; font-size: 18px; font-weight: 800;">
                        <span style="color: #172033;">Total Amount</span>
                        <span style="color: #172033;">{format_rupee(grand_total)}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
                has_out_of_stock = any(item['stock'] <= 0 for item in cart_items_data)
                has_over_stock = any(item['qty'] > item['stock'] for item in cart_items_data)
                if has_out_of_stock or has_over_stock:
                    st.warning("⚠️ Some items in your bag exceed available stock. Please adjust quantities before proceeding.")
                if st.button("Proceed to Delivery Address →", type="primary", use_container_width=True, key="cart_to_s2", disabled=(has_out_of_stock or has_over_stock)):
                    st.session_state.checkout_step = 2
                    st.rerun()

        # STEP 2: SHIPPING DESTINATION
        elif st.session_state.checkout_step == 2:
            st.markdown("<h4 style='font-size: 16px; margin-bottom: 12px;'>Select Delivery Address</h4>", unsafe_allow_html=True)
            col_addr_list, col_addr_snap = st.columns([7, 5], gap="large")

            with col_addr_list:
                if not st.session_state.user:
                    st.warning("Please sign in to choose or save your delivery destination.")
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
                            "Choose a delivery destination:",
                            options=addr_options,
                            format_func=lambda x: addr_map[x],
                            index=addr_options.index(st.session_state.selected_address_id) if st.session_state.selected_address_id in addr_options else (addr_options.index(default_id) if default_id in addr_options else 0),
                            key="cart_addr_radio"
                        )
                        st.session_state.selected_address_id = selected_id
                        st.session_state.selected_address_text = addr_map[selected_id]
                    else:
                        st.info("No saved addresses. Please add a destination below.")
                        st.session_state.selected_address_text = ""

                    # Inline Add Destination
                    with st.expander("+ Add New Delivery Destination", expanded=(not addresses)):
                        with st.form("cart_inline_addr_form"):
                            lbl = st.text_input("Address Label (e.g. Home, Office)", value="Home")
                            rec = st.text_input("Recipient Name", value=st.session_state.user.get('name', ''))
                            st_addr = st.text_input("Street Address", placeholder="100 Silicon Parkway")
                            ct = st.text_input("City", placeholder="Bengaluru")
                            stt = st.text_input("State", placeholder="KA")
                            zp = st.text_input("Postal Code / PIN", placeholder="560001")
                            def_chk = st.checkbox("Set as default shipping address", value=(not addresses))
                            if st.form_submit_button("Save Destination", type="primary"):
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
                                else:
                                    st.warning("Please provide street and city.")

                    b_s1, b_s3 = st.columns(2, gap="small")
                    with b_s1:
                        if st.button("← Back to Review Cart", use_container_width=True):
                            st.session_state.checkout_step = 1
                            st.rerun()
                    with b_s3:
                        if st.button("Proceed to Payment →", key="to_s3_from_s2", type="primary", use_container_width=True):
                            if not addresses and not st.session_state.get('selected_address_text'):
                                st.error("Please add a delivery destination first.")
                            else:
                                st.session_state.checkout_step = 3
                                st.rerun()

            with col_addr_snap:
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 1px solid #E5E9F0; border-radius: 8px; padding: 20px;">
                    <h4 style="font-size: 15px; margin: 0 0 10px 0; color: #172033;">Order Snapshot</h4>
                    <div style="font-size: 13px; color: #687386; margin-bottom: 6px;">Items: <strong style="color: #172033;">{sum(st.session_state.cart.values())}</strong></div>
                    <div style="font-size: 13px; color: #687386; margin-bottom: 6px;">Subtotal: <strong style="color: #172033;">{format_rupee(subtotal)}</strong></div>
                    <div style="font-size: 13px; color: #687386; margin-bottom: 6px;">Shipping: <strong style="color: #172033;">{'FREE' if shipping == 0 else format_rupee(shipping)}</strong></div>
                    <div style="font-size: 13px; color: #687386; margin-bottom: 10px;">Tax: <strong style="color: #172033;">{format_rupee(tax)}</strong></div>
                    <div style="border-top: 1px solid #E5E9F0; padding-top: 10px; font-size: 18px; font-weight: 800; color: #172033;">
                        Total: {format_rupee(grand_total)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # STEP 3: PAYMENT & CONFIRMATION
        elif st.session_state.checkout_step == 3:
            st.markdown("<h4 style='font-size: 16px; margin-bottom: 12px;'>Payment Method & Order Execution</h4>", unsafe_allow_html=True)
            col_p_meth, col_p_conf = st.columns([7, 5], gap="large")

            with col_p_meth:
                payment_methods = [
                    "💳 Credit / Debit Card (Nexus Pay)",
                    "📱 UPI / Instant NetBanking (Zero Fee)",
                    "📦 Cash on Delivery (COD)",
                    "🏦 Direct Bank Wire / NEFT"
                ]
                chosen_pay = st.radio("Select Payment Instrument:", payment_methods, index=0, key="cart_payment_radio")
                st.session_state.selected_payment_method = chosen_pay

                selected_addr = st.session_state.get('selected_address_text', 'Standard Delivery Destination')
                st.markdown(f"""
                <div style="background: #F8FAFC; border: 1px solid #E5E9F0; border-radius: 6px; padding: 14px; margin: 16px 0;">
                    <div style="font-size: 10px; font-weight: 700; color: #687386; text-transform: uppercase;">Delivery Address Confirmed</div>
                    <div style="font-size: 13px; font-weight: 600; color: #172033; margin-top: 4px;">📍 {selected_addr}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("← Change Destination", use_container_width=True):
                    st.session_state.checkout_step = 2
                    st.rerun()

            with col_p_conf:
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 1px solid #E5E9F0; border-radius: 8px; padding: 22px;">
                    <h4 style="font-size: 16px; margin: 0 0 12px 0; color: #172033;">Final Payment Summary</h4>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px;">
                        <span style="color: #687386;">Subtotal</span><strong style="color: #172033;">{format_rupee(subtotal)}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px;">
                        <span style="color: #687386;">Shipping</span><strong style="color: #172033;">{'FREE' if shipping == 0 else format_rupee(shipping)}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 10px;">
                        <span style="color: #687386;">Estimated Tax</span><strong style="color: #172033;">{format_rupee(tax)}</strong>
                    </div>
                    <div style="border-top: 1px solid #E5E9F0; padding-top: 10px; display: flex; justify-content: space-between; align-items: baseline;">
                        <span style="font-size: 15px; font-weight: 700; color: #172033;">Total Payable</span>
                        <span style="font-size: 22px; font-weight: 800; color: #172033;">{format_rupee(grand_total)}</span>
                    </div>
                    <div style="font-size: 11px; color: #687386; margin-top: 10px;">
                        🔒 PostgreSQL ACID row lock guarantees inventory reservation with zero overselling.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
                if st.button(f"⚡ Place Order ({format_rupee(grand_total)})", type="primary", use_container_width=True, key="cart_place_final_btn"):
                    if not st.session_state.user:
                        st.error("Please sign in before executing your order.")
                    else:
                        order_payload = {
                            "user_id": st.session_state.user['id'],
                            "items": items_payload,
                            "shipping_address": st.session_state.get('selected_address_text', 'Standard Delivery Destination'),
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
                            st.cache_data.clear()  # Invalidate cached product queries so updated inventory is visible
                            st.rerun()


# ==============================================================================
# VIEW 4: CUSTOMER PROFILE & ADDRESS BOOK (NO FACET SIDEBAR)
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
        st.markdown(f"<p style='font-size: 12px; color: #687386; margin-bottom: 20px;'>Manage account credentials and delivery destinations for <strong>{user['name']}</strong>.</p>", unsafe_allow_html=True)

        prof_c, addr_c = st.columns([5, 7], gap="large")

        with prof_c:
            st.markdown("<h4 style='font-size: 15px; margin-bottom: 10px;'>Account Credentials</h4>", unsafe_allow_html=True)
            with st.form("prof_edit_form"):
                pn = st.text_input("Full Name", value=user.get('name', ''))
                pe = st.text_input("Email Address", value=user.get('email', ''))
                st.markdown(f"<div style='font-size: 11px; color: #687386; margin-bottom: 10px;'>Customer Account ID: #{user.get('id')}</div>", unsafe_allow_html=True)
                if st.form_submit_button("Save Profile Changes", type="primary"):
                    res, err = put_json(f"/users/{user['id']}", {"name": pn.strip(), "email": pe.strip().lower()})
                    if res:
                        st.session_state.user['name'] = pn.strip()
                        st.session_state.user['email'] = pe.strip().lower()
                        st.success("Profile saved successfully!")
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
                    def_tag = "<span style='background: #EDFBF4; color: #16865C; font-size: 9px; font-weight: 700; padding: 2px 6px; border-radius: 4px; margin-left: 6px;'>DEFAULT</span>" if is_def else ""
                    st.markdown(f"""
                    <div style="background: #FFFFFF; border: 1px solid #E5E9F0; border-radius: 6px; padding: 12px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: baseline;">
                            <strong style="font-size: 13px; color: #172033;">📍 {a['label']} {def_tag}</strong>
                            <span style="font-size: 11px; color: #687386;">{a.get('country', 'India')}</span>
                        </div>
                        <div style="font-size: 12px; color: #687386; margin-top: 2px;">{a['recipient_name']} — {a['street']}, {a['city']}, {a['state']} {a['postal_code']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    ca_def, ca_del = st.columns([2, 1], gap="small")
                    with ca_def:
                        if not is_def:
                            if st.button("Set Default", key=f"p_sdef_{aid}", use_container_width=True):
                                put_json(f"/users/{user['id']}/addresses/{aid}/default")
                                st.session_state.selected_address_id = aid
                                st.rerun()
                    with ca_del:
                        if st.button("Delete", key=f"p_del_{aid}", use_container_width=True):
                            delete_req(f"/users/{user['id']}/addresses/{aid}")
                            st.rerun()
            else:
                st.info("No addresses saved yet.")

            with st.expander("+ Add New Address"):
                with st.form("prof_add_addr_form"):
                    lbl = st.text_input("Label (e.g. Home, Work)", value="Home")
                    rc = st.text_input("Recipient Name", value=user.get('name', ''))
                    stt = st.text_input("Street Address", placeholder="100 Silicon Parkway")
                    cy = st.text_input("City", placeholder="Bengaluru")
                    se = st.text_input("State", placeholder="KA")
                    zc = st.text_input("Postal Code / PIN", placeholder="560001")
                    is_d = st.checkbox("Make this my default delivery address")
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
# VIEW 5: ORDER HISTORY (NO FACET SIDEBAR)
# ==============================================================================
elif st.session_state.page == "Orders":
    user = st.session_state.user
    if not user:
        st.markdown("<h2 style='margin-bottom: 6px;'>Your Orders</h2>", unsafe_allow_html=True)
        st.warning("Please sign in to view your order receipts.")
        if st.button("🔑 Sign In / Register", type="primary"):
            set_page("Auth")
            st.rerun()
    else:
        user_id = user['id']
        st.markdown("<h2 style='margin-bottom: 4px;'>Your Orders</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 12px; color: #687386; margin-bottom: 20px;'>Displaying confirmed receipts for <strong>{user['name']}</strong> (Customer #{user_id})</p>", unsafe_allow_html=True)

        orders = fetch_json(f"/orders?user_id={user_id}") or []
        if not orders:
            st.markdown("""
            <div style="background: #FFFFFF; border: 1px solid #E5E9F0; border-radius: 8px; padding: 40px; text-align: center;">
                <div style="font-size: 36px; margin-bottom: 6px;">📦</div>
                <h4 style="margin: 0 0 4px 0; color: #172033;">No orders placed yet</h4>
                <p style="font-size: 12px; color: #687386;">Complete an order to see your confirmed purchase receipts here.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🛍️ Browse Products", type="primary"):
                set_page("Catalog")
                st.rerun()
        else:
            for o in orders:
                order_id = o['id']
                created = o.get('created_at', 'Recently')
                total_inr = format_rupee(o.get('total', 0.0))
                status = o.get('status', 'completed').capitalize()
                addr = o.get('shipping_address') or 'Standard Registered Destination'
                pay_method = o.get('payment_method') or 'Credit Card'

                with st.expander(f"📦 Order #{order_id} — {total_inr} — {status} ({created})", expanded=True):
                    st.markdown(f"""
                    <div style="background: #F8FAFC; border: 1px solid #E5E9F0; border-radius: 6px; padding: 10px 14px; margin-bottom: 10px; font-size: 12px; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                        <div><strong>📍 Destination:</strong> {addr}</div>
                        <div><strong>💳 Payment:</strong> {pay_method}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    items = fetch_json(f"/orders/{order_id}/items") or []
                    for it in items:
                        unit_inr = format_rupee(it['price'])
                        row_inr = format_rupee(float(it['price']) * it['qty'])
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid #E5E9F0; font-size: 12px;">
                            <div>
                                <strong style="color: #172033;">{it['product_name']}</strong>
                                <span style="color: #687386; font-size: 10px; margin-left: 6px;">(SKU: {it['product_id']})</span>
                            </div>
                            <div>
                                <span style="color: #687386;">{it['qty']} × {unit_inr} = </span>
                                <strong style="color: #172033;">{row_inr}</strong>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)


# ==============================================================================
# VIEW 6: CUSTOMER AUTHENTICATION (SIGN IN / REGISTER)
# ==============================================================================
elif st.session_state.page == "Auth":
    st.markdown("<h2 style='margin-bottom: 4px;'>Customer Sign In</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 12px; color: #687386; margin-bottom: 20px;'>Sign in to manage your addresses and view past orders.</p>", unsafe_allow_html=True)

    if st.session_state.user:
        u = st.session_state.user
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E5E9F0; border-radius: 8px; padding: 24px; margin-bottom: 20px;">
            <h4 style="margin: 0 0 4px 0; color: #172033;">Currently Signed In as {u.get('name', 'Customer')}</h4>
            <div style="font-size: 12px; color: #687386; margin-bottom: 12px;">{u.get('email', '')} • Customer ID #{u.get('id', '')}</div>
            <p style="font-size: 13px; color: #687386; margin: 0;">Your session is active. You can browse the catalog or manage your saved destinations.</p>
        </div>
        """, unsafe_allow_html=True)

        ca1, ca2, ca3 = st.columns(3, gap="small")
        with ca1:
            if st.button("🛍️ Browse Products", use_container_width=True, type="primary"):
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
        auth_t1, auth_t2 = st.tabs(["🔑 Sign In", "📝 Create Account"])
        with auth_t1:
            st.markdown("""
            <div style="background: #EAF2FF; border: 1px solid #C8DCFE; border-radius: 6px; padding: 12px; margin-bottom: 16px; font-size: 12px; color: #1E5BC6;">
                💡 <strong>Demo Credentials</strong>: <code>demo@nexus.com</code> / <code>demo123</code>
            </div>
            """, unsafe_allow_html=True)
            if st.button("⚡ 1-Click Login as Demo User", type="primary", use_container_width=True, key="auth_quick_demo"):
                res, err = post_json("/auth/login", {"email": "demo@nexus.com", "password": "demo123"})
                if res and "user" in res:
                    st.session_state.user = res["user"]
                    st.toast("⚡ Welcome back, Demo User!", icon="✅")
                    set_page("Catalog")
                    st.rerun()
                else:
                    st.error(f"Login failed: {err}")

            st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E5E9F0;'/>", unsafe_allow_html=True)
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
                rn = st.text_input("Full Name", placeholder="Aditi Sharma")
                re_em = st.text_input("Email Address", placeholder="aditi@example.com")
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
# VIEW 7: DATABASE TELEMETRY & SYSTEM HEALTH (NO FACET SIDEBAR)
# ==============================================================================
elif st.session_state.page == "Databases":
    st.markdown("<h2 style='margin-bottom: 4px;'>Database & Architecture Telemetry</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 12px; color: #687386; margin-bottom: 20px;'>Live query routing across PostgreSQL (ACID & Auth), MongoDB (Catalog & SVGs), and ChromaDB (Vector Similarity).</p>", unsafe_allow_html=True)

    debug_info = fetch_json("/debug/requests")
    if debug_info and 'requests' in debug_info and debug_info['requests']:
        st.dataframe(debug_info['requests'], use_container_width=True)
    else:
        st.info("No queries recorded yet.")
