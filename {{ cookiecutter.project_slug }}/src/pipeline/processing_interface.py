"""
This script contains the preprocessing logic
"""

import typer
app = typer.Typer(help='Preprocessing interface')

from nipype import Function, Node
from . import processing


@app.command()
def new_pipeline():
    """
    Generate a new preprocessing pipeline with a subfolder in the BIDS dataset
    """

    # For now, we generate a generic pipeline called "test-pipeline"
    # Need to figure out how to manage multiple pipelines
    # Also need functionality to choose which pipeline to execute
    processing.create_derivatives_dataset('test-pipeline')
    typer.echo(f'test-pipeline derivative subfolder created in BIDS dataset')


@app.command()
def preprocess_subject(sub: str):
    """
    Launch preprocessing step for the given subject
    """

    # Assuming we are running test-pipeline
    getraw = processing.Preprocessing(
        sub_id=sub,
    )
    processed_raw = getraw.run()
