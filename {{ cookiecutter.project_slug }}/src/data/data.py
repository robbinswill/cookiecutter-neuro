"""
Contains methods to create and query BIDS folders and metadata
"""

from pathlib import Path
import json
import os

from mne_bids import BIDSPath, write_raw_bids
import bids.config
from bids import BIDSLayout
bids.config.set_option('extension_initial_dot', True)

from omegaconf import OmegaConf, open_dict
from hydra import compose, initialize
from hydra.utils import call
from hydra.core.global_hydra import GlobalHydra
GlobalHydra.instance().clear()
initialize(config_path='../conf/')


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
    cfg = compose('env.yaml')
    PROJECT_ROOT = cfg.PROJECT
    OmegaConf.set_struct(cfg, True)
    with open_dict(cfg):
        cfg.DATASET = dataset_root
    with open(Path(PROJECT_ROOT).joinpath('src', 'conf', 'env.yaml'), 'w') as fp:
        OmegaConf.save(config=cfg, f=fp.name)
    fp.close()


def set_bids_path(dataset_root: str):
    """
    Point this project to an already-existing BIDS dataset
    """

    # Add the BIDS root to the .env file
    cfg = compose('env.yaml')
    PROJECT_ROOT = cfg.PROJECT
    OmegaConf.set_struct(cfg, True)
    with open_dict(cfg):
        cfg.DATASET = dataset_root
    with open(Path(PROJECT_ROOT).joinpath('src', 'conf', 'env.yaml'), 'w') as fp:
        OmegaConf.save(config=cfg, f=fp.name)
    fp.close()


def get_bids_path():
    """
    Return the BIDS dataset root
    """
    cfg = compose('env.yaml')
    return cfg.DATASET


def create_staging_dir():
    """
    Generate a directory for staging data inputs
    This assumes you want to create a generic staging folder in the project folder (easy)
    """
    cfg = compose('env.yaml')
    PROJECT_ROOT = cfg.PROJECT

    staging_dir = Path(PROJECT_ROOT).joinpath('{{ cookiecutter.project_slug }}_staging')
    staging_dir.mkdir(exist_ok=True, parents=True)
    OmegaConf.set_struct(cfg, True)
    with open_dict(cfg):
        cfg.STAGING = staging_dir.__str__()
    with open(Path(PROJECT_ROOT).joinpath('src', 'conf', 'env.yaml'), 'w') as fp:
        OmegaConf.save(config=cfg, f=fp.name)
    fp.close()


def set_staging_path(staging_root: str):
    """
    Set the STAGING env variable to an already-existing staging folder
    """
    cfg = compose('env.yaml')
    PROJECT_ROOT = cfg.PROJECT
    OmegaConf.set_struct(cfg, True)
    with open_dict(cfg):
        cfg.STAGING = staging_root
    with open(Path(PROJECT_ROOT).joinpath('src', 'conf', 'env.yaml'), 'w') as fp:
        OmegaConf.save(config=cfg, f=fp.name)
    fp.close()


def get_staging_path():
    """
    Return the path to the staging folder
    """
    cfg = compose('env.yaml')
    return cfg.STAGING


def add_bids_subject(filename: str):
    """
    Add a subject to this project's BIDS dataset
    """

    # Get the number of subjects currently in the BIDS dataset
    layout = BIDSLayout(root=Path(get_bids_path()).joinpath('raw_data').__str__())
    num_subs = len(layout.get(return_type='id', target='subject'))
    new_sub_id = num_subs + 1

    # Generate the MNE Raw object
    conf = compose("config.yaml")

    raw = call(conf.read_raw, vhdr_fname=Path(get_staging_path()).joinpath(filename))
    raw.info['line_freq'] = conf.raw_params.line_freq
    raw.info['ch_name'] = conf.raw_params.data_type

    # Generate the BIDSPath and write
    bids_path = BIDSPath(subject=new_sub_id.__str__(), root=Path(get_bids_path()).joinpath('raw_data').__str__(),
                         datatype=conf.raw_params.data_type)
    write_raw_bids(raw, bids_path, overwrite=True)

