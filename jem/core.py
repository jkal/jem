import logging
import click
from jem.commands import *

@click.group()
def app():
    pass

def main():
    app.add_command(init)
    app.add_command(tag)
    app.add_command(list)
    app.add_command(delete)
    app.add_command(tags)
    app.add_command(random)
    app.add_command(grep)
    app()

if __name__ == '__main__':
    main()