"""
Contains all of the preprocessing logic for the {{ cookiecutter.project_name }} project
"""

from pathlib import Path
import os
import json

from nipype.interfaces.base import BaseInterfaceInputSpec, BaseInterface, TraitedSpec, Str, File

from omegaconf import OmegaConf, open_dict
from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra
GlobalHydra.instance().clear()
initialize(config_path='../conf/')


def _get_raw(sub: str, out_file):
    """
    Returns the MNE Raw object based on the given subject ID
    """

    from pathlib import Path

    from bids import BIDSLayout
    from hydra import compose
    from hydra.utils import call
    GlobalHydra.instance().clear()
    initialize(config_path='../conf/')

    cfg = compose('env.yaml')
    dataset_root = cfg.DATASET

    cfg = compose("config.yaml")
    layout = BIDSLayout(root=Path(dataset_root).joinpath('raw_data').__str__())
    raw_file = layout.get(subject=sub, extension=cfg.raw_extension, suffix=cfg.data_type,
                          return_type='filename')[0]
    raw_to_save = call(cfg.raw, vhdr_fname=raw_file)
    raw_to_save.save(out_file.__str__())


class PreprocessingInputSpec(BaseInterfaceInputSpec):
    sub_id = Str(mandatory=True, desc='The subject ID to preprocess')
    out_file = File(desc='The raw file in .fif format')


class PreprocessingOutputSpec(TraitedSpec):
    out_file = File(desc='The raw file in .fif format')


class Preprocessing(BaseInterface):
    input_spec = PreprocessingInputSpec
    output_spec = PreprocessingOutputSpec

    def _run_interface(self, runtime):
        # Call the Preprocessing logic here
        _get_raw(
            self.inputs.sub_id,
            self.inputs.out_file
        )
        return runtime

    def _list_outputs(self):
        return {'out_file': self.inputs.out_file}


def create_derivatives_dataset(pipeline_root: str, pipeline_desc: str):
    """
    Create a pipeline subfolder in the BIDS dataset
    """

    # Create the pipeline directory
    cfg = compose('env.yaml')
    DATASET_ROOT = Path(cfg.DATASET)
    pipeline_dir = DATASET_ROOT.joinpath('derivatives', pipeline_root)
    pipeline_dir.mkdir(exist_ok=True, parents=True)

    # Add the pipeline directory to .env
    PROJECT_ROOT = Path(cfg.PROJECT)
    OmegaConf.set_struct(cfg, True)
    with open_dict(cfg):
        cfg.PIPELINE = pipeline_dir.__str__()
    with open(PROJECT_ROOT.joinpath('src', 'conf', 'env.yaml'), 'w') as fp:
        OmegaConf.save(config=cfg, f=fp.name)
    fp.close()

    # Create dataset_description.json for this pipeline
    deriv_data = {'Name': pipeline_root + ' outputs',
                  'BIDSVersion': '1.6.0',
                  'DatasetType': 'derivative',
                  'GeneratedBy': [
                      {'Name': pipeline_root,
                       'Desc': pipeline_desc}
                  ],
                  'SourceDatasets': [
                      {'URL': DATASET_ROOT.joinpath('raw_data').__str__()}
                  ]}
    PIPELINE_ROOT = Path(cfg.PIPELINE)
    with open(PIPELINE_ROOT.joinpath('dataset_description.json'), 'w') as f:
        json.dump(deriv_data, f, indent=2)
    f.close()

