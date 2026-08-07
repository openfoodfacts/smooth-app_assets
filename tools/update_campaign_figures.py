#!/usr/bin/env python3
"""Publish the live donation campaign figures into the tagline JSON files.

The Donorbox API needs a paid plan, but the campaign page renders the figures
server side, so they can be read straight out of the HTML. This writes three
optional fields onto the campaign's news item:

    "currency": "EUR"      ISO code, derived from the symbol on the page
    "goal": 170000.0       campaign goal
    "raised": 44155.91     raised so far

Apps that do not know these fields ignore them, and the smooth-app card falls
back to its previous look when any of them is missing, so publishing them is
safe for every already-installed version.

Nothing is written unless every figure parses and passes the sanity checks in
`validate_figures`. A stale number is acceptable; a wrong one is not.

Usage:
    python tools/update_campaign_figures.py            # fetch and update
    python tools/update_campaign_figures.py --dry-run  # report, change nothing
"""

import argparse
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

CAMPAIGN_URL = 'https://donorbox.org/help-open-food-facts-stay-afloat'
NEWS_ID = 'donation_campaign_2026'
TAGLINE_FILES = (
    'prod/tagline/android/main.json',
    'prod/tagline/ios/main.json',
    'prod/tagline/web/main.json',
)

# Donorbox prints a symbol, the app needs an ISO code for its currency format.
CURRENCY_BY_SYMBOL = {'€': 'EUR', '$': 'USD', '£': 'GBP'}

# A parse that silently goes wrong is worse than yesterday's number, so a drop
# larger than this is treated as a bad read rather than as refunds.
MAX_PLAUSIBLE_DROP = 0.10

USER_AGENT = (
    'openfoodfacts-smooth-app_assets campaign figure updater '
    '(+https://github.com/openfoodfacts/smooth-app_assets)'
)


class FigureError(Exception):
    """Raised when the page cannot be read into figures worth publishing."""


def fetch_page(url=CAMPAIGN_URL):
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode('utf-8', errors='replace')
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as error:
        raise FigureError(f'could not fetch {url}: {error}') from error


def parse_amount(text):
    """Read '44.155,91 €' or '€44,155.91' into a float.

    Donorbox localises the separators, so the decimal separator is whichever of
    '.' and ',' comes last. With only one separator present, treat it as decimal
    only when exactly two digits follow it.
    """
    digits = re.sub(r'[^\d.,]', '', text)
    if not digits:
        raise FigureError(f'no number in {text!r}')

    if ',' in digits and '.' in digits:
        decimal = ',' if digits.rfind(',') > digits.rfind('.') else '.'
        thousands = '.' if decimal == ',' else ','
        digits = digits.replace(thousands, '').replace(decimal, '.')
    elif ',' in digits:
        digits = digits.replace(',', '.' if re.search(r',\d{2}$', digits) else '')
    elif re.search(r'\.\d{3}$', digits):
        # '170.000' is thousands, not a fractional part.
        digits = digits.replace('.', '')

    try:
        return float(digits)
    except ValueError as error:
        raise FigureError(f'could not read a number from {text!r}') from error


def parse_currency(text):
    for symbol, code in CURRENCY_BY_SYMBOL.items():
        if symbol in text:
            return code
    raise FigureError(f'no known currency symbol in {text!r}')


def scrape_figures(html):
    """Pull raised, goal and currency out of the campaign page.

    `total-raised` carries an id. The goal does not: it is the one bold
    paragraph in the same block without an id, so it is matched structurally.
    """
    raised_match = re.search(
        r'id="total-raised"[^>]*>(?P<value>[^<]+)<', html
    )
    if raised_match is None:
        raise FigureError('no #total-raised on the page, the markup changed')
    raised_text = raised_match.group('value').strip()

    bold = re.findall(r'<p(?P<attrs>[^>]*class="bold"[^>]*)>(?P<value>[^<]+)<', html)
    goal_text = next(
        (
            value.strip()
            for attrs, value in bold
            if 'id=' not in attrs
            and any(symbol in value for symbol in CURRENCY_BY_SYMBOL)
        ),
        None,
    )
    if goal_text is None:
        raise FigureError('no goal figure on the page, the markup changed')

    return {
        'currency': parse_currency(raised_text),
        'goal': parse_amount(goal_text),
        'raised': parse_amount(raised_text),
    }


def validate_figures(figures, previous_raised=None):
    """Refuse anything that would make the meter lie."""
    raised, goal = figures['raised'], figures['goal']

    if raised <= 0:
        raise FigureError(f'raised must be positive, got {raised}')
    if goal <= 0:
        raise FigureError(f'goal must be positive, got {goal}')
    if raised > goal * 3:
        raise FigureError(
            f'raised {raised} is more than three times the goal {goal}, '
            'that is a bad parse rather than a very good week'
        )
    if previous_raised is not None and raised < previous_raised * (1 - MAX_PLAUSIBLE_DROP):
        raise FigureError(
            f'raised dropped from {previous_raised} to {raised}, more than '
            f'{MAX_PLAUSIBLE_DROP:.0%}, refusing to publish it'
        )


def plan_update(path, figures):
    """Return the new content for [path], or None when it would not change.

    Nothing is written here: every file is planned before any is written, so a
    file that cannot be read leaves the others untouched rather than half of
    them updated.

    The files are not consistently key sorted as a whole, so the document is
    dumped in its original order and only this one item is sorted, which keeps
    the diff to the lines that actually changed.
    """
    try:
        original = pathlib.Path(path).read_text(encoding='utf-8')
        document = json.loads(original)
        item = document['news'][NEWS_ID]
    except (OSError, ValueError) as error:
        raise FigureError(f'could not read {path}: {error}') from error
    except KeyError as error:
        raise FigureError(f'{path} has no news item {NEWS_ID!r}') from error

    item.update(figures)
    document['news'][NEWS_ID] = {key: item[key] for key in sorted(item)}

    updated = json.dumps(document, indent=2, ensure_ascii=False) + '\n'
    return None if updated == original else updated


def previous_raised(path=TAGLINE_FILES[0]):
    try:
        document = json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
        return document['news'][NEWS_ID].get('raised')
    except (OSError, ValueError, KeyError):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='report the figures without writing the files',
    )
    arguments = parser.parse_args()

    try:
        figures = scrape_figures(fetch_page())
        validate_figures(figures, previous_raised())
        plans = {path: plan_update(path, figures) for path in TAGLINE_FILES}
    except FigureError as error:
        print(f'campaign figures not updated: {error}', file=sys.stderr)
        return 1

    print(
        'read {raised:.2f} of {goal:.2f} {currency}'.format(**figures),
        f'({figures["raised"] / figures["goal"]:.1%})',
    )

    changed = [path for path, content in plans.items() if content is not None]
    if not arguments.dry_run:
        for path in changed:
            pathlib.Path(path).write_text(plans[path], encoding='utf-8')

    if not changed:
        print('figures unchanged, nothing to commit')
    else:
        verb = 'would update' if arguments.dry_run else 'updated'
        print(f'{verb}: ' + ', '.join(changed))
    return 0


if __name__ == '__main__':
    sys.exit(main())
