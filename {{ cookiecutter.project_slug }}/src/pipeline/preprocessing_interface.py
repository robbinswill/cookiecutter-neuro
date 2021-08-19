"""
This script contains the preprocessing logic
"""

import typer
app = typer.Typer(help='Preprocessing interface')

import json
from nipype import Node
from .preprocessing import Preprocessing, create_derivatives_dataset
from mne_bids import BIDSPath
from pathlib import Path

from omegaconf import OmegaConf, open_dict
from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra
GlobalHydra.instance().clear()
initialize(config_path='../conf/')


@app.command()
def new_pipeline(pipeline_name: str = typer.Option(..., prompt='Enter a name for the new pipeline'),
                 pipeline_desc: str = typer.Option(..., prompt='Provide a short description of the pipeline')):
    """
    Generate a new preprocessing pipeline with a subfolder in the BIDS dataset
    """

    # Need to figure out how to manage multiple pipelines
    # Also need functionality to choose which pipeline to execute
    create_derivatives_dataset(pipeline_name, pipeline_desc)
    typer.echo(f'{pipeline_name} derivative subfolder created in BIDS dataset')


@app.command()
def preprocess_subject(sub: str = typer.Option(..., prompt='Enter subject ID'),
                       pipeline: str = typer.Option(..., prompt='Enter pipeline name')):
    """
    Launch preprocessing step for the given subject
    """

    # Assume we are running test-pipeline, with no tasks, sessions, runs, etc.
    # Retrieve desired filename for derivative outputs, to pass to preprocessing function
    cfg = compose('env.yaml')
    pipeline_root = cfg[pipeline]

    cfg = compose('config.yaml')
    bids_deriv_path = BIDSPath(subject=sub, root=pipeline_root, datatype=cfg.raw_params.data_type)

    filepath = Path(bids_deriv_path.__str__() + '_desc-'
                    + pipeline + '_' + cfg.raw_params.data_type + '.fif')


    # Assuming we are running test-pipeline
    pre_raw = Node(Preprocessing(sub_id=sub, out_file=filepath), name='preproc_node')
    pre_raw.run()
