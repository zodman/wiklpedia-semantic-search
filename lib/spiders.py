from RPA.Browser.Selenium import Selenium
import re
import logging
from lib import constants
import SeleniumLibrary.errors

log = logging.getLogger(__name__)


class SpiderError(Exception):
    pass


class SpiderErrorNotFound(Exception):
    pass


class Spider:
    drv = Selenium()

    def __init__(self, url):
        self.url = url

    def open(self):
        log.info(f'opening browser {self.url}')
        if not self.drv.open_available_browser(self.url,
                                               headless=constants.HEADLESS):
            raise SpiderError('Browser cannot open')

    def close(self):
        log.info(f'closing browser {self.url}')
        self.drv.close_browser()

    def parse_page(self):
        log.info('parsing')
        try:
            return self.parse()
        except Exception as e:
            raise SpiderError(e)

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


class WikipediaScientistSpider(Spider):

    def open(self):
        super().open()
        text = 'Wikipedia does not have an article with this exact name.'
        locator = f"xpath://*[contains(., '{text}')]"
        try:
            is_present = self.drv.find_element(locator) is not None
            if is_present:
                raise SpiderErrorNotFound
        except SeleniumLibrary.errors.ElementNotFound:
            pass

    def _clean(self, txt):
        return re.sub(r'\[\d{0,4}\]', ' ', txt)

    def _get_content(self):
        elements = self.drv.find_elements(
            'xpath://*[@id="mw-content-text"]/div/'
            '*[self::p or self::h3/span[@class="mw-headline"]]')
        summary_list = []
        for node in elements:
            txt = node.text
            if node.tag_name == 'h3':
                txt = f'\n{node.text}\n'
            if txt.strip() == '':
                continue
            txt = self._clean(txt)
            summary_list.append(txt)
        return summary_list

    def _get_biography_table(self):
        try:
            bio_table = self.drv.find_element(
                "xpath://table[contains(@class,'biography')]")
        except SeleniumLibrary.errors.ElementNotFound:
            return {}
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
        page_content = self._get_content()
        biography = self._get_biography_table()
        return dict(heading=heading,
                    summary=page_content[0],
                    biography=biography,
                    page_content=page_content)
