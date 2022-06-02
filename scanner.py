"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""


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
        self.start_col = None  # show error bar at the start of the symbol
        self.start_line = None


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
        self.current_line = 1
        self.current_col = 0

        # <--- Create Symbol Types --->
        self.symbol_type_list = [
            self.COMMA,
            self.SEMICOLON,
            self.DOT,
            self.RIGHT_ARROW,
            self.BRACKET,
            self.CURLY_BRACKET,
            self.DTYPE_OUTPUT_PIN,
            self.DTYPE_INPUT_PIN,
            self.GATE_PIN,
            self.INPUT_NUMBER,
            self.NUMBER,
            self.KEYWORD,
            self.GATE_NAME,
            self.DEVICE_NAME,
            self.ERROR,
            self.EOF,
        ] = range(16)

        # <--- Define Symbols Within Types --->
        self.punctuation_list = [",", ";", ".", "=>"]

        self.bracket_list = ["(", ")"]

        self.curly_bracket_list = ["{", "}"]

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

        self.dtype_output_pin_list = ["Q", "QBAR"]

        self.dtype_pin_list = ["DATA", "CLK", "SET", "CLEAR"]

        self.gates_pin_list = [
            "I1",
            "I2",
            "I3",
            "I4",
            "I5",
            "I6",
            "I7",
            "I8",
            "I9",
            "I10",
            "I11",
            "I12",
            "I13",
            "I14",
            "I15",
            "I16",
        ]

        # <--- Create ID's and populate names list --->
        [
            self.COMMA_ID,
            self.SEMICOLON_ID,
            self.DOT_ID,
            self.RIGHT_ARROW_ID,
        ] = self.names.lookup(self.punctuation_list)

        [self.LEFT_BRACKET_ID, self.RIGHT_BRACKET_ID] = self.names.lookup(
            self.bracket_list
        )

        [self.LEFT_CURLY_BRACKET_ID,
            self.RIGHT_CURLY_BRACKET_ID] = self.names.lookup(
                self.curly_bracket_list)

        [
            self.DEVICES_ID,
            self.CONNECT_ID,
            self.MONITOR_ID,
            self.END_ID,
        ] = self.names.lookup(self.keywords_list)

        [self.Q_ID, self.QBAR_ID] = self.names.lookup(
            self.dtype_output_pin_list)

        [self.DATA_ID, self.CLK_ID, self.SET_ID,
            self.CLEAR_ID] = self.names.lookup(self.dtype_pin_list)

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

        [
            self.I1_ID,
            self.I2_ID,
            self.I3_ID,
            self.I4_ID,
            self.I5_ID,
            self.I6_ID,
            self.I7_ID,
            self.I8_ID,
            self.I9_ID,
            self.I10_ID,
            self.I11_ID,
            self.I12_ID,
            self.I13_ID,
            self.I14_ID,
            self.I15_ID,
            self.I16_ID,
        ] = self.names.lookup(self.gates_pin_list)

        self.current_character = ""

        # Opens the definition file
        self.path = path
        self.file = open(path)
        self.file_error = open(path)
        self.logger = logger
        self.logger.info("\nNow reading file...")
        self.logger.info("File name:  " + self.file.name)

    def advance(self, read_error_file=False):
        """Read next character and update current character."""
        self.current_character = self.file.read(1)
        self.current_col += 1
        if self.current_character != "":
            if ord(self.current_character) == 10:  # newline
                self.current_line += 1
                self.current_col = 0

    def skip_spaces(self):
        """Assign next non whitespace character to current character."""
        self.advance()
        while self.current_character.isspace():
            self.advance()

    def get_device_name(self):
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

    def get_capital_name(self):
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

    def get_number(self):
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

    def get_error_line(self, line_num, line_col):
        """Return the line with error and put marker under error column."""
        f = open(self.path)
        data = f.read()
        data = data.split('\n')
        
        output_string = data[line_num - 1]
        white_space = " "

        marker = ""
        for i in range(line_col - 1):
            marker += white_space

        marker += "^"
        output_string += "\n"
        output_string += marker
        return output_string

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        if self.current_col == 0 and self.current_line == 1:
            self.advance()
        symbol = Symbol()
        if self.current_character.isspace():
            self.skip_spaces()  # current character now not whitespace
        self.logger.debug(f"Line: {self.current_line}, Col:{self.current_col}")
        symbol.start_line = self.current_line
        symbol.start_col = self.current_col
        # assignment uses if statements as the sequences of char vary
        # order in assignment matters so carefull when adding new types
        if self.current_character.islower():  # device name
            device_name = self.get_device_name()[0]
            symbol.type = self.DEVICE_NAME
            [symbol.id] = self.names.lookup([device_name])

        elif (
            self.current_character.isalpha() and self.current_character != "I"
        ):  # keyword which is not input pin to a gate of from I1, or I10
            capital_string = self.get_capital_name()[0]
            if capital_string in self.keywords_list:  # keyword
                symbol.type = self.KEYWORD
                [symbol.id] = self.names.lookup([capital_string])
            elif capital_string in self.gate_name_list:  # gatename
                symbol.type = self.GATE_NAME
                [symbol.id] = self.names.lookup([capital_string])
            elif capital_string in self.dtype_output_pin_list:  # output pin
                symbol.type = self.DTYPE_OUTPUT_PIN
                [symbol.id] = self.names.lookup([capital_string])
            elif capital_string in self.dtype_pin_list:  # input pin
                symbol.type = self.DTYPE_INPUT_PIN
                [symbol.id] = self.names.lookup([capital_string])
            else:  # error
                symbol.type = self.ERROR
                [symbol.id] = self.names.lookup([capital_string])

        elif self.current_character == "I":
            self.advance()
            if self.current_character.isdigit():
                symbol.type = self.GATE_PIN
                input_pin_string = "I" + self.get_number()[0]
                [symbol.id] = self.names.lookup([input_pin_string])
            else:
                symbol.type = self.ERROR

        elif self.current_character.isdigit():
            symbol.id = int(self.get_number()[0])
            symbol.type = self.NUMBER

        # punctuation
        elif self.current_character == "=":
            self.advance()  # check if next character satisfies =>
            if self.current_character == ">":
                symbol.type = self.RIGHT_ARROW
                symbol.id = self.RIGHT_ARROW_ID
                self.advance()
            else:
                symbol.type = self.ERROR
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
            symbol.type = self.ERROR
            self.advance()
        try:
            if symbol.type == self.NUMBER:
                self.logger.debug(f"{symbol.type}, {symbol.id}")
            else:
                self.logger.debug(
                    f"{symbol.type}, {self.names.get_name_string(symbol.id)}"
                )
        except BaseException:
            self.logger.debug(f"{symbol.type}, {symbol.id}")

        return symbol
