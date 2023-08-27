import numpy as np
import pytest
from hypothesis import given, assume
from hypothesis.strategies import text, dictionaries, floats
from protocol import BaseSequence, BaseParameter  # Replace with actual import path
from protocol.base import NumericParameter
from protocol.utils import slugify


# Test initialization and defaults
def test_initialization_defaults():
    sequence = BaseSequence()
    assert sequence.name == 'Sequence'
    assert len(sequence.params) == 0
    assert sequence.path is None
    assert sequence.subject_id is None
    assert sequence.session_id is None
    assert sequence.run_id is None
    assert sequence._mutable


# Test adding parameters
def test_add_parameter():
    parameter = NumericParameter(name="TestParameter", value=123)
    sequence = BaseSequence()
    sequence.add(parameter)
    assert parameter.name in sequence.params
    assert sequence[parameter.name] == parameter


def test_add_non_baseparameter():
    sequence = BaseSequence()
    with pytest.raises(ValueError):
        sequence.add("invalid_parameter")


# Test setting and getting session info
def test_session_info():
    sequence = BaseSequence()
    sequence.set_session_info("subject_123", "session_456", "run_789")
    subject_id, session_id, run_id = sequence.get_session_info()
    assert subject_id == "subject_123"
    assert session_id == "session_456"
    assert run_id == "run_789"


# Test getting parameters
@given(parameter_name=text(), parameter_value=floats())
def test_get_parameter(parameter_name, parameter_value):
    sequence = BaseSequence()
    if np.isnan(parameter_value):
        with pytest.raises(ValueError):
            parameter = NumericParameter(name=parameter_name,
                                     value=parameter_value)
        return
    else:
        parameter = NumericParameter(name=parameter_name,
                                     value=parameter_value)
    sequence.add(parameter)
    retrieved_parameter = sequence[parameter_name]
    assert retrieved_parameter == parameter


def test_get_non_existing_parameter():
    sequence = BaseSequence()
    with pytest.raises(KeyError):
        retrieved_parameter = sequence["NonExistingParameter"]
    default_value = sequence.get("NonExistingParameter", "DefaultValue")
    assert default_value == "DefaultValue"


# Test equivalence and compliance
@given(params_dict=dictionaries(text(), floats()))
def test_equivalence_and_compliance(params_dict):
    assume(all(not np.isnan(value) for value in params_dict.values()))
    sequence1 = BaseSequence()
    sequence1.add(NumericParameter(name=name, value=value) for name, value in params_dict.items())
    sequence2 = BaseSequence()
    sequence2.add(NumericParameter(name=name, value=value) for name, value in params_dict.items())
    assert sequence1 == sequence2
    compliant, non_compliant_params = sequence1.compliant(sequence2)
    assert compliant
    assert len(non_compliant_params) == 0


# Test parameter deletion and iterable behavior
@given(parameter_name=text(), parameter_value=floats())
def test_deletion_and_iterable(parameter_name, parameter_value):
    assume(not np.isnan(parameter_value))
    sequence = BaseSequence()
    parameter = NumericParameter(name=parameter_name, value=parameter_value)
    sequence.add(parameter)
    assert parameter_name in sequence
    del sequence[parameter_name]
    assert parameter_name not in sequence


# Test string representation
@given(parameter_name1=text(), parameter_value1=floats(), parameter_name2=text(), parameter_value2=floats())
def test_string_representation(parameter_name1, parameter_value1,
                               parameter_name2, parameter_value2):
    sequence = BaseSequence()

    if (not parameter_name1) or np.isnan(parameter_value1):
        with pytest.raises(ValueError):
            parameter1 = NumericParameter(name=parameter_name1,
                                          value=parameter_value1)
        return
    else:
        parameter1 = NumericParameter(name=parameter_name1,
                                      value=parameter_value1)

    if (not parameter_name2) or np.isnan(parameter_value2):
        with pytest.raises(ValueError):
            parameter2 = NumericParameter(name=parameter_name2,
                                          value=parameter_value2)
        return
    else:
        parameter2 = NumericParameter(name=parameter_name2,
                                      value=parameter_value2)

    sequence.add(parameter1)
    sequence.add(parameter2)
    if parameter_name1 == parameter_name2:
        assert str(sequence) == f"Sequence({slugify(parameter_name1)}={parameter_value2})"
    else:
        try:
            assert str(sequence) == f"Sequence({slugify(parameter_name1)}={parameter_value1},{slugify(parameter_name2)}={parameter_value2})"
        except AssertionError:
            assert str(sequence) == f"Sequence({slugify(parameter_name2)}={parameter_value2},{slugify(parameter_name1)}={parameter_value1})"
