from spiders import WikipediaSpider, BrainQuotes


def crawler_wikipedia():
    url = 'https://en.wikipedia.org/wiki/Galileo_Galilei'
    return WikipediaSpider.run(url)


def crawler_quotes():
    url = "https://www.brainyquote.com/search_results?x=0&y=0&q=Galileo+Galilei"
    return BrainQuotes.run(url)


def crawler():
    data = {}
    wiki_data = crawler_wikipedia()
    data.update(wiki_data)
    quotes_data = crawler_quotes()
    data.update(quotes_data)
    return data
