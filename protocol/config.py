# Do not import anything from protocol modules in this file.
# It will lead to circular imports. Let it be pristine
import logging
import tempfile
from enum import Enum
from pathlib import Path


def configure_logger(log, output_dir, mode='w', level='ERROR'):
    """
    Initiate log files.

    Parameters
    ----------
    log : logging.Logger
        The logger object.
    mode : str, (``'w'``, ``'a'``)
        The writing mode to the log files.
        Defaults to ``'w'``, overwrites previous files.    """

    console_handler = logging.StreamHandler()  # creates the handler
    warn_formatter = '%(filename)s:%(name)s:%(funcName)s:%(lineno)d: %(message)s'
    error_formatter = '%(asctime)s - %(levelname)s - %(message)s'
    if output_dir is None:
        output_dir = tempfile.gettempdir()
    output_dir = Path(output_dir) / '.protocol'
    output_dir.mkdir(parents=True, exist_ok=True)

    warn_file = output_dir / 'warn.log'
    if level == 'WARNING':
        warn = logging.FileHandler(warn_file, mode=mode)
        warn.setLevel(logging.WARN)
        warn.setFormatter(logging.Formatter(warn_formatter))
        log.addHandler(warn)

    # keep only errors on console
    console_handler.setLevel(logging.ERROR)  # sets the handler info
    console_handler.setFormatter(logging.Formatter(error_formatter))
    log.addHandler(console_handler)

    error_file = output_dir / 'error.log'
    error = logging.FileHandler(error_file, mode=mode)
    error.setLevel(logging.ERROR)
    error.setFormatter(logging.Formatter(error_formatter))
    log.addHandler(error)
    return log


class UnspecifiedType(object):
    """Class to denote an unspecified value

    Reasons include:
        - not specified in the original source e.g., DICOM image header
        - enocded as None or similar; or presumed to be default

    We need this to correctly inform the downstream users of the source,
        to prevent them from assigning default values or imputing them another way!
    """


    def __init__(self):
        """constructor"""


    def __str__(self):
        return 'Unspecified'


    def __repr__(self):
        return 'Unspecified'


class InvalidType(UnspecifiedType):
    """Class to denote an invalid value

    Reasons include:
        - not specified in the original source e.g., DICOM image header
        - enocded as None or similar; or presumed to be default

    We need this to correctly inform the downstream users of the source,
        to prevent them from assigning default values or imputing them another way!
    """


    def __init__(self):
        """constructor"""
        super().__init__()


    def __str__(self):
        return 'InvalidType'


    def __repr__(self):
        return 'InvalidType'


Unspecified = UnspecifiedType()
Invalid = InvalidType()

# Constant Dicom Identifiers Used for dataset creation and manipulation
SESSION_INFO_DICOM_TAGS = {
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
    "te"                 : (0x18, 0x81),
    "patient_sex"        : (0x10, 0x40),
    "patient_age"        : (0x10, 0x1010),
    "ContentDate"        : (0x08, 0x0023),
    "ContentTime"        : (0x08, 0x0033),
    }

