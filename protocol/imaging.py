from abc import ABC
from numbers import Number
from pathlib import Path

import numpy as np
import pydicom
from protocol import BaseSequence
from protocol.base import BaseParameter, NumericParameter, CategoricalParameter
from protocol import config as cfg
from protocol.config import (ACRONYMS_IMAGING_PARAMETERS as ACRONYMS,
                             BASE_IMAGING_PARAMS_DICOM_TAGS as DICOM_TAGS,
                             Unspecified)
from protocol.utils import get_dicom_param_value, header_exists, import_string, parse_csa_params

class RepetitionTime(NumericParameter):
    """Parameter specific class for RepetitionTime"""

    _name = 'RepetitionTime'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='ms',
                         range=(0, 100000),
                         # TODO verify the accuracy of this range
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class FlipAngle(NumericParameter):
    """Parameter specific class for FlipAngle"""

    _name = "FlipAngle"

    def __init__(self, value=Unspecified):
        """constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='degrees',
                         range=(0, 360),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])

        # overriding default from parent class
        self.decimals = 0

        # acceptable range could be achieved with different levels of tolerance
        #   from +/- 5 degrees to +/- 20 degrees
        self.abs_tolerance = 0  # degrees

    # overriding base class method
    def _check_compliance(self, other):
        """Method to check if one parameter value is compatible w.r.t another,
            either in equality or within acceptable range, for that data type.
        """

        if np.isclose(self.value, other.value, atol=self.abs_tolerance):
            return True
        else:
            return False


class EchoTime(NumericParameter):
    """Parameter specific class for EffectiveEchoSpacing"""

    _name = "EchoTime"

    def __init__(self, value=Unspecified):
        """constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='ms',
                         range=(0, 10000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class EffectiveEchoSpacing(NumericParameter):
    """Parameter specific class for EffectiveEchoSpacing"""

    _name = "EffectiveEchoSpacing"

    def __init__(self, value=Unspecified):
        """constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='mm',
                         range=(0, 1000),
                         required=False,
                         severity='critical',
                         dicom_tag=None,
                         acronym=ACRONYMS[self._name])


class PhaseEncodingDirection(CategoricalParameter):
    """Parameter specific class for PhaseEncodingDirection"""

    _name = 'PhaseEncodingDirection'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name],
                         allowed_values=cfg.allowed_values_PED)


class ScanningSequence(CategoricalParameter):
    """Parameter specific class for PhaseEncodingDirection"""

    _name = 'ScanningSequence'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


# # shortcuts
#
# TR=RepetitionTime
# TE=EchoTime
# PED=PhaseEncodingDirection
# FA=FlipAngle
# EES=EffectiveEchoSpacing
#
# ScanSeq = ScanningSequence
#
# # common to all vendors (EES can only be read from private CSA headers)
# IMAGING_PARAM_CLASSES = [TR,
#                          TE,
#                          PED,
#                          FA,
#                          ScanSeq]


class ImagingSequence(BaseSequence, ABC):
    """Class representing an Imaging sequence

    Although we would use it mostly for MR imaging sequences to start with,
      it should be able to store any sequence captured by DICOM: CT, XRAY etc
    """

    def __init__(self,
                 name='MRI',
                 dicom=None,
                 imaging_params=None, ):
        """constructor"""

        super().__init__(name=name)

        self.multi_echo = False
        self.imaging_params = imaging_params
        self.imaging_params_classes = []
        if self.imaging_params is not None:
            self._init_param_classes()
        if dicom is not None:
            self.parse(dicom)

    def _init_param_classes(self):
        for p in self.imaging_params:
            param_cls_name = f'protocol.imaging.{p}'
            cls_object = import_string(param_cls_name)
            self.imaging_params_classes.append(cls_object)

    def parse(self, dicom, imaging_params=None):
        """Parses the parameter values from a given DICOM object or file."""
        if self.imaging_params is None:
            if imaging_params is None:
                raise ValueError('imaging_params must be provided either during'
                                 ' initialization or during parse() call')
            else:
                self._init_param_classes()

        if not isinstance(dicom, pydicom.FileDataset):
            if not isinstance(dicom, Path):
                raise ValueError('Input must be a pydicom FileDataset or Path')
            else:
                if not dicom.exists():
                    raise IOError('input dicom path does not exist!')
                dicom = pydicom.dcmread(dicom)

        for param_class in self.imaging_params_classes:
            pname = param_class._name
            self[pname] = param_class(get_dicom_param_value(dicom, pname))

        # self['is3d'] = self['MRAcquisitionType'] == '3D'

        # self["EffectiveEchoSpacing"] = EffectiveEchoSpacing(
        #     get_effective_echo_spacing(dicom))

    def _parse_private(self, dicom):
        """vendor specific private headers"""

        if header_exists(dicom):
            csa_header, csa_values = parse_csa_params(dicom)
            for name, val in csa_values.items():
                print(name, val)
        else:
            print('No private header found in DICOM file')
            # TODO consider throwing a warning when expected header doesnt exist
            # TODO need ways to specific parameter could not be read or queryable etc
            # params['MultiSliceMode'] = None
            # params['ipat'] = None
            # params['shim'] = None
            # params['PhaseEncodingDirection'] = None

    def from_dict(self, params_dict):
        """Populates the sequence parameters from a dictionary."""
        if self.imaging_params is None:
            self.imaging_params = list(params_dict.keys())
            self._init_param_classes()

        for param_class in self.imaging_params_classes:
            pname = param_class._name
            self[pname] = param_class(params_dict[pname])


class SiemensImagingSequence(ImagingSequence):
    """Siemens specific sequence parsing
    """

    def __init__(self,
                 name='MRI',
                 dcm_path=None):
        """constructor"""

        super().__init__(name=name)

    def _parse_private_header(self):
        """method to parse vendor specific headers"""
