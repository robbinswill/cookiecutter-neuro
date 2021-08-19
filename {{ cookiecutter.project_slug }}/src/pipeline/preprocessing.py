"""
Contains all of the preprocessing logic for the {{ cookiecutter.project_name }} project
"""

from pathlib import Path
import json

import mne
from nipype.interfaces.base import BaseInterfaceInputSpec, BaseInterface, TraitedSpec, Str, File

from omegaconf import OmegaConf, open_dict
from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra
GlobalHydra.instance().clear()
initialize(config_path='../conf/')


def _preprocessing(sub, out_file):
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

    # Load MNE Raw file
    cfg = compose("config.yaml")
    # Can we define a different root when stringing pipelines together?
    layout = BIDSLayout(root=Path(dataset_root).joinpath('raw_data').__str__())
    raw_file = layout.get(subject=sub, extension=cfg.raw_params.raw_extension, suffix=cfg.raw_params.data_type,
                          return_type='filename')[0]
    raw_load = call(cfg.read_raw, vhdr_fname=raw_file, preload=True)

    # Filter loaded MNE Raw file
    pre_cfg = cfg.preprocessing_params
    raw_filt = raw_load.copy().filter(l_freq=pre_cfg.l_freq, h_freq=pre_cfg.h_freq,
                                      l_trans_bandwidth=pre_cfg.l_trans_bandwidth,
                                      h_trans_bandwidth=pre_cfg.h_trans_bandwidth,
                                      filter_length=pre_cfg.filter_length,
                                      method=pre_cfg.method,
                                      picks=mne.pick_types(raw_load.info, eeg=True, eog=True),
                                      n_jobs=pre_cfg.n_jobs)

    # Save filtered MNE Raw file
    raw_filt.save(out_file.__str__())


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
        _preprocessing(
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
        cfg[pipeline_root] = pipeline_dir.__str__()
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
    with open(Path(cfg[pipeline_root]).joinpath('dataset_description.json'), 'w') as f:
        json.dump(deriv_data, f, indent=2)
    f.close()

