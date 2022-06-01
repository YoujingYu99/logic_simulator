from scanner import Symbol, Scanner
from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
import logging
import sys

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

    def __init__(self, names, devices, network, monitors, scanner, logger):
        """Initialise constants."""
        self.names = names
        self.scanner = scanner
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.success = 1
        self.symbol = ""
        self.error_count = 0
        self.logger = logger

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        # Read first character

        self.symbol = self.scanner.get_symbol()
        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.DEVICES_ID
        ):
            self.logger.debug("<--- Find DEVICES --->")
            self.symbol = self.scanner.get_symbol()
            if (
                self.symbol.type != self.scanner.CURLY_BRACKET
                and self.symbol.id != self.scanner.LEFT_CURLY_BRACKET_ID
            ):
                self.error("LEFT_CURLY_BRACE_EXPECTED")
            else:
                self.symbol = self.scanner.get_symbol()
            self.device()
            self.symbol = self.scanner.get_symbol()

            while (
                (self.symbol.type != self.scanner.CURLY_BRACKET)
                and (self.symbol.id != self.scanner.RIGHT_CURLY_BRACKET_ID)
                and self.symbol.type != self.scanner.KEYWORD
            ):
                self.logger.debug("-- Another device found")
                self.device()
                self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.KEYWORD:
                self.error("RIGHT_CURLY_BRACE_EXPECTED")

        self.symbol = self.scanner.get_symbol()
        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.CONNECT_ID
        ):
            self.logger.debug("<--- Find CONNECT --->")
            self.symbol = self.scanner.get_symbol()
            if (
                self.symbol.type != self.scanner.CURLY_BRACKET
                and self.symbol.id != self.scanner.LEFT_CURLY_BRACKET_ID
            ):
                self.error("LEFT_CURLY_BRACE_EXPECTED")
            else:
                self.logger.debug("-Start first connection")
                self.symbol = self.scanner.get_symbol()

            self.create_conn()
            self.symbol = self.scanner.get_symbol()

            while (self.symbol.type != self.scanner.CURLY_BRACKET) and (
                self.symbol.id != self.scanner.RIGHT_CURLY_BRACKET_ID
                and self.symbol.type != self.scanner.KEYWORD
            ):
                self.logger.debug("-- Another connection found")
                self.create_conn()
                self.symbol = self.scanner.get_symbol()

            if self.symbol.type == self.scanner.KEYWORD:
                self.error("RIGHT_CURLY_BRACE_EXPECTED")
            else:
                self.symbol = self.scanner.get_symbol()

        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.MONITOR_ID
        ):
            self.logger.debug("<--- Find MONITOR --->")
            self.symbol = self.scanner.get_symbol()
            if (
                self.symbol.type != self.scanner.CURLY_BRACKET
                and self.symbol.id != self.scanner.LEFT_CURLY_BRACKET_ID
            ):
                self.error("LEFT_CURLY_BRACE_EXPECTED")
            else:
                self.symbol = self.scanner.get_symbol()
            self.logger.debug("-Start first monitor point")

            self.make_monitor()
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.EOF:
                self.error("RIGHT_CURLY_BRACE_EXPECTED")
                self.error("MISSING_END_KEYWORD")
            while (
                int(self.symbol.id)
                not in [
                    self.scanner.RIGHT_CURLY_BRACKET_ID,
                    self.scanner.END_ID,
                ]
                and self.symbol.type != self.scanner.EOF
            ):
                self.logger.debug("-- Another monitor point found")
                self.make_monitor()
                self.symbol = self.scanner.get_symbol()

        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.END_ID
            or self.symbol.type == self.scanner.EOF
        ):
            self.error("RIGHT_CURLY_BRACE_EXPECTED")
        else:
            self.symbol = self.scanner.get_symbol()
            self.logger.debug(
                f"{self.symbol.type}, {self.names.get_name_string(self.symbol.id)}"
            )

        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.END_ID
        ):
            self.logger.debug("<--- End of file found --->")
        elif self.symbol.type == self.scanner.EOF:
            self.error("MISSING_END_KEYWORD")

        if self.error_count > 0:
            print(
                f"{self.error_count} errors found, please resolve them and try again"
            )
            return False
        else:
            print("No Errors found")
            return True


    def make_monitor(self):
        """
        Function to parse the monitor line as per the EBNF spec
        """
        if self.symbol.type != self.scanner.DEVICE_NAME:
            self.error("DEVICE_NAME_EXPECTED")
        device_id = self.symbol.id
        output_id = None

        self.symbol = self.scanner.get_symbol()
        if int(self.symbol.type) == self.scanner.DOT:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.DTYPE_OUTPUT_PIN:
                output_id = self.symbol.id
                self.symbol = self.scanner.get_symbol()
            else:
                self.error("OUTPUT_PIN_EXPECTED")

        self.monitors.make_monitor(device_id, output_id, cycles_completed=0)

        if self.symbol.type == self.scanner.SEMICOLON:
            pass
        else:
            pass

        if self.symbol.type != self.scanner.SEMICOLON:
            self.error("SEMICOLON_EXPECTED")
        else:
            pass
        self.logger.debug("-Monitor point ended")

    def create_conn(self):
        """
        Method to parse connection creation as per EBNF spec
        """
        if self.symbol.type != self.scanner.DEVICE_NAME:
            self.error("DEVICE_NAME_EXPECTED")
        first_device_id = self.symbol.id
        first_port_id = None
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.DOT:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.output_pin:
                first_port_id = self.symbol.id
                self.scanner.get_symbol()
            else:
                self.error("OUTPUT_PIN_EXPECTED")

        if self.symbol.type != self.scanner.RIGHT_ARROW:
            self.error("RIGHT_ARROW_EXPECTED")
        else:
            self.symbol = self.scanner.get_symbol()

        if self.symbol.type != self.scanner.DEVICE_NAME:
            self.error("DEVICE_NAME_EXPECTED")
        second_device_id = self.symbol.id

        self.symbol = self.scanner.get_symbol()

        if self.symbol.type != self.scanner.DOT:
            self.error("INPUT_SPECIFICATION_EXPECTED")
        else:
            self.symbol = self.scanner.get_symbol()
        if self.symbol.type not in [
            self.scanner.DTYPE_INPUT_PIN,
            self.scanner.GATE_PIN,
        ]:
            self.error("NOT_VALID_INPUT")
        else:
            second_port_id = self.symbol.id

            # Make Connection
            self.network.make_connection(
                first_device_id,
                first_port_id,
                second_device_id,
                second_port_id,
            )

            self.symbol = self.scanner.get_symbol()
        if self.symbol.type != self.scanner.SEMICOLON:
            self.error("SEMICOLON_EXPECTED")
        self.logger.debug("-Connection Ended")

    def device(self):
        """
        Method to parse devices
        """
        if self.symbol.id == self.scanner.CLOCK_ID:
            self.logger.debug("-CLOCK found, start to parse CLOCK")
            self.clock_devices(self.symbol.id)
        elif self.symbol.id == self.scanner.SWITCH_ID:
            self.logger.debug("-SWITCH found, start to parse SWITCH")
            self.switch_devices(self.symbol.id)
        elif self.symbol.id == self.scanner.DTYPE_ID:
            self.logger.debug("-DTYPE found, start to parse DTYPE")
            self.dtype_devices(self.symbol.id)
        elif (
            self.symbol.id == self.scanner.AND_ID
            or self.symbol.id == self.scanner.NAND_ID
            or self.symbol.id == self.scanner.OR_ID
            or self.symbol.id == self.scanner.NOR_ID
        ):
            self.logger.debug("-GATE found, start to parse GATE")
            self.gate_devices(self.symbol.id)
        # elif self.symbol.id == self.XOR_ID:
        #     self.logger.debug("-GATE found, start to parse GATE")
        #     self.xor()
        else:
            self.error("DEVICE_TYPE_NOT_DECLARED")

    def gate_devices(self, device_kind):
        """
        Method to parse and create device.
        """
        # First Gate
        self.device_name()
        device_id = self.symbol.id

        self.symbol = self.scanner.get_symbol()
        if self.symbol.id != self.scanner.LEFT_BRACKET_ID:
            self.error("LEFT_BRACKET_EXPECTED")
        else:

            self.symbol = self.scanner.get_symbol()
            # FIXME type of symbol ID behaves a bit weirdly
            # not sure if this is intentional
            self.input_number()
            device_property = self.symbol.id
            self.symbol = self.scanner.get_symbol()
            if self.symbol.id != self.scanner.RIGHT_BRACKET_ID:
                self.error("RIGHT_BRACKET_EXPECTED")
            else:

                # Create device
                self.devices.make_device(
                    device_id, device_kind, device_property
                )

                # More devices
                self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.COMMA:
            while self.symbol.type == self.scanner.COMMA:
                self.device_name()
                device_id = self.symbol.id
                self.symbol = self.scanner.get_symbol()
                if not (
                    self.symbol.type == self.scanner.BRACKET
                    and self.symbol.id == self.scanner.LEFT_BRACKET_ID
                ):
                    self.error("LEFT_BRACKET_EXPECTED")
                else:
                    self.symbol = self.scanner.get_symbol()
                    self.input_number()
                    device_property = self.symbol.id
                    if not (
                        self.symbol.type == self.scanner.BRACKET
                        and self.symbol.id == self.scanner.RIGHT_BRACKET_ID
                    ):
                        self.error("RIGHT_BRACKET_EXPECTED")
                    else:
                        self.symbol = self.scanner.get_symbol()  # comma check

                # Create device
                self.devices.make_device(
                    device_id, device_kind, device_property
                )

        if not self.symbol.type == self.scanner.SEMICOLON:
            self.error("SEMICOLON_EXPECTED")
        self.logger.debug("-End of GATE statement")

    def dtype_devices(self, device_kind):
        """
        Method to parse dtype latches
        """
        self.device_name()
        device_id = self.symbol.id
        self.symbol = self.scanner.get_symbol()
        while self.symbol.type == self.scanner.COMMA:
            self.device_name()
            self.symbol = self.scanner.get_symbol()
        # Create device
        self.devices.make_device(device_id, device_kind, device_property=None)
        if self.symbol.type == self.scanner.SEMICOLON:
            self.logger.debug("-End of DTYPE statement")

        else:
            self.logger.error("SEMILCOLON_EXPECTED")

    def switch_devices(self, device_kind):
        """
        Method to parse switch defenitions
        """
        # First device
        self.device_name()
        device_id = self.symbol.id

        self.symbol = self.scanner.get_symbol()
        if not (
            self.symbol.type == self.scanner.BRACKET
            and self.symbol.id == self.scanner.LEFT_BRACKET_ID
        ):
            self.error("LEFT_BRACKET_EXPECTED")
        else:
            self.symbol = self.scanner.get_symbol()
            if not (
                self.symbol.type == self.scanner.NUMBER
                and int(self.symbol.id) in range(0, 2)
            ):
                self.error("INVALID_STATE_OF_SWITCH")
            else:
                device_property = self.symbol.id
                self.symbol = self.scanner.get_symbol()
            if not (
                self.symbol.type == self.scanner.BRACKET
                and self.symbol.id == self.scanner.RIGHT_BRACKET_ID
            ):
                self.error("RIGHT_BRACKET_EXPECTED")
            else:
                # Create device
                self.devices.make_device(
                    device_id, device_kind, device_property
                )

                # More devices
                self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.COMMA:
            while self.symbol.type == self.scanner.COMMA:
                self.device_name()
                device_id = self.symbol.id

                self.symbol = self.scanner.get_symbol()
                if not (
                    self.symbol.type == self.scanner.BRACKET
                    and self.symbol.id == self.scanner.LEFT_BRACKET_ID
                ):
                    self.error("LEFT_BRACKET_EXPECTED")
                self.symbol = self.scanner.get_symbol()

                if not (
                    self.symbol.type == self.scanner.NUMBER
                    and (int(self.symbol.id) in range(0, 2))
                ):
                    self.error("INVALID_STATE_OF_SWITCH")
                device_property = self.symbol.id
                self.symbol = self.scanner.get_symbol()
                if not (
                    self.symbol.type == self.scanner.BRACKET
                    and self.symbol.id == self.scanner.RIGHT_BRACKET_ID
                ):
                    self.error("RIGHT_BRACKET_EXPECTED")
                else:
                    self.symbol = self.scanner.get_symbol()  # comma check
                    # Create device
                    self.devices.make_device(
                        device_id, device_kind, device_property
                    )

        if not self.symbol.type == self.scanner.SEMICOLON:
            self.error("SEMICOLON_EXPECTED")
        self.logger.debug("-End of SWITCH statement")

    def clock_devices(self, device_kind):
        """
        Method to parse clock devices
        """
        # First Device
        self.device_name()
        device_id = self.symbol.id

        self.symbol = self.scanner.get_symbol()
        if not (
            self.symbol.type == self.scanner.BRACKET
            and self.symbol.id == self.scanner.LEFT_BRACKET_ID
        ):
            self.error("LEFT_BRACKET_EXPECTED")
        else:
            self.symbol = self.scanner.get_symbol()
            if not (
                self.symbol.type == self.scanner.NUMBER
                and int(self.symbol.id) > 0
            ):
                self.error("INVALID_CYCLE_VALUE")
            device_property = self.symbol.id
            self.symbol = self.scanner.get_symbol()
            if not (
                self.symbol.type == self.scanner.BRACKET
                and self.symbol.id == self.scanner.RIGHT_BRACKET_ID
            ):
                self.error("RIGHT_BRACKET_EXPECTED")
            else:
                # Create device
                self.devices.make_device(
                    device_id, device_kind, device_property
                )

                # More devices
                self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.COMMA:
            while self.symbol.type == self.scanner.COMMA:
                self.device_name()
                device_id = self.symbol.id
                self.symbol = self.scanner.get_symbol()
                if not (
                    self.symbol.type == self.scanner.BRACKET
                    and self.symbol.id == self.scanner.LEFT_BRACKET_ID
                ):
                    self.error("LEFT_BRACKET_EXPECTED")
                else:
                    self.symbol = self.scanner.get_symbol()
                    if not (
                        self.symbol.type == self.scanner.NUMBER
                        and int(self.symbol.id) > 0
                    ):
                        self.error("INVALID_CYCLE_VALUE")
                    device_property = self.symbol.id
                    self.symbol = self.scanner.get_symbol()
                    if not (
                        self.symbol.type == self.scanner.BRACKET
                        and self.symbol.id == self.scanner.RIGHT_BRACKET_ID
                    ):
                        self.error("RIGHT_BRACKET_EXPECTED")
                    else:
                        self.symbol = self.scanner.get_symbol()  # comma check

                        # Create device
                        self.devices.make_device(
                            device_id, device_kind, device_property
                        )

        if not self.symbol.type == self.scanner.SEMICOLON:
            self.error("SEMICOLON_EXPECTED")

        self.logger.debug("-End of CLOCK statement")

    # def output_pin(self):
    #     """
    #     Method to parse output pins
    #     """
    #     if self.symbol == self.scanner.Q:
    #         self.symbol = self.scanner.getsymbol()
    #     elif self.symbol == self.scanner.QBAR:
    #         self.symbol = self.scanner.getsymbol()
    #     else:
    #         # output pin specified but not describes
    #         self.error("OUTPUT_PIN_NOT_DESCRIBED")

    # def input_pin(self):
    #     if self.symbol == self.scanner.I:
    #         self.symbol = self.scanner.getsymbol()
    #         self.input_number()
    #     elif (
    #         self.symbol.type == self.scanner.KEYWORDS
    #         and self.symbol.id == self.scanner.DATA_ID
    #     ):
    #         self.symbol = self.scanner.getsymbol()
    #     elif (
    #         self.symbol.type == self.scanner.KEYWORDS
    #         and self.symbol.id == self.scanner.CLK_ID
    #     ):
    #         self.symbol = self.scanner.getsymbol()
    #     elif (
    #         self.symbol.type == self.scanner.KEYWORDS
    #         and self.symbol.id == self.scanner.SET_ID
    #     ):
    #         self.symbol = self.scanner.getsymbol()
    #     elif (
    #         self.symbol.type == self.scanner.KEYWORDS
    #         and self.symbol.id == self.scanner.CLEAR_ID
    #     ):
    #         self.symbol = self.scanner.getsymbol()
    #     else:
    #         # unknown symbol or not specified
    #         self.error("UNKOWN_SYMBOL")

    def input_number(self):
        if self.symbol.type == self.scanner.NUMBER and (
            int(self.symbol.id) in range(1, 17)
        ):
            self.symbol = self.scanner.get_symbol()
        else:
            # error of invalid input
            self.error("INVALID_INPUT_INITIALISATION")

    # def on_off(self):
    #     """
    #     Method to parse on/off parameter
    #     """
    #     if self.symbol == self.scanner.ZERO:
    #         self.symbol = self.scanner.getsymbol()
    #     elif self.symol == self.scanner.ONE:
    #         self.symbol = self.scanner.getsymbol()
    #     else:
    #         # error: 0 or 1 expected
    #         self.error("0_OR_1_EXPECTED")

    def device_name(self):
        """
        Method to parse device names
        """
        # Identifier EBNF statement implicity defined by DEVICE_NAME type
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.DEVICE_NAME:
            pass
        else:
            self.error("DEVICE_NAME_EXPECTED")

    def error(self, error_type):
        """
        Method to handle errors and skip to next appropriate symbol"
        """
        self.error_count += 1
        self.logger.error(error_type)
        self.logger.error(
            f"""Error location: line:{self.scanner.current_line}
                             column:{self.scanner.current_col}"""
        )
        if error_type == "LEFT_CURLY_BRACE_EXPECTED":
            print("Missing '{'")
        elif error_type == "RIGHT_CURLY_BRACE_EXPECTED":
            print("Missing '}'")
            if self.symbol.type == self.scanner.EOF:
                return
            while self.symbol.type != self.scanner.KEYWORD:
                self.symbol = self.scanner.get_symbol()
        elif error_type == "MISSING_END_KEYWORD":
            print("Missing END to indicate end of definition file")
            sys.exit()
        elif error_type == "DEVICE_NAME_EXPECTED":
            print("Device output to monitor not specified")
            while self.symbol.id not in [
                self.scanner.SEMICOLON_ID,
                self.scanner.RIGHT_CURLY_BRACKET_ID,
            ] and self.symbol.type not in [
                self.scanner.EOF,
                self.scanner.KEYWORD,
            ]:
                self.symbol = self.scanner.get_symbol()
        elif error_type == "SEMICOLON_EXPECTED":
            print("Semicolon expected at end of line.")
            while self.symbol.type not in [
                self.scanner.CURLY_BRACKET,
                self.scanner.KEYWORD,
                self.scanner.EOF,
                self.scanner.SEMICOLON,
            ]:
                self.symbol = self.scanner.get_symbol()
        elif error_type == "OUTPUT_PIN_EXPECTED":
            print("Output pin not specified")
            while self.symbol.type not in [
                self.scanner.SEMICOLON,
                self.scanner.CURLY_BRACKET,
                self.scanner.EOF,
                self.scanner.KEYWORD,
            ]:
                self.symbol = self.scanner.get_symbol()
        elif error_type == "RIGHT_ARROW_EXPECTED":
            print("Right arrow expected to signify connect")

        elif error_type in ["INPUT_SPECIFICATION_EXPECTED", "NOT_VALID_INPUT"]:
            print("Input expected but no specified")
            while self.symbol.type not in [
                self.scanner.SEMICOLON,
                self.scanner.CURLY_BRACKET,
                self.scanner.EOF,
                self.scanner.KEYWORD,
            ]:
                self.symbol = self.scanner.get_symbol()
        elif error_type == "DEVICE_TYPE_NOT_DECLARED":
            print("Device type not specified, please specify")
            while self.symbol.type not in [
                self.scanner.SEMICOLON,
                self.scanner.CURLY_BRACKET,
                self.scanner.EOF,
                self.scanner.KEYWORD,
            ]:
                self.symbol = self.scanner.get_symbol()

        elif error_type == "LEFT_BRACKET_EXPECTED":
            print("'(' expected but not present")
            while self.symbol.type not in [
                self.scanner.SEMICOLON,
                self.scanner.CURLY_BRACKET,
                self.scanner.EOF,
                self.scanner.KEYWORD,
                self.scanner.DEVICE_NAME,
                self.scanner.COMMA,
            ]:
                self.symbol = self.scanner.get_symbol()
        elif error_type == "INVALID_INPUT_INITIALISATION":
            print("Number of inputs incorrectly configured")
            self.symbol = self.scanner.get_symbol()
        elif error_type == "RIGHT_BRACKET_EXPECTED":
            print("')' expected at end of initialisaition")
            while self.symbol.type not in [
                self.scanner.SEMICOLON,
                self.scanner.CURLY_BRACKET,
                self.scanner.EOF,
                self.scanner.KEYWORD,
                self.scanner.DEVICE_NAME,
                self.scanner.COMMA,
            ]:
                self.symbol = self.scanner.get_symbol()
        elif error_type == "INVALID_CYCLE_VALUE":
            print("Invalid value of clock cycles")
            while self.symbol.type not in [
                self.scanner.SEMICOLON,
                self.scanner.CURLY_BRACKET,
                self.scanner.EOF,
                self.scanner.KEYWORD,
                self.scanner.DEVICE_NAME,
                self.scanner.COMMA,
                self.scanner.BRACKET,
            ]:
                self.symbol = self.scanner.get_symbol()
        elif error_type == "INVALID_STATE_OF_SWITCH":
            print("Invalid state of switch")
            while self.symbol.type not in [
                self.scanner.SEMICOLON,
                self.scanner.CURLY_BRACKET,
                self.scanner.EOF,
                self.scanner.KEYWORD,
                self.scanner.DEVICE_NAME,
                self.scanner.COMMA,
                self.scanner.BRACKET,
            ]:
                self.symbol = self.scanner.get_symbol()
        elif error_type == "UNKNOWN_INPUT":
            print("Incorrect_input_pin")
            while self.symbol.type not in [
                self.scanner.SEMICOLON,
                self.scanner.CURLY_BRACKET,
                self.scanner.EOF,
                self.scanner.KEYWORD,
            ]:
                self.symbol = self.scanner.get_symbol()
        else:
            raise NotImplementedError


# configure the loggers, they should always be configured in top level file and
# then passed into the following classes so that the level can be configured

# Uncomment to run

path_definition = "definitions/circuit.def"
scanner_logger = logging.getLogger("scanner")
parser_logger = logging.getLogger("parser")
logging.basicConfig(level=logging.DEBUG)

names_instance = Names()
scanner_instance = Scanner(path_definition, names_instance, scanner_logger)
device_instance = Devices(names_instance)
network_instance = Network(names_instance, device_instance)
monitor_instance = Monitors(names_instance, device_instance, network_instance)

parser_1 = Parser(
    names_instance,
    device_instance,
    network_instance,
    monitor_instance,
    scanner_instance,
    parser_logger,
)

a = parser_1.parse_network()
print('--Check all devices have been created')
print(parser_1.devices.find_devices())
print(parser_1.devices.get_device(42).inputs) # This is the DTYPE device
print(parser_1.devices.get_device(42).outputs) # DTYPE 
print(parser_1.devices.get_device(46).inputs)


print('--Check all network inputs are satisfied')
print(parser_1.network.check_network())


monitored_signal_list, non_monitored_signal_list = parser_1.monitors.get_signal_names()

print('--List monitor points')
print(monitored_signal_list)

parser_1.monitors.display_signals()
