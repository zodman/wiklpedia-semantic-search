from RPA.Browser.Selenium import Selenium
from dotenv import load_dotenv, find_dotenv
import random

from dateutil.parser import parse as dparse
import os
import re
import click
import logging

logging.basicConfig(level=logging.DEBUG)

for log_name in list(logging.root.manager.loggerDict.keys()) + [
        'RobotFramework',
]:
    logging.getLogger(log_name).setLevel(logging.CRITICAL)

log = logging.getLogger(__name__)

load_dotenv(find_dotenv())

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
        log.info(f'parsing')
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
    summary = data['summary']
    born_txt = data['biography'].get('born')
    born_date = dparse(born_txt, fuzzy=True).date()
    quote = random.choice(data['quotes']) if data.get('quotes') else None

    click.secho(f'{title}', fg='green')
    click.secho(f'{summary}', fg='white')
    click.secho(f'🎂 {born_date.strftime("%x")}', fg='yellow')
    if quote:
        click.secho(f'{quote}', fg='green')


if __name__ == "__main__":
    main()
