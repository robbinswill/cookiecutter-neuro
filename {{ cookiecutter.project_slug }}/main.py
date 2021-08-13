"""
Driver script for cookiecutter-neuro. Provides a CLI for users.
"""

from src.data import generate_bids

import typer
app = typer.Typer(help='{{ cookiecutter.project_name }} main interface')
app.add_typer(generate_bids.app, name='bids')


@app.command()
def preprocess():
    """
    Preprocess a batch or subject
    """
    pass


if __name__ == '__main__':
    app()
