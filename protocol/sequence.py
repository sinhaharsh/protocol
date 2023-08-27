from abc import ABC
from pathlib import Path

import pydicom

from protocol import BaseSequence, logger, BaseParameter
from protocol.config import Unspecified, UnspecifiedType
from protocol.imaging import VariableEchoTime, VariableEchoNumber
from protocol.utils import import_string, get_dicom_param_value, header_exists, \
    parse_csa_params


class ImagingSequence(BaseSequence, ABC):
    """Class representing an Imaging sequence

    Although we would use it mostly for MR imaging sequences to start with,
      it should be able to store any sequence captured by DICOM: CT, XRAY etc
    """

    def __init__(self,
                 name='MRI',
                 dicom=None,
                 imaging_params=None,
                 required_params=None,
                 path=None,):
        """constructor"""

        self.multi_echo = False
        self.params_classes = []

        if imaging_params is not None:
            self.imaging_params = imaging_params
        else:
            self.imaging_params = []

        if required_params is not None:
            self.required_params = required_params
        else:
            self.required_params = []

        self.parameters = set(self.imaging_params + self.required_params)

        super().__init__(name=name, path=path)

        if self.parameters:
            self._init_param_classes()
        if dicom is not None:
            self.parse(dicom)
            self._parse_private(dicom)

    def _init_param_classes(self):
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
                self[pname] = param_class(get_dicom_param_value(dicom, pname))

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
        else:
            logger.warn('No private header found in DICOM file')
            # TODO: consider throwing a warning when expected header doesnt
            #  exist
            # TODO: need ways to specific parameter could not be read or
            #  queryable etc

    def from_dict(self, params_dict):
        """Populates the sequence parameters from a dictionary."""
        self.parameters = set(params_dict.keys())
        self.imaging_params = set(params_dict.keys())

        for pname, value in params_dict.items():
            if isinstance(value, BaseParameter):
                self[pname] = value
            elif isinstance(value, UnspecifiedType):
                param_cls_name = f'protocol.imaging.{pname}'
                param_cls = import_string(param_cls_name)
                self[pname] = param_cls(value)
            else:
                param_cls_name = f'protocol.imaging.{pname}'
                param_cls = import_string(param_cls_name)
                self[pname] = param_cls(Unspecified)

    def set_echo_times(self, echo_times, echo_number=None):
        """Sets the echo times for a multi-echo sequence."""

        if len(echo_times) > 1:
            self.multi_echo = True
        else:
            self.multi_echo = False

        self['EchoTime'] = VariableEchoTime(echo_times)
        if echo_number is not None:
            self['EchoNumber'] = VariableEchoNumber(echo_number)


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
        pass

