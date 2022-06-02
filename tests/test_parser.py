"""Tests the parser module"""
from names import Names
from parse import Parser
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
import pytest
from unittest import mock
from unittest.mock import DEFAULT
from unittest.mock import patch, mock_open
import logging

# creds to Niko for this mock
def new_scanner(file_text):
    """Return a new scanner instance."""
    # Mocking open file as string even though path expected
    mocked_open_function = mock_open(read_data=file_text)

    with patch("builtins.open", mocked_open_function) as mock_file:
        names_instance = Names()
        scanner_logger = logging.getLogger("scanner")
        return Scanner("temp_dir", names_instance, scanner_logger)


# helper method to make parser to work with
def return_parser(test_text):
    scanner = new_scanner(test_text)
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    parser_logger = logging.getLogger("parser")
    return Parser(names, devices, network, monitors, scanner, parser_logger)


# this replaces all the methods within the parser
@patch.multiple(
    "parse.Parser",
    make_monitor=DEFAULT,
    create_conn=DEFAULT,
    device=DEFAULT,
    gate_devices=DEFAULT,
    dtype_devices=DEFAULT,
    switch_devices=DEFAULT,
    clock_devices=DEFAULT,
    input_number=DEFAULT,
    device_name=DEFAULT,
)
def test_parse_network(**mocks):
    """
    This function checks that the parse_network method works
    Note that function calls within are patched with a mock as they
    are not being tested. Calls to them can be tested however
    """
    test_file = """DEVICES{
    DTYPE dtype;
    SWITCH sw1(0), sw2(1), sw3(0);
    CLOCK clock(10);
}
CONNECT{
    sw1 => dtype.SET;
}
MONITOR{
    dtype.Q;
}
END"""
    parser = return_parser(test_file)
    assert parser.parse_network()


@patch("parse.Parser.error")
@pytest.mark.parametrize(
    "text,error",
    [
        ("dtype", "SEMICOLON_EXPECTED"),
        ("dtype.;", "OUTPUT_PIN_EXPECTED"),
        (";", "DEVICE_NAME_EXPECTED"),
    ],
)
def test_make_monitor_errors(error_mock, text, error):
    """
    Function to test make_monitor method of parser
    """
    parser = return_parser(text)
    parser.symbol = parser.scanner.get_symbol()
    parser.make_monitor()
    error_mock.assert_called_with(error)


@patch("parse.Parser.error")
def test_make_monitor_basic(error_mock):
    """
    Function to tetst make_monitor works by itself
    """
    text = "dtype.Q;"
    parser = return_parser(text)
    parser.symbol = parser.scanner.get_symbol()
    parser.make_monitor()

    assert error_mock.not_called


@patch("parse.Parser.error")
@pytest.mark.parametrize(
    "text,error",
    [
        ("sw1 => dtype.SET", "SEMICOLON_EXPECTED"),
        ("dtype1. => dtype.SET;", "OUTPUT_PIN_EXPECTED"),
        (" ;", "DEVICE_NAME_EXPECTED"),
        ("sw1 => ;", "DEVICE_NAME_EXPECTED"),
        ("sw1 dtype.SET;", "RIGHT_ARROW_EXPECTED"),
        ("sw1 => dtype;", "INPUT_SPECIFICATION_EXPECTED"),
        ("sw1 => dtype.FOO;", "NOT_VALID_INPUT"),
    ],
)
def test_create_conn_errors(error_mock, text, error):
    """
    Function to test make_monitor method of parser
    """
    parser = return_parser(text)
    parser.symbol = parser.scanner.get_symbol()
    parser.create_conn()
    # note, no assertion of being called once as error skipping is not functional
    error_mock.assert_any_call(error)


@patch("parse.Parser.error")
@pytest.mark.parametrize(
    "text",
    [("sw1 => dtype.SET;"), ("dtype.Q => gate.I1;")],
)
def test_create_conn_clean(error_mock, text):
    """
    Function to test make_monitor method of parser
    """
    parser = return_parser(text)
    parser.symbol = parser.scanner.get_symbol()
    parser.create_conn()
    # note, no assertion of being called once as error skipping is not functional
    error_mock.assert_not_called()


