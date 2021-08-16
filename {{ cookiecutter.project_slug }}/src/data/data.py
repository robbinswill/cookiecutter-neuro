"""
Contains methods to create and query BIDS folders and metadata
"""

from pathlib import Path
import json
import os

from dotenv import find_dotenv, load_dotenv

from mne_bids import BIDSPath, write_raw_bids
import bids.config
from bids import BIDSLayout
bids.config.set_option('extension_initial_dot', True)

from omegaconf import DictConfig, OmegaConf
from hydra import compose, initialize_config_dir
from hydra.utils import call

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

PROJECT_ROOT = Path(os.getenv("PROJECT"))


def create_bids_dataset(dataset_root: str):
    """
    Creates a BIDS-compliant dataset at the given root, with the raw_data subfolder
    and required metadata
    """

    # Create the raw_data subfolder and json file
    Path(dataset_root).joinpath('raw_data').mkdir(exist_ok=True, parents=True)
    Path(dataset_root).joinpath('raw_data', 'dataset_description.json').touch(exist_ok=True)

    # Populate dataset_description.json
    dataset_desc = {
        'Name': '{{ cookiecutter.project_name }}',
        'BIDSVersion': '1.6.0',
        'DatasetType': 'raw'
    }
    with open(Path(dataset_root).joinpath('raw_data', 'dataset_description.json'), 'w') as f:
        json.dump(dataset_desc, f, indent=2)
    f.close()

    # Add the BIDS root to the .env file
    with open(PROJECT_ROOT.joinpath('.env'), 'w') as f:
        f.write(f'DATASET = {dataset_root}\n')
    f.close()


def set_bids_path(dataset_root: str):
    """
    Point this project to an already-existing BIDS dataset
    """

    # Add the BIDS root to the .env file
    with open(PROJECT_ROOT.joinpath('.env'), 'w') as f:
        f.write(f'DATASET = {dataset_root}\n')
    f.close()


def get_bids_path():
    """
    Return the BIDS dataset root
    """
    return Path(os.getenv("DATASET"))


def create_staging_dir():
    """
    Generate a directory for staging data inputs
    This assumes you want to create a generic staging folder in the project folder (easy)
    """
    staging_dir = PROJECT_ROOT.joinpath('{{ cookiecutter.project_slug }}_staging')
    staging_dir.mkdir(exist_ok=True, parents=True)
    with open(PROJECT_ROOT.joinpath('.env'), 'w') as f:
        f.write(f'STAGING = {staging_dir}\n')
    f.close()


def set_staging_path(staging_root: str):
    """
    Set the STAGING env variable to an already-existing staging folder
    """
    with open(PROJECT_ROOT.joinpath('.env'), 'w') as f:
        f.write(f'STAGING = {staging_root}\n')
    f.close()


def get_staging_path():
    """
    Return the path to the staging folder
    """
    return Path(os.getenv("STAGING"))


def add_bids_subject(filename: str):
    """
    Add a subject to this project's BIDS dataset
    """

    # Get the number of subjects currently in the BIDS dataset
    layout = BIDSLayout(root=get_bids_path().joinpath('raw_data').__str__())
    num_subs = len(layout.get(return_type='id', target='subject'))
    new_sub_id = num_subs + 1

    # Generate the MNE Raw object
    initialize_config_dir(config_dir=PROJECT_ROOT.joinpath('src', 'conf').__str__())
    cfg = compose("config.yaml")
    raw = call(cfg.raw, vhdr_fname=get_bids_path().joinpath(filename))
    raw.info['line_freq'] = cfg['line_freq']
    raw.info['ch_name'] = cfg['data_type']

    # Generate the BIDSPath and write
    bids_path = BIDSPath(subject=new_sub_id, root=get_bids_path().joinpath('raw_data').__str__(),
                         datatype=cfg['data_type'])
    write_raw_bids(raw, bids_path, overwrite=True)

