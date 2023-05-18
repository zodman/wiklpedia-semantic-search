from spiders import WikipediaSpider, BrainQuotes


def crawler_wikipedia(name):
    name_text = name.replace(" ", "_")
    url = 'https://en.wikipedia.org/wiki/{}'.format(name_text)
    return WikipediaSpider.run(url)


def crawler_quotes(name):
    url = "https://www.brainyquote.com/search_results?x=0&y=0&q={}".format(
        name)
    return BrainQuotes.run(url)


def crawler(name):
    data = {}
    for crawler_func in (crawler_wikipedia, crawler_quotes):
        data_tmp = crawler_func(name)
        data.update(data_tmp)
    return data
