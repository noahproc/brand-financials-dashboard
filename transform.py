#!/usr/bin/env python3
"""
Transform Phia_CFO_Brand_Analysis.html:
  1. Replace real brand names with fictional ones
  2. Scale all financial figures by ~0.81x
  3. Remove em-dashes (replace with " - " or ", " as appropriate)
  4. Update CSS color palette to Phia brand-adjacent aesthetic
"""
import re, json, math

INPUT  = "Phia_CFO_Brand_Analysis.html"
OUTPUT = "Phia_CFO_Portfolio_Analysis.html"

SCALE = 0.81           # monetary / transaction scaling factor
TRX_SCALE = 0.79       # slightly different so transaction counts diverge

BRAND_MAP = {
    # raw HTML display name -> fake name
    "Amazon":                    "Nexus Market",
    "The Realreal":              "Prestige Resale",
    "Nordstrom":                 "Harrington & Co",
    "Quince":                    "Meridian Basics",
    "Bloomingdale'S":            "Bellmore Select",
    "Bloomingdale's":            "Bellmore Select",
    "Macy'S":                    "Hartwell's",
    "Macy's":                    "Hartwell's",
    "Target":                    "Apex General",
    "Anthropologie":             "Terra & Thread",
    "Saks Fifth Avenue":         "Ashford Gallery",
    "J.Crew":                    "Calloway Style",
    "Etsy":                      "Craft Haven",
    "Sephora":                   "Luminara Beauty",
    "Revolve":                   "Cascade Boutique",
    "Seatgeek":                  "EventSphere",
    "Nike":                      "Apex Athletics",
    "Mytheresa":                 "Palazzo Luxe",
    "Vuori":                     "Kinetic Life",
    "Shopbop":                   "Prism Select",
    "Ticketmaster":              "TicketVault",
    "Neiman Marcus":             "Whitmore Gallery",
    "Alo Yoga":                  "Solstice Studio",
    "Farfetch":                  "Globe Couture",
    "Meshki":                    "Velara Collective",
    "Free People":               "Wanderer & Co",
    "Tory Burch":                "Caitlin Rhodes",
    "Madewell":                  "Stonegate Denim",
    "Lowe'S":                    "Habitat Supply",
    "Lowe's":                    "Habitat Supply",
    "Loft":                      "Cedarwood Co",
    "Lulus":                     "Vivace",
    "Tuckernuck":                "Brentwood Prep",
    "Coach Outlet":              "Astor Outlet",
    "Dermstore":                 "Glow Lab",
    "Best Buy":                  "ElectroPulse",
    "Ayr":                       "Slate Studio",
    "Net-A-Porter":              "Circuit Couture",
    "Abercrombie & Fitch":       "Crestwood & Co",
    "Lululemon":                 "Fluid Form",
    "Skims":                     "Sculpt",
    "J.Crew Factory":            "Calloway Outlet",
    "Reformation":               "Verdure Mode",
    "Walmart":                   "Prism Deals",
    "The Home Depot":            "BuildRight Supply",
    "Ann Taylor":                "Hawthorne Career",
    "Alice + Olivia":            "Margaux & Riva",
    "New Balance":               "Stride & Co",
    "Ugg":                       "Cozy Peak",
    "Gap Canada":                "Canvas Collective",
    "Fashionphile":              "Heirloom Exchange",
    "Cettire":                   "Trevi Couture",
    "Designer Shoe Warehouse":   "SoleVault",
    "Everlane":                  "Transparency Co",
    "Lands' End":                "Broadshore Classic",
    "Veronica Beard":            "Cordelia & James",
    "Ulta":                      "Radiance Pro",
    "Spanx":                     "Contour Lab",
    "\u014cura":                 "Aura Health",
    "\u014dura":                 "Aura Health",
    "Coach":                     "Astor Leather",
    "Old Navy":                  "Foundry Basics",
    "Hanna Andersson":           "Sprout & Co",
    "Michaels Stores":           "Create Studio",
    "Rugs.Com":                  "Weave & Thread",
    "Poshmark":                  "Closet Loop",
    "Serena & Lily":             "Coastal Home Co",
    "Adidas":                    "Nexus Sport",
    "Cos":                       "Form Collective",
    "Shutterfly":                "Memora",
    "Lulu And Georgia":          "Hearth & Linen",
    "Pottery Barn":              "Hearthstone Living",
    "Kendra Scott":              "Ember Jewel",
    "Steve Madden":              "Cobblestone Shoes",
    "Rag & Bone":                "Greystone Made",
    "Marshalls":                 "Clearance Avenue",
    "Ssense":                    "Axiom Mode",
    "Victoria'S Secret":         "Bloom Intimate",
    "Victoria's Secret":         "Bloom Intimate",
    "Mango":                     "Solena",
    "West Elm":                  "Arbor Living",
    "Sharkninja":                "Vortex Home",
    "Tibi":                      "Atelier Tiara",
    "Ring Concierge":            "Constellation Fine",
    "Aviator Nation":            "Pacific Current",
    "Express":                   "Meridian Style",
    "1800Flowers.Com":           "Bloom & Send",
    "1800flowers.com":           "bloom & send",
    "Fwrd":                      "Apex Mode",
    "Bluemercury":               "Clarity Beauty",
    "Kohl'S":                    "Parkside Market",
    "Kohl's":                    "Parkside Market",
    "Cando":                     "WellPath",
    "cando":                     "wellpath",
    "Thredup (Us)":              "Refresh Resale",
    "thredup (us)":              "refresh resale",
    "Jcpenney":                  "Westfield Fashion",
    "jcpenney":                  "westfield fashion",
    "Finish Line":               "Sprint Shoe",
    "Dolce Vita":                "Bellina Shoes",
    "Lola Blankets":             "Warmth Co",
    "lola blankets":             "warmth co",
    "Bombas Socks":              "Comfort Loop",
    "bombas socks":              "comfort loop",
    "Ruggable":                  "Roots & Weave",
    "Away":                      "Voyage & Co",
    "1-800 Contacts":            "ClearView Optical",
    "1-800 contacts":            "clearview optical",
    "Journeys":                  "Sole District",
    "Beyond Yoga":               "Restore Active",
    "beyond yoga":               "restore active",
    "Jomashop.Com":              "Timepiece Vault",
    "jomashop.com":              "timepiece vault",
    "Mango (Us/Mx)":             "Solena US",
    "mango (us/mx)":             "solena us",
    "Dick'S Sporting Goods":     "Pinnacle Sports",
    "dick's sporting goods":     "pinnacle sports",
}

