import pytest
import crawlers
import formats
import constants
import utils
from datetime import date


def test_date_object():
    value = utils.get_date_from_string(
        '"4 January 1643 [O.S. 25 December 1642][a]\n'
        'Woolsthorpe-by-Colsterworth, Lincolnshire, England"')
    assert isinstance(value, date)


@pytest.mark.parametrize('name', [
    "Ferdinand Cohn",
    "William Kirby",
])
def test_crawler_others(name):
    data = crawlers.crawler(name)
    assert 'heading' in data and data['heading'] != ''
    assert 'summary' in data and data['summary'] != ''
    assert 'biography' in data and data['biography'] == {}


@pytest.mark.parametrize('name', constants.SCIENTISTS)
def test_crawler(name):
    data = crawlers.crawler(name)
    assert 'heading' in data and data['heading'] != ''
    assert 'summary' in data and data['summary'] != ''
    assert 'biography' in data and len(data['biography'].items()) > 0
    assert 'born' in data['biography']
    assert 'died' in data['biography']
    assert 'quotes' in data and len(data['quotes']) > 0


@pytest.mark.parametrize('name', constants.SCIENTISTS)
def test_main_crawl(name):
    data = crawlers.Scientistic.crawl(name)
    assert 'title' in data and data['title'] != ''
    assert 'summary' in data and data['summary'] != ''
    assert 'born_date' in data
    assert 'dead_date' in data
    assert 'quote' in data
    assert formats.to_text([data]) is None
    assert formats.to_json([data]) is None
