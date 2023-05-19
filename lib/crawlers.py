from lib.spiders import WikipediaScientistSpider, BrainQuotes
import textwrap
import random
import re
from lib import utils


def crawler_wikipedia(name):
    name_text = name.replace(" ", "_")
    url = 'https://en.wikipedia.org/wiki/{}'.format(name_text)
    return WikipediaScientistSpider.run(url)


def crawler_quotes(name):
    url = "https://www.brainyquote.com/search_results?x=0&y=0&q={}".format(
        name)
    return BrainQuotes.run(url)


def run_crawlers(name):
    data = {}
    for crawler_func in (crawler_wikipedia, crawler_quotes):
        data_tmp = crawler_func(name)
        data.update(data_tmp)
    return data


class Scientist:

    @classmethod
    def crawl(cls, name):
        data = run_crawlers(name)
        return cls.transform_crawled_data(data)

    @classmethod
    def transform_crawled_data(cls, data):
        title = data['heading']
        summary = '\n'.join(textwrap.wrap(data['summary']))
        page_content = '\n'.join(data['page_content'])
        born_txt = data['biography'].get('born', '')
        born_date = utils.get_date_from_string(born_txt)

        dead_date = ''
        if data['biography'].get('died'):
            dead_txt = data['biography']['died']
            if '(aged' in dead_txt:
                dead_txt = re.sub(r'\(aged.*', '', dead_txt,
                                  re.MULTILINE | re.DOTALL)
            dead_date = utils.get_date_from_string(dead_txt)

        quote = random.choice(data['quotes']) if data.get('quotes') else None

        return dict(title=title,
                    summary=summary,
                    born_date=born_date,
                    dead_date=dead_date,
                    page_content=page_content,
                    quote=quote)
