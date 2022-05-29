#########
# these are temp imports for development
from unittest.mock import Mock
from scanner import Symbol, Scanner
from names import Names

#########
## TODO: implement errors and returns from them

"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""


class Parser:

    """Parse the definition file and build the logic network.

    The parser deals with error handling. It analyses the syntactic and
    semantic correctness of the symbols it receives from the scanner, and
    then builds the logic network. If there are errors in the definition file,
    the parser detects this and tries to recover from it, giving helpful
    error messages.

    Parameters
    ----------
    names: instance of the names.Names() class.
    devices: instance of the devices.Devices() class.
    network: instance of the network.Network() class.
    monitors: instance of the monitors.Monitors() class.
    scanner: instance of the scanner.Scanner() class.

    Public methods
    --------------
    parse_network(self): Parses the circuit definition file.
    """
    # def __init__(self, names, devices, network, monitors, scanner):
    def __init__(self, names, scanner):
        """Initialise constants."""
        self.__names = names
        self.scanner = scanner
        self.success = 1
        self.symbol  = ""
        self.error_count = 0

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.

        # Read first character
        self.scanner.advance()

        # Run to parse whole file and print outputs
        # for i in range(70):
        #     symbol1 = self.scanner.get_symbol()
        #     if symbol1.type == 15:
        #         break
        #     print("ID, string")
        #     print(symbol1.type)
        #     print("---")

        self.symbol = self.scanner.get_symbol()
        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.DEVICES_ID
        ):
            self.device()
            while self.symbol.type != self.scanner.ENDBRACK:
                self.symbol = self.scanner.getsymbol()
                self.device()
            self.symbol = self.scanner.getsymbol()

        """


        elif (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.CONNECT_ID
        ):
            self.symbol = self.scanner.getsymbol()
            self.make_connection()
            while self.symbol.type != self.scanner.ENDBRACK:
                self.symbol = self.scanner.getsymbol()
                self.scanner.make_connection()
            self.symbol = self.scanner.getsymbol()

        elif (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.MONITOR_ID
        ):
            self.symbol = self.scanner.getsymbol()
            self.make_monitor()
            while self.symbol.type != self.scanner.ENDBRACK:
                self.symbol = self.scanner.getsymbol()
                self.make_monitor()
            self.symbol - self.scanner.getsymbol()

        elif self.symbol.type == self.scanner.ENDBRACK:
            self.symbol = self.scanner.getsymbol()

        elif (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.END
        ):
            return 1 if self.success else 0
        else:
            # issue in network syntax, double check the file
            self.error("NETWORK_SYNTAX_ERROR")
        """

    def make_monitor(self):
        """
        Fucntion to parse the monitor line as per the EBNF spec
        """
        self.device_name()
        if self.symbol.type == self.scanner.DOT:
            self.output_pin()
        self.symbol = self.scanner.getsymbol()
        if self.symbol.type == self.scanner.SEMICOLON:
            # TODO decide how ot do return properly
            self.symbol = self.scanner.getsymbol()
            return 1
        else:
            # error, semicolon expected to end statement
            self.error("SEMICOLON_EXPECTED_AT_LINE_END")

    def create_conn(self):
        """
        Method to parse connection creation as per EBNF spec
        """
        self.device_name()
        if self.symbol == self.scanner.DOT:
            self.output_pin()
        if self.symbol == self.scanner.CONN:
            self.symbol = self.scanner.getsymbol()
            if self.symbol == self.scanner.DOT:
                self.input_pin()
            else:
                # error due to lack of input reference
                self.error("NO_INPUT_REFERENCE")
            if self.symbol == self.scanner.SEMICOLON:
                self.symbol = self.scanner.getsymbol()
                return 1
            else:
                # line non terminated error
                self.error("SEMICOLON_EXPECTED_AT_LINE_END")
        else:
            # error: connection symbol expected
            self.error("CONNECTION_SYMBOL_EXPECTED")

    def device(self):
        """
        Method to parse devices
        TODO this
        """
        # TODO: complete this 
        self.symbol = self.scanner.get_symbol()
        
        if (self.symbol.type == self.scanner.CURLY_BRACKET 
            and self.symbol.id == self.scanner.LEFT_CURLY_BRACKET_ID
        ):
            pass

        self.symbol = self.scanner.get_symbol()

        if self.symbol.id == self.scanner.CLOCK_ID:
            self.clock_devices()
        elif self.symbol.id == self.scanner.SWITCH_ID:
            self.switch_devices()
        elif self.symbol.id == self.scanner.DTYPE_ID:
            print('pass')
            self.dtype_devices()
        elif self.symbol.id == (self.gate_devices or
            self.AND_ID or
            self.NAND_ID or
            self.OR_ID or
            self.NOR_ID or
            self.DTYPE_ID or
            self.XOR_ID):
            self.gate_devices()


        
        
        


        

    def gate_devices(self):
        """
        Method to parse gates
        """
        self.gatename()
        self.device_name()
        if self.symbol == self.scanner.LEFTBRACK:
            self.input_number()
        else:
            # syntax error, "(" expected
            self.error("LEFTBRACKET_EXPECTED")
        if self.symbol == self.scanner.RIGHTBRACK:
            self.symbol = self.scanner.getsymbol()
        else:
            # syntax error
            self.error("RIGHTBRACKET_EXPECTED")
        while self.symbol == self.scanner.COMA:
            # same code as above, just repeated
            self.symbol = self.scanner.getsymbol()
            self.device_name()
            if self.symbol == self.scanner.LEFTBRACK:
                self.input_number()
            else:
                # syntax error, "(" expected
                self.error("LEFTBRACKET_EXPECTED")
            if self.symbol == self.scanner.RIGHTBRACK:
                self.symbol = self.scanner.getsymbol()
            else:
                # syntax error
                self.error("RIGHTBRACKET_EXPECTED")
        if self.symbol == self.scanner.SEMICOLON:
            self.symbol = self.scanner.getsymbol()
            return 1
        else:
            # error: semicolon expected
            self.error("SEMICOLON_EXPECTED_AT_LINE_END")

    def dtype_devices(self):
        """
        Method to parse dtype latches
        """
        self.symbol = self.scanner.get_symbol()
        if (
            self.symbol.type == self.scanner.GATE_NAME
            and self.symbol.id == self.scanner.DTYPE_ID
        ):
            print('pass 2')
            self.device_name()
            while self.symbol == self.scanner.COMA:
                self.symbol = self.scanner.getsymbol()
                self.device_name()
            if self.symbol == self.scanner.SEMICOLON:
                self.symbol = self.scanner.getsymbol()
                return 1
            else:
                # error, semicolon expected
                self.error("SEMICOLON_EXPECTED_AT_LINE_END")
        else:
            # error, codeword DTYPE expected
            self.error("CODEWORD_EXPECTED")

    def switch_devices(self):
        """
        Method to parse switch defenitions
        """
        if (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.SWITCH_ID
        ):
            self.symbol = self.scanner.getsymbol()
            self.device_name()
            if self.symbol == self.scanner.LEFTBRACK:
                self.symbol = self.scanner.getsymbol()
            else:
                # syntax error, missing braket
                self.error("LEFTBRACKET_EXPECTED")
            self.on_off()
            if self.symbol == self.scanner.RIGHTBRACK:
                self.symbol = self.scanner.getsymbol()
            else:
                # syntax error
                self.error("RIGHTBRACKET_EXPECTED")
            while self.symbol == self.scanner.COMA:
                self.symbol = self.scanner.getsymbol()
                self.device_name()
                if self.symbol == self.scanner.LEFTBRACK:
                    self.symbol = self.scanner.getsymbol()
                else:
                    # syntax error, missing braket
                    self.error("LEFTBRACKET_EXPECTED")
                self.on_off()
                if self.symbol == self.scanner.RIGHTBRACK:
                    self.symbol = self.scanner.getsymbol()
                else:
                    # syntax error
                    self.error("RIGHTBRACKET_EXPECTED")
            else:
                # error, no codeword
                self.error("CODEWORD_EXPECTED")

    def clock_devices(self):
        """
        Method to parse clock devices
        """
        if (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.CLOCK_ID
        ):
            self.symbol = self.scanner.getsymbol()
            self.device_name()

            if self.symbol == self.scanner.LEFTBRACK:
                self.symbol = self.scanner.getsymbol()
            else:
                # error, backet expected
                self.error("LEFTBRACKET_EXPECTED")
            self.non_zero()
            while self.symbol != self.scanner.LEFTBRACK:
                self.digit()
            if self.symbol == self.scanner.LEFTBRACK:
                self.symbol = self.scanner.getsymbol()
            else:
                # error, bracket not closed
                self.error("RIGHTBRACKET_EXPECTED")

            while self.symbol == self.scanner.COMA:
                self.symbol = self.getsymbol()

                self.device_name()

                if self.symbol == self.scanner.LEFTBRACK:
                    self.symbol = self.scanner.getsymbol()
                else:
                    # error, backet expected
                    self.error("RIGHTBRACKET_EXPECTED")
                self.non_zero()
                while self.symbol != self.scanner.RIGHTBRACK:
                    self.digit()
                if self.symbol == self.scanner.RIGHTBRACK:
                    self.symbol = self.scanner.getsymbol()
                else:
                    # error, bracket not closed
                    self.error("RIGHTBRACKET_EXPECTED")

            if self.symbol == self.scanner.SEMICOLON:
                self.symbol = self.scanner.getsymbol()
                return 1
            else:
                # error, semicolon expected
                self.error("SEMICOLON_EXPECTED_AT_LINE_END")

    def gatename(self):
        """
        Method to parse gate name titles
        """
        if (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.AND_ID
        ):
            self.symbol = self.getsymbol()
            return 1
        elif (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.NAND_ID
        ):
            self.symbol = self.scanner.getsymbol()
            return 1
        elif (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.OR_ID
        ):
            self.symbol = self.scanner.getsymbol()
            return 1
        elif (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.NOR_ID
        ):
            self.symbol = self.scanner.getsymbol()
            return 1
        else:
            # error, not a valid gate name
            self.error("GATE_NAME_INVALID")

    def output_pin(self):
        """
        Method to parse output pins
        """
        if self.symbol == self.scanner.Q:
            self.symbol = self.scanner.getsymbol()
            return 1
        elif self.symbol == self.scanner.QBAR:
            self.symbol = self.scanner.getsymbol()
            return 1
        else:
            # output pin specified but not describes
            self.error("OUTPUT_PIN_NOT_DESCRIBED")

    def input_pin(self):
        if self.symbol == self.scanner.I:
            self.symbol = self.scanner.getsymbol()
            self.input_number()
            return 1
        elif (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.DATA_ID
        ):
            self.symbol = self.scanner.getsymbol()
            return 1
        elif (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.CLK_ID
        ):
            self.symbol = self.scanner.getsymbol()
            return 1
        elif (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.SET_ID
        ):
            self.symbol = self.scanner.getsymbol()
            return 1
        elif (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.CLEAR_ID
        ):
            self.symbol = self.scanner.getsymbol()
            return 1
        else:
            # unknown symbol or not specified
            self.error("UNKOWN_SYMBOL")

    def input_number(self):
        if self.symbol.type in self.scaner.INPUTNUM:
            self.symbol = self.scanner.getsymbol()
            return 1
        else:
            # error of invalid input
            self.error("NUMBER_OF_INPUTS_INVALID")

    def on_off(self):
        """
        Method to parse on/off parameter
        """
        if self.symbol == self.scanner.ZERO:
            self.symbol = self.scanner.getsymbol()
            return 1
        elif self.symol == self.scanner.ONE:
            self.symbol = self.scanner.getsymbol()
            return 1
        else:
            # error: 0 or 1 expected
            self.error("0_OR_1_EXPECTED")

    def device_name(self):
        """
        Method to parse device names
        """
        if self.symbol.type == self.scanner.KEYWORDS:
            # error ketword cannon be an indentifier
            self.error("KEYWORD_CANNOT_BE_IDENTIFIER")
        else:
            self.identifier()

    def identifier(self):
        """
        Function to handle parseing of identifiers
        """
        if self.symbol[0] != self.scanner.LOWERLETTER:
            # error idenitifies myst start with a lowercase lower_letter
            self.error("IDENTIFIERS_START_WITH_LOWERCASE")
        elif any(
            char not in self.scanner.LETTER or char not in self.scanner.DIGIT
            for char in self.symbol
        ):
            # error unexpected symbol
            self.error("UNEXPECTED_SYMBOL")
        else:
            return 1

    def error(self, error_type):
        self.error_cound += 1


path_definition = "definitions/circuit.def"

names_instance = Names()

scanner_instance = Scanner(path_definition, names_instance)

parser_1 = Parser(names_instance, scanner_instance)

a = parser_1.parse_network()
