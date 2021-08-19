"""
This script contains the preprocessing logic
"""

import typer
app = typer.Typer(help='Preprocessing interface')

import json
from nipype import Function, Node
from .preprocessing import Preprocessing, create_derivatives_dataset
from bids import BIDSLayout
from mne_bids import BIDSPath
from pathlib import Path

from omegaconf import OmegaConf, open_dict
from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra
GlobalHydra.instance().clear()
initialize(config_path='../conf/')


@app.command()
def new_pipeline():
    """
    Generate a new preprocessing pipeline with a subfolder in the BIDS dataset
    """

    # For now, we generate a generic pipeline called "test-pipeline"
    # Need to figure out how to manage multiple pipelines
    # Also need functionality to choose which pipeline to execute
    create_derivatives_dataset('test-pipeline')
    typer.echo(f'test-pipeline derivative subfolder created in BIDS dataset')


@app.command()
def preprocess_subject(sub: str):
    """
    Launch preprocessing step for the given subject
    """

    # Assume we are running test-pipeline, with no tasks, sessions, runs, etc.
    # Retrieve desired filename for derivative outputs, to pass to preprocessing function
    cfg = compose('env.yaml')
    pipeline_root = cfg.PIPELINE

    cfg = compose('config.yaml')
    bids_deriv_path = BIDSPath(subject=sub, root=pipeline_root, datatype=cfg.data_type)

    with open(Path(pipeline_root).joinpath('dataset_description.json')) as fp:
        json_file = json.load(fp)
    fp.close()
    filepath = Path(bids_deriv_path.__str__() + '_desc-'
                    + json_file['GeneratedBy'][0]['Desc'] + '_' + cfg.data_type + '.fif')


    # Assuming we are running test-pipeline
    pre_raw = Node(Preprocessing(sub_id=sub, out_file=filepath), name='preproc_node')
    result = pre_raw.run()
