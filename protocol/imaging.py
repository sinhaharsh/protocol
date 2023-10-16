from abc import ABC
from copy import deepcopy
from datetime import datetime
from pathlib import Path

import numpy as np
import pydicom
from lxml import objectify

from protocol import config as cfg, logger
from protocol.base import (BaseImagingProtocol, BaseParameter, BaseSequence,
                           CategoricalParameter, MultiValueCategoricalParameter,
                           MultiValueNumericParameter, NumericParameter)
from protocol.config import (ACRONYMS_IMAGING_PARAMETERS as ACRONYMS_IMG,
                             BASE_IMAGING_PARAMS_DICOM_TAGS as DICOM_TAGS,
                             SESSION_INFO_DICOM_TAGS as SESSION_TAGS,
                             Invalid, Unspecified, UnspecifiedType,
                             ProtocolType)
from protocol.utils import (auto_convert, convert2ascii, get_dicom_param_value,
                            get_sequence_name, header_exists, import_string,
                            parse_csa_params)


class Manufacturer(CategoricalParameter):
    """
    Parameter specific class for Manufacturer
    """

    _name = 'Manufacturer'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


class ReceiveCoilActiveElements(CategoricalParameter):
    """Parameter specific class for ReceiveCoilName"""

    _name = 'ReceiveCoilActiveElements'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


class SequenceVariant(MultiValueCategoricalParameter):
    """Parameter specific class for SequenceVariant"""

    _name = 'SequenceVariant'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='optional',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


class ShimSetting(MultiValueNumericParameter):
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
                         acronym=ACRONYMS_IMG[self._name],
                         ordered=True)


class ShimMode(CategoricalParameter):
    """Parameter specific class for ShimSetting"""

    _name = 'ShimMode'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         required=True,
                         severity='critical',
                         dicom_tag=None,
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])

        # overriding default from parent class
        self.decimals = 0

        # acceptable range could be achieved with different levels of tolerance
        #   from +/- 5 degrees to +/- 20 degrees
        self.abs_tolerance = 0  # degrees


class MultiValueEchoTime(MultiValueNumericParameter):
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
                         acronym=ACRONYMS_IMG[self._name])


class EchoTime(MultiValueNumericParameter):
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
                         acronym=ACRONYMS_IMG[self._name])


class MultiValueEchoNumber(MultiValueNumericParameter):
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
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


class PhaseEncodingDirection(CategoricalParameter):
    """Parameter specific class for PhaseEncodingDirection"""

    _name = 'PhaseEncodingDirection'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name],
                         allowed_values=cfg.allowed_values_PED)


class ScanningSequence(CategoricalParameter):
    """Parameter specific class for """

    _name = 'ScanningSequence'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class ParallelAcquisitionTechnique(CategoricalParameter):
    """Parameter specific class for """

    _name = 'ParallelAcquisitionTechnique'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=None,
                         acronym=ACRONYMS_IMG[self._name])


class PhasePolarity(CategoricalParameter):
    """Parameter specific class for """

    _name = 'PhasePolarity'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dtype=int,
                         dicom_tag=None,
                         acronym=ACRONYMS_IMG[self._name])


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
                         acronym=ACRONYMS_IMG[self._name])


class BodyPartExamined(CategoricalParameter):
    """Parameter specific class for BodyPartExamined"""

    _name = 'BodyPartExamined'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class PercentPhaseFOV(NumericParameter):
    """Parameter specific class for PercentPhaseFOV"""

    _name = 'PercentPhaseFOV'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='%',
                         range=(0, 100),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class NumberOfAverages(NumericParameter):
    _name = 'NumberOfAverages'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class SliceThickness(NumericParameter):
    _name = 'SliceThickness'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='mm',
                         range=(0, 1000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class PercentSampling(NumericParameter):
    _name = 'PercentSampling'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='%',
                         range=(0, 100),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class AngioFlag(CategoricalParameter):
    _name = 'AngioFlag'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class ImagingFrequency(NumericParameter):
    _name = 'ImagingFrequency'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='Hz',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class ImagedNucleus(CategoricalParameter):
    _name = 'ImagedNucleus'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class SpacingBetweenSlices(NumericParameter):
    _name = 'SpacingBetweenSlices'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         units='mm',
                         range=(0, 1000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class TransmitCoilName(CategoricalParameter):
    _name = 'TransmitCoilName'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class AcquisitionMatrix(MultiValueNumericParameter):
    _name = 'AcquisitionMatrix'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class SAR(NumericParameter):
    _name = 'SAR'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='W/kg',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class SliceMeasurementDuration(NumericParameter):
    _name = 'SliceMeasurementDuration'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='s',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class GradientMode(CategoricalParameter):
    _name = 'GradientMode'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class FlowCompensation(CategoricalParameter):
    _name = 'FlowCompensation'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class SliceResolution(NumericParameter):
    _name = 'SliceResolution'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=None,
                         acronym=ACRONYMS_IMG[self._name])


class ImagePositionPatient(MultiValueNumericParameter):
    _name = 'ImagePositionPatient'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=None,
                         acronym=ACRONYMS_IMG[self._name])


