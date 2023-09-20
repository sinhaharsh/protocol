# -*- coding: utf-8 -*-

"""Top-level package for protocol."""

__author__ = """Pradeep Reddy Raamana"""
__email__ = 'raamana@gmail.com'
__version__ = '0.1.0'

import logging

from protocol.logger import INFO_FORMATTER, init_log_files
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# defines the stream handler
_ch = logging.StreamHandler()  # creates the handler
_ch.setLevel(logging.INFO)  # sets the handler info
# sets the handler formatting
_ch.setFormatter(logging.Formatter(INFO_FORMATTER))
# adds the handler to the global variable: log
logger.addHandler(_ch)
init_log_files(logger, mode='w')


from protocol.base import (BaseParameter, BaseSequence, BaseProtocol,
                           BaseMRImagingProtocol)
from protocol.config import (BASE_IMAGING_PARAMETER_NAMES,
                             BASE_IMAGING_PARAMS_DICOM_TAGS)
from protocol.imaging import ImagingSequence, SiemensMRImagingProtocol
