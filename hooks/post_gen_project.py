from pathlib import Path
import os

from omegaconf import DictConfig, OmegaConf
from hydra import compose, initialize_config_dir
from hydra.utils import call

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

# Write dataset, staging and project root paths to .env
if __name__ == '__main__':
    Path(PROJECT_DIRECTORY).joinpath('src', 'conf', 'env.yaml').touch(exist_ok=True)
    to_insert = PROJECT_DIRECTORY.__str__()
    conf = OmegaConf.create({'PROJECT': '{}'.format(to_insert)})
    with open(Path(PROJECT_DIRECTORY).joinpath('src', 'conf', 'env.yaml'), 'w') as fp:
        OmegaConf.save(config=conf, f=fp.name)
    fp.close()
