import click
import crawlers
import utils
import constants
import formats
import logging

log = logging.getLogger(__name__)


@click.command
@click.option('--format', type=click.Choice(['txt', 'json']), default='txt')
def main(format):
    formats.introduction()
    data_list = []
    for scient_name in constants.SCIENTISTS:
        click.secho(f'🕷️ Scrapping {scient_name}', fg='green')
        data = crawlers.Scientistic.crawl(scient_name)
        data_list.append(data)
    if format == 'json':
        formats.to_json(data_list)
    else:
        formats.to_text(data_list)
    utils.send_heartbeat()


if __name__ == "__main__":
    main()
