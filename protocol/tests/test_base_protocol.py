import pytest
from hypothesis import given, settings
from hypothesis import HealthCheck
from hypothesis.strategies import text, lists, dictionaries
from protocol import BaseMRImagingProtocol, \
    ImagingSequence  # Replace with actual import path


# Test initialization and defaults
def test_initialization_defaults():
    protocol = BaseMRImagingProtocol()
    assert protocol.name == 'MRIProtocol'
    assert protocol.category == 'MR'
    assert len(protocol._seq) == 0


# Test adding sequences
def test_add_sequence(sample_dcm):
    sequence = ImagingSequence(dicom=sample_dcm)
    protocol = BaseMRImagingProtocol()
    protocol.add(sequence)
    assert len(protocol._seq) == 1
    assert protocol[sequence.name] == sequence


def test_add_invalid_type():
    with pytest.raises(TypeError):
        protocol = BaseMRImagingProtocol(name="TestProtocol",
                                         category="TestCategory")


def test_add_duplicate_name(sample_dcm):
    protocol = BaseMRImagingProtocol()
    sequence1 = ImagingSequence(name="Sequence1", dicom=sample_dcm)
    sequence2 = ImagingSequence(name="Sequence1", dicom=sample_dcm)
    protocol.add(sequence1)
    with pytest.raises(ValueError):
        protocol.add(sequence2)


# Test protocol emptiness
def test_protocol_emptiness():
    empty_protocol = BaseMRImagingProtocol()
    assert not empty_protocol
    non_empty_protocol = BaseMRImagingProtocol()
    non_empty_protocol.add(ImagingSequence())
    assert non_empty_protocol


# Test getting sequences
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(sequence_name=text())
def test_get_sequence(sequence_name, sample_dcm):
    protocol = BaseMRImagingProtocol()
    sequence = ImagingSequence(name=sequence_name, dicom=sample_dcm)
    protocol.add(sequence)
    retrieved_sequence = protocol[sequence_name]
    assert retrieved_sequence == sequence


def test_get_non_existing_sequence():
    protocol = BaseMRImagingProtocol()
    with pytest.raises(KeyError):
        retrieved_sequence = protocol["NonExistingSequence"]


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
