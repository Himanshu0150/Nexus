import streamlit as st
import urllib.request
import urllib.parse
import json

# --- 1. Page Configuration & Custom CSS ---
st.set_page_config(
    page_title="NEXUS ELECTRONICS — Precision Hardware Storefront",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://localhost:8000"

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">

<style>
/* Universal Base Text & High-Contrast Typography */
:root, html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #0f172a !important;
    background-color: #fbf9f9 !important;
}

/* Headings default to dark slate */
h1, h2, h3, h4, h5, h6, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: #0f172a !important;
    font-weight: 800 !important;
}

/* Markdown text */
div[data-testid="stMarkdownContainer"] {
    color: #0f172a;
}
div[data-testid="stMarkdownContainer"] > p {
    color: #0f172a;
}

/* Streamlit Radio Buttons (Crucial for Address and Payment selection in dark mode) */
div[data-testid="stRadio"] label,
div[data-testid="stRadio"] label *,
div[data-testid="stRadio"] p,
div[data-testid="stRadio"] span {
    color: #0f172a !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* Checkbox Labels */
div[data-testid="stCheckbox"] label,
div[data-testid="stCheckbox"] label * {
    color: #0f172a !important;
    font-weight: 600 !important;
}

/* Form Inputs, Selectboxes, Number Inputs, Labels */
label[data-testid="stWidgetLabel"],
label[data-testid="stWidgetLabel"] *,
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
    color: #0f172a !important;
    font-weight: 700 !important;
    font-size: 13px !important;
}

/* Text Input & Number Input Boxes */
input[type="text"], input[type="password"], input[type="number"], textarea, select {
    color: #0f172a !important;
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}

/* Expander Titles */
[data-testid="stExpander"] details summary,
[data-testid="stExpander"] details summary * {
    color: #0f172a !important;
    font-weight: 700 !important;
}

/* Alert / Warning / Error Boxes */
div[data-testid="stAlert"] {
    background-color: #fff1f2 !important;
    border: 1px solid #fecdd3 !important;
}
div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p,
div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] span {
    color: #9f1239 !important;
    font-weight: 600 !important;
}

