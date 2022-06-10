"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""

from scanner import Scanner
from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
import logging
import sys
import wx

_ = wx.GetTranslation


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
    parse_network(self): Parses the circuit definition file as per EBNF spec.

    make_monitor(self): Parse the monitor line.

    create_conn(self): Parse connection creation.

    device(self): Parse devices.

    gate_devices(self, device_kind): Parse and create device.

    dtype_devices(self, device_kind): Parse dtype latches.

    xor_devices(self, device_kind): Parse xor gates.

    not_devices(self, device_kind): Parse not gate.

    switch_devices(self, device_kind): Parse switch defenitions.

    clock_devices(self, device_kind): Parse clock devices.

    input_number(self): Parse input numbers.

    device_semantic_error_check(self, error_type): Check if defined devices
                                                   have no semantic erros.

    device_name(self): Parse device names.

    error(self, error_type): Handle errors and skip to next appropriate symbol.



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
        self.error_string = ""  # when new error encountered add $
        self.logger = logger

        self.semantic_error_dict = {
            "INPUT_TO_INPUT": _("Input is connected to an input."),
            "OUTPUT_TO_OUTPUT": _("Output is connected to an output."),
            "INPUT_CONNECTED": _("Input is already connected."),
            "PORT_ABSENT": _("Port accessed is absent."),
            "DEVICE_ABSENT": _("Device accessed is absent."),
            "NOT_OUTPUT": _("Monitoring point is not an output."),
            "MONITOR_PRESENT": _("Monitor is not present."),
            "INVALID_QUALIFIER": _("Qualifier is invalid."),
            "NO_QUALIFIER": _("No qualifier present."),
            "BAD_DEVICE": _("The device kind is incorrect."),
            "QUALIFIER_PRESENT": _("No qualifier should be present."),
            "DEVICE_PRESENT": _("Device already created.")
        }

    def parse_network(self):
        """Parse the circuit definition file."""
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
                "".join((str(self.symbol.type), ",",
                        self.names.get_name_string(self.symbol.id)))
            )

        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.END_ID
        ):
            self.logger.debug("<--- End of file found --->")
        elif self.symbol.type == self.scanner.EOF:
            self.error("MISSING_END_KEYWORD")

        if self.error_count > 0:
            err_msg = str(self.error_count)
            err_msg += _("errors found, please resolve them and try again")
            print(err_msg)
            return False
        else:
            print(_("No Errors found"))
            return True

    def make_monitor(self):
        """Parse the monitor line as per the EBNF spec."""
        if self.symbol.type != self.scanner.DEVICE_NAME:
            self.error("DEVICE_NAME_EXPECTED")
        else:
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

            monitor_return = self.monitors.make_monitor(
                device_id, output_id, cycles_completed=0
            )
            if monitor_return == self.monitors.NOT_OUTPUT:
                self.error("NOT_OUTPUT")
            elif monitor_return == self.monitors.NOT_OUTPUT:
                self.error("MONITOR_PRESENT")

        if self.symbol.type != self.scanner.SEMICOLON:
            self.error("SEMICOLON_EXPECTED")
        else:
            pass
        self.logger.debug("-Monitor point ended")

    def create_conn(self):
        """Parse connection creation as per EBNF spec."""
        if self.symbol.type != self.scanner.DEVICE_NAME:
            self.error("DEVICE_NAME_EXPECTED")
        else:
            first_device_id = self.symbol.id
            first_port_id = None
            self.symbol = self.scanner.get_symbol()

        if self.symbol.type == self.scanner.DOT:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.DTYPE_OUTPUT_PIN:
                first_port_id = self.symbol.id
                self.symbol = self.scanner.get_symbol()
            else:
                self.error("OUTPUT_PIN_EXPECTED")

        if self.symbol.type != self.scanner.RIGHT_ARROW:
            self.error("RIGHT_ARROW_EXPECTED")
        else:
            self.symbol = self.scanner.get_symbol()

        if self.symbol.type != self.scanner.DEVICE_NAME:
            self.error("DEVICE_NAME_EXPECTED")
        else:
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

                if self.error_count == 0:
                    # Make Connection
                    network_return = self.network.make_connection(
                        first_device_id,
                        first_port_id,
                        second_device_id,
                        second_port_id,
                    )
                    if network_return == self.network.INPUT_TO_INPUT:
                        self.error("INPUT_TO_INPUT")
                    elif network_return == self.network.OUTPUT_TO_OUTPUT:
                        self.error("OUTPUT_TO_OUTPUT")
                    elif network_return == self.network.INPUT_CONNECTED:
                        self.error("INPUT_CONNECTED")
                    elif network_return == self.network.PORT_ABSENT:
                        self.error("PORT_ABSENT")
                    elif network_return == self.network.DEVICE_ABSENT:
                        self.error("DEVICE_ABSENT")

            self.symbol = self.scanner.get_symbol()
        if self.symbol.type != self.scanner.SEMICOLON:
            self.error("SEMICOLON_EXPECTED")
        self.logger.debug("-Connection Ended")

    def device(self):
        """Parse devices as per EBNF spec."""
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
        elif self.symbol.id == self.scanner.XOR_ID:
            self.logger.debug("-GATE found, start to parse GATE")
            self.xor_devices(self.symbol.id)
        elif self.symbol.id == self.scanner.NOT_ID:
            self.logger.debug("-GATE founf, start to parse GATE")
            self.not_devices(self.symbol.id)
        else:
            self.error("DEVICE_TYPE_NOT_DECLARED")

    def gate_devices(self, device_kind):
        """Parse and create device."""
        # First Gate
        self.device_name()
        device_id = self.symbol.id

        self.symbol = self.scanner.get_symbol()
        if self.symbol.id != self.scanner.LEFT_BRACKET_ID:
            self.error("LEFT_BRACKET_EXPECTED")
        else:

            self.symbol = self.scanner.get_symbol()

            if self.symbol.type == self.scanner.NUMBER and (
                int(self.symbol.id) in range(1, 17)
            ):
                device_property = self.symbol.id
                self.symbol = self.scanner.get_symbol()
            else:
                # error of invalid input
                self.error("INVALID_INPUT_INITIALISATION")

            if self.symbol.id != self.scanner.RIGHT_BRACKET_ID:
                self.error("RIGHT_BRACKET_EXPECTED")
            else:

                # Create device
                device_return = self.devices.make_device(
                    device_id, device_kind, device_property
                )
                self.device_semantic_error_check(device_return)

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
                    # self.input_number()
                    if self.symbol.type == self.scanner.NUMBER and (
                        int(self.symbol.id) in range(1, 17)
                    ):
                        device_property = self.symbol.id
                        self.symbol = self.scanner.get_symbol()
                    else:
                        # error of invalid input
                        self.error("INVALID_INPUT_INITIALISATION")
                    if not (
                        self.symbol.type == self.scanner.BRACKET
                        and self.symbol.id == self.scanner.RIGHT_BRACKET_ID
                    ):
                        self.error("RIGHT_BRACKET_EXPECTED")
                    else:
                        # Create device
                        device_return = self.devices.make_device(
                            device_id, device_kind, device_property
                        )
                        self.device_semantic_error_check(device_return)
                        self.symbol = self.scanner.get_symbol()  # comma check

        if not self.symbol.type == self.scanner.SEMICOLON:
            self.error("SEMICOLON_EXPECTED")
        self.logger.debug("-End of GATE statement")

    def dtype_devices(self, device_kind):
        """Parse dtype latches."""
        self.device_name()
        device_id = self.symbol.id
        self.symbol = self.scanner.get_symbol()
        while self.symbol.type == self.scanner.COMMA:
            self.device_name()
            self.symbol = self.scanner.get_symbol()
        # Create device
        device_return = self.devices.make_device(
            device_id, device_kind, device_property=None
        )
        self.device_semantic_error_check(device_return)
        if self.symbol.type == self.scanner.SEMICOLON:
            self.logger.debug("-End of DTYPE statement")

        else:
            self.error("SEMICOLON_EXPECTED")

    def xor_devices(self, device_kind):
        """Parse xor gates."""
        self.device_name()
        device_id = self.symbol.id
        self.symbol = self.scanner.get_symbol()
        while self.symbol.type == self.scanner.COMMA:
            self.device_name()
            self.symbol = self.scanner.get_symbol()
        # Create device
        device_return = self.devices.make_device(
            device_id, device_kind, device_property=None
        )
        self.device_semantic_error_check(device_return)
        if self.symbol.type == self.scanner.SEMICOLON:
            self.logger.debug("-End of XOR statement")

        else:
            self.error("SEMICOLON_EXPECTED")

    def not_devices(self, device_kind):
        """Parse not gate."""
        # due to the different nature of NOT gate, it gets it's own parser
        self.device_name()
        device_id = self.symbol.id
        self.symbol = self.scanner.get_symbol()
        while self.symbol.type == self.scanner.COMMA:
            self.device_name()
            self.symbol = self.scanner.get_symbol()
        # Create device
        device_return = self.devices.make_device(
            device_id, device_kind, device_property=None
        )
        self.device_semantic_error_check(device_return)
        if self.symbol.type == self.scanner.SEMICOLON:
            self.logger.debug("-End of XOR statement")

        else:
            self.error("SEMICOLON_EXPECTED")
        # uses same structure as XOR one

    def switch_devices(self, device_kind):
        """Parse switch defenitions."""
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
                device_return = self.devices.make_device(
                    device_id, device_kind, device_property
                )
                self.device_semantic_error_check(device_return)

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
                    device_return = self.devices.make_device(
                        device_id, device_kind, device_property
                    )
                    self.device_semantic_error_check(device_return)

        if not self.symbol.type == self.scanner.SEMICOLON:
            self.error("SEMICOLON_EXPECTED")
        self.logger.debug("-End of SWITCH statement")

    def clock_devices(self, device_kind):
        """Parse clock devices."""
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
                device_return = self.devices.make_device(
                    device_id, device_kind, device_property
                )
                self.device_semantic_error_check(device_return)

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
                        device_return = self.devices.make_device(
                            device_id, device_kind, device_property
                        )
                        self.device_semantic_error_check(device_return)

        if not self.symbol.type == self.scanner.SEMICOLON:
            self.error("SEMICOLON_EXPECTED")

        self.logger.debug("-End of CLOCK statement")

    def input_number(self):
        """Parse input numbers."""
        if self.symbol.type == self.scanner.NUMBER and (
            int(self.symbol.id) in range(1, 17)
        ):
            self.symbol = self.scanner.get_symbol()
        else:
            # error of invalid input
            self.error("INVALID_INPUT_INITIALISATION")

    def device_semantic_error_check(self, error_type):
        """Check if defined devices have no semantic erros."""
        if error_type == self.devices.INVALID_QUALIFIER:
            self.error("INVALID_QUALIFIER")
        elif error_type == self.devices.INVALID_QUALIFIER:
            self.error("INVALID_QUALIFIER")
        elif error_type == self.devices.BAD_DEVICE:
            self.error("BAD_DEVICE")
        elif error_type == self.devices.QUALIFIER_PRESENT:
            self.error("QUALIFIER_PRESENT")
        elif error_type == self.devices.DEVICE_PRESENT:
            self.error("DEVICE_PRESENT")

    def device_name(self):
        """Parse device names."""
        # Identifier EBNF statement implicity defined by DEVICE_NAME type
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.DEVICE_NAME:
            pass
        else:
            self.error("DEVICE_NAME_EXPECTED")

    def error(self, error_type):
        """Handle errors and skip to next appropriate symbol."""
        self.error_count += 1
        self.logger.error(error_type)
        self.logger.error(
            f"""Error location: line:{self.scanner.current_line}
                             column:{self.scanner.current_col}"""
        )
        self.logger.error(
            self.scanner.get_error_line(
                self.scanner.current_line, self.scanner.current_col
            )
        )
        location_txt = (
            _("Error location: line:")
            + str(self.scanner.current_line)
            + _("column:")
            + str(self.scanner.current_col)
            + "$"
        )
        self.error_string += location_txt
        self.error_string += (
            self.scanner.get_error_line(
                self.scanner.current_line, self.scanner.current_col
            )
            + "$"
        )
        if error_type == "LEFT_CURLY_BRACE_EXPECTED":  #
            er_msg = _("Missing '{'")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))
        elif error_type == "RIGHT_CURLY_BRACE_EXPECTED":
            er_msg = _("Missing '}'")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))
            if self.symbol.type == self.scanner.EOF:
                return
            while self.symbol.type != self.scanner.KEYWORD:
                self.symbol = self.scanner.get_symbol()
        elif error_type == "MISSING_END_KEYWORD":
            er_msg = _("Missing END to indicate end of definition file")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))
            sys.exit()
        elif error_type == "DEVICE_NAME_EXPECTED":
            er_msg = _("Device not specified")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))

            while self.symbol.id not in [
                self.scanner.SEMICOLON_ID,
                self.scanner.RIGHT_CURLY_BRACKET_ID,
            ] and self.symbol.type not in [
                self.scanner.EOF,
                self.scanner.KEYWORD,
                self.scanner.DEVICE_NAME,
            ]:
                self.symbol = self.scanner.get_symbol()
        elif error_type == "SEMICOLON_EXPECTED":
            er_msg = _("Semicolon expected at end of line.")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))
            while self.symbol.type not in [
                self.scanner.CURLY_BRACKET,
                self.scanner.KEYWORD,
                self.scanner.EOF,
                self.scanner.SEMICOLON,
            ]:
                self.symbol = self.scanner.get_symbol()
        elif error_type == "OUTPUT_PIN_EXPECTED":
            er_msg = _("Output pin not specified")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))
            while self.symbol.type not in [
                self.scanner.SEMICOLON,
                self.scanner.CURLY_BRACKET,
                self.scanner.EOF,
                self.scanner.KEYWORD,
            ]:
                self.symbol = self.scanner.get_symbol()
        elif error_type == "RIGHT_ARROW_EXPECTED":
            er_msg = _("Right arrow expected to signify connect")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))

        elif error_type in ["INPUT_SPECIFICATION_EXPECTED", "NOT_VALID_INPUT"]:
            er_msg = _("Input expected but no specified")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))
            while self.symbol.type not in [
                self.scanner.SEMICOLON,
                self.scanner.CURLY_BRACKET,
                self.scanner.EOF,
                self.scanner.KEYWORD,
            ]:
                self.symbol = self.scanner.get_symbol()
        elif error_type == "DEVICE_TYPE_NOT_DECLARED":
            er_msg = _("Device type not specified, please specify")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))
            while self.symbol.type not in [
                self.scanner.SEMICOLON,
                self.scanner.CURLY_BRACKET,
                self.scanner.EOF,
                self.scanner.KEYWORD,
            ]:
                self.symbol = self.scanner.get_symbol()

        elif error_type == "LEFT_BRACKET_EXPECTED":
            er_msg = _("'(' expected but not present")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))
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
            er_msg = _("Number of inputs incorrectly configured")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))
            self.symbol = self.scanner.get_symbol()
        elif error_type == "RIGHT_BRACKET_EXPECTED":
            er_msg = _("')' expected at end of initialisaition")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))
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
            er_msg = _("Invalid value of clock cycles")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))
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
            er_msg = _("Invalid state of switch")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))
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
            er_msg = _("Incorrect_input_pin")
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))
            while self.symbol.type not in [
                self.scanner.SEMICOLON,
                self.scanner.CURLY_BRACKET,
                self.scanner.EOF,
                self.scanner.KEYWORD,
            ]:
                self.symbol = self.scanner.get_symbol()
        elif error_type in self.semantic_error_dict:
            er_msg = self.semantic_error_dict[error_type]
            print(er_msg)
            self.error_string += "".join((er_msg, "$"))
        else:
            raise NotImplementedError
