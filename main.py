from lib import utils
import click
from lib import crawlers
from lib import constants
from lib import formats
from lib import spiders
import os
import json
from lib import populate as base_populate
from lib import bonus as base_bonus
import logging

log = logging.getLogger(__name__)


def execute_robot(name):
    click.secho(f'🕷️ Scrapping {name}', fg='green')
    try:
        return crawlers.Scientist.crawl(name)
    except spiders.SpiderErrorNotFound:
        click.secho(f'{name} Not Found', fg='red')


@click.group
def cli():
    pass


@cli.command
@click.option('--format',
              type=click.Choice(['txt', 'json']),
              default='txt',
              help='output format')
@click.option('--other', help='Other scientistic name')
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

    if format == 'json' and len(data_list) > 0:
        formats.to_json(data_list)
        if other:
            formats.to_text(data_list)
    else:
        formats.to_text(data_list)
    utils.send_heartbeat()


@cli.command
def populate():  # pragma: no cover
    if os.path.exists(constants.JSON_FILENAME):
        data_list = json.loads(open(constants.JSON_FILENAME).read())
        documents = base_populate.convert_scientsts_to_documents(data_list)
        base_populate.populate(documents)
        click.secho('finished', fg='green')
    else:
        click.secho('json not exist', fg='red')


@cli.command()
def bonus():  # pragma: no cover
    base_bonus.bonus()


if __name__ == "__main__":
    utils.configure_loggers()
    cli()
