from RPA.Browser.Selenium import Selenium
import random
import textwrap
import os
import re
import click
import logging
import utils

log = logging.getLogger(__name__)


HEADLESS = os.environ.get("HEADLESS")


class Spider:
    drv = Selenium()

    def __init__(self, url):
        self.url = url

    def open(self):
        log.info(f'opening browser {self.url}')
        self.drv.open_available_browser(self.url, headless=HEADLESS)

    def close(self):
        log.info(f'closing browser {self.url}')
        self.drv.close_browser()

    def parse_page(self):
        log.info('parsing')
        return self.parse()

    def parse(self):
        assert False, 'needs implement'

    @classmethod
    def run(cls, url):
        spider = cls(url)
        spider.open()
        data = spider.parse_page()
        spider.close()
        return data


class BrainQuotes(Spider):

    def parse(self):
        elements = self.drv.find_elements('xpath://*[@title="view quote"]')
        quotes = [i.text for i in elements]
        return dict(quotes=quotes)


class WikipediaSpider(Spider):

    def _clean(self, txt):
        return re.sub(r'\[\d{0,2}\]', ' ', txt)

    def _get_summary(self):
        elements = self.drv.find_elements(
            'xpath://*[@id="mw-content-text"]/div/*[self::p or self::h3/span[@class="mw-headline"]]'
        )
        summary_list = []
        for i in elements:
            if i.tag_name == 'h3':
                txt = f'\n{i.text}\n'
            else:
                txt = i.text
            if txt.strip() == '':
                continue
            txt = self._clean(txt)
            summary_list.append(txt)
        return summary_list[0]

    def _get_biography_table(self):
        bio_table = self.drv.find_element(
            "xpath://table[contains(@class,'biography')]")
        elements_label = self.drv.find_elements(
            'xpath://tr/th[@class="infobox-label"]', parent=bio_table)
        elements_data = self.drv.find_elements(
            'xpath://tr/td[@class="infobox-data"]', parent=bio_table)
        biography_data = {}
        for label, value in zip(elements_label, elements_data):
            label_text = label.text.strip().lower()
            biography_data[label_text] = self._clean(value.text)
        return biography_data

    def parse(self):
        heading = self.drv.find_element('xpath://h1[@id="firstHeading"]').text
        summary = self._get_summary()
        biography = self._get_biography_table()
        return dict(heading=heading, summary=summary, biography=biography)


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


@click.command
def main():
    data = crawler()
    title = data['heading']
    summary = '\n'.join(textwrap.wrap(data['summary']))
    born_txt = data['biography'].get('born')
    born_date = utils.get_date_from_string(born_txt)

    dead_date = None
    if data['biography'].get('died'):
        dead_txt = data['biography']['died']
        dead_date = utils.get_date_from_string(dead_txt)

    quote = random.choice(data['quotes']) if data.get('quotes') else None

    click.secho(f'{title}', fg='green')
    click.secho(f'{summary}', fg='white')
    if born_date:
        click.secho(f'🎂 {born_date}', fg='yellow')
    if dead_date:
        click.secho(f'🪦 {dead_date}', fg='gray')
    if quote:
        click.secho(f'{quote}', fg='green')


if __name__ == "__main__":
    main()
