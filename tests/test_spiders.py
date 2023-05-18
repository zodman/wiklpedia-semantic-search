import spiders
import pytest


def test_spider_open(mocker):

    drv_mock = mocker.patch('spiders.Spider.drv')
    drv_mock.open_available_browser.return_value = 0

    s = spiders.Spider('url')
    with pytest.raises(spiders.SpiderError):
        s.open()


def test_spider_parse(mocker):

    drv_mock = mocker.patch('spiders.Spider.drv')
    drv_mock.open_available_browser.return_value = 1

    s = spiders.Spider('url')
    s.open()
    with pytest.raises(AssertionError):
        s.parse()


def test_spider_parse_page(mocker):

    drv_mock = mocker.patch('spiders.Spider.drv')
    drv_mock.open_available_browser.return_value = 1
    mocker.patch('spiders.Spider.parse')

    s = spiders.Spider('url')
    s.open()
    s.parse_page()
    s.close()


def test_spider_parse_with_exception(mocker):

    drv_mock = mocker.patch('spiders.Spider.drv')
    drv_mock.open_available_browser.return_value = 1
    mocker.patch('spiders.Spider.parse',
                 side_effect=spiders.SpiderError('mock'))

    s = spiders.Spider('url')
    s.open()
    with pytest.raises(spiders.SpiderError):
        s.parse_page()
    s.close()


def test_spider_run(mocker):
    mocker.patch('spiders.Spider.drv')
    mocker.patch('spiders.Spider.parse')
    spiders.Spider.run('test')


def test_spider_brainquotes(mocker):
    mocker.patch('spiders.Spider.drv')
    mocker.patch('spiders.Spider.drv.find_elements', side_effect=[[]])
    spider = spiders.BrainQuotes('')
    spider.open()
    spider.parse()


def test_spider_wikipedia_summary(mocker):
    drv_mock = mocker.patch('spiders.Spider.drv')
    drv_mock.open_available_browser.return_value = 1

    element = mocker.MagicMock()
    element.text.return_value = 'foobar'
    element2 = mocker.MagicMock()
    element.text.return_value = 'foobar'
    mocker.patch('re.sub', side_effect=['foobar',''])

    mocker.patch('spiders.Spider.drv.find_elements',
                 side_effect=[
                     [element, element2],
                 ])
    spider = spiders.WikipediaScientistSpider('')
    r = spider._get_summary()
    assert r == 'foobar'


def test_spider_wikipedia_bbiography(mocker):
    drv_mock = mocker.patch('spiders.Spider.drv')
    drv_mock.open_available_browser.return_value = 1

    element = mocker.MagicMock()
    element.text.return_value = 'foobar'
    element2 = mocker.MagicMock()
    element.text.return_value = 'foobar'
    mocker.patch('re.sub', side_effect=['foobar',''])

    mocker.patch('spiders.Spider.drv.find_elements',
                 side_effect=[
                     [element, element2],
                 ])
    spider = spiders.WikipediaScientistSpider('')
    r = spider._get_summary()
    assert r == 'foobar'
