"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""
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

    def __init__(self, path, names, logger):
        """Open specified file and initialise reserved words and IDs."""
        self.names = names

        # <--- Create Symbol Types --->
        self.symbol_type_list = [
            self.COMMA,
            self.SEMICOLON,
            self.DOT,
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
        ] = range(16)

        # <--- Define Symbols Within Types --->
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

        # <--- Create ID's and populate names list --->
        [
            self.COMMA_ID,
            self.SEMICOLON_ID,
            self.DOT_ID,
            self.EQUALS_ID,
            self.RIGHT_ARROW_ID,
        ] = self.names.lookup(self.punctuation_list)

        [self.LEFT_BRACKET_ID, self.RIGHT_BRACKET_ID] = self.names.lookup(
            self.bracket_list
        )

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

        [self.DATA_ID, self.CLK_ID, self.SET_ID, self.CLEAR_ID] = self.names.lookup(
            self.input_pin_list
        )

        [self.Q_ID, self.BAR_ID] = self.names.lookup(self.output_pin_list)

        [self.LEFT_CURLY_BRACKET_ID, self.RIGHT_CURLY_BRACKET_ID] = self.names.lookup(
            self.curly_bracket_list
        )

        self.current_character = ""

        # Opens the definition file
        self.file = open(path)
        self.logger = logger
        self.logger.info("\nNow reading file...")
        self.logger.info("File name:  " + self.file.name)

    def advance(self) -> None:
        """Read next character and update current character."""
        self.current_character = self.file.read(1)

    def skip_spaces(self) -> None:
        """Assign next non whitespace character to current character."""
        self.advance()
        while self.current_character.isspace():
            self.advance()

    def get_device_name(self) -> tuple[str, str]:
        """Extract the device name in the following seq of characters.

        Assumes that the initial character is a lower case character. Then
        finds the whole device name. Device name ended when a nonalphanumeric
        character is found.
        """
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

    def get_capital_name(self) -> tuple[str, str]:
        """Extract name in sequence of capital characters.

        Assumes that the initial character is an upper case character. Then
        finds the whole uppercase word. Word ended when a non uppercase
        character is found.
        """
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

    def get_number(self) -> tuple[str, str]:
        """Extract number in the next sequence of characters.

        Assumes current character is a number. Finds the whole number.
        Termination occurs when non numeric character is found.
        """
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
        symbol = Symbol()  #
        if self.current_character.isspace():
            self.skip_spaces()  # current character now not whitespace
        # assignment uses if statements as the sequences of char vary
        if self.current_character.islower():  # device name
            device_name = self.get_device_name()[0]
            symbol.type = self.DEVICE_NAME
            [symbol.id] = self.names.lookup([device_name])

        elif (
            self.current_character.isalpha() and self.current_character != "I"
        ):  # keyword which is not input pin
            capital_string = self.get_capital_name()[0]
            if capital_string in self.keywords_list:  # keyword
                symbol.type = self.KEYWORD
                [symbol.id] = self.names.lookup([capital_string])
            elif capital_string in self.gate_name_list:  # gatename
                symbol.type = self.GATE_NAME
                [symbol.id] = self.names.lookup([capital_string])
            elif capital_string in self.output_pin_list:  # output pin
                symbol.type = self.OUTPUT_PIN
                [symbol.id] = self.names.lookup([capital_string])
            elif capital_string in self.input_pin_list:  # input pin
                symbol.type = self.INPUT_PIN
                [symbol.id] = self.names.lookup([capital_string])
            else:  # error
                symbol.type = self.ERROR_NAMES
                [symbol.id] = self.names.lookup([capital_string])

        elif self.current_character == "I":
            # Saves only the input number.
            self.advance()
            if self.current_character.isdigit():
                symbol.type = self.INPUT_NUMBER
                symbol.id = self.get_number()[0]
            else:
                symbol.type = self.ERROR_NAMES

        elif self.current_character.isdigit():
            symbol.id = self.get_number()[0]
            symbol.type = self.NUMBER

        # punctuation
        elif self.current_character == "=":
            self.advance()  # check if next character satisfies =>
            if self.current_character == ">":
                symbol.type = self.RIGHT_ARROW
                symbol.id = self.RIGHT_ARROW_ID
                self.advance()
            else:
                symbol.type = self.ERROR_NAMES
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
        try:
            self.logger.debug(f"{symbol.type}, {self.names.get_name_string(symbol.id)}")
        except:
            self.logger.debug(f"{symbol.type}, {symbol.id}")

        return symbol


# Run file and simple test
# names_instance = Names()

# path_definition = "definitions/circuit.def"
# a_scanner = Scanner(path_definition, names_instance)
# a_scanner.advance()
# for i in range(70):
#     symbol1 = a_scanner.get_symbol()
#     if symbol1.type == 16:
#         break
#     print("ID, string")
#     print(symbol1.type, names_instance.get_name_string(symbol1.id))
#     print("---")
