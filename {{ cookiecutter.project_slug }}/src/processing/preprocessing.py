"""
This script contains the preprocessing logic
"""

import typer
app = typer.Typer(help='Data preprocessing interface')

import os
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
from nipype import Function, Node

#todo could probably move these into config:

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()
# load up the entries as environment variables
load_dotenv(dotenv_path)

STAGING_ROOT = Path(os.getenv("STAGING"))
DATASET_ROOT = Path(os.getenv("DATASET"))
PROJECT_ROOT = Path(os.getenv("PROJECT"))


def _get_raw(project_root: str, dataset_root: str, sub: str):
    """
    Returns the MNE Raw object based on the given subject ID
    """

    from bids import BIDSLayout
    from omegaconf import DictConfig, OmegaConf
    from hydra import compose, initialize_config_dir
    from hydra.utils import call

    initialize_config_dir(config_dir=project_root)
    cfg = compose("config.yaml")

    layout = BIDSLayout(root=dataset_root)
    raw_file = layout.get(subject=sub, extension=cfg['raw_extension'], suffix=cfg['data_type'],
                          return_type='filename')[0]
    return call(cfg.raw, vhdr_fname=raw_file)


@app.command()
def preprocess_subject(sub: str):
    """
    Launch preprocessing step for the given subject
    """

    getraw = Node(Function(input_names=['project_root', 'dataset_root', 'sub'],
                           output_names=['raw'],
                           function=_get_raw),
                  name='raw_node')
    getraw.inputs.project_root = PROJECT_ROOT.joinpath('src', 'conf').__str__()
    getraw.inputs.dataset_root = DATASET_ROOT.joinpath('raw_data').__str__()
    getraw.inputs.sub = sub
    getraw.run()
    raw = getraw.result.outputs.raw

    # Later try reading in and filtering a raw object
    print('done')
