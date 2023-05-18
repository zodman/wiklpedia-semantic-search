from RPA.Browser.Selenium import Selenium
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

HEADLESS = os.environ.get("HEADLESS")


class Spider:
    drv = Selenium()

    def __init__(self, url):
        self.url = url

    def open(self):
        self.drv.open_available_browser(self.url, headless=HEADLESS)

    def close(self):
        self.drv.close_browser()

    def parse(self):
        assert False, 'needs implement'


class WikipediaSpider(Spider):

    def parse(self):
        heading = self.drv.find_element('xpath://h1[@id="firstHeading"]').text
        return dict(heading=heading)


def crawler():
    url = 'https://en.wikipedia.org/wiki/Galileo_Galilei'
    spider = WikipediaSpider(url)
    spider.open()
    data = spider.parse()
    spider.close()
    return data


def main():
    crawl()


if __name__ == "__main__":
    main()
