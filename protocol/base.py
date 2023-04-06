# -*- coding: utf-8 -*-

"""Main module."""
# A [imaging] Parameter is a container class for a single value, with a name
#       with methods to check for compliance and validity
# A [imaging] Sequence is defined as a set of parameters
#       implemented as a dict
# A [Sequence] Protocol is an unmutable Sequence for reference
# An Imaging Protocol is an ordered sequence of Sequences for a single session
#       although their order isn't used or checked in any way
class Unspecified(object):
    """Class to denote an unspecified value

    Reasons include:
        - not specified in the original source e.g., DICOM image header
        - enocded as None or similar; or presumed to be default

    We need this to correctly inform the downstream users of the source,
        to prevent them from assigning default values or imputing them another way!
    """

    def __init__(self):
        """constructor"""

        return NotImplemented


class BaseParameter(ABC):
    """
    Container class to support various parameter data types
      including numerical continuous (time), categorical (site), or an array of them
    """


    def __init__(self,
                 name='parameter',
                 value=Unspecified,
                 dtype=float,
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

        self.value = value
        self.dtype = dtype
        self.units = units
        self.range = range
        self.steps = steps

        self.name = name
        self.acronym = acronym
        self.dicom_tag = dicom_tag

        self.decimals = 2  # numerical tolerance in decimal places


    def compliant(self, other):
        """Method to check if one parameter value is compatible w.r.t another,
            either in equality or within acceptable range, for that data type.

        If any of the values to be compared are Unspecified, it returns False
        """

        if self.value is Unspecified or other.value is Unspecified:
            warn('one of the values being compared is Unspecified!', UserWarning)
            return False
        else:
            return self._check_compliance(other)


    @abstractmethod
    def _check_compliance(self, other):
        """Method to check if one parameter value is compatible w.r.t another,
            either in equality or within acceptable range, for that data type.
        """


    def __eq__(self, other):
        """equality is defined as compliance here"""

        return self.compliant(other)


    def __repr__(self):
        """repr"""

        return f'{self.name}({self.value})'

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
                 params: dict = None):
        """constructor"""

        super().__init__()

        self.name = name
        self.params = set()

        if isinstance(params, dict):
            self.params = set(list(params.keys()))
            self.__dict__.update(params)

        # parameters and their values can be modified
        self._mutable = True


    def add(self, param_list: Union[BaseParameter, list[BaseParameter]]):
        """method to add new parameters; overwrite previous values if exists."""

        if not isinstance(param_list, Iterable):
            param_list = [param_list, ]

        for param in param_list:
            if not isinstance(param, BaseParameter):
                raise ValueError(f'Input value {param} is not of type BaseParameter')

            # retaining full Parameter instance, not just value
            self.__dict__[param.name] = param
            self.params.add(param.name)


    def __setitem__(self,
                    key : str,
                    value: BaseParameter):
        """setter"""

        if not isinstance(value, BaseParameter):
            raise ValueError('Input value is not of type BaseParameter')

        if not isinstance(key, str):
            raise ValueError('Input name is not a string!')

        self.__dict__[key] = value
        self.params.add(key)


    def __getitem__(self, name,
                    not_found_value=Unspecified):
        """getter"""

        try:
            return self.__dict__[name]
        except KeyError:
            return not_found_value


    def compliant(self, other):
        """Method to check if one sequence is compatible w.r.t another,
            either in equality or within acceptable range, for each parameter.
        """

        if not isinstance(other, BaseSequence):
            raise TypeError(f'Sequence to compare {other} is not of type '
                            f'BaseSequence')

        non_compliant_params = list()

        for pname in self.params:
            this_param = self.__dict__[pname]
            that_param = other[pname]
            if not that_param.compliant(this_param):
                non_compliant_params.append((this_param, that_param))

        bool_flag = len(non_compliant_params) < 1

        return bool_flag, non_compliant_params


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
            plist.append(f'{param.name}={param.value}')

        return '{}({})'.format(self.name, ','.join(plist))

    def __repr__(self):
        return self.__str__()


class ImagingSequence(BaseSequence, ABC):
    """Class representing an Imaging sequence

    Although we would use it mostly for MR imaging sequences to start with,
      it should be able to store any sequence captured by DICOM: CT, XRAY etc
    """


    def __init__(self, name='MRI'):
        """constructor"""

        super().__init__(name=name)


    def from_dicom(self, dcm_path):
        """Parses the parameter values from a given DICOM file."""

