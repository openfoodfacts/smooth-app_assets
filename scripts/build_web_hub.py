#!/usr/bin/env python3
"""
Generate the standalone mobile-first "Scan Champion" scanning list HTML.
Refactored to provide a simple, high-density Google Keep-style checklist
for scanning and photographing popular products in store or in pantry.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Scan Champion 🤳🍫 — Scanning List | Open Food Facts</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Matomo -->
    <script>
      var _paq = window._paq = window._paq || [];
      /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
      _paq.push(['setDoNotTrack', true]);
      _paq.push(['disableCookies']);
      _paq.push(['trackPageView']);
      _paq.push(['enableLinkTracking']);
      (function() {
        var u="https://analytics.openfoodfacts.org/";
        _paq.push(['setTrackerUrl', u+'matomo.php']);
        _paq.push(['setSiteId', '19']);
        var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
        g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
      })();
    </script>
    <noscript><p><img src="https://analytics.openfoodfacts.org/matomo.php?idsite=19&amp;rec=1" style="border:0;" alt="" /></p></noscript>
    <!-- End Matomo Code -->
    <style>
        :root {
            --primary: #1b7340;
            --primary-dark: #12522c;
            --primary-light: #e8f5e9;
            --primary-border: #a5d6a7;
            --accent-gold: #f59e0b;
            --accent-blue: #2563eb;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --text-light: #94a3b8;
            --border: #e2e8f0;
            --border-hover: #cbd5e1;
            --radius-lg: 14px;
            --radius-md: 10px;
            --radius-sm: 6px;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.08);
            --item-height: 40px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.45;
            padding-bottom: 70px;
            -webkit-font-smoothing: antialiased;
        }

        /* Top Sticky Header */
        header {
            background: #ffffff;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: var(--shadow-sm);
        }

        .header-container {
            max-width: 820px;
            margin: 0 auto;
            padding: 10px 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }

        .brand-area {
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            color: var(--text-main);
            min-width: 0;
        }

        .brand-emoji {
            font-size: 22px;
            line-height: 1;
            flex-shrink: 0;
        }

        .brand-text {
            display: flex;
            flex-direction: column;
            min-width: 0;
        }

        .brand-title {
            font-size: 15px;
            font-weight: 800;
            letter-spacing: -0.3px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .brand-badge {
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--primary);
        }

        .country-select-wrapper {
            position: relative;
            flex-shrink: 0;
        }

        select.country-select {
            appearance: none;
            -webkit-appearance: none;
            background: #ffffff;
            border: 1.5px solid var(--border);
            padding: 6px 28px 6px 10px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            color: var(--text-main);
            cursor: pointer;
            box-shadow: var(--shadow-sm);
            max-width: 170px;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        select.country-select:focus {
            outline: none;
            border-color: var(--primary);
        }

        .country-select-wrapper::after {
            content: '▾';
            font-size: 11px;
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }

        main {
            max-width: 820px;
            margin: 0 auto;
            padding: 10px 12px;
        }

        /* Mission / Guide Card */
        .guide-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            margin-bottom: 10px;
            box-shadow: var(--shadow-sm);
            overflow: hidden;
            transition: all 0.2s ease;
        }

        .guide-header {
            padding: 10px 14px;
            background: linear-gradient(135deg, #1b7340 0%, #155724 100%);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            user-select: none;
        }

        .guide-header-title {
            font-size: 13px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .guide-toggle-btn {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: #ffffff;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
        }

        .guide-body {
            padding: 12px 14px;
            font-size: 13px;
            color: var(--text-main);
        }

        .guide-body.collapsed {
            display: none;
        }

        .guide-headline {
            font-weight: 700;
            font-size: 13px;
            margin-bottom: 8px;
            color: var(--primary-dark);
        }

        .guide-steps {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 8px;
            margin-bottom: 8px;
        }

        .guide-step {
            display: flex;
            align-items: flex-start;
            gap: 8px;
            background: var(--bg);
            border: 1px solid var(--border);
            padding: 8px 10px;
            border-radius: var(--radius-sm);
        }

        .guide-step-icon {
            font-size: 16px;
            flex-shrink: 0;
            margin-top: 1px;
        }

        .guide-step-text {
            font-size: 12px;
            line-height: 1.35;
        }

        .guide-step-text strong {
            display: block;
            color: var(--text-main);
            font-weight: 600;
        }

        .guide-tip-banner {
            background: #fffbeb;
            border: 1px solid #fef3c7;
            border-radius: var(--radius-sm);
            padding: 6px 10px;
            font-size: 12px;
            color: #92400e;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Sticky Control Bar */
        .controls-sticky {
            position: sticky;
            top: 53px;
            background: var(--bg);
            padding: 6px 0 8px 0;
            z-index: 90;
            border-bottom: 1px solid rgba(226, 232, 240, 0.8);
            margin-bottom: 8px;
        }

        /* 2 Tabs */
        .tab-bar {
            display: flex;
            background: #e2e8f0;
            border-radius: var(--radius-md);
            padding: 3px;
            gap: 3px;
            margin-bottom: 8px;
        }

        .tab-btn {
            flex: 1;
            padding: 8px 6px;
            border: none;
            background: transparent;
            border-radius: var(--radius-sm);
            font-size: 12.5px;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.15s ease;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            white-space: nowrap;
        }

        .tab-btn.active {
            background: #ffffff;
            color: var(--text-main);
            box-shadow: var(--shadow-sm);
            font-weight: 700;
        }

        .tab-btn .badge-pill {
            background: #e2e8f0;
            color: var(--text-main);
            padding: 1px 6px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 700;
        }

        .tab-btn.active .badge-pill {
            background: var(--primary-light);
            color: var(--primary-dark);
        }

        /* Search + Toolbar */
        .toolbar-row {
            display: flex;
            gap: 6px;
            align-items: center;
        }

        .search-box-wrapper {
            position: relative;
            flex: 1;
        }

        .search-box-wrapper input {
            width: 100%;
            padding: 8px 30px 8px 30px;
            border: 1px solid var(--border);
            border-radius: 20px;
            font-size: 13px;
            background: #ffffff;
            color: var(--text-main);
            box-shadow: var(--shadow-sm);
        }

        .search-box-wrapper input:focus {
            outline: none;
            border-color: var(--primary);
        }

        .search-icon {
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 12px;
            color: var(--text-muted);
            pointer-events: none;
        }

        .search-clear-btn {
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            background: #e2e8f0;
            border: none;
            color: var(--text-muted);
            border-radius: 50%;
            width: 18px;
            height: 18px;
            font-size: 10px;
            cursor: pointer;
            display: none;
            align-items: center;
            justify-content: center;
        }

        .search-clear-btn.visible {
            display: flex;
        }

        .btn-reset {
            background: #ffffff;
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 7px 10px;
            border-radius: 20px;
            font-size: 11.5px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
            flex-shrink: 0;
            box-shadow: var(--shadow-sm);
        }

        .btn-reset:hover {
            background: #fee2e2;
            color: #b91c1c;
            border-color: #fca5a5;
        }

        /* Mini Progress Bar */
        .progress-strip {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 6px;
            font-size: 11.5px;
            color: var(--text-muted);
            padding: 0 4px;
        }

        .progress-bar-track {
            flex: 1;
            height: 6px;
            background: #e2e8f0;
            border-radius: 10px;
            overflow: hidden;
        }

        .progress-bar-fill {
            height: 100%;
            background: var(--primary);
            border-radius: 10px;
            transition: width 0.3s ease;
        }

        .progress-text {
            font-weight: 600;
            white-space: nowrap;
        }

        /* Google Keep Style Checklist */
        .checklist-container {
            display: grid;
            grid-template-columns: 1fr;
            gap: 4px;
        }

        @media (min-width: 620px) {
            .checklist-container {
                grid-template-columns: repeat(2, 1fr);
                gap: 6px;
            }
        }

        /* Checklist Item Row */
        .check-item {
            display: flex;
            align-items: center;
            gap: 10px;
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 8px 12px;
            min-height: var(--item-height);
            cursor: pointer;
            user-select: none;
            transition: background 0.12s ease, border-color 0.12s ease;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        }

        .check-item:hover {
            border-color: var(--border-hover);
            background: #fdfdfd;
        }

        .check-item:active {
            transform: scale(0.995);
        }

        /* Checkbox Box */
        .check-box {
            width: 18px;
            height: 18px;
            border: 1.8px solid #94a3b8;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            transition: all 0.15s ease;
            background: #ffffff;
        }

        .check-item.done .check-box {
            background: var(--primary);
            border-color: var(--primary);
        }

        .check-box svg {
            display: none;
            width: 12px;
            height: 12px;
            stroke: #ffffff;
            stroke-width: 2.5;
            fill: none;
        }

        .check-item.done .check-box svg {
            display: block;
        }

        /* Item Text */
        .check-label-wrap {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex: 1;
            min-width: 0;
            gap: 6px;
        }

        .check-label {
            font-size: 13px;
            font-weight: 500;
            color: var(--text-main);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .check-item.done .check-label {
            text-decoration: line-through;
            color: var(--text-light);
        }

        .item-priority-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #f97316;
            flex-shrink: 0;
            title: "Missing staple";
        }

        /* Completed Accordion Divider (Keep Style) */
        .completed-section {
            margin-top: 14px;
            border-top: 1px solid var(--border);
            padding-top: 10px;
        }

        .completed-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 10px;
            font-size: 12px;
            font-weight: 700;
            color: var(--text-muted);
            cursor: pointer;
            border-radius: var(--radius-sm);
            user-select: none;
            background: #f1f5f9;
            margin-bottom: 6px;
        }

        .completed-header:hover {
            background: #e2e8f0;
        }

        .completed-header .chevron {
            font-size: 11px;
            transition: transform 0.2s ease;
        }

        .completed-header.collapsed .chevron {
            transform: rotate(-90deg);
        }

        .completed-items-list.collapsed {
            display: none;
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 30px 16px;
            color: var(--text-muted);
            background: #ffffff;
            border: 1px dashed var(--border);
            border-radius: var(--radius-md);
            margin-top: 10px;
        }

        .empty-state-icon {
            font-size: 32px;
            margin-bottom: 6px;
        }

        .empty-state-title {
            font-weight: 700;
            font-size: 14px;
            color: var(--text-main);
            margin-bottom: 4px;
        }

        .empty-state-desc {
            font-size: 12px;
        }

        /* Discrete Footer */
        footer {
            margin-top: 30px;
            padding-top: 16px;
            border-top: 1px solid var(--border);
            text-align: center;
            font-size: 11px;
            color: var(--text-muted);
        }

        footer a {
            color: var(--text-muted);
            text-decoration: underline;
        }
    </style>
</head>
<body>

    <!-- Sticky App Header -->
    <header>
        <div class="header-container">
            <div class="brand-area">
                <span class="brand-emoji">🤳🍫</span>
                <div class="brand-text">
                    <span class="brand-title">Scan Champion</span>
                    <span class="brand-badge">Open Food Facts</span>
                </div>
            </div>
            <div class="country-select-wrapper">
                <select id="countrySelect" class="country-select" aria-label="Select country"></select>
            </div>
        </div>
    </header>

    <main>
        <!-- Instructions / Scanning Guide (Collapsible for active shoppers) -->
        <section class="guide-card" id="guideCard">
            <div class="guide-header" id="guideToggle">
                <div class="guide-header-title">
                    <span>🛒 Scan Champion Instructions</span>
                </div>
                <button class="guide-toggle-btn" id="guideToggleBtn">Hide tips</button>
            </div>
            <div class="guide-body" id="guideBody">
                <div class="guide-headline">Scan and photograph popular products sold in your country</div>
                <div class="guide-steps">
                    <div class="guide-step">
                        <span class="guide-step-icon">🏪</span>
                        <div class="guide-step-text">
                            <strong>In Store or In Pantry</strong>
                            Scan products with the Open Food Facts app using this Scan List.
                        </div>
                    </div>
                    <div class="guide-step">
                        <span class="guide-step-icon">📸</span>
                        <div class="guide-step-text">
                            <strong>Add 3 Clean Photos</strong>
                            Product front packaging, ingredient lists, and nutrition facts.
                        </div>
                    </div>
                    <div class="guide-step">
                        <span class="guide-step-icon">🌟</span>
                        <div class="guide-step-text">
                            <strong>Popular Products</strong>
                            Categories we absolutely need for your country basket.
                        </div>
                    </div>
                </div>
                <div class="guide-tip-banner">
                    <span>💡</span>
                    <span><strong>Pro-tip:</strong> If a category sounds strange, just go to the closest category in the aisle!</span>
                </div>
            </div>
        </section>

        <!-- Sticky Controls Bar: 2 Tabs, Search, and Progress -->
        <div class="controls-sticky">
            <!-- 2 Tabs: High Priority (Missing) & All Categories -->
            <div class="tab-bar">
                <button class="tab-btn active" data-tab="missing" id="tabMissing">
                    <span>🔥 High Priority (Missing)</span>
                    <span class="badge-pill" id="badgeMissing">0</span>
                </button>
                <button class="tab-btn" data-tab="all" id="tabAll">
                    <span>📋 All Categories</span>
                    <span class="badge-pill" id="badgeAll">0</span>
                </button>
            </div>

            <!-- Search + Reset Bar -->
            <div class="toolbar-row">
                <div class="search-box-wrapper">
                    <span class="search-icon">🔍</span>
                    <input type="search" id="searchInput" placeholder="Filter categories (e.g. beer, bread, cheese)..." autocomplete="off" />
                    <button class="search-clear-btn" id="searchClearBtn" aria-label="Clear search">✕</button>
                </div>
                <button class="btn-reset" id="btnReset" title="Clear all ticks for this country">
                    <span>↺</span>
                    <span>Reset</span>
                </button>
            </div>

            <!-- Mini Progress Indicator -->
            <div class="progress-strip">
                <div class="progress-bar-track">
                    <div class="progress-bar-fill" id="progressBarFill" style="width: 0%;"></div>
                </div>
                <span class="progress-text" id="progressSummary">0 / 0 scanned</span>
            </div>
        </div>

        <!-- Active Unchecked Items (High Density Checklist) -->
        <div class="checklist-container" id="activeChecklist">
            <!-- Items rendered via JS -->
        </div>

        <!-- Completed Items Section (Google Keep Style) -->
        <section class="completed-section" id="completedSection" style="display: none;">
            <div class="completed-header" id="completedHeader">
                <span id="completedHeaderLabel">✓ Completed (0 items)</span>
                <span class="chevron">▾</span>
            </div>
            <div class="checklist-container completed-items-list" id="completedChecklist">
                <!-- Completed items rendered via JS -->
            </div>
        </section>

        <!-- Empty State Container -->
        <div id="emptyState" style="display: none;"></div>

        <!-- Minimal Discrete Footer -->
        <footer>
            Open Food Facts · Scan Champion Scanning List · Ticks saved locally on your device
        </footer>
    </main>

    <!-- Load Data Feeds -->
    <script src="data.js"></script>
    <script>
        // State management
        let currentCountry = 'at';
        let currentTab = 'missing'; // 'missing' or 'all'
        let currentSearch = '';
        let completedCollapsed = false;

        function getStorageKey(country) {
            return 'scan_champion_done_' + country;
        }

        function getCheckedTags(country) {
            try {
                const stored = localStorage.getItem(getStorageKey(country));
                return stored ? new Set(JSON.parse(stored)) : new Set();
            } catch (e) {
                console.error('Error reading localStorage', e);
                return new Set();
            }
        }

        function saveCheckedTags(country, tagSet) {
            try {
                localStorage.setItem(getStorageKey(country), JSON.stringify(Array.from(tagSet)));
            } catch (e) {
                console.error('Error writing localStorage', e);
            }
        }

        function getParam(param) {
            const params = new URLSearchParams(window.location.search);
            return params.get(param);
        }

        function toggleItem(tag) {
            const checkedSet = getCheckedTags(currentCountry);
            if (checkedSet.has(tag)) {
                checkedSet.delete(tag);
            } else {
                checkedSet.add(tag);
                if (navigator.vibrate) {
                    try { navigator.vibrate(12); } catch (e) {}
                }
            }
            saveCheckedTags(currentCountry, checkedSet);
            render();
        }

        function resetCurrentCountry() {
            const countryMeta = (window.CAMPAIGN_STATS && window.CAMPAIGN_STATS.countries) ? window.CAMPAIGN_STATS.countries[currentCountry] : null;
            const countryName = countryMeta ? countryMeta.name : currentCountry.toUpperCase();
            if (confirm(`Reset all checked categories for ${countryName}?`)) {
                localStorage.removeItem(getStorageKey(currentCountry));
                render();
            }
        }

        function init() {
            if (!window.CAMPAIGN_STATS || !window.COUNTRIES_DATA) {
                console.error('Campaign data not loaded');
                return;
            }

            const countries = window.CAMPAIGN_STATS.countries;
            const select = document.getElementById('countrySelect');
            select.innerHTML = '';

            const paramC = getParam('country');
            const userLocale = (navigator.language || '').toLowerCase().split('-')[1];

            // Populate country select with flags and names
            const sortedCodes = Object.keys(countries).sort((a, b) => countries[a].name.localeCompare(countries[b].name));
            sortedCodes.forEach(code => {
                const c = countries[code];
                const opt = document.createElement('option');
                opt.value = code;
                opt.textContent = `${c.flag} ${c.name}`;
                select.appendChild(opt);
            });

            // Set initial country
            if (paramC && countries[paramC.toLowerCase()]) {
                currentCountry = paramC.toLowerCase();
            } else if (userLocale && countries[userLocale]) {
                currentCountry = userLocale;
            } else {
                currentCountry = 'at';
            }
            select.value = currentCountry;

            // Country selection change
            select.addEventListener('change', (e) => {
                currentCountry = e.target.value;
                const url = new URL(window.location);
                url.searchParams.set('country', currentCountry);
                window.history.replaceState({}, '', url);

                if (window._paq) {
                    _paq.push(['setCustomUrl', window.location.href]);
                    _paq.push(['setDocumentTitle', 'Scan Champion - ' + (countries[currentCountry] ? countries[currentCountry].name : currentCountry.toUpperCase())]);
                    _paq.push(['trackPageView']);
                }
                render();
            });

            // Tab Buttons (2 tabs: missing, all)
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentTab = btn.getAttribute('data-tab');
                    render();
                });
            });

            // Search input
            const searchInput = document.getElementById('searchInput');
            const clearBtn = document.getElementById('searchClearBtn');

            searchInput.addEventListener('input', (e) => {
                currentSearch = e.target.value.toLowerCase().trim();
                clearBtn.classList.toggle('visible', !!currentSearch);
                render();
            });

            clearBtn.addEventListener('click', () => {
                searchInput.value = '';
                currentSearch = '';
                clearBtn.classList.remove('visible');
                render();
                searchInput.focus();
            });

            // Reset button
            document.getElementById('btnReset').addEventListener('click', resetCurrentCountry);

            // Completed header toggle (Google Keep style)
            const completedHeader = document.getElementById('completedHeader');
            completedHeader.addEventListener('click', () => {
                completedCollapsed = !completedCollapsed;
                completedHeader.classList.toggle('collapsed', completedCollapsed);
                document.getElementById('completedChecklist').classList.toggle('collapsed', completedCollapsed);
            });

            // Guide collapse toggle
            const guideCard = document.getElementById('guideCard');
            const guideBody = document.getElementById('guideBody');
            const guideToggle = document.getElementById('guideToggle');
            const guideToggleBtn = document.getElementById('guideToggleBtn');

            const isGuideCollapsed = localStorage.getItem('scan_champion_guide_collapsed') === 'true';
            if (isGuideCollapsed) {
                guideBody.classList.add('collapsed');
                guideToggleBtn.textContent = 'Show tips';
            }

            guideToggle.addEventListener('click', () => {
                const collapsed = guideBody.classList.toggle('collapsed');
                guideToggleBtn.textContent = collapsed ? 'Show tips' : 'Hide tips';
                localStorage.setItem('scan_champion_guide_collapsed', collapsed ? 'true' : 'false');
            });

            render();
        }

        function createItemNode(item, isChecked, isMissing) {
            const div = document.createElement('div');
            div.className = 'check-item' + (isChecked ? ' done' : '');
            div.setAttribute('data-tag', item.category_tag);

            div.innerHTML = `
                <div class="check-box" aria-hidden="true">
                    <svg viewBox="0 0 24 24">
                        <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                </div>
                <div class="check-label-wrap">
                    <span class="check-label">${item.category_name}</span>
                    ${(currentTab === 'all' && isMissing) ? '<span class="item-priority-dot" title="High Priority Missing"></span>' : ''}
                </div>
            `;

            div.addEventListener('click', () => {
                toggleItem(item.category_tag);
            });

            return div;
        }

        function render() {
            const countryFull = window.COUNTRIES_DATA[currentCountry];
            if (!countryFull) return;

            const allCategories = countryFull.categories;
            const checkedSet = getCheckedTags(currentCountry);

            // Compute counts for the 2 tabs
            const missingCategories = allCategories.filter(c => !c.has_code);
            const totalMissing = missingCategories.length;
            const checkedMissing = missingCategories.filter(c => checkedSet.has(c.category_tag)).length;

            const totalAll = allCategories.length;
            const checkedAll = allCategories.filter(c => checkedSet.has(c.category_tag)).length;

            // Update tab badges
            document.getElementById('badgeMissing').textContent = `${checkedMissing}/${totalMissing}`;
            document.getElementById('badgeAll').textContent = `${checkedAll}/${totalAll}`;

            // Determine active pool based on current tab
            const sourcePool = (currentTab === 'missing') ? missingCategories : allCategories;
            const currentCheckedCount = (currentTab === 'missing') ? checkedMissing : checkedAll;
            const currentTotalCount = sourcePool.length;

            // Update Progress Bar
            const pct = currentTotalCount > 0 ? Math.round((currentCheckedCount / currentTotalCount) * 100) : 0;
            document.getElementById('progressBarFill').style.width = `${pct}%`;
            document.getElementById('progressSummary').textContent = `${currentCheckedCount} of ${currentTotalCount} scanned (${pct}%)`;

            // Filter items by search query
            let filtered = sourcePool;
            if (currentSearch) {
                filtered = sourcePool.filter(c => 
                    c.category_name.toLowerCase().includes(currentSearch) ||
                    c.category_tag.toLowerCase().includes(currentSearch)
                );
            }

            // Split into Unchecked and Completed (Google Keep style)
            const activeItems = [];
            const completedItems = [];

            filtered.forEach(item => {
                const isChecked = checkedSet.has(item.category_tag);
                if (isChecked) {
                    completedItems.push(item);
                } else {
                    activeItems.push(item);
                }
            });

            // Render Active Items
            const activeListEl = document.getElementById('activeChecklist');
            activeListEl.innerHTML = '';
            activeItems.forEach(item => {
                activeListEl.appendChild(createItemNode(item, false, !item.has_code));
            });

            // Render Completed Items
            const completedSection = document.getElementById('completedSection');
            const completedListEl = document.getElementById('completedChecklist');
            const completedHeaderLabel = document.getElementById('completedHeaderLabel');

            if (completedItems.length > 0) {
                completedSection.style.display = 'block';
                completedHeaderLabel.textContent = `✓ Completed (${completedItems.length} item${completedItems.length > 1 ? 's' : ''})`;
                completedListEl.innerHTML = '';
                completedItems.forEach(item => {
                    completedListEl.appendChild(createItemNode(item, true, !item.has_code));
                });
            } else {
                completedSection.style.display = 'none';
            }

            // Empty state check
            const emptyStateEl = document.getElementById('emptyState');
            if (filtered.length === 0) {
                emptyStateEl.style.display = 'block';
                if (currentSearch) {
                    emptyStateEl.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-state-icon">🔍</div>
                            <div class="empty-state-title">No categories found</div>
                            <div class="empty-state-desc">No categories in this list match "<strong>${currentSearch}</strong>".</div>
                        </div>
                    `;
                } else if (currentTab === 'missing' && totalMissing === 0) {
                    emptyStateEl.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-state-icon">🎉</div>
                            <div class="empty-state-title">All high-priority categories covered!</div>
                            <div class="empty-state-desc">Switch to "All Categories" to discover more products to photograph.</div>
                        </div>
                    `;
                }
            } else if (activeItems.length === 0 && completedItems.length > 0 && !currentSearch) {
                emptyStateEl.style.display = 'block';
                emptyStateEl.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">🏆</div>
                        <div class="empty-state-title">Scan Champion! All ${completedItems.length} items checked!</div>
                        <div class="empty-state-desc">Great job! You scanned all categories in this list. Tap completed items to uncheck or hit Reset to scan again.</div>
                    </div>
                `;
            } else {
                emptyStateEl.style.display = 'none';
            }
        }

        window.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
"""

DEST_FILES = [
    os.path.join(BASE_DIR, 'photos-for-impact', 'index.html'),
    os.path.join(BASE_DIR, 'release-website', 'photos-for-impact', 'index.html'),
]

def main():
    for dest_file in DEST_FILES:
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(HTML_CONTENT.strip() + '\n')
        print(f"Generated {dest_file} successfully!")

if __name__ == '__main__':
    main()
