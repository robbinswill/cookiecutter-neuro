"""
Driver script for cookiecutter-neuro. Provides a CLI for users.
"""

from src.data.data_interface import app as data_app
from src.pipeline.preprocessing_interface import app as proc_app

import typer
app = typer.Typer(help='{{ cookiecutter.project_name }} main interface')
app.add_typer(data_app, name='data')
app.add_typer(proc_app, name='proc')


if __name__ == '__main__':
    app()
