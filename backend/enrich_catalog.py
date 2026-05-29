"""
enrich_catalog.py
=================
AI-Powered Ecommerce Catalog Enrichment Engine for Soham Gift Platform

Transforms supplier-style catalog products into premium ecommerce-ready 
corporate gifting listings.

Usage:
    python enrich_catalog.py --dry-run          # Preview all, no DB changes
    python enrich_catalog.py --save             # Enrich & save all products
    python enrich_catalog.py --save --sku SKU   # Enrich one product by SKU
    python enrich_catalog.py --save --name NAME # Enrich one product by name
    python enrich_catalog.py --save --missing-only  # Only enrich incomplete products
"""

import os
import sys
import re
import json
import argparse
import textwrap
from decimal import Decimal

# ─── Django Setup ────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from products.models import Product, Category


# ═══════════════════════════════════════════════════════════════════════════════
# KNOWLEDGE BASE
# All corporate gifting enrichment templates live here.
# ═══════════════════════════════════════════════════════════════════════════════

CATEGORY_TONE = {
    "Office Gifts":         "corporate office environment",
    "Stationery":           "executive desk and boardroom",
    "Corporate Gift Sets":  "premium corporate gifting",
    "Drinkware":            "health-conscious executive lifestyle",
    "Travel Accessories":   "business travel and executive mobility",
    "Tech Gifts":           "modern tech-forward workspace",
    "Executive Pens":       "luxury writing instruments",
    "Desk Accessories":     "executive desk aesthetics",
    "Promotional Merchandise": "high-impact brand promotion",
}

# ─── Component Detection ──────────────────────────────────────────────────────
COMPONENT_KEYWORDS = {
    "pen":          ["pen", "ballpen", "ballpoint", "writing", "writer", "ink"],
    "keychain":     ["keychain", "keyring", "key chain", "key ring", "keyholder"],
    "diary":        ["diary", "notebook", "journal", "notepad", "notes", "elastic"],
    "cardholder":   ["cardholder", "card holder", "card case", "business card"],
    "perfume":      ["perfume", "fragrance", "scent", "deodorant", "perfumo"],
    "wallet":       ["wallet", "purse", "card wallet", "slim wallet"],
    "mug":          ["mug", "cup", "coffee mug", "tea mug"],
    "bottle":       ["bottle", "flask", "tumbler", "sipper", "hydro"],
    "copper":       ["copper", "ayurvedic"],
    "insulated":    ["hydrox", "insulated", "vacuum", "thermal", "double wall"],
    "leather":      ["leather", "leatherette", "pu leather", "faux leather"],
    "metal":        ["metal", "metallic", "stainless", "aluminium", "steel"],
    "ceramic":      ["ceramic", "porcelain"],
    "gift_set":     ["set", "trio", "duo", "combo", "collection", "gift set"],
    "badge_access": ["id", "badge", "lanyard", "access card"],
}

def detect_components(name: str, image: str = "") -> list:
    """Detect product components from name and image filename."""
    text = (name + " " + (image or "")).lower()
    found = []
    for component, keywords in COMPONENT_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                found.append(component)
                break
    return list(set(found))


# ─── Title Enrichment ─────────────────────────────────────────────────────────

SUPPLIER_CODE_PATTERN = re.compile(
    r'\s*\(?\s*[Ss][Rr]\.?\s*\d{2,4}\s*\)?|\s*\(?\s*model\s*[#:]?\s*\w+\s*\)?',
    re.IGNORECASE
)

TITLE_UPGRADES = {
    # Exact / partial match → upgraded title
    "premium ceramic mug":              "Soham Premium Ceramic Coffee Mug | Custom Logo Corporate Gift",
    "luxury leather notebook":          "Soham Executive Leather Notebook | 100 GSM Premium Corporate Diary",
    "silver metallic pen":              "Soham Classic Executive Metallic Pen | Personalized Corporate Pen",
    "classic pen & keychain duo":       "Soham Executive Pen & Keychain Gift Set | Premium Branded Duo",
    "classic pen and keychain duo":     "Soham Executive Pen & Keychain Gift Set | Premium Branded Duo",
    "stylish pen & keyring":            "Soham Stylish Pen & Keyring Corporate Set | Promotional Gift",
    "stylish pen and keyring":          "Soham Stylish Pen & Keyring Corporate Set | Promotional Gift",
    "executive trio":                   "Soham Executive Trio Gift Set | Premium Pen, Keychain & Cardholder",
    "corporate gift set":               "Soham Signature Corporate Gift Set | Pen, Keychain & Cardholder",
    "perfumo luxury set":               "Soham Perfumo Luxury Gift Set | Wallet, Perfume, Pen & Cardholder",
    "red elastic notebook set":         "Soham Red Elastic Diary & Pen Set | Premium Branded Stationery",
    "black mars notebook set":          "Soham Black Mars Executive Diary & Pen Set | Corporate Stationery",
    "premium pen & keychain":           "Soham Premium Pen & Keychain Gift Set | Executive Branded Combo",
    "premium pen and keychain":         "Soham Premium Pen & Keychain Gift Set | Executive Branded Combo",
    "elegant pen & cardholder":         "Soham Elegant Executive Pen & Cardholder Set | Networking Gift",
    "elegant pen and cardholder":       "Soham Elegant Executive Pen & Cardholder Set | Networking Gift",
    "male & female perfume set":        "Soham Dual Signature Perfume Gift Set | His & Hers Corporate Gift",
    "male and female perfume set":      "Soham Dual Signature Perfume Gift Set | His & Hers Corporate Gift",
    "copper hydration set":             "Soham Pure Copper Hydration Gift Set | 500ml Bottle & 2 Mugs",
    "hydrox black gift set":            "Soham HydroX Black Insulated Bottle Gift Set | Pen & Keychain",
    "hydrox white gift set":            "Soham HydroX White Insulated Bottle Gift Set | Pen & Keychain",
    "red elastic diary set":            "Soham Red Elastic Executive Diary Set | Premium Corporate Stationery",
    "black mars diary set":             "Soham Black Mars Executive Diary & Pen Set | Corporate Stationery",
    "executive pen & keychain":         "Soham Executive Pen & Keychain Gift Set | Premium Branded Combo",
    "executive pen and keychain":       "Soham Executive Pen & Keychain Gift Set | Premium Branded Combo",
    "professional pen & cardholder":    "Soham Professional Pen & Cardholder Gift Set | Executive Combo",
    "professional pen and cardholder":  "Soham Professional Pen & Cardholder Gift Set | Executive Combo",
}

