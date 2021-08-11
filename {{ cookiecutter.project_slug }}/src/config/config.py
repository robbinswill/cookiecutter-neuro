"""
Define every single thing that can be configurable and can be changed in the future. Good examples are training
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
# Enter your project-specific requirements below:


__C.PREPROCESSING_PARAMS = ConfigurationNode()
__C.PREPROCESSING_PARAMS.DESCRIPTION = 'Parameters for preprocessing pipeline'
# Enter your project-specific preprocessing parameters below:


__C.ANALYSIS_PARAMS = ConfigurationNode()
__C.ANALYSIS_PARAMS.DESCRIPTION = 'Parameters for post-preprocessing analysis'
# Enter your project-specific analysis parameters below:

