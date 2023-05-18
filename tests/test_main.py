import main


def test_quotes_spider():
    data = main.crawler_quotes()
    assert 'quotes' in data and len(data['quotes']) > 0


def test_wikipedia_spider():
    data = main.crawler_wikipedia()

    assert 'heading' in data and data['heading'] != ''
    assert 'summary' in data and data['summary'] != ''
    assert 'was an Italian astronomer' in data['summary']
    assert 'biography' in data and len(data['biography'].items()) > 0
    assert 'born' in data['biography']
