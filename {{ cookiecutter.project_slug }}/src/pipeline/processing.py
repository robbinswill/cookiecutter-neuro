"""
Contains all of the preprocessing logic for the {{ cookiecutter.project_name }} project
"""

from pathlib import Path
import os
import json

from nipype.interfaces.base import BaseInterfaceInputSpec, BaseInterface, TraitedSpec, Str, File

from omegaconf import OmegaConf, open_dict
from hydra import compose, initialize
from hydra.utils import call
from hydra.core.global_hydra import GlobalHydra
GlobalHydra.instance().clear()
initialize(config_path='../conf/')


def _get_raw(sub: str):
    """
    Returns the MNE Raw object based on the given subject ID
    """
    import os
    from dotenv import find_dotenv, load_dotenv
    from pathlib import Path

    from bids import BIDSLayout
    from omegaconf import DictConfig, OmegaConf
    from hydra import compose, initialize_config_dir
    from hydra.utils import call

    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    DATASET_ROOT = Path(os.getenv("DATASET"))
    PROJECT_ROOT = Path(os.getenv("PROJECT"))
    dataset_root = DATASET_ROOT.joinpath('raw_data').__str__()
    project_root = PROJECT_ROOT.joinpath('src', 'conf').__str__()

    initialize_config_dir(config_dir=project_root)
    cfg = compose("config.yaml")

    layout = BIDSLayout(root=dataset_root)
    raw_file = layout.get(subject=sub, extension=cfg['raw_extension'], suffix=cfg['data_type'],
                          return_type='filename')[0]
    return call(cfg.raw, vhdr_fname=raw_file)


class PreprocessingInputSpec(BaseInterfaceInputSpec):
    sub_id = Str(mandatory=True, desc='The subject ID to preprocess')


class PreprocessingOutputSpec(TraitedSpec):
    out_raw = File(desc='The preprocesses MNE Raw file')


class Preprocessing(BaseInterface):
    input_spec = PreprocessingInputSpec
    output_spec = PreprocessingOutputSpec

    def _run_interface(self, runtime):
        # Call the Preprocessing logic here
        _get_raw(
            self.inputs.sub_id
        )
        return runtime

    def _list_outputs(self):
        return {'out_raw': self.output_spec.out_raw}


def create_derivatives_dataset(pipeline_root: str):
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
                      {'Name': pipeline_root}
                  ],
                  'SourceDatasets': [
                      {'URL': DATASET_ROOT.joinpath('raw_data').__str__()}
                  ]}
    PIPELINE_ROOT = Path(cfg.PIPELINE)
    with open(PIPELINE_ROOT.joinpath('dataset_description.json'), 'w') as f:
        json.dump(deriv_data, f, indent=2)
    f.close()