.nexus-announcement {
    background: #f5f3f3;
    border-bottom: 1px solid #e5e7eb;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 500;
    color: #475569 !important;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 8px;
    margin-bottom: 18px;
}
.nexus-announcement span, .nexus-announcement strong {
    color: #334155 !important;
}
.nexus-announcement .badge-dot {
    width: 7px;
    height: 7px;
    background: #0650cc;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
}
.nexus-logo-title {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #0f172a !important;
    margin: 0;
    line-height: 1.1;
}
.nexus-logo-sub {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.18em;
    color: #0650cc !important;
    text-transform: uppercase;
}
.nexus-hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
    border-radius: 16px;
    padding: 30px 36px;
    color: #ffffff !important;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.15);
}
.nexus-hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255, 255, 255, 0.12) !important;
    backdrop-filter: blur(8px);
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #93c5fd !important;
    margin-bottom: 10px;
}
.nexus-hero-pill span {
    color: #93c5fd !important;
}
.nexus-hero h1 {
    font-size: 30px !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em;
    margin: 0 0 8px 0;
    color: #ffffff !important;
    line-height: 1.2;
}
.nexus-hero p {
    font-size: 14px !important;
    color: #cbd5e1 !important;
    max-width: 650px;
    line-height: 1.5;
    margin: 0 0 16px 0;
}
.nexus-spec-ticker {
    display: flex;
    gap: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
    padding-top: 12px;
}
.nexus-spec-item {
    font-size: 12px;
    color: #cbd5e1 !important;
}
.nexus-spec-item strong {
    color: #ffffff !important;
    font-weight: 600;
    margin-right: 4px;
}
.nexus-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 18px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.badge-category {
    background: #eef2ff !important;
    color: #4338ca !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    padding: 3px 9px;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    display: inline-block;
}
.badge-stock-in {
    background: #ecfdf5 !important;
    color: #065f46 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    padding: 3px 8px;
    border-radius: 6px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
.badge-stock-low {
    background: #fef2f2 !important;
    color: #991b1b !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    padding: 3px 8px;
    border-radius: 6px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    min-height: 44px !important;
    transition: all 0.15s ease !important;
}
button[kind="primary"],
button[kind="primary"] *,
button[data-testid="baseButton-primary"],
button[data-testid="baseButton-primary"] *,
button[data-testid="baseButton-primary"] p,
button[data-testid="baseButton-primary"] span {
    background-color: #0650cc !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}
button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {
    background-color: #043e9e !important;
}
button[kind="secondary"],
button[kind="secondary"] *,
button[data-testid="baseButton-secondary"],
button[data-testid="baseButton-secondary"] *,
button[data-testid="baseButton-secondary"] p,
button[data-testid="baseButton-secondary"] span {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid #cbd5e1 !important;
    font-weight: 600 !important;
}
button[kind="secondary"]:hover,
button[data-testid="baseButton-secondary"]:hover {
    background-color: #f1f5f9 !important;
}
.shipping-progress-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.progress-bar-bg {
    width: 100%;
    height: 8px;
    background: #e2e8f0;
    border-radius: 9999px;
    overflow: hidden;
    margin-top: 6px;
}
.progress-bar-fill {
    height: 100%;
    background: #0650cc;
    border-radius: 9999px;
    transition: width 0.4s ease;
}
.step-indicator {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 12px 18px;
    margin-bottom: 20px;
}
.step-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 600;
}
.step-num {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
}
.step-active .step-num { background: #0650cc !important; color: #ffffff !important; }
.step-active { color: #0650cc !important; }
.step-inactive .step-num { background: #e2e8f0 !important; color: #64748b !important; }
.step-inactive { color: #64748b !important; }
.step-completed .step-num { background: #10b981 !important; color: #ffffff !important; }
.step-completed { color: #10b981 !important; }

section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e5e7eb !important;
}
</style>
""", unsafe_allow_html=True)


# --- 2. API Helper Functions ---
def fetch_json(endpoint):
    try:
        with urllib.request.urlopen(f"{API_URL}{endpoint}", timeout=8) as response:
            return json.loads(response.read().decode())
    except Exception as e:
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
        except:
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
    st.session_state.page = "Catalog"
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None
if 'checkout_step' not in st.session_state:
    st.session_state.checkout_step = 1  # 1: Cart, 2: Address, 3: Payment, 4: Confirm
if 'selected_address_id' not in st.session_state:
    st.session_state.selected_address_id = None
if 'selected_payment_method' not in st.session_state:
    st.session_state.selected_payment_method = "Credit Card (Nexus Pay)"

# Current logged-in user state (defaults to Demo User ID 1 on initial startup)
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

def add_to_cart_action(pid, qty=1):
    prod = fetch_json(f"/products/{pid}")
    if not prod:
        st.error("Product not found.")
        return
    current_qty = st.session_state.cart.get(pid, 0)
    max_stock = prod.get('stock', 0)
    if current_qty + qty > max_stock:
        st.error(f"Cannot add {qty} more. Only {max_stock} units in stock!")
    else:
        st.session_state.cart[pid] = current_qty + qty
        st.toast(f"🛒 Added {prod['name']} (Qty: {qty}) to your cart!", icon="✅")


# --- 4. Sidebar Controls (Customer Profile & Authentication) ---
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
        <span style="font-size: 22px;">⚡</span>
        <div>
            <div style="font-size: 16px; font-weight: 800; letter-spacing: -0.02em; line-height: 1.1;">NEXUS</div>
            <div style="font-size: 9px; font-weight: 700; color: #0650cc; letter-spacing: 0.12em;">ELECTRONICS</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Active User Profile Box
    user = st.session_state.user
    if user:
        st.markdown(f"""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 8px;">
            <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase;">Active Customer Profile</div>
            <div style="font-size: 14px; font-weight: 700; color: #0f172a; margin-top: 2px;">👤 {user['name']}</div>
            <div style="font-size: 11px; color: #475569;">{user['email']}</div>
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
        <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 10px; padding: 12px; margin-bottom: 8px;">
            <div style="font-size: 11px; font-weight: 700; color: #b45309; text-transform: uppercase;">Not Signed In</div>
            <div style="font-size: 13px; font-weight: 600; color: #92400e; margin-top: 2px;">Guest Customer</div>
            <div style="font-size: 11px; color: #b45309;">Sign in to save addresses & track orders.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚡ 1-Click Demo Login", key="sidebar_demo_login", use_container_width=True, type="primary"):
            res, err = post_json("/auth/login", {"email": "demo@nexus.com", "password": "demo123"})
            if res and "user" in res:
                st.session_state.user = res["user"]
                st.session_state.selected_address_id = None
                st.toast("⚡ Signed in as Demo User!", icon="✅")
                st.rerun()

    # Navigation Buttons
    nav_items = [
        ("Catalog", "🛍️ Hardware Catalog"),
        ("Cart", f"🛒 Cart & Checkout ({sum(st.session_state.cart.values())})"),
        ("Profile", "👤 Profile & Addresses"),
        ("Orders", "📦 Order History"),
        ("Auth", "🔑 Sign In / Register"),
        ("Databases", "📊 Database Telemetry")
    ]
    
    for p_id, label in nav_items:
        is_active = (st.session_state.page == p_id)
        btn_type = "primary" if is_active else "secondary"
        if st.button(label, key=f"nav_{p_id}", use_container_width=True, type=btn_type):
            set_page(p_id)
            st.rerun()

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #e5e7eb;'/>", unsafe_allow_html=True)
    
    # Telemetry Monitor
    st.markdown("""
    <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748b; margin-bottom: 6px;">
        Database Status
    </div>
    <div style="display: flex; flex-direction: column; gap: 4px; font-size: 11px; color: #334155;">
        <div>🐘 <strong>PostgreSQL</strong>: <span style="color: #16a34a;">Users, Addresses, Stock</span></div>
        <div>🍃 <strong>MongoDB</strong>: <span style="color: #16a34a;">Product Catalog (100)</span></div>
        <div>🔮 <strong>ChromaDB</strong>: <span style="color: #16a34a;">Vector Search Ready</span></div>
    </div>
    """, unsafe_allow_html=True)


# --- 5. Global Top Bar ---
st.markdown("""
<div class="nexus-announcement">
    <div>
        <span class="badge-dot"></span>
        <strong style="color: #111827;">SPRING HARDWARE RELEASE 2025</strong>
        <span style="color: #94a3b8; margin: 0 6px;">/</span>
        <span>Complimentary expedited courier dispatch on all domestic orders over $150</span>
    </div>
    <div style="font-size: 11px; color: #64748b;">
        <span>Direct Technical Support • Enterprise Procurement</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Top Bar with Quick Cart button
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("""
    <div style="display: flex; align-items: baseline; gap: 8px;">
        <h1 class="nexus-logo-title">NEXUS</h1>
        <span class="nexus-logo-sub">ELECTRONICS</span>
    </div>
    """, unsafe_allow_html=True)

with col_head2:
    cart_count = sum(st.session_state.cart.values())
    if st.button(f"🛒 Cart: {cart_count} items", key="quick_view_cart", use_container_width=True):
        set_page("Cart")
        st.rerun()


# ==============================================================================
# VIEW: CATALOG PAGE
# ==============================================================================
if st.session_state.page == "Catalog":
    st.markdown("""
    <div class="nexus-hero">
        <div class="nexus-hero-pill">
            <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #60a5fa;"></span>
            Nexus Hardware Release 2025
        </div>
        <h1>Technology for everyday life.</h1>
        <p>
            Engineered for seamless productivity, immersive sound, and all-day endurance.
            Discover precision computing instruments, high-performance electronics, and curated tech.
        </p>
        <div class="nexus-spec-ticker">
            <div class="nexus-spec-item"><strong>100% CNC</strong> Aerospace Alloy</div>
            <div class="nexus-spec-item"><strong>Zero Overselling</strong> PostgreSQL ACID</div>
            <div class="nexus-spec-item"><strong>AI Recommendations</strong> Vector Embeddings</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cat_col, search_col = st.columns([1, 1])
    with cat_col:
        categories = ["All", "laptops", "phones", "shoes", "books"]
        cat_labels = {
            "All": "🌐 All Categories (100)",
            "laptops": "💻 Laptops (25)",
            "phones": "📱 Smartphones (25)",
            "shoes": "👟 Shoes & Apparel (25)",
            "books": "📚 Technical Books (25)"
        }
        category = st.selectbox(
            "Category Filter",
            categories,
            format_func=lambda x: cat_labels.get(x, x),
            label_visibility="collapsed"
        )
    with search_col:
        search_q = st.text_input(
            "Search Catalog",
            placeholder="Search by product name, model, or specs...",
            label_visibility="collapsed"
        )
    
    query_parts = []
    if category != "All":
        query_parts.append(f"category={urllib.parse.quote(category)}")
    if search_q:
        query_parts.append(f"q={urllib.parse.quote(search_q)}")
    
    qs = "&".join(query_parts)
    products = fetch_json(f"/products?{qs}" if qs else "/products") or []
    
    if not products:
        st.info("No products found matching your search.")
    else:
        st.markdown(f"<div style='font-size: 13px; color: #64748b; margin-bottom: 16px;'>Showing <strong>{len(products)}</strong> products</div>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for idx, p in enumerate(products):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="nexus-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span class="badge-category">{p['category']}</span>
                        <span class="badge-stock-in">● {p['product_id']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                img_url = f"{API_URL}/products/{p['product_id']}/image"
                st.image(img_url, use_column_width=True)
                
                st.markdown(f"""
                <div style="margin: 8px 0 4px 0;">
                    <div style="font-size: 16px; font-weight: 700; color: #111827; line-height: 1.3;">{p['name']}</div>
                    <div style="font-size: 13px; color: #64748b; margin: 4px 0 8px 0;">{p['description']}</div>
                    <div style="font-size: 20px; font-weight: 800; color: #0650cc;">${p['price']:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                
                btn_col1, btn_col2 = st.columns([1, 1])
                with btn_col1:
                    if st.button("Details", key=f"det_{p['product_id']}", use_container_width=True):
                        st.session_state.selected_product = p['product_id']
                        set_page("Product")
                        st.rerun()
                with btn_col2:
                    if st.button("Add 🛒", key=f"add_{p['product_id']}", use_container_width=True, type="primary"):
                        add_to_cart_action(p['product_id'], 1)
                        st.rerun()
                
                st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# VIEW: PRODUCT DETAILS PAGE
# ==============================================================================
elif st.session_state.page == "Product":
    pid = st.session_state.selected_product
    if not pid:
        set_page("Catalog")
        st.rerun()
    prod = fetch_json(f"/products/{pid}")
    if not prod:
        st.error("Failed to load product.")
        if st.button("← Back to Catalog"):
            set_page("Catalog")
            st.rerun()
    else:
        st.markdown(f"""
        <nav style="font-size: 13px; color: #64748b; margin-bottom: 14px;">
            <span>Catalog</span> / <span style="text-transform: capitalize;">{prod['category']}</span> / <strong style="color: #111827;">{prod['name']}</strong>
        </nav>
        """, unsafe_allow_html=True)
        
        if st.button("← Back to Catalog", key="back_btn"):
            set_page("Catalog")
            st.rerun()
            
        left_col, right_col = st.columns([5, 6], gap="large")
        with left_col:
            st.image(f"{API_URL}/products/{pid}/image", use_column_width=True)
            st.markdown("""
            <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 14px;">
                <div style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px; font-size: 12px; color: #334155;">
                    🛡️ <strong>Certified Unibody</strong>: Zero bloatware, precision tolerance.
                </div>
                <div style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px; font-size: 12px; color: #334155;">
                    ⚡ <strong>ACID Guarantee</strong>: Real-time inventory reservation.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with right_col:
            stock = prod.get('stock', 0)
            stock_badge = f"<span class='badge-stock-in'>● In Stock ({stock} available)</span>" if stock > 5 else f"<span class='badge-stock-low'>⚠️ Low Stock ({stock} left)</span>"
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span class="badge-category">{prod['category']}</span>
                {stock_badge}
            </div>
            <h1 style="font-size: 28px; font-weight: 800; color: #111827; margin: 0 0 8px 0;">{prod['name']}</h1>
            <div style="font-size: 26px; font-weight: 800; color: #0650cc; margin-bottom: 12px;">${prod['price']:,.2f}</div>
            <p style="font-size: 14px; color: #475569; line-height: 1.6; margin-bottom: 16px;">{prod['description']}</p>
            """, unsafe_allow_html=True)
            
            # Attributes Chips
            attrs = prod.get('attributes', {})
            if attrs:
                chips_html = "".join([
                    f"<div style='background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; margin-right: 8px; margin-bottom: 8px; display: inline-block;'>"
                    f"<div style='font-size: 10px; color: #64748b; text-transform: uppercase; font-weight: 700;'>{k}</div>"
                    f"<div style='font-size: 13px; font-weight: 700; color: #0f172a;'>{v}</div></div>"
                    for k, v in attrs.items()
                ])
                st.markdown(f"<div style='display: flex; flex-wrap: wrap; margin-bottom: 8px;'>{chips_html}</div>", unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 14px 0; border: none; border-top: 1px solid #e5e7eb;'/>", unsafe_allow_html=True)
            
            qty = st.number_input("Quantity", min_value=1, max_value=max(1, stock), value=1)
            btn_col_a, btn_col_b = st.columns(2)
            with btn_col_a:
                if stock > 0:
                    if st.button("🛒 Add to Cart", key="add_det_btn", use_container_width=True):
                        add_to_cart_action(pid, qty)
                        st.rerun()
                else:
                    st.button("Out of Stock", disabled=True, use_container_width=True)
            with btn_col_b:
                if stock > 0:
                    if st.button("⚡ Buy Now", key="buy_now_det_btn", use_container_width=True, type="primary"):
                        add_to_cart_action(pid, qty)
                        set_page("Cart")
                        st.session_state.checkout_step = 1
                        st.rerun()

        # Similar Products
        st.markdown("<hr style='margin: 28px 0 16px 0; border: none; border-top: 1px solid #e5e7eb;'/>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #0f172a; font-size: 18px; font-weight: 700;'>Similar Products (Vector Search)</h3>", unsafe_allow_html=True)
        similar = fetch_json(f"/products/{pid}/similar") or []
        if similar:
            sim_cols = st.columns(len(similar))
            for i, s in enumerate(similar):
                with sim_cols[i]:
                    st.image(f"{API_URL}/products/{s['product_id']}/image", use_column_width=True)
                    st.markdown(f"<div style='font-size: 12px; font-weight: 700; truncate;'>{s['name']}</div><div style='font-size: 13px; font-weight: 800; color: #0650cc;'>${s['price']:,.2f}</div>", unsafe_allow_html=True)
                    if st.button("View", key=f"sim_view_{s['product_id']}", use_container_width=True):
                        st.session_state.selected_product = s['product_id']
                        st.rerun()


# ==============================================================================
# VIEW: MULTI-STEP CHECKOUT & CART
# ==============================================================================
elif st.session_state.page == "Cart":
    st.markdown("<h1 style='color: #0f172a; font-size: 26px; font-weight: 800; margin-bottom: 4px;'>Checkout & Order Fulfillment</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; font-size: 13px; margin-bottom: 18px;'>Review items, specify shipping address, and confirm payment</p>", unsafe_allow_html=True)
    
    # -------------------------------------------------------------
    # STEP 4: ORDER CONFIRMATION / SUCCESS SCREEN
    # -------------------------------------------------------------
    if st.session_state.get('checkout_step') == 4:
        last_id = st.session_state.get('last_order_id', 'N/A')
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #bbf7d0; border-radius: 16px; padding: 40px; text-align: center; box-shadow: 0 4px 16px rgba(16, 185, 129, 0.08); margin-bottom: 24px;">
            <div style="font-size: 54px; margin-bottom: 12px;">🎉</div>
            <div style="display: inline-block; background: #ecfdf5; color: #065f46; font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: 9999px; text-transform: uppercase; margin-bottom: 12px;">
                Transaction Approved • ACID Verified
            </div>
            <h2 style="font-size: 24px; font-weight: 800; color: #0f172a; margin: 0 0 8px 0;">Order #{last_id} Successfully Placed!</h2>
            <p style="font-size: 14px; color: #475569; max-width: 520px; margin: 0 auto 20px auto; line-height: 1.5;">
                Thank you for your order. Your items have been securely reserved in PostgreSQL and routed for expedited courier dispatch.
            </p>
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px; display: inline-block; text-align: left; font-size: 13px; color: #334155; margin-bottom: 20px;">
                <div style="color: #0f172a;">📍 <strong style="color: #0f172a;">Delivery Address:</strong> {st.session_state.get('selected_address_text', 'Standard Delivery Address')}</div>
                <div style="margin-top: 4px; color: #0f172a;">💳 <strong style="color: #0f172a;">Payment Method:</strong> {st.session_state.get('selected_payment_method', 'Credit Card')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c_hist, c_cat = st.columns(2)
        with c_hist:
            if st.button("📦 View Order in Order History", type="primary", use_container_width=True):
                st.session_state.checkout_step = 1
                set_page("Orders")
                st.rerun()
        with c_cat:
            if st.button("🛍️ Continue Shopping", use_container_width=True):
                st.session_state.checkout_step = 1
                set_page("Catalog")
                st.rerun()

    # -------------------------------------------------------------
    # EMPTY CART STATE
    # -------------------------------------------------------------
    elif not st.session_state.cart:
        st.markdown("""
        <div style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 14px; padding: 44px; text-align: center; margin-bottom: 24px;">
            <div style="font-size: 44px; margin-bottom: 8px;">🛒</div>
            <h3 style="font-size: 20px; font-weight: 800; color: #0f172a; margin-bottom: 6px;">Your cart is currently empty</h3>
            <p style="font-size: 13px; color: #64748b; margin-bottom: 20px;">Browse our precision hardware catalog to add cutting-edge gear.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🛍️ Browse Full Hardware Catalog", type="primary", use_container_width=True):
            set_page("Catalog")
            st.rerun()
            
        st.markdown("<h4 style='font-size: 16px; font-weight: 700; color: #0f172a; margin: 28px 0 14px 0;'>Popular Hardware Picks (1-Click Add)</h4>", unsafe_allow_html=True)
        featured_prods = fetch_json("/products?limit=4") or []
        if featured_prods:
            f_cols = st.columns(min(4, len(featured_prods)))
            for idx, fp in enumerate(featured_prods[:4]):
                with f_cols[idx]:
                    st.image(f"{API_URL}/products/{fp['product_id']}/image", use_column_width=True)
                    st.markdown(f"""
                    <div style="font-size: 13px; font-weight: 700; color: #0f172a; margin-top: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{fp['name']}</div>
                    <div style="font-size: 15px; font-weight: 800; color: #0650cc; margin: 2px 0 8px 0;">${fp['price']:,.2f}</div>
                    """, unsafe_allow_html=True)
                    if st.button("Add to Cart", key=f"quick_add_{fp['product_id']}", use_container_width=True, type="primary"):
                        add_to_cart_action(fp['product_id'], 1)
                        st.session_state.checkout_step = 1
                        st.rerun()

    else:
        # Interactive Step Navigation Bar
        step_col1, step_col2, step_col3 = st.columns(3)
        with step_col1:
            s1_type = "primary" if st.session_state.checkout_step == 1 else "secondary"
            if st.button(f"1️⃣ Review Items ({sum(st.session_state.cart.values())})", key="tab_step_1", use_container_width=True, type=s1_type):
                st.session_state.checkout_step = 1
                st.rerun()
        with step_col2:
            s2_type = "primary" if st.session_state.checkout_step == 2 else "secondary"
            if st.button("2️⃣ Delivery Address", key="tab_step_2", use_container_width=True, type=s2_type):
                st.session_state.checkout_step = 2
                st.rerun()
        with step_col3:
            s3_type = "primary" if st.session_state.checkout_step == 3 else "secondary"
            if st.button("3️⃣ Payment & Confirm", key="tab_step_3", use_container_width=True, type=s3_type):
                st.session_state.checkout_step = 3
                st.rerun()
        
        st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
        
        # Calculate subtotal and load product data
        subtotal = 0.0
        items_payload = []
        cart_items_data = []
        for pid, qty in list(st.session_state.cart.items()):
            prod = fetch_json(f"/products/{pid}")
            if prod:
                total_line = prod['price'] * qty
                subtotal += total_line
                items_payload.append({"product_id": pid, "qty": qty})
                cart_items_data.append({
                    "product_id": pid, "name": prod['name'], "price": prod['price'],
                    "qty": qty, "total": total_line, "stock": prod.get('stock', 0)
                })

        shipping = 0.0 if subtotal >= 150.0 else 15.0
        tax = round(subtotal * 0.08, 2)
        grand_total = round(subtotal + shipping + tax, 2)

        # -------------------------------------------------------------
        # STEP 1: REVIEW CART ITEMS
        # -------------------------------------------------------------
        if st.session_state.checkout_step == 1:
            col_l, col_r = st.columns([7, 5], gap="large")
            with col_l:
                st.markdown("<h4 style='font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 12px;'>Cart Items</h4>", unsafe_allow_html=True)
                for item in cart_items_data:
                    pid = item['product_id']
                    with st.container():
                        st.markdown(f"""
                        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
                            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
                                <strong style="font-size: 15px; font-weight: 700; color: #0f172a;">{item['name']}</strong>
                                <span style="font-size: 16px; font-weight: 800; color: #0650cc;">${item['total']:,.2f}</span>
                            </div>
                            <div style="font-size: 12px; color: #475569;">Unit Price: ${item['price']:,.2f} &nbsp;•&nbsp; Stock Available: {item['stock']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_img, col_qty, col_del = st.columns([1.5, 3.5, 2])
                        with col_img:
                            st.image(f"{API_URL}/products/{pid}/image", width=75)
                        with col_qty:
                            st.markdown("<div style='font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase; margin-bottom: 2px;'>Quantity</div>", unsafe_allow_html=True)
                            new_qty = st.number_input(
                                "Quantity",
                                min_value=1,
                                max_value=max(1, item['stock']),
                                value=item['qty'],
                                key=f"cart_qty_{pid}",
                                label_visibility="collapsed"
                            )
                            if new_qty != item['qty']:
                                st.session_state.cart[pid] = new_qty
                                st.rerun()
                        with col_del:
                            st.markdown("<div style='padding-top: 18px;'></div>", unsafe_allow_html=True)
                            if st.button("🗑️ Remove", key=f"del_{pid}", use_container_width=True):
                                del st.session_state.cart[pid]
                                st.rerun()
                        st.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid #f1f5f9;'/>", unsafe_allow_html=True)

                c_shop, c_clr = st.columns([2, 1])
                with c_shop:
                    if st.button("🛍️ Add More Products / Continue Shopping", use_container_width=True):
                        set_page("Catalog")
                        st.rerun()
                with c_clr:
                    if st.button("🗑️ Clear Cart", use_container_width=True):
                        st.session_state.cart = {}
                        st.rerun()

            with col_r:
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px;">
                    <h3 style="font-size: 16px; font-weight: 700; color: #0f172a; margin-top: 0; margin-bottom: 12px;">Order Summary</h3>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; color: #334155;">
                        <span style="color: #334155;">Subtotal ({sum(st.session_state.cart.values())} items)</span><strong style="color: #0f172a;">${subtotal:,.2f}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; color: #334155;">
                        <span style="color: #334155;">Expedited Courier Shipping</span><strong style="color: #0f172a;">{'FREE' if shipping == 0 else f'${shipping:,.2f}'}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 10px; color: #334155;">
                        <span style="color: #334155;">Estimated Tax (8%)</span><strong style="color: #0f172a;">${tax:,.2f}</strong>
                    </div>
                    <div style="border-top: 1px solid #e2e8f0; padding-top: 10px; display: flex; justify-content: space-between; font-size: 16px; font-weight: 800;">
                        <span style="color: #0f172a;">Total</span><span style="color: #0650cc;">${grand_total:,.2f}</span>
                    </div>
                    <div style="font-size: 11px; color: #16a34a; font-weight: 600; margin-top: 8px;">
                        {'✓ Qualifying for Free Expedited Shipping!' if shipping == 0 else f'Add ${(150.0 - subtotal):,.2f} more for Free Shipping!'}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
                if st.button("Proceed to Delivery Address →", type="primary", use_container_width=True, key="to_step_2_btn"):
                    st.session_state.checkout_step = 2
                    st.rerun()

        # -------------------------------------------------------------
        # STEP 2: SELECT DELIVERY ADDRESS
        # -------------------------------------------------------------
        elif st.session_state.checkout_step == 2:
            st.markdown("<h3 style='font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 14px;'>Step 2: Shipping Destination</h3>", unsafe_allow_html=True)
            
            col_addrs, col_summary = st.columns([7, 5], gap="large")
            
            with col_addrs:
                if not st.session_state.user:
                    st.markdown("""
                    <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 12px; padding: 18px; margin-bottom: 16px;">
                        <div style="font-size: 14px; font-weight: 700; color: #92400e; margin-bottom: 4px;">🔒 Account Authentication Required</div>
                        <div style="font-size: 12px; color: #b45309; line-height: 1.5;">
                            Please sign in or create an account to select a delivery address and complete checkout.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("⚡ 1-Click Sign In as Demo User (demo@nexus.com)", type="primary", use_container_width=True, key="quick_demo_step2"):
                        res, err = post_json("/auth/login", {"email": "demo@nexus.com", "password": "demo123"})
                        if res and "user" in res:
                            st.session_state.user = res["user"]
                            st.toast("⚡ Signed in as Demo User!", icon="✅")
                            st.rerun()
                        else:
                            st.error(f"Sign in failed: {err}")
                            
                    st.markdown("<div style='text-align: center; font-size: 12px; font-weight: 600; color: #64748b; margin: 12px 0;'>— OR SIGN IN MANUALLY —</div>", unsafe_allow_html=True)
                    
                    in_t1, in_t2 = st.tabs(["Sign In", "Create Account"])
                    with in_t1:
                        with st.form("inline_login_step2"):
                            l_email = st.text_input("Email Address", key="s2_login_email")
                            l_pass = st.text_input("Password", type="password", key="s2_login_pass")
                            if st.form_submit_button("Sign In & Continue"):
                                if l_email and l_pass:
                                    res, err = post_json("/auth/login", {"email": l_email.strip(), "password": l_pass.strip()})
                                    if res and "user" in res:
                                        st.session_state.user = res["user"]
                                        st.toast(f"Welcome back, {res['user']['name']}!", icon="✅")
                                        st.rerun()
                                    else:
                                        st.error(f"Sign in failed: {err}")
                                else:
                                    st.warning("Please enter email and password.")
                    with in_t2:
                        with st.form("inline_reg_step2"):
                            r_name = st.text_input("Full Name", key="s2_reg_name")
                            r_email = st.text_input("Email Address", key="s2_reg_email")
                            r_pass = st.text_input("Password", type="password", key="s2_reg_pass")
                            if st.form_submit_button("Register & Continue"):
                                if r_name and r_email and r_pass:
                                    res, err = post_json("/auth/register", {"name": r_name.strip(), "email": r_email.strip(), "password": r_pass.strip()})
                                    if res and "user" in res:
                                        st.session_state.user = res["user"]
                                        st.toast(f"🎉 Account created! Welcome, {res['user']['name']}!", icon="✅")
                                        st.rerun()
                                    else:
                                        st.error(f"Registration failed: {err}")
                                else:
                                    st.warning("Please fill in all registration fields.")
                                    
                    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
                    if st.button("← Back to Review Items", key="b_to_s1_guest", use_container_width=True):
                        st.session_state.checkout_step = 1
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
                            key="s2_addr_radio"
                        )
                        st.session_state.selected_address_id = selected_id
                        st.session_state.selected_address_text = addr_map[selected_id]
                    else:
                        st.info("No saved addresses found. Please add a shipping address below.")
                        st.session_state.selected_address_text = ""

                    # Inline Add Address Form (No nested columns to avoid StreamlitAPIException)
                    with st.expander("+ Add a New Shipping Address", expanded=(not addresses)):
                        with st.form("inline_add_addr_form"):
                            new_label = st.text_input("Address Label (e.g., Home, Work, Office)", value="Home")
                            new_name = st.text_input("Recipient Full Name", value=st.session_state.user.get('name', ''))
                            new_street = st.text_input("Street Address", placeholder="123 Technology Way")
                            new_city = st.text_input("City", placeholder="San Francisco")
                            new_state = st.text_input("State / Region", placeholder="CA")
                            new_zip = st.text_input("Postal Code / Zip", placeholder="94105")
                            new_default = st.checkbox("Set as default delivery destination", value=(not addresses))

                            if st.form_submit_button("Save & Use This Address", type="primary"):
                                if new_street and new_city:
                                    payload = {
                                        "label": new_label,
                                        "recipient_name": new_name,
                                        "street": new_street,
                                        "city": new_city,
                                        "state": new_state,
                                        "postal_code": new_zip,
                                        "is_default": new_default
                                    }
                                    res, err = post_json(f"/users/{user_id}/addresses", payload)
                                    if res:
                                        st.success("Address added!")
                                        st.rerun()
                                    else:
                                        st.error(f"Failed to add address: {err}")
                                else:
                                    st.warning("Please provide street and city.")

                    btn_b, btn_f = st.columns(2)
                    with btn_b:
                        if st.button("← Back to Review Items", key="b_to_s1", use_container_width=True):
                            st.session_state.checkout_step = 1
                            st.rerun()
                    with btn_f:
                        if st.button("Continue to Payment →", key="to_s3_btn", type="primary", use_container_width=True):
                            if not addresses and not st.session_state.get('selected_address_text'):
                                st.error("Please add a shipping address first.")
                            else:
                                st.session_state.checkout_step = 3
                                st.rerun()

            with col_summary:
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px;">
                    <h4 style="font-size: 15px; font-weight: 700; color: #0f172a; margin-top: 0; margin-bottom: 12px;">Order Snapshot</h4>
                    <div style="font-size: 13px; color: #334155; margin-bottom: 6px;">Total Items: <strong style="color: #0f172a;">{sum(st.session_state.cart.values())}</strong></div>
                    <div style="font-size: 13px; color: #334155; margin-bottom: 6px;">Subtotal: <strong style="color: #0f172a;">${subtotal:,.2f}</strong></div>
                    <div style="font-size: 13px; color: #334155; margin-bottom: 6px;">Shipping: <strong style="color: #0f172a;">{'FREE' if shipping == 0 else f'${shipping:,.2f}'}</strong></div>
                    <div style="font-size: 13px; color: #334155; margin-bottom: 10px;">Tax: <strong style="color: #0f172a;">${tax:,.2f}</strong></div>
                    <div style="border-top: 1px solid #e2e8f0; padding-top: 8px; font-size: 16px; font-weight: 800; color: #0650cc;">
                        Total: ${grand_total:,.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # -------------------------------------------------------------
        # STEP 3: PAYMENT METHOD & FINAL ORDER CONFIRMATION
        # -------------------------------------------------------------
        elif st.session_state.checkout_step == 3:
            st.markdown("<h3 style='font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 14px;'>Step 3: Payment Method & Final Review</h3>", unsafe_allow_html=True)
            
            col_pay, col_confirm = st.columns([7, 5], gap="large")
            with col_pay:
                st.markdown("<h4 style='font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 10px;'>Select Payment Instrument</h4>", unsafe_allow_html=True)
                
                payment_methods = [
                    "💳 Credit Card (Nexus Pay)",
                    "🍎 Apple Pay / Google Pay One-Touch",
                    "📦 Cash on Courier Delivery (COD)",
                    "🏦 Direct Bank Transfer / ACH"
                ]
                chosen_pay = st.radio(
                    "Payment method:",
                    payment_methods,
                    index=0,
                    label_visibility="collapsed",
                    key="s3_pay_radio"
                )
                st.session_state.selected_payment_method = chosen_pay

                # Delivery Address Confirmation Box
                selected_addr_text = st.session_state.get('selected_address_text', 'Default Registered Address')
                st.markdown(f"""
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px; margin: 16px 0;">
                    <div style="font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase;">Shipping Destination</div>
                    <div style="font-size: 13px; font-weight: 600; color: #0f172a; margin-top: 4px;">📍 {selected_addr_text}</div>
                </div>
                """, unsafe_allow_html=True)

                btn_b2, btn_b_cart = st.columns(2)
                with btn_b2:
                    if st.button("← Change Address", key="b_to_s2", use_container_width=True):
                        st.session_state.checkout_step = 2
                        st.rerun()
                with btn_b_cart:
                    if st.button("← Review Cart", key="b_to_s1_from_3", use_container_width=True):
                        st.session_state.checkout_step = 1
                        st.rerun()

            with col_confirm:
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 22px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
                    <h3 style="font-size: 17px; font-weight: 700; color: #0f172a; margin-top: 0; margin-bottom: 14px;">Order Final Summary</h3>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; color: #334155;">
                        <span style="color: #334155;">Items Subtotal ({sum(st.session_state.cart.values())} items)</span><strong style="color: #0f172a;">${subtotal:,.2f}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; color: #334155;">
                        <span style="color: #334155;">Expedited Courier Dispatch</span><strong style="color: #0f172a;">{'FREE' if shipping == 0 else f'${shipping:,.2f}'}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 12px; color: #334155;">
                        <span style="color: #334155;">Estimated Tax (8%)</span><strong style="color: #0f172a;">${tax:,.2f}</strong>
                    </div>
                    <div style="border-top: 1px solid #e2e8f0; padding-top: 12px; display: flex; justify-content: space-between; align-items: baseline;">
                        <span style="font-size: 16px; font-weight: 700; color: #0f172a;">Total Charged</span>
                        <span style="font-size: 24px; font-weight: 800; color: #0650cc;">${grand_total:,.2f}</span>
                    </div>
                    <div style="font-size: 11px; color: #64748b; margin-top: 8px;">
                        PostgreSQL ACID lock guarantees stock protection with zero overselling.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
                
                # Place Order CTA
                if st.button(f"⚡ Confirm Order & Pay (${grand_total:,.2f})", type="primary", use_container_width=True, key="final_order_btn"):
                    if not st.session_state.user:
                        st.error("Please sign in or create an account before confirming your order.")
                    else:
                        user_id = st.session_state.user['id']
                        order_payload = {
                            "user_id": user_id,
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
                            st.toast(f"🎉 Order #{res['order_id']} placed successfully!", icon="✅")
                            st.rerun()


# ==============================================================================
# VIEW: USER PROFILE & ADDRESS MANAGER
# ==============================================================================
elif st.session_state.page == "Profile":
    user = st.session_state.user
    if not user:
        st.warning("Please sign in to view your profile and manage addresses.")
        if st.button("🔑 Go to Sign In / Register", type="primary"):
            set_page("Auth")
            st.rerun()
    else:
        st.markdown(f"<h1 style='color: #0f172a; font-size: 26px; font-weight: 800; margin-bottom: 4px;'>Customer Profile & Addresses</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 13px; color: #64748b; margin-bottom: 24px;'>Manage account credentials, saved shipping destinations, and preferences</p>", unsafe_allow_html=True)

        prof_col, addr_col = st.columns([5, 7], gap="large")
        
        # Profile Details & Edit
        with prof_col:
            st.markdown("<h3 style='color: #0f172a; font-size: 18px; font-weight: 700; margin-bottom: 12px;'>Account Information</h3>", unsafe_allow_html=True)
            with st.form("edit_profile_form"):
                p_name = st.text_input("Full Name", value=user.get('name', ''))
                p_email = st.text_input("Email Address", value=user.get('email', ''))
                st.markdown(f"<div style='font-size: 12px; color: #64748b; margin-bottom: 12px;'>Customer Account ID: #{user.get('id')}</div>", unsafe_allow_html=True)
                
                if st.form_submit_button("Save Profile Changes"):
                    res, err = put_json(f"/users/{user['id']}", {"name": p_name.strip(), "email": p_email.strip().lower()})
                    if res:
                        st.session_state.user['name'] = p_name.strip()
                        st.session_state.user['email'] = p_email.strip().lower()
                        st.success("Profile updated successfully!")
                        st.rerun()
                    else:
                        st.error(f"Failed to update profile: {err}")
            
            if st.button("🚪 Sign Out of Account", use_container_width=True):
                st.session_state.user = None
                st.session_state.cart = {}
                st.session_state.selected_address_id = None
                st.toast("Signed out successfully.")
                set_page("Auth")
                st.rerun()

        # Address Manager
        with addr_col:
            st.markdown("<h3 style='color: #0f172a; font-size: 18px; font-weight: 700; margin-bottom: 12px;'>Saved Delivery Addresses</h3>", unsafe_allow_html=True)
            addresses = fetch_json(f"/users/{user['id']}/addresses") or []
            
            if addresses:
                for a in addresses:
                    aid = a['id']
                    is_def = a.get('is_default', False)
                    def_badge = "<span style='background: #ecfdf5; color: #065f46; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; margin-left: 6px;'>DEFAULT</span>" if is_def else ""
                    st.markdown(f"""
                    <div style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <strong style="color: #0f172a; font-size: 14px;">📍 {a['label']} {def_badge}</strong>
                            <span style="font-size: 12px; color: #64748b;">{a.get('country', 'USA')}</span>
                        </div>
                        <div style="font-size: 13px; color: #334155;">{a['recipient_name']}</div>
                        <div style="font-size: 13px; color: #475569;">{a['street']}, {a['city']}, {a['state']} {a['postal_code']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    c_def, c_del = st.columns([2, 1])
                    with c_def:
                        if not is_def:
                            if st.button("Set Default", key=f"set_def_{aid}", use_container_width=True):
                                put_json(f"/users/{user['id']}/addresses/{aid}/default")
                                st.rerun()
                    with c_del:
                        if st.button("Delete", key=f"del_addr_{aid}", use_container_width=True):
                            delete_req(f"/users/{user['id']}/addresses/{aid}")
                            st.rerun()
            else:
                st.info("No addresses saved yet.")

            # Add New Address Form
            with st.expander("+ Add New Address"):
                with st.form("add_new_addr_profile"):
                    col_a1, col_a2 = st.columns(2)
                    with col_a1:
                        lbl = st.text_input("Label (e.g. Home, Office)", value="Home")
                        rec_name = st.text_input("Recipient Name", value=user.get('name', ''))
                        street = st.text_input("Street Address", placeholder="123 Silicon Way")
                    with col_a2:
                        city = st.text_input("City", placeholder="San Francisco")
                        st_name = st.text_input("State", placeholder="CA")
                        zip_code = st.text_input("Postal Code", placeholder="94105")
                    def_chk = st.checkbox("Make this my default shipping address")

                    if st.form_submit_button("Save New Address"):
                        if street and city:
                            payload = {
                                "label": lbl, "recipient_name": rec_name, "street": street,
                                "city": city, "state": st_name, "postal_code": zip_code,
                                "is_default": def_chk
                            }
                            res, err = post_json(f"/users/{user['id']}/addresses", payload)
                            if res:
                                st.success("Address saved!")
                                st.rerun()
                            else:
                                st.error(f"Error: {err}")
                        else:
                            st.warning("Please provide street and city.")


# ==============================================================================
# VIEW: ORDER HISTORY PAGE
# ==============================================================================
elif st.session_state.page == "Orders":
    user = st.session_state.user
    if not user:
        st.markdown("<h1 style='color: #0f172a; font-size: 26px; font-weight: 800; margin-bottom: 6px;'>Your Order History</h1>", unsafe_allow_html=True)
        st.warning("Please sign in or create an account to view your past orders.")
        if st.button("🔑 Go to Sign In / Register", type="primary"):
            set_page("Auth")
            st.rerun()
    else:
        user_id = user['id']
        st.markdown("<h1 style='color: #0f172a; font-size: 26px; font-weight: 800; margin-bottom: 6px;'>Your Order History</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #475569; font-size: 13px; margin-bottom: 20px;'>Displaying confirmed hardware orders for <strong style='color: #0f172a;'>{user['name']}</strong> (Customer #{user_id})</p>", unsafe_allow_html=True)
        
        orders = fetch_json(f"/orders?user_id={user_id}") or []
        if not orders:
            st.markdown("""
            <div style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 36px; text-align: center;">
                <div style="font-size: 36px; margin-bottom: 8px;">📦</div>
                <h3 style="font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">No orders found yet</h3>
                <p style="font-size: 13px; color: #64748b;">Complete a checkout to record your hardware order here.</p>
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
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px; font-size: 12px; color: #334155; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                        <div><strong style="color: #0f172a;">📍 Shipping Address:</strong> {addr}</div>
                        <div><strong style="color: #0f172a;">💳 Payment:</strong> {pay_method}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    items = fetch_json(f"/orders/{order_id}/items") or []
                    for it in items:
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #f1f5f9; font-size: 13px;">
                            <div>
                                <strong style="color: #0f172a;">{it['product_name']}</strong>
                                <span style="color: #64748b; font-size: 11px; margin-left: 6px;">(ID: {it['product_id']})</span>
                            </div>
                            <div>
                                <span style="color: #64748b;">{it['qty']} × ${float(it['price']):,.2f} = </span>
                                <strong style="color: #0650cc;">${float(it['price']) * it['qty']:,.2f}</strong>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)


# ==============================================================================
# VIEW: AUTHENTICATION (LOGIN / REGISTRATION)
# ==============================================================================
elif st.session_state.page == "Auth":
    st.markdown("<h1 style='color: #0f172a; font-size: 26px; font-weight: 800; margin-bottom: 6px;'>Customer Authentication</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; font-size: 13px; margin-bottom: 20px;'>Sign in with your Nexus account to manage saved addresses and track orders</p>", unsafe_allow_html=True)
    
    if st.session_state.user:
        u = st.session_state.user
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 28px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <div style="font-size: 32px;">👤</div>
                <div>
                    <h3 style="font-size: 18px; font-weight: 800; color: #0f172a; margin: 0;">Currently Signed In as {u.get('name', 'Customer')}</h3>
                    <div style="font-size: 13px; color: #64748b;">{u.get('email', '')} &nbsp;•&nbsp; Account #{u.get('id', '')}</div>
                </div>
            </div>
            <p style="font-size: 13px; color: #475569; margin-bottom: 18px;">
                Your account is active. You can proceed with checkout, manage your shipping addresses, or view past order receipts.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        ca1, ca2, ca3, ca4 = st.columns(4)
        with ca1:
            if st.button("🛍️ Hardware Catalog", use_container_width=True, type="primary"):
                set_page("Catalog")
                st.rerun()
        with ca2:
            if st.button("🛒 Cart & Checkout", use_container_width=True):
                set_page("Cart")
                st.rerun()
        with ca3:
            if st.button("📦 Order History", use_container_width=True):
                set_page("Orders")
                st.rerun()
        with ca4:
            if st.button("🚪 Sign Out", use_container_width=True):
                st.session_state.user = None
                st.session_state.cart = {}
                st.session_state.selected_address_id = None
                st.toast("Signed out successfully.")
                st.rerun()
    else:
        auth_tab1, auth_tab2 = st.tabs(["🔑 Sign In", "📝 Create New Account"])
        
        with auth_tab1:
            st.markdown("<h4 style='color: #0f172a; font-size: 16px; font-weight: 700; margin-bottom: 10px;'>Sign in to your Nexus account</h4>", unsafe_allow_html=True)
            
            # 1-Click Demo Login Shortcut
            st.markdown("""
            <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 12px; margin-bottom: 16px; font-size: 12px; color: #1e40af;">
                💡 <strong>Demo Account Credentials</strong>: <code>demo@nexus.com</code> / <code>demo123</code>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("⚡ 1-Click Quick Login as Demo User", type="primary", use_container_width=True, key="auth_page_demo_btn"):
                res, err = post_json("/auth/login", {"email": "demo@nexus.com", "password": "demo123"})
                if res and "user" in res:
                    st.session_state.user = res["user"]
                    st.session_state.selected_address_id = None
                    st.toast("⚡ Welcome back, Demo User!", icon="✅")
                    target = st.session_state.pop("return_to", "Catalog")
                    set_page(target)
                    st.rerun()
                else:
                    st.error(f"Login failed: {err}")
                    
            st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #e5e7eb;'/>", unsafe_allow_html=True)
            
            with st.form("manual_login_form"):
                in_email = st.text_input("Email Address", placeholder="name@example.com")
                in_pass = st.text_input("Password", type="password")
                
                if st.form_submit_button("Sign In", use_container_width=True):
                    clean_e = in_email.strip()
                    clean_p = in_pass.strip()
                    if clean_e and clean_p:
                        res, err = post_json("/auth/login", {"email": clean_e, "password": clean_p})
                        if res and "user" in res:
                            st.session_state.user = res["user"]
                            st.session_state.selected_address_id = None
                            st.toast(f"Welcome back, {res['user']['name']}!", icon="✅")
                            target = st.session_state.pop("return_to", "Catalog")
                            set_page(target)
                            st.rerun()
                        else:
                            st.error(f"Sign in failed: {err}")
                    else:
                        st.warning("Please provide both email and password.")

        with auth_tab2:
            st.markdown("<h4 style='color: #0f172a; font-size: 16px; font-weight: 700; margin-bottom: 10px;'>Register for a Nexus Account</h4>", unsafe_allow_html=True)
            with st.form("register_form"):
                reg_name = st.text_input("Full Name", placeholder="e.g. Alex Mercer")
                reg_email = st.text_input("Email Address", placeholder="alex@example.com")
                reg_pass = st.text_input("Choose Password", type="password")
                
                if st.form_submit_button("Create Account", use_container_width=True):
                    clean_name = reg_name.strip()
                    clean_email = reg_email.strip()
                    clean_pass = reg_pass.strip()
                    if clean_name and clean_email and clean_pass:
                        res, err = post_json("/auth/register", {"name": clean_name, "email": clean_email, "password": clean_pass})
                        if res and "user" in res:
                            st.session_state.user = res["user"]
                            st.session_state.selected_address_id = None
                            st.toast(f"🎉 Account created! Welcome, {res['user']['name']}!", icon="✅")
                            target = st.session_state.pop("return_to", "Catalog")
                            set_page(target)
                            st.rerun()
                        else:
                            st.error(f"Registration failed: {err}")
                    else:
                        st.warning("Please fill in all fields.")


# ==============================================================================
# VIEW: DATABASE TELEMETRY
# ==============================================================================
elif st.session_state.page == "Databases":
    st.markdown("<h1 style='color: #0f172a; font-size: 26px; font-weight: 800; margin-bottom: 6px;'>System & Database Telemetry</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 13px; color: #64748b; margin-bottom: 20px;'>Live query routing across PostgreSQL (ACID & Auth), MongoDB (Catalog), and ChromaDB (Vector Similarity)</p>", unsafe_allow_html=True)
    
    debug_info = fetch_json("/debug/requests")
    if debug_info and 'requests' in debug_info and debug_info['requests']:
        st.table(debug_info['requests'])
    else:
        st.info("No queries logged yet.")