class PatientPosition(CategoricalParameter):
    _name = 'PatientPosition'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class SliceLocation(NumericParameter):
    _name = 'SliceLocation'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class SamplesPerPixel(NumericParameter):
    _name = 'SamplesPerPixel'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class PhotometricInterpretation(CategoricalParameter):
    _name = 'PhotometricInterpretation'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class Rows(NumericParameter):
    _name = 'Rows'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class Columns(NumericParameter):
    _name = 'Columns'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class PixelSpacing(MultiValueNumericParameter):
    _name = 'PixelSpacing'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='mm',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class BitsAllocated(NumericParameter):
    _name = 'BitsAllocated'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class BitsStored(NumericParameter):
    _name = 'BitsStored'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='NA',
                         range=(0, 100),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class HighBit(NumericParameter):
    _name = 'HighBit'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='',
                         range=(0, 100),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class PixelRepresentation(NumericParameter):
    _name = 'PixelRepresentation'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='',
                         range=(0, 100),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class SmallestImagePixelValue(NumericParameter):
    _name = 'SmallestImagePixelValue'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class LargestImagePixelValue(NumericParameter):
    _name = 'LargestImagePixelValue'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class WindowCenter(NumericParameter):
    _name = 'WindowCenter'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class WindowWidth(NumericParameter):
    _name = 'WindowWidth'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         units='',
                         range=(0, 100000),
                         required=True,
                         severity='critical',
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class WindowCenterWidthExplanation(CategoricalParameter):
    _name = 'WindowCenterWidthExplanation'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class CoilString(CategoricalParameter):
    _name = 'CoilString'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class PATMode(CategoricalParameter):
    _name = 'PATMode'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class PositivePCSDirections(CategoricalParameter):
    _name = 'PositivePCSDirections'


    def __init__(self, value=Unspecified):
        """Constructor"""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class VariableFlipAngleFlag(CategoricalParameter):
    _name = 'VariableFlipAngleFlag'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class ImageOrientationPatient(MultiValueNumericParameter):
    _name = 'ImageOrientationPatient'


    def __init__(self, value=Unspecified):
        """Constructor."""
        if not isinstance(value, UnspecifiedType):
            value = list(value)

        super().__init__(name=self._name,
                         value=value,
                         dicom_tag=DICOM_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name],
                         ordered=True)
        self.decimals = 0


    def __repr__(self):
        """repr"""

        name = self.acronym if self.acronym else self.name
        return f'{name}{self.get_value()})'


    def get_value(self):
        """getter"""
        if not isinstance(self._value, UnspecifiedType):
            return [np.round(v, self.decimals) for v in self._value]
        return self._value


class ContentDate(CategoricalParameter):
    """Parameter specific class for BodyPartExamined"""

    _name = 'ContentDate'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=SESSION_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class ContentTime(CategoricalParameter):
    """Parameter specific class for BodyPartExamined"""

    _name = 'ContentTime'


    def __init__(self, value=Unspecified):
        """Constructor."""

        super().__init__(name=self._name,
                         value=value,
                         dtype=str,
                         dicom_tag=SESSION_TAGS[self._name],
                         acronym=ACRONYMS_IMG[self._name])


