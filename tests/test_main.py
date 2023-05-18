import pytest
import crawlers
import utils
import main
import formats


@pytest.mark.parametrize('name', utils.SCIENTISTS)
def test_crawler(name):
    data = crawlers.crawler(name)
    assert 'heading' in data and data['heading'] != ''
    assert 'summary' in data and data['summary'] != ''
    assert 'biography' in data and len(data['biography'].items()) > 0
    assert 'born' in data['biography']
    assert 'died' in data['biography']
    assert 'quotes' in data and len(data['quotes']) > 0


@pytest.mark.parametrize('name', utils.SCIENTISTS)
def test_main_crawl(name):
    data = main.Scientistic.crawl(name)
    assert 'title' in data and data['title'] != ''
    assert 'summary' in data and data['summary'] != ''
    assert 'born_date' in data
    assert 'dead_date' in data
    assert 'quote' in data
    assert formats.to_text([data]) is None
    assert formats.to_json([data]) is None
