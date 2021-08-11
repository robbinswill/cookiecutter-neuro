import pathlib
import os

# Generate .env file in project directory
project_dir = os.getcwd()
pathlib.Path(project_dir).joinpath('.env').touch()

# Write dataset and staging paths to .env
f = open('.env', 'a')
f.write('DATASET = {{ cookiecutter.bids_path }}\n')
f.write('STAGING = {{ cookiecutter.staging_path }}\n')
f.close()
