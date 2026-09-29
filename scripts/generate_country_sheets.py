#!/usr/bin/env python3
"""
Generate per-country CSV datasets and summary reports from the master representative products CSV.
"""

import csv
import os
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'representative_products.csv')
OUT_DIR = os.path.join(BASE_DIR, 'data', 'countries_csv')


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Missing master CSV: {CSV_PATH}")

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    by_country = defaultdict(list)
    for r in rows:
        country = r.get('Country', '').strip()
        if country:
            by_country[country].append(r)

    print(f"Loaded {len(rows)} rows across {len(by_country)} countries.")
    for country, c_rows in sorted(by_country.items()):
        filename = os.path.join(OUT_DIR, f"{country.replace(' ', '_')}.csv")
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=c_rows[0].keys())
            writer.writeheader()
            writer.writerows(c_rows)
        with_code = sum(1 for r in c_rows if r.get('code', '').strip())
        print(f"  {country}: {len(c_rows)} items ({with_code} with barcode, {len(c_rows) - with_code} missing) -> {filename}")

    print(f"\nSuccessfully generated {len(by_country)} country CSV files in {OUT_DIR}")


if __name__ == '__main__':
    main()
