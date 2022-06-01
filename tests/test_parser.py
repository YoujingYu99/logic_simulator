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
@pytest.mark.parametrize("text,error", [("dtype", "SEMICOLON_EXPECTED")])
def test_make_monitor(error_mock, text, error):
    """
    Function to test make_monitor method of parser
    """
    parser = return_parser(text)
    parser.symbol = parser.scanner.get_symbol()
    parser.make_monitor()
    error_mock.assert_called_with(error)
