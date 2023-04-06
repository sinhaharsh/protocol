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