def clean_supplier_title(name: str) -> str:
    """Remove supplier codes (Sr 125, etc.) from product name."""
    cleaned = SUPPLIER_CODE_PATTERN.sub('', name).strip()
    cleaned = re.sub(r'\s{2,}', ' ', cleaned)
    return cleaned

import re
import re

def generate_premium_title(title: str, category: str = "", components=None):
    if not title:
        return "Premium Corporate Gift"

    # Remove numbers
    title = re.sub(r'\b\d{2,5}\b', '', title)

    # Remove supplier/internal words
    remove_words = [
        'Soham',
        'RC',
        'DBKP',
        'DBPP',
        'BPK',
        'BTP',
        'TC',
        'SG',
        'Model',
        'Code'
    ]

    words = title.split()

    cleaned_words = [
        word for word in words
        if word.upper() not in [w.upper() for w in remove_words]
    ]

    cleaned = " ".join(cleaned_words)

    # Remove extra spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    # Premium naming improvements
    cleaned = cleaned.replace("Pen", "Executive Pen")
    cleaned = cleaned.replace("Bottle", "Steel Bottle")

    return cleaned

# ─── Description Templates ────────────────────────────────────────────────────

DESCRIPTION_TEMPLATES = {
    "mug": """Elevate every morning ritual with the **{title}** — a thoughtfully crafted ceramic mug designed for the discerning corporate professional. Engineered from premium-grade ceramic with a smooth, glazed finish, this mug radiates understated elegance on any executive desk.

Perfectly suited for personalised corporate gifting, this mug can be embossed with your company logo, brand colours, or a custom message — transforming a simple coffee break into a powerful brand moment. Whether gifted at a product launch, annual celebration, or as an onboarding welcome kit, it creates a lasting impression.

**Why Executives Love It:**  
The ergonomic handle ensures a comfortable grip during long meetings or focused work sessions. The wide-mouth opening makes it ideal for stirring, and the generous capacity keeps your beverage warm through extended office hours. The high-quality ceramic retains heat efficiently while remaining safe for daily use.

**Perfect For:**  
Corporate welcome kits, employee recognition programs, client gifting, festive gift baskets, desk personalisation, and brand promotional campaigns. Each piece arrives in a premium gift-ready box that adds visual impact to your brand presentation.

**Bulk Ordering:**  
Soham Gift specialises in high-volume corporate orders with consistent quality standards. Minimum order quantities start from 50 units with competitive pricing brackets that improve at 100, 250, and 500 units.

*Customisation available: logo printing, name engraving, custom message, and brand colour matching. Contact our gifting desk for bespoke ordering.*""",

    "diary_pen": """Introduce elegance to every meeting room with the **{title}** — an executive diary and pen set crafted for professionals who appreciate the finer details. This premium set combines a high-quality diary featuring luxurious {cover_material} cover and smooth {paper_gsm} GSM writing paper, paired with a precision-engineered metallic pen that delivers effortless writing.

Designed for the boardroom, client meetings, and everyday executive use, this set projects professionalism and sophistication. The supple cover wraps around the diary with an elastic pen loop that keeps both pieces secure and organised — ready for any high-powered setting.

**For the Modern Executive:**  
Whether capturing strategies in a boardroom, sketching product roadmaps, or journaling goals — this set is engineered to keep pace with ambition. The pen features a smooth-flow ink mechanism that glides across the premium writing surface without skipping or bleeding.

**Corporate Branding:**  
The wide, debossable cover panel is ideal for laser engraving your company logo, conference hashtag, or recipient's name — creating a personalised keepsake that reinforces your brand story at every meeting.

**Gifting Contexts:**  
Welcome kits for new joiners, farewell gifts, conference and summit giveaways, incentive rewards, performance recognition gifts, and annual day hampers. Arrives in a premium gift box suitable for direct desk delivery.

**Bulk Orders:**  
Available with logo branding from 50 units, with volume pricing at 100, 250, and 500 units. Contact Soham Gift for bulk corporate orders with customisation.

*All sets are individually quality-checked and packaged in our signature Soham Gift boxes. Custom inserts and ribbon tying available.*""",

    "pen_keychain": """Make every handshake memorable with the **{title}** — a premium pen and keychain duo curated for impactful corporate gifting. This thoughtfully assembled set pairs a sleek metallic writing instrument with a polished, durable keychain — two everyday essentials that your recipients will use and appreciate long after the gifting occasion.

The pen is crafted with a smooth-click mechanism and premium ink that ensures consistent, clean writing. The keychain features a robust metal clasp that holds keys securely while adding a refined accent to any key ring, bag, or laptop bag zipper.

**The Power of Everyday Gifting:**  
Unlike gifts that end up in drawers, a quality pen and keychain are used daily — keeping your brand, logo, or message visible in clients' hands, desks, and pockets. This makes it one of the highest-ROI corporate gift categories for brand recall.

**Customisation Options:**  
Both the pen barrel and keychain tag can be laser-engraved or screen-printed with your company logo, name, event name, or a short motivational message. The result is a premium branded item that doubles as a walking advertisement.

**Ideal For:**  
Client meetings, trade show giveaways, new joiner welcome kits, bulk promotional campaigns, dealer gifting, conference bags, and appreciation gifts. The set arrives in a compact, premium gift box perfect for mailing or desk delivery.

**Volume Pricing:**  
With Soham Gift's volume pricing structure, bulk orders of 100+ units unlock significant per-unit savings while maintaining zero compromise on quality. Contact us for a custom quotation.

*Minimum Order Quantity: 25 units. Available with custom gift wrapping and personalised message cards.*""",

    "pen_cardholder": """Command attention in every professional encounter with the **{title}** — a refined executive set designed for those who lead with class. Combining a precision-crafted metallic pen with a sleek, business card holder, this duo transforms essential professional tools into statement gifting pieces.

The cardholder features a smooth-sliding ejection mechanism and elegant matte or brushed metallic finish — ensuring your business cards are presented with the confidence they deserve. The pen delivers a premium writing experience with its balanced weight and smooth ink flow, making it as comfortable in boardrooms as it is impressive on a desk.

**Why It Works:**  
First impressions count, and handing out a business card from a premium cardholder signals professionalism before a word is spoken. Paired with a branded pen, this set becomes one of the most functional and high-visibility gifts in the corporate gifting space.

**Ideal For:**  
New joiner welcome kits, client appreciation gifts, networking events, career milestone celebrations, executive conference giveaways, and premium promotional campaigns.

**Customisation:**  
Engrave your company name or logo on the pen barrel and cardholder surface. Both pieces available in multiple colour finishes to match your brand palette. Arrive beautifully packaged in a premium Soham Gift presentation box.

*Available from 25 units. Volume pricing available at 100, 250, and 500+ units. Contact our corporate gifting team for custom branding specifications.*""",

    "executive_trio": """Set the gold standard for corporate gifting with the **{title}** — a three-piece executive luxury set that embodies professional excellence. This sophisticated collection brings together a premium metallic pen, an elegant keychain, and a sleek business cardholder in one curated presentation — the ultimate combination for impressing clients, rewarding top performers, and welcoming senior executives.

Engineered for precision and presence, each piece in the trio reflects the meticulous craftsmanship that Soham Gift is renowned for. The pen glides with smooth ink flow. The keychain is built to last decades. The cardholder holds 10–12 cards with ease and ejects them with a single press.

**A Gift That Speaks Volumes:**  
When you present this trio at a corporate event, client meeting, or year-end celebration, it communicates that your brand values quality, thoughtfulness, and attention to detail. Each piece can be individually laser-engraved — or the entire set can carry a unified branding theme with consistent logos and colour finishes.

**The Three-Piece Advantage:**  
Unlike single-item gifts, a trio set delivers perceived value that far exceeds its price point. Recipients use all three items daily — amplifying brand exposure across home, office, and travel touchpoints.

**Perfect For:**  
C-suite gifting, investor relations, senior leadership rewards, client acquisition campaigns, product launches, summit giveaways, and franchise partner gifts. Presented in a rigid gift box with satin lining.

*Minimum Order: 20 units. Premium custom gift wrapping, branded ribbon, and personalised message cards available. Choose from Silver, Gold, and Gunmetal finish variants.*""",

    "perfume_set": """Indulge in the art of gifting with the **{title}** — an opulent fragrance experience curated for the discerning executive lifestyle. This exclusive set presents a collection of premium eau de parfum in an elegantly designed gift box, making it one of the most coveted luxury corporate gifts for special occasions.

Crafted for the modern professional who appreciates sensory excellence, the fragrances strike a confident balance between sophistication and longevity. Whether for celebrating milestones, client appreciation, or festive gifting seasons, this perfume set communicates luxury without reservation.

**A Sensory Brand Statement:**  
Fragrance is one of the most emotionally resonant gift categories — associated with luxury, memory, and personal care. Gifting a premium perfume set positions your brand as thoughtful, generous, and premium. The presentation box is gift-ready straight from delivery.

**Gifting Occasions:**  
Diwali hampers, corporate anniversary gifts, client retention gifts, VIP dealer gifting, year-end CEO gifts, wedding favours, and premium event giveaways. The set photographs beautifully for social media unboxing coverage.

**Customisation:**  
Gift box can be custom-branded with your company logo and message. Available with a personalised message card, custom ribbon, and premium tissue wrapping inside the box.

*Minimum Order: 10 units. This product is especially popular for festive season corporate gifting from October–January. Early booking recommended.*""",

    "copper_set": """Reconnect with ancient wellness wisdom through the **{title}** — a premium copper hydration set rooted in Ayurvedic tradition and reimagined for the modern executive. This exquisite set includes a hand-crafted 500ml pure copper bottle and two elegant copper mugs — presenting a complete hydration ritual that is as beneficial as it is beautiful.

Copper vessels have been used for centuries in Ayurvedic practice to promote digestive health, immunity, and vitality. The naturally antibacterial properties of copper make it an ideal material for storing and serving water — combining wellness with luxury in a gift that recipients will genuinely treasure.

**Craftsmanship Meets Wellness:**  
Each piece is hand-finished with traditional artisan techniques, resulting in a rich, warm copper patina that deepens beautifully with use. The bottle's leakproof cap ensures secure carrying, while the mugs hold approximately 150ml each — perfect for serving water or chai at your desk.

**Premium Gifting Appeal:**  
The copper set is one of the highest emotional-value corporate gifts — it is both functional and meaningful, wellness-oriented, and deeply culturally resonant. It stands apart from typical branded merchandise by offering a lifestyle upgrade.

**Perfect For:**  
Diwali gift hampers, senior executive returns, wellness-focused employee gifting, yoga retreat gifts, Ayurveda brand launches, and high-value client appreciation. Presented in a premium wooden gift box or luxury white rigid box.

*Hand-crafted. Minor surface variations are natural and reflect authentic craftsmanship. Personalised engraving available on bottle. Minimum Order: 15 units.*""",

    "hydrox_bottle": """Hydrate in style with the **{title}** — a premium insulated bottle and executive gift set built for the active corporate professional. Featuring the acclaimed HydroX double-wall vacuum insulation technology, this sleek bottle keeps beverages cold for 24 hours and hot for 12 hours — making it the ultimate desk and travel companion.

Paired with a precision-crafted metallic pen and a durable keychain, this complete set delivers maximum gifting value across multiple daily use cases. The bottle's powder-coated finish is fingerprint-resistant, and its wide-mouth design is compatible with ice cubes and fruit infusers.

**Why HydroX?**  
The HydroX series has become one of the most-requested corporate gifting items in the Indian market, combining premium aesthetics, superior insulation performance, and exceptional logo branding space. Whether on the boardroom table, gym bag, or travel kit — this bottle makes your brand visible everywhere.

**Customisation:**  
The bottle's cylindrical body offers a large, flat branding surface ideal for laser engraving or UV digital printing. The pen can be barrel-printed and the keychain can be engraved — giving you a fully branded three-piece gift set.

**Ideal For:**  
Sports events, health & wellness campaigns, year-end employee gifts, sales incentive rewards, client welcome kits, and large-scale bulk gifting programs. Arrives in a premium branded gift box with foam insert.

*Available in Black and White. Minimum Order: 25 units. BPA-free, food-safe stainless steel interior. NSF/ANSI certified materials.*""",

    "perfumo_luxury": """Redefine luxury gifting with the **{title}** — a curated four-piece executive collection that brings together a premium wallet, an exclusive fragrance, a precision pen, and a sleek cardholder into one spectacular gift experience. This comprehensive set is designed for those rare occasions when only the finest will do.

Presented in a rigid, satin-lined gift box with individual cushioned compartments for each piece, this set creates an unboxing experience that rivals the finest luxury brands. The wallet is crafted from premium leatherette with multiple card slots and a clean bill compartment. The perfume is a sophisticated, long-lasting fragrance. The pen writes with beautiful precision. The cardholder holds cards with a smooth-ejection mechanism.

**When Occasions Demand the Extraordinary:**  
This four-piece set is reserved for your most valued relationships — senior clients, board members, key business partners, and top performers who have gone above and beyond. Presenting this set signals that your appreciation is as premium as your brand.

**Brand Integration:**  
Each piece carries discreet co-branding opportunities — the wallet interior, pen barrel, cardholder surface, and gift box lid can all carry your logo. The assembled result is a branded luxury hamper that recipients remember for years.

**Perfect For:**  
Corporate anniversary milestones, C-suite gifting, investor relations gifts, luxury event giveaways, celebrity endorsement kits, and board meeting gifts. This set generates significant unboxing content value on social media.

*Minimum Order: 10 units. Customisation consultations available. Arrives in a premium outer carton suitable for courier delivery without additional packaging.*""",

    "default": """Elevate your corporate gifting experience with the **{title}** — a premium product crafted to reflect excellence, warmth, and brand sophistication. Designed for the Indian corporate market, this product combines functional quality with premium aesthetics to create gifting moments that truly resonate.

Whether you're expressing appreciation to a valued client, welcoming a new team member, or celebrating a company milestone — this product delivers the perfect blend of practicality and luxury. It's not just a gift; it's a statement of your brand's commitment to quality.

**Designed for Impact:**  
Every detail — from the materials selected to the finish applied — is chosen to create a lasting impression. Soham Gift's quality assurance ensures each unit meets the highest standards before it reaches your recipient.

**Customisation Capabilities:**  
Your brand can come alive on this product through laser engraving, screen printing, UV digital printing, or embossing — depending on the surface and material. Our design team will guide you through the full customisation process to ensure your logo and message look premium and consistent.

**Corporate Gifting Applications:**  
New joiner welcome kits, client retention gifts, dealer incentive programs, performance awards, festive Diwali hampers, conference bags and event giveaways, product launches, and CSR initiatives.

**Volume Benefits:**  
Soham Gift's tiered pricing structure rewards higher order quantities with better per-unit rates — allowing you to maximise your gifting budget without compromising on quality. 

*Contact our corporate gifting desk for bespoke bulk orders, custom packaging, and personalised message card programs.*"""
}

