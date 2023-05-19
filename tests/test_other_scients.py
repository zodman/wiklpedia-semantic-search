import pytest
from lib import crawlers
from lib import formats


@pytest.mark.parametrize('name', ['Euclid', 'Alan Turing'])
def test_others(name):
    data = crawlers.Scientist.crawl(name)
    assert 'title' in data and data['title'] != ''
    assert 'summary' in data and data['summary'] != ''
    assert 'born_date' in data
    assert 'dead_date' in data
    assert 'quote' in data
    assert formats.to_text([data]) is None
    assert formats.to_json([data]) is None
