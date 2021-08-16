"""
Driver script for cookiecutter-neuro. Provides a CLI for users.
"""

from src.data import data_interface
from src.processing import processing_interface

import typer
app = typer.Typer(help='{{ cookiecutter.project_name }} main interface')
app.add_typer(data_interface.app, name='data')
app.add_typer(processing_interface.app, name='proc')


if __name__ == '__main__':
    app()
