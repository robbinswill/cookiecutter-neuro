"""
Driver script for cookiecutter-neuro. Provides a CLI for users.
"""

from src.data import generate_bids
from src.processing import preprocessing

import typer
app = typer.Typer(help='{{ cookiecutter.project_name }} main interface')
app.add_typer(generate_bids.app, name='bids')
app.add_typer(preprocessing.app, name='processing')


if __name__ == '__main__':
    app()
