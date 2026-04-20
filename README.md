# Phia Brand Portfolio Intelligence Report

A self-contained, single-file interactive analytics dashboard built to analyze affiliate partner performance across a 12-month fiscal year. Designed as a portfolio piece demonstrating data analysis, visualization, and product thinking in the context of a consumer affiliate platform.

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | The full interactive dashboard — open directly in any browser, no server needed |
| `transform.py` | Anonymization pipeline that generated `index.html` from the original source data |

---

## What the Dashboard Does

`index.html` is a standalone analytics report covering the top 100 brand partners by GMV across April 2025–March 2026. Everything is embedded — data, charts, styles, and interactivity — in a single HTML file with no build step or backend.

**Sections:**

1. **KPI Strip** — five headline metrics (total GMV, revenue, top-100 share, active brands, avg commission rate) rendered at a glance
2. **Executive Summary** — eight insight cards with specific, quantified observations written for a CFO audience: concentration risk, growth trajectory, commission gap opportunity, vertical mix, partner momentum, inactive brand reactivation, long-tail health, and direct partnership upgrade candidates
3. **Portfolio Growth Trajectory** — combo bar/line chart of monthly GMV and revenue across the full fiscal year, showing the platform's 154x scale from April to March
4. **Revenue Concentration Analysis** — horizontal concentration bars + doughnut chart showing the power-law distribution across brand tiers (top 1 brand, brands 2–10, 11–25, 26–50, 51–100, long tail)
5. **Vertical Segmentation** — GMV and Rev/GMV% by vertical category, plus three side-by-side charts: partner momentum (expanding/decreasing/same/inactive), commission rate bands, and a bubble chart of effective CPA vs. GMV for the top 20 brands
6. **Top 100 Brand Table** — fully interactive: sortable by any column, filterable by vertical and commission trend, searchable by brand name. All 100 rows rendered statically with live client-side logic
7. **Strategic Opportunities** — six opportunity cards covering rate normalization, partnership tier upgrades, beauty vertical expansion, inactive brand reactivation, marketplace rate compression, and luxury segment prioritization
8. **Risk Assessment** — three tiers (high / medium / low) in plain text with colored labels, covering structural risks (marketplace dependency, rate compression, no-commission anomaly), medium risks (inactive churn, entertainment lumping, seasonality), and well-managed positives (brand diversity, expansion momentum, premium rate capture)

---

## How `transform.py` Works

The original source report (`Phia_CFO_Brand_Analysis.html`) contained real brand names and actual financial figures from a live affiliate network. `transform.py` is the anonymization and reskinning pipeline that produced `index.html` for portfolio use.

**What it does:**

1. **Brand name substitution** — a 100-entry `BRAND_MAP` replaces every real brand name (Amazon → Nexus Market, Sephora → Luminara Beauty, Nike → Apex Athletics, etc.) across JSON data blocks, HTML table cells, and narrative prose
2. **Financial scaling** — all GMV and revenue figures are multiplied by `0.81x`, transaction counts by `0.79x`, so the numbers diverge slightly and are not directly reversible. Percentage ratios (Rev/GMV, Eff. CPA) are preserved since they're analytically meaningful
3. **Narrative text replacement** — ~90 string replacements patch financial figures cited in the insight prose ($4.9M → $4.0M, etc.) and scrub any remaining real brand name references that slipped through the JSON replacement
4. **CSS palette swap** — the original blue-navy design system is replaced with a Phia-branded sage/dark-green aesthetic (CSS variable overrides + Chart.js defaults)
5. **Platform reference sanitization** — removes or generalizes any references to the real platform name ("Phia's last-click attribution" → "the platform's last-click attribution")
6. **Em-dash normalization** — replaces all `&mdash;`, `&#8212;`, and unicode `—` with plain ` - ` for cleaner rendering

The output (`index.html`) is analytically faithful to the original with the same structure, same rankings, same strategic conclusions but fully anonymized for public sharing.

---

## Stack

- Vanilla HTML/CSS/JS — no framework, no bundler, no dependencies beyond CDN
- [Chart.js 4.4](https://www.chartjs.org/) for all visualizations
- [Glacial Indifference](https://www.cdnfonts.com/glacial-indifference.font) (CDN) for typography
- Python 3 + stdlib only (`re`, `json`, `math`) for the transform script
