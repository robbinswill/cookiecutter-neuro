import pathlib
import os

# Generate .env file in project directory
project_dir = os.getcwd()
pathlib.Path(project_dir).joinpath('.env').touch()

# Write dataset, staging and project root paths to .env
f = open('.env', 'a')
f.write('PROJECT = {{ cookiecutter.project_path }}\n')
f.close()
