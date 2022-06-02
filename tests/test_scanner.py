"""Tests for the scanner module."""

import pytest
from unittest.mock import patch, mock_open
from scanner import Scanner
from names import Names
import logging


def new_scanner(file_text):
    """Return a new scanner instance."""
    # Mocking open file as string even though path expected
    mocked_open_function = mock_open(read_data=file_text)

    with patch("builtins.open", mocked_open_function) as mock_file:
        names_instance = Names()
        scanner_logger = logging.getLogger("scanner")
        return Scanner("temp_dir", names_instance, scanner_logger)


def test_advance():
    """Test if the whole file is read."""
    file_string = "name$python hELLO π%right"
    scanner = new_scanner(file_string)
    read_string = ""
    for i in range(len(file_string)):
        scanner.advance()
        char = scanner.current_character
        read_string += char
    assert file_string == read_string


@pytest.mark.parametrize(
    "input_string, expected_string",
    [
        ("name$", ("name", "$")),
        ("python ", ("python", " ")),
        ("hELLO", ("hELLO", "")),
        ("dπ%", ("dπ", "%")),
        ("DEVICE", ("DEVICE", "")),
    ],
)
def test_get_device_name(input_string, expected_string):
    """Test if a whole name string is extracted.

    Assumes that the current character is lower case.
    """
    file_string = input_string
    scanner = new_scanner(file_string)

    device_name = scanner.get_device_name()

    assert device_name == expected_string


@pytest.mark.parametrize(
    "input_string, expected_string",
    [
        ("CAPITAL", ("CAPITAL", "")),
        ("CAPiTAL", ("CAP", "i")),
        ("CAP1TAl", ("CAP", "1")),
    ],
)
def test_get_capital_name(input_string, expected_string):
    """Test if a whole keyname string is extracted.

    Assumes that the current character is upper case.
    """
    file_string = input_string
    scanner = new_scanner(file_string)

    keyword = scanner.get_capital_name()

    assert keyword == expected_string


@pytest.mark.parametrize(
    "input_string, expected_char",
    [
        ("\t", ""),
        ("\n ", ""),
        ("\r ", ""),
        ("\f%", "%"),
        (" ", ""),
        ("  a", "a"),
        ("a  ", "a"),
    ],
)
def test_skip_spaces(input_string, expected_char):
    """Test if the the space chatacters are skipped."""
    file_string = input_string
    scanner = new_scanner(file_string)

    scanner.skip_spaces()
    char = scanner.current_character
    assert char == expected_char


@pytest.mark.parametrize(
    "input_string, expected_string",
    [
        ("13405", ("13405", "")),
        ("2345253fgdfg", ("2345253", "f")),
        ("00001", ("00001", "")),
    ],
)
def test_get_number(input_string, expected_string):
    """Test if a whole number string is extracted.

    Assumes that the current character is a digit.
    """
    file_string = input_string
    scanner = new_scanner(file_string)

    number = scanner.get_number()

    assert number == expected_string


@pytest.mark.parametrize(
    "input_string, expected_string",
    [
        (",", 0),
        (";", 1),
        (".", 2),
        ("=>", 3),
        ("(", 4),
        ("{", 5),
        ("Q", 6),
        ("DATA", 7),
        ("I7", 12),
        ("123456", 10),
        ("DEVICES", 11),
        ("QBAR", 7),
        ("dtypeName", 13),
        ("$$", 14),
        ("", 15),
    ],
)
def test_get_symbol_types(input_string, expected_string):
    """Test if symbol types are correctly extracted."""
    file_string = input_string
    scanner = new_scanner(file_string)

    symbol = scanner.get_symbol()

    assert symbol.type == expected_string


@pytest.mark.parametrize(
    "input_string, expected_string",
    [
        (",", 0),
        (";", 1),
        (".", 2),
        ("=>", 3),
        ("(", 4),
        ("{", 5),
        ("Q", 6),
        ("DATA", 7),
        ("I124", 8),
        ("123456", 10),
        ("DEVICES", 11),
        ("CLOCK", 12),
        ("dtypeName", 13),
        ("$$", 14),
        ("", 15),
    ],
)
def test_get_symbol_types(input_string, expected_string):
    """Test if symbol types are correctly extracted."""
    file_string = input_string
    scanner = new_scanner(file_string)

    symbol = scanner.get_symbol()

    assert symbol.type == expected_string


@pytest.mark.parametrize(
    "input_string, expected_string",
    [
        (",", 0),
        (";", 1),
        (".", 2),
        ("=>", 3),
        ("(", 4),
        (")", 5),
        ("{", 6),
        ("}", 7),
        ("DEVICES", 8),
        ("CLEAR", 17),
        ("QBAR", 13),
        ("1234", 1234),
        ("I13", 38),
    ],
)
def test_get_symbol_id(input_string, expected_string):
    """Test if symbol ids are correctly extracted."""
    file_string = input_string
    scanner = new_scanner(file_string)

    symbol = scanner.get_symbol()

    assert symbol.id == expected_string


def test_column_and_line_count():
    """Test if the column and line counter is correct."""
    file_string = "DEVICES{\n    DTYPE dtype;"
    scanner = new_scanner(file_string)

    symbol = scanner.get_symbol()  # DEVICES
    assert symbol.start_col == 1
    assert symbol.start_line == 1

    symbol = scanner.get_symbol()  # {
    assert symbol.start_col == 8
    assert symbol.start_line == 1

    symbol = scanner.get_symbol()  # DTYPE
    assert symbol.start_col == 5
    assert symbol.start_line == 2

    symbol = scanner.get_symbol()  # dtype
    assert symbol.start_col == 11
    assert symbol.start_line == 2

    symbol = scanner.get_symbol()  # ;
    assert symbol.start_col == 16
    assert symbol.start_line == 2


def test_column_and_line_count():
    """Test if the column and line counter is correct."""
    file_string = "DEVICES{\n    DTYPE dtype;"
    scanner = new_scanner(file_string)

    mocked_open_function = mock_open(read_data=file_string)

    with patch("builtins.open", mocked_open_function) as mock_file:
        error_line = scanner.get_error_line(2, 1)
        assert '    DTYPE dtype;\n^' == error_line