def select_description_template(components: list, category: str) -> str:
    """Select the best description template based on detected components."""
    comp_set = set(components)
    
    if "mug" in comp_set and "bottle" not in comp_set:
        return "mug"
    elif "copper" in comp_set:
        return "copper_set"
    elif "insulated" in comp_set or "hydrox" in comp_set.union({"hydrox" for c in comp_set if "hydro" in components}):
        return "hydrox_bottle"
    elif "wallet" in comp_set and "perfume" in comp_set:
        return "perfumo_luxury"
    elif "perfume" in comp_set:
        return "perfume_set"
    elif "pen" in comp_set and "keychain" in comp_set and "cardholder" in comp_set:
        return "executive_trio"
    elif "pen" in comp_set and "cardholder" in comp_set:
        return "pen_cardholder"
    elif "pen" in comp_set and "keychain" in comp_set:
        return "pen_keychain"
    elif ("diary" in comp_set or "notebook" in comp_set) and "pen" in comp_set:
        return "diary_pen"
    return "default"
def generate_description(product_name: str, title: str, components: list, specs: dict) -> str:
    """Generate clean premium ecommerce description."""

    material = specs.get("Material", "Premium quality material")
    color = specs.get("Color", "Elegant finish")
    packaging = specs.get("Packaging", "Premium gift box")
    usage = specs.get("Usage", "Corporate gifting")

    description = f"""
A premium corporate gifting product designed for professional branding and executive use.

Key Features:
• Elegant premium finish
• Modern professional styling
• Ideal for corporate gifting
• Suitable for logo branding
• Durable and practical design

Specifications:
Material: {material}
Color: {color}
Packaging: {packaging}
Usage: {usage}
"""

    return description.strip()


