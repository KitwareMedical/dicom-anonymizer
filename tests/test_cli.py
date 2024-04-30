import pytest
import pydicom
import sys

from unittest.mock import patch

from dicomanonymizer.anonymizer import main
from dicomanonymizer.simpledicomanonymizer import empty


@pytest.fixture
def a_simple_dataset():
    dataset = pydicom.Dataset()
    dataset.add_new((0x0010, 0x0010), "PN", "Test Name")
    return dataset


@pytest.fixture
def an_anonymize_mock():
    with patch("dicomanonymizer.anonymizer.anonymize") as anonymize_mock:
        yield anonymize_mock


def test_basic_cli(an_anonymize_mock):
    sys.argv = ['cmd', 'input', 'output']
    main()
    an_anonymize_mock.assert_called_once_with("input", "output", {}, True)


def test_simple_tag_arguments(an_anonymize_mock):
    sys.argv = ['cmd', 'input', 'output', '-t', '(0x0010, 0x0010)', 'empty']
    main()
    an_anonymize_mock.assert_called_once_with("input", "output", {(0x0010, 0x0010): empty}, True)


def test_complex_tag_arguments(an_anonymize_mock, a_simple_dataset):
    sys.argv = ['cmd', 'input', 'output', '-t', '(0x0010, 0x0010)', 'replace_with_value', 'Replaced']
    main()
    # Call the function created by our arguments to make sure it works as expected
    an_anonymize_mock.call_args.args[2][(0x0010, 0x0010)](a_simple_dataset, (0x0010, 0x0010))
    assert a_simple_dataset[(0x0010, 0x0010)].value == "Replaced"


@patch("builtins.open")
def test_dictionnay_argument(an_open_mock, an_anonymize_mock):
    class FakeFile:
        def read(self):
            return '{"(0x0010, 0x0010)": "empty"}'

    an_open_mock.return_value.__enter__.return_value = FakeFile()
    sys.argv = ['cmd', 'input', 'output', '--dictionary', 'whatever.json']
    main()
    an_anonymize_mock.assert_called_once_with("input", "output", {(0x0010, 0x0010): empty}, True)


@patch("builtins.open")
def test_complex_dictionnary_argument(an_open_mock, an_anonymize_mock, a_simple_dataset):
    class FakeFile:
        def read(self):
            return '{"(0x0010, 0x0010)": {"action":"regexp", "find": "Name", "replace": "Replaced"}}'

    an_open_mock.return_value.__enter__.return_value = FakeFile()
    sys.argv = ['cmd', 'input', 'output', '--dictionary', 'whatever.json']
    main()
    # Call the function created by our arguments to make sure it works as expected
    an_anonymize_mock.call_args.args[2][(0x0010, 0x0010)](a_simple_dataset, (0x0010, 0x0010))
    assert a_simple_dataset[(0x0010, 0x0010)].value == "Test Replaced"


def test_unrecognized_action_gives_helpful_error():
    sys.argv = ['cmd', 'input', 'output', '-t', '(0x0010, 0x0010)', 'wrong_action']
    try:
        main()
    except ValueError as e:
        assert "not recognized" in str(e)


def test_wrong_number_of_arguments_gives_helpful_error():
    sys.argv = ['cmd', 'input', 'output', '-t', '(0x0010, 0x0010)', 'replace_with_value']
    try:
        main()
    except ValueError as e:
        assert "number of arguments" in str(e)
