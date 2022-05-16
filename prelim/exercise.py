#!/usr/bin/env python3
"""Preliminary exercises for Part IIA Project GF2."""
import sys
from mynames import MyNames


def open_file(path):
    """Open and return the file specified by path."""
    # Open a file
    try:
        fo = open(path, "r+")
        print("Name of the file: ", fo.name)

        return fo

    except IOError:
        print("Error: can't find file or read data")

    else:
        print("Written content in the file successfully")


def get_next_character(input_file):
    """Read and return the next character in input_file."""
    char = input_file.read(1)
    if char == "":
        return None
    else:
        return char


def get_next_non_whitespace_character(input_file):
    """Seek and return the next non-whitespace character in input_file."""
    while True:
        char = input_file.read(1)
        if char.isspace():
            continue
        elif char == "":
            return None
        else:
            return char


def get_next_number(input_file):
    """Seek the next number in input_file.

    Return the number (or None) and the next non-numeric character.
    """
    # find start of number
    while True:
        char = input_file.read(1)
        if char.isdigit():
            num = char
            break
        elif char == "":
            return None

    # find next non_digit
    while True:
        char = input_file.read(1)
        if char.isdigit():
            num = num + char
        else:
            return [num, char]


def get_next_name(input_file):
    """Seek the next name string in input_file.

    Return the name string (or None) and the next non-alphanumeric character.
    """
    # find start of name
    while True:
        char = input_file.read(1)
        if char.isalpha():
            name = char
            break
        elif char == "":
            return None

    # find next non_alnum
    while True:
        char = input_file.read(1)
        if char.isalnum():
            name = name + char
        else:
            return [name, char]


def main():
    """Preliminary exercises for Part IIA Project GF2."""
    # Check command line arguments
    arguments = sys.argv[1:]
    if len(arguments) != 1:
        print("Error! One command line argument is required.")
        sys.exit()

    else:

        print("\nNow opening file...")
        # Print the path provided and try to open the file for reading
        file_path = arguments[0]
        print(file_path)
        fo = open_file(file_path)

        print("\nNow reading file...")
        # Print out all the characters in the file, until the end of file
        while True:
            char = get_next_character(fo)
            if char is None:
                break
            print(char, end="")

        print("\nNow skipping spaces...")
        # Print out all the characters in the file, without spaces
        fo.seek(0)
        while True:
            char = get_next_non_whitespace_character(fo)
            if char is None:
                break
            print(char, end="")

        print("\nNow reading numbers...")
        # Print out all the numbers in the file
        fo.seek(0)
        while True:
            num = get_next_number(fo)
            if num is None:
                break
            print(num)

        print("\nNow reading names...")
        # Print out all the names in the file
        fo.seek(0)
        while True:
            name = get_next_name(fo)
            if name is None:
                break
            print(name)

        print("\nNow censoring bad names...")
        # Print out only the good names in the file
        name = MyNames()
        bad_name_ids = [
            name.lookup("Terrible"),
            name.lookup("Horrid"),
            name.lookup("Ghastly"),
            name.lookup("Awful"),
        ]
        fo.seek(0)
        while True:
            name1 = get_next_name(fo)
            if name1 is None:
                break

            name_generated = name.lookup(name1[0])
            if name_generated not in bad_name_ids:
                print(name.get_string(name_generated))


if __name__ == "__main__":
    main()
