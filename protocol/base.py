# -*- coding: utf-8 -*-

"""Main module containing the core classes."""

from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from numbers import Number
from typing import Iterable
from typing import Union

import numpy as np

from protocol import logger
from protocol.config import (UnspecifiedType, Unspecified,
                             SUPPORTED_IMAGING_MODALITIES)
from protocol.utils import convert2ascii


# A [imaging] Parameter is a container class for a single value, with a name
#       with methods to check for compliance and validity
# A [imaging] Sequence is defined as a set of parameters
#       implemented as a dict
# A [Sequence] Protocol is an unmutable Sequence for reference
# An Imaging Protocol is an ordered sequence of Sequences for a single session
#       although their order isn't used or checked in any way


class BaseParameter(ABC):
    """
    Container class to support various parameter data types
      including numerical continuous (time), categorical (site), or an array of them
    """

    def __init__(self,
                 name='parameter',
                 value=Unspecified,
                 dtype=None,
                 units='ms',
                 steps=1,
                 range=None,
                 required=True,
                 severity='critical',
                 dicom_tag=None,
                 acronym=None):
        """constructor"""

        self.required = required
        self.severity = severity

        self._value = value
        self.dtype = dtype
        self.units = units
        self.range = range
        self.steps = steps
        if not name:
            raise ValueError('Parameter name cannot be empty!')
        self.name = convert2ascii(name)
        self.acronym = acronym
        self.dicom_tag = dicom_tag

        self.decimals = 2  # numerical tolerance in decimal places

    def get_value(self):
        return self._value

    def compliant(self, other):
        """
        Method to check if one parameter value is compatible w.r.t another,
            either in equality or within acceptable range, for that data type.

        TODO: if self(reference) is UnspecifiedType, return True. This is to allow
         for a parameter to be optional, but if self(reference) is specified, and other is not,
         return False.
        """

        if isinstance(self._value, UnspecifiedType) or isinstance(other._value, UnspecifiedType):
            logger.warning(f'one of the values being compared is UnspecifiedType'
                           f'in {self.name}')
            return True
        # elif isinstance(other.value, UnspecifiedType):
        #     return False
        else:
            return self._check_compliance(other)

    @abstractmethod
    def _check_compliance(self, other):
        """Method to check if one parameter value is compatible w.r.t another,
            either in equality or within acceptable range, for that data type.
        """

    @abstractmethod
    def _compare_value(self, other):
        """
        Method to compare the values of two parameters
        """

    @abstractmethod
    def _compare_units(self, other):
        """
        Method to compare the units of two parameters
        """

    def __eq__(self, other):
        """equality is defined as compliance here"""

        return self.compliant(other)

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        """repr"""

        name = self.acronym if self.acronym else self.name
        return f'{name}({self._value})'

    def __str__(self):
        return self.__repr__()


class MultiValueNumericParameter(BaseParameter):
    """Parameter specific class for EchoTime"""

    def __init__(self,
                 name,
                 value,
                 dicom_tag=None,
                 acronym=None,
                 units=None,
                 range=None,
                 steps=None,
                 required=True,
                 severity='critical', ):
        """Constructor."""

        super().__init__(name=name,
                         value=value,
                         dtype=Number,
                         units=units,
                         range=range,
                         steps=steps,
                         required=required,
                         severity=severity,
                         dicom_tag=dicom_tag,
                         acronym=acronym)

        if not isinstance(value, UnspecifiedType):
            if isinstance(value, Iterable):
                if not all([isinstance(v, self.dtype) for v in value]):
                    raise TypeError(f'Input {value} is not of type {self.dtype}'
                                    f' for {self.name}')
                self._value = sorted([float(v) for v in value])

            elif isinstance(value, self.dtype):
                self._value = [float(value)]
            else:
                raise TypeError(f'Input {value} is not of type {self.dtype} for'
                                f' {self.name}')

        # overriding default from parent class
        self.decimals = 3

    @property
    def get_value(self):
        if isinstance(self._value, UnspecifiedType):
            return self._value
        if len(self._value) == 1:
            return self._value[0]
        else:
            return self._value

    def _check_compliance(self, other):
        """Method to check if one parameter value is compatible w.r.t another,
            either in equality or within acceptable range, for that data type.
        """
        return self._compare_value(other) and self._compare_units(other)

    def _compare_value(self, other):
        # tolerance is 1e-N where N = self.decimals
        for v, o in zip(self._value, other._value):
            if not np.isclose(v, o, atol=1 ** -self.decimals):
                return False
        return True

    def _compare_units(self, other):
        # TODO: implement unit conversion
        return self.units == other.units


