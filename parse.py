#########
# these are temp imports for development
from unittest.mock import Mock
from scanner import Symbol

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

    def __init__(self, names, devices, network, monitors, scanner):
        """Initialise constants."""
        self.__names = names
        self.scanner = scanner
        self.success = 1

    # note, this is yet to be tested in combination with the scanner, mocking is used for symbols atm
    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.

        if (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.DEVICES_ID
        ):
            self.symbol = self.scanner.getsymbol()
            self.device()
            while self.symbol.type != self.scanner.ENDBRACK:
                self.symbol = self.scanner.getsymbol()
                self.device()
            self.symbol = self.scanner.getsymbol()

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
            self.error()

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
            # TODO sort out proper error handling and display
            self.error()

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
                self.error()
            if self.symbol == self.scanner.SEMICOLON:
                self.symbol = self.scanner.getsymbol()
                return 1
            else:
                # line non terminated error
                self.error()
        else:
            # error: connection symbol expected
            self.error()

    def device(self):
        """
        Method to parse devices
        TODO this
        """

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
            self.error()
        if self.symbol == self.scanner.RIGHTBRACK:
            self.symbol = self.scanner.getsymbol()
        else:
            # syntax error
            self.error()
        while self.symbol == self.scanner.COMA:
            # same code as above, just repeated
            self.symbol = self.scanner.getsymbol()
            self.device_name()
            if self.symbol == self.scanner.LEFTBRACK:
                self.input_number()
            else:
                # syntax error, "(" expected
                self.error()
            if self.symbol == self.scanner.RIGHTBRACK:
                self.symbol = self.scanner.getsymbol()
            else:
                # syntax error
                self.error()
        if self.symbol == self.scanner.SEMICOLON:
            self.symbol = self.scanner.getsymbol()
            return 1
        else:
            self.error()

    def dtype_devices(self):
        """
        Method to parse dtype latches
        """
        if (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.DTYPE_ID
        ):
            self.device_name()
            while self.symbol == self.scanner.COMA:
                self.symbol = self.scanner.getsymbol()
                self.device_name()
            if self.symbol == self.scanner.SEMICOLON:
                self.symbol = self.scanner.getsymbol()
                return 1
            else:
                # error, semicolon expected
                self.error()
        else:
            # error, codeword DTYPE expected
            self.error()

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
                self.error()
            self.on_off()
            if self.symbol == self.scanner.RIGHTBRACK:
                self.symbol = self.scanner.getsymbol()
            else:
                # syntax error
                self.error()
            while self.symbol == self.scanner.COMA:
                self.symbol = self.scanner.getsymbol()
                self.device_name()
                if self.symbol == self.scanner.LEFTBRACK:
                    self.symbol = self.scanner.getsymbol()
                else:
                    # syntax error, missing braket
                    self.error()
                self.on_off()
                if self.symbol == self.scanner.RIGHTBRACK:
                    self.symbol = self.scanner.getsymbol()
                else:
                    # syntax error
                    self.error()
            else:
                # error, no codeword
                self.error()

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
                self.error()
            self.non_zero()
            while self.symbol != self.scanner.LEFTBRACK:
                self.digit()
            if self.symbol == self.scanner.LEFTBRACK:
                self.symbol = self.scanner.getsymbol()
            else:
                # error, bracket not closed
                self.error()

            while self.symbol == self.scanner.COMA:
                self.symbol = self.getsymbol()

                self.device_name()

                if self.symbol == self.scanner.LEFTBRACK:
                    self.symbol = self.scanner.getsymbol()
                else:
                    # error, backet expected
                    self.error()
                self.non_zero()
                while self.symbol != self.scanner.LEFTBRACK:
                    self.digit()
                if self.symbol == self.scanner.LEFTBRACK:
                    self.symbol = self.scanner.getsymbol()
                else:
                    # error, bracket not closed
                    self.error()

            if self.symbol == self.scanner.SEMICOLON:
                self.symbol = self.scanner.getsymbol()
                return 1
            else:
                # error, semicolon expected
                self.error()

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
            self.error()

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
            self.error()

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
            self.error()

    def input_number(self):
        input_num_list = [
            self.scanner.ONE,
            self.scanner.TWO,
            self.scanner.THREE,
            self.scanner.FOUR,
            self.scanner.FIVE,
            self.scanner.SIX,
            self.scanner.SEVEN,
            self.scanner.EIGHT,
            self.scanner.NINE,
            self.scanner.TEN,
            self.scanner.ELEVEN,
            self.scanner.TWELVE,
            self.scanner.THIRTEEN,
            self.scanner.FOURTEEN,
            self.scanner.FIFTEEN,
            self.scanner.SIXTEEN,
        ]
        # other ways to do it, depending on the scanner
        if self.symbol.type in input_num_list:
            self.symbol = self.scanner.getsymbol()
            return 1
        else:
            # error of invalid input
            self.error()
