
from protocol.base import BaseParameter
from protocol.config import BASE_IMAGING_PARAMS_DICOM_TAGS as DICOM_TAGS, \
    Unspecified
import pydicom
from typing import Optional

def get_dicom_param_value(dicom: pydicom.FileDataset,
                            name: str,
                            not_found_value=None):
    """
    Extracts value from dicom metadata looking up the corresponding HEX tag
    in DICOM_TAGS

    Parameters
    ----------
    dicom : pydicom.FileDataset
        dicom object read from pydicom.read_file

    name : str
        parameter name such as MagneticFieldStrength or Manufacturer

    not_found_value : object
        value to be returned if name is not found

    Returns
    -------
    This method return a value for the given key. If key is not available,
    then returns default value None.
    """
    # TODO: consider name.lower()
    try:
        data = dicom.get(DICOM_TAGS[name], not_found_value)
    except KeyError:
        return not_found_value

    if data:
        return data.value
    else:
        return not_found_value


def parse_csa_params(dicom: pydicom.FileDataset,
                     not_found_value=None
                     ) -> dict:
    """
    Returns params parsed from private CSA header from Siemens scanner exported DICOM

    Parameters
    ----------
    dicom : pydicom.FileDataset
        dicom object read from pydicom.read_file

    not_found_value : object
        value to be returned if a parameter is not found

    Returns
    -------
    dict
        Contains PED, multi-slice mode, iPAT and shim_mode

    """
    csa_header = csareader.read(get_header(dicom, 'series_header_info'))
    items = utils.safe_get(csa_header, 'tags.MrPhoenixProtocol.items')
    if items:
        text = items[0]
    else:
        raise AttributeError('CSA Header exists, but xProtocol is missing')

    slice_code = get_csa_props("sKSpace.ucMultiSliceMode", text)
    slice_mode = config.SLICE_MODE.get(slice_code, not_found_value)

    ipat_code = get_csa_props("sPat.ucPATMode", text)
    ipat = config.PAT.get(ipat_code, not_found_value)

    shim_code = get_csa_props("sAdjData.uiAdjShimMode", text)
    shim = config.SHIM.get(shim_code, not_found_value)

    ped = get_phase_encoding(dicom, csa_header)

    values = {'MultiSliceMode': slice_mode,
              'ipat': ipat,
              'shim': shim,
              'PhaseEncodingDirection': ped}

    return csa_header, values


def get_csa_props(parameter, corpus):
    """Extract parameter code from CSA header text

    we want 0x1 from e.g.
    sAdjData.uiAdjShimMode                = 0x1
    """
    index = corpus.find(parameter)
    if index == -1:
        return -1

    shift = len(parameter)+6
    if index + shift > len(corpus):
        print(f"#WARNING: {parameter} in CSA too short: '{corpus[index:]}'")
        return -1

    # 6 chars after parameter text, 3rd value
    param_val = corpus[index:index + shift]
    code_parts = re.split('[\t\n]', param_val)
    if len(code_parts) >= 3:
        return code_parts[2]

    # if not above, might look like:
    # sAdjData.uiAdjShimMode                = 0x1

    # this runs multiple times on every dicom
    # regexp is expesive? dont use unless we need to
    match = re.search(r'=\s*([^\n]+)', corpus[index:])
    if match:
        match = match.groups()[0]
        # above is also a string. dont worry about conversion?
        # match = int(match, 0)  # 0x1 -> 1
        return match

    # couldn't figure out
    return -1


def get_effective_echo_spacing(dicom: pydicom.FileDataset,
                               not_found_value=Unspecified
                               ) -> Optional[float]:
    """
    Calculates effective echo spacing in sec.
    * For Siemens
    Effective Echo Spacing (s) =
    (BandwidthPerPixelPhaseEncode * MatrixSizePhase)^-1

    * For Philips
    echo spacing (msec) =
     1000*water-fat shift (per pixel)/(water-fat shift(in Hz)*echo_train_length)

    Parameters
    ----------
    dicom : pydicom.FileDataset

    Returns
    -------
    float value for effective echo spacing
    """

    bwp_phase_encode = get_dicom_param_value(dicom, 'PixelBandwidth')
    phase_encoding = get_dicom_param_value(dicom, 'PhaseEncodingSteps')

    if (bwp_phase_encode is None) or (phase_encoding is None):
        return not_found_value
    denominator = (bwp_phase_encode * phase_encoding)
    if denominator:
        value = 1000 / denominator
        # Match value to output of dcm2niix
        return value / 1000
    else:
        return not_found_value
