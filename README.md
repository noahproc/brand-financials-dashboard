# Phia Brand Portfolio Analysis

A data transformation pipeline that anonymizes and scales a brand portfolio intelligence report for external presentation.

## Overview

`transform.py` takes `Phia_CFO_Brand_Analysis.html` (the raw internal report) and produces `Phia_CFO_Portfolio_Analysis.html` (a sanitized version suitable for portfolio/demo use) by:

- **Anonymizing brand names** — 100+ real retailers mapped to fictional equivalents (e.g. Amazon → Nexus Market, Nordstrom → Harrington & Co)
- **Scaling financial figures** — GMV and revenue scaled by ~0.81×, transaction counts by ~0.79×, so relative metrics remain realistic
- **Stripping internal references** — removes Phia-specific branding, replaces em-dashes, updates titles and date badges
- **Reskinning the UI** — swaps the CSS color palette from navy/blue to a sage/green aesthetic and injects the Inter font

## Files

| File | Description |
|------|-------------|
| `Phia_CFO_Brand_Analysis.html` | Source report (internal, not for sharing) |
| `Phia_CFO_Portfolio_Analysis.html` | Anonymized output (portfolio-safe) |
| `transform.py` | Transformation script |

## Usage

```bash
python3 transform.py