# ─── Key Features ─────────────────────────────────────────────────────────────

FEATURES_BY_COMPONENT = {
    "mug": [
        "🫖 Premium food-grade ceramic construction with smooth glazed finish",
        "🎨 Wide-mouth design for easy filling, stirring, and cleaning",
        "✋ Ergonomic handle with comfortable grip even when hot",
        "🔥 Excellent heat retention — keeps beverages warm longer",
        "🏷️ Premium branding surface ideal for logo printing or engraving",
        "📦 Arrives in a premium gift-ready presentation box",
        "🎁 Perfect for corporate welcome kits, festive hampers, and desk gifting",
        "🧼 Microwave and dishwasher safe — built for daily executive use",
    ],
    "pen": [
        "✒️ Premium metallic barrel with smooth, professional finish",
        "🖊️ Ultra-smooth ink flow mechanism — skip-free writing on all paper types",
        "⚖️ Balanced weight distribution for comfortable long-form writing",
        "🔄 Click mechanism with satisfying tactile response",
        "🏷️ Laser-engravable barrel for logo, name, or message branding",
        "🎁 Elegant gift-ready packaging — no extra wrapping required",
        "🖋️ Suitable for everyday executive use, client meetings, and conferences",
    ],
    "keychain": [
        "🔑 Heavy-duty metal clasp with secure locking ring",
        "✨ Premium brushed or polished metallic finish — scratch resistant",
        "🏷️ Engravable surface for logo, monogram, or brand message",
        "💪 Durable alloy construction — built to last years of daily use",
        "🎁 Compact and lightweight — perfect as a standalone or add-on gift",
        "🌟 Consistent finish across bulk orders — ideal for large gifting programs",
    ],
    "diary": [
        "📖 Premium {cover_material} cover with debossing-ready surface",
        "📝 {paper_gsm} GSM acid-free writing paper for superior ink experience",
        "📎 Integrated elastic pen loop keeps pen secure at all times",
        "🔖 Ribbon bookmark for quick page access in meetings",
        "📅 Dated or undated pages with monthly planner spreads",
        "📏 A5 size — ideal for executive use in meetings and conferences",
        "🏷️ Front and back cover available for laser engraving or foil stamping",
        "📦 Arrives in a branded gift box for premium presentation",
    ],
    "notebook": [
        "📖 Premium {cover_material} cover with debossing-ready surface",
        "📝 High GSM acid-free paper for ink-bleed-free writing",
        "🔖 Ribbon bookmark for quick page access",
        "📐 A5 executive size — perfect balance of portability and space",
        "🏷️ Front and back cover available for laser engraving",
        "📦 Arrives in a branded gift box for premium presentation",
    ],
    "cardholder": [
        "💼 Holds 10–12 standard business cards with ease",
        "⚡ Single-press ejection mechanism for smooth card presentation",
        "✨ Premium metallic / leatherette finish in multiple colour options",
        "🕶️ Slim profile — fits in shirt pocket or laptop bag with ease",
        "🏷️ Engravable surface for brand logo or monogram",
        "🎁 Premium packaging — gift-ready from the box",
    ],
    "perfume": [
        "🌸 Long-lasting premium eau de parfum — 8+ hours wear time",
        "🎨 Sophisticated fragrance profile — confident, modern, and refined",
        "💎 Elegantly designed bottle with premium cap and spray atomiser",
        "🎁 Gift-ready luxury presentation box with satin tissue lining",
        "👔 Suitable for everyday professional and formal occasions",
        "🌿 Alcohol-based formulation with skin-safe certified ingredients",
        "📸 Photogenic unboxing experience — ideal for social media campaigns",
    ],
    "wallet": [
        "💳 Multiple card slots (6–8) and a dedicated bill compartment",
        "🛡️ RFID blocking lining protects cards from digital theft",
        "🎨 Premium leatherette exterior with stitched edge detailing",
        "📐 Slim form factor — no bulge in jacket or trouser pocket",
        "🏷️ Interior monogramming or exterior logo embossing available",
        "💪 Reinforced stitching for extended daily use durability",
    ],
    "bottle": [
        "💧 BPA-free, food-safe stainless steel interior",
        "🌡️ Double-wall vacuum insulation — cold 24 hrs, hot 12 hrs",
        "🔒 Leakproof cap with secure locking mechanism",
        "🧊 Wide-mouth opening — fits ice cubes and fruit infusers",
        "🏷️ Large flat branding surface for laser engraving or UV printing",
        "♻️ Eco-friendly reusable alternative to single-use plastic bottles",
        "🎁 Arrives in a premium gift box with foam insert",
    ],
    "copper": [
        "🥇 Made from pure 99.9% food-grade copper",
        "🌿 Ayurvedic tradition — copper-stored water has wellness benefits",
        "🔬 Naturally antibacterial surface — inhibits microbial growth",
        "🎨 Hand-finished with traditional artisan copper techniques",
        "🔒 Leakproof cap with food-safe rubber gasket",
        "✨ Develops beautiful patina with regular use — unique to each piece",
        "🎁 Arrives in a premium wooden or luxury rigid gift box",
        "🏷️ Engraving available on bottle body for corporate branding",
    ],
    "insulated": [
        "🌡️ Advanced double-wall vacuum insulation technology",
        "❄️ Keeps drinks cold for 24 hours, hot for 12 hours",
        "🔒 100% leakproof design — safe for bags and laptop cases",
        "🧊 Wide mouth accommodates ice cubes and cleaning brushes",
        "🏷️ Laser engravable powder coat finish — premium branding surface",
        "♻️ Eco-conscious reusable design — reduces plastic bottle usage",
        "🎁 Gift-ready box with foam insert for safe transport",
    ],
    "gift_set": [
        "🎁 Curated multi-piece set in a premium presentation gift box",
        "✨ Uniform finish across all pieces — cohesive luxury aesthetic",
        "🏷️ All pieces customisable with logo engraving / printing",
        "📦 Rigid gift box with satin lining and foam inserts",
        "🌟 Creates a premium unboxing experience for recipients",
        "🎯 High perceived value — cost-effective for corporate gifting ROI",
    ],
}

