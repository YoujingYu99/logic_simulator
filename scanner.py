"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""
from winreg import KEY_WOW64_32KEY
from names import Names


class Symbol:

    """Encapsulate a symbol and store its properties.

    Parameters
    ----------
    No parameters.

    Public methods
    --------------
    No public methods.
    """

    def __init__(self):
        """Initialise symbol properties."""
        self.type = None
        self.id = None


class Scanner:

    """Read circuit definition file and translate the characters into symbols.

    Once supplied with the path to a valid definition file, the scanner
    translates the sequence of characters in the definition file into symbols
    that the parser can use. It also skips over comments and irrelevant
    formatting characters, such as spaces and line breaks.

    Parameters
    ----------
    path: path to the circuit definition file.
    names: instance of the names.Names() class.

    Public methods
    -------------
    get_symbol(self): Translates the next sequence of characters into a symbol
                      and returns the symbol.
    """

    def __init__(self, path, names):
        """Open specified file and initialise reserved words and IDs."""
        self.names = names

        # Initialises a list of symbol types (including EOF for the end of the
        # file)
        self.symbol_type_list = [
            self.COMMA,
            self.SEMICOLON,
            self.DOT,
            self.EQUALS,
            self.RIGHT_ARROW,
            self.BRACKET,
            self.CURLY_BRACKET,
            self.OUTPUT_PIN,
            self.INPUT_PIN,
            self.INPUT_NUMBER,
            self.CLOCK_CYCLES,
            self.NUMBER,
            self.KEYWORD,
            self.GATE_NAME,
            self.DEVICE_NAME,
            self.ERROR_NAMES,
            self.EOF,
        ] = range(17)

        self.punctuation_list = [",", ";", ".", "=", "=>"]

        self.keywords_list = ["DEVICES", "CONNECT", "MONITOR", "END"]

        self.gate_name_list = [
            "CLOCK",
            "SWITCH",
            "AND",
            "NAND",
            "OR",
            "NOR",
            "DTYPE",
            "XOR",
        ]

        self.output_pin_list = ["Q", "BAR"]

        self.input_pin_list = ["DATA", "CLK", "SET", "CLEAR"]

        self.bracket_list = ["(", ")"]

        self.curly_bracket_list = ["{", "}"]

        [
            self.COMMA_ID,
            self.SEMICOLON_ID,
            self.DOT_ID,
            self.EQUALS_ID,
            self.RIGHT_ARROW_ID,
        ] = self.names.lookup(self.punctuation_list)

        [
            self.DEVICES_ID,
            self.CONNECT_ID,
            self.MONITOR_ID,
            self.END_ID,
        ] = self.names.lookup(self.keywords_list)

        [
            self.CLOCK_ID,
            self.SWITCH_ID,
            self.AND_ID,
            self.NAND_ID,
            self.OR_ID,
            self.NOR_ID,
            self.DTYPE_ID,
            self.XOR_ID,
        ] = self.names.lookup(self.gate_name_list)

        [self.DATA_ID, self.CLK_ID, self.SET_ID,
            self.CLEAR_ID] = self.names.lookup(self.input_pin_list)

        [self.Q_ID, self.BAR_ID] = self.names.lookup(self.output_pin_list)

        [self.LEFT_BRACKET_ID, self.RIGHT_BRACKET_ID] = self.names.lookup(
            self.bracket_list
        )

        [self.LEFT_CURLY_BRACKET_ID,
            self.RIGHT_CURLY_BRACKET_ID] = self.names.lookup(
                                                self.curly_bracket_list)

        self.current_character = "*"

        # Opens the definition file
        self.file = open(path)
        print("\nNow reading file...")
        print("File name:  " + self.file.name)

    def advance(self):
        """Assign next character to current current character."""
        self.current_character = self.file.read(1)

    def skip_spaces(self):
        """Assign next non whitespace character to current character."""
        self.advance()

        while self.current_character.isspace():
            self.advance()

    def get_name(self):
        """get_name is similar to get_next_name in the preliminary exercises,
        except that it now assumes the current character is a letter, returns
        only the name string and places the next nonalphanumeric character
        in current_character"""

    def get_right_arrow(self):
        """Assumes that the current character is an equals"""

    def get_device_name(self):
        """Assumes that the initial character is a lower case character. Then
        finds the whole device name. Device name ended when a nonalphanumberic
        character is found."""
        char = "a"
        name_string = ""

        name_string += self.current_character
        while char.isalnum():
            self.advance()
            char = self.current_character
            if char.isalnum():
                name_string += char
            else:
                return (name_string, char)

    def get_capital_name(self):
        """Assumes that the initial character is a upper case character. Then
        finds the whole uppercase word. Word ended when a non uppercase
        character is found."""
        char = "A"
        name_string = ""

        name_string += self.current_character
        while char.isupper():
            self.advance()
            char = self.current_character
            if char.isupper():
                name_string += char
            else:
                return (name_string, char)

    def get_number(self):
        """Assumes current character is a number. Finds the whole number.
        Termination occurs when non numeric character is found."""
        char = "1"
        number_string = ""

        number_string += self.current_character
        while char.isnumeric():
            self.advance()
            char = self.current_character
            if char.isnumeric():
                number_string += char
            else:
                return (number_string, char)

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""

        symbol = Symbol()
        if self.current_character == "*":
            self.skip_spaces()  # current character now not whitespace
        if self.current_character.isspace():
            self.skip_spaces()  # current character now not whitespace

        if self.current_character.islower():  # device name
            device_name, char = self.get_device_name()
            symbol.type = self.DEVICE_NAME
            [symbol.id] = self.names.lookup([device_name])

        elif (
            self.current_character.isalpha() and self.current_character != "I"
        ):  # keyword which is not input pin
            capital_string, char = self.get_capital_name()
            if capital_string in self.keywords_list:  # keyword
                symbol.type = self.KEYWORD
                [symbol.id] = self.names.lookup([capital_string])
            elif capital_string in self.gate_name_list:  # gatename
                symbol.type = self.GATE_NAME
                [symbol.id] = self.names.lookup([capital_string])
            elif capital_string in self.output_pin_list:  # output pin
                symbol.type = self.OUTPUT_PIN
                [symbol.id] = self.names.lookup([capital_string])
            elif capital_string in self.input_pin_list:
                symbol.type = self.INPUT_PIN
                [symbol.id] = self.names.lookup([capital_string])
            else:  # error
                symbol.type = self.ERROR_NAMES
                [symbol.id] = self.names.lookup([capital_string])

        elif self.current_character == "I":
            # Saves only the input number.
            self.advance()
            if self.current_character.isnumeric():
                number_string, char = self.get_number()
                symbol.type = self.INPUT_NUMBER
                [symbol.id] = self.names.lookup([number_string])
            else:
                symbol.type = self.ERROR_NAMES
                [symbol.id] = self.names.lookup([number_string])

        elif self.current_character.isnumeric():
            number_string, char = self.get_number()
            symbol.type = self.NUMBER
            [symbol.id] = self.names.lookup([number_string])

        elif self.current_character.isdigit():  # number
            symbol.id = self.get_number()
            symbol.type = self.NUMBER

        # punctuation
        elif self.current_character == "=":
            # LL(1)
            self.advance()
            if self.current_character == ">":
                symbol.type = self.RIGHT_ARROW
                symbol.id = self.RIGHT_ARROW_ID
                self.advance()
            else:
                symbol.type = self.EQUALS
        elif self.current_character == ".":
            symbol.type = self.DOT
            [symbol.id] = self.names.lookup([self.current_character])
            self.advance()
        elif self.current_character == ",":
            symbol.type = self.COMMA
            [symbol.id] = self.names.lookup([self.current_character])
            self.advance()
        elif self.current_character == ";":
            symbol.type = self.SEMICOLON
            [symbol.id] = self.names.lookup([self.current_character])
            self.advance()
        elif self.current_character == "(":
            symbol.type = self.BRACKET
            [symbol.id] = self.names.lookup([self.current_character])
            self.advance()
        elif self.current_character == ")":
            symbol.type = self.BRACKET
            [symbol.id] = self.names.lookup([self.current_character])
            self.advance()
        elif self.current_character == "{":
            symbol.type = self.CURLY_BRACKET
            [symbol.id] = self.names.lookup([self.current_character])
            self.advance()
        elif self.current_character == "}":
            symbol.type = self.CURLY_BRACKET
            [symbol.id] = self.names.lookup([self.current_character])
            self.advance()

        # end of file
        elif self.current_character == "":
            symbol.type = self.EOF
        else:  # not a valid character
            self.advance()

        return symbol


names_instance = Names()

path_definition = "definitions/circuit.def"
a_scanner = Scanner(path_definition, names_instance)

for i in range(70):
    symbol1 = a_scanner.get_symbol()
    if symbol1.type == 16:
        break
    print("ID, string")
    print(symbol1.type, names_instance.get_name_string(symbol1.id))
    print("---")
