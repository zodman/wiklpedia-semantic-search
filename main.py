import click
import crawlers
import utils


@click.command
def main():
    data = crawlers.crawler()
    title = data['heading']
    summary = '\n'.join(textwrap.wrap(data['summary']))
    born_txt = data['biography'].get('born')
    born_date = utils.get_date_from_string(born_txt)

    dead_date = None
    if data['biography'].get('died'):
        dead_txt = data['biography']['died']
        dead_date = utils.get_date_from_string(dead_txt)

    quote = random.choice(data['quotes']) if data.get('quotes') else None

    click.secho(f'{title}', fg='green')
    click.secho(f'{summary}', fg='white')
    if born_date:
        click.secho(f'🎂 {born_date}', fg='yellow')
    if dead_date:
        click.secho(f'🪦 {dead_date}', fg='gray')
    if quote:
        click.secho(f'{quote}', fg='green')


if __name__ == "__main__":
    main()