# Additional text replacements for the insight prose
TEXT_REPLACEMENTS = [
    # Full proper names as they appear in narrative text
    ("Amazon alone drives",                "Nexus Market alone drives"),
    ("Amazon adjusts",                     "Nexus Market adjusts"),
    ("Amazon absorbs",                     "Nexus Market absorbs"),
    ("Amazon's $4.9M",                     "Nexus Market's $4.0M"),
    ("Amazon's $4.9M GMV",                 "Nexus Market's $4.0M GMV"),
    ("Amazon = 9.3%",                      "Nexus Market = 9.2%"),
    ("Amazon Concentration Risk",          "Top Marketplace Concentration Risk"),
    ("Amazon Dependency",                  "<strong>Top Marketplace Dependency"),
    ("Single-brand concentration at 9.3% GMV", "Single-brand concentration at 9.2% GMV"),
    ("Amazon, Nordstrom, and Bloomingdale",    "Nexus Market, Harrington & Co, and Bellmore Select"),
    ("Amazon, Etsy, Walmart, and Target",      "Nexus Market, Craft Haven, Prism Deals, and Apex General"),
    ("Amazon ($4.9M, 3.2%)",               "Nexus Market ($4.0M, 3.2%)"),
    ("Amazon alone",                       "Nexus Market alone"),
    ("241K+ transactions from Amazon",     "190K+ transactions from Nexus Market"),
    ("241,427 transactions",               "190,527 transactions"),
    ("$4.9M GMV (9.3%",                    "$4.0M GMV (9.2%"),
    ("$156K revenue",                      "$127K revenue"),
    ("$156K annualized",                   "$127K annualized"),
    ("~$37K in April 2025",                "~$30K in April 2025"),
    ("$5.7M in March 2026",                "$4.6M in March 2026"),
    ("GMV remained above $5M",             "GMV remained above $4M"),
    ("154x increase",                      "154x increase"),
    ("$5.7M March GMV",                    "$4.6M March GMV"),
    ("The RealReal (1.8%)",                "Prestige Resale (1.8%)"),
    ("The RealReal",                       "Prestige Resale"),
    ("Macy's (2.6%)",                      "Hartwell's (2.6%)"),
    ("Target (2.8%)",                      "Apex General (2.8%)"),
    ("Ticketmaster (1.3%)",                "TicketVault (1.3%)"),
    ("UGG (0.9%)",                         "Cozy Peak (0.9%)"),
    ("Quince (Tier 1 candidate)",          "Meridian Basics (Tier 1 candidate)"),
    ("Vuori",                              "Kinetic Life"),
    ("Shopbop",                            "Prism Select"),
    ("Tory Burch",                         "Caitlin Rhodes"),
    ("Sephora",                            "Luminara Beauty"),
    ("Nike",                               "Apex Athletics"),
    ("Quince",                             "Meridian Basics"),
    ("Alo Yoga's $319K",                   "Solstice Studio's $259K"),
    ("Alo Yoga",                           "Solstice Studio"),
    ("Pottery Barn and West Elm",          "Hearthstone Living and Arbor Living"),
    ("Pottery Barn ($125K)",               "Hearthstone Living ($101K)"),
    ("West Elm ($117K)",                   "Arbor Living ($95K)"),
    ("Kohl's ($112K)",                     "Parkside Market ($91K)"),
    ("Serena &amp; Lily ($132K)",          "Coastal Home Co ($107K)"),
    ("Serena & Lily ($132K)",              "Coastal Home Co ($107K)"),
    ("Mango US ($98K)",                    "Solena US ($79K)"),
    ("6 Inactive Brands &mdash; $904K GMV Recovery Target", "6 Inactive Brands - $733K GMV Recovery Target"),
    ("6 Inactive Brands -- $904K GMV Recovery Target", "6 Inactive Brands - $733K GMV Recovery Target"),
    ("$904K+ GMV",                         "$733K+ GMV"),
    ("$904K historical",                   "$733K historical"),
    ("~$4.3M Annual Rev",                  "~$3.5M Annual Rev"),
    ("~$4.3M in annual",                   "~$3.5M in annual"),
    ("Fashion/Apparel ($10.7M GMV)",       "Fashion/Apparel ($8.7M GMV)"),
    ("Luxury Fashion ($4.0M)",             "Luxury Fashion ($3.2M)"),
    ("Beauty ($1.1M, 2.1% share)",         "Beauty ($0.9M, 2.1% share)"),
    ("Sephora's #12 rank",                 "Luminara Beauty's #12 rank"),
    ("Sephora (#12, $589K)",               "Luminara Beauty (#12, $477K)"),
    ("Ulta (#54, $164K)",                  "Radiance Pro (#54, $133K)"),
    ("Tatcha, Charlotte Tilbury, Rare Beauty", "Petal Lab, Mira Glow, Rare Bloom"),
    ("Dermstore (16.5%)",                  "Glow Lab (16.5%)"),
    ("Bluemercury (14.1%)",                "Clarity Beauty (14.1%)"),
    ("Sephora (Expanding, 12.5%)",         "Luminara Beauty (Expanding, 12.5%)"),
    ("Ulta (Expanding, 11.6%)",            "Radiance Pro (Expanding, 11.6%)"),
    ("J.Crew (#10, $632K GMV, 13.5% rate)", "Calloway Style (#10, $511K GMV, 13.5% rate)"),
    ("Madewell (#26, $296K, 14.9%)",       "Stonegate Denim (#26, $240K, 14.9%)"),
    ("Anthropologie (#8, $739K, 14.4%)",   "Terra & Thread (#8, $599K, 14.4%)"),
    ("Free People (#24, $301K, 13.7%)",    "Wanderer & Co (#24, $244K, 13.7%)"),
    ("J.Crew, Madewell &amp; Anthropologie Signal", "Calloway Style, Stonegate Denim &amp; Terra & Thread Signal"),
    ("J.Crew, Madewell & Anthropologie",   "Calloway Style, Stonegate Denim & Terra & Thread"),
    ("Mytheresa ($607 avg basket)",        "Palazzo Luxe ($607 avg basket)"),
    ("Farfetch ($518)",                    "Globe Couture ($518)"),
    ("Net-a-Porter ($436)",               "Circuit Couture ($436)"),
    ("Fashionphile ($786)",               "Heirloom Exchange ($786)"),
    ("Alice + Olivia ($590)",             "Margaux & Riva ($590)"),
    ("Mytheresa, Farfetch, Net-a-Porter, Cettire, Fashionphile",
     "Palazzo Luxe, Globe Couture, Circuit Couture, Trevi Couture, Heirloom Exchange"),
    ("Ann Taylor, Everlane, Lands' End",  "Hawthorne Career, Transparency Co, Broadshore Classic"),
    ("Nordstrom",                          "Harrington & Co"),
    ("Bloomingdale'S",                     "Bellmore Select"),
    ("Bloomingdale's",                     "Bellmore Select"),
    ("Cando ($112K GMV)",                  "WellPath ($91K GMV)"),
    ("Cando",                              "WellPath"),
    ("Seatgeek ($437K GMV)",              "EventSphere ($354K GMV)"),
    ("Ticketmaster ($354K)",              "TicketVault ($287K)"),
    ("Skimlinks, LTK",                    "SkimNet, ShopNow"),
    ("Rakuten/CJ networks",               "affiliate networks"),
    ("Connexity model",                   "cost-per-click model"),
    # Financial headline figures in badges and KPI cards
    ("6,552 Active Brands",               "5,849 Active Brands"),
    ("$53.1M Total GMV",                  "$43.0M Total GMV"),
    ("$4.5M Total Revenue",               "$3.6M Total Revenue"),
    ("6,838 total tracked",               "6,127 total tracked"),
    ("6,552 active partners",             "5,849 active partners"),
    ("6,452 brands",                      "5,752 brands"),
    ("6,838 brands tracked",              "6,127 brands tracked"),
    ("$53.1M",                            "$43.0M"),
    ("$30.9M",                            "$25.0M"),
    ("$30.9M of $53.1M",                  "$25.0M of $43.0M"),
    ("$22.2M",                            "$18.0M"),
    ("$8.1M",                             "$6.6M"),
    ("$6.0M",                             "$4.9M"),
    ("$5.8M",                             "$4.7M"),
    ("$6.2M",                             "$5.0M"),
    ("$11.5M of the $30.9M",              "$9.3M of the $25.0M"),
    ("$6.5M GMV (12.2%",                  "$5.3M GMV (12.2%"),
    ("$207K revenue",                     "$168K revenue"),
    ("$6.9M GMV",                         "$5.6M GMV"),
    ("$26M GMV",                          "$21M GMV"),
    ("8.5% blended Rev/GMV rate",         "8.4% blended Rev/GMV rate"),
    ("vs. 20% Phia target rate",          "vs. 20% platform target rate"),
    ("Phia's stated 20% standard",        "the platform's stated 20% standard"),
    ("Phia's last-click attribution",     "the platform's last-click attribution"),
    ("Phia's 20% target",                 "the platform's 20% target"),
    ("Phia's core demographic",           "the platform's core demographic"),
    ("Phia's user quality",               "the platform's user quality"),
    ("Phia's activewear user segment",    "the platform's activewear user segment"),
    ("Phia absorbs",                      "the platform absorbs"),
    ("Phia lists",                        "the platform lists"),
    ("Phia's discovery surface",          "the platform's discovery surface"),
    ("Phia's affluent user segment",      "the platform's affluent user segment"),
    ("Phia's stage",                      "the platform's stage"),
    ("Phia's top performers",             "the platform's top performers"),
    ("Phia's partnership model",          "the platform's partnership model"),
    ("Phia's margin profile",             "the platform's margin profile"),
    ("Phia's user experience",            "the platform's user experience"),
    ("Phia's traffic quality",            "the platform's traffic quality"),
    ("Phia's core demographic sweet spot", "the platform's core demographic sweet spot"),
    ("Phia's brand partner",              "brand partner"),
    ("Phia's 20%",                        "the 20%"),
    # subtitle/section text
    ("Top 100 Partners by GMV &mdash; April 2025 through March 2026 &mdash; Full Fiscal Year View",
     "Top 100 Partners by GMV - April 2025 through March 2026 - Full Fiscal Year View"),
    ("Click column headers to sort &mdash; All metrics for fiscal year Apr '25&ndash;Mar '26",
     "Click column headers to sort - All metrics for fiscal year Apr '25-Mar '26"),
    ("Brand Portfolio Intelligence Report &mdash; Confidential &amp; Proprietary",
     "Brand Portfolio Intelligence Report - Confidential &amp; Proprietary"),
    # miscellaneous em-dashes in prose
    ("&mdash;", " - "),
    ("&#8212;", " - "),
    (" — ", " - "),
    (" -- ", " - "),
]