BASE_IMAGING_PARAMS_DICOM_TAGS = {
    ## Hardware Parameters
    'Manufacturer'                  : (0x08, 0x70),
    'ManufacturersModelName'        : (0x08, 0x1090),
    'SoftwareVersions'              : (0x18, 0x1020),
    'MagneticFieldStrength'         : (0x18, 0x87),
    'ReceiveCoilName'               : (0x18, 0x1250),
    'ReceiveCoilActiveElements'     : (0x51, 0x100F),
    'MRTransmitCoilSequence'        : (0x18, 0x9049),

    ## Sequence Specifics
    'ScanningSequence'              : (0x18, 0x20),
    'SequenceVariant'               : (0x18, 0x21),
    'ScanOptions'                   : (0x18, 0x22),
    'SequenceName'                  : (0x18, 0x24),
    'NonLinearGradientCorrection'   : (0x08, 0x08),
    'MRAcquisitionType'             : (0x18, 0x23),
    'MTState'                       : (0x18, 0x9020),
    'SpoilingState'                 : (0x18, 0x9016),

    ## In-Plane Spatial Encoding
    'ParallelReductionFactorInPlane': (0x18, 0x9069),
    'ParallelAcquisitionTechnique'  : (0x18, 0x9078),
    'PartialFourier'                : (0x18, 0x9081),
    'PartialFourierDirection'       : (0x18, 0x9036),
    'PhaseEncodingDirection'        : (0x18, 0x1312),

    ## Timing Parameters
    'EchoTime'                      : (0x18, 0x81),
    'InversionTime'                 : (0x18, 0x82),
    'DwellTime'                     : (0x19, 0x1018),
    'RepetitionTime'                : (0x18, 0x80),

    ## RF & Contrast Parameters
    'FlipAngle'                     : (0x18, 0x1314),

    ## Slice Acceleration Parameters
    'MultiBandAccelerationFactor'   : (0x43, 0x1083),

    ## Misc Parameters
    'BodyPartExamined'              : (0x18, 0x15),
    'EchoTrainLength'               : (0x18, 0x0091),
    'PixelBandwidth'                : (0x18, 0x95),
    'PhaseEncodingSteps'            : (0x18, 0x89),
    'EchoNumber'                    : (0x18, 0x86),

    ## Session Info
    "PercentPhaseFOV"               : (0x18, 0x0094),
    "PercentSampling"               : (0x18, 0x0093),
    "VariableFlipAngleFlag"         : (0x18, 0x1315),
    "ImageOrientationPatient"       : (0x20, 0x37),
    "SliceThickness"                : (0x18, 0x0050),
    "NumberOfAverages"              : (0x18, 0x0083),
    "AngioFlag"                     : (0x18, 0x0025),
    "ImagingFrequency"              : (0x18, 0x0084),
    "ImagedNucleus"                 : (0x18, 0x0085),
    "SpacingBetweenSlices"          : (0x18, 0x0088),
    "TransmitCoilName"              : (0x18, 0x1251),
    "AcquisitionMatrix"             : (0x18, 0x1310),
    "SAR"                           : (0x18, 0x1316),
    "SliceMeasurementDuration"      : (0x19, 0x100b),
    "GradientMode"                  : (0x19, 0x100f),
    "FlowCompensation"              : (0x19, 0x1011),
    "SliceResolution"               : (0x19, 0x1017),
    "ImagePositionPatient"          : (0x20, 0x32),
    "PatientPosition"               : (0x18, 0x5100),
    "SliceLocation"                 : (0x20, 0x1041),
    "SamplesPerPixel"               : (0x28, 0x0002),
    "PhotometricInterpretation"     : (0x28, 0x0004),
    "Rows"                          : (0x28, 0x0010),
    "Columns"                       : (0x28, 0x0011),
    "PixelSpacing"                  : (0x28, 0x0030),
    "BitsAllocated"                 : (0x28, 0x0100),
    "BitsStored"                    : (0x28, 0x0101),
    "HighBit"                       : (0x28, 0x0102),
    "PixelRepresentation"           : (0x28, 0x0103),
    "SmallestImagePixelValue"       : (0x28, 0x0106),
    "LargestImagePixelValue"        : (0x28, 0x0107),
    "WindowCenter"                  : (0x28, 0x1050),
    "WindowWidth"                   : (0x28, 0x1051),
    "WindowCenterWidthExplanation"  : (0x28, 0x1055),
    "CoilString"                    : (0x51, 0x100f),
    "PATMode"                       : (0x51, 0x1011),
    "PositivePCSDirections"         : (0x51, 0x1013),
    }

