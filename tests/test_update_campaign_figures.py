#!/usr/bin/env python3
"""
Check that the campaign figure updater refuses bad input instead of publishing it.

The point of these checks is the failure paths, not the happy one: the updater
runs unattended on a schedule against a page nobody here controls, so what
matters is that a changed page, a localised number or an implausible figure
leaves the tagline files exactly as they were.

Run with: python tests/test_update_campaign_figures.py
"""

import io
import json
import os
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from tools.update_campaign_figures import (  # noqa: E402
    FigureError,
    NEWS_ID,
    NEWS_IDS,
    REPO_ROOT,
    TAGLINE_FILES,
    apply_updates,
    campaign_is_published,
    parse_amount,
    plan_update,
    previous_published,
    previous_raised,
    publish,
    scrape_figures,
    scrape_page_percent,
    validate_figures,
)

# Shaped like the real block: three bold paragraphs, only one of them the goal,
# and the drawn width floored to 25 the way Donorbox floors it against 25.97%.
PAGE = '''
<style> .progress .meter { width: 25%; } </style>
<div class="campaign">
  <p class="bold" id="total-raised">44.155,91 €</p>
  <p id="paid-count" class="bold">517</p>
  <p class="bold">170.000 €</p>
</div>
'''


def a_tagline_file(directory, name, raised=None):
    """Write a minimal tagline file and return its path."""
    item = {'url': 'https://example.org'}
    if raised is not None:
        item['raised'] = raised
    path = pathlib.Path(directory) / name
    path.write_text(json.dumps({'news': {NEWS_ID: item}}), encoding='utf-8')
    return str(path)


def expect_error(description, function, *arguments):
    try:
        function(*arguments)
    except FigureError:
        return
    raise AssertionError(f'{description} should have raised FigureError')


def test_scrapes_the_page():
    figures = scrape_figures(PAGE)
    assert figures == {'currency': 'EUR', 'count': 517, 'goal': 170000.0, 'raised': 44155.91}, figures


def test_reads_both_separator_conventions():
    assert parse_amount('44.155,91 €') == 44155.91
    assert parse_amount('$44,155.91') == 44155.91
    assert parse_amount('170.000 €') == 170000.0
    assert parse_amount('£170,000') == 170000.0
    # One separator, three digits after it, is thousands and not a fraction.
    assert parse_amount('1.500') == 1500.0


def test_refuses_a_page_it_cannot_read():
    expect_error('markup without #total-raised', scrape_figures, '<p>nothing here</p>')
    expect_error(
        'a raised figure with no goal beside it',
        scrape_figures,
        '<p class="bold" id="total-raised">44.155,91 €</p>',
    )
    expect_error('a currency we do not know', scrape_figures, PAGE.replace('€', '¤'))
    expect_error('text with no digits at all', parse_amount, 'soon')
    expect_error('markup without #paid-count', scrape_figures,
                 PAGE.replace('id="paid-count"', ''))
    expect_error('a count with no digits', scrape_figures,
                 PAGE.replace('>517<', '>soon<'))


def test_strips_separators_from_the_count():
    assert scrape_figures(PAGE.replace('>517<', '>1.517<'))['count'] == 1517


def test_refuses_an_implausible_count():
    figures = {'raised': 44155.91, 'goal': 170000.0, 'currency': 'EUR', 'count': 0}
    expect_error('a zero count', validate_figures, figures)
    # A donor-goal display like "517 / 1.000" would concatenate into 5171000.
    figures['count'] = scrape_figures(PAGE.replace('>517<', '>517 / 1.000<'))['count']
    expect_error('more gifts than units raised', validate_figures, figures)
    figures['count'] = 400
    expect_error('a count that collapses', validate_figures, figures, None, None, 517)
    # Refunds happen; a small drop goes through.
    figures['count'] = 510
    validate_figures(figures, None, None, 517)


def test_reads_the_percentage_the_page_draws():
    assert scrape_page_percent(PAGE) == 25.0


def test_refuses_a_page_that_draws_no_progress_bar():
    # Failing closed matters here: this number exists to catch a page whose
    # markup moved, so a missing bar is the case it is for, not an excuse.
    expect_error('a page with no meter', scrape_page_percent, '<p>no bar here</p>')


def test_refuses_figures_the_page_itself_contradicts():
    # Two numbers in one text node concatenate into a plausible-looking goal,
    # and only the page's own percentage catches it.
    expect_error(
        'a goal that disagrees with the drawn percentage',
        validate_figures,
        {'raised': 44155.91, 'goal': 26170000.0, 'currency': 'EUR', 'count': 517},
        None,
        25.0,
    )
    # The real figures agree with it, inside the tolerance Donorbox's flooring
    # already eats about half of: 25.97 computed against a drawn 25.
    validate_figures({'raised': 44155.91, 'goal': 170000.0, 'currency': 'EUR', 'count': 517}, None, 25.0)


