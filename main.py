import click
import crawlers
import utils
import textwrap
import random
import re
import formats

SCIENTISTS = [
    "Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"
]


class Scientistic:

    @classmethod
    def crawl(cls, name):
        data = crawlers.crawler(name)
        title = data['heading']
        summary = '\n'.join(textwrap.wrap(data['summary']))
        born_txt = data['biography'].get('born')
        born_date = utils.get_date_from_string(born_txt)

        dead_date = None
        if data['biography'].get('died'):
            dead_txt = data['biography']['died']
            if '(aged' in dead_txt:
                dead_txt = re.sub(r'\(aged.*', '', dead_txt,
                                  re.MULTILINE | re.DOTALL)
            dead_date = utils.get_date_from_string(dead_txt)

        quote = random.choice(data['quotes']) if data.get('quotes') else None
        formats.to_text(title, summary, born_date, dead_date, quote)


@click.command
def main():
    for scient_name in SCIENTISTS:
        Scientistic.crawl(scient_name)


if __name__ == "__main__":
    main()
