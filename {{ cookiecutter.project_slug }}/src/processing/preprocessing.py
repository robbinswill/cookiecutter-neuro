"""
Contains all of the preprocessing logic for the {{ cookiecutter.project_name }} project
"""

import os
from dotenv import find_dotenv, load_dotenv
from pathlib import Path


# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()
# load up the entries as environment variables
load_dotenv(dotenv_path)

STAGING_ROOT = Path(os.getenv("STAGING"))
DATASET_ROOT = Path(os.getenv("DATASET"))
PROJECT_ROOT = Path(os.getenv("PROJECT"))


class Preprocessing:
    """
    To be used by the processing interface for implementing preprocessing steps
    """
    def __init__(self):
        self.project_root = PROJECT_ROOT.joinpath('src', 'conf').__str__()
        self.dataset_root = DATASET_ROOT.joinpath('raw_data').__str__()


    def _get_raw(self, sub: str):
        """
        Returns the MNE Raw object based on the given subject ID
        """
        from bids import BIDSLayout
        from omegaconf import DictConfig, OmegaConf
        from hydra import compose, initialize_config_dir
        from hydra.utils import call

        initialize_config_dir(config_dir=self.project_root)
        cfg = compose("config.yaml")

        layout = BIDSLayout(root=self.dataset_root)
        raw_file = layout.get(subject=sub, extension=cfg['raw_extension'], suffix=cfg['data_type'],
                              return_type='filename')[0]
        self.raw = call(cfg.raw, vhdr_fname=raw_file)