class MRImagingProtocol(BaseImagingProtocol):
    """Base class for all MR imaging protocols, including neuroimaging datasets
    """


    def __init__(self,
                 name="MRIProtocol",
                 category='MR',
                 filepath=None,
                 type=ProtocolType.INFERRED_FROM_DATASET):
        """constructor"""
        self.filepath = filepath
        self.type = type
        super().__init__(name=name, category=category)

        self._seq = dict()


    @property
    def category(self):
        return self._category


    def add(self, seq):
        """Adds a new sequence to the current protocol"""

        if not isinstance(seq, BaseSequence):
            raise TypeError(
                'Invalid type! Must be a valid instance of BaseSequence')

        if seq.name in self._seq:
            raise ValueError(
                'This sequence already exists! Double check or rename!')

        self._seq[seq.name] = seq


    def get_sequence_ids(self):
        """Returns the list of sequence ids in the protocol"""
        return list(self._seq.keys())


    def __bool__(self):
        """Checks if the protocol is empty"""

        if len(self._seq) < 1:
            return False
        else:
            return True


    def __getitem__(self, name):
        """getter"""

        try:
            return self._seq[name]
        except KeyError:
            raise KeyError(f'{name} has not been set yet')


    @staticmethod
    def _get_value_and_unit(v):
        value, unit = v, None
        if v.endswith('ms'):
            value, unit = v.split('ms')[0], 'ms'
        elif v.endswith('mm'):
            value, unit = v.split('mm')[0], 'mm'
        elif v.endswith('deg'):
            value, unit = v.split('deg')[0], 'deg'
        elif v.endswith('Hz/Px'):
            value, unit = v.split('Hz/Px')[0], 'Hz/Px'
        elif v.endswith('%'):
            value, unit = v.split('%')[0], '%'
        return value.strip(), unit


    def add_sequence_from_dict(self, seq_name, param_dict):
        """
        Adds a sequence to the protocol from a dictionary
        """
        seq = ImagingSequence(name=seq_name)
        seq.from_dict(param_dict)
        self.add(seq)


