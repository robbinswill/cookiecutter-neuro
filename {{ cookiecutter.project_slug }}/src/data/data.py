"""
This script retrieves all input files from "Staging", then moves them to the BIDS-compliant "Dataset" folder.
Currently, this script assumes that all inputs are in the "Staging" folder
"""

import typer
app = typer.Typer(help='Data generation interface')

import data_interface
import os
import json
from dotenv import find_dotenv, load_dotenv
from pathlib import Path

from mne_bids import BIDSPath, write_raw_bids
import bids.config
from bids import BIDSLayout
bids.config.set_option('extension_initial_dot', True)

from omegaconf import DictConfig, OmegaConf
from hydra import compose, initialize_config_dir
from hydra.utils import call


# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()
# load up the entries as environment variables
load_dotenv(dotenv_path)

STAGING_ROOT = Path(os.getenv("STAGING"))
DATASET_ROOT = Path(os.getenv("DATASET"))
PROJECT_ROOT = Path(os.getenv("PROJECT"))
PIPELINE_ROOT = Path(os.getenv("PIPELINE"))


@app.command()
def new_bids(dataset_root: str = typer.Option(..., prompt="Enter the root for the new BIDS dataset")):
    """
    Generate a new BIDS-compliant dataset
    """
    data_interface.create_bids_dataset(dataset_root)
    typer.echo(f"BIDS created at {dataset_root}")


@app.command()
def set_bids(dataset_root: str = typer.Option(..., prompt="Enter the root for current BIDS dataset")):
    """
    Attach an already-existing BIDS dataset to this project
    """
    data_interface.set_bids_path(dataset_root)
    typer.echo(f"BIDS set at {dataset_root}")


@app.command()
def set_staging(staging_root: str = typer.Option(..., prompt='Enter the root for a current staging folder')):
    """
    Attach an already-existing staging directory to this project
    """
    data_interface.set_staging_path(staging_root)
    typer.echo(f"Staging folder set at {staging_root}")


@app.command()
def new_subject(filename: str = typer.Option(..., prompt='Enter the required brain-imaging filename, as per the mne.io.read_raw_ spec')):
    """
    Add a subject to this project's BIDS dataset
    """
    data_interface.add_bids_subject(filename)
    typer.echo("Subject added")


def create_derivative(pipeline: str):
    """
    Start a derivatives folder for the given pipeline.
    This function will be called by the preprocessing command
    """

    PIPELINE_ROOT.joinpath(pipeline).mkdir(exist_ok=True)
    PIPELINE_ROOT.joinpath('dataset_description.json').touch(exist_ok=True)

    # Add data to dataset_description.json
    dataset_desc = {
        'Name': '{{ cookiecutter.project_name}} preprocessing outputs',
        'BIDSVersion': '1.6.0',
        'DatasetType': 'derivative',
        'GeneratedBy': {
            'Name': pipeline
        },
        'SourceDatasets': DATASET_ROOT.joinpath('raw_data').__str__()
    }
    with open(Path(PIPELINE_ROOT).joinpath(pipeline), 'w') as f:
        json.dump(dataset_desc, f, indent=2)
    f.close()