# ---- CSS color overrides (Phia-inspired sage/warm palette) ----------------
OLD_CSS = """:root {
    --phia-dark: #0a0e1a;
    --phia-navy: #0d1b2e;
    --phia-blue: #1a3a5c;
    --phia-accent: #4f8ef7;
    --phia-teal: #00c9b1;
    --phia-gold: #f5c842;
    --phia-rose: #f472b6;
    --text-primary: #f0f4ff;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: #1e3251;
    --card-bg: #0f1e35;
    --card-border: #1e3a5f;
    --success: #10b981;
    --danger: #ef4444;
    --warning: #f59e0b;
    --font: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
  }"""

NEW_CSS = """:root {
    --phia-dark: #0d0f0e;
    --phia-navy: #111a16;
    --phia-blue: #1a2e22;
    --phia-accent: #6db88a;
    --phia-teal: #4caf76;
    --phia-gold: #f0b840;
    --phia-rose: #f08080;
    --text-primary: #eef5f0;
    --text-secondary: #93b09e;
    --text-muted: #5d7a65;
    --border: #1e3028;
    --card-bg: #121e17;
    --card-border: #1e3828;
    --success: #4caf76;
    --danger: #e05555;
    --warning: #e6982a;
    --font: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
  }"""

# Additional CSS injection after :root block for Inter font + Chart.js colors
CHART_COLOR_PATCH = """
Chart.defaults.color = '#93b09e';
Chart.defaults.borderColor = '#1e3028';"""

