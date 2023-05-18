import main, crawl


def test_wikipedia_spider():

    data = crawl()
    assert 'heading' in data


def test_main():
    main.main()
