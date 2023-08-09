import warnings
from abc import ABC
from numbers import Number
from pathlib import Path

import numpy as np
import pydicom
from protocol import BaseSequence
from protocol.base import BaseParameter, NumericParameter, CategoricalParameter, VariableNumericParameter
from protocol import config as cfg
from protocol.config import (ACRONYMS_IMAGING_PARAMETERS as ACRONYMS,
                             BASE_IMAGING_PARAMS_DICOM_TAGS as DICOM_TAGS,
                             Unspecified, UnspecifiedType)
from protocol.utils import get_dicom_param_value, header_exists, import_string, \
    parse_csa_params


class Manufacturer(CategoricalParameter):
    """Parameter specific class for Manufacturer"""

    _name = 'Manufacturer'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class ManufacturersModelName(CategoricalParameter):
    """Parameter specific class for ManufacturersModelName"""

    _name = 'ManufacturersModelName'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class SoftwareVersions(CategoricalParameter):
    """Parameter specific class for SoftwareVersions"""

    _name = 'SoftwareVersions'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class MagneticFieldStrength(NumericParameter):
    """Parameter specific class for MagneticFieldStrength"""

    _name = 'MagneticFieldStrength'

    def __init__(self, value=Unspecified):
        """Constructor."""
        if isinstance(value, str):
            if value.endswith('T'):
                value = value[:-1]
            try:
                value = float(value)
            except ValueError:
                raise ValueError(f"Could not convert {value} to float")

        super().__init__(name=self._name,
                         value=value,
                         units='T',
                         range=(0, 100),
                         # TODO verify the accuracy of this range
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class ReceiveCoilName(CategoricalParameter):
    """Parameter specific class for ReceiveCoilName"""

    _name = 'ReceiveCoilName'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class MRTransmitCoilSequence(CategoricalParameter):
    """Parameter specific class for MRTransmitCoilSequence"""

    _name = 'MRTransmitCoilSequence'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class SequenceVariant(CategoricalParameter):
    """Parameter specific class for SequenceVariant"""

    _name = 'SequenceVariant'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class ScanOptions(CategoricalParameter):
    """Parameter specific class for ScanOptions"""

    _name = 'ScanOptions'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class SequenceName(CategoricalParameter):
    """Parameter specific class for SequenceName"""

    _name = 'SequenceName'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class NonLinearGradientCorrection(CategoricalParameter):
    """Parameter specific class for NonLinearGradientCorrection"""

    _name = 'NonLinearGradientCorrection'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class MRAcquisitionType(CategoricalParameter):
    """Parameter specific class for MRAcquisitionType"""

    _name = 'MRAcquisitionType'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class MTState(CategoricalParameter):
    """Parameter specific class for MTState"""

    _name = 'MTState'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class SpoilingState(CategoricalParameter):
    """Parameter specific class for SpoilingState"""

    _name = 'SpoilingState'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class ParallelReductionFactorInPlane(NumericParameter):
    """Parameter specific class for ParallelReductionFactorInPlane"""

    _name = 'ParallelReductionFactorInPlane'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100),
                         # TODO verify the accuracy of this range
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class ParallelAcquisitionTechnique(NumericParameter):
    """Parameter specific class for ParallelAcquisitionTechnique"""

    _name = 'ParallelAcquisitionTechnique'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100),
                         # TODO verify the accuracy of this range
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class PartialFourier(NumericParameter):
    """Parameter specific class for PartialFourier"""

    _name = 'PartialFourier'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100),
                         # TODO verify the accuracy of this range
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class PartialFourierDirection(NumericParameter):
    """Parameter specific class for PartialFourierDirection"""

    _name = 'PartialFourierDirection'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100),
                         # TODO verify the accuracy of this range
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class DwellTime(NumericParameter):
    """Parameter specific class for DwellTime"""

    _name = 'DwellTime'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='s',
                         range=(0, 100),
                         # TODO verify the accuracy of this range
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class MultiBandAccelerationFactor(NumericParameter):
    """Parameter specific class for MultiBandAccelerationFactor"""

    _name = 'MultiBandAccelerationFactor'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100),
                         # TODO verify the accuracy of this range
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class EchoTrainLength(NumericParameter):
    """Parameter specific class for EchoTrainLength"""

    _name = 'EchoTrainLength'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100),
                         # TODO verify the accuracy of this range
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class PixelBandwidth(NumericParameter):
    """Parameter specific class for PixelBandwidth"""

    _name = 'PixelBandwidth'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='Hz',
                         range=(0, 100000),
                         # TODO verify the accuracy of this range
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class PhaseEncodingSteps(NumericParameter):
    """Parameter specific class for PhaseEncodingSteps"""

    _name = 'PhaseEncodingSteps'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100000),
                         # TODO verify the accuracy of this range
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