class SiemensMRImagingProtocol(MRImagingProtocol):
    def __init__(self, name='SiemensMRProtocol',
                 category='MR',
                 filepath=None,
                 type=ProtocolType.USER_DEFINED,
                 program_name=None,
                 convert_ped=True):
        super().__init__(name=name, category=category, filepath=filepath, type=type)
        self.programs = {}
        self.header_title = None
        self._parameter_map = {
            'PhaseEncodingDirection'      : ['Routine', 'Phase enc. dir.'],
            'EchoTime'                    : ['Routine', 'TE'],
            'RepetitionTime'              : ['Routine', 'TR'],
            'FlipAngle'                   : ['Contrast - Common', 'Flip angle'],
            'ParallelAcquisitionTechnique': ['Resolution - iPAT', 'Accel. mode'],
            'MultiSliceMode'              : ['Sequence - Part 1', 'Multi-slice mode'],
            'PixelBandwidth'              : ['Sequence - Part 1', 'Bandwidth'],
            'RecieveCoilActiveElements'   : ['Routine', 'Coil elements'],
            'InversionTime'               : ['Contrast - Common', 'TI'],
            'MRAcquisitionType'           : ['Sequence - Part 1', 'Dimension'],
            'PercentPhaseFOV'             : ['Geometry - Common', 'FoV phase'],
            'NumberOfAverages'            : ['Routine', 'Averages'],
            'SliceThickness'              : ['Geometry - Common', 'Slice thickness'],
            }
        self.program_name = program_name

        # If PED is A >> P or P >> A, R >> L or L >> R, then use this flag to
        # convert to ROW/COL
        # This is because DICOM tags are ROW/COL, but Siemens uses A >> P, R >> L
        self.convert_ped = convert_ped
        if filepath is not None:
            self.from_xml(filepath)
            self._add_sequences_from_file()


    def _add_sequences_from_file(self):
        if self.program_name is None:
            # there is more than one protocol file in the XML
            # specify the number of protocol
            # we are taking the first one, assuming it is the latest
            self.program_name = list(self.programs.keys())[0]
            # raise ValueError('Program name not set. Use set_program_name() to
            # set it')
        for sequence_name in self.programs[self.program_name].keys():
            seq = ImagingSequence(name=sequence_name)
            parameters = {}
            for param_name in self._parameter_map.keys():
                parameters[param_name] = self._get_parameter(sequence_name,
                                                             param_name)
            seq.from_dict(parameters)
            self.add(seq)


    def set_program_name(self, program_name):
        self.program_name = program_name


    def add_to_map(self, parameter_name, access_keys):
        self._parameter_map[parameter_name] = access_keys


    def get_program_names(self):
        return self.programs.keys()


    def _get_parameter(self, sequence_name, parameter_name):
        def get_value(programs, program_name, sequence_name, access_keys):
            # recursively get the value
            access_keys = deepcopy(access_keys)
            root_ = programs[program_name][sequence_name]
            while access_keys:
                key = access_keys.pop(0)
                try:
                    root_ = root_[key]
                except KeyError as e:
                    logger.warn(
                        f'Parameter not found in the sequence {sequence_name}.')
                    raise e
            return root_


        if self.program_name is None:
            raise ValueError(
                'Program name not set. Use set_program_name() to set it')

        try:
            access_keys = self._parameter_map[parameter_name]
            value = get_value(self.programs, self.program_name, sequence_name,
                              access_keys)
        except KeyError:
            logger.warn(f'Parameter not found : {parameter_name}')
            return Unspecified

        # convert PED to DICOM tags
        if parameter_name == 'PhaseEncodingDirection' and self.convert_ped:
            if value == 'A >> P' or value == 'P >> A':
                return 'COL'
            if value == 'R >> L' or value == 'L >> R':
                return 'ROW'
        else:
            return value


    def from_xml(self, filepath=None):
        """
        A function to parse the XML file and extract the parameters for
        each sequence
        """
        # check if the file exists
        if filepath is None:
            filepath = self.filepath
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f'File {filepath} does not exist')

        # check if the file is an XML file
        if not filepath.suffix == '.xml':
            raise ValueError(f'File {filepath} is not an XML file')

        # read the tree
        tree = objectify.parse(filepath)
        # get the root
        root = tree.getroot()
        # get the header title, which is the name of the scanner
        # it is not used, but saved for future
        self.header_title = root.PrintTOC.TOC.HeaderTitle

        # there are two types of children in the root
        # 1. PrintTOC : this is the table of contents
        # 2. PrintProtocol : this is the actual protocol
        for child in root.getchildren():
            if child.tag == 'PrintTOC':
                for program in \
                        child.TOC.root.region.NormalExam_dot_engine.getchildren():
                    prog_name = program.get('name')
                    self.programs[prog_name] = {}
                    # get the sequences for each program
                    for protocol in program.getchildren():
                        seq_name = convert2ascii(protocol.get('name'))
                        self.programs[prog_name][seq_name] = dict(
                            protocol.attrib)
            elif child.tag == 'PrintProtocol':
                # The protocol is organized into cards. Each card contains a set
                # of parameters
                protocol = child.Protocol
                for step in protocol.getchildren():
                    if step.tag == 'SubStep':
                        header_path = step.ProtHeaderInfo.HeaderProtPath.text
                        header_property = step.ProtHeaderInfo.HeaderProperty.text
                        prog_name = header_path.split('\\')[-2]
                        seq_name = convert2ascii(header_path.split('\\')[-1])
                        self.programs[prog_name][seq_name][
                            'header_property'] = header_property
                        for card in step.getchildren():
                            if card.tag == 'Card':
                                for parameter in card.getchildren():
                                    label = parameter.Label.text.strip()
                                    # TODO: Also add unit to the reference protocol
                                    value, unit = self._get_value_and_unit(
                                        parameter.ValueAndUnit.text.strip())
                                    card_name = card.get('name')
                                    if card_name not in self.programs[prog_name][seq_name]:
                                        self.programs[prog_name][seq_name][card_name] = {}
                                    self.programs[prog_name][seq_name][card_name][label] = auto_convert(value)


