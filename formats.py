import click
import constants
from datetime import date
import textwrap
import json
import os


def introduction():
    click.secho('🤖 Im robot scrapper for wikipedia Scientificts')


def to_text(list_kwargs):
    for kwargs in list_kwargs:
        title = kwargs.get('title')
        summary = kwargs.get('summary')
        born_date = kwargs.get('born_date')
        dead_date = kwargs.get('dead_date')
        quote = kwargs.get('quote')
        years = ''
        if hasattr(born_date, "year") and hasattr(dead_date, 'year'):
            years = f'({born_date.year} - {dead_date.year})'

        click.secho(f'➡️  {title} {years}', fg='green', bold=True)
        click.secho(f'📖 {summary}', fg='white')

        if born_date:
            now = date.today()
            if hasattr(born_date, 'year'):
                years = now.year - born_date.year
                click.secho(
                    f'🎂 {born_date.strftime(constants.DATE_FORMAT)}'
                    f' if {title} still alive will have {years} '
                    'years',
                    fg='yellow')
            else:
                click.secho(f'🎂 {born_date}', fg='yellow')

        if dead_date:
            if hasattr(dead_date, 'strftime'):
                dead_date = dead_date.strftime(constants.DATE_FORMAT)
            click.secho(f'🪦 {dead_date}', fg='bright_black')

        if quote:
            quote_txt = '\n'.join(textwrap.wrap(quote))
            click.secho(f'\n\n"{quote_txt}" - {title}', fg='cyan')


def to_json(list_kwargs):
    filename = os.path.join(constants.BASE_DIR, 'scientifics.json')
    prev_content = json.loads(open(filename).read())
    content = json.dumps(list_kwargs + prev_content, default=str)
    with open(filename, 'w') as file:
        file.write(content)
    click.secho(f'{filename} file was generated', fg='green')