@patch("parse.Parser.error")
def test_device_errors(error_mock):
    """
    Function to test error handling of device method
    """
    text = "FOO"
    parser = return_parser(text)
    parser.symbol = parser.scanner.get_symbol()
    parser.device()
    error_mock.assert_called_with("DEVICE_TYPE_NOT_DECLARED")


@patch.multiple(
    "parse.Parser",
    clock_devices=DEFAULT,
    switch_devices=DEFAULT,
    dtype_devices=DEFAULT,
    gate_devices=DEFAULT,
    error=DEFAULT,
)
@pytest.mark.parametrize(
    "text", ["CLOCK", "SWITCH", "DTYPE", "AND", "NAND", "OR", "NOR"]
)
def test_device_clean(text, **mocks):
    parser = return_parser(text)
    parser.symbol = parser.scanner.get_symbol()
    parser.device()
    parser.error.assert_not_called()


@patch.multiple(
    "parse.Parser",
    input_number=DEFAULT,
    error=DEFAULT,
)
@pytest.mark.parametrize(
    "text,test_error",
    [
        ("and10);", "LEFT_BRACKET_EXPECTED"),
        ("and(10;", "RIGHT_BRACKET_EXPECTED"),
        ("and(10), and210);", "LEFT_BRACKET_EXPECTED"),
        ("and(10), and2(10 ;", "RIGHT_BRACKET_EXPECTED"),
        ("and(10)", "SEMICOLON_EXPECTED"),
        ("and(10), and2(10)", "SEMICOLON_EXPECTED"),
    ],
)
def test_gate_devices_errors(text, test_error, **mocks):
    parser = return_parser(text)
    parser.gate_devices(mock.Mock())
    parser.error.assert_any_call(test_error)


@patch("parse.Parser.error")
@pytest.mark.parametrize("text,test_error", [("dtype", "SEMICOLON_EXPECTED")])
def test_dtype_devices_errors(error_mock, text, test_error):
    parser = return_parser(text)
    parser.gate_devices(mock.Mock())
    error_mock.assert_any_call(test_error)


@patch("parse.Parser.error")
def test_dtype_devices_clean(error_mock):

    parser = return_parser("dtype;")
    parser.dtype_devices(mock.Mock())
    error_mock.assert_not_called()


@patch("parse.Parser.error")
@pytest.mark.parametrize(
    "text,test_error",
    [
        ("sw10);", "LEFT_BRACKET_EXPECTED"),
        ("sw(10);", "INVALID_STATE_OF_SWITCH"),
        ("sw(0;", "RIGHT_BRACKET_EXPECTED"),
        ("sw1(1), sw10);", "LEFT_BRACKET_EXPECTED"),
        ("sw1(1), sw(10);", "INVALID_STATE_OF_SWITCH"),
        ("sw1(1), sw(0;", "RIGHT_BRACKET_EXPECTED"),
        ("sw(0)", "SEMICOLON_EXPECTED"),
    ],
)
def test_switch_devices_errors(error_mock, text, test_error):
    parser = return_parser(text)
    parser.switch_devices(mock.Mock())
    error_mock.assert_any_call(test_error)


@patch("parse.Parser.error")
@pytest.mark.parametrize(
    "text", ["sw(1);", "sw(1), sw1(0);", "sw(1),sw2(1),sw3(0);"]
)
def test_switch_devices_clean(error_mock, text):
    parser = return_parser(text)
    parser.switch_devices(mock.Mock())
    error_mock.assert_not_called()


@patch("parse.Parser.error")
@pytest.mark.parametrize(
    "text,test_error",
    [
        ("clock10);", "LEFT_BRACKET_EXPECTED"),
        ("clock(-6);", "INVALID_CYCLE_VALUE"),
        ("clock(0;", "RIGHT_BRACKET_EXPECTED"),
        ("clock1(1), clock10);", "LEFT_BRACKET_EXPECTED"),
        ("clock1(1), clock(0;", "RIGHT_BRACKET_EXPECTED"),
        ("clock1(2), clock(-6);", "INVALID_CYCLE_VALUE"),
        ("clock(0)", "SEMICOLON_EXPECTED"),
    ],
)
def test_clock_devices_errors(error_mock, text, test_error):
    parser = return_parser(text)
    parser.clock_devices(mock.Mock())
    print(error_mock.call_args_list)
    error_mock.assert_any_call(test_error)