def generate_key_features(components: list, specs: dict) -> list:
    """Generate a deduplicated list of key features for the product."""
    cover = specs.get("Cover Material", "Premium Leatherette")
    gsm = specs.get("Paper GSM", "80")
    
    features = []
    seen = set()
    
    # Prioritise components in this order
    priority_order = [
        "copper", "insulated", "bottle", "mug",
        "perfume", "wallet", "gift_set",
        "diary", "notebook", "cardholder", "keychain", "pen",
    ]
    
    for comp in priority_order:
        if comp in components:
            for feat in FEATURES_BY_COMPONENT.get(comp, []):
                f = feat.format(cover_material=cover, paper_gsm=gsm)
                if f not in seen:
                    seen.add(f)
                    features.append(f)
    
    if not features:
        features = [
            "🏆 Premium quality materials — handpicked for corporate gifting",
            "🎨 Sophisticated design language for boardroom and desk use",
            "🏷️ Full customisation: engraving, printing, and foil stamping available",
            "📦 Premium gift packaging — ready to present from the box",
            "🎁 Ideal for corporate welcome kits, recognition programs, and events",
            "🔄 Consistent quality across units — perfect for bulk orders",
            "🌟 Complete Soham Gift quality assurance on every unit",
        ]
    
    # Always add a few universal ones at the end (max 10 total)
    universal = [
        "📦 Ships in a premium Soham Gift presentation box",
        "🛡️ 100% quality checked — Soham Gift assurance on every unit",
        "🎯 Trusted by 500+ corporate clients across India",
    ]
    for u in universal:
        if u not in seen and len(features) < 10:
            features.append(u)
    
    return features[:10]


# ─── Specifications ───────────────────────────────────────────────────────────

