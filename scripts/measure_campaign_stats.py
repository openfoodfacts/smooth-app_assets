#!/usr/bin/env python3
"""
Photos for Impact - Measurement Engine and Stats Tracker
Tracks progress of representative products for 32 countries.
Measures start-of-campaign baseline, current coverage %, and missing products.
"""

import csv
import json
import os
import sys
from datetime import datetime
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'representative_products.csv')
SCRATCH_CSV = '/Users/pierre/.gemini/antigravity/brain/0d4fa303-1fa1-4bb0-86d5-9d0b279f044a/scratch/sheet.csv'
DATA_DIR = os.path.join(BASE_DIR, 'data')
BASELINE_FILE = os.path.join(DATA_DIR, 'baseline_2026_09_18.json')
STATS_FILE = os.path.join(DATA_DIR, 'campaign_stats.json')
COUNTRIES_DATA_FILE = os.path.join(DATA_DIR, 'countries_data.json')

COUNTRY_METADATA = {
    'Austria': {'code': 'at', 'flag': '🇦🇹', 'off_tag': 'en:austria', 'languages': ['de']},
    'Belgium': {'code': 'be', 'flag': '🇧🇪', 'off_tag': 'en:belgium', 'languages': ['fr', 'nl', 'de']},
    'Bulgaria': {'code': 'bg', 'flag': '🇧🇬', 'off_tag': 'en:bulgaria', 'languages': ['bg']},
    'Croatia': {'code': 'hr', 'flag': '🇭🇷', 'off_tag': 'en:croatia', 'languages': ['hr']},
    'Cyprus': {'code': 'cy', 'flag': '🇨🇾', 'off_tag': 'en:cyprus', 'languages': ['el', 'tr']},
    'Czech Republic': {'code': 'cs', 'flag': '🇨🇿', 'off_tag': 'en:czech-republic', 'languages': ['cs']},
    'Denmark': {'code': 'dk', 'flag': '🇩🇰', 'off_tag': 'en:denmark', 'languages': ['da']},
    'Estonia': {'code': 'ee', 'flag': '🇪🇪', 'off_tag': 'en:estonia', 'languages': ['et']},
    'Finland': {'code': 'fi', 'flag': '🇫🇮', 'off_tag': 'en:finland', 'languages': ['fi', 'sv']},
    'France': {'code': 'fr', 'flag': '🇫🇷', 'off_tag': 'en:france', 'languages': ['fr']},
    'Germany': {'code': 'de', 'flag': '🇩🇪', 'off_tag': 'en:germany', 'languages': ['de']},
    'Greece': {'code': 'el', 'flag': '🇬🇷', 'off_tag': 'en:greece', 'languages': ['el']},
    'Hungary': {'code': 'hu', 'flag': '🇭🇺', 'off_tag': 'en:hungary', 'languages': ['hu']},
    'Ireland': {'code': 'ie', 'flag': '🇮🇪', 'off_tag': 'en:ireland', 'languages': ['en', 'ga']},
    'Italy': {'code': 'it', 'flag': '🇮🇹', 'off_tag': 'en:italy', 'languages': ['it']},
    'Latvia': {'code': 'lv', 'flag': '🇱🇻', 'off_tag': 'en:latvia', 'languages': ['lv']},
    'Lithuania': {'code': 'lt', 'flag': '🇱🇹', 'off_tag': 'en:lithuania', 'languages': ['lt']},
    'Luxembourg': {'code': 'lu', 'flag': '🇱🇺', 'off_tag': 'en:luxembourg', 'languages': ['fr', 'de', 'lb']},
    'Malta': {'code': 'mt', 'flag': '🇲🇹', 'off_tag': 'en:malta', 'languages': ['mt', 'en']},
    'Montenegro': {'code': 'me', 'flag': '🇲🇪', 'off_tag': 'en:montenegro', 'languages': ['sr', 'hr']},
    'Netherlands': {'code': 'nl', 'flag': '🇳🇱', 'off_tag': 'en:netherlands', 'languages': ['nl']},
    'Norway': {'code': 'no', 'flag': '🇳🇴', 'off_tag': 'en:norway', 'languages': ['nb', 'no']},
    'Poland': {'code': 'pl', 'flag': '🇵🇱', 'off_tag': 'en:poland', 'languages': ['pl']},
    'Portugal': {'code': 'pt', 'flag': '🇵🇹', 'off_tag': 'en:portugal', 'languages': ['pt']},
    'Romania': {'code': 'ro', 'flag': '🇷🇴', 'off_tag': 'en:romania', 'languages': ['ro']},
    'Serbia': {'code': 'rs', 'flag': '🇷🇸', 'off_tag': 'en:serbia', 'languages': ['sr']},
    'Slovakia': {'code': 'sk', 'flag': '🇸🇰', 'off_tag': 'en:slovakia', 'languages': ['sk']},
    'Slovenia': {'code': 'si', 'flag': '🇸🇮', 'off_tag': 'en:slovenia', 'languages': ['sl']},
    'Spain': {'code': 'es', 'flag': '🇪🇸', 'off_tag': 'en:spain', 'languages': ['es', 'ca', 'gl', 'eu']},
    'Sweden': {'code': 'se', 'flag': '🇸🇪', 'off_tag': 'en:sweden', 'languages': ['sv']},
    'Switzerland': {'code': 'ch', 'flag': '🇨🇭', 'off_tag': 'en:switzerland', 'languages': ['de', 'fr', 'it']},
    'United Kingdom': {'code': 'uk', 'flag': '🇬🇧', 'off_tag': 'en:united-kingdom', 'languages': ['en']},
}


