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

# Paths below are resolved against the repository, not the current directory,
# so the script works the same from anywhere. An absolute path passes through.
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

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

# The page draws its own progress bar. Our arithmetic has to agree with it, in
# percentage points, or one of the two numbers we read was not what we thought.
# Donorbox floors its width, so about 1 of these 2 points is its rounding rather
# than slack. Every misparse seen so far lands at least 4 points out.
MAX_PERCENT_DISAGREEMENT = 2.0

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


def scrape_page_percent(html):
    """Return the percentage the page draws in its own progress bar.

    This is the campaign's own arithmetic, so it is the one number on the page
    that can contradict ours.

    Missing it is an error rather than a skipped check. The whole point of this
    number is to catch a run where the markup moved under us, so treating
    "the markup moved" as "check not applicable" would disable it exactly when
    it is needed.
    """
    match = re.search(r'\.meter\s*\{[^}]*width:\s*(?P<value>[\d.]+)%', html)
    if match is None:
        raise FigureError(
            'no progress bar width on the page, so nothing corroborates the '
            'figures we read. The markup changed'
        )
    return float(match.group('value'))


def validate_figures(figures, previous_raised=None, page_percent=None):
    """Refuse anything that would make the meter lie.

    Every refusal leaves the published figures alone, so a run that is wrongly
    refused stays refused until someone corrects the JSON by hand. The bounds
    below are set wide enough that only a misparse should reach them.
    """
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
    if previous_raised is not None:
        if raised < previous_raised * (1 - MAX_PLAUSIBLE_DROP):
            raise FigureError(
                f'raised dropped from {previous_raised} to {raised}, more than '
                f'{MAX_PLAUSIBLE_DROP:.0%}, refusing to publish it'
            )
        # Bounded by the goal rather than by a multiple of the previous figure.
        # A multiple would be self-locking: once it refuses, nothing is written,
        # so the figure it compares against never advances and every later run
        # refuses too. Raising more than the entire goal in one day is the
        # impossible part, and that does not go stale.
        if raised - previous_raised > goal:
            raise FigureError(
                f'raised jumped from {previous_raised} to {raised}, i.e. by '
                f'more than the whole {goal} goal in one run, refusing it'
            )
    if page_percent is not None:
        if page_percent >= 100:
            # Clamped, so it no longer states a ratio. It does still say the
            # goal was reached, and skipping the check outright would let a
            # misparsed goal through exactly when nothing else can catch one.
            # Same tolerance the other branch gets: the evidence that Donorbox
            # floors rather than rounds is one observation, and a wrong refusal
            # here would wedge the run at the campaign's best moment.
            if raised < goal * (1 - MAX_PERCENT_DISAGREEMENT / 100):
                raise FigureError(
                    f'the page draws a full meter, so {raised} should have '
                    f'reached the {goal} goal. One of the two is wrong'
                )
        else:
            computed = raised / goal * 100
            if abs(computed - page_percent) > MAX_PERCENT_DISAGREEMENT:
                raise FigureError(
                    f'we read {raised} of {goal}, i.e. {computed:.1f}%, but the '
                    f'page draws {page_percent:.1f}%. One of the two figures is '
                    'not the one we think it is'
                )


def plan_update(path, figures):
    """Return the new content for `path`, or None when it would not change.

    Nothing is written here: every file is planned before any is written, so a
    file that cannot be read leaves the others untouched rather than half of
    them updated.

    The files are not consistently key sorted as a whole, so the document is
    dumped in its original order and only this one item is sorted, which keeps
    the diff to the lines that actually changed.
    """
    try:
        original = (REPO_ROOT / path).read_text(encoding='utf-8')
        document = json.loads(original)
        item = document['news'][NEWS_ID]
        item.update(figures)
        document['news'][NEWS_ID] = {key: item[key] for key in sorted(item)}
        updated = json.dumps(document, indent=2, ensure_ascii=False) + '\n'
    except (OSError, ValueError, TypeError, AttributeError) as error:
        # Anything but a readable object of the shape we index into.
        raise FigureError(f'could not read {path}: {error}') from error
    except KeyError as error:
        raise FigureError(f'{path} has no news item {NEWS_ID!r}') from error

    return None if updated == original else updated


def plan_all(paths, figures):
    """Plan every file before any of them is written.

    This is the all-or-nothing step: one unreadable file raises before a single
    write has happened, so the others keep the figures they had.
    """
    return {path: plan_update(path, figures) for path in paths}


def previous_raised(paths=TAGLINE_FILES):
    """Highest `raised` already published, across every file we are about to write.

    The highest, not the first: the files can drift apart after a hand edit, and
    the drop guard is only worth having if it compares against the largest
    figure any of them currently shows.
    """
    published = []
    for path in paths:
        try:
            document = json.loads((REPO_ROOT / path).read_text(encoding='utf-8'))
            value = document['news'][NEWS_ID].get('raised')
        except (OSError, ValueError, TypeError, KeyError):
            continue
        if isinstance(value, (int, float)):
            published.append(value)

    if not published:
        print(
            'no previously published figure found, so the plausibility check '
            'against it is skipped for this run',
            file=sys.stderr,
        )
        return None
    return max(published)


def campaign_is_published(paths=TAGLINE_FILES):
    """True while at least one tagline file still carries the campaign item.

    Once the campaign is over the item is removed from the feed and this run has
    nothing left to do, which is a clean exit rather than a failure: a scheduled
    job that goes red every morning forever gets deleted.

    A file we cannot read is not evidence of that, so it raises. Otherwise three
    corrupt files would report "the campaign is over" and exit 0 for good.
    """
    published = False
    for path in paths:
        try:
            document = json.loads((REPO_ROOT / path).read_text(encoding='utf-8'))
            published = published or NEWS_ID in document['news']
        except (OSError, ValueError, TypeError, KeyError) as error:
            raise FigureError(f'could not read {path}: {error}') from error
    return published


def apply_updates(plans, dry_run=False):
    """Write every planned file. Returns the paths that changed."""
    changed = [path for path, content in plans.items() if content is not None]
    if not dry_run:
        for path in changed:
            # newline='' writes the '\n' we built rather than os.linesep, so the
            # bytes are the same whichever platform runs this.
            (REPO_ROOT / path).write_text(
                plans[path], encoding='utf-8', newline=''
            )
    return changed


def publish(figures, paths=TAGLINE_FILES, dry_run=False):
    """Plan every file, then write. Returns the paths that changed.

    This is the whole write path, and `main` does nothing else, so a test can
    drive the real sequencing without a network call. Keep it that way: the
    ordering only holds because planning finishes before writing starts.
    """
    return apply_updates(plan_all(paths, figures), dry_run)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='report the figures without writing the files',
    )
    arguments = parser.parse_args()

    try:
        if not campaign_is_published():
            print(f'no {NEWS_ID} item in the tagline files, nothing to update')
            return 0

        html = fetch_page()
        figures = scrape_figures(html)
        validate_figures(figures, previous_raised(), scrape_page_percent(html))
        print(
            'read {raised:.2f} of {goal:.2f} {currency}'.format(**figures),
            f'({figures["raised"] / figures["goal"]:.1%})',
        )
        changed = publish(figures, TAGLINE_FILES, arguments.dry_run)
    except FigureError as error:
        print(f'campaign figures not updated: {error}', file=sys.stderr)
        return 1

    if not changed:
        print('figures unchanged, nothing to commit')
    else:
        verb = 'would update' if arguments.dry_run else 'updated'
        print(f'{verb}: ' + ', '.join(changed))
    return 0


if __name__ == '__main__':
    sys.exit(main())
