"""
This script contains the preprocessing logic
"""

import typer
app = typer.Typer(help='Data preprocessing interface')

import os
import json
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
from bids import BIDSLayout
from nipype.interfaces.io import BIDSDataGrabber
from nipype.pipeline import Node, MapNode, Workflow


# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()
# load up the entries as environment variables
load_dotenv(dotenv_path)

STAGING_ROOT = Path(os.getenv("STAGING"))
DATASET_ROOT = Path(os.getenv("DATASET"))
PROJECT_ROOT = Path(os.getenv("PROJECT"))


@app.command()
def preprocess_subject(sub: str):
    """
    Launch preprocessing step for the given subject
    """
    layout = BIDSLayout(DATASET_ROOT.joinpath('raw_data').__str__())
    subject_ids = layout.get(return_type='id', target='subject')
    test_id = subject_ids[0]  # Gets sub-1 ID


    

    # Later try reading in and filtering a raw object
    print('done')