OLD_CHART_DEFAULTS = """Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = '#1e3251';"""

# ---- JSON data scaling -------------------------------------------------------
def scale_brand(b):
    """Return a copy of brand dict with scaled numeric fields."""
    def s(v, factor=SCALE):
        if isinstance(v, float): return round(v * factor, 2)
        if isinstance(v, int):   return max(1, int(v * factor))
        return v
    out = dict(b)
    # Replace name
    display = b.get("brand", "")
    raw = b.get("brand_raw", "")
    out["brand"]     = BRAND_MAP.get(display, display)
    out["brand_raw"] = BRAND_MAP.get(raw,     BRAND_MAP.get(raw.title(), raw))
    # Scale money fields
    for key in ("total_gmv", "total_rev"):
        out[key] = round(b[key] * SCALE, 2)
    # Scale transaction count separately
    out["total_trx"] = max(1, int(b["total_trx"] * TRX_SCALE))
    # Recalculate rev_to_gmv_pct from scaled values (keep ratio unchanged)
    # just keep the original percentage - only $ amounts change
    # Scale monthly GMV array
    out["monthly_gmv"] = [round(x * SCALE, 2) for x in b["monthly_gmv"]]
    return out

def scale_summary(s):
    out = dict(s)
    for key in ("total_gmv_all","total_rev_all","top10_gmv","top25_gmv",
                "top50_gmv","top100_gmv","top100_rev"):
        if key in s:
            out[key] = round(s[key] * SCALE, 2)
    out["monthly_gmv"] = [round(x * SCALE, 2) for x in s["monthly_gmv"]]
    out["monthly_rev"] = [round(x * SCALE, 2) for x in s["monthly_rev"]]
    out["total_active_brands"] = 5849
    # scale verticals
    out["verticals"] = [
        {**v, "gmv": round(v["gmv"]*SCALE, 2), "rev": round(v["rev"]*SCALE, 2)}
        for v in s["verticals"]
    ]
    # scale category GMV
    out["categories"] = [
        {**c, "gmv": round(c["gmv"]*SCALE, 2)} for c in s["categories"]
    ]
    return out