SPEC_TEMPLATES = {
    "mug": {
        "Material": "Food-Grade Ceramic",
        "Capacity": "330 ml",
        "Height": "9 cm",
        "Diameter": "8.5 cm",
        "Finish": "High-Gloss Glazed",
        "Customisation": "Logo Printing, Name Engraving, Full-Colour Sublimation",
        "MOQ": "50 units",
        "Box Dimensions": "11 × 11 × 10.5 cm",
        "Dishwasher Safe": "Yes",
        "Microwave Safe": "Yes",
    },
    "pen": {
        "Material": "Metallic Alloy Barrel",
        "Mechanism": "Click / Twist (varies by model)",
        "Ink Type": "Oil-Based Ballpoint",
        "Ink Colour": "Blue / Black",
        "Tip Size": "0.7 mm Medium",
        "Barrel Diameter": "1.2 cm",
        "Length": "14 cm",
        "Weight": "18 g",
        "Customisation": "Laser Engraving, Screen Printing",
        "MOQ": "25 units",
    },
    "keychain": {
        "Material": "Zinc Alloy / Stainless Steel",
        "Finish": "Brushed Metallic / Polished Chrome",
        "Ring Diameter": "3 cm",
        "Overall Length": "8–10 cm",
        "Weight": "35 g",
        "Engraving Area": "3 × 2 cm",
        "Customisation": "Laser Engraving, Screen Printing",
        "MOQ": "50 units",
    },
    "diary": {
        "Cover Material": "Premium PU Leather",
        "Cover Finish": "Soft Touch / Matte",
        "Paper GSM": "80",
        "Pages": "192 pages (96 leaves)",
        "Size": "A5 (14.8 × 21 cm)",
        "Ruling": "Lined / Plain (as specified)",
        "Closure": "Elastic Band",
        "Pen Loop": "Yes — integrated elastic loop",
        "Bookmark": "Satin ribbon bookmark",
        "Customisation": "Debossing, Foil Stamping, Screen Printing, UV Printing",
        "MOQ": "50 units",
    },
    "notebook": {
        "Cover Material": "Premium PU Leather",
        "Paper GSM": "80",
        "Pages": "192 pages",
        "Size": "A5 (14.8 × 21 cm)",
        "Closure": "Elastic Band",
        "Customisation": "Debossing, Screen Printing",
        "MOQ": "50 units",
    },
    "cardholder": {
        "Material": "Zinc Alloy / Premium Leatherette",
        "Capacity": "10–12 business cards",
        "Mechanism": "Spring-loaded push ejection",
        "Finish": "Brushed Metallic / Matte Black",
        "Dimensions": "9.5 × 6.2 × 0.9 cm",
        "Weight": "55 g",
        "Customisation": "Laser Engraving, UV Printing",
        "MOQ": "30 units",
    },
    "perfume": {
        "Type": "Eau de Parfum",
        "Volume": "50 ml",
        "Fragrance Family": "Woody / Floral / Fresh (varies)",
        "Longevity": "8–10 hours on skin",
        "Bottle Material": "Premium glass with metallic cap",
        "Spray Type": "Fine mist atomiser",
        "Gender": "Unisex / His / Hers (as specified)",
        "Customisation": "Gift box branding, message card",
        "MOQ": "10 units",
    },
    "wallet": {
        "Material": "Premium PU Leatherette",
        "Card Slots": "6–8",
        "Bill Compartment": "Yes",
        "RFID Blocking": "Yes",
        "Dimensions": "11 × 9.5 × 1.2 cm (closed)",
        "Closure": "Bi-fold",
        "Customisation": "Embossing, UV Printing",
        "MOQ": "20 units",
    },
    "bottle": {
        "Material": "304 Stainless Steel (Interior), 18/8 Food Grade",
        "Capacity": "500 ml",
        "Insulation": "Double-wall vacuum insulation",
        "Cold Hold": "Up to 24 hours",
        "Hot Hold": "Up to 12 hours",
        "Cap Type": "Leakproof screw-cap lid",
        "Mouth Diameter": "5.5 cm (wide mouth)",
        "Height": "23 cm",
        "Diameter": "7.5 cm",
        "Finish": "Powder-Coated Matte",
        "BPA Free": "Yes",
        "Customisation": "Laser Engraving, UV Digital Printing",
        "MOQ": "25 units",
        "Certification": "Food-safe, BPA-free",
    },
    "copper": {
        "Material": "99.9% Pure Copper",
        "Capacity (Bottle)": "500 ml",
        "Capacity (Mug)": "150 ml each",
        "Set Contents": "1 Copper Bottle + 2 Copper Mugs",
        "Finish": "Hand-polished copper patina",
        "Cap Type": "Leakproof threaded copper cap",
        "Height (Bottle)": "26 cm",
        "Cleaning": "Hand wash only",
        "Customisation": "Laser Engraving on bottle",
        "Benefits": "Ayurvedic — antimicrobial, alkalising",
        "MOQ": "15 units",
        "Certifications": "Food-safe copper, artisan handcrafted",
    },
    "insulated": {
        "Material": "18/8 Food-Grade Stainless Steel",
        "Capacity": "500 ml",
        "Insulation": "Double-wall vacuum (HydroX Technology)",
        "Cold Hold": "Up to 24 hours",
        "Hot Hold": "Up to 12 hours",
        "Cap Type": "100% Leakproof screw-lid",
        "Mouth Diameter": "5.5 cm",
        "Height": "24 cm",
        "Diameter": "7.2 cm",
        "Finish": "Premium powder-coat matte",
        "BPA Free": "Yes",
        "Customisation": "Laser Engraving, UV Printing, Screen Printing",
        "MOQ": "25 units",
    },
    "default": {
        "Material": "Premium Quality",
        "Finish": "Corporate-grade premium finish",
        "Customisation": "Laser Engraving / Screen Printing / UV Printing",
        "Packaging": "Premium gift box",
        "MOQ": "25 units",
        "Quality Standard": "Soham Gift Quality Assured",
    }
}

def generate_specifications(components: list, product_name: str) -> dict:
    """Generate structured product specifications."""
    specs = {}
    
    # Build layered specs based on primary components
    priority_order = [
        "copper", "insulated", "bottle", "mug",
        "perfume", "wallet", "diary", "notebook",
        "cardholder", "keychain", "pen",
    ]
    
    for comp in priority_order:
        if comp in components:
            specs.update(SPEC_TEMPLATES.get(comp, {}))
            break
    
    if not specs:
        specs = SPEC_TEMPLATES["default"].copy()
    
    # Add secondary component specs (Pack Contents)
    if len(components) > 1:
        pack_parts = []
        comp_labels = {
            "pen": "1 Metallic Pen",
            "keychain": "1 Metal Keychain",
            "diary": "1 Executive Diary",
            "notebook": "1 Premium Notebook",
            "cardholder": "1 Business Cardholder",
            "perfume": "1 Premium Perfume (50ml)",
            "wallet": "1 Leatherette Wallet",
            "mug": "1 Ceramic Mug",
            "bottle": "1 Insulated Bottle (500ml)",
            "copper": "1 Copper Bottle (500ml)",
        }
        for comp in priority_order:
            if comp in components and comp in comp_labels:
                pack_parts.append(comp_labels[comp])
        if len(pack_parts) > 1:
            specs["Pack Contents"] = ", ".join(pack_parts)
    
    # Add general fields
    specs["Branding Options"] = "Company logo, name, event name, motivational quote"
    specs["Delivery Time"] = "7–10 working days for branded orders"
    
    return specs


