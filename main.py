from RPA.Browser.Selenium import Selenium
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

HEADLESS = os.environ.get("HEADLESS")


class Spider:
    selenium = Selenium()

    def __init__(self, url):
        self.url = url

    def open(self):
        self.selenium.open_available_browser(self.url, headless=HEADLESS)

    def close(self):
        self.selenium.close_browser()

    def parse(self):
        assert False, 'needs implement'


class WikipediaSpider(Spider):

    def parse(self):
        pass


def main():
    url = 'https://en.wikipedia.org/wiki/Galileo_Galilei'
    spider = WikipediaSpider(url)
    spider.open()
    spider.parse()
    spider.close()


if __name__ == "__main__":
    main()
