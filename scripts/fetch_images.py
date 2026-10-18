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
    cat_label    = _esc(category.upper())
    pid_label    = _esc(product_id)
    band         = theme['band']
    badge_bg     = theme['badge']
    badge_txt    = theme['badge_text']
    icon         = theme['icon']

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="220" viewBox="0 0 400 220">
  <defs>
    <linearGradient id="bgGrad_{pid_label}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{band}" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="{band}" stop-opacity="0.80"/>
    </linearGradient>
    <radialGradient id="glow_{pid_label}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Background container with subtle border -->
  <rect width="400" height="220" rx="10" fill="url(#bgGrad_{pid_label})"/>
  
  <!-- Subtle technical grid pattern -->
  <circle cx="200" cy="110" r="85" fill="url(#glow_{pid_label})"/>
  <circle cx="40"  cy="30"  r="50" fill="#ffffff" fill-opacity="0.05"/>
  <circle cx="360" cy="190" r="60" fill="#ffffff" fill-opacity="0.05"/>
  <line x1="20" y1="110" x2="130" y2="110" stroke="#ffffff" stroke-opacity="0.2" stroke-dasharray="3,3"/>
  <line x1="270" y1="110" x2="380" y2="110" stroke="#ffffff" stroke-opacity="0.2" stroke-dasharray="3,3"/>

  <!-- Large Category Icon -->
  <text x="200" y="115"
        font-size="64"
        text-anchor="middle"
        dominant-baseline="middle"
        font-family="Segoe UI Emoji, Apple Color Emoji, Noto Color Emoji, sans-serif">{icon}</text>

  <!-- Precision Category Watermark & SKU -->
  <rect x="14" y="14" width="85" height="20" rx="4" fill="{badge_bg}" fill-opacity="0.95"/>
  <text x="56" y="27"
        font-size="9"
        font-weight="700"
        fill="{badge_txt}"
        text-anchor="middle"
        font-family="system-ui, -apple-system, Arial, sans-serif"
        letter-spacing="1">{cat_label}</text>

  <rect x="320" y="14" width="66" height="20" rx="4" fill="#000000" fill-opacity="0.25"/>
  <text x="353" y="27"
        font-size="9"
        font-weight="600"
        fill="#ffffff"
        text-anchor="middle"
        font-family="monospace">{pid_label}</text>

  <!-- Outer stroke -->
  <rect x="0.5" y="0.5" width="399" height="219" rx="9.5"
        fill="none" stroke="#000000" stroke-opacity="0.1"/>
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
