# 📸 Photos for Impact: Representative Products Campaign Guide

This guide explains the architecture, operational workflow, and maintenance of the **Photos for Impact** campaign across all 32 countries in Open Food Facts.

---

## 1. Campaign Strategy & Architecture

In countries with small communities (~20 Daily Active Users), conversion requires frictionless user journeys:
1. **In-App Tagline**: Users see a localized, motivating banner highlighting missing representative foods in their country.
2. **Mobile Campaign Hub (`release-website/photos-for-impact/`)**:
   - Tapping the banner opens their country view directly (`?country=at`, `?country=lv`, etc.).
   - Shows real-time coverage percentage, shopping lists of missing products, and 1-tap links to photograph or verify products in Open Food Facts and Hunger Games.
3. **Structured Google Spreadsheet**:
   - 1 Leaderboard Overview tab with live formula tracking.
   - 32 Country-specific tabs with category tags, clean names, status dropdowns, and deep links.
4. **Automated Measurement Pipeline**:
   - Baseline recorded at launch (`2026-09-18`).
   - Scheduled GitHub Action workflow (`.github/workflows/update-campaign-stats.yml`) keeping stats updated.

---

## 2. Reorganizing the Public Google Spreadsheet

To split the 3,124 rows of the master spreadsheet into **1 Overview Tab + 32 Country Tabs** with live formulas:

1. Open the public Google Sheet:
   [https://docs.google.com/spreadsheets/d/1LiO3IFgGZ2ftYpXLrFh8LpgBaTKBKeggz3jLwv8dxB8/edit](https://docs.google.com/spreadsheets/d/1LiO3IFgGZ2ftYpXLrFh8LpgBaTKBKeggz3jLwv8dxB8/edit)
2. In the top menu, click **Extensions** ➔ **Apps Script**.
3. Open the file [`scripts/GoogleAppsScript_SplitCountries.js`](../scripts/GoogleAppsScript_SplitCountries.js).
4. Copy the entire script, paste it into the Apps Script editor, replacing any default code.
5. Click **Save** (💾) and then click **Run** (`createPhotosForImpactTabs`).
6. When prompted, grant Google permissions to modify the spreadsheet.
7. Within ~30–60 seconds:
   - Your original raw sheet is preserved as `_Raw_Master_Data`.
   - A new **`📊 Leaderboard & Overview`** tab is created at the front with dynamic summary formulas (`=COUNTA`, `=COUNTIF`) linking to all countries.
   - 32 country tabs (e.g. `🇦🇹 Austria`, `🇨🇭 Switzerland`, `🇱🇻 Latvia`) are generated with frozen headers, KPI metric cards, and status dropdowns.

---

## 3. Tagline Campaign Assets & Validation

The campaign is configured across all three platforms:
- Android: `prod/tagline/android/main.json`
- iOS: `prod/tagline/ios/main.json`
- Web: `prod/tagline/web/main.json`

### Country-Level Targeting
`tagline_feed` defines feeds for `_AT`, `_BE`, `_BG`, `_HR`, `_CY`, `_CZ`, `_DK`, `_EE`, `_FI`, `_FR`, `_DE`, `_GR`, `_HU`, `_IE`, `_IT`, `_LV`, `_LT`, `_LU`, `_MT`, `_ME`, `_NL`, `_NO`, `_PL`, `_PT`, `_RO`, `_RS`, `_SK`, `_SI`, `_ES`, `_SE`, `_CH`, `_UK`.

Each country feed overrides the URL to deep-link to the user's country in the Campaign Hub:
```json
"_AT": {
  "news": [
    {
      "id": "photos_for_impact_2026",
      "override": {
        "url": "https://openfoodfacts.github.io/smooth-app_assets/photos-for-impact/?country=at"
      }
    }
  ]
}
```

### Validating Changes
Run the schema test suite anytime you modify taglines:
```bash
python3 tests/validate_tagline_json.py
```

---

## 4. Measurement & Dynamic Stats Pipeline

### Running the Measurement Script
```bash
python3 scripts/measure_campaign_stats.py
```
Outputs:
- `data/baseline_2026_09_18.json`: Preserves the start-of-campaign baseline.
- `data/campaign_stats.json`: Latest coverage % and deltas per country.
- `data/countries_data.json`: Full category listings and metadata.
- `release-website/photos-for-impact/data.js`: Real-time data feed for the web hub.

### GitHub Actions Automation
The workflow `.github/workflows/update-campaign-stats.yml` runs every Sunday at midnight (or on demand via GitHub's "Run workflow" button) to refresh metrics and commit updates.
