#!/usr/bin/env python3
"""
Generate the standalone mobile-first campaign hub HTML for Photos for Impact.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST_FILE = os.path.join(BASE_DIR, 'release-website', 'photos-for-impact', 'index.html')

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Photos for Impact — Open Food Facts</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #347644;
            --primary-dark: #22562E;
            --primary-light: #EBF3E8;
            --accent: #2D72D2;
            --accent-orange: #E87A00;
            --bg: #F8F9FA;
            --card-bg: #FFFFFF;
            --text-main: #1C2024;
            --text-muted: #60646C;
            --border: #E6E8EB;
            --radius-lg: 16px;
            --radius-md: 12px;
            --radius-sm: 8px;
            --shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            --shadow-sm: 0 2px 6px rgba(0, 0, 0, 0.04);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.5;
            padding-bottom: 60px;
        }

        /* Top Header */
        header {
            background: #FFFFFF;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: var(--shadow-sm);
        }

        .header-container {
            max-width: 680px;
            margin: 0 auto;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .logo-area {
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: var(--text-main);
            font-weight: 700;
            font-size: 16px;
        }

        .logo-badge {
            background: var(--primary);
            color: #FFFFFF;
            padding: 4px 8px;
            border-radius: var(--radius-sm);
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .country-select-wrapper {
            position: relative;
        }

        select.country-select {
            appearance: none;
            background: #FFFFFF;
            border: 1px solid var(--border);
            padding: 8px 32px 8px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            color: var(--text-main);
            cursor: pointer;
            box-shadow: var(--shadow-sm);
        }

        .country-select-wrapper::after {
            content: '▼';
            font-size: 10px;
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }

        main {
            max-width: 680px;
            margin: 0 auto;
            padding: 16px;
        }

        /* Hero Card */
        .hero-card {
            background: linear-gradient(135deg, #2D72D2 0%, #174EA6 100%);
            color: #FFFFFF;
            border-radius: var(--radius-lg);
            padding: 24px 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 24px rgba(45, 114, 210, 0.25);
            position: relative;
            overflow: hidden;
        }

        .hero-card::after {
            content: '📸';
            font-size: 120px;
            position: absolute;
            right: -15px;
            bottom: -25px;
            opacity: 0.15;
            pointer-events: none;
        }

        .hero-tag {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(8px);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 12px;
        }

        .hero-title {
            font-size: 22px;
            font-weight: 800;
            margin-bottom: 8px;
            line-height: 1.3;
        }

        .hero-subtitle {
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 20px;
            max-width: 520px;
        }

        /* Progress Bar in Hero */
        .progress-box {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(10px);
            border-radius: var(--radius-md);
            padding: 16px;
        }

        .progress-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 8px;
        }

        .progress-pct {
            font-size: 28px;
            font-weight: 800;
        }

        .progress-label {
            font-size: 13px;
            opacity: 0.9;
        }

        .progress-bar-bg {
            background: rgba(255, 255, 255, 0.25);
            border-radius: 10px;
            height: 12px;
            overflow: hidden;
            margin-bottom: 12px;
        }

        .progress-bar-fill {
            background: #FFB800;
            height: 100%;
            border-radius: 10px;
            transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .progress-stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            text-align: center;
        }

        .stat-item {
            background: rgba(0, 0, 0, 0.15);
            padding: 8px;
            border-radius: var(--radius-sm);
        }

        .stat-num {
            font-size: 16px;
            font-weight: 700;
        }

        .stat-desc {
            font-size: 11px;
            opacity: 0.85;
        }

        /* Quick Action Guide */
        .guide-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 16px;
            margin-bottom: 20px;
            box-shadow: var(--shadow-sm);
        }

        .guide-title {
            font-size: 15px;
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .steps-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .step-row {
            display: flex;
            gap: 12px;
            align-items: flex-start;
        }

        .step-bubble {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: var(--primary-light);
            color: var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 700;
            flex-shrink: 0;
            margin-top: 2px;
        }

        .step-text {
            font-size: 13px;
            color: var(--text-muted);
        }

        .step-text strong {
            color: var(--text-main);
        }

        /* Filter Tabs */
        .tab-bar {
            display: flex;
            background: #EAECEF;
            border-radius: var(--radius-md);
            padding: 4px;
            margin-bottom: 16px;
            gap: 4px;
        }

        .tab-btn {
            flex: 1;
            padding: 10px 8px;
            border: none;
            background: transparent;
            border-radius: var(--radius-sm);
            font-size: 13px;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s;
            text-align: center;
        }

        .tab-btn.active {
            background: #FFFFFF;
            color: var(--text-main);
            box-shadow: var(--shadow-sm);
        }

        /* Search input */
        .search-box {
            position: relative;
            margin-bottom: 16px;
        }

        .search-box input {
            width: 100%;
            padding: 12px 16px 12px 38px;
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            font-size: 14px;
            background: #FFFFFF;
            color: var(--text-main);
        }

        .search-box::before {
            content: '🔍';
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 14px;
            color: var(--text-muted);
        }

        /* Category Item Cards */
        .items-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .item-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 14px 16px;
            box-shadow: var(--shadow-sm);
            display: flex;
            flex-direction: column;
            gap: 8px;
            transition: transform 0.15s;
        }

        .item-card:active {
            transform: scale(0.99);
        }

        .item-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 10px;
        }

        .item-title {
            font-size: 15px;
            font-weight: 600;
            color: var(--text-main);
        }

        .item-tag {
            font-size: 11px;
            color: var(--text-muted);
            font-family: monospace;
        }

        .badge-status {
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            white-space: nowrap;
        }

        .badge-missing {
            background: #FFF3E0;
            color: #D9530F;
            border: 1px solid #FFE0B2;
        }

        .badge-covered {
            background: #E8F5E9;
            color: #2E7D32;
            border: 1px solid #C8E6C9;
        }

        .item-actions {
            display: flex;
            gap: 8px;
            margin-top: 4px;
            flex-wrap: wrap;
        }

        .btn-action {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 12px;
            border-radius: var(--radius-sm);
            font-size: 12px;
            font-weight: 600;
            text-decoration: none;
            transition: background 0.15s;
        }

        .btn-primary {
            background: var(--primary);
            color: #FFFFFF;
        }

        .btn-primary:hover {
            background: var(--primary-dark);
        }

        .btn-secondary {
            background: #F0F4F8;
            color: var(--accent);
            border: 1px solid #D9E2EC;
        }

        .btn-secondary:hover {
            background: #E2E8F0;
        }

        /* Footer community banner */
        .footer-banner {
            margin-top: 30px;
            padding: 20px;
            background: #FFFFFF;
            border: 1px dashed var(--border);
            border-radius: var(--radius-lg);
            text-align: center;
        }

        .footer-banner h3 {
            font-size: 16px;
            margin-bottom: 6px;
        }

        .footer-banner p {
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 14px;
        }

        .btn-sheet {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #0F9D58;
            color: #FFFFFF;
            padding: 10px 18px;
            border-radius: 24px;
            text-decoration: none;
            font-weight: 600;
            font-size: 13px;
            box-shadow: 0 4px 10px rgba(15, 157, 88, 0.25);
        }
    </style>
</head>
<body>

    <header>
        <div class="header-container">
            <a href="#" class="logo-area">
                <span>🥗 Open Food Facts</span>
                <span class="logo-badge">Campaign</span>
            </a>
            <div class="country-select-wrapper">
                <select id="countrySelect" class="country-select" aria-label="Select country"></select>
            </div>
        </div>
    </header>

    <main>
        <!-- Hero Section -->
        <section class="hero-card">
            <div class="hero-tag" id="heroTag">Photos for Impact</div>
            <h1 class="hero-title" id="heroTitle">Loading campaign...</h1>
            <p class="hero-subtitle" id="heroSubtitle">Photograph missing everyday foods in your country to complete our representative food basket.</p>

            <div class="progress-box">
                <div class="progress-header">
                    <div class="progress-pct" id="progressPct">0%</div>
                    <div class="progress-label" id="progressCount">0 / 0 covered</div>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" id="progressBar" style="width: 0%;"></div>
                </div>
                <div class="progress-stats-grid">
                    <div class="stat-item">
                        <div class="stat-num" id="statMissing">0</div>
                        <div class="stat-desc">Missing Photos</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-num" id="statCovered">0</div>
                        <div class="stat-desc">In Database</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-num" id="statBaseline">0%</div>
                        <div class="stat-desc">Launch Baseline</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Action Guide -->
        <section class="guide-card">
            <h2 class="guide-title">⚡ How to contribute during your grocery run</h2>
            <div class="steps-container">
                <div class="step-row">
                    <div class="step-bubble">1</div>
                    <div class="step-text"><strong>Pick a missing category</strong> from the list below before shopping.</div>
                </div>
                <div class="step-row">
                    <div class="step-bubble">2</div>
                    <div class="step-text"><strong>Scan the barcode</strong> using the Open Food Facts app when in the store.</div>
                </div>
                <div class="step-row">
                    <div class="step-bubble">3</div>
                    <div class="step-text"><strong>Snap 3 photos:</strong> Front packaging, ingredients list, and nutrition table.</div>
                </div>
            </div>
        </section>

        <!-- Category Browser -->
        <section>
            <div class="tab-bar">
                <button class="tab-btn active" data-filter="missing" id="tabMissing">📸 Missing Items (<span id="countTabMissing">0</span>)</button>
                <button class="tab-btn" data-filter="covered" id="tabCovered">✅ In Database (<span id="countTabCovered">0</span>)</button>
                <button class="tab-btn" data-filter="all" id="tabAll">All Categories (<span id="countTabAll">0</span>)</button>
            </div>

            <div class="search-box">
                <input type="search" id="searchInput" placeholder="Search categories (e.g. beer, bread, cheese)..." />
            </div>

            <div class="items-list" id="itemsList">
                <p style="text-align:center; padding: 20px; color: var(--text-muted);">Loading categories...</p>
            </div>
        </section>

        <!-- Community Spreadsheet Link -->
        <section class="footer-banner">
            <h3>Prefer editing on desktop?</h3>
            <p>You can also collaborate directly in our public community Google Spreadsheet with one tab per country.</p>
            <a href="https://docs.google.com/spreadsheets/d/1LiO3IFgGZ2ftYpXLrFh8LpgBaTKBKeggz3jLwv8dxB8/edit#gid=0" target="_blank" class="btn-sheet">
                <span>📊 Open Public Google Spreadsheet</span>
            </a>
        </section>
    </main>

    <!-- Load live stats feed -->
    <script src="data.js"></script>
    <script>
        let currentCountry = 'at';
        let currentFilter = 'missing';
        let currentSearch = '';

        function getParam(param) {
            const params = new URLSearchParams(window.location.search);
            return params.get(param);
        }

        function init() {
            if (!window.CAMPAIGN_STATS || !window.COUNTRIES_DATA) {
                console.error('Data not loaded');
                return;
            }

            const countries = window.CAMPAIGN_STATS.countries;
            const select = document.getElementById('countrySelect');
            select.innerHTML = '';

            const paramC = getParam('country');
            const userLocale = (navigator.language || '').toLowerCase().split('-')[1];

            // Populate country select
            const sortedCodes = Object.keys(countries).sort((a, b) => countries[a].name.localeCompare(countries[b].name));
            sortedCodes.forEach(code => {
                const c = countries[code];
                const opt = document.createElement('option');
                opt.value = code;
                opt.textContent = `${c.flag} ${c.name}`;
                select.appendChild(opt);
            });

            // Auto-select country from query param or fallback
            if (paramC && countries[paramC.toLowerCase()]) {
                currentCountry = paramC.toLowerCase();
            } else if (userLocale && countries[userLocale]) {
                currentCountry = userLocale;
            } else {
                currentCountry = 'at'; // Default
            }

            select.value = currentCountry;
            select.addEventListener('change', (e) => {
                currentCountry = e.target.value;
                const url = new URL(window.location);
                url.searchParams.set('country', currentCountry);
                window.history.replaceState({}, '', url);
                render();
            });

            // Tab listeners
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentFilter = btn.getAttribute('data-filter');
                    renderList();
                });
            });

            // Search listener
            document.getElementById('searchInput').addEventListener('input', (e) => {
                currentSearch = e.target.value.toLowerCase().trim();
                renderList();
            });

            render();
        }

        function render() {
            const countryMeta = window.CAMPAIGN_STATS.countries[currentCountry];
            const countryFull = window.COUNTRIES_DATA[currentCountry];

            if (!countryMeta || !countryFull) return;

            document.getElementById('heroTag').textContent = `${countryMeta.flag} ${countryMeta.name} · Priority Quest`;
            document.getElementById('heroTitle').textContent = `Help complete ${countryMeta.name}'s food database!`;
            document.getElementById('heroSubtitle').textContent = `We have recorded ${countryMeta.coverage_pct}% of representative staples. Photograph the remaining ${countryMeta.missing} missing foods!`;

            document.getElementById('progressPct').textContent = `${countryMeta.coverage_pct}%`;
            document.getElementById('progressCount').textContent = `${countryMeta.with_code} / ${countryMeta.total} covered`;
            document.getElementById('progressBar').style.width = `${countryMeta.coverage_pct}%`;

            document.getElementById('statMissing').textContent = countryMeta.missing;
            document.getElementById('statCovered').textContent = countryMeta.with_code;
            document.getElementById('statBaseline').textContent = `${countryMeta.start_baseline_pct}%`;

            const missingCount = countryFull.categories.filter(c => !c.has_code).length;
            const coveredCount = countryFull.categories.filter(c => c.has_code).length;
            document.getElementById('countTabMissing').textContent = missingCount;
            document.getElementById('countTabCovered').textContent = coveredCount;
            document.getElementById('countTabAll').textContent = countryFull.categories.length;

            renderList();
        }

        function renderList() {
            const countryFull = window.COUNTRIES_DATA[currentCountry];
            if (!countryFull) return;

            const container = document.getElementById('itemsList');
            let items = countryFull.categories;

            // Apply filter
            if (currentFilter === 'missing') {
                items = items.filter(c => !c.has_code);
            } else if (currentFilter === 'covered') {
                items = items.filter(c => c.has_code);
            }

            // Apply search
            if (currentSearch) {
                items = items.filter(c => 
                    c.category_name.toLowerCase().includes(currentSearch) ||
                    c.category_tag.toLowerCase().includes(currentSearch) ||
                    (c.code && c.code.includes(currentSearch))
                );
            }

            if (items.length === 0) {
                container.innerHTML = `<div style="text-align: center; padding: 40px 10px; color: var(--text-muted);">
                    <div style="font-size: 40px; margin-bottom: 8px;">🎉</div>
                    <p style="font-weight: 600;">No products found matching your search.</p>
                </div>`;
                return;
            }

            container.innerHTML = items.map(item => {
                const isMissing = !item.has_code;
                const statusBadge = isMissing 
                    ? `<span class="badge-status badge-missing">📸 Needs Barcode & Photo</span>`
                    : `<span class="badge-status badge-covered">✅ In OFF (${item.code})</span>`;

                let actionButtons = '';
                if (!isMissing) {
                    actionButtons = `
                        <a href="https://world.openfoodfacts.org/product/${item.code}" target="_blank" class="btn-action btn-primary">
                            <span>🔍 View in OFF App</span>
                        </a>
                        <a href="${item.hunger_games_url}" target="_blank" class="btn-action btn-secondary">
                            <span>🎮 Categorize</span>
                        </a>
                    `;
                } else {
                    actionButtons = `
                        <a href="${item.hunger_games_url}" target="_blank" class="btn-action btn-secondary">
                            <span>🎯 Hunger Games Quest</span>
                        </a>
                        <span style="font-size: 11px; color: var(--text-muted); align-self: center;">
                            👉 In store: Scan with Open Food Facts app!
                        </span>
                    `;
                }

                return `
                    <div class="item-card">
                        <div class="item-top">
                            <div>
                                <div class="item-title">${item.category_name}</div>
                                <div class="item-tag">${item.category_tag}</div>
                            </div>
                            ${statusBadge}
                        </div>
                        <div class="item-actions">
                            ${actionButtons}
                        </div>
                    </div>
                `;
            }).join('');
        }

        window.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
"""

def main():
    os.makedirs(os.path.dirname(DEST_FILE), exist_ok=True)
    with open(DEST_FILE, 'w', encoding='utf-8') as f:
        f.write(HTML_CONTENT)
    print(f"Generated {DEST_FILE} successfully!")

if __name__ == '__main__':
    main()