class ImagingSequence(BaseSequence, ABC):
    """Class representing an Imaging sequence

    Although we would use it mostly for MR imaging sequences to start with
    it should be able to store any sequence captured by DICOM: CT, XRAY etc
    """


    def __init__(self,
                 name='MRI',
                 dicom=None,
                 imaging_params=None,
                 required_params=None,
                 path=None, ):
        """constructor"""

        self.multi_echo = False
        self.params_classes = []
        self.parameters = set(ACRONYMS_IMG.keys())

        super().__init__(name=name, path=path)

        if self.parameters:
            self._init_param_classes()
        if dicom is not None:
            self.parse(dicom)
            self._parse_private(dicom)
            self.set_session_info(dicom)


    def set_session_info(self, dicom):
        """
        Sets the session information from the DICOM header. This is used to
        set the session_id, subject_id, run_id and timestamp
        """
        if not isinstance(dicom, pydicom.FileDataset):
            raise TypeError('Input must be a pre-read pydicom object.')

        #   name: SeriesNumber_Suffix
        #   priority order: SeriesDescription, SequenceName, ProtocolName
        self.name = get_sequence_name(dicom)
        self.subject_id = str(dicom.get('PatientID', None))
        # series number is a proxy for session?
        self.series_number = str(dicom.get('SeriesNumber', None))
        self.session_id = str(dicom.get('StudyInstanceUID', None))
        self.run_id = dicom.get('SeriesInstanceUID', None)
        # if self.series_number:
        #     self.name = f'{self.name}_{self.series_number}'
        date = dicom.get('ContentDate', None)
        time = dicom.get('ContentTime', None)
        # TODO: time format varies across datasets. Find a way to
        #   reconcile differences and use it in timestamp
        if not isinstance(date, UnspecifiedType):
            datetime_obj = datetime.strptime(date, '%Y%m%d')
            self.timestamp = datetime_obj.strftime('%m_%d_%Y')


    def _init_param_classes(self):
        """
        Initializes the parameter classes for the sequence.
        """
        for p in self.parameters:
            param_cls_name = f'protocol.imaging.{p}'
            try:
                cls_object = import_string(param_cls_name)
            except ImportError:
                logger.error(f'Could not import {param_cls_name}')
                raise ImportError(f'Could not import {param_cls_name}')
            self.params_classes.append(cls_object)


    def parse(self, dicom, params=None):
        """Parses the parameter values from a given DICOM object or file."""
        if self.parameters is None:
            if params is None:
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

        for param_class in self.params_classes:
            pname = param_class._name
            value = get_dicom_param_value(dicom, pname)
            if value is None:
                self[pname] = param_class(Unspecified)
            else:
                try:
                    self[pname] = param_class(value)
                except TypeError or ValueError:
                    self[pname] = param_class(Invalid)


    def _parse_private(self, dicom):
        """vendor specific private headers"""

        if header_exists(dicom):
            csa_header, csa_values = parse_csa_params(dicom)
            for name, val in csa_values.items():
                param_cls_name = f'protocol.imaging.{name}'

                try:
                    param_cls = import_string(param_cls_name)
                    if name in self.parameters:
                        self[name] = param_cls(val)
                except ImportError:
                    logger.error(f'Could not import {param_cls_name}')
                except TypeError or ValueError:
                    self[name] = param_cls(Invalid)
        else:
            logger.warn('No private header found in DICOM file')
            # TODO: throw a warning when expected header doesnt exist
            # TODO: warn if specific parameter couldn't be read or queryable etc


    def from_dict(self, params_dict):
        """
        Populates the sequence parameters from a dictionary.

        Parameters
        ----------
        params_dict : dict
            Dictionary containing the parameter names and values as key, value pairs.
        """
        self.parameters = set(params_dict.keys())

        for pname, value in params_dict.items():
            if isinstance(value, float) and np.isnan(value):
                value = Unspecified

            if isinstance(value, BaseParameter):
                self[pname] = value
            else:
                param_cls_name = f'protocol.imaging.{pname}'
                param_cls = import_string(param_cls_name)
                try:
                    self[pname] = param_cls(value)
                except TypeError or ValueError:
                    self[pname] = param_cls(Invalid)


    def set_echo_times(self, echo_times, echo_number=None):
        """Sets the echo times for a multi-echo sequence."""

        if len(echo_times) > 1:
            self.multi_echo = True
        else:
            self.multi_echo = False

        self['EchoTime'] = MultiValueEchoTime(echo_times)
        if echo_number is not None:
            self['EchoNumber'] = MultiValueEchoNumber(echo_number)