def replace_brands_in_json(m):
    """Given a regex match for the BRANDS JSON, scale and rename all entries."""
    raw = m.group(1)
    data = json.loads(raw)
    scaled = [scale_brand(b) for b in data]
    return "const BRANDS = " + json.dumps(scaled, separators=(',', ':')) + ";"

def replace_summary_json(m):
    raw = m.group(1)
    data = json.loads(raw)
    scaled = scale_summary(data)
    return "const SUMMARY = " + json.dumps(scaled, separators=(',', ':')) + ";"

# ---- Main -------------------------------------------------------------------
with open(INPUT, "r", encoding="utf-8") as f:
    html = f.read()

# 1. CSS palette
html = html.replace(OLD_CSS, NEW_CSS, 1)

# 2. Chart.js defaults
html = html.replace(OLD_CHART_DEFAULTS, CHART_COLOR_PATCH.strip(), 1)

# 3. Add Inter font import after <head>
if "@import url('https://fonts.googleapis.com/css2?family=Inter" not in html:
    html = html.replace(
        "<style>",
        "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');\n<style>",
        1
    )
    # wrap inside <head> instead
    html = html.replace(
        "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');\n<style>",
        "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'>\n<style>",
        1
    )

# 4. Scale JSON data blocks
html = re.sub(r'const BRANDS = (\[.*?\]);', replace_brands_in_json, html, flags=re.DOTALL)
html = re.sub(r'const SUMMARY = (\{.*?\});', replace_summary_json, html, flags=re.DOTALL)