# ─── SEO Fields ───────────────────────────────────────────────────────────────

def generate_meta_title(title: str, category: str) -> str:
    """Generate a 55–60 char SEO meta title."""
    clean = title.split("|")[0].strip()
    meta = f"{clean} | Soham Gift"
    if len(meta) > 60:
        meta = f"{clean[:46]}... | Soham Gift"
    return meta

def generate_meta_description(title: str, components: list, category: str, price: float) -> str:
    """Generate a 140–160 char SEO meta description."""
    comp_labels = {
        "pen": "executive pen", "keychain": "metal keychain",
        "diary": "premium diary", "cardholder": "business cardholder",
        "mug": "ceramic mug", "bottle": "insulated bottle",
        "copper": "pure copper bottle", "perfume": "luxury perfume",
        "wallet": "premium wallet",
    }
    
    parts = [comp_labels[c] for c in components if c in comp_labels][:3]
    items_str = " & ".join(parts) if parts else category.lower()
    
    base = clean_supplier_title(title).split("|")[0].strip()
    
    desc = (
        f"Shop {base} | Premium {items_str} for corporate gifting. "
        f"Bulk orders from ₹{int(price):,}. Logo branding, custom engraving available. "
        f"Order from Soham Gift — India's trusted corporate gifting partner."
    )
    
    # Trim to 160
    if len(desc) > 160:
        desc = desc[:157] + "..."
    return desc

def generate_tags(title: str, components: list, category: str) -> str:
    """Generate comma-separated SEO tags."""
    base_tags = [
        "corporate gifts india",
        "corporate gifting",
        "premium corporate gifts",
        "bulk corporate gifts",
        "branded corporate gifts",
        "soham gift",
        category.lower(),
    ]
    
    comp_tags = {
        "pen":          ["executive pen", "metallic pen", "branded pen", "pen gift"],
        "keychain":     ["metal keychain", "branded keychain", "corporate keychain"],
        "diary":        ["executive diary", "corporate diary", "branded notebook", "office diary"],
        "notebook":     ["premium notebook", "corporate notebook", "branded diary"],
        "cardholder":   ["business card holder", "corporate cardholder", "executive cardholder"],
        "perfume":      ["corporate perfume gift", "luxury perfume set", "perfume gift set"],
        "wallet":       ["corporate wallet gift", "premium wallet", "leather wallet gift"],
        "mug":          ["corporate mug", "branded mug", "coffee mug gift", "ceramic mug"],
        "bottle":       ["insulated bottle", "corporate bottle", "branded water bottle"],
        "copper":       ["copper bottle gift", "ayurvedic copper bottle", "pure copper gift"],
        "insulated":    ["vacuum insulated bottle", "thermos gift", "hydrox bottle"],
        "gift_set":     ["corporate gift set", "executive gift set", "premium gift combo"],
    }
    
    all_tags = base_tags[:]
    for comp in components:
        all_tags.extend(comp_tags.get(comp, []))
    
    # Add occasion tags
    all_tags += [
        "diwali corporate gifts", "employee gifts",
        "client gifts", "bulk gift india",
        "promotional gifts", "conference giveaways",
    ]
    
    # Deduplicate and limit
    seen = set()
    unique = []
    for t in all_tags:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    
    return ", ".join(unique[:20])


# ─── Pricing Validator ────────────────────────────────────────────────────────

def validate_and_suggest_pricing(product_name: str, components: list, price: float, discount_price) -> dict:
    """Validate price and suggest discount_price if missing."""
    suggestions = {}
    
    # Suggest discount price if not set (10-15% off)
    if not discount_price and price > 500:
        discount_pct = 0.12  # 12% off
        suggested = round(price * (1 - discount_pct) / 50) * 50  # round to nearest 50
        suggestions["discount_price"] = suggested
    
    return suggestions


# ─── Badge Recommender ────────────────────────────────────────────────────────

def recommend_badge(product_name: str, components: list, price: float, current_badge: str) -> tuple:
    """Recommend badge_text and badge_color based on price and product type."""
    if current_badge:
        return current_badge, None  # Keep existing badge
    
    name_lower = product_name.lower()
    
    if price >= 2500:
        return "LUXURY", "#8B5CF6"
    elif price >= 1500:
        return "PREMIUM", "#D91656"
    elif "copper" in components:
        return "WELLNESS", "#B45309"
    elif any(c in components for c in ["perfume", "wallet"]):
        return "GIFT IDEA", "#EC4899"
    elif price <= 500:
        return "BUDGET PICK", "#059669"
    elif "gift_set" in components:
        return "BESTSELLER", "#D91656"
    else:
        return "POPULAR", "#3B82F6"


# ─── Popularity Score ─────────────────────────────────────────────────────────

def suggest_popularity_score(components: list, is_trending: bool, price: float) -> int:
    """Suggest a popularity score for the product."""
    score = 40
    if is_trending:
        score += 30
    if "gift_set" in components:
        score += 10
    if price >= 1500:
        score += 10
    if "perfume" in components:
        score += 5
    if "copper" in components:
        score += 5
    return min(score, 100)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENRICHMENT ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def enrich_product(product, dry_run: bool = True, verbose: bool = True) -> dict:
    """Enrich a single product and return the enrichment payload."""
    
    # 1. Detect components
    components = detect_components(product.name, product.image or "")
    
    # 2. Get category name
    try:
        cat_name = product.category.name
    except Exception:
        cat_name = "Corporate Gifts"
    
    # 3. Generate premium title
    premium_title = generate_premium_title(product.name, cat_name, components)
    
    # 4. Generate specifications (needed for description context)
    specs = generate_specifications(components, product.name)
    
    # 5. Generate description
    description = generate_description(product.name, premium_title, components, specs)
    
    # 6. Generate key features
    key_features = generate_key_features(components, specs)
    
    # 7. Generate SEO
    meta_title = generate_meta_title(premium_title, cat_name)
    meta_description = generate_meta_description(
        premium_title, components, cat_name, float(product.price)
    )
    tags = generate_tags(product.name, components, cat_name)
    
    # 8. Pricing
    price_suggestions = validate_and_suggest_pricing(
        product.name, components, float(product.price), product.discount_price
    )
    
    # 9. Badge
    badge_text, badge_color = recommend_badge(
        product.name, components, float(product.price), product.badge_text
    )
    
    # 10. Popularity
    pop_score = suggest_popularity_score(
        components, product.is_trending, float(product.price)
    )
    
    payload = {
        "name": premium_title,
        "description": description,
        "key_features": json.dumps(key_features, ensure_ascii=False),
        "specifications": json.dumps(specs, ensure_ascii=False),
        "meta_title": meta_title,
        "meta_description": meta_description,
        "tags": tags,
        "badge_text": badge_text,
        "popularity_score": pop_score,
    }
    
    if badge_color:
        payload["badge_color"] = badge_color
    if "discount_price" in price_suggestions:
        payload["discount_price"] = price_suggestions["discount_price"]
    
    if verbose:
        print_enrichment_preview(product, payload, components)
    
    if not dry_run:
        for field, value in payload.items():
            setattr(product, field, value)
        product.save()
        print(f"  ✅ Saved: {product.sku or product.id}")
    
    return payload