ACRONYMS_IMAGING_PARAMETERS = {
    'Manufacturer'                  : 'MFR',
    'ManufacturersModelName'        : 'MMN',
    'SoftwareVersions'              : 'SV',
    'MagneticFieldStrength'         : 'MFS',
    'ReceiveCoilName'               : 'RCN',
    'ReceiveCoilActiveElements'     : 'RCAE',
    'MRTransmitCoilSequence'        : 'MTCS',
    'ScanningSequence'              : 'SSEQ',
    'SequenceVariant'               : 'SEQV',
    'ScanOptions'                   : 'SCOP',
    'SequenceName'                  : 'SQNM',
    'NonLinearGradientCorrection'   : 'NLGC',
    'MRAcquisitionType'             : 'MRAT',
    'MTState'                       : 'MTS',
    'SpoilingState'                 : 'SPLS',
    'ParallelReductionFactorInPlane': 'PRFIP',
    'ParallelAcquisitionTechnique'  : 'PAT',
    'PartialFourier'                : 'PF',
    'PartialFourierDirection'       : 'PFD',
    'PhaseEncodingDirection'        : 'PED',
    'EchoTime'                      : 'TE',
    'InversionTime'                 : 'TI',
    'DwellTime'                     : 'DT',
    'RepetitionTime'                : 'TR',
    'FlipAngle'                     : 'FA',
    'MultiBandAccelerationFactor'   : 'MAF',
    'BodyPartExamined'              : 'BPE',
    'EchoTrainLength'               : 'ETL',
    'PixelBandwidth'                : 'PBW',
    'PhaseEncodingSteps'            : 'PES',
    'ShimMode'                      : 'SHM',
    'ShimSetting'                   : 'SHS',
    'MultiSliceMode'                : 'MSM',
    'EchoNumber'                    : 'EN',
    'PhasePolarity'                 : 'PHPL',
    'PercentPhaseFOV'               : 'PPFOV',
    'PercentSampling'               : 'PS',
    'VariableFlipAngleFlag'         : 'VFAF',
    'ImageOrientationPatient'       : 'IOP',
    'SliceThickness'                : 'ST',
    'NumberOfAverages'              : 'NAV',
    'AngioFlag'                     : 'AF',
    'ImagingFrequency'              : 'IF',
    'ImagedNucleus'                 : 'IN',
    'SpacingBetweenSlices'          : 'SBS',
    'TransmitCoilName'              : 'TCN',
    'AcquisitionMatrix'             : 'ACQM',
    'SAR'                           : 'SAR',
    'SliceMeasurementDuration'      : 'SMD',
    'GradientMode'                  : 'GM',
    'FlowCompensation'              : 'FC',
    'SliceResolution'               : 'SR',
    'ImagePositionPatient'          : 'IPP',
    'PatientPosition'               : 'PP',
    'SliceLocation'                 : 'SL',
    'SamplesPerPixel'               : 'SPP',
    'PhotometricInterpretation'     : 'PI',
    'Rows'                          : 'R',
    'Columns'                       : 'C',
    'PixelSpacing'                  : 'PS',
    'BitsAllocated'                 : 'BA',
    'BitsStored'                    : 'BS',
    'HighBit'                       : 'HB',
    'PixelRepresentation'           : 'PR',
    'SmallestImagePixelValue'       : 'SIPV',
    'LargestImagePixelValue'        : 'LIPV',
    'WindowCenter'                  : 'WC',
    'WindowWidth'                   : 'WW',
    'WindowCenterWidthExplanation'  : 'WCWE',
    'CoilString'                    : 'CS',
    'PATMode'                       : 'PATM',
    'PositivePCSDirections'         : 'PPCSD',
    }

ACRONYMS_SESSION_INFO = {
    "SeriesInstanceUID": "SIUID",
    "PatientName"      : "PN",
    "PatientID"        : "PID",
    "StudyID"          : "SID",
    "SeriesDescription": "SD",
    "SeriesNumber"     : "SN",
    "ProtocolName"     : "PN",
    "SequenceName"     : "SQNM",

    }

BASE_IMAGING_PARAMETER_NAMES = list(BASE_IMAGING_PARAMS_DICOM_TAGS.keys())

# Constant dicom Identifiers used to extract dicom headers
HEADER_TAGS = {
    "image_header_info" : (0x29, 0x1010),
    "series_header_info": (0x29, 0x1020),
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
    "SK"  : "segmented k-space",
    "MTC" : "magnetization transfer contrast",
    "SS"  : "steady state",
    "TRSS": "time reversed steady state",
    "SP"  : "spoiled",
    "MP"  : "MAG prepared",
    "OSP" : "oversampling phase",
    "NONE": "no sequence variant"
    }

PAT = {
    "1": 'Not Selected',
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

# , 'CT', 'PET', 'SPECT', 'US', 'NM', 'MG', 'CR', 'DX', 'OT']
SUPPORTED_IMAGING_MODALITIES = ['MR']


class ProtocolType(Enum):
    INFERRED_FROM_DATASET = 1
    USER_DEFINED = 2