class NumericParameter(BaseParameter):
    """Parameter specific class for RepetitionTime"""

    def __init__(self,
                 name,
                 value,
                 dicom_tag=None,
                 acronym=None,
                 units=None,
                 range=None,
                 steps=None,
                 required=True,
                 severity='critical', ):
        """Constructor."""

        super().__init__(name=name,
                         value=value,
                         dtype=Number,
                         units=units,
                         range=range,
                         steps=steps,
                         required=required,
                         severity=severity,
                         dicom_tag=dicom_tag,
                         acronym=acronym)

        if not isinstance(value, UnspecifiedType):
            if not isinstance(value, self.dtype):
                raise TypeError(f'Input {value} is not of type {self.dtype} for'
                                f' {self.name}')
            if np.isnan(value):
                raise ValueError(f'Input {value} is not a valid number for '
                                 f'{self.name}')
            self._value = float(value)

        # overriding default from parent class
        self.decimals = 3

    def _check_compliance(self, other):
        """Method to check if one parameter value is compatible w.r.t another,
            either in equality or within acceptable range, for that data type.
        """
        return self._compare_value(other) and self._compare_units(other)

    def _compare_value(self, other):
        # tolerance is 1e-N where N = self.decimals
        if np.isclose(self._value, other._value, atol=1 ** -self.decimals):
            return True
        else:
            return False

    def _compare_units(self, other):
        # TODO: implement unit conversion
        return self.units == other.units


class MultiValueCategoricalParameter(BaseParameter):
    """Parameter specific class for PhaseEncodingDirection"""

    def __init__(self,
                 name,
                 value,
                 dicom_tag=None,
                 acronym=None,
                 dtype=Iterable,
                 required=True,
                 severity='critical',
                 units=None,
                 range=None,
                 allowed_values=tuple()):

        """Constructor."""

        super().__init__(name=name,
                         value=value,
                         dtype=dtype,
                         units=units,
                         range=range,
                         required=required,
                         severity=severity,
                         dicom_tag=dicom_tag,
                         acronym=acronym)

        self.allowed_values = allowed_values
        if not isinstance(value, UnspecifiedType):
            if not isinstance(value, self.dtype):
                try:
                    value = self.dtype(value)
                except TypeError:
                    raise TypeError(f'Got input {value} of type {type(value)}. '
                                    f'Expected {self.dtype} for {self.name}')
            self._value = [str(v).upper() for v in value]

        # if allowed_values is set, check if input value is allowed
        if self.allowed_values and (value not in self.allowed_values):
            raise ValueError(f'Invalid value for {self.name}. '
                             f'Must be one of {self.allowed_values}')

    def _check_compliance(self, other):
        """Method to check if one parameter value is compatible w.r.t another,
            either in equality or within acceptable range, for that data type.
        """
        return self._compare_value(other) and self._compare_units(other)

    def _compare_units(self, other):
        # TODO: implement unit conversion
        return self.units == other.units

    def _compare_value(self, other):
        if isinstance(other._value, self.dtype):
            value_to_compare = other._value
        else:
            raise TypeError(f'Invalid type. Must be an instance of '
                            f'{self.dtype} or {self}')
        return set(self._value) == set(other._value)


class CategoricalParameter(BaseParameter):
    """Parameter specific class for PhaseEncodingDirection"""

    def __init__(self,
                 name,
                 value,
                 dicom_tag=None,
                 acronym=None,
                 dtype=str,
                 required=True,
                 severity='critical',
                 units=None,
                 range=None,
                 allowed_values=tuple()):

        """Constructor."""

        super().__init__(name=name,
                         value=value,
                         dtype=dtype,
                         units=units,
                         range=range,
                         required=required,
                         severity=severity,
                         dicom_tag=dicom_tag,
                         acronym=acronym)

        self.allowed_values = allowed_values
        if not isinstance(value, UnspecifiedType):
            if not isinstance(value, self.dtype):
                try:
                    value = self.dtype(value)
                except TypeError:
                    raise TypeError(f'Got input {value} of type {type(value)}. '
                                    f'Expected {self.dtype} for {self.name}')

            if isinstance(value, str):
                # strip whitespaces if any
                value = "".join(value.split())
                self._value = str(value).upper()

        # if allowed_values is set, check if input value is allowed
        if self.allowed_values and (value not in self.allowed_values):
            raise ValueError(f'Invalid value for {self.name}. '
                             f'Must be one of {self.allowed_values}')

    def _check_compliance(self, other):
        """Method to check if one parameter value is compatible w.r.t another,
            either in equality or within acceptable range, for that data type.
        """
        return self._compare_value(other) and self._compare_units(other)

    def _compare_units(self, other):
        # TODO: implement unit conversion
        return self.units == other.units

    def _compare_value(self, other):
        if isinstance(other, type(self)):
            value_to_compare = other._value
        elif isinstance(other, self.dtype):
            value_to_compare = other
        else:
            raise TypeError(f'Invalid type. Must be an instance of '
                            f'{self.dtype} or {self}')

        return self.value == value_to_compare


