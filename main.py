import click
import crawlers
import utils
import constants
import formats
import logging
import spiders

log = logging.getLogger(__name__)


def execute_robot(name):
    click.secho(f'🕷️ Scrapping {name}', fg='green')
    try:
        return crawlers.Scientistic.crawl(name)
    except spiders.SpiderErrorNotFound:
        click.secho(f'{name} Not Found', fg='red')


@click.group
def cli():
    pass


@cli.command
@click.option('--format', type=click.Choice(['txt', 'json']), default='txt')
@click.option('--other')
def run(format, other):
    formats.introduction()
    data_list = []

    if other:
        data = execute_robot(other)
        if data:
            data_list.append(data)
    else:
        for scient_name in constants.SCIENTISTS:
            data = execute_robot(scient_name)
            if data:
                data_list.append(data)

    if format == 'json':
        formats.to_json(data_list)
    else:
        formats.to_text(data_list)
    utils.send_heartbeat()


if __name__ == "__main__":
    cli()
