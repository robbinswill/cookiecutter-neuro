"""
This script retrieves all input files from "Staging", then moves them to the BIDS-compliant "Dataset" folder.
Currently, this script assumes that all inputs are in the "Staging" folder
"""

from dotenv import find_dotenv, load_dotenv
from pathlib import Path
import os

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()
# load up the entries as environment variables
load_dotenv(dotenv_path)

STAGING_ROOT = Path(os.getenv("STAGING"))
DATASET_ROOT = Path(os.getenv("DATASET"))
