import click
import utils
from datetime import date
import textwrap


def to_text(title, summary, born_date, dead_date, quote):
    years = ''
    if hasattr(born_date, "year") and hasattr(dead_date, 'year'):
        years = f'({born_date.year} - {dead_date.year})'

    click.secho(f'➡️  {title} {years}', fg='green', bold=True)
    click.secho(f'📖 {summary}', fg='white')

    if born_date:
        now = date.today()
        if not isinstance(born_date, str):
            years = now.year - born_date.year
            click.secho(
                f'🎂 {born_date.strftime(utils.DATE_FORMAT)} if {title} still alive will have {years} years',
                fg='yellow')
        else:
            click.secho(f'🎂 {born_date}', fg='yellow')

    if dead_date:
        click.secho(
            f'🪦 {dead_date.strftime(utils.DATE_FORMAT) if not isinstance(dead_date,str) else dead_date}',
            fg='bright_black')

    if quote:
        quote_txt = '\n'.join(textwrap.wrap(quote))
        click.secho(f'\n\n"{quote_txt}" - {title}', fg='cyan')
