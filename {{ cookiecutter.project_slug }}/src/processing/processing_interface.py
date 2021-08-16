"""
This script contains the preprocessing logic
"""

import typer
app = typer.Typer(help='Data preprocessing interface')

from nipype import Function, Node
from .processing import Preprocessing
from ..data import data


@app.command()
def preprocess_subject(sub: str):
    """
    Launch preprocessing step for the given subject
    """

    # Create Derivatives folder to hold processed data



    getraw = Preprocessing(
        sub_id=sub,
    )
    processed_raw = getraw.run()
