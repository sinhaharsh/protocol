from collections import namedtuple

from numpy import nan

Unspecified = nan

# class Unspecified(object):
#     """Class to denote an unspecified value
#
#     Reasons include:
#         - not specified in the original source e.g., DICOM image header
#         - enocded as None or similar; or presumed to be default
#
#     We need this to correctly inform the downstream users of the source,
#         to prevent them from assigning default values or imputing them another way!
#     """
#
#     def __init__(self):
#         """constructor"""
#
#         return NotImplemented
#
#     def __str__(self):
#         return 'Unspecified'
#
#     def __repr__(self):
#         return 'Unspecified'


# Constant Dicom Identifiers Used for dataset creation and manipulation
SESSION_INFO = {
    "series_instance_uid": (0x20, 0x0e),
    "sequence"           : (0x18, 0x20),
    "variant"            : (0x18, 0x21),
    "patient_name"       : (0x10, 0x10),
    "patient_id"         : (0x10, 0x20),
    "study_id"           : (0x08, 0x1030),
    "series_description" : (0x08, 0x103E),
    "series_number"      : (0x20, 0x11),
    "protocol_name"      : (0x18, 0x1030),
    "sequence_name"      : (0x18, 0x24),
    "image_type"         : (0x08, 0x08),
    "echo_number"        : (0x18, 0x86),
    "te"                 : [0x18, 0x81],
    "patient_sex"        : [0x10, 0x40],
    "patient_age"        : [0x10, 0x1010],
    }

BASE_IMAGING_PARAMS_DICOM_TAGS = {
    'Manufacturer'          : [0x08, 0x70],
    'BodyPartExamined'      : [0x18, 0x15],
    'EchoTime'              : [0x18, 0x81],
    'RepetitionTime'        : [0x18, 0x80],
    'MagneticFieldStrength' : [0x18, 0x87],
    'FlipAngle'             : [0x18, 0x1314],
    'PhaseEncodingDirection': [0x18, 0x1312],
    'EchoTrainLength'       : [0x18, 0x0091],
    'PixelBandwidth'        : [0x18, 0x95],
    'ScanningSequence'      : [0x18, 0x20],
    'SequenceVariant'       : [0x18, 0x21],
    'MRAcquisitionType'     : [0x18, 0x23],
    'PhaseEncodingSteps'    : [0x18, 0x89]
    }

ACRONYMS_IMAGING_PARAMETERS = {
    'Manufacturer'          : 'MFR',
    'BodyPartExamined'      : 'BPE',
    'EchoTime'              : 'TE',
    'RepetitionTime'        : 'TR',
    'MagneticFieldStrength' : 'MFS',
    'FlipAngle'             : 'FA',
    'PhaseEncodingDirection': 'PED',
    'PhaseEncodingSteps'    : 'PES',
    'EchoTrainLength'       : 'ETL',
    'PixelBandwidth'        : 'PBW',
    'ScanningSequence'      : 'SSEQ',
    'SequenceVariant'       : 'SEQV',
    'MRAcquisitionType'     : 'MRAT',
    'EffectiveEchoSpacing'  : 'EES',
    }

BASE_IMAGING_PARAMETER_NAMES = list(BASE_IMAGING_PARAMS_DICOM_TAGS.keys())


# Constant dicom Identifiers used to extract dicom headers
HEADER_TAGS = {
    "image_header_info": [0x29, 0x1010],
    "series_header_info": [0x29, 0x1020],
}
SLICE_MODE = {
    "1": "sequential",
    "2": "interleaved",
    "4": "singleshot"
}
SSDict = {
    "SE": "Spin Echo",
    "IR": "Inversion Recovery",
    "GR": "Gradient Recalled",
    "EP": "Echo Planar",
    "RM": "Research Mode"
}
SVDict = {
    "SK": "segmented k-space",
    "MTC": "magnetization transfer contrast",
    "SS": "steady state",
    "TRSS": "time reversed steady state",
    "SP": "spoiled",
    "MP": "MAG prepared",
    "OSP": "oversampling phase",
    "NONE": "no sequence variant"
}

PAT = {
    "1": 'None',
    "2": 'Grappa',
    "3": 'Sense'
}

SHIM = {
    "1": 'tune_up',
    "2": 'standard',
    "4": 'advanced'
}

ATDict = ["2D", "3D"]

allowed_values_PED = list(['i', 'j', 'k',
                           'i-', 'j-', 'k-',
                           'ROW', 'COL'])