# 5. Text replacements (brand names + financial figures + em-dashes)
for old, new in TEXT_REPLACEMENTS:
    html = html.replace(old, new)

# 6. Any remaining em-dash entities / unicode
html = html.replace("&mdash;", " - ")
html = html.replace("\u2014", " - ")
html = html.replace("&#8212;", " - ")
# Replace en-dash between numbers/words too
html = re.sub(r'(?<=[A-Za-z0-9])\s*&ndash;\s*(?=[A-Za-z0-9])', "-", html)
html = html.replace("&ndash;", "-")
html = html.replace("\u2013", "-")

# 7. Update title
html = html.replace(
    "<title>Phia — CFO Brand Portfolio Analysis | April 2026</title>",
    "<title>Brand Portfolio Performance Analysis | April 2026</title>"
)

# 8. Update header date badge "Confidential" note
html = html.replace("April 3, 2026 &nbsp;|&nbsp; Confidential",
                    "April 2026 &nbsp;|&nbsp; Illustrative")

# 9. Update concentration bar labels in HTML
bar_labels = {
    "#1 Amazon":     "#1 Nexus Market",
    "#2–10 Brands":  "#2-10 Brands",
    "Amazon":        "Nexus Market",
}
for old, new in bar_labels.items():
    html = html.replace(f'>{old}<', f'>{new}<')

# 10. Update chart accent colours that are hardcoded in gradient strings
html = html.replace("rgba(79,142,247,", "rgba(109,184,138,")
html = html.replace("rgba(79,142,247,0.08)", "rgba(109,184,138,0.08)")
html = html.replace("rgba(79,142,247,0.05)", "rgba(109,184,138,0.05)")
html = html.replace("rgba(79,142,247,0.12)", "rgba(109,184,138,0.12)")
html = html.replace("rgba(79,142,247,0.25)", "rgba(109,184,138,0.25)")
html = html.replace("rgba(79,142,247,0.1)", "rgba(109,184,138,0.1)")
html = html.replace("rgba(79,142,247,0.15)", "rgba(109,184,138,0.15)")
html = html.replace("#4f8ef7", "#6db88a")
html = html.replace("#4F8EF7", "#6DB88A")

# 11. Add portfolio disclaimer note near header
DISCLAIMER = """<div style="background:rgba(109,184,138,0.08);border:1px solid rgba(109,184,138,0.2);border-radius:8px;padding:12px 20px;margin:0 48px 0;max-width:1400px;margin-left:auto;margin-right:auto;font-size:12px;color:#93b09e;">
  <strong style="color:#6db88a;">Portfolio Analysis Sample</strong> - Brand names, partner counts, and financial figures in this report have been anonymized and scaled for portfolio presentation purposes. All analytical frameworks and methodology are original work.
</div>"""
html = html.replace('<div class="main">', DISCLAIMER + '\n<div class="main">', 1)

# 12. Remove "CFO Intelligence Report" label + make subtitle generic
html = html.replace("CFO Intelligence Report", "Intelligence Report")
html = html.replace("CFO-level observations", "Executive-level observations")
html = html.replace("CFO and board-level", "leadership-level")

# 13. Systematic sweep: replace ALL brand names in HTML table cells and prose
#     using BRAND_MAP. This catches anything TEXT_REPLACEMENTS missed.
for old_name, new_name in BRAND_MAP.items():
    # table cell pattern
    html = html.replace(
        f'class="brand-name">{old_name}</td>',
        f'class="brand-name">{new_name}</td>'
    )
    # also replace bare brand name in prose if it still appears
    # (use word-boundary style: surrounded by non-alphanumeric or start/end)
    html = html.replace(old_name, new_name)

# 14. Clean up "Brands like Amazon" in remaining insight prose
html = html.replace(
    "Brands like Amazon (3.2%), Prestige Resale",
    "Brands like Nexus Market (3.2%), Prestige Resale"
)
# 15. Fix any "target" (non-brand) that may have been over-replaced back
#     "Apex General rate" -> "target rate"
html = html.replace("vs. 20% platform Apex General rate", "vs. 20% platform target rate")
html = html.replace("Apex General rate</div>", "target rate</div>")

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Done. Written to {OUTPUT}")