def load_source_csv():
    path = CSV_PATH if os.path.exists(CSV_PATH) else SCRATCH_CSV
    if not os.path.exists(path):
        raise FileNotFoundError(f"Source CSV not found at {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def clean_category_name(cat_tag):
    if cat_tag.startswith('en:'):
        cat_tag = cat_tag[3:]
    return cat_tag.replace('-', ' ').capitalize()


def build_country_datasets(rows):
    by_country = defaultdict(list)
    for r in rows:
        country = r.get('Country', '').strip()
        if country:
            by_country[country].append(r)

    stats = {
        'campaign_id': 'photos_for_impact_2026',
        'baseline_date': '2026-09-18',
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_countries': len(by_country),
        'total_items': len(rows),
        'total_with_code': sum(1 for r in rows if r.get('code', '').strip()),
        'total_missing': sum(1 for r in rows if not r.get('code', '').strip()),
        'overall_coverage_pct': round((sum(1 for r in rows if r.get('code', '').strip()) / len(rows)) * 100, 1),
        'countries': {}
    }

    country_full_data = {}

    for country, c_rows in sorted(by_country.items()):
        total = len(c_rows)
        with_code = [r for r in c_rows if r.get('code', '').strip()]
        no_code = [r for r in c_rows if not r.get('code', '').strip()]
        coverage_pct = round((len(with_code) / total) * 100, 1) if total > 0 else 0

        meta = COUNTRY_METADATA.get(country, {
            'code': c_rows[0].get('country code', '').lower(),
            'flag': '🌍',
            'off_tag': c_rows[0].get('off_country_id', f'en:{country.lower()}'),
            'languages': ['en']
        })

        stats['countries'][meta['code']] = {
            'name': country,
            'code': meta['code'],
            'flag': meta['flag'],
            'off_tag': meta['off_tag'],
            'languages': meta['languages'],
            'total': total,
            'with_code': len(with_code),
            'missing': len(no_code),
            'coverage_pct': coverage_pct,
            'start_baseline_pct': coverage_pct,
            'delta_pct': 0.0
        }

        country_items = []
        for r in c_rows:
            code = r.get('code', '').strip()
            cat_tag = r.get('Category', '').strip()
            item = {
                'category_tag': cat_tag,
                'category_name': clean_category_name(cat_tag),
                'code': code,
                'has_code': bool(code),
                'status': 'In database' if code else 'Needs photo / barcode',
                'off_url': f"https://world.openfoodfacts.org/product/{code}" if code else "",
                'hunger_games_url': f"https://hunger.openfoodfacts.org/questions?value_tag={cat_tag}&type=category&country={meta['off_tag']}&sorted=true",
                'needed_recipe': r.get('Is_needed_a_recipe ? Mano', '').strip()
            }
            country_items.append(item)

        country_full_data[meta['code']] = {
            'metadata': stats['countries'][meta['code']],
            'categories': country_items
        }

    return stats, country_full_data


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if os.path.exists(SCRATCH_CSV) and not os.path.exists(CSV_PATH):
        with open(SCRATCH_CSV, 'r', encoding='utf-8') as src, open(CSV_PATH, 'w', encoding='utf-8') as dst:
            dst.write(src.read())

    rows = load_source_csv()
    stats, country_data = build_country_datasets(rows)

    if not os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print(f"Created initial campaign baseline at {BASELINE_FILE}")

    with open(BASELINE_FILE, 'r', encoding='utf-8') as f:
        baseline = json.load(f)

    for code, c_stat in stats['countries'].items():
        base_c = baseline.get('countries', {}).get(code, {})
        base_pct = base_c.get('coverage_pct', c_stat['coverage_pct'])
        c_stat['start_baseline_pct'] = base_pct
        c_stat['delta_pct'] = round(c_stat['coverage_pct'] - base_pct, 1)

    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"Updated {STATS_FILE} with current metrics.")

    with open(COUNTRIES_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(country_data, f, indent=2, ensure_ascii=False)
    print(f"Saved country datasets to {COUNTRIES_DATA_FILE}")

    os.makedirs(os.path.join(BASE_DIR, 'release-website', 'photos-for-impact'), exist_ok=True)
    js_dest = os.path.join(BASE_DIR, 'release-website', 'photos-for-impact', 'data.js')
    with open(js_dest, 'w', encoding='utf-8') as f:
        f.write("window.CAMPAIGN_STATS = " + json.dumps(stats, indent=2, ensure_ascii=False) + ";\n")
        f.write("window.COUNTRIES_DATA = " + json.dumps(country_data, indent=2, ensure_ascii=False) + ";\n")
    print(f"Exported data.js to {js_dest}")


if __name__ == '__main__':
    main()