class BaseSequence(MutableMapping):
    """Container to capture imaging parameter values for a given sequence.

    Intended usage:

    seq = Sequence()
    seq.params['name'] = value

    if seq1.compliant(seq2):
        # they are compliant
    else:
        # not compliant

    """

    def __init__(self,
                 name: str = 'Sequence',
                 params: dict = None,
                 path: str = None, ):
        """constructor"""

        super().__init__()

        self.name = convert2ascii(name)
        self.params = set()
        self.path = path
        self.subject_id = None
        self.session_id = None
        self.run_id = None
        self.timestamp = None
        if isinstance(params, dict):
            self.params = set(list(params.keys()))
            self.__dict__.update(params)

        # parameters and their values can be modified
        self._mutable = True

    def get_session_info(self):
        """method to get metadata to the sequence"""
        return self.subject_id, self.session_id, self.run_id

    def add(self, param_list: Union[BaseParameter, Iterable[BaseParameter]]):
        """method to add new parameters; overwrite previous values if exists."""

        if not isinstance(param_list, Iterable):
            param_list = [param_list, ]

        for param in param_list:
            if not isinstance(param, BaseParameter):
                raise ValueError(
                    f'Input value {param} is not of type BaseParameter')

            # retaining full Parameter instance, not just value
            self.__dict__[param.name] = param
            self.params.add(param.name)

    def __setitem__(self,
                    key: str,
                    value: BaseParameter):
        """setter"""

        if not isinstance(value, BaseParameter):
            raise ValueError('Input value is not of type BaseParameter')

        if not isinstance(key, str):
            raise ValueError('Input name is not a string!')

        self.__dict__[key] = value
        self.params.add(key)

    def get(self, name, not_found_value=None):
        return self.__getitem__(name=name, not_found_value=not_found_value)

    def __getitem__(self, name,
                    not_found_value=None):
        """getter"""

        try:
            return self.__dict__[name]
        except KeyError:
            if not_found_value is not None:
                return not_found_value
            else:
                raise KeyError(f'{name} has not been set yet')

    def compliant(self, other):
        """Method to check if one sequence is compatible w.r.t another,
            either in equality or within acceptable range, for each parameter.
        """

        if not isinstance(other, BaseSequence):
            raise TypeError(f'Sequence to compare {other} is not of type '
                            f'BaseSequence')

        if self.params != other.params:
            diff = self.params.symmetric_difference(other.params)
            # Don't raise error, just warn. It might be the case that
            # the two sequences are different. For example, if compliance
            # is checked only for a subset of parameters.
            logger.info('different sets of parameters - '
                        'below params exist in one but not the other :\n\t{}'
                        ''.format(diff))
            # return False, diff  # TODO varying dtype: list of names!

        non_compliant_params = list()

        for pname in self.params:
            if pname in other.params:
                this_param = self.__dict__[pname]
                that_param = other[pname]
                if not that_param.compliant(this_param):
                    non_compliant_params.append((this_param, that_param))
            else:
                logger.warn(f'{pname} not found in other sequence {other}')

        bool_flag = len(non_compliant_params) < 1

        return bool_flag, non_compliant_params  # list of BaseParameter classes

    def __eq__(self, other):
        """equivalence operator"""

        bool_flag, _ = self.compliant(other)
        return bool_flag

    def __delitem__(self, key):
        del self.__dict__[key]
        self.params.remove(key)

    def __iter__(self):
        return iter(self.params)

    def __len__(self):
        return len(self.params)

    def __str__(self):
        """human readable representation"""

        plist = list()
        for key in self.params:
            param = self.__dict__[key]
            name = param.acronym if param.acronym else param.name
            plist.append(f'{name}={param._value}')

        return '{}({})'.format(self.name, ','.join(plist))

    def __repr__(self):
        return self.__str__()


class BaseProtocol:
    """
    Base class for all protocols.

    A protocol is a sequence, except it is not mutable, to serve as a reference.
    """

    def __init__(self,
                 name="Protocol"):
        """constructor"""
        self._mutable = False
        self.name = convert2ascii(name)


class BaseImagingProtocol(BaseProtocol):
    """Base class for all imaging protocols such as MRI / neuroimaging.
    """

    def __init__(self,
                 name='ImagingProtocol',
                 category='MR'):
        """constructor
        """

        super().__init__(name=name)

        # to distinguish between different types of imaging: MR, CT, XRAY etc.
        #   as they touch different portions of DICOM
        if category not in SUPPORTED_IMAGING_MODALITIES:
            raise TypeError(f'This modality {category} not supported.'
                            f'Choose one of {SUPPORTED_IMAGING_MODALITIES}')
        else:
            self._category = category