def test_reads_a_clamped_meter_as_the_goal_being_reached():
    # An over-funded campaign draws 100% whatever the real ratio, so the bar
    # states no ratio and must not refuse a legitimate figure.
    validate_figures({'raised': 200000.0, 'goal': 170000.0, 'currency': 'EUR', 'count': 517}, None, 100.0)

    # It does still say the goal was reached. Skipping the check outright here
    # would wave through a misparsed goal at the one moment nothing else can
    # catch one, since `raised > goal * 3` only guards a misparsed raised.
    expect_error(
        'a full meter under a goal we never reached',
        validate_figures,
        {'raised': 175000.0, 'goal': 26170000.0, 'currency': 'EUR', 'count': 517},
        174000.0,
        100.0,
    )

    # A hair short of the goal is within the same tolerance the other branch
    # gets, in case the page ever rounds the width up instead of flooring it.
    validate_figures({'raised': 169500.0, 'goal': 170000.0, 'currency': 'EUR', 'count': 517}, None, 100.0)


def test_refuses_implausible_figures():
    expect_error(
        'a raised far above the goal',
        validate_figures,
        {'raised': 900000.0, 'goal': 170000.0, 'currency': 'EUR', 'count': 517},
    )
    expect_error(
        'a zero goal',
        validate_figures,
        {'raised': 100.0, 'goal': 0.0, 'currency': 'EUR', 'count': 517},
    )
    # A total that collapses is a bad parse, not a day of refunds.
    expect_error(
        'a raised that dropped by more than 10%',
        validate_figures,
        {'raised': 30000.0, 'goal': 170000.0, 'currency': 'EUR', 'count': 517},
        44155.91,
    )
    # Raising more than the whole goal in one run is a misparse, not a good day.
    # The app renders the unclamped percentage, so this would read "294%".
    expect_error(
        'a raised that jumped by more than the goal',
        validate_figures,
        {'raised': 500000.0, 'goal': 170000.0, 'currency': 'EUR', 'count': 517},
        44155.91,
    )
    # A small drop is plausible and must still go through.
    validate_figures({'raised': 43000.0, 'goal': 170000.0, 'currency': 'EUR', 'count': 517}, 44155.91)
    # So must a long gap between runs. Bounding the rise by a multiple of the
    # last published figure would refuse this and then never recover, because a
    # refusal writes nothing and the figure it compares against never moves.
    validate_figures({'raised': 140000.0, 'goal': 170000.0, 'currency': 'EUR', 'count': 517}, 44155.91)


def test_planning_writes_nothing():
    figures = {'currency': 'EUR', 'count': 517, 'goal': 170000.0, 'raised': 44155.91}
    with tempfile.TemporaryDirectory() as directory:
        path = pathlib.Path(directory) / 'main.json'
        original = json.dumps({'news': {NEWS_ID: {'url': 'https://example.org'}}})
        path.write_text(original, encoding='utf-8')

        content = plan_update(str(path), figures)

        assert content is not None
        assert json.loads(content)['news'][NEWS_ID]['raised'] == 44155.91
        # The file itself is untouched until every file has been planned.
        assert path.read_text(encoding='utf-8') == original


def test_planning_updates_every_donation_item_the_file_has():
    figures = {'currency': 'EUR', 'goal': 170000.0, 'raised': 44155.91, 'count': 517}
    with tempfile.TemporaryDirectory() as directory:
        path = pathlib.Path(directory) / 'web.json'
        path.write_text(json.dumps({'news': {
            'other_news': {'url': 'https://example.org'},
            NEWS_IDS[0]: {'url': 'https://example.org'},
            NEWS_IDS[1]: {'url': 'https://example.org'},
        }}), encoding='utf-8')

        news = json.loads(plan_update(str(path), figures))['news']

        assert news[NEWS_IDS[0]]['count'] == 517
        assert news[NEWS_IDS[1]]['count'] == 517
        # An item the file does not carry is not invented, and an unrelated
        # item is not touched.
        assert NEWS_IDS[2] not in news
        assert news['other_news'] == {'url': 'https://example.org'}


def test_planning_reports_a_file_it_cannot_use():
    figures = {'currency': 'EUR', 'count': 517, 'goal': 170000.0, 'raised': 44155.91}
    with tempfile.TemporaryDirectory() as directory:
        # A file with no donation item is skipped, not refused: the campaign
        # item is retired from all three files while the web banner items stay.
        missing_item = pathlib.Path(directory) / 'no-item.json'
        missing_item.write_text('{"news": {}}', encoding='utf-8')
        assert plan_update(str(missing_item), figures) is None

        broken = pathlib.Path(directory) / 'broken.json'
        broken.write_text('{not json', encoding='utf-8')
        expect_error('a file that is not JSON', plan_update, str(broken), figures)

        # Valid JSON, but not the shape we index into. The last one is the news
        # item itself being a scalar, which reaches the update rather than the
        # lookup, so it fails differently.
        for name, content in (('list.json', '[]'), ('scalar.json', '5'),
                              ('news-list.json', '{"news": []}'),
                              ('item.json', '{"news": {"%s": 5}}' % NEWS_ID)):
            wrong_shape = pathlib.Path(directory) / name
            wrong_shape.write_text(content, encoding='utf-8')
            expect_error(f'{content} at the top level', plan_update,
                         str(wrong_shape), figures)

        expect_error(
            'a file that does not exist',
            plan_update,
            str(pathlib.Path(directory) / 'absent.json'),
            figures,
        )


