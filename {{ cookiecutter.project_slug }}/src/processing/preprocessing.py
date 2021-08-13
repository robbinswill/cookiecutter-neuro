"""
This script contains the preprocessing logic
"""

import typer
app = typer.Typer(help='Data preprocessing interface')

from bids.layout import BIDSLayout
from nipype.interfaces.io import BIDSDataGrabber
from nipype.pipeline import Node, MapNode, Workflow


