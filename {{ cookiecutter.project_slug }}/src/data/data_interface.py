"""
This script retrieves all input files from "Staging", then moves them to the BIDS-compliant "Dataset" folder.
Currently, this script assumes that all inputs are in the "Staging" folder
"""

import typer
app = typer.Typer(help='Data generation interface')

import data
import os
import json
from dotenv import find_dotenv, load_dotenv
from pathlib import Path

from mne_bids import BIDSPath, write_raw_bids
import bids.config
from bids import BIDSLayout
bids.config.set_option('extension_initial_dot', True)


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
    data.create_bids_dataset(dataset_root)
    typer.echo(f"BIDS created at {dataset_root}")


@app.command()
def set_bids(dataset_root: str = typer.Option(..., prompt="Enter the root for current BIDS dataset")):
    """
    Attach an already-existing BIDS dataset to this project
    """
    data.set_bids_path(dataset_root)
    typer.echo(f"BIDS set at {dataset_root}")


@app.command()
def new_staging():
    """
    Generates a new staging folder within the current project directory
    """
    data.create_staging_dir()
    typer.echo("New staging folder created in the project directory")


@app.command()
def set_staging(staging_root: str = typer.Option(..., prompt='Enter the root for a current staging folder')):
    """
    Attach an already-existing staging directory to this project
    """
    data.set_staging_path(staging_root)
    typer.echo(f"Staging folder set at {staging_root}")


@app.command()
def new_subject(filename: str = typer.Option(..., prompt='Enter the required brain-imaging filename, as per the mne.io.read_raw_ spec')):
    """
    Add a subject to this project's BIDS dataset
    """
    data.add_bids_subject(filename)
    typer.echo("Subject added")
