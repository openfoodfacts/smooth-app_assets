#!/usr/bin/env python3
"""
Check that the campaign figure updater refuses bad input instead of publishing it.

The point of these checks is the failure paths, not the happy one: the updater
runs unattended on a schedule against a page nobody here controls, so what
matters is that a changed page, a localised number or an implausible figure
leaves the tagline files exactly as they were.

Run with: python tests/test_update_campaign_figures.py
"""

import json
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from tools.update_campaign_figures import (  # noqa: E402
    FigureError,
    NEWS_ID,
    apply_updates,
    parse_amount,
    plan_update,
    scrape_figures,
    scrape_page_percent,
    validate_figures,
)

# Shaped like the real block: three bold paragraphs, only one of them the goal.
PAGE = '''
<style> .progress .meter { width: 26%; } </style>
<div class="campaign">
  <p class="bold" id="total-raised">44.155,91 €</p>
  <p id="paid-count" class="bold">517</p>
  <p class="bold">170.000 €</p>
</div>
'''


def expect_error(description, function, *arguments):
    try:
        function(*arguments)
    except FigureError:
        return
    raise AssertionError(f'{description} should have raised FigureError')


def test_scrapes_the_page():
    figures = scrape_figures(PAGE)
    assert figures == {'currency': 'EUR', 'goal': 170000.0, 'raised': 44155.91}, figures


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


def test_reads_the_percentage_the_page_draws():
    assert scrape_page_percent(PAGE) == 26.0
    assert scrape_page_percent('<p>no bar here</p>') is None


def test_refuses_figures_the_page_itself_contradicts():
    # Two numbers in one text node concatenate into a plausible-looking goal,
    # and only the page's own percentage catches it.
    expect_error(
        'a goal that disagrees with the drawn percentage',
        validate_figures,
        {'raised': 44155.91, 'goal': 26170000.0, 'currency': 'EUR'},
        None,
        26.0,
    )
    # The real figures agree with it, to well inside the tolerance.
    validate_figures({'raised': 44155.91, 'goal': 170000.0, 'currency': 'EUR'}, None, 26.0)


def test_refuses_implausible_figures():
    expect_error(
        'a raised far above the goal',
        validate_figures,
        {'raised': 900000.0, 'goal': 170000.0, 'currency': 'EUR'},
    )
    expect_error(
        'a zero goal',
        validate_figures,
        {'raised': 100.0, 'goal': 0.0, 'currency': 'EUR'},
    )
    # A total that collapses is a bad parse, not a day of refunds.
    expect_error(
        'a raised that dropped by more than 10%',
        validate_figures,
        {'raised': 30000.0, 'goal': 170000.0, 'currency': 'EUR'},
        44155.91,
    )
    # A total that multiplies overnight is a misparse, not a good day. The app
    # renders the unclamped percentage, so this would read "294%" on the card.
    expect_error(
        'a raised that jumped past 3x',
        validate_figures,
        {'raised': 500000.0, 'goal': 170000.0, 'currency': 'EUR'},
        44155.91,
    )
    # A small drop is plausible and must still go through.
    validate_figures({'raised': 43000.0, 'goal': 170000.0, 'currency': 'EUR'}, 44155.91)


def test_planning_writes_nothing():
    figures = {'currency': 'EUR', 'goal': 170000.0, 'raised': 44155.91}
    with tempfile.TemporaryDirectory() as directory:
        path = pathlib.Path(directory) / 'main.json'
        original = json.dumps({'news': {NEWS_ID: {'url': 'https://example.org'}}})
        path.write_text(original, encoding='utf-8')

        content = plan_update(str(path), figures)

        assert content is not None
        assert json.loads(content)['news'][NEWS_ID]['raised'] == 44155.91
        # The file itself is untouched until every file has been planned.
        assert path.read_text(encoding='utf-8') == original


def test_planning_reports_a_file_it_cannot_use():
    figures = {'currency': 'EUR', 'goal': 170000.0, 'raised': 44155.91}
    with tempfile.TemporaryDirectory() as directory:
        missing_item = pathlib.Path(directory) / 'no-item.json'
        missing_item.write_text('{"news": {}}', encoding='utf-8')
        expect_error('a file without the news item', plan_update, str(missing_item), figures)

        broken = pathlib.Path(directory) / 'broken.json'
        broken.write_text('{not json', encoding='utf-8')
        expect_error('a file that is not JSON', plan_update, str(broken), figures)

        # Valid JSON, but not the shape we index into.
        for name, content in (('list.json', '[]'), ('scalar.json', '5'),
                              ('news-list.json', '{"news": []}')):
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
    """The behaviour the maintainer asked about, end to end.

    Planning all three before writing any is what makes this pass. Writing each
    file as it is planned would leave the first two already changed.
    """
    figures = {'currency': 'EUR', 'goal': 170000.0, 'raised': 44155.91}
    good = json.dumps({'news': {NEWS_ID: {'url': 'https://example.org'}}})

    with tempfile.TemporaryDirectory() as directory:
        paths = []
        for name in ('android.json', 'ios.json'):
            path = pathlib.Path(directory) / name
            path.write_text(good, encoding='utf-8')
            paths.append(str(path))
        broken = pathlib.Path(directory) / 'web.json'
        broken.write_text('{not json', encoding='utf-8')
        paths.append(str(broken))

        try:
            {path: plan_update(path, figures) for path in paths}
        except FigureError:
            pass
        else:
            raise AssertionError('the broken third file should have been refused')

        for path in paths[:2]:
            assert pathlib.Path(path).read_text(encoding='utf-8') == good, path


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
