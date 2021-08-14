"""
This script retrieves all input files from "Staging", then moves them to the BIDS-compliant "Dataset" folder.
Currently, this script assumes that all inputs are in the "Staging" folder
"""

import typer
app = typer.Typer(help='BIDS data generation interface')

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


@app.command()
def create_bids():
    """
    Start a BIDS-compliant dataset at DATASET_ROOT
    """
    DATASET_ROOT.joinpath('raw_data').mkdir(exist_ok=True, parents=True)
    Path(DATASET_ROOT).joinpath('raw_data', 'dataset_description.json').touch(exist_ok=True)

    # Add data to dataset_description.json
    dataset_desc = {
        'Name': 'Dataset',
        'BIDSVersion': '1.6.0',
        'DatasetType': 'raw'
    }
    with open(Path(DATASET_ROOT).joinpath('raw_data', 'dataset_description.json'), 'w') as f:
        json.dump(dataset_desc, f, indent=2)
    f.close()


@app.command()
def new_subject():
    """
    Add a subject to this project's BIDS dataset
    """

    # Get number of subject currently in BIDS dataset
    # This could probably be smoother
    layout = BIDSLayout(DATASET_ROOT.joinpath('raw_data').__str__())
    subject_id = len(layout.get_subjects()) + 1

    # Start by reading in the Raw filenames
    filename = input("Enter the required brain-imaging filename, based on the mne.io.read_raw_ function: ")

    # Generate the MNE Raw object
    initialize_config_dir(config_dir=PROJECT_ROOT.joinpath('src', 'conf').__str__())
    cfg = compose("config.yaml")
    test = STAGING_ROOT.joinpath(filename)
    print(test)
    raw = call(cfg.raw, vhdr_fname=STAGING_ROOT.joinpath(filename))
    raw.info['line_freq'] = cfg['line_freq']
    raw.info['ch_name'] = cfg['data_type']

    # Generate the BIDSPath and write
    bids_path = BIDSPath(subject=subject_id.__str__(), root=DATASET_ROOT.joinpath('raw_data').__str__(),
                         datatype=cfg['data_type'])
    write_raw_bids(raw, bids_path, overwrite=True)
