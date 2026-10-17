import sys
import os

# Add parent directory to path to import db queries
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.mongo_queries import get_mongo_client, store_product_image

# Clean, modern card design — light background, coloured header band, crisp typography
CATEGORY_THEMES = {
    'laptops': {'band': '#6366f1', 'badge': '#eef2ff', 'badge_text': '#4338ca',
                'price': '#4338ca', 'icon': '💻'},
    'shoes':   {'band': '#10b981', 'badge': '#ecfdf5', 'badge_text': '#065f46',
                'price': '#059669', 'icon': '👟'},
    'books':   {'band': '#f97316', 'badge': '#fff7ed', 'badge_text': '#9a3412',
                'price': '#ea580c', 'icon': '📚'},
    'phones':  {'band': '#0ea5e9', 'badge': '#f0f9ff', 'badge_text': '#0c4a6e',
                'price': '#0284c7', 'icon': '📱'},
}

def _esc(text):
    """Escape XML special characters for safe SVG embedding."""
    return (str(text)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))

def _wrap_name(name, max_len=20):
    """Split long names into two lines for the SVG card."""
    if len(name) <= max_len:
        return name, ''
    # Try to split at a space near the middle
    mid = len(name) // 2
    split = name.rfind(' ', 0, mid + 8)
    if split == -1:
        split = mid
    return name[:split], name[split:].strip()

def generate_product_svg(name, category, price, product_id):
    theme = CATEGORY_THEMES.get(category, CATEGORY_THEMES['laptops'])
    line1, line2 = _wrap_name(_esc(name))
    cat_label    = _esc(category.upper())
    price_label  = _esc(f"${price:,.2f}")
    pid_label    = _esc(product_id)
    band         = theme['band']
    badge_bg     = theme['badge']
    badge_txt    = theme['badge_text']
    price_col    = theme['price']
    icon         = theme['icon']

    # Vertical position for name: shift up if single line, stay if two lines
    name_y1 = '198' if line2 else '208'
    name_y2 = '218'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="280" viewBox="0 0 400 280">

  <!-- Card shadow / border -->
  <rect x="2" y="2" width="396" height="276" rx="14" fill="#00000018"/>
  <!-- White card -->
  <rect width="396" height="274" rx="14" fill="#ffffff"/>

  <!-- Coloured header band -->
  <rect width="396" height="148" rx="14" fill="{band}"/>
  <!-- Cover bottom-radius of band -->
  <rect y="134" width="396" height="14" fill="{band}"/>

  <!-- Subtle dot pattern on band -->
  <circle cx="30"  cy="30"  r="40" fill="#ffffff" fill-opacity="0.06"/>
  <circle cx="370" cy="20"  r="55" fill="#ffffff" fill-opacity="0.05"/>
  <circle cx="340" cy="130" r="35" fill="#ffffff" fill-opacity="0.05"/>
  <circle cx="60"  cy="120" r="28" fill="#ffffff" fill-opacity="0.06"/>

  <!-- Large category icon -->
  <text x="200" y="102"
        font-size="68"
        text-anchor="middle"
        dominant-baseline="middle"
        font-family="Segoe UI Emoji, Apple Color Emoji, Noto Color Emoji, sans-serif">{icon}</text>

  <!-- Category badge -->
  <rect x="145" y="154" width="106" height="22" rx="11" fill="{badge_bg}"/>
  <text x="198" y="169"
        font-size="10.5"
        font-weight="700"
        fill="{badge_txt}"
        text-anchor="middle"
        font-family="system-ui, -apple-system, Arial, sans-serif"
        letter-spacing="1.2">{cat_label}</text>

  <!-- Product name (up to two lines) -->
  <text x="198" y="{name_y1}"
        font-size="17"
        font-weight="700"
        fill="#111827"
        text-anchor="middle"
        font-family="system-ui, -apple-system, Arial, sans-serif">{line1}</text>
  <text x="198" y="{name_y2}"
        font-size="17"
        font-weight="700"
        fill="#111827"
        text-anchor="middle"
        font-family="system-ui, -apple-system, Arial, sans-serif">{line2}</text>

  <!-- Divider -->
  <line x1="40" y1="230" x2="356" y2="230" stroke="#f3f4f6" stroke-width="1.2"/>

  <!-- Price -->
  <text x="198" y="255"
        font-size="20"
        font-weight="800"
        fill="{price_col}"
        text-anchor="middle"
        font-family="system-ui, -apple-system, Arial, sans-serif">{price_label}</text>

  <!-- Product ID micro label -->
  <text x="198" y="272"
        font-size="9"
        fill="#d1d5db"
        text-anchor="middle"
        font-family="monospace">{pid_label}</text>

  <!-- Outer border -->
  <rect x="0.5" y="0.5" width="395" height="273" rx="14"
        fill="none" stroke="#e5e7eb" stroke-width="1"/>
</svg>'''
    return svg.encode('utf-8')


def main():
    client   = get_mongo_client()
    products = list(client["shop"].products.find(
        {}, {"_id": 0, "product_id": 1, "name": 1, "category": 1, "price": 1}
    ))

    print(f"Generating SVG cards for {len(products)} products...")
    for prod in products:
        pid       = prod["product_id"]
        svg_bytes = generate_product_svg(prod["name"], prod["category"], prod["price"], pid)
        store_product_image(pid, svg_bytes, mime_type="image/svg+xml")
        print(f"  OK  {pid} — {prod['name']}")

    print(f"\nDone: {len(products)} product cards stored in MongoDB.")


if __name__ == "__main__":
    main()
