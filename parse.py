#########
# these are temp imports for development
from unittest.mock import Mock
from scanner import Symbol

#########


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
            if self.symbol.type == self.__scanner.DOT:
                self.output_pin()
            self.symbol = self.scanner.getsymbol()
            if self.symbol.type == self.scanner.SEMICOLON:
                # TODO decide how ot do return properly
                self.symbol = self.scanner.getsymbol()
                return 1
            else:
                # TODO sort out proper error handling and display
                self.error()

        def create_conn():
            """
            Function to parse connection creation as per EBNF spec
            """