class ShimSetting(NumericParameter):
    """Parameter specific class for ShimSetting"""

    _name = 'ShimSetting'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100000),
                         # TODO verify the accuracy of this range
                         required=True,
                         severity='critical',
                         dicom_tag=None,
                         acronym=ACRONYMS[self._name])


class MultiSliceMode(CategoricalParameter):
    """Parameter specific class for MultiSliceMode"""

    _name = 'MultiSliceMode'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='critical',
                         dicom_tag=None,
                         acronym=ACRONYMS[self._name])


class EchoNumber(NumericParameter):
    """Parameter specific class for EchoNumber"""

    _name = 'EchoNumber'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100000),
                         # TODO verify the accuracy of this range
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])


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


class VariableEchoTime(VariableNumericParameter):
    """Parameter specific class for EchoTime"""

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


class EchoTime(NumericParameter):
    """Parameter specific class for EchoTime"""

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


class VariableEchoNumber(VariableNumericParameter):
    """Parameter specific class for EchoTime"""

    _name = "EchoNumber"

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


class IPat(CategoricalParameter):
    """Parameter specific class for PhaseEncodingDirection"""

    _name = 'IPat'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=None,
                         acronym=ACRONYMS[self._name])


class PhasePolarity(CategoricalParameter):
    """Parameter specific class for PhaseEncodingDirection"""

    _name = 'PhasePolarity'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dtype=int,
                         dicom_tag=None,
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
                 imaging_params=None,
                 path=None,):
        """constructor"""

        super().__init__(name=name, path=path)

        self.multi_echo = False
        self.imaging_params = imaging_params
        self.imaging_params_classes = []
        if self.imaging_params is not None:
            self._init_param_classes()
        if dicom is not None:
            self.parse(dicom)
            self._parse_private(dicom)

    def _init_param_classes(self):
        for p in self.imaging_params:
            param_cls_name = f'protocol.imaging.{p}'
            try:
                cls_object = import_string(param_cls_name)
            except ImportError:
                raise ImportError(f'Could not import {param_cls_name}')
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
            value = get_dicom_param_value(dicom, pname)
            if value is not None:
                self[pname] = param_class(get_dicom_param_value(dicom, pname))

    def _parse_private(self, dicom):
        """vendor specific private headers"""

        if header_exists(dicom):
            csa_header, csa_values = parse_csa_params(dicom)
            for name, val in csa_values.items():
                param_cls_name = f'protocol.imaging.{name}'

                try:
                    param_cls = import_string(param_cls_name)
                except ImportError:
                    raise ImportError(f'Could not import {param_cls_name}')

                if name in self.imaging_params:
                    self[name] = param_cls(val)
        else:
            warnings.warn('No private header found in DICOM file')
            # TODO: consider throwing a warning when expected header doesnt
            #  exist
            # TODO: need ways to specific parameter could not be read or
            #  queryable etc

    def from_dict(self, params_dict):
        """Populates the sequence parameters from a dictionary."""
        if self.imaging_params is None:
            self.imaging_params = list(params_dict.keys())
            self._init_param_classes()

        for param_class in self.imaging_params_classes:
            pname = param_class._name
            self[pname] = param_class(params_dict[pname])

    def set_echo_times(self, echo_times):
        """Sets the echo times for a multi-echo sequence."""
        if len(echo_times) > 1:
            self.multi_echo = True
            self['EchoTime'] = EchoTime(echo_times)
        else:
            self.multi_echo = False
            self['EchoTime'] = EchoTime(echo_times[0])


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


class InversionTime(NumericParameter):
    """Parameter specific class for InversionTime"""

    _name = 'InversionTime'

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


class BodyPartExamined(CategoricalParameter):
    """Parameter specific class for BodyPartExamined"""

    _name = 'BodyPartExamined'

    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS[self._name])
