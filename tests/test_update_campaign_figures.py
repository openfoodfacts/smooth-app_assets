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
    parse_amount,
    plan_update,
    scrape_figures,
    validate_figures,
)

PAGE = '''
<div class="campaign">
  <p class="bold" id="total-raised">44.155,91 €</p>
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

        expect_error(
            'a file that does not exist',
            plan_update,
            str(pathlib.Path(directory) / 'absent.json'),
            figures,
        )


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
