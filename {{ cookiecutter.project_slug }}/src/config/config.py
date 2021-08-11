"""
define every single thing that can be configurable and can be changed in the future. Good examples are training
hyperparameters, folder paths, the model architecture, metrics, flags.
"""

from yacs.config import CfgNode as ConfigurationNode
import os
from pathlib import Path


# Declare subject, experiment and analysis parameters
__C = ConfigurationNode()
cfg = __C
__C.DESCRIPTION = 'Default config for NCIL-Framework package'

__C.SUBJECT_INPUTS = ConfigurationNode()
__C.SUBJECT_INPUTS.DESCRIPTION = 'Required inputs for each subject'
# Enter your project specific requirements below:
__C.SUBJECT_INPUTS.NAME = 'sub-name'

