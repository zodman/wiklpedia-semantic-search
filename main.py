import click
import crawlers
import utils
import constants
import textwrap
import random
import re
import formats


class Scientistic:

    @classmethod
    def crawl(cls, name):
        data = crawlers.crawler(name)
        title = data['heading']
        summary = '\n'.join(textwrap.wrap(data['summary']))
        born_txt = data['biography'].get('born')
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
                    quote=quote)


@click.command
@click.option('--format', type=click.Choice(['txt', 'json']), default='txt')
def main(format):
    with click.progressbar(constans.SCIENTISTS) as bar:
        data_list = []
        for scient_name in bar:
            data = Scientistic.crawl(scient_name)
            data_list.append(data)
    if format == 'json':
        formats.to_json(data_list)
    else:
        formats.to_text(data_list)


if __name__ == "__main__":
    main()