def print_enrichment_preview(product, payload, components):
    """Pretty-print the enrichment output for a product."""
    SEP = "─" * 70
    print(f"\n{SEP}")
    print(f"📦 ORIGINAL:  {product.name}")
    print(f"🏷️  SKU:       {product.sku or 'Not Assigned'}")
    print(f"📂 CATEGORY:  {product.category.name}")
    print(f"💰 PRICE:     ₹{product.price}")
    print(f"🔍 COMPONENTS DETECTED: {', '.join(components) if components else 'None'}")
    print(SEP)
    print(f"✨ ENRICHED TITLE:")
    print(f"   {payload['name']}")
    print(f"\n📋 META TITLE:")
    print(f"   {payload['meta_title']}")
    print(f"\n🔎 META DESCRIPTION:")
    print(f"   {payload['meta_description']}")
    print(f"\n🏷️  TAGS:")
    print(f"   {payload['tags'][:120]}...")
    print(f"\n⭐ KEY FEATURES (first 3):")
    features = json.loads(payload['key_features'])
    for f in features[:3]:
        print(f"   • {f}")
    print(f"   ... +{len(features) - 3} more features")
    print(f"\n📊 SPECS (first 5):")
    specs = json.loads(payload['specifications'])
    for i, (k, v) in enumerate(specs.items()):
        if i >= 5:
            break
        print(f"   {k}: {v}")
    print(f"   ... +{max(0, len(specs)-5)} more specs")
    print(f"\n🎀 BADGE: [{payload['badge_text']}]  |  POPULARITY: {payload['popularity_score']}/100")
    if "discount_price" in payload:
        print(f"💸 SUGGESTED DISCOUNT PRICE: ₹{payload['discount_price']}")
    print(f"\n📝 DESCRIPTION PREVIEW (first 300 chars):")
    print(textwrap.fill(
        re.sub(r'\*\*.*?\*\*', lambda m: m.group().replace('**',''), payload['description'])[:300],
        width=68, initial_indent="   ", subsequent_indent="   "
    ))
    print("   ...")


def is_product_incomplete(product) -> bool:
    """Check if a product needs enrichment."""
    try:
        feats = json.loads(product.key_features)
        specs = json.loads(product.specifications)
    except Exception:
        return True
    
    if not feats or len(feats) == 0:
        return True
    if not specs or len(specs) == 0:
        return True
    if not product.meta_title or product.meta_title == product.name:
        return True
    if not product.meta_description or len(product.meta_description) < 50:
        return True
    return False


def run_enrichment(dry_run: bool, sku: str = None, name: str = None, missing_only: bool = False):
    """Main runner — enriches products based on filters."""
    
    print("\n" + "═" * 70)
    print("🎁  SOHAM GIFT — AI CATALOG ENRICHMENT ENGINE")
    print(f"{'🔍 DRY RUN MODE — No changes saved' if dry_run else '💾 SAVE MODE — Changes will be written to DB'}")
    print("═" * 70)
    
    # Filter products
    if sku:
        products = Product.objects.filter(sku=sku)
        if not products.exists():
            print(f"❌ No product found with SKU: {sku}")
            return
    elif name:
        products = Product.objects.filter(name__icontains=name)
        if not products.exists():
            print(f"❌ No product found with name containing: {name}")
            return
    else:
        products = Product.objects.all().order_by('category__name', 'name')
    
    if missing_only:
        products = [p for p in products if is_product_incomplete(p)]
        print(f"📋 Found {len(products)} incomplete products to enrich\n")
    else:
        products = list(products)
        print(f"📋 Found {len(products)} products to enrich\n")
    
    if not products:
        print("✅ All products are already enriched!")
        return
    
    enriched_count = 0
    for product in products:
        try:
            enrich_product(product, dry_run=dry_run, verbose=True)
            enriched_count += 1
        except Exception as e:
            print(f"\n❌ Error enriching '{product.name}': {e}")
            import traceback; traceback.print_exc()
    
    print(f"\n{'═' * 70}")
    print(f"🎉 ENRICHMENT COMPLETE")
    print(f"   Products processed: {enriched_count}")
    print(f"   Mode: {'DRY RUN — run with --save to persist' if dry_run else 'SAVED ✅'}")
    print("═" * 70)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI ENTRYPOINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="AI-Powered Catalog Enrichment Engine for Soham Gift",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          python enrich_catalog.py --dry-run
          python enrich_catalog.py --save
          python enrich_catalog.py --save --missing-only
          python enrich_catalog.py --dry-run --name "HydroX"
        """)
    )
    parser.add_argument("--dry-run", action="store_true", default=False,
                        help="Preview enrichments without saving to DB (default)")
    parser.add_argument("--save", action="store_true", default=False,
                        help="Save enrichments to the database")
    parser.add_argument("--sku", type=str, default=None,
                        help="Enrich only the product with this SKU")
    parser.add_argument("--name", type=str, default=None,
                        help="Enrich products whose name contains this string")
    parser.add_argument("--missing-only", action="store_true", default=False,
                        help="Only enrich products with incomplete data")
    
    args = parser.parse_args()
    
    # Default to dry-run if neither flag set
    dry_run = not args.save
    
    run_enrichment(
        dry_run=dry_run,
        sku=args.sku,
        name=args.name,
        missing_only=args.missing_only,
    )
