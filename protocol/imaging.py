from protocol.base import BaseParameter, Unspecified
from protocol.config import (BASE_IMAGING_PARAMS_DICOM_TAGS as IMAGING_PARAMS,
                             ACRONYMS_IMAGING_PARAMETERS as ACRONYMS)
import numpy as np
from numbers import Number


class RepetitionTime(BaseParameter):
    """Parameter specific class for RepetitionTime"""


    def __init__(self, value=Unspecified):
        """Constructor."""

        _name = 'RepetitionTime'
        super().__init__(name=_name,
                         dtype=Number,
                         units='ms',
                         range=(0, 100000),  # TODO verify the accuracy of this range
                         required=True,
                         severity='critical',
                         dicom_tag=IMAGING_PARAMS[_name],
                         acronym=ACRONYMS[_name])

        if not isinstance(value, self.dtype):
            raise TypeError(f'Input {value} is not of type {self.dtype}')

        self.value = value

        # overriding default from parent class
        self.decimals = 3


    def _check_compliance(self, other):
        """Method to check if one parameter value is compatible w.r.t another,
            either in equality or within acceptable range, for that data type.
        """

        # tolerance is 1e-N where N = self.decimals
        if np.isclose(self.value, other.value, atol=1 ** -self.decimals):
            return True
        else:
            return False


class FlipAngle(BaseParameter):
    """Parameter specific class for FlipAngle"""


    def __init__(self, value=Unspecified):
        """Constructor."""

        _name = 'FlipAngle'
        super().__init__(name=_name, dtype=Number, required=True,
                         severity='critical', dicom_tag=IMAGING_PARAMS[_name],
                         acronym=ACRONYMS[_name])

        if not isinstance(value, self.dtype):
            raise TypeError(f'Input {value} is not of type {self.dtype}')

        self.value = value

        # overriding default from parent class
        self.decimals = 0

        # acceptable range could be achieved with different levels of tolerance
        #   from +/- 5 degrees to +/- 20 degrees
        self.abs_tolerance = 0  # degrees


    def _check_compliance(self, other):
        """Method to check if one parameter value is compatible w.r.t another,
            either in equality or within acceptable range, for that data type.
        """

        if np.isclose(self.value, other.value, atol=self.abs_tolerance):
            return True
        else:
            return False


class PhaseEncodingDirection(BaseParameter):
    """Parameter specific class for PhaseEncodingDirection"""


    def __init__(self, value=Unspecified):
        """Constructor."""

        _name = 'PhaseEncodingDirection'
        super().__init__(name=_name, dtype=str, required=True,
                         severity='critical', dicom_tag=IMAGING_PARAMS[_name],
                         acronym=ACRONYMS[_name])

        self.allowed_values = list(['i',  'j',  'k',
                                    'i-', 'j-', 'k-'])

        if not isinstance(value, self.dtype):
            raise TypeError(f'Input {value} is not of type {self.dtype}')

        # TODO allow for different formats such as ROW, COLUMN etc
        if value not in self.allowed_values:
            raise ValueError(f'Invalid value for PED. '
                             f'Must be one of {self.allowed_values}')

        self.value = str(value).lower()


    def _check_compliance(self, other):
        """Method to check if one parameter value is compatible w.r.t another,
            either in equality or within acceptable range, for that data type.
        """

        if isinstance(other, self):
            value_to_compare = other.value
        elif isinstance(other, self.dtype):
            value_to_compare = other
        else:
            raise TypeError(f'Invalid type. Must be an instance of '
                            f'{self.dtype} or {self}')

        return self.value == value_to_compare


# shortcuts

TR=RepetitionTime
PED=PhaseEncodingDirection
FA=FlipAngle
