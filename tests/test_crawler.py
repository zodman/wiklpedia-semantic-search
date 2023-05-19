from lib import crawlers


def test_crawler_brainquotes():
    quote = 'My name doest not exists here aleluya'
    crawlers.crawler_quotes(quote)
