from datetime import datetime
import json
from os.path import isfile

import click


CONFIG_DB_PATH = './task_2/database.json'


@click.group()
def main():
    """Simple ToDo app with a command line interface."""
    if not isfile(CONFIG_DB_PATH):
        with open(CONFIG_DB_PATH, 'w', encoding='utf-8') as db:
            db.write(json.dumps({}, indent=4))


@click.command()
@click.option('--tasks', '-t', multiple=True, help='Enter task name.')
def add(tasks):
    """Add an item to list."""
    if tasks:
        with open(CONFIG_DB_PATH, 'r', encoding='utf-8') as db:
            data = json.load(db)

        for task in tasks:
            data[task] = None

        with open(CONFIG_DB_PATH, 'w', encoding='utf-8') as db:
            json.dump(data, db)

        click.echo('-> Your tasks are recorded')
    else:
        click.echo('-! Please, enter a task.')


@click.command()
@click.option('--tasks', '-t', multiple=True, help='Enter task name.')
def remove(tasks):
    """Remove an item from list."""
    if tasks:
        with open(CONFIG_DB_PATH, 'r', encoding='utf-8') as db:
            data = json.load(db)

        for task in tasks:
            data.pop(task)

        with open(CONFIG_DB_PATH, 'w', encoding='utf-8') as db:
            json.dump(data, db)

        click.echo('-> Your tasks are removed')
    else:
        click.echo('-! Please, enter a task.')


@click.command()
@click.option('--task', '-t', help='Enter task name.')
def done(task):
    """Mark a task as completed."""
    if task:
        with open(CONFIG_DB_PATH, 'r', encoding='utf-8') as db:
            data = json.load(db)

        data[task] = datetime.now().strftime("%Y-%d-%m")

        with open(CONFIG_DB_PATH, 'w', encoding='utf-8') as db:
            json.dump(data, db)

        click.echo(f'-> You have completed the task: {task}')
    else:
        click.echo('-! Please, enter a task.')


@click.command()
@click.option('--all_item', '-a', is_flag=True, help='Show planned and completed tasks.')
def todo(all_item):
    """Show my planned tasks."""
    with open(CONFIG_DB_PATH, 'r', encoding='utf-8') as db:
        data = json.load(db)
        if all_item:
            click.echo('-> List your all tasks:')
            for item in data:
                click.echo(f'-- {item};')
        else:
            click.echo('-> List your planned tasks:')
            for item in data.items():
                if not item[1]:
                    click.echo(f'-- {item[0]};')


@click.command()
def statistic():
    """Get my statistic."""
    stats = {}
    with open(CONFIG_DB_PATH, 'r', encoding='utf-8') as db:
        data = json.load(db)
        for task, date in data.items():
            stats[date] = stats.get(date, 0) + 1

        stats.pop(None)
        click.echo('-> Your statistics:')
        for date, counter in stats.items():
            click.echo(f"-- {date}: you've completed {counter} tasks!")


main.add_command(add)
main.add_command(remove)
main.add_command(done)
main.add_command(todo)
main.add_command(statistic)

if __name__ == '__main__':
    main()
