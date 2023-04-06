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