def test_a_bad_third_file_leaves_the_first_two_untouched():
    """The behaviour the maintainer asked about, through the real write path.

    This calls `publish`, which is all `main` does, so writing each file as it
    is planned would fail here instead of passing quietly.
    """
    figures = {'currency': 'EUR', 'count': 517, 'goal': 170000.0, 'raised': 44155.91}

    with tempfile.TemporaryDirectory() as directory:
        paths = [a_tagline_file(directory, name)
                 for name in ('android.json', 'ios.json')]
        before = [pathlib.Path(path).read_text(encoding='utf-8') for path in paths]

        broken = pathlib.Path(directory) / 'web.json'
        broken.write_text('{not json', encoding='utf-8')
        paths.append(str(broken))

        expect_error('a broken third file', publish, figures, paths)

        for path, original in zip(paths, before):
            assert pathlib.Path(path).read_text(encoding='utf-8') == original, path


def test_takes_the_highest_previously_published_figure():
    with tempfile.TemporaryDirectory() as directory:
        paths = [
            a_tagline_file(directory, 'android.json', raised=100.0),
            a_tagline_file(directory, 'ios.json', raised=44155.91),
            a_tagline_file(directory, 'web.json', raised=44155.91),
        ]
        # The first file has drifted. Comparing against it would let the other
        # two be halved without the drop guard noticing.
        assert previous_raised(paths) == 44155.91


def test_takes_the_highest_count_across_items():
    with tempfile.TemporaryDirectory() as directory:
        path = pathlib.Path(directory) / 'web.json'
        path.write_text(json.dumps({'news': {
            NEWS_IDS[0]: {'count': 517},
            NEWS_IDS[2]: {'count': 600},
            NEWS_IDS[1]: {'count': 'soon'},
        }}), encoding='utf-8')
        assert previous_published('count', [str(path)]) == 600


def test_says_so_when_there_is_no_baseline():
    with tempfile.TemporaryDirectory() as directory:
        path = a_tagline_file(directory, 'android.json')

        stderr, sys.stderr = sys.stderr, io.StringIO()
        try:
            assert previous_raised([path]) is None
            reported = sys.stderr.getvalue()
        finally:
            sys.stderr = stderr

        # Silence here would disable the only historical guard with no trace.
        assert 'no previously published raised' in reported, reported


def test_knows_when_the_campaign_is_over_and_when_it_cannot_tell():
    with tempfile.TemporaryDirectory() as directory:
        present = a_tagline_file(directory, 'android.json')
        assert campaign_is_published([present]) is True

        gone = pathlib.Path(directory) / 'empty.json'
        gone.write_text('{"news": {}}', encoding='utf-8')
        assert campaign_is_published([str(gone)]) is False

        # The banner items outlive the campaign item and still need figures.
        banner_only = pathlib.Path(directory) / 'web.json'
        banner_only.write_text(json.dumps({'news': {NEWS_IDS[2]: {}}}), encoding='utf-8')
        assert campaign_is_published([str(gone), str(banner_only)]) is True

        # An unreadable file is not evidence that the campaign ended, so it
        # must not be reported as "nothing to update" and exit 0.
        broken = pathlib.Path(directory) / 'broken.json'
        broken.write_text('{not json', encoding='utf-8')
        expect_error('an unreadable file', campaign_is_published, [str(broken)])

        wrong_shape = pathlib.Path(directory) / 'shape.json'
        wrong_shape.write_text('{"news": 5}', encoding='utf-8')
        expect_error('a non container news field', campaign_is_published,
                     [str(wrong_shape)])


def test_resolves_relative_paths_against_the_repository():
    """A run from any directory has to find the tagline files.

    Asserted by changing directory, since resolving against the caller's cwd is
    exactly the regression this guards, and it would pass from the repo root.
    """
    here = os.getcwd()
    with tempfile.TemporaryDirectory() as elsewhere:
        try:
            os.chdir(elsewhere)
            for path in TAGLINE_FILES:
                assert (REPO_ROOT / path).is_file(), path
        finally:
            os.chdir(here)


def test_dry_run_writes_nothing():
    original = json.dumps({'news': {NEWS_ID: {'url': 'https://example.org'}}})
    with tempfile.TemporaryDirectory() as directory:
        path = pathlib.Path(directory) / 'main.json'
        path.write_text(original, encoding='utf-8')
        plans = {str(path): 'REPLACED'}

        assert apply_updates(plans, dry_run=True) == [str(path)]
        assert path.read_text(encoding='utf-8') == original

        assert apply_updates(plans) == [str(path)]
        assert path.read_text(encoding='utf-8') == 'REPLACED'


def main():
    tests = [value for name, value in sorted(globals().items())
             if name.startswith('test_') and callable(value)]
    for test in tests:
        test()
        print(f'ok  {test.__name__}')
    print(f'{len(tests)} checks passed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
