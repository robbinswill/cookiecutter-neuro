"""
Contains all of the preprocessing logic for the {{ cookiecutter.project_name }} project
"""

from pathlib import Path
import os

from dotenv import find_dotenv, load_dotenv

from nipype.interfaces.base import BaseInterfaceInputSpec, BaseInterface, TraitedSpec, Str, File

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

PROJECT_ROOT = Path(os.getenv("PROJECT"))


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
    pipeline_dir = PROJECT_ROOT.joinpath(pipeline_root)
    pipeline_dir.mkdir(exist_ok=True, parents=True)

    # Add the pipeline directory to .env
    with open(PROJECT_ROOT.joinpath('.env'), 'w') as f:
        f.write(f'PIPELINE = {pipeline_dir}\n')
    f.close()
